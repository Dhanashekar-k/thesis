"""
models.py — Core dataclasses for Stage 1 knowledge extraction.

Every downstream stage (FSM enrichment, NuSMV generation) consumes these
structures. Keep fields stable — changes here ripple everywhere.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RawBlock:
    """
    A single layout block from PaddleOCR _res.json.

    label    : PaddleOCR label — 'text', 'paragraph_title', 'table',
               'table_title', 'image', 'figure_title', etc.
    order    : reading order within the page (None for decorative/structural
               blocks: headers, footers, page numbers).
    bbox     : (x1, y1, x2, y2) in PDF pixel coordinates.
    group_id : PaddleOCR group assignment (blocks sharing a group_id belong
               to the same logical unit, e.g. image + caption).
    """
    page:     int
    block_id: int
    label:    str
    content:  str
    bbox:     tuple[int, int, int, int]
    order:    Optional[int]
    group_id: int


@dataclass
class Requirement:
    """
    A single normative requirement identified by a V2G20-XXXX tag.

    req_id     : canonical ID, e.g. "V2G20-1747"
    text       : the sentence (or short paragraph) containing the ID
    page       : source page number
    section_id : clause number of the enclosing section, e.g. "8.4.3.2"
                 (None if undetermined)
    """
    req_id:     str
    text:       str
    page:       int
    section_id: Optional[str] = None


@dataclass
class Section:
    """
    A single clause/section of the document.

    clause_id      : dotted clause number, e.g. "7.9.2.5"
                     Empty string for unnumbered sections (Foreword, Annex etc.)
    title          : section heading text
    content_blocks : all RawBlocks belonging to this section, in reading order
    pages          : sorted list of page numbers this section spans
    requirements   : V2G20 requirements found inside this section
    """
    clause_id:      str
    title:          str
    content_blocks: list[RawBlock]    = field(default_factory=list)
    pages:          list[int]         = field(default_factory=list)
    requirements:   list[Requirement] = field(default_factory=list)


@dataclass
class TableRow:
    cells: list[str]


@dataclass
class Table:
    """
    A (possibly multi-page) table reconstructed by TableStitcher.

    table_id   : auto-assigned sequential ID, e.g. "T0012"
    caption    : text from the preceding table_title block, if any
    header     : column names from the first header row
    rows       : all data rows (header row excluded)
    pages      : source pages — len > 1 means multi-page table
    section_id : clause number of the enclosing section
    """
    table_id:   str
    caption:    Optional[str]
    header:     list[str]
    rows:       list[TableRow]
    pages:      list[int]         = field(default_factory=list)
    section_id: Optional[str]    = None


@dataclass
class Figure:
    """
    A figure (image block) and its caption.

    figure_id  : normalised ID extracted from caption, e.g. "Figure 215"
    image_path : absolute path to the cropped .jpg file (empty if not found)
    bbox       : bounding box of the image block in the source PDF page
    """
    figure_id:  str
    caption:    str
    image_path: str
    page:       int
    bbox:       tuple[int, int, int, int]


@dataclass
class PageData:
    """
    Everything extracted from a single PDF page.

    blocks    : content blocks in reading order (noise already removed by loader)
    image_dir : directory containing the cropped image files for this page
    """
    page_index: int
    blocks:     list[RawBlock]
    md_content: str
    image_dir:  str