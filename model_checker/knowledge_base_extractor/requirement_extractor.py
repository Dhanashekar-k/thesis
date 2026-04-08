"""
requirement_extractor.py — Extract V2G20-XXXX normative requirement IDs.

In ISO 15118-20 the tags appear in several forms:

    ... the EVCC shall send SessionSetupReq [V2G20-1747].
    V2G20-1747 The EVCC shall ...
    ... (see V2G20-1747 and V2G20-1748) ...
    ... condition V2G20-1747/V2G20-1748 applies ...

Every unique ID in a block is extracted once.  The surrounding sentence is
stored as context so Stage 2 can classify it without re-reading the full text.
"""

from __future__ import annotations

import re
from models import RawBlock, Requirement

# Primary pattern: V2G20 + dash + 4 or more digits.
# Handles bracketed/parenthesised variants automatically via \b word boundary.
_REQ_RE = re.compile(r"\bV2G20-(\d{4,})\b")

# Simple sentence splitter: split after sentence-ending punctuation + whitespace,
# or on newlines. Keeps the split conservative to avoid cutting mid-reference.
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n")


def extract_requirements_from_block(
    block: RawBlock,
    section_id: str | None = None,
) -> list[Requirement]:
    """
    Return a Requirement for every unique V2G20-XXXX ID in block.content.
    The req.text field is set to the sentence that contains the ID.
    Multiple occurrences of the same ID within the block are deduplicated —
    the first occurrence wins.
    """
    if not block.content:
        return []

    sentences = _split_sentences(block.content)
    found: dict[str, Requirement] = {}

    for sentence in sentences:
        for m in _REQ_RE.finditer(sentence):
            req_id = f"V2G20-{m.group(1)}"
            if req_id not in found:
                found[req_id] = Requirement(
                    req_id=req_id,
                    text=sentence.strip(),
                    page=block.page,
                    section_id=section_id,
                )

    return list(found.values())


def extract_requirements_from_text(
    text: str,
    page: int,
    section_id: str | None = None,
) -> list[Requirement]:
    """Convenience wrapper when you have raw text rather than a RawBlock."""
    dummy = RawBlock(
        page=page, block_id=-1, label="text",
        content=text, bbox=(0, 0, 0, 0), order=None, group_id=-1,
    )
    return extract_requirements_from_block(dummy, section_id=section_id)


def has_requirements(block: RawBlock) -> bool:
    """Quick check — does this block contain any V2G20 IDs?"""
    return bool(_REQ_RE.search(block.content))


def collect_all_req_ids(text: str) -> list[str]:
    """
    Return all V2G20-XXXX IDs found in text, in order of appearance.
    Useful for quick scanning without sentence-level context.
    """
    return [f"V2G20-{m.group(1)}" for m in _REQ_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.  Non-empty parts only.
    Splits on: '. ', '! ', '? ' (followed by whitespace) and newlines.
    """
    parts = _SENT_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]