"""
table_stitcher.py — Reconstruct multi-page tables from per-page table blocks.

Problem
-------
PaddleOCR outputs one table block per page. When an ISO 15118-20 table spans
multiple pages, the PDF renderer repeats the header row at the top of each
continuation page. We need to:

  1. Detect that a table block on page N+1 is a continuation of the table
     that ended at the bottom of page N.
  2. Strip the duplicated header row from the continuation.
  3. Append the data rows to the same Table object.

Continuation detection criteria (all must hold):
  a. There is an open table from the previous page.
  b. The new table block appears as the FIRST content block on the page.
  c. Column count of the new block matches the open table.
  d. Header similarity >= threshold (default 0.85).
     Similarity = fraction of column headers that match case-insensitively.

Table content format from PaddleOCR (markdown pipe-table):
    | Field Name | Type | M/O | Description |
    |---|---|---|---|
    | EVSEId     | string | M | Unique identifier ... |
"""

from __future__ import annotations

import re
from models import RawBlock, Table, TableRow

# Separator row cells: only dashes, colons, and whitespace
_SEPARATOR_RE = re.compile(r"^\s*[-:]+\s*$")


def parse_markdown_table(content: str) -> tuple[list[str], list[TableRow]]:
    """
    Parse a PaddleOCR pipe-table string into (header, rows).

    Returns ([], []) if content does not look like a valid pipe-table.
    The alignment separator row is consumed and not included in output.
    """
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    if not lines:
        return [], []

    header:        list[str]      = []
    rows:          list[TableRow] = []
    separator_seen: bool          = False

    for line in lines:
        if not line.startswith("|"):
            # Non-pipe line — could be HTML table fragment; skip
            continue

        # Split on | and strip; drop the empty cells from leading/trailing |
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells:
            continue

        # Detect separator row (|---|---|)
        if all(_SEPARATOR_RE.match(c) for c in cells if c):
            separator_seen = True
            continue

        if not separator_seen:
            header = cells
        else:
            rows.append(TableRow(cells=cells))

    return header, rows


def _header_similarity(h1: list[str], h2: list[str]) -> float:
    """
    Fraction of column headers that match case-insensitively after stripping.
    Returns 0.0 if the column counts differ.
    """
    if not h1 or not h2 or len(h1) != len(h2):
        return 0.0
    matches = sum(1 for a, b in zip(h1, h2) if a.lower() == b.lower())
    return matches / len(h1)


class TableStitcher:
    """
    Stateful stitcher.  Feed it blocks one at a time across all pages and
    it accumulates Table objects, merging continuations automatically.

    Usage:
        stitcher = TableStitcher()
        for page in pages:
            ordered = [b for b in page.blocks if b.order is not None]
            for i, block in enumerate(ordered):
                stitcher.feed(block, is_first_on_page=(i == 0),
                              page=page.page_index)
        stitcher.close()
        tables = stitcher.tables
    """

    def __init__(self, similarity_threshold: float = 0.85) -> None:
        self.tables:          list[Table]   = []
        self._open:           Table | None  = None
        self._counter:        int           = 0
        self._threshold:      float         = similarity_threshold
        self._pending_caption: str | None   = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def feed(
        self,
        block: RawBlock,
        is_first_on_page: bool = False,
        page: int | None = None,
    ) -> None:
        """Process a single block."""
        pg = page if page is not None else block.page

        # Table caption (table_title) always immediately precedes its table
        if block.label == "table_title":
            self._pending_caption = block.content.strip()
            return

        if block.label != "table":
            # Any non-table content closes the continuation window
            if block.label not in ("paragraph_title", "figure_title"):
                # Paragraph titles and figure titles between pages don't break
                # tables (they appear in running headers on some pages).
                self._open = None
            return

        # ── Parse the table block ──────────────────────────────────────
        header, rows = parse_markdown_table(block.content)

        if not header and not rows:
            # Unparseable table — close open table and skip
            self._open = None
            return

        # ── Decide: continuation or new table? ────────────────────────
        if (
            self._open is not None
            and is_first_on_page
            and _header_similarity(self._open.header, header) >= self._threshold
        ):
            # Continuation page: append rows, skip duplicate header
            self._open.rows.extend(rows)
            if pg not in self._open.pages:
                self._open.pages.append(pg)
            # Discard any repeated caption on continuation page
            self._pending_caption = None

        else:
            # New table
            self._counter += 1
            t = Table(
                table_id=f"T{self._counter:04d}",
                caption=self._pending_caption,
                header=header,
                rows=rows,
                pages=[pg],
            )
            self.tables.append(t)
            self._open = t
            self._pending_caption = None

    def close(self) -> None:
        """Explicitly close any open table at end of document."""
        self._open = None