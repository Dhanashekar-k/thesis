"""
section_processor.py — Section-level document processor.

Reads and merges content from BOTH data sources per the spec:
  - .md files  → PRIMARY semantic content (text, requirements, tables)
  - JSON files → STRUCTURAL metadata (block labels, bboxes, reading order,
                  multi-page continuity, text ↔ table ↔ image linkage)

Processes ALL sections from the knowledge base, section-by-section (not
page-by-page), with full multi-page merging for text, tables, and images.

Each section yields a SectionChunk containing:
  - merged markdown text (from .md)
  - extracted HTML tables with titles and metadata (from JSON block structure)
  - image references with captions and bounding boxes (from JSON)
  - requirement IDs found in the section
  - provenance tracking
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Data classes for processed sections
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TableBlock:
    """A single logical table extracted from one or more pages."""
    title: str
    html: str
    page_span: list[int]
    clause_context: str = ""
    bbox: Optional[list[int]] = None

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "html": self.html,
            "page_span": self.page_span,
            "clause_context": self.clause_context,
        }


@dataclass
class ImageRef:
    """Reference to an image/figure found in the section."""
    caption: str
    image_path: str
    page: int
    bbox: Optional[list[int]] = None
    surrounding_text: str = ""

    def to_dict(self) -> dict:
        return {
            "caption": self.caption,
            "image_path": self.image_path,
            "page": self.page,
        }


@dataclass
class SectionChunk:
    """A fully processed section ready for VLM extraction."""
    clause_id: str
    title: str
    pages: list[int]
    merged_text: str          # semantic content from .md files
    tables: list[TableBlock]  # HTML tables with titles
    images: list[ImageRef]    # image references with captions
    requirement_ids: list[str]
    block_count: int = 0      # from JSON metadata

    def to_dict(self) -> dict:
        return {
            "clause_id": self.clause_id,
            "title": self.title,
            "pages": self.pages,
            "merged_text_length": len(self.merged_text),
            "table_count": len(self.tables),
            "image_count": len(self.images),
            "requirement_ids": self.requirement_ids,
            "block_count": self.block_count,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Page content readers
# ═══════════════════════════════════════════════════════════════════════════

def _read_md_page(md_dir: Path, page: int) -> str:
    """Read the markdown content for a single page."""
    fpath = md_dir / f"iso20_spec_{page}.md"
    if fpath.exists():
        return fpath.read_text(encoding="utf-8", errors="replace")
    return ""


def _read_json_page(json_dir: Path, page: int) -> list[dict]:
    """Read JSON blocks for a single page. Returns list of block dicts."""
    fpath = json_dir / f"iso20_spec_{page}_res.json"
    if not fpath.exists():
        return []
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
        return data.get("parsing_res_list", [])
    except (json.JSONDecodeError, OSError):
        return []


# ═══════════════════════════════════════════════════════════════════════════
# Multi-page table merging
# ═══════════════════════════════════════════════════════════════════════════

def _is_table_continuation(prev_blocks: list[dict], curr_blocks: list[dict]) -> bool:
    """
    Detect if a table on the current page is a continuation of a table
    from the previous page (multi-page table).

    Heuristics:
    1. Previous page ends with a table block (last non-header/footer block)
    2. Current page starts with a table block (first non-header/footer block)
    3. No section title between them
    """
    if not prev_blocks or not curr_blocks:
        return False

    # Find last content block on previous page
    prev_content = [b for b in prev_blocks
                    if b.get("block_label") not in ("header", "footer", "number",
                                                     "header_image", "footer_image")]
    curr_content = [b for b in curr_blocks
                    if b.get("block_label") not in ("header", "footer", "number",
                                                     "header_image", "footer_image")]

    if not prev_content or not curr_content:
        return False

    prev_last = prev_content[-1]
    curr_first = curr_content[0]

    # Both must be tables
    if prev_last.get("block_label") != "table" or curr_first.get("block_label") != "table":
        return False

    # Check that current page doesn't start with a new title before the table
    for b in curr_content:
        if b.get("block_label") == "table":
            return True
        if b.get("block_label") in ("paragraph_title", "figure_title"):
            # A title before the table means it's a new table
            title_text = b.get("block_content", "")
            if re.match(r"Table\s+\d+", title_text):
                return False  # New table with its own title
            break

    return True


def _merge_table_html(html1: str, html2: str) -> str:
    """
    Merge two HTML table fragments, being careful about row deduplication.

    For continuation tables, the second table may repeat the header row.
    We detect and remove duplicate headers.
    """
    from html.parser import HTMLParser

    class _RowExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.rows: list[str] = []
            self._in_row = False
            self._row_parts: list[str] = []
            self._depth = 0

        def handle_starttag(self, tag, attrs):
            if tag == "tr":
                self._in_row = True
                self._row_parts = [f"<tr>"]
            elif self._in_row:
                attr_str = " ".join(f'{k}="{v}"' for k, v in attrs)
                self._row_parts.append(f"<{tag} {attr_str}>" if attr_str else f"<{tag}>")

        def handle_endtag(self, tag):
            if tag == "tr" and self._in_row:
                self._row_parts.append("</tr>")
                self.rows.append("".join(self._row_parts))
                self._in_row = False
            elif self._in_row:
                self._row_parts.append(f"</{tag}>")

        def handle_data(self, data):
            if self._in_row:
                self._row_parts.append(data)

    ext1 = _RowExtractor()
    ext1.feed(html1)
    rows1 = ext1.rows

    ext2 = _RowExtractor()
    ext2.feed(html2)
    rows2 = ext2.rows

    if not rows2:
        return html1
    if not rows1:
        return html2

    # Check if first row of table2 matches first row of table1 (header duplication)
    if rows2 and rows1:
        # Simple text-content comparison after stripping tags
        def _text(html_str):
            return re.sub(r"<[^>]+>", "", html_str).strip().lower()

        if _text(rows2[0]) == _text(rows1[0]):
            rows2 = rows2[1:]  # skip duplicate header

    all_rows = rows1 + rows2
    return "<table>" + "".join(all_rows) + "</table>"


# ═══════════════════════════════════════════════════════════════════════════
# Image/figure extraction from JSON blocks
# ═══════════════════════════════════════════════════════════════════════════

def _extract_images_from_blocks(
    blocks: list[dict],
    page: int,
    md_dir: Path,
) -> list[ImageRef]:
    """
    Extract image references from JSON blocks on a single page.

    JSON blocks with label 'image' or 'chart' have bboxes but EMPTY content.
    The actual image files live in md_dir/imgs/ with naming pattern:
      img_in_image_box_{x1}_{y1}_{x2}_{y2}.jpg   (for label='image')
      img_in_chart_box_{x1}_{y1}_{x2}_{y2}.jpg   (for label='chart')
    Captions come from adjacent figure_title blocks.
    """
    images = []
    pending_caption = ""
    imgs_dir = md_dir / "imgs"

    # Map JSON block label → filename prefix
    _LABEL_TO_PREFIX = {
        "image": "image_box",
        "chart": "chart_box",
        "image_box": "image_box",
        "chart_box": "chart_box",
    }

    for i, block in enumerate(blocks):
        label = block.get("block_label", "")
        content = block.get("block_content", "")
        bbox = block.get("block_bbox")

        if label == "figure_title" and not re.match(r"Table\s+\d+", content):
            # This is likely a figure caption (not a table title)
            pending_caption = content

        elif label in _LABEL_TO_PREFIX:
            img_path = ""
            prefix = _LABEL_TO_PREFIX[label]

            if bbox:
                # Construct path from bbox — the actual file naming pattern
                bstr = f"img_in_{prefix}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.jpg"
                candidate = imgs_dir / bstr
                if candidate.exists():
                    img_path = str(candidate)

            # Gather surrounding text for context
            surrounding = ""
            for j in range(max(0, i - 2), min(len(blocks), i + 3)):
                if j != i and blocks[j].get("block_label") not in (
                    "header", "footer", "number", "image", "chart",
                    "image_box", "chart_box",
                ):
                    surrounding += blocks[j].get("block_content", "") + " "

            if img_path or pending_caption:
                images.append(ImageRef(
                    caption=pending_caption,
                    image_path=img_path,
                    page=page,
                    bbox=bbox,
                    surrounding_text=surrounding.strip()[:500],
                ))
                pending_caption = ""

    return images


# ═══════════════════════════════════════════════════════════════════════════
# Image extraction from .md text (fallback / reconciliation)
# ═══════════════════════════════════════════════════════════════════════════

_MD_IMG_RE = re.compile(r'<img\s+src="(imgs/[^"]+)"', re.IGNORECASE)


def _extract_images_from_md(
    md_text: str,
    page: int,
    md_dir: Path,
) -> list[ImageRef]:
    """
    Extract image references from .md content using <img src="imgs/..."> tags.

    The .md files use HTML img tags (not markdown ![]() syntax).
    This is the most reliable source for image paths.
    """
    images = []
    imgs_dir = md_dir / "imgs"

    for m in _MD_IMG_RE.finditer(md_text):
        rel_path = m.group(1)  # e.g. "imgs/img_in_image_box_300_243_947_1481.jpg"
        full_path = md_dir / rel_path
        if full_path.exists():
            # Try to find a caption: look for figure title near the img tag
            start = max(0, m.start() - 500)
            context_before = md_text[start:m.start()]
            caption = ""
            # Look for "Figure N — description" pattern nearby
            cap_match = re.search(
                r'(Figure\s+\d+\s*[\u2014\-\u2013]+\s*.+?)(?:\n|$)',
                context_before,
            )
            if cap_match:
                caption = cap_match.group(1).strip()

            images.append(ImageRef(
                caption=caption,
                image_path=str(full_path),
                page=page,
            ))

    return images


# ═══════════════════════════════════════════════════════════════════════════
# Table extraction from JSON blocks
# ═══════════════════════════════════════════════════════════════════════════

def _extract_tables_from_blocks(
    blocks: list[dict],
    page: int,
) -> list[TableBlock]:
    """Extract table blocks from a page's JSON, preserving titles from figure_title."""
    tables = []
    pending_title = ""
    clause_context = ""

    for block in blocks:
        label = block.get("block_label", "")
        content = block.get("block_content", "")

        if label == "paragraph_title":
            clause_context = content
        elif label == "figure_title":
            pending_title = content
        elif label == "table" and content.strip():
            tables.append(TableBlock(
                title=pending_title,
                html=content,
                page_span=[page],
                clause_context=clause_context,
                bbox=block.get("block_bbox"),
            ))
            pending_title = ""

    return tables


# ═══════════════════════════════════════════════════════════════════════════
# Requirement ID extraction (with normalization)
# ═══════════════════════════════════════════════════════════════════════════

from normalization import extract_req_ids as _norm_extract_req_ids, normalize_text


def _extract_requirement_ids(text: str) -> list[str]:
    """Extract all V2G20-XXXX requirement IDs from text AFTER normalization."""
    return _norm_extract_req_ids(text)


def _normalize_table_header(html: str) -> str:
    """Normalize table HTML header cells: lowercase, strip whitespace, collapse duplicates."""
    import re as _re
    def _norm_cell(m):
        tag = m.group(1)    # td or th
        attrs = m.group(2)  # any attributes
        content = m.group(3)
        # Collapse whitespace and normalize
        content = _re.sub(r'\s+', ' ', content).strip()
        return f"<{tag}{attrs}>{content}</{tag}>"
    # Only normalize header row cells (first <tr> block)
    return _re.sub(r'<(t[hd])([^>]*)>(.*?)</\1>', _norm_cell, html, count=20)


# ═══════════════════════════════════════════════════════════════════════════
# Main processor
# ═══════════════════════════════════════════════════════════════════════════

def process_all_sections(
    kb_data: dict,
    ocr_base_dir: Path,
    excluded_pages: list[int] | None = None,
) -> list[SectionChunk]:
    """
    Process ALL sections from the knowledge base.

    For each section:
    1. Read .md files for all pages in the section → merge into semantic text
    2. Read JSON files for structural metadata → extract tables, images, block order
    3. Handle multi-page table continuity
    4. Handle multi-page image captions (caption on prior page, image on next)
    5. Extract requirement IDs

    Returns list of SectionChunk, one per KB section.
    """
    excluded = set(excluded_pages or [])
    md_dir = ocr_base_dir / "markdown"
    json_dir = ocr_base_dir / "json"
    sections = kb_data.get("sections", [])

    results: list[SectionChunk] = []
    total_pages_processed = 0
    total_tables = 0
    total_images = 0

    # Cache previously-read JSON blocks per page for multi-page detection
    page_blocks_cache: dict[int, list[dict]] = {}

    for sec in sections:
        clause_id = sec.get("clause_id", "")
        title = sec.get("title", "")
        pages = sec.get("pages", [])

        # Filter excluded pages
        pages = [p for p in pages if p not in excluded]
        if not pages:
            continue

        # 1. Merge .md content for all pages in this section
        md_parts = []
        for page in pages:
            md_text = _read_md_page(md_dir, page)
            if md_text.strip():
                md_parts.append(md_text)
        merged_text = "\n\n".join(md_parts)

        # 2. Read JSON blocks for structural metadata
        all_tables: list[TableBlock] = []
        all_images: list[ImageRef] = []
        block_count = 0
        prev_blocks: list[dict] = []

        for page in pages:
            # Read blocks (with caching)
            if page not in page_blocks_cache:
                page_blocks_cache[page] = _read_json_page(json_dir, page)
            blocks = page_blocks_cache[page]
            block_count += len(blocks)

            # Extract tables from this page
            page_tables = _extract_tables_from_blocks(blocks, page)

            # Check for multi-page table continuation
            if page_tables and all_tables and prev_blocks:
                if _is_table_continuation(prev_blocks, blocks):
                    # Merge with last table from previous page
                    last_table = all_tables[-1]
                    cont_table = page_tables[0]
                    last_table.html = _merge_table_html(last_table.html, cont_table.html)
                    last_table.page_span.append(page)
                    page_tables = page_tables[1:]  # consume the continuation

            all_tables.extend(page_tables)

            # Extract images from this page — two sources:
            # 1. JSON blocks (have bbox + captions from figure_title)
            page_images_json = _extract_images_from_blocks(blocks, page, md_dir)
            # 2. .md text (has reliable <img src="imgs/..."> paths)
            page_md = _read_md_page(md_dir, page)
            page_images_md = _extract_images_from_md(page_md, page, md_dir)

            # Reconcile: .md paths are authoritative, JSON adds captions/bbox
            # Build set of paths already found from JSON
            json_paths = {img.image_path for img in page_images_json if img.image_path}
            md_paths = {img.image_path for img in page_images_md if img.image_path}

            # Start with JSON-extracted (they have captions + bbox)
            for img in page_images_json:
                if img.image_path:
                    all_images.append(img)

            # Add any .md images NOT already found via JSON
            for img in page_images_md:
                if img.image_path and img.image_path not in json_paths:
                    all_images.append(img)

            # Also enrich JSON images that lack paths with .md paths
            if page_images_json and md_paths:
                for img in page_images_json:
                    if not img.image_path and md_paths:
                        # Assign first unmatched .md path
                        unmatched = md_paths - json_paths
                        if unmatched:
                            img.image_path = unmatched.pop()
                            if img not in all_images:
                                all_images.append(img)

            prev_blocks = blocks

        # 3. Normalize merged text (fix OCR-corrupted requirement IDs)
        merged_text = normalize_text(merged_text, context=f"section_{clause_id}")

        # 4. Normalize table headers
        for tb in all_tables:
            tb.html = _normalize_table_header(tb.html)

        # 5. Extract requirement IDs from normalized merged text
        req_ids = _extract_requirement_ids(merged_text)

        # 4. Handle cross-page captions: if last block of prev page is figure_title
        # and first block of next page is image, link them
        # (already handled in _extract_images_from_blocks via pending_caption)

        chunk = SectionChunk(
            clause_id=clause_id,
            title=title,
            pages=pages,
            merged_text=merged_text,
            tables=all_tables,
            images=all_images,
            requirement_ids=req_ids,
            block_count=block_count,
        )
        results.append(chunk)

        total_pages_processed += len(pages)
        total_tables += len(all_tables)
        total_images += len(all_images)

    print(f"[section_processor] Processed {len(results)} sections, "
          f"{total_pages_processed} pages, "
          f"{total_tables} tables, {total_images} images")

    return results
