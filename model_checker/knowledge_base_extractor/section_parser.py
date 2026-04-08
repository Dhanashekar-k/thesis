"""
section_parser.py — Detect section boundaries and build a flat Section list.

ISO 15118-20 uses this PaddleOCR pattern for numbered clauses:

    paragraph_title  "3.5"                 ← bare clause number
    paragraph_title  "certificate"         ← term / section title
    text             "electronic document ..."

    paragraph_title  "3.8"
    paragraph_title  "charging station operator"
    paragraph_title  "CSO"                 ← abbreviation (3rd consecutive title)
    text             "secondary actor ..."

And for top-level unnumbered sections:
    paragraph_title  "Foreword"
    text             ...

The parser is intentionally lenient: blocks that don't match any expected
pattern are still assigned to the current open section so no content is lost.
"""

from __future__ import annotations

import re
from models import RawBlock, PageData, Section

# Dotted clause number: 3, 3.5, 7.9.2.5, A.1.2 (supports Annex letters)
_CLAUSE_RE = re.compile(r"^([A-Z]|\d+)(?:\.\d+){0,6}$")

# Inline clause + title in one block: "7.9.2.5 Certificate installation"
_INLINE_RE = re.compile(r"^((?:[A-Z]|\d+)(?:\.\d+){0,6})\s{1,4}(.+)$")

# Abbreviation: short all-caps or mixed-caps word (CSO, EIM, PnC, TLS, BC, AC …)
_ABBREV_RE = re.compile(r"^[A-Z][A-Za-z]{0,7}$")


def _looks_like_clause(text: str) -> bool:
    return bool(_CLAUSE_RE.match(text.strip()))


def _parse_heading(text: str) -> tuple[str, str] | None:
    """
    Try to extract (clause_id, title) from a paragraph_title block.
    Returns None if the text is empty.

    Outcomes:
        ("3.5",  "")                  — standalone clause number
        ("7.9",  "Authorization")     — inline clause + title
        ("",     "Foreword")          — unnumbered heading
    """
    t = text.strip()
    if not t:
        return None

    if _CLAUSE_RE.match(t):
        return (t, "")

    m = _INLINE_RE.match(t)
    if m:
        return (m.group(1), m.group(2).strip())

    return ("", t)


class SectionParser:
    """
    Stateful parser that walks pages in order and builds a flat list of
    Section objects.  Nesting can be reconstructed later from clause_id
    prefix matching if needed.
    """

    def __init__(self) -> None:
        self._sections:       list[Section] = []
        self._current:        Section | None = None
        self._pending_clause: str | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_page(self, page: PageData) -> None:
        """Feed all ordered blocks from one page into the parser."""
        ordered = [b for b in page.blocks if b.order is not None]
        for block in ordered:
            self._process_block(block, page.page_index)

    def get_sections(self) -> list[Section]:
        return self._sections

    # ------------------------------------------------------------------
    # Internal state machine
    # ------------------------------------------------------------------

    def _process_block(self, block: RawBlock, page: int) -> None:
        label = block.label
        text  = block.content.strip()

        if label == "paragraph_title":
            self._handle_title_block(text, page)
        else:
            # Any non-title block closes the pending clause state
            self._pending_clause = None
            self._append_to_current(block, page)

    def _handle_title_block(self, text: str, page: int) -> None:
        """
        State machine for multi-block heading detection.

        Transitions:
          IDLE        + clause_number  → HAVE_CLAUSE
          HAVE_CLAUSE + title_text     → OPEN section, back to IDLE
          HAVE_CLAUSE + clause_number  → OPEN anon section for first,
                                         re-enter HAVE_CLAUSE
          IDLE        + plain text     → OPEN unnumbered section
          OPEN        + abbreviation   → attach abbreviation to section title
                                         (only if no content yet, same page)
          OPEN        + plain text     → OPEN new unnumbered section
        """
        parsed = _parse_heading(text)
        if parsed is None:
            return

        clause_id, title = parsed

        # ── Case 1: standalone clause number ──────────────────────────
        if clause_id and not title:
            if self._pending_clause:
                # Two bare numbers in a row — open anonymous section for first
                self._open_section(self._pending_clause, "", page)
            self._pending_clause = clause_id
            return

        # ── Case 2: inline "clause + title" ───────────────────────────
        if clause_id and title:
            self._pending_clause = None
            self._open_section(clause_id, title, page)
            return

        # ── Case 3: plain text heading (no clause number) ─────────────
        if self._pending_clause:
            # (a) pending clause + this title → open section
            self._open_section(self._pending_clause, text, page)
            self._pending_clause = None
            return

        if (
            self._current is not None
            and _ABBREV_RE.match(text)
            and page in self._current.pages           # same page as opening
            and len(self._current.content_blocks) == 0  # no body content yet
        ):
            # (b) abbreviation — append to section title, e.g. "CSO"
            self._current.title = f"{self._current.title} ({text})"
            return

        # (c) new unnumbered section (Foreword, Annex title, etc.)
        self._open_section("", text, page)

    def _open_section(self, clause_id: str, title: str, page: int) -> None:
        sec = Section(clause_id=clause_id, title=title, pages=[page])
        self._sections.append(sec)
        self._current = sec

    def _append_to_current(self, block: RawBlock, page: int) -> None:
        if self._current is None:
            # Content before any heading — open a synthetic root section
            self._open_section("", "PREAMBLE", block.page)
        if page not in self._current.pages:
            self._current.pages.append(page)
        self._current.content_blocks.append(block)