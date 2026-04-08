"""
multimodal_extractor.py — VLM-based multimodal extraction.

Process each SectionChunk through the VLM to extract ALL protocol semantics.
No pre-classification or early filtering — the VLM decides what's relevant.

For each chunk, sends:
  - merged .md text
  - extracted HTML tables
  - image references with captions
  - surrounding context

The VLM interprets text + tables + images jointly and returns structured data.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from llm_client import InferenceClient, _extract_json
from section_processor import SectionChunk


# ═══════════════════════════════════════════════════════════════════════════
# System prompt
# ═══════════════════════════════════════════════════════════════════════════

_SYSTEM_PROMPT = """\
You are an expert in ISO 15118-20 (Vehicle-to-Grid Communication Interface).
You extract structured protocol semantics from spec content including text, tables, and images.

RULES:
- Extract ALL protocol-relevant information, not just AC-specific
- Preserve ISO variable and message names EXACTLY (e.g. ResponseCode, EVSEProcessing)
- Do NOT invent or rename variables
- Distinguish normative requirements ([V2G20-xxxx] SHALL/MUST) from informative text
- Tables may contain ANYTHING: variables, constraints, enums, timing, schemas
- Images may contain ANYTHING: examples, flows, constraints, state diagrams
- Return valid JSON only, no markdown fences or commentary
"""


# ═══════════════════════════════════════════════════════════════════════════
# Extraction prompt — unified for all content types
# ═══════════════════════════════════════════════════════════════════════════

_EXTRACT_PROMPT = """\
Analyze this ISO 15118-20 spec content and extract ALL protocol semantics.

SECTION: {clause_id} — {title}
PAGES: {pages}

=== TEXT CONTENT ===
{text_content}

{table_section}

{image_section}

Extract and return a JSON object with these categories. Include ALL items found.
Empty arrays for categories with no content.

{{
  "messages": [
    {{"name": "MessageName", "direction": "request|response", "description": "..."}}
  ],
  "field_definitions": [
    {{"message": "MsgName", "field": "FieldName", "type": "TypeName", "mandatory": true|false, "description": "...", "allowed_values": ["..."]}}
  ],
  "variables": [
    {{"name": "ISOVarName", "domain": ["val1", "val2"], "description": "..."}}
  ],
  "guards": [
    {{"expr": "VarName = Value", "actor": "EVCC|SECC|BOTH", "applies_to_messages": ["..."], "source_req": "V2G20-xxxx"}}
  ],
  "actions": [
    {{"expr": "send MsgReq", "actor": "EVCC|SECC", "applies_to_messages": ["..."], "source_req": "V2G20-xxxx"}}
  ],
  "response_codes": [
    {{"message": "MsgRes", "valid_codes": ["OK", "FAILED_...", "WARNING_..."]}}
  ],
  "timing_constraints": [
    {{"timer_name": "V2G_EVCC_Msg_Timeout", "applies_to": ["MsgReq"], "value_seconds": 2.0, "actor": "EVCC|SECC|BOTH", "source_req": "V2G20-xxxx"}}
  ],
  "sequence_constraints": [
    {{"condition": "ResponseCode = OK", "current_message": "MsgRes", "next_allowed": ["NextMsgReq"], "actor": "EVCC", "source_req": "V2G20-xxxx"}}
  ],
  "invariants": [
    {{"expr": "condition", "scope": "state|session|global", "applies_to_states": ["..."], "source_req": "V2G20-xxxx"}}
  ],
  "field_constraints": [
    {{"field": "FieldName", "message": "MsgName", "allowed_values": ["..."], "mandatory": true|false, "source_req": "V2G20-xxxx"}}
  ],
  "enumerations": [
    {{"type_name": "TypeName", "values": ["val1", "val2", ...], "description": "..."}}
  ]
}}
"""


# ═══════════════════════════════════════════════════════════════════════════
# Chunk splitting for large sections
# ═══════════════════════════════════════════════════════════════════════════

_MAX_CHUNK_CHARS = 6000  # VLM context budget per call


def _split_text_into_chunks(text: str, max_chars: int = _MAX_CHUNK_CHARS) -> list[str]:
    """
    Split long text into chunks at paragraph boundaries.
    Keeps semantic units together.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    paragraphs = re.split(r'\n\n+', text)
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current)
            current = para
        else:
            current = current + "\n\n" + para if current else para

    if current:
        chunks.append(current)

    return chunks


# ═══════════════════════════════════════════════════════════════════════════
# Result merging
# ═══════════════════════════════════════════════════════════════════════════

ALL_CATEGORIES = [
    "messages", "field_definitions", "variables", "guards", "actions",
    "response_codes", "timing_constraints", "sequence_constraints",
    "invariants", "field_constraints", "enumerations",
]

# ═══════════════════════════════════════════════════════════════════════════
# VLM output schema validation
# ═══════════════════════════════════════════════════════════════════════════

# Required keys per category — items missing required keys are logged and dropped
_REQUIRED_KEYS: dict[str, list[str]] = {
    "messages":              ["name"],
    "field_definitions":     ["message", "field"],
    "variables":             ["name"],
    "guards":                ["expr"],
    "actions":               ["expr"],
    "response_codes":        ["message", "valid_codes"],
    "timing_constraints":    ["timer_name"],
    "sequence_constraints":  ["current_message", "next_allowed"],
    "invariants":            ["expr"],
    "field_constraints":     ["field"],
    "enumerations":          ["type_name", "values"],
}

_vlm_validation_log: list[dict] = []


def get_vlm_validation_log() -> list[dict]:
    """Return the VLM validation log for audit."""
    return _vlm_validation_log


def _validate_vlm_item(category: str, item: dict, source: str = "") -> bool:
    """Validate a single VLM output item against schema. Logs failures."""
    if not isinstance(item, dict):
        _vlm_validation_log.append({
            "category": category, "source": source,
            "reason": "not a dict", "item": str(item)[:200],
        })
        return False

    required = _REQUIRED_KEYS.get(category, [])
    missing = [k for k in required if not item.get(k)]
    if missing:
        _vlm_validation_log.append({
            "category": category, "source": source,
            "reason": f"missing required keys: {missing}",
            "item": {k: item.get(k, "") for k in required},
        })
        return False

    return True


def _ensure_confidence(item: dict, category: str) -> None:
    """Ensure every item has a confidence field, defaulting to 0.5."""
    if "confidence" not in item:
        item["confidence"] = 0.5


def merge_results(results: list[dict], source: str = "") -> dict:
    """Merge multiple VLM extraction results, deduplicating by content.
    Validates each item and ensures confidence field."""
    merged = {cat: [] for cat in ALL_CATEGORIES}
    seen = set()

    for result in results:
        if not isinstance(result, dict):
            continue
        for cat in ALL_CATEGORIES:
            items = result.get(cat, [])
            if not isinstance(items, list):
                continue
            for item in items:
                if not _validate_vlm_item(cat, item, source=source):
                    continue
                _ensure_confidence(item, cat)
                key = _dedup_key(cat, item)
                if key and key in seen:
                    continue
                if key:
                    seen.add(key)
                merged[cat].append(item)

    return merged


def _dedup_key(category: str, item: dict) -> str:
    if category in ("guards", "actions", "invariants"):
        return f"{category}:{item.get('expr', '')}:{item.get('source_req', '')}"
    elif category == "field_definitions":
        return f"fd:{item.get('message', '')}:{item.get('field', '')}"
    elif category == "field_constraints":
        return f"fc:{item.get('field', '')}:{item.get('message', '')}"
    elif category == "timing_constraints":
        return f"tc:{item.get('timer_name', '')}:{','.join(item.get('applies_to', []))}"
    elif category == "sequence_constraints":
        return f"sc:{item.get('current_message', '')}:{','.join(item.get('next_allowed', []))}"
    elif category == "response_codes":
        return f"rc:{item.get('message', '')}"
    elif category == "messages":
        return f"msg:{item.get('name', '')}"
    elif category == "variables":
        return f"var:{item.get('name', '')}"
    elif category == "enumerations":
        return f"enum:{item.get('type_name', '')}"
    return ""


# ═══════════════════════════════════════════════════════════════════════════
# Build prompt content for tables and images
# ═══════════════════════════════════════════════════════════════════════════

def _build_table_section(tables: list) -> str:
    """Build the table section of the prompt."""
    if not tables:
        return ""
    parts = ["=== TABLES ==="]
    for i, tbl in enumerate(tables):
        title = tbl.title if hasattr(tbl, 'title') else tbl.get("title", "")
        html = tbl.html if hasattr(tbl, 'html') else tbl.get("html", "")
        parts.append(f"\n--- Table {i+1}: {title} ---")
        # Truncate very large tables to fit context
        parts.append(html[:3000])
    return "\n".join(parts)


def _build_image_section(images: list) -> str:
    """Build the image section of the prompt."""
    if not images:
        return ""
    parts = ["=== FIGURES/IMAGES ==="]
    for i, img in enumerate(images):
        caption = img.caption if hasattr(img, 'caption') else img.get("caption", "")
        surrounding = ""
        if hasattr(img, 'surrounding_text'):
            surrounding = img.surrounding_text
        elif isinstance(img, dict):
            surrounding = img.get("surrounding_text", "")
        parts.append(f"\n--- Figure {i+1}: {caption} ---")
        if surrounding:
            parts.append(f"Context: {surrounding[:300]}")
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# Single-section extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract_from_section(
    chunk: SectionChunk,
    client: InferenceClient,
) -> dict:
    """
    Extract protocol semantics from a single SectionChunk via VLM.

    Handles chunking for large sections, sends tables and images
    alongside text, and merges results.
    """
    if not chunk.merged_text.strip() and not chunk.tables:
        return {cat: [] for cat in ALL_CATEGORIES}

    table_section = _build_table_section(chunk.tables)
    image_section = _build_image_section(chunk.images)

    # Split text into manageable chunks
    text_chunks = _split_text_into_chunks(chunk.merged_text)

    chunk_results = []
    for i, text_part in enumerate(text_chunks):
        # Include tables and images only with the first chunk
        t_sec = table_section if i == 0 else ""
        i_sec = image_section if i == 0 else ""

        prompt = _EXTRACT_PROMPT.format(
            clause_id=chunk.clause_id,
            title=chunk.title,
            pages=", ".join(str(p) for p in chunk.pages),
            text_content=text_part,
            table_section=t_sec,
            image_section=i_sec,
        )

        try:
            result = client.complete_json(prompt, system=_SYSTEM_PROMPT)
            if result and isinstance(result, dict):
                chunk_results.append(result)
        except Exception as e:
            print(f"  [extractor] VLM error on {chunk.clause_id} chunk {i}: {e}")

    if not chunk_results:
        return {cat: [] for cat in ALL_CATEGORIES}

    return merge_results(chunk_results, source=chunk.clause_id)


# ═══════════════════════════════════════════════════════════════════════════
# Batch extraction over all sections
# ═══════════════════════════════════════════════════════════════════════════

def extract_all_sections(
    section_chunks: list[SectionChunk],
    client: InferenceClient,
) -> dict:
    """
    Process ALL section chunks through VLM and merge results.

    No filtering here — processes every section provided.
    Returns merged extraction dict across all sections.
    """
    all_results = []
    total = len(section_chunks)

    for idx, chunk in enumerate(section_chunks):
        # Skip empty sections
        if not chunk.merged_text.strip() and not chunk.tables and not chunk.images:
            continue

        print(f"  [{idx+1}/{total}] {chunk.clause_id} ({chunk.title[:50]}) "
              f"— {len(chunk.merged_text)} chars, "
              f"{len(chunk.tables)} tables, {len(chunk.images)} images")

        result = extract_from_section(chunk, client)

        # Check if we got anything
        n_items = sum(len(result.get(k, [])) for k in ALL_CATEGORIES)
        if n_items > 0:
            all_results.append(result)

    merged = merge_results(all_results, source="all_sections")

    # Summary
    for cat in ALL_CATEGORIES:
        n = len(merged.get(cat, []))
        if n > 0:
            print(f"  [extractor] {cat}: {n} items")

    # Log validation stats
    if _vlm_validation_log:
        print(f"  [extractor] VLM validation: {len(_vlm_validation_log)} items dropped")

    return merged
