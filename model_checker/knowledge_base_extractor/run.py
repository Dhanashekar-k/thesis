"""
run.py — Stage 1 pipeline orchestrator.

Usage
-----
    python run.py --input-dir /path/to/ocr_output --output knowledge_base.json

Pipeline order (order matters):
  1. loader.py        — reads _res.json + .md, filters noise, sorts blocks
  2. section_parser   — tracks current section as blocks are consumed
  3. table_stitcher   — detects multi-page table continuations
  4. figure_catalog   — matches image blocks to figure_title blocks
  5. req_extractor    — finds V2G20-XXXX IDs in text blocks
  6. knowledge_base   — accumulates everything, serialises to JSON

Key ordering constraint: SectionParser must run first per-page so that the
section_id context is available when RequirementExtractor runs on each block.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from loader import load_all_pages
from section_parser import SectionParser
from requirement_extractor import extract_requirements_from_block
from table_stitcher import TableStitcher
from figure_catalog import FigureCatalog
from knowledge_base import KnowledgeBase


def run_pipeline(
    input_dir: str,
    output_path: str,
    verbose: bool = True,
) -> KnowledgeBase:

    t0 = time.perf_counter()

    # ── 1. Load all pages ───────────────────────────────────────────────
    pages = load_all_pages(input_dir, verbose=verbose)
    if not pages:
        print("[ERROR] No pages found. Check --input-dir.", file=sys.stderr)
        sys.exit(1)

    # ── 2. Initialise handlers ──────────────────────────────────────────
    section_parser = SectionParser()
    table_stitcher = TableStitcher(similarity_threshold=0.85)
    figure_catalog = FigureCatalog()
    kb             = KnowledgeBase(total_pages=len(pages))

    # ── 3. Process page by page ─────────────────────────────────────────
    for page in pages:
        # Ordered blocks are text/table/paragraph_title in reading order.
        # Unordered blocks are image and figure_title (block_order is None).
        ordered   = [b for b in page.blocks if b.order is not None]
        unordered = [b for b in page.blocks if b.order is None]
        # loader.py already sorts unordered by y-position (image before caption)

        # ── 3a. Section parser sees ordered blocks first ────────────────
        section_parser.process_page(page)

        # ── 3b. Walk ordered blocks ─────────────────────────────────────
        for block_idx, block in enumerate(ordered):
            is_first = (block_idx == 0)

            # TableStitcher
            table_stitcher.feed(
                block,
                is_first_on_page=is_first,
                page=page.page_index,
            )

            # FigureCatalog (ordered — rare but possible for inline captions)
            figure_catalog.feed(block, img_dir=page.image_dir)

            # RequirementExtractor — text blocks only
            if block.label == "text":
                current_sec = section_parser._current
                section_id  = current_sec.clause_id if current_sec else None
                reqs        = extract_requirements_from_block(
                    block, section_id=section_id
                )
                for req in reqs:
                    kb.add_requirement(req)
                    # Also attach to section for quick section-level lookup
                    if current_sec is not None and req not in current_sec.requirements:
                        current_sec.requirements.append(req)

        # ── 3c. Walk unordered blocks (image + figure_title) ────────────
        # These are sorted by y-position by loader.py so image precedes
        # its figure_title caption even though both have order=None.
        for block in unordered:
            figure_catalog.feed(block, img_dir=page.image_dir)

    # ── 4. Finalise handlers ────────────────────────────────────────────
    table_stitcher.close()

    kb.sections = section_parser.get_sections()
    kb.tables   = table_stitcher.tables
    kb.figures  = figure_catalog.figures

    _annotate_table_sections(kb)

    # ── 5. Report ───────────────────────────────────────────────────────
    elapsed = time.perf_counter() - t0
    if verbose:
        print()
        print("─" * 52)
        print(f"  Stage 1 complete  ({elapsed:.1f}s)")
        print("─" * 52)
        print(f"  Pages processed   : {len(pages)}")
        print(f"  Sections found    : {len(kb.sections)}")
        print(f"  Unique req IDs    : {len(kb.requirements)}")
        print(f"  Tables            : {len(kb.tables)}")
        print(f"  Multi-page tables : {sum(1 for t in kb.tables if len(t.pages) > 1)}")
        print(f"  Figures           : {len(kb.figures)}")
        print("─" * 52)

    kb.save(output_path)
    return kb


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _annotate_table_sections(kb: KnowledgeBase) -> None:
    """
    Best-effort: set Table.section_id by finding which section was active
    on the table's first page.  We pick the section whose first page is the
    highest page number still <= the table's first page (i.e. the most recent
    section that had already started before the table appeared).
    """
    # Map: page_number → last section to open on that page
    page_to_section: dict[int, object] = {}
    for sec in kb.sections:
        if sec.pages:
            pg = sec.pages[0]
            page_to_section[pg] = sec   # later sections on same page win

    for table in kb.tables:
        if not table.pages:
            continue
        first_page = table.pages[0]
        # Walk backwards up to 50 pages to find the owning section
        for pg in range(first_page, max(0, first_page - 50), -1):
            if pg in page_to_section:
                table.section_id = page_to_section[pg].clause_id
                break


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 1 — Extract knowledge from PaddleOCR output",
    )
    parser.add_argument(
        "--input-dir", "-i",
        required=True,
        help=(
            "Directory containing iso20_spec_N.md and "
            "iso20_spec_N_res.json files, plus an imgs/ subdirectory"
        ),
    )
    parser.add_argument(
        "--output", "-o",
        default="knowledge_base.json",
        help="Output path for the knowledge base JSON (default: knowledge_base.json)",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output",
    )
    args = parser.parse_args()

    run_pipeline(
        input_dir=args.input_dir,
        output_path=args.output,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()