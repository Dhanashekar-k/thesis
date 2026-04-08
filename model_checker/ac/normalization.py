"""
normalization.py — Requirement ID normalization for OCR-corrupted ISO references.

All ISO requirement IDs follow [V2G20-XXXX] where XXXX is numeric.
OCR corruption may produce partial forms:
    V2G20-XXXX]   — missing opening bracket
    2G20-XXXX]    — missing [V
    G20-XXXX]     — missing [V2
    20-XXXX]      — missing [V2G
    -XXXX]        — missing [V2G20
    XXXX]         — only identifier + closing bracket
    V20G0-XXXX    — character transposition
    V2G2O-XXXX    — O instead of 0

This module is imported and applied universally before any downstream processing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class NormalizationLog:
    """Tracks every normalization applied."""
    entries: list[dict] = field(default_factory=list)

    def record(self, original: str, normalized: str, context: str = ""):
        if original != normalized:
            self.entries.append({
                "original": original,
                "normalized": normalized,
                "context": context,
            })

    def summary(self) -> dict:
        return {
            "total_normalizations": len(self.entries),
            "entries": self.entries,
        }


# Singleton log for the pipeline run
_normalization_log = NormalizationLog()


def get_normalization_log() -> NormalizationLog:
    """Get the global normalization log."""
    return _normalization_log


def reset_normalization_log() -> None:
    """Reset the log (e.g. between pipeline runs)."""
    global _normalization_log
    _normalization_log = NormalizationLog()


# ═══════════════════════════════════════════════════════════════════════════
# Core normalization
# ═══════════════════════════════════════════════════════════════════════════

# Pattern to match any corrupted V2G20-XXXX reference
# Captures the numeric ID at the end
# Matches: [V2G20-1234], V2G20-1234], 2G20-1234], G20-1234], 20-1234], -1234], 1234]
# Also: V20G0-1234, V2G2O-1234, [V2G20-1234
_CORRUPTED_REQ_RE = re.compile(
    r'(?:\[?)'                          # optional opening bracket
    r'(?:V2G20|V20G0|V2G2O|V2G0|'      # full or transposed prefix
    r'2G20|G20|20)?'                    # partial prefix (OCR dropped leading chars)
    r'-'                                # hyphen (always present)
    r'(\d{1,5})'                        # the numeric ID (1-5 digits)
    r'(?:\]?)'                          # optional closing bracket
)

# Stricter pattern for detection in flowing text (must have some V2G context)
_PARTIAL_REQ_RE = re.compile(
    r'(?:\[?)'
    r'(?:V2?G?2?0?|V20G0|V2G2O)'       # at least some prefix chars
    r'-'
    r'(\d{1,5})'
    r'(?:\]?)'
)

# Well-formed pattern
_WELLFORMED_REQ_RE = re.compile(r'\[V2G20-(\d+)\]')

# Any token that looks like a corrupted req ID
_TOKEN_REQ_RE = re.compile(
    r'\b'
    r'(?:V2G20|V20G0|V2G2O|2G20|G20)'
    r'-'
    r'(\d{1,5})'
    r'\b'
)


def normalize_req_id(token: str, context: str = "") -> str:
    """
    Normalize a single requirement ID token to [V2G20-XXXX] form.

    Input may be any partial or corrupted form.
    Returns the normalized form, or the original if no pattern matches.
    """
    token = token.strip()

    # Already well-formed
    if _WELLFORMED_REQ_RE.fullmatch(token):
        return token

    # Try to extract the numeric ID from corrupted forms
    # First try: token looks like a known corruption pattern
    m = re.match(
        r'\[?(?:V2G20|V20G0|V2G2O|V2G0|2G20|G20|20)?-(\d{1,5})\]?$',
        token,
    )
    if m:
        normalized = f"[V2G20-{m.group(1)}]"
        _normalization_log.record(token, normalized, context)
        return normalized

    # Bare number with closing bracket: "1234]"
    m = re.match(r'(\d{1,5})\]$', token)
    if m:
        normalized = f"[V2G20-{m.group(1)}]"
        _normalization_log.record(token, normalized, context)
        return normalized

    return token


def normalize_text(text: str, context: str = "") -> str:
    """
    Normalize ALL requirement ID references in a block of text.

    Replaces every corrupted/partial V2G20 reference with its
    canonical [V2G20-XXXX] form.

    Returns the normalized text.
    """
    if not text:
        return text

    def _replacer(m: re.Match) -> str:
        original = m.group(0)
        num = m.group(1)
        normalized = f"[V2G20-{num}]"
        if original != normalized:
            _normalization_log.record(original, normalized, context)
        return normalized

    # Pass 1: Fix well-known corruptions with clear prefix
    # V20G0-XXXX, V2G2O-XXXX (transposition/OCR errors)
    result = re.sub(
        r'\[?(?:V20G0|V2G2O)-(\d{1,5})\]?',
        _replacer, text,
    )

    # Pass 2: Fix partial prefixes that still have enough signal
    # Must have at least "G20-" or "2G20-" or "V2G20-" prefix
    result = re.sub(
        r'\[?(?:V2G20|2G20|G20)-(\d{1,5})\]?',
        _replacer, result,
    )

    # Pass 3: Fix missing brackets on otherwise correct refs
    # "V2G20-1234" without brackets → "[V2G20-1234]"
    result = re.sub(
        r'(?<!\[)V2G20-(\d{1,5})(?!\])',
        lambda m: (
            _normalization_log.record(m.group(0), f"[V2G20-{m.group(1)}]", context)
            or f"[V2G20-{m.group(1)}]"
        ),
        result,
    )

    return result


def extract_req_ids(text: str) -> list[str]:
    """
    Extract all V2G20-XXXX requirement IDs from text AFTER normalization.

    Returns list of normalized IDs like ["V2G20-1234", "V2G20-5678"].
    (Without brackets, as used internally.)
    """
    normalized = normalize_text(text)
    return [f"V2G20-{m.group(1)}" for m in _WELLFORMED_REQ_RE.finditer(normalized)]


def normalize_req_id_bare(bare_id: str, context: str = "") -> str:
    """
    Normalize a bare requirement ID (without brackets).

    Input: "V2G20-1234" or "V20G0-1234" etc.
    Output: "V2G20-1234"
    """
    bare_id = bare_id.strip()
    m = re.match(
        r'(?:V2G20|V20G0|V2G2O|V2G0|2G20|G20|20)?-(\d{1,5})$',
        bare_id,
    )
    if m:
        normalized = f"V2G20-{m.group(1)}"
        if bare_id != normalized:
            _normalization_log.record(bare_id, normalized, context)
        return normalized
    return bare_id


def normalize_ref_list(refs: list[str], context: str = "") -> list[str]:
    """Normalize a list of bare requirement IDs."""
    return [normalize_req_id_bare(r, context) for r in refs]
