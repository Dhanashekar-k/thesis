from __future__ import annotations

import argparse
import base64
import hashlib
import json
from tqdm import tqdm
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests

JSONL_FILES = {
    "sections": "sections.jsonl",
    "pages": "pages.jsonl",
    "blocks": "blocks.jsonl",
    "text_units": "text_units.jsonl",
    "figures": "figures.jsonl",
    "tables": "tables.jsonl",
    "edges": "edges.jsonl",
}

WHITESPACE_RE = re.compile(r"\s+")
ACRONYM_DEF_RE = re.compile(r"\b([A-Z][A-Za-z][A-Za-z0-9_\-/ ]{2,80}?)\s*\(([A-Z][A-Z0-9]{1,15})\)")
REQ_STYLE_RE = re.compile(r"\[(?:[A-Z][A-Z0-9]{1,15}-\d{3,6})\]")
MESSAGE_NAME_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*(?:Req|Res))\b")
ID_TERM_RE = re.compile(r"\b([A-Z]{2,}[A-Z0-9_-]*ID|[A-Z]{2,}[A-Z0-9_-]*|[A-Za-z][A-Za-z0-9_]+ID)\b")
TERM_SPLIT_RE = re.compile(r"[;,/]|\band\b|\bor\b", re.IGNORECASE)

DEFAULT_TEXT_PROMPT = """You are enriching technical protocol evidence for cybersecurity-oriented graph retrieval.
Return strict JSON only.

Primary objective:
Represent the evidence in security-aware language while staying fully grounded in the provided content.
Prioritize concepts relevant to attack surface, trust boundaries, identities, credentials, certificates,
authentication, authorization, message flows, state transitions, confidentiality, integrity, availability,
privacy-sensitive identifiers, metering/billing data, backend/secondary-actor interactions, timing constraints,
and protocol preconditions.

Rules:
1. Write a short proxy_description focused on what this evidence means in protocol/security terms.
2. Extract the main concepts/entities in this evidence.
3. Mark whether each concept is defined here or just mentioned/used.
4. Extract only relations explicitly supported by this evidence.
5. Prefer protocol/security wording such as actor, credential, identifier, trust anchor, message, field,
   session, timer, state, constraint, backend actor, attack surface, privacy-sensitive data.
6. If the evidence has no real cybersecurity significance, keep the description neutral rather than inventing one.
7. Do not invent vulnerabilities, threats, or implications beyond the evidence.

Output schema:
{
  "proxy_description": "...",
  "concepts": [
    {
      "name": "...",
      "type": "actor|message|certificate|identifier|session|security|authorization|metering|billing|protocol_object|requirement_topic|acronym|definition|other",
      "aliases": ["..."],
      "is_definition": true,
      "confidence": 0.0
    }
  ],
  "relations": [
    {
      "source": "concept name",
      "target": "concept name",
      "relation": "defines|uses|authenticates|identifies|references|belongs_to|interacts_with|supports|contains|related_to",
      "confidence": 0.0
    }
  ],
  "keywords": ["..."],
  "classification": "definition|requirement|explanation|message_semantics|security_note|timing_rule|table_description|figure_description|other"
}
"""

DEFAULT_VISION_PROMPT = """You are enriching technical protocol figures and tables for cybersecurity-oriented graph retrieval.
Return strict JSON only.

Use the image together with the provided caption and local context.
Describe the figure/table in security-aware protocol language.
Prioritize what it shows about actors, trust boundaries, credentials, certificates, identifiers, message flow,
state progression, timers, data fields, backend interactions, privacy-sensitive data, and security-relevant constraints.

Rules:
1. proxy_description should explain what the figure/table represents in protocol/security terms.
2. Extract the main concepts shown or implied by the visual plus caption/context.
3. Extract only relations directly supported by the visual/caption/context.
4. If the visual is architectural or sequential, capture who talks to whom, what is exchanged, and any trust/security role.
5. If the visual is a table, capture what is being enumerated or constrained (fields, identifiers, algorithms, message parts, rules, timers, etc.).
6. Do not invent vulnerabilities or speculative attacks.
7. If the content is not security-relevant, stay neutral rather than forcing a security interpretation.

Use the same schema:
{
  "proxy_description": "...",
  "concepts": [
    {
      "name": "...",
      "type": "actor|message|certificate|identifier|session|security|authorization|metering|billing|protocol_object|requirement_topic|acronym|definition|other",
      "aliases": ["..."],
      "is_definition": false,
      "confidence": 0.0
    }
  ],
  "relations": [
    {
      "source": "concept name",
      "target": "concept name",
      "relation": "defines|uses|authenticates|identifies|references|belongs_to|interacts_with|supports|contains|related_to|illustrates|tabulates",
      "confidence": 0.0
    }
  ],
  "keywords": ["..."],
  "classification": "figure_description|table_description|other"
}
"""


def norm_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text or "").strip()


def canonical_slug(text: str) -> str:
    text = norm_text(text).lower()
    text = re.sub(r"[^a-z0-9._:-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "unknown"


def safe_json_loads(text: str) -> Optional[dict]:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None
    return None


def read_jsonl(path: Path) -> List[dict]:
    records: List[dict] = []
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


class JsonlWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.f = self.path.open("w", encoding="utf-8")
        self.count = 0
        self._seen: set[str] = set()

    def write(self, obj: dict, unique_key: Optional[str] = None) -> bool:
        if unique_key:
            v = obj.get(unique_key)
            if v is None:
                raise ValueError(f"Missing unique key {unique_key} for {self.path}")
            if v in self._seen:
                return False
            self._seen.add(v)
        self.f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        self.count += 1
        return True

    def close(self) -> None:
        self.f.close()


@dataclass
class EvidenceUnit:
    evidence_id: str
    modality: str
    section_id: Optional[str]
    page_indices: List[int]
    raw_text: str
    source_ids: List[str]
    caption: Optional[str] = None
    image_path: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    context_text: str = ""
    requirement_refs: List[str] = field(default_factory=list)
    proxy_description: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    classification: Optional[str] = None
    concepts: List[dict] = field(default_factory=list)
    relations: List[dict] = field(default_factory=list)
    llm_status: str = "not_run"
    llm_error: Optional[str] = None


class OpenAICompatClient:
    def __init__(self, api_base: str, model: str, api_key: str = "EMPTY", timeout: int = 180, max_retries: int = 3) -> None:
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

    def _post(self, payload: dict) -> dict:
        url = f"{self.api_base}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        last_err: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.post(url, headers=headers, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_err = e
                if attempt == self.max_retries:
                    raise
                time.sleep(1.5 * attempt)
        raise RuntimeError(f"Chat completion failed: {last_err}")

    def chat_json(self, system_prompt: str, user_text: str, image_paths: Optional[List[str]] = None, temperature: float = 0.0) -> dict:
        content: List[dict] = [{"type": "text", "text": user_text}]
        for path in image_paths or []:
            if not path:
                continue
            p = Path(path)
            if not p.exists():
                continue
            mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
            b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
            content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}})

        payload = {
            "model": self.model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content if image_paths else user_text},
            ],
        }
        res = self._post(payload)
        choice = res["choices"][0]["message"]["content"]
        parsed = safe_json_loads(choice)
        if parsed is None:
            raise ValueError(f"Model did not return valid JSON: {choice[:500]}")
        return parsed


def load_phase1_bundle(phase1_root: Path) -> Dict[str, List[dict]]:
    bundle: Dict[str, List[dict]] = {}
    for key, name in JSONL_FILES.items():
        bundle[key] = read_jsonl(phase1_root / name)
    return bundle


def build_lookup(records: Iterable[dict], key: str) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for r in records:
        if key in r and r[key] is not None:
            out[str(r[key])] = r
    return out


def extract_deterministic_concepts(text: str, section_title: Optional[str] = None) -> Tuple[List[dict], List[dict], List[str]]:
    concepts: Dict[str, dict] = {}
    relations: List[dict] = []
    keywords: List[str] = []

    def upsert(name: str, ctype: str = "other", aliases: Optional[List[str]] = None, is_definition: bool = False, confidence: float = 0.6) -> None:
        key = canonical_slug(name)
        if key not in concepts:
            concepts[key] = {
                "name": norm_text(name),
                "type": ctype,
                "aliases": sorted(set(a for a in (aliases or []) if a and norm_text(a) and norm_text(a) != norm_text(name))),
                "is_definition": bool(is_definition),
                "confidence": float(confidence),
            }
        else:
            concepts[key]["aliases"] = sorted(set(concepts[key].get("aliases", [])) | set(aliases or []))
            concepts[key]["is_definition"] = concepts[key].get("is_definition", False) or bool(is_definition)
            concepts[key]["confidence"] = max(float(concepts[key].get("confidence", 0.0)), float(confidence))
            if concepts[key].get("type") == "other" and ctype != "other":
                concepts[key]["type"] = ctype

    if section_title:
        title = norm_text(section_title)
        if title:
            upsert(title, ctype="definition", is_definition=True, confidence=0.7)
            keywords.extend([w for w in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", title)[:8]])

    for m in ACRONYM_DEF_RE.finditer(text or ""):
        full = norm_text(m.group(1))
        short = norm_text(m.group(2))
        if len(full.split()) <= 12:
            upsert(full, ctype="acronym", aliases=[short], is_definition=True, confidence=0.85)
            upsert(short, ctype="acronym", aliases=[full], is_definition=False, confidence=0.8)
            relations.append({"source": short, "target": full, "relation": "defines", "confidence": 0.85, "source_type": "deterministic"})

    for req in REQ_STYLE_RE.findall(text or ""):
        clean = req.strip("[]")
        upsert(clean, ctype="requirement_topic", confidence=0.9)
        keywords.append(clean)

    for msg in MESSAGE_NAME_RE.findall(text or ""):
        upsert(msg, ctype="message", confidence=0.8)
        keywords.append(msg)

    for tok in ID_TERM_RE.findall(text or ""):
        if len(tok) < 3:
            continue
        ctype = "identifier" if tok.endswith("ID") else "other"
        upsert(tok, ctype=ctype, confidence=0.65)

    return list(concepts.values()), relations, sorted(set(keywords))


def find_section_title(section_id: Optional[str], sections_by_id: Dict[str, dict]) -> Optional[str]:
    if not section_id:
        return None
    rec = sections_by_id.get(section_id)
    return rec.get("title") if rec else None


def gather_text_neighbors(text_units: List[dict], current_index: int, window: int = 1) -> List[str]:
    parts: List[str] = []
    for offset in range(1, window + 1):
        prev_idx = current_index - offset
        next_idx = current_index + offset
        if prev_idx >= 0:
            parts.append(f"PREV[{offset}]: {norm_text(text_units[prev_idx].get('text', ''))[:1200]}")
        if next_idx < len(text_units):
            parts.append(f"NEXT[{offset}]: {norm_text(text_units[next_idx].get('text', ''))[:1200]}")
    return parts


def gather_page_local_text(page_index: int, text_units_by_page: Dict[int, List[dict]], limit: int = 3) -> str:
    units = text_units_by_page.get(page_index, [])[:limit]
    return "\n".join(norm_text(u.get("text", ""))[:1200] for u in units if u.get("text"))


def build_evidence_units(bundle: Dict[str, List[dict]]) -> List[EvidenceUnit]:
    sections_by_id = build_lookup(bundle["sections"], "section_id")
    text_units = sorted(bundle["text_units"], key=lambda x: (x.get("start_page_index", 10**9), x.get("text_unit_id", "")))
    figures = sorted(bundle["figures"], key=lambda x: (x.get("start_page_index", 10**9), x.get("figure_id", "")))
    tables = sorted(bundle["tables"], key=lambda x: (x.get("start_page_index", 10**9), x.get("table_id", "")))

    text_units_by_page: Dict[int, List[dict]] = defaultdict(list)
    for tu in text_units:
        for p in tu.get("page_indices", []):
            text_units_by_page[int(p)].append(tu)

    evidence: List[EvidenceUnit] = []
    for idx, tu in enumerate(text_units):
        section_title = find_section_title(tu.get("section_id"), sections_by_id)
        context_chunks = []
        if section_title:
            context_chunks.append(f"SECTION: {section_title}")
        context_chunks.extend(gather_text_neighbors(text_units, idx, window=1))
        ev = EvidenceUnit(
            evidence_id=f"evidence:text:{tu['text_unit_id']}",
            modality="text",
            section_id=tu.get("section_id"),
            page_indices=[int(p) for p in tu.get("page_indices", [])],
            raw_text=norm_text(tu.get("text", "")),
            source_ids=list(tu.get("block_ids", [])),
            extra={
                "text_unit_id": tu.get("text_unit_id"),
                "start_page_index": tu.get("start_page_index"),
                "end_page_index": tu.get("end_page_index"),
                "section_title": section_title,
            },
            context_text="\n".join(context_chunks),
            requirement_refs=list(tu.get("requirement_refs", [])),
        )
        evidence.append(ev)

    for fig in figures:
        page_context = gather_page_local_text(int(fig.get("start_page_index", 0)), text_units_by_page)
        section_title = find_section_title(fig.get("section_id"), sections_by_id)
        context_chunks = []
        if section_title:
            context_chunks.append(f"SECTION: {section_title}")
        if fig.get("caption"):
            context_chunks.append(f"CAPTION: {norm_text(fig['caption'])}")
        if page_context:
            context_chunks.append(f"LOCAL_TEXT: {page_context}")
        ev = EvidenceUnit(
            evidence_id=f"evidence:figure:{fig['figure_id']}",
            modality="figure",
            section_id=fig.get("section_id"),
            page_indices=[int(p) for p in fig.get("page_indices", [])],
            raw_text=norm_text(fig.get("caption", "")),
            source_ids=[x for x in [fig.get("image_block_id"), fig.get("caption_block_id")] if x],
            caption=fig.get("caption"),
            image_path=fig.get("image_path"),
            extra={
                "figure_id": fig.get("figure_id"),
                "caption_number": fig.get("caption_number"),
                "section_title": section_title,
            },
            context_text="\n".join(context_chunks),
        )
        evidence.append(ev)

    for tbl in tables:
        page_context = gather_page_local_text(int(tbl.get("start_page_index", 0)), text_units_by_page)
        section_title = find_section_title(tbl.get("section_id"), sections_by_id)
        raw_table = norm_text(tbl.get("raw_html", ""))
        if len(raw_table) > 8000:
            raw_table = raw_table[:8000] + " ... [truncated]"
        context_chunks = []
        if section_title:
            context_chunks.append(f"SECTION: {section_title}")
        if tbl.get("caption"):
            context_chunks.append(f"CAPTION: {norm_text(tbl['caption'])}")
        if page_context:
            context_chunks.append(f"LOCAL_TEXT: {page_context}")
        ev = EvidenceUnit(
            evidence_id=f"evidence:table:{tbl['table_id']}",
            modality="table",
            section_id=tbl.get("section_id"),
            page_indices=[int(p) for p in tbl.get("page_indices", [])],
            raw_text=raw_table,
            source_ids=list(tbl.get("table_block_ids", [])),
            caption=tbl.get("caption"),
            extra={
                "table_id": tbl.get("table_id"),
                "caption_number": tbl.get("caption_number"),
                "section_title": section_title,
                "caption_block_id": tbl.get("caption_block_id"),
            },
            context_text="\n".join(context_chunks),
        )
        evidence.append(ev)

    return evidence


def make_prompt_payload(ev: EvidenceUnit) -> str:
    parts = [f"MODALITY: {ev.modality}"]
    if ev.extra.get("section_title"):
        parts.append(f"SECTION_TITLE: {ev.extra['section_title']}")
    if ev.caption:
        parts.append(f"CAPTION: {norm_text(ev.caption)}")
    if ev.requirement_refs:
        parts.append(f"REQUIREMENT_REFS: {', '.join(ev.requirement_refs)}")
    if ev.context_text:
        parts.append(f"CONTEXT:\n{ev.context_text}")
    if ev.raw_text:
        label = "RAW_TEXT" if ev.modality == "text" else ("RAW_TABLE" if ev.modality == "table" else "RAW_EVIDENCE_TEXT")
        parts.append(f"{label}:\n{ev.raw_text[:12000]}")
    return "\n\n".join(parts)


def enrich_evidence_with_model(
    evidence: List[EvidenceUnit],
    client: Optional[OpenAICompatClient],
    use_vlm_for_figures: bool,
    use_llm_for_text: bool,
    use_llm_for_tables: bool,
) -> None:
    total = len(evidence)

    for idx, ev in enumerate(tqdm(evidence, desc="Phase 2 enrichment"), start=1):
        print(f"[Enrich] {idx}/{total} | {ev.modality} | {ev.evidence_id}", flush=True)

        det_concepts, det_relations, det_keywords = extract_deterministic_concepts(
            ev.raw_text + "\n" + (ev.caption or ""),
            ev.extra.get("section_title"),
        )
        ev.concepts.extend(det_concepts)
        ev.relations.extend(det_relations)
        ev.keywords = sorted(set(ev.keywords) | set(det_keywords) | set(ev.requirement_refs))

        should_call = False
        system_prompt = DEFAULT_TEXT_PROMPT
        image_paths: List[str] = []

        if client is not None:
            if ev.modality == "text" and use_llm_for_text:
                should_call = True
            elif ev.modality == "table" and use_llm_for_tables:
                should_call = True
                system_prompt = DEFAULT_TEXT_PROMPT
            elif ev.modality == "figure" and use_vlm_for_figures:
                should_call = True
                system_prompt = DEFAULT_VISION_PROMPT
                if ev.image_path:
                    image_paths = [ev.image_path]

        if not should_call:
            ev.llm_status = "skipped"
            print(f"[Enrich] {idx}/{total} SKIPPED | {ev.evidence_id}", flush=True)
            continue

        try:
            parsed = client.chat_json(
                system_prompt=system_prompt,
                user_text=make_prompt_payload(ev),
                image_paths=image_paths,
            )
            ev.proxy_description = norm_text(parsed.get("proxy_description", "")) or None
            ev.classification = norm_text(parsed.get("classification", "")) or None
            ev.keywords = sorted(
                set(ev.keywords)
                | set(norm_text(k) for k in parsed.get("keywords", []) if norm_text(k))
            )

            for c in parsed.get("concepts", []):
                name = norm_text(c.get("name", ""))
                if not name:
                    continue
                ev.concepts.append(
                    {
                        "name": name,
                        "type": norm_text(c.get("type", "other")) or "other",
                        "aliases": sorted(
                            set(
                                norm_text(a)
                                for a in c.get("aliases", [])
                                if norm_text(a) and norm_text(a) != name
                            )
                        ),
                        "is_definition": bool(c.get("is_definition", False)),
                        "confidence": float(c.get("confidence", 0.6) or 0.6),
                        "source_type": "llm",
                    }
                )

            for r in parsed.get("relations", []):
                src = norm_text(r.get("source", ""))
                dst = norm_text(r.get("target", ""))
                rel = norm_text(r.get("relation", "related_to")) or "related_to"
                if not src or not dst:
                    continue
                ev.relations.append(
                    {
                        "source": src,
                        "target": dst,
                        "relation": rel,
                        "confidence": float(r.get("confidence", 0.6) or 0.6),
                        "source_type": "llm",
                    }
                )

            ev.llm_status = "ok"
            print(f"[Enrich] {idx}/{total} OK | {ev.evidence_id}", flush=True)

        except Exception as e:
            ev.llm_status = "error"
            ev.llm_error = str(e)
            print(f"[Enrich] {idx}/{total} ERROR | {ev.evidence_id} | {e}", flush=True)

        ev.concepts = dedup_concepts(ev.concepts)
        ev.relations = dedup_relations(ev.relations)
        if ev.proxy_description is None:
            ev.proxy_description = deterministic_proxy(ev)

    for ev in evidence:
        if ev.proxy_description is None:
            ev.proxy_description = deterministic_proxy(ev)
        ev.concepts = dedup_concepts(ev.concepts)
        ev.relations = dedup_relations(ev.relations)


def deterministic_proxy(ev: EvidenceUnit) -> str:
    if ev.modality == "text":
        return norm_text((ev.extra.get("section_title") or "") + " — " + ev.raw_text[:260]).strip(" —")
    if ev.modality == "figure":
        return norm_text((ev.caption or "Figure")[:260])
    if ev.modality == "table":
        prefix = ev.caption or "Table"
        suffix = ev.raw_text[:180]
        return norm_text(f"{prefix} — {suffix}")
    return norm_text(ev.raw_text[:260])


def dedup_concepts(concepts: List[dict]) -> List[dict]:
    merged: Dict[str, dict] = {}
    for c in concepts:
        name = norm_text(c.get("name", ""))
        if not name:
            continue
        key = canonical_slug(name)
        aliases = sorted(set(norm_text(a) for a in c.get("aliases", []) if norm_text(a) and norm_text(a) != name))
        if key not in merged:
            merged[key] = {
                "name": name,
                "type": c.get("type", "other") or "other",
                "aliases": aliases,
                "is_definition": bool(c.get("is_definition", False)),
                "confidence": float(c.get("confidence", 0.6) or 0.6),
                "source_type": c.get("source_type", "deterministic"),
            }
        else:
            merged[key]["aliases"] = sorted(set(merged[key].get("aliases", [])) | set(aliases))
            merged[key]["is_definition"] = merged[key].get("is_definition", False) or bool(c.get("is_definition", False))
            merged[key]["confidence"] = max(float(merged[key].get("confidence", 0.0)), float(c.get("confidence", 0.6) or 0.6))
            if merged[key].get("type") == "other" and c.get("type"):
                merged[key]["type"] = c.get("type")
            if merged[key].get("source_type") != "llm" and c.get("source_type") == "llm":
                merged[key]["source_type"] = "llm"
    return list(merged.values())


def dedup_relations(relations: List[dict]) -> List[dict]:
    merged: Dict[Tuple[str, str, str], dict] = {}
    for r in relations:
        src = norm_text(r.get("source", ""))
        dst = norm_text(r.get("target", ""))
        rel = norm_text(r.get("relation", "related_to")) or "related_to"
        if not src or not dst:
            continue
        key = (canonical_slug(src), rel, canonical_slug(dst))
        payload = {
            "source": src,
            "target": dst,
            "relation": rel,
            "confidence": float(r.get("confidence", 0.6) or 0.6),
            "source_type": r.get("source_type", "deterministic"),
        }
        if key not in merged or payload["confidence"] > merged[key]["confidence"]:
            merged[key] = payload
    return list(merged.values())


def normalize_concept_name(name: str) -> str:
    name = norm_text(name)
    name = re.sub(r"\s+", " ", name)
    return name


def build_concept_graph(evidence: List[EvidenceUnit]) -> Tuple[List[dict], List[dict], Dict[str, str]]:
    concept_nodes: Dict[str, dict] = {}
    alias_to_concept: Dict[str, str] = {}
    semantic_edges: List[dict] = []
    edge_seen: set[Tuple[str, str, str, str]] = set()

    def concept_id_for(name: str, ctype: str = "other") -> str:
        canon = normalize_concept_name(name)
        slug = canonical_slug(canon)
        cid = f"concept:{slug}"
        if cid not in concept_nodes:
            concept_nodes[cid] = {
                "concept_id": cid,
                "name": canon,
                "type": ctype or "other",
                "aliases": [],
                "source_evidence_ids": [],
                "definition_evidence_ids": [],
                "confidence": 0.0,
            }
        else:
            if concept_nodes[cid]["type"] == "other" and ctype and ctype != "other":
                concept_nodes[cid]["type"] = ctype
        alias_to_concept[canonical_slug(canon)] = cid
        return cid

    def add_edge(src: str, rel: str, dst: str, **props: Any) -> None:
        key = (src, rel, dst, json.dumps(props, sort_keys=True, ensure_ascii=False))
        if key in edge_seen:
            return
        edge_seen.add(key)
        payload = {"src": src, "rel": rel, "dst": dst}
        if props:
            payload["props"] = props
        semantic_edges.append(payload)

    for ev in evidence:
        ev_node = ev.evidence_id
        for req in ev.requirement_refs:
            rid = req.strip("[]")
            req_id = f"requirement:{rid}"
            add_edge(ev_node, "references_requirement", req_id, confidence=1.0, source_type="deterministic")

        for c in ev.concepts:
            cname = normalize_concept_name(c["name"])
            cid = concept_id_for(cname, c.get("type", "other"))
            concept_nodes[cid]["confidence"] = max(float(concept_nodes[cid].get("confidence", 0.0)), float(c.get("confidence", 0.6) or 0.6))
            concept_nodes[cid]["source_evidence_ids"] = sorted(set(concept_nodes[cid]["source_evidence_ids"]) | {ev_node})
            if c.get("is_definition"):
                concept_nodes[cid]["definition_evidence_ids"] = sorted(set(concept_nodes[cid]["definition_evidence_ids"]) | {ev_node})
            aliases = [normalize_concept_name(a) for a in c.get("aliases", []) if normalize_concept_name(a)]
            concept_nodes[cid]["aliases"] = sorted(set(concept_nodes[cid].get("aliases", [])) | set(aliases))
            for alias in aliases:
                alias_to_concept[canonical_slug(alias)] = cid
            add_edge(ev_node, "mentions_concept", cid, confidence=float(c.get("confidence", 0.6) or 0.6), source_type=c.get("source_type", "deterministic"))
            if c.get("is_definition"):
                add_edge(ev_node, "defines_concept", cid, confidence=float(c.get("confidence", 0.6) or 0.6), source_type=c.get("source_type", "deterministic"))
            if ev.section_id:
                add_edge(cid, "appears_in_section", ev.section_id, confidence=float(c.get("confidence", 0.6) or 0.6), source_type="derived")

        local_cids = sorted({alias_to_concept[canonical_slug(normalize_concept_name(c['name']))] for c in ev.concepts if normalize_concept_name(c.get('name', ''))})
        for i in range(len(local_cids)):
            for j in range(i + 1, len(local_cids)):
                add_edge(local_cids[i], "cooccurs_with", local_cids[j], evidence_id=ev_node, source_type="derived", confidence=0.55)
                add_edge(local_cids[j], "cooccurs_with", local_cids[i], evidence_id=ev_node, source_type="derived", confidence=0.55)

        for r in ev.relations:
            src_name = normalize_concept_name(r["source"])
            dst_name = normalize_concept_name(r["target"])
            src_cid = alias_to_concept.get(canonical_slug(src_name)) or concept_id_for(src_name)
            dst_cid = alias_to_concept.get(canonical_slug(dst_name)) or concept_id_for(dst_name)
            add_edge(src_cid, r["relation"], dst_cid, evidence_id=ev_node, confidence=float(r.get("confidence", 0.6) or 0.6), source_type=r.get("source_type", "llm"))

    return list(concept_nodes.values()), semantic_edges, alias_to_concept


def write_outputs(output_root: Path, evidence: List[EvidenceUnit], concepts: List[dict], semantic_edges: List[dict], phase1_root: Path, llm_cfg: dict) -> dict:
    output_root.mkdir(parents=True, exist_ok=True)
    evidence_w = JsonlWriter(output_root / "evidence_units.jsonl")
    concepts_w = JsonlWriter(output_root / "concept_nodes.jsonl")
    edges_w = JsonlWriter(output_root / "semantic_edges.jsonl")

    for ev in evidence:
        evidence_w.write(
            {
                "evidence_id": ev.evidence_id,
                "modality": ev.modality,
                "section_id": ev.section_id,
                "page_indices": ev.page_indices,
                "raw_text": ev.raw_text,
                "caption": ev.caption,
                "image_path": ev.image_path,
                "source_ids": ev.source_ids,
                "extra": ev.extra,
                "context_text": ev.context_text,
                "requirement_refs": ev.requirement_refs,
                "proxy_description": ev.proxy_description,
                "keywords": ev.keywords,
                "classification": ev.classification,
                "concepts": ev.concepts,
                "relations": ev.relations,
                "llm_status": ev.llm_status,
                "llm_error": ev.llm_error,
            },
            unique_key="evidence_id",
        )

    for c in concepts:
        concepts_w.write(c, unique_key="concept_id")

    for edge in semantic_edges:
        edges_w.write(edge)

    evidence_w.close()
    concepts_w.close()
    edges_w.close()

    manifest = {
        "phase": 2,
        "description": "Semantic enrichment and multimodal graph construction over Phase 1 evidence.",
        "phase1_root": str(phase1_root.resolve()),
        "outputs": {
            "evidence_units": str((output_root / "evidence_units.jsonl").resolve()),
            "concept_nodes": str((output_root / "concept_nodes.jsonl").resolve()),
            "semantic_edges": str((output_root / "semantic_edges.jsonl").resolve()),
        },
        "llm": llm_cfg,
        "stats": {
            "evidence_unit_count": evidence_w.count,
            "concept_count": concepts_w.count,
            "semantic_edge_count": edges_w.count,
            "text_evidence_count": sum(1 for e in evidence if e.modality == "text"),
            "figure_evidence_count": sum(1 for e in evidence if e.modality == "figure"),
            "table_evidence_count": sum(1 for e in evidence if e.modality == "table"),
            "llm_ok_count": sum(1 for e in evidence if e.llm_status == "ok"),
            "llm_error_count": sum(1 for e in evidence if e.llm_status == "error"),
            "llm_skipped_count": sum(1 for e in evidence if e.llm_status in {"skipped", "not_run"}),
        },
        "notes": [
            "Phase 2 consumes Phase 1 outputs only; it does not re-parse OCR.",
            "Raw evidence remains the source of truth. Proxy descriptions are retrieval helpers only.",
            "Deterministic signals are combined with optional LLM/VLM enrichment for concept and relation extraction.",
        ],
    }
    with (output_root / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 2 semantic enrichment and multimodal graph construction.")
    p.add_argument("--phase1-root", type=Path, required=True, help="Directory containing Phase 1 JSONL outputs.")
    p.add_argument("--output-root", type=Path, required=True, help="Output directory for Phase 2 artifacts.")
    p.add_argument("--api-base", type=str, default=os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:8000/v1"), help="OpenAI-compatible API base.")
    p.add_argument("--model", type=str, default=os.environ.get("OPENAI_MODEL", "Qwen/Qwen2.5-VL-72B-Instruct"), help="Model name for LLM/VLM enrichment.")
    p.add_argument("--api-key", type=str, default=os.environ.get("OPENAI_API_KEY", "EMPTY"), help="API key for OpenAI-compatible server.")
    p.add_argument("--disable-llm", action="store_true", help="Disable all LLM/VLM enrichment.")
    p.add_argument("--disable-text-llm", action="store_true", help="Disable text-unit enrichment only.")
    p.add_argument("--disable-table-llm", action="store_true", help="Disable table enrichment only.")
    p.add_argument("--disable-figure-vlm", action="store_true", help="Disable figure enrichment only.")
    p.add_argument("--max-evidence", type=int, default=None, help="Optional limit for debugging/testing.")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)

    print("[Phase 2] Loading Phase 1 bundle...", flush=True)
    bundle = load_phase1_bundle(args.phase1_root)

    print("[Phase 2] Building evidence units...", flush=True)
    evidence = build_evidence_units(bundle)
    print(f"[Phase 2] Built {len(evidence)} evidence units.", flush=True)

    if args.max_evidence is not None:
        evidence = evidence[: args.max_evidence]
        print(f"[Phase 2] Limited to first {len(evidence)} evidence units.", flush=True)

    client: Optional[OpenAICompatClient] = None
    if not args.disable_llm:
        print("[Phase 2] Initializing OpenAI-compatible client...", flush=True)
        client = OpenAICompatClient(api_base=args.api_base, model=args.model, api_key=args.api_key)

    print("[Phase 2] Starting enrichment...", flush=True)
    enrich_evidence_with_model(
        evidence=evidence,
        client=client,
        use_vlm_for_figures=not args.disable_figure_vlm and not args.disable_llm,
        use_llm_for_text=not args.disable_text_llm and not args.disable_llm,
        use_llm_for_tables=not args.disable_table_llm and not args.disable_llm,
    )

    print("[Phase 2] Building concept graph...", flush=True)
    concepts, semantic_edges, _alias_map = build_concept_graph(evidence)
    print(f"[Phase 2] Built {len(concepts)} concepts and {len(semantic_edges)} semantic edges.", flush=True)

    print("[Phase 2] Writing outputs...", flush=True)
    manifest = write_outputs(
        output_root=args.output_root,
        evidence=evidence,
        concepts=concepts,
        semantic_edges=semantic_edges,
        phase1_root=args.phase1_root,
        llm_cfg={
            "enabled": not args.disable_llm,
            "api_base": None if args.disable_llm else args.api_base,
            "model": None if args.disable_llm else args.model,
            "text_enabled": not args.disable_text_llm and not args.disable_llm,
            "table_enabled": not args.disable_table_llm and not args.disable_llm,
            "figure_enabled": not args.disable_figure_vlm and not args.disable_llm,
        },
    )

    print(json.dumps(manifest["stats"], indent=2), flush=True)
    print(f"Wrote manifest to {args.output_root / 'manifest.json'}", flush=True)


if __name__ == "__main__":
    main()
