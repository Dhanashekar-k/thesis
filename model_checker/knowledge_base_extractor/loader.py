"""loader.py — Load PaddleOCR output for individual pages or an entire directory.

Expected directory layout:
    <base_dir>/
        json/
            iso20_spec_<N>_res.json
        markdown/
            iso20_spec_<N>.md
            imgs/
                img_in_image_box_<x1>_<y1>_<x2>_<y2>.jpg

Example:
    OCR_output_1.5/
        json/
        markdown/
            imgs/
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator

from models import RawBlock, PageData

# Block labels that carry no semantic content — always excluded.
_NOISE_LABELS: frozenset[str] = frozenset({
    "header",
    "footer",
    "number",        # page number block
    "footer_image",
    "header_image",
    "aside_text",
    "footnote",
    "seal",
})

# Matches the page index in filenames like "iso20_spec_25_res.json"
_PAGE_INDEX_RE = re.compile(r"iso20_spec_(\d+)_res\.json$")


def _get_layout_paths(base_dir: str | Path) -> tuple[Path, Path, Path]:
    """
    Resolve the PaddleOCR 1.5 directory layout.

    Returns:
        (json_dir, markdown_dir, image_dir)
    """
    base = Path(base_dir)
    json_dir = base / "json"
    markdown_dir = base / "markdown"
    image_dir = markdown_dir / "imgs"

    if not json_dir.exists():
        raise FileNotFoundError(f"JSON directory not found: {json_dir}")

    if not markdown_dir.exists():
        raise FileNotFoundError(f"Markdown directory not found: {markdown_dir}")

    # imgs may not always exist for every run, so do not hard-fail unless you want strict behavior
    return json_dir, markdown_dir, image_dir


def load_page(page_index: int, base_dir: str | Path) -> PageData:
    """
    Load and return a PageData for the given page index.

    Raises FileNotFoundError if the JSON file does not exist.
    The markdown file is optional — if missing, md_content is set to "".
    """
    json_dir, markdown_dir, image_dir = _get_layout_paths(base_dir)

    json_path = json_dir / f"iso20_spec_{page_index}_res.json"
    md_path = markdown_dir / f"iso20_spec_{page_index}.md"

    if not json_path.exists():
        raise FileNotFoundError(f"OCR result not found: {json_path}")

    with json_path.open(encoding="utf-8") as fh:
        raw = json.load(fh)

    md_content = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    blocks = _parse_blocks(raw["parsing_res_list"], page_index)

    return PageData(
        page_index=page_index,
        blocks=blocks,
        md_content=md_content,
        image_dir=str(image_dir),
    )


def load_all_pages(base_dir: str | Path, verbose: bool = True) -> list[PageData]:
    """
    Discover and load every page present in base_dir/json, in page-number order.

    Pages that fail to load are skipped with a warning rather than aborting
    the run — a single corrupt JSON should not stop a large job.
    """
    json_dir, _, _ = _get_layout_paths(base_dir)
    json_files = sorted(json_dir.glob("iso20_spec_*_res.json"))

    page_indices: list[int] = []
    for f in json_files:
        m = _PAGE_INDEX_RE.search(f.name)
        if m:
            page_indices.append(int(m.group(1)))
    page_indices.sort()

    if verbose:
        print(f"[loader] Found {len(page_indices)} pages in {json_dir}")

    pages: list[PageData] = []
    for idx in page_indices:
        try:
            pages.append(load_page(idx, base_dir))
        except Exception as exc:
            print(f"[loader][WARN] Skipping page {idx}: {exc}")

    return pages


def iter_pages(base_dir: str | Path) -> Iterator[PageData]:
    """Lazy iterator — yields one PageData at a time to keep memory low."""
    json_dir, _, _ = _get_layout_paths(base_dir)
    json_files = sorted(json_dir.glob("iso20_spec_*_res.json"))

    for f in json_files:
        m = _PAGE_INDEX_RE.search(f.name)
        if not m:
            continue
        idx = int(m.group(1))
        try:
            yield load_page(idx, base_dir)
        except Exception as exc:
            print(f"[loader][WARN] Skipping page {idx}: {exc}")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_blocks(raw_blocks: list[dict], page: int) -> list[RawBlock]:
    """
    Parse parsing_res_list from the JSON, filter noise, and return
    content blocks with ordered blocks first (sorted by block_order),
    followed by unordered blocks sorted by y-position.

    This ordering guarantees that:
      - SectionParser and RequirementExtractor always see text in reading order.
      - FigureCatalog always sees an image block before its figure_title.
    """
    ordered: list[RawBlock] = []
    unordered: list[RawBlock] = []

    for b in raw_blocks:
        label = b.get("block_label", "unknown")
        content = b.get("block_content", "").strip()

        # Drop noise labels entirely
        if label in _NOISE_LABELS:
            continue

        # Skip empty content except for image blocks (they carry no text)
        if not content and label != "image":
            continue

        bbox_raw = b.get("block_bbox", [0, 0, 0, 0])
        block = RawBlock(
            page=page,
            block_id=b.get("block_id", -1),
            label=label,
            content=content,
            bbox=tuple(bbox_raw),
            order=b.get("block_order"),
            group_id=b.get("group_id", -1),
        )

        if block.order is not None:
            ordered.append(block)
        else:
            unordered.append(block)

    ordered.sort(key=lambda b: b.order)
    unordered.sort(key=lambda b: b.bbox[1])  # sort by top-y so image < caption

    return ordered + unordered