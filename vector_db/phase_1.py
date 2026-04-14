from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

IGNORED_BLOCK_LABELS = {
    "header",
    "header_image",
    "footer",
    "footer_image",
    "number",
    "footnote",
    "aside_text",
}

TEXTUAL_BLOCK_LABELS = {"text", "list", "figure_title", "paragraph_title"}
ARTIFACT_BLOCK_LABELS = {"image", "table"}

CLAUSE_ID_RE = re.compile(r"^(\d+(?:\.\d+)*|annex\s+[a-z])\b", re.IGNORECASE)
GENERIC_REQUIREMENT_RE = re.compile(r"\[([A-Z][A-Z0-9]{1,15}-\d{3,6})\]")
CAPTION_ID_RE = r"(?:[A-Z]\.\d+(?:\.\d+)*|[A-Z]|\d+(?:\.\d+)*)"
DASH_SEP_RE = r"(?:-|—|–|:)"
FIGURE_CAPTION_RE = re.compile(rf"^(figure|fig\.?)\s+({CAPTION_ID_RE})\s*{DASH_SEP_RE}\s*\S", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(rf"^table\s+({CAPTION_ID_RE})\s*{DASH_SEP_RE}\s*\S", re.IGNORECASE)
FIGURE_REF_RE = re.compile(rf"\b(?:figure|fig\.?)\s+({CAPTION_ID_RE})\b", re.IGNORECASE)
TABLE_REF_RE = re.compile(rf"\btable\s+({CAPTION_ID_RE})\b", re.IGNORECASE)
IMG_TAG_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)
MD_IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
HTML_TABLE_RE = re.compile(r"(<table\b.*?</table>)", re.IGNORECASE | re.DOTALL)
CENTERED_DIV_TEXT_RE = re.compile(r'<div[^>]*>\s*(.*?)\s*</div>', re.IGNORECASE | re.DOTALL)
WHITESPACE_RE = re.compile(r"\s+")


@dataclass
class SectionRecord:
    clause_id: str
    title: str
    pages: List[int]
    requirement_ids: List[str]
    block_count: int

    @property
    def section_id(self) -> str:
        if self.clause_id:
            return f"section:{self.clause_id}"
        return f"section:title:{slugify(self.title)}"


@dataclass
class BlockRecord:
    page_index: int
    block_id: int
    order_key: Tuple[int, int]
    label: str
    original_label: str
    text: str
    bbox: Optional[List[int]]
    group_id: Optional[int]
    block_order: Optional[int]
    image_path: Optional[str] = None
    markdown_table_html: Optional[str] = None
    section_id: Optional[str] = None
    heading_clause_id: Optional[str] = None
    heading_text: Optional[str] = None
    requirement_refs: List[str] = field(default_factory=list)
    figure_refs: List[str] = field(default_factory=list)
    table_refs: List[str] = field(default_factory=list)
    node_id: Optional[str] = None

    @property
    def is_substantive(self) -> bool:
        if self.label in ARTIFACT_BLOCK_LABELS:
            return True
        if self.label == "paragraph_title":
            return True
        if self.label == "figure_title":
            return True
        return bool(self.text)


@dataclass
class PageRecord:
    page_index: int
    page_count: Optional[int]
    width: Optional[int]
    height: Optional[int]
    json_path: str
    markdown_path: Optional[str]
    markdown_image_refs: List[str]
    markdown_image_paths: List[str]
    markdown_tables: List[str]
    section_candidates: List[SectionRecord]
    blocks: List[BlockRecord]
    node_id: Optional[str] = None


def norm_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text or "").strip()


def slugify(text: str) -> str:
    text = norm_text(text).lower()
    text = re.sub(r"[^a-z0-9._:-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "unknown"


def norm_title(text: str) -> str:
    text = norm_text(text).lower()
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def infer_page_index_from_name(path: Path) -> int:
    m = re.search(r"(\d+)(?:_res)?\.[^.]+$", path.name)
    if not m:
        raise ValueError(f"Could not infer page index from filename: {path}")
    return int(m.group(1))


def resolve_input_dirs(input_root: Optional[Path], json_dir: Optional[Path], markdown_dir: Optional[Path]) -> Tuple[Path, Path]:
    if json_dir and markdown_dir:
        return json_dir, markdown_dir
    if input_root is None:
        raise ValueError("Provide --input-root or both --json-dir and --markdown-dir")

    nested_json = input_root / "json"
    nested_md = input_root / "markdown"
    if nested_json.exists() and nested_md.exists():
        return nested_json, nested_md

    return input_root, input_root


def parse_markdown_image_refs(md_text: str) -> List[str]:
    refs: List[str] = []
    refs.extend(IMG_TAG_RE.findall(md_text or ""))
    refs.extend(MD_IMG_RE.findall(md_text or ""))
    out: List[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


def parse_markdown_tables(md_text: str) -> List[str]:
    return [norm_text(t) for t in HTML_TABLE_RE.findall(md_text or "")]


def resolve_relative_path(base_dir: Path, ref: str) -> str:
    return str((base_dir / ref).resolve())


def title_looks_like_figure_or_table(text: str, kind: Optional[str] = None) -> bool:
    t = norm_text(text)
    if not t or len(t) > 260:
        return False
    if re.match(r"^(note|key)\b", t, flags=re.IGNORECASE):
        return False
    if kind == "figure":
        return bool(FIGURE_CAPTION_RE.match(t))
    if kind == "table":
        return bool(TABLE_CAPTION_RE.match(t))
    return bool(FIGURE_CAPTION_RE.match(t) or TABLE_CAPTION_RE.match(t))


def is_note_like(text: str) -> bool:
    return bool(re.match(r"^note\s*\d*\b", norm_text(text), flags=re.IGNORECASE))


def is_key_like(text: str) -> bool:
    return norm_text(text).lower() == "key"


def is_section_heading_like(text: str) -> bool:
    return bool(CLAUSE_ID_RE.match(norm_text(text)))


def extract_clause_id_from_heading(text: str) -> Optional[str]:
    t = norm_text(text)
    m = CLAUSE_ID_RE.match(t)
    if not m:
        return None
    value = m.group(1)
    return value.title() if value.lower().startswith("annex") else value


def heading_prefix_only(text: str) -> bool:
    t = norm_text(text)
    if not t:
        return False
    return bool(re.fullmatch(r"\d+(?:\.\d+)*", t) or re.fullmatch(r"annex\s+[a-z]", t, flags=re.IGNORECASE))


def heading_suffix_candidate(text: str) -> bool:
    t = norm_text(text)
    if not t:
        return False
    if heading_prefix_only(t):
        return False
    if title_looks_like_figure_or_table(t):
        return False
    if is_note_like(t) or is_key_like(t):
        return False
    if len(t) > 180:
        return False
    return True


def is_forward_figure_reference_text(text: str) -> bool:
    t = norm_text(text)
    if not t or FIGURE_CAPTION_RE.match(t):
        return False
    patterns = [
        rf"\bsee\s+figure\s+{CAPTION_ID_RE}\b",
        rf"\brefer\s+to\s+figure\s+{CAPTION_ID_RE}\b",
        rf"\bfigure\s+{CAPTION_ID_RE}\s+provides\b",
        rf"\bfigure\s+{CAPTION_ID_RE}\s+shows\b",
        rf"\bfigure\s+{CAPTION_ID_RE}\s+depicts\b",
        rf"\bfigure\s+{CAPTION_ID_RE}\s+illustrates\b",
    ]
    return any(re.search(p, t, flags=re.IGNORECASE) for p in patterns)


def is_secondary_figure_label(text: str) -> bool:
    t = norm_text(text)
    if not t:
        return False
    if title_looks_like_figure_or_table(t):
        return False
    if is_note_like(t) or is_key_like(t) or is_section_heading_like(t):
        return False
    if len(t) > 120 or len(t.split()) > 8:
        return False
    if re.search(rf"\bfigure\s+{CAPTION_ID_RE}\b", t, flags=re.IGNORECASE):
        return False
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_\-]*$", t))


def normalize_block_label(original_label: str, text: str) -> str:
    t = norm_text(text)
    if not t:
        return original_label
    if is_section_heading_like(t):
        return "paragraph_title"
    if original_label == "figure_title":
        if is_note_like(t):
            return "text"
        if is_forward_figure_reference_text(t):
            return "text"
        if is_key_like(t):
            return "paragraph_title"
    return original_label


def extract_requirement_refs(
    text: str,
    known_requirement_ids: Optional[set[str]] = None,
    known_requirement_prefixes: Optional[List[str]] = None,
) -> List[str]:
    if not text:
        return []
    found: List[str] = []
    seen: set[str] = set()

    for rid in GENERIC_REQUIREMENT_RE.findall(text):
        if known_requirement_ids is not None and rid not in known_requirement_ids:
            continue
        if rid not in seen:
            seen.add(rid)
            found.append(rid)

    if known_requirement_ids:
        # Recover partially broken OCR forms like [-1234] or [20-1234] by attaching known prefixes.
        fallback_digits = re.findall(r"\[(?:[A-Z0-9]{0,10})?-(\d{3,6})\]", text)
        prefixes = known_requirement_prefixes or sorted({rid.rsplit("-", 1)[0] for rid in known_requirement_ids})
        if len(prefixes) == 1:
            prefix = prefixes[0]
            for digits in fallback_digits:
                rid = f"{prefix}-{digits}"
                if rid in known_requirement_ids and rid not in seen:
                    seen.add(rid)
                    found.append(rid)

    return found


def extract_figure_numbers(text: str) -> List[str]:
    return [x for x in FIGURE_REF_RE.findall(text or "")]


def extract_table_numbers(text: str) -> List[str]:
    return [x for x in TABLE_REF_RE.findall(text or "")]


def extract_figure_caption_number(text: str) -> Optional[str]:
    m = FIGURE_CAPTION_RE.match(norm_text(text))
    return m.group(2) if m else None


def extract_table_caption_number(text: str) -> Optional[str]:
    m = TABLE_CAPTION_RE.match(norm_text(text))
    return m.group(1) if m else None


def block_starts_mid_paragraph(text: str) -> bool:
    t = norm_text(text)
    if not t:
        return False
    if is_section_heading_like(t) or is_note_like(t):
        return False
    if re.match(r"^\[?V2G20-\d{3,4}\]?", t):
        return False
    return t[:1].islower() or t.startswith((")", "]", ",", ";", ":", "and ", "or "))


def substantive_indices(blocks: List[BlockRecord]) -> List[int]:
    return [i for i, b in enumerate(blocks) if b.is_substantive]


def merge_html_parts(parts: Iterable[str]) -> str:
    values = [p for p in parts if p]
    return "\n\n".join(values)


def load_knowledge_base(kb_path: Optional[Path]) -> Tuple[Optional[dict], Dict[int, List[SectionRecord]], Dict[str, SectionRecord], set[str], List[str]]:
    if kb_path is None or not kb_path.exists():
        return None, {}, {}, set(), []
    kb = load_json(kb_path)
    page_to_sections: Dict[int, List[SectionRecord]] = {}
    section_by_clause: Dict[str, SectionRecord] = {}
    for raw in kb.get("sections", []):
        section = SectionRecord(
            clause_id=(raw.get("clause_id") or "").strip(),
            title=(raw.get("title") or "").strip(),
            pages=list(raw.get("pages", [])),
            requirement_ids=list(raw.get("requirement_ids", [])),
            block_count=int(raw.get("block_count", 0) or 0),
        )
        if section.clause_id:
            section_by_clause[section.clause_id] = section
        for p in section.pages:
            page_to_sections.setdefault(int(p), []).append(section)
    known_requirement_ids = set((kb.get("requirements") or {}).keys())
    for sec in section_by_clause.values():
        known_requirement_ids.update(sec.requirement_ids)
    prefixes = sorted({rid.rsplit("-", 1)[0] for rid in known_requirement_ids if "-" in rid})
    return kb, page_to_sections, section_by_clause, known_requirement_ids, prefixes


def page_can_continue_section(active_section_id: Optional[str], page_index: int, page_sections: List[SectionRecord], section_by_clause: Dict[str, SectionRecord]) -> Optional[str]:
    if not active_section_id:
        return None
    sec = section_by_clause.get(active_section_id)
    if not sec:
        return None
    if page_index in sec.pages:
        return active_section_id
    if active_section_id in {s.clause_id for s in page_sections if s.clause_id}:
        return active_section_id
    return None


class JsonlWriter:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = path.open("w", encoding="utf-8")
        self.count = 0
        self.written_ids: set[str] = set()

    def write(self, payload: dict, unique_id_key: Optional[str] = None) -> None:
        if unique_id_key:
            value = payload[unique_id_key]
            if value in self.written_ids:
                return
            self.written_ids.add(value)
        self.fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.count += 1

    def close(self) -> None:
        self.fh.close()


class EdgeWriter(JsonlWriter):
    def write_edge(self, src: str, rel: str, dst: str, **props: object) -> None:
        key = f"{src}|{rel}|{dst}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
        payload = {"src": src, "rel": rel, "dst": dst}
        if props:
            payload["props"] = props
        super().write(payload, unique_id_key=None if False else None)
        # manual de-dup because write() with a computed key would store the whole edge id externally


def write_edge_dedup(edge_writer: JsonlWriter, seen: set[str], src: str, rel: str, dst: str, **props: object) -> None:
    key = f"{src}|{rel}|{dst}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    if key in seen:
        return
    seen.add(key)
    payload = {"src": src, "rel": rel, "dst": dst}
    if props:
        payload["props"] = props
    edge_writer.write(payload)


def pair_input_files(json_dir: Path, markdown_dir: Path) -> Tuple[List[Path], Dict[int, Path]]:
    json_files: List[Path] = []
    for p in json_dir.glob("*.json"):
        try:
            infer_page_index_from_name(p)
        except ValueError:
            continue
        json_files.append(p)
    json_files = sorted(json_files, key=infer_page_index_from_name)
    if not json_files:
        raise FileNotFoundError(f"No page JSON files found in {json_dir}")

    markdown_files: Dict[int, Path] = {}
    for p in markdown_dir.glob("*.md"):
        try:
            page_idx = infer_page_index_from_name(p)
        except ValueError:
            continue
        markdown_files[page_idx] = p
    return json_files, markdown_files


def maybe_combine_heading_blocks(blocks: List[dict]) -> List[dict]:
    out: List[dict] = []
    i = 0
    while i < len(blocks):
        b = dict(blocks[i])
        original_label = b.get("block_label", "")
        effective_label = normalize_block_label(original_label, b.get("block_content", ""))
        b["effective_label"] = effective_label
        b["original_block_label"] = original_label

        if effective_label == "paragraph_title" and heading_prefix_only(b.get("block_content", "")) and i + 1 < len(blocks):
            nxt = dict(blocks[i + 1])
            nxt_original = nxt.get("block_label", "")
            nxt_effective = normalize_block_label(nxt_original, nxt.get("block_content", ""))
            nxt["effective_label"] = nxt_effective
            nxt["original_block_label"] = nxt_original
            if nxt_effective == "paragraph_title" and heading_suffix_candidate(nxt.get("block_content", "")):
                combined = dict(nxt)
                combined["block_content"] = f"{norm_text(b.get('block_content', ''))} {norm_text(nxt.get('block_content', ''))}".strip()
                combined["combined_from_block_ids"] = [b.get("block_id"), nxt.get("block_id")]
                out.append(combined)
                i += 2
                continue

        out.append(b)
        i += 1
    return out


def build_phase1(
    input_root: Optional[Path],
    json_dir: Optional[Path],
    markdown_dir: Optional[Path],
    kb_path: Optional[Path],
    output_root: Path,
    keep_ignored_blocks: bool = False,
) -> None:
    resolved_json_dir, resolved_md_dir = resolve_input_dirs(input_root, json_dir, markdown_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    kb, page_to_sections, section_by_clause, known_requirement_ids, known_requirement_prefixes = load_knowledge_base(kb_path)
    json_files, md_files_by_page = pair_input_files(resolved_json_dir, resolved_md_dir)

    sections_w = JsonlWriter(output_root / "sections.jsonl")
    pages_w = JsonlWriter(output_root / "pages.jsonl")
    blocks_w = JsonlWriter(output_root / "blocks.jsonl")
    text_units_w = JsonlWriter(output_root / "text_units.jsonl")
    figures_w = JsonlWriter(output_root / "figures.jsonl")
    tables_w = JsonlWriter(output_root / "tables.jsonl")
    edges_w = JsonlWriter(output_root / "edges.jsonl")
    edge_seen: set[str] = set()

    for sections in page_to_sections.values():
        for sec in sections:
            sections_w.write(
                {
                    "section_id": sec.section_id,
                    "clause_id": sec.clause_id,
                    "title": sec.title,
                    "pages": sec.pages,
                    "requirement_ids": sec.requirement_ids,
                    "block_count": sec.block_count,
                    "source": "knowledge_base",
                },
                unique_id_key="section_id",
            )

    page_records: List[PageRecord] = []
    active_section_id_global: Optional[str] = None

    for json_path in json_files:
        page_json = load_json(json_path)
        page_index = int(page_json.get("page_index") if page_json.get("page_index") is not None else infer_page_index_from_name(json_path))
        md_path = md_files_by_page.get(page_index)
        md_text = load_text(md_path) if md_path and md_path.exists() else ""
        md_image_refs = parse_markdown_image_refs(md_text)
        md_image_paths = [resolve_relative_path(resolved_md_dir, ref) for ref in md_image_refs]
        md_tables = parse_markdown_tables(md_text)

        page_sections = page_to_sections.get(page_index, [])
        title_to_section_map: Dict[str, List[SectionRecord]] = {}
        for sec in page_sections:
            key = norm_title(sec.title)
            if key:
                title_to_section_map.setdefault(key, []).append(sec)

        raw_blocks = list(page_json.get("parsing_res_list", []))
        prepped_blocks = maybe_combine_heading_blocks(raw_blocks)
        blocks: List[BlockRecord] = []
        image_counter = 0
        table_counter = 0
        for idx, raw in enumerate(prepped_blocks):
            label = raw.get("effective_label", raw.get("block_label", ""))
            original_label = raw.get("original_block_label", raw.get("block_label", ""))
            if not keep_ignored_blocks and label in IGNORED_BLOCK_LABELS:
                continue
            text = norm_text(raw.get("block_content", ""))
            image_path = None
            markdown_table_html = None
            if label == "image" and image_counter < len(md_image_paths):
                image_path = md_image_paths[image_counter]
                image_counter += 1
            elif label == "table" and table_counter < len(md_tables):
                markdown_table_html = md_tables[table_counter]
                table_counter += 1

            blocks.append(
                BlockRecord(
                    page_index=page_index,
                    block_id=int(raw.get("block_id", idx)),
                    order_key=(
                        int(raw.get("block_bbox", [10**9, 10**9, 10**9, 10**9])[1]),
                        int(raw.get("block_bbox", [10**9, 10**9, 10**9, 10**9])[0]),
                        10**9 if raw.get("block_order") is None else int(raw.get("block_order")),
                        int(raw.get("block_id", idx)),
                    ),
                    label=label,
                    original_label=original_label,
                    text=text,
                    bbox=raw.get("block_bbox"),
                    group_id=raw.get("group_id"),
                    block_order=raw.get("block_order"),
                    image_path=image_path,
                    markdown_table_html=markdown_table_html,
                    requirement_refs=extract_requirement_refs(text, known_requirement_ids, known_requirement_prefixes),
                    figure_refs=extract_figure_numbers(text),
                    table_refs=extract_table_numbers(text),
                )
            )

        blocks.sort(key=lambda b: b.order_key)
        section_anchors: List[Tuple[int, str]] = []
        for idx, b in enumerate(blocks):
            if b.label != "paragraph_title":
                continue
            clause_id = extract_clause_id_from_heading(b.text)
            matched_section_id: Optional[str] = None
            if clause_id and clause_id in section_by_clause:
                matched_section_id = clause_id
                b.heading_clause_id = clause_id
                b.heading_text = b.text
            else:
                hits = title_to_section_map.get(norm_title(b.text), [])
                if len(hits) == 1 and hits[0].clause_id:
                    matched_section_id = hits[0].clause_id
                    b.heading_clause_id = hits[0].clause_id
                    b.heading_text = hits[0].title
            if matched_section_id:
                section_anchors.append((idx, matched_section_id))

        carried_section_id = page_can_continue_section(active_section_id_global, page_index, page_sections, section_by_clause)
        if carried_section_id is None and len([s for s in page_sections if s.clause_id]) == 1:
            carried_section_id = [s for s in page_sections if s.clause_id][0].clause_id

        current_anchor_ptr = 0
        current_section_id = carried_section_id
        last_resolved_section_id: Optional[str] = carried_section_id
        for idx, b in enumerate(blocks):
            while current_anchor_ptr < len(section_anchors) and section_anchors[current_anchor_ptr][0] <= idx:
                current_section_id = section_anchors[current_anchor_ptr][1]
                current_anchor_ptr += 1
            matched_section_id = current_section_id
            if b.label == "paragraph_title" and b.heading_clause_id:
                matched_section_id = b.heading_clause_id
            if matched_section_id is None and idx == 0 and block_starts_mid_paragraph(b.text):
                matched_section_id = carried_section_id
            b.section_id = matched_section_id
            if matched_section_id:
                last_resolved_section_id = matched_section_id

        active_section_id_global = page_can_continue_section(last_resolved_section_id, page_index + 1, page_to_sections.get(page_index + 1, []), section_by_clause) or last_resolved_section_id

        page_record = PageRecord(
            page_index=page_index,
            page_count=page_json.get("page_count"),
            width=page_json.get("width"),
            height=page_json.get("height"),
            json_path=str(json_path.resolve()),
            markdown_path=str(md_path.resolve()) if md_path else None,
            markdown_image_refs=md_image_refs,
            markdown_image_paths=md_image_paths,
            markdown_tables=md_tables,
            section_candidates=page_sections,
            blocks=blocks,
        )
        page_record.node_id = f"page:{page_index}"
        page_records.append(page_record)

        pages_w.write(
            {
                "page_id": page_record.node_id,
                "page_index": page_index,
                "page_count": page_record.page_count,
                "width": page_record.width,
                "height": page_record.height,
                "json_path": page_record.json_path,
                "markdown_path": page_record.markdown_path,
                "markdown_image_refs": page_record.markdown_image_refs,
                "markdown_image_paths": page_record.markdown_image_paths,
                "candidate_section_ids": [s.clause_id for s in page_sections if s.clause_id],
                "candidate_section_titles": [s.title for s in page_sections if s.title],
            },
            unique_id_key="page_id",
        )

        last_block_id: Optional[str] = None
        for block in blocks:
            block.node_id = f"page:{page_index}:block:{block.block_id}"
            blocks_w.write(
                {
                    "block_id": block.node_id,
                    "page_index": page_index,
                    "source_block_id": block.block_id,
                    "block_label": block.label,
                    "original_block_label": block.original_label,
                    "block_order": block.block_order,
                    "group_id": block.group_id,
                    "text": block.text,
                    "bbox": block.bbox,
                    "image_path": block.image_path,
                    "markdown_table_html": block.markdown_table_html,
                    "section_id": block.section_id,
                    "heading_clause_id": block.heading_clause_id,
                    "heading_text": block.heading_text,
                    "requirement_refs": block.requirement_refs,
                    "figure_refs": block.figure_refs,
                    "table_refs": block.table_refs,
                },
                unique_id_key="block_id",
            )
            write_edge_dedup(edges_w, edge_seen, page_record.node_id, "contains_block", block.node_id)
            if block.section_id and block.section_id in section_by_clause:
                write_edge_dedup(edges_w, edge_seen, section_by_clause[block.section_id].section_id, "contains_block", block.node_id)
            if last_block_id:
                write_edge_dedup(edges_w, edge_seen, last_block_id, "next_block", block.node_id)
            last_block_id = block.node_id
            for rid in block.requirement_refs:
                write_edge_dedup(edges_w, edge_seen, block.node_id, "mentions_requirement", f"requirement:{rid}")

        for sec in page_sections:
            write_edge_dedup(edges_w, edge_seen, sec.section_id, "contains_page", page_record.node_id)

    page_by_idx = {p.page_index: p for p in page_records}
    assigned_title_blocks: set[str] = set()
    assigned_image_blocks: set[str] = set()
    assigned_table_blocks: set[str] = set()

    # Promote artifacts using caption-driven rules first.
    global_blocks: List[BlockRecord] = []
    global_index_by_node: Dict[str, int] = {}
    for page in page_records:
        for b in page.blocks:
            if b.node_id:
                global_index_by_node[b.node_id] = len(global_blocks)
            global_blocks.append(b)

    def is_caption_block(block: BlockRecord, kind: str) -> bool:
        if block.label not in {"figure_title", "paragraph_title", "text"}:
            return False
        return title_looks_like_figure_or_table(block.text, kind)

    def is_hard_boundary_before_artifact(block: BlockRecord) -> bool:
        if block.label == "paragraph_title" and not is_caption_block(block, "figure") and not is_caption_block(block, "table"):
            return True
        if block.label == "image":
            return True
        return False

    def first_substantive_index(page: PageRecord) -> Optional[int]:
        subs = substantive_indices(page.blocks)
        return subs[0] if subs else None

    def page_has_caption_before_idx(page: PageRecord, idx: int, kind: str) -> bool:
        for pos in range(0, idx):
            blk = page.blocks[pos]
            if is_caption_block(blk, kind):
                return True
        return False

    def find_first_table_after_caption(caption_idx: int) -> Optional[BlockRecord]:
        saw_page_break = False
        for j in range(caption_idx + 1, len(global_blocks)):
            cur = global_blocks[j]
            if cur.page_index != global_blocks[j - 1].page_index:
                saw_page_break = True
            if is_caption_block(cur, "table") or is_caption_block(cur, "figure"):
                return None
            if cur.label == "paragraph_title":
                return None
            if cur.label == "table" and cur.node_id and cur.node_id not in assigned_table_blocks:
                return cur
            if cur.label == "text" and cur.text and not is_note_like(cur.text) and not is_key_like(cur.text):
                if saw_page_break:
                    return None
        return None

    def collect_table_span(first_table: BlockRecord) -> List[BlockRecord]:
        parts: List[BlockRecord] = []
        page_idx = first_table.page_index
        pos = page_by_idx[page_idx].blocks.index(first_table)

        while True:
            page = page_by_idx[page_idx]
            # collect consecutive table blocks from current position until a hard boundary
            while pos < len(page.blocks):
                cur = page.blocks[pos]
                if cur.label == "table" and cur.node_id and cur.node_id not in assigned_table_blocks:
                    parts.append(cur)
                    assigned_table_blocks.add(cur.node_id)
                    pos += 1
                    continue
                if cur.label == "text" and (is_note_like(cur.text) or is_key_like(cur.text) or not cur.text):
                    pos += 1
                    continue
                break

            next_page = page_by_idx.get(page_idx + 1)
            if next_page is None:
                break
            first_idx = first_substantive_index(next_page)
            if first_idx is None:
                break
            first_blk = next_page.blocks[first_idx]
            if is_caption_block(first_blk, "table") or is_caption_block(first_blk, "figure"):
                break
            if first_blk.label == "paragraph_title":
                break
            if first_blk.label != "table":
                break
            if page_has_caption_before_idx(next_page, first_idx, "table") or page_has_caption_before_idx(next_page, first_idx, "figure"):
                break
            page_idx = next_page.page_index
            pos = first_idx

        return parts

    # Caption-driven tables: caption can be on previous page; table can span multiple following pages.
    for i, block in enumerate(global_blocks):
        if not block.node_id or block.node_id in assigned_title_blocks:
            continue
        if not is_caption_block(block, "table"):
            continue

        first_table = find_first_table_after_caption(i)
        if not first_table:
            continue
        parts = collect_table_span(first_table)
        if not parts:
            continue

        assigned_title_blocks.add(block.node_id)
        start_page = block.page_index
        end_page = max(x.page_index for x in parts)
        html_parts = [x.markdown_table_html or x.text for x in parts]
        table_node_id = f"table:page:{start_page}:block:{block.block_id}"
        tables_w.write(
            {
                "table_id": table_node_id,
                "page_indices": sorted({x.page_index for x in parts} | {block.page_index}),
                "start_page_index": start_page,
                "end_page_index": end_page,
                "caption": block.text,
                "caption_number": extract_table_caption_number(block.text),
                "section_id": next((x.section_id for x in parts if x.section_id), block.section_id),
                "table_block_ids": [x.node_id for x in parts],
                "caption_block_id": block.node_id,
                "raw_html": merge_html_parts(html_parts),
                "raw_html_parts": html_parts,
            },
            unique_id_key="table_id",
        )
        for x in parts:
            write_edge_dedup(edges_w, edge_seen, page_by_idx[x.page_index].node_id, "contains_table", table_node_id)
            write_edge_dedup(edges_w, edge_seen, table_node_id, "has_table_block", x.node_id)
        write_edge_dedup(edges_w, edge_seen, page_by_idx[block.page_index].node_id, "contains_table", table_node_id)
        write_edge_dedup(edges_w, edge_seen, table_node_id, "has_caption_block", block.node_id)

    # Fallback tables for uncaptioned table spans.
    for page in page_records:
        subs = substantive_indices(page.blocks)
        if not subs:
            continue
        i = 0
        while i < len(page.blocks):
            b = page.blocks[i]
            if b.label != "table" or not b.node_id or b.node_id in assigned_table_blocks:
                i += 1
                continue
            parts = [b]
            assigned_table_blocks.add(b.node_id)
            end_page = b.page_index
            html_parts = [b.markdown_table_html or b.text]
            cursor = global_index_by_node[b.node_id] + 1
            while cursor < len(global_blocks):
                cur = global_blocks[cursor]
                if is_caption_block(cur, "table") or is_caption_block(cur, "figure"):
                    break
                if cur.label == "paragraph_title":
                    break
                if cur.label == "text" and cur.text:
                    break
                if cur.label == "table" and cur.node_id and cur.node_id not in assigned_table_blocks:
                    parts.append(cur)
                    assigned_table_blocks.add(cur.node_id)
                    html_parts.append(cur.markdown_table_html or cur.text)
                    end_page = cur.page_index
                cursor += 1
            table_node_id = f"table:page:{b.page_index}:block:{b.block_id}:uncaptioned"
            tables_w.write(
                {
                    "table_id": table_node_id,
                    "page_indices": sorted({x.page_index for x in parts}),
                    "start_page_index": b.page_index,
                    "end_page_index": end_page,
                    "caption": None,
                    "caption_number": None,
                    "section_id": next((x.section_id for x in parts if x.section_id), b.section_id),
                    "table_block_ids": [x.node_id for x in parts],
                    "caption_block_id": None,
                    "raw_html": merge_html_parts(html_parts),
                    "raw_html_parts": html_parts,
                },
                unique_id_key="table_id",
            )
            for x in parts:
                write_edge_dedup(edges_w, edge_seen, page_by_idx[x.page_index].node_id, "contains_table", table_node_id)
                write_edge_dedup(edges_w, edge_seen, table_node_id, "has_table_block", x.node_id)
            i += 1

    figure_number_to_ids: Dict[str, List[str]] = {}

    def register_figure(fig_id: str, caption: Optional[str]) -> None:
        if not caption:
            return
        num = extract_figure_caption_number(caption)
        if num is None:
            return
        figure_number_to_ids.setdefault(num, []).append(fig_id)

    def find_preceding_image_for_caption(caption_idx: int) -> Optional[BlockRecord]:
        for k in range(caption_idx - 1, -1, -1):
            cur = global_blocks[k]
            if is_caption_block(cur, "figure"):
                break
            if cur.label == "image" and cur.node_id and cur.node_id not in assigned_image_blocks:
                return cur
        return None

    def find_following_image_for_caption(caption_idx: int) -> Optional[BlockRecord]:
        for k in range(caption_idx + 1, min(len(global_blocks), caption_idx + 12)):
            cur = global_blocks[k]
            if is_caption_block(cur, "figure") or is_caption_block(cur, "table"):
                break
            if cur.label == "paragraph_title" and not is_caption_block(cur, "figure"):
                break
            if cur.label == "image" and cur.node_id and cur.node_id not in assigned_image_blocks:
                return cur
        return None

    for i, block in enumerate(global_blocks):
        if not block.node_id or block.node_id in assigned_title_blocks:
            continue
        if not is_caption_block(block, "figure"):
            continue
        image_block = find_preceding_image_for_caption(i) or find_following_image_for_caption(i)
        if not image_block or not image_block.node_id:
            continue
        assigned_title_blocks.add(block.node_id)
        assigned_image_blocks.add(image_block.node_id)
        fig_id = f"figure:page:{image_block.page_index}:block:{image_block.block_id}"
        figures_w.write(
            {
                "figure_id": fig_id,
                "page_indices": sorted({block.page_index, image_block.page_index}),
                "start_page_index": min(block.page_index, image_block.page_index),
                "end_page_index": max(block.page_index, image_block.page_index),
                "caption": block.text,
                "caption_number": extract_figure_caption_number(block.text),
                "image_path": image_block.image_path,
                "image_block_id": image_block.node_id,
                "caption_block_id": block.node_id,
                "bbox": image_block.bbox,
                "section_id": image_block.section_id or block.section_id,
            },
            unique_id_key="figure_id",
        )
        register_figure(fig_id, block.text)
        write_edge_dedup(edges_w, edge_seen, page_by_idx[image_block.page_index].node_id, "contains_figure", fig_id)
        if block.page_index != image_block.page_index:
            write_edge_dedup(edges_w, edge_seen, page_by_idx[block.page_index].node_id, "contains_figure", fig_id)
        write_edge_dedup(edges_w, edge_seen, fig_id, "has_image_block", image_block.node_id)
        write_edge_dedup(edges_w, edge_seen, fig_id, "has_caption_block", block.node_id)

        img_idx = global_index_by_node[image_block.node_id]
        cap_idx = global_index_by_node[block.node_id]
        lo, hi = sorted((img_idx, cap_idx))
        for k in range(lo + 1, hi):
            mid = global_blocks[k]
            if not mid.node_id or mid.node_id in assigned_title_blocks:
                continue
            if mid.label in {"figure_title", "text"} and is_secondary_figure_label(mid.text):
                assigned_title_blocks.add(mid.node_id)
                write_edge_dedup(edges_w, edge_seen, fig_id, "has_secondary_label_block", mid.node_id)
    # Link figure/table references from blocks after all artifacts exist.
    for page in page_records:
        for b in page.blocks:
            if not b.node_id:
                continue
            for fig_no in b.figure_refs:
                for fig_id in figure_number_to_ids.get(fig_no, []):
                    write_edge_dedup(edges_w, edge_seen, b.node_id, "references_figure", fig_id, figure_number=fig_no)
            for tbl_no in b.table_refs:
                write_edge_dedup(edges_w, edge_seen, b.node_id, "references_table_number", f"table-number:{tbl_no}", table_number=tbl_no)

    # Build text units from contiguous raw text evidence.
    text_unit_counter = 0
    prev_text_unit_id: Optional[str] = None
    carry_open_unit: Optional[dict] = None

    def flush_unit(unit: Optional[dict]) -> Optional[str]:
        nonlocal text_unit_counter, prev_text_unit_id
        if not unit or not unit["block_ids"]:
            return None
        text_unit_counter += 1
        unit_id = f"text-unit:{text_unit_counter:06d}"
        payload = dict(unit)
        payload["text_unit_id"] = unit_id
        text_units_w.write(payload, unique_id_key="text_unit_id")
        for bid in payload["block_ids"]:
            write_edge_dedup(edges_w, edge_seen, unit_id, "has_block", bid)
        for pid in sorted(set(payload["page_ids"])):
            write_edge_dedup(edges_w, edge_seen, pid, "contains_text_unit", unit_id)
        if payload.get("section_id") and payload["section_id"] in section_by_clause:
            write_edge_dedup(edges_w, edge_seen, section_by_clause[payload["section_id"]].section_id, "contains_text_unit", unit_id)
        if prev_text_unit_id:
            write_edge_dedup(edges_w, edge_seen, prev_text_unit_id, "next_text_unit", unit_id)
        prev_text_unit_id = unit_id
        return unit_id

    for page in page_records:
        blocks = page.blocks
        unit = carry_open_unit
        if unit is not None and unit.get("closed"):
            unit = None
        if unit is not None:
            unit.pop("closed", None)
        for idx, b in enumerate(blocks):
            if b.label not in {"text"} or not b.text or not b.node_id:
                if unit and b.label in {"paragraph_title", "image", "table"}:
                    flush_unit(unit)
                    unit = None
                continue

            should_start_new = False
            if unit is None:
                should_start_new = True
            else:
                same_section = unit.get("section_id") == b.section_id
                previous_text = unit["text_parts"][-1] if unit["text_parts"] else ""
                if not same_section:
                    should_start_new = True
                elif b.page_index != unit["end_page_index"]:
                    if not block_starts_mid_paragraph(b.text):
                        should_start_new = True
                elif previous_text.endswith((".", ":", ";")) and not block_starts_mid_paragraph(b.text):
                    should_start_new = True

            if should_start_new:
                flush_unit(unit)
                unit = {
                    "page_indices": [b.page_index],
                    "page_ids": [page.node_id],
                    "start_page_index": b.page_index,
                    "end_page_index": b.page_index,
                    "section_id": b.section_id,
                    "block_ids": [b.node_id],
                    "text_parts": [b.text],
                    "text": b.text,
                    "requirement_refs": list(b.requirement_refs),
                }
            else:
                unit["page_indices"].append(b.page_index)
                unit["page_ids"].append(page.node_id)
                unit["end_page_index"] = b.page_index
                unit["block_ids"].append(b.node_id)
                unit["text_parts"].append(b.text)
                unit["text"] = norm_text(unit["text"] + " " + b.text)
                unit["requirement_refs"] = sorted(set(unit["requirement_refs"]) | set(b.requirement_refs))

        carry_open_unit = unit
        if carry_open_unit is not None:
            last_sub = substantive_indices(blocks)
            last_text_block = None
            for b in reversed(blocks):
                if b.label == "text" and b.text:
                    last_text_block = b
                    break
            can_continue = False
            if last_text_block and last_sub and blocks[last_sub[-1]].node_id == last_text_block.node_id:
                can_continue = not (carry_open_unit["text_parts"][-1].endswith((".", ":", ";")) and not block_starts_mid_paragraph(carry_open_unit["text_parts"][-1]))
            if not can_continue:
                flush_unit(carry_open_unit)
                carry_open_unit = None
            else:
                carry_open_unit["closed"] = True
                carry_open_unit.pop("closed", None)

    flush_unit(carry_open_unit)

    manifest = {
        "input_root": str(input_root.resolve()) if input_root else None,
        "json_dir": str(resolved_json_dir.resolve()),
        "markdown_dir": str(resolved_md_dir.resolve()),
        "kb_path": str(kb_path.resolve()) if kb_path else None,
        "outputs": {
            "sections": str((output_root / "sections.jsonl").resolve()),
            "pages": str((output_root / "pages.jsonl").resolve()),
            "blocks": str((output_root / "blocks.jsonl").resolve()),
            "text_units": str((output_root / "text_units.jsonl").resolve()),
            "figures": str((output_root / "figures.jsonl").resolve()),
            "tables": str((output_root / "tables.jsonl").resolve()),
            "edges": str((output_root / "edges.jsonl").resolve()),
        },
        "stats": {
            "section_count": sections_w.count,
            "page_count": pages_w.count,
            "block_count": blocks_w.count,
            "text_unit_count": text_units_w.count,
            "figure_count": figures_w.count,
            "table_count": tables_w.count,
            "edge_count": edges_w.count,
            "has_knowledge_base": kb is not None,
        },
        "notes": [
            "Phase 1 outputs canonical raw evidence records and structural links only.",
            "Handles split clause headings, section carryover, next-page figure captions, and multipage tables.",
            "Uses markdown order to recover image paths and table HTML without hardcoding document-specific rules.",
            "Unmatched images are preserved as untitled figures instead of being dropped.",
        ],
    }
    with (output_root / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    for writer in [sections_w, pages_w, blocks_w, text_units_w, figures_w, tables_w, edges_w]:
        writer.close()

    print(json.dumps(manifest["stats"], indent=2))
    print(f"Wrote manifest to {(output_root / 'manifest.json').resolve()}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 1 canonicalizer for OCR markdown/json outputs.")
    p.add_argument("--input-root", type=Path, default=None, help="Root containing json/ and markdown/ or a flat directory with both.")
    p.add_argument("--json-dir", type=Path, default=None, help="Explicit JSON directory.")
    p.add_argument("--markdown-dir", type=Path, default=None, help="Explicit markdown directory.")
    p.add_argument("--kb-path", type=Path, default=None, help="Optional knowledge_base.json.")
    p.add_argument("--output-root", type=Path, required=True, help="Output directory.")
    p.add_argument("--keep-ignored-blocks", action="store_true", help="Keep headers/footers/number blocks.")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    build_phase1(
        input_root=args.input_root,
        json_dir=args.json_dir,
        markdown_dir=args.markdown_dir,
        kb_path=args.kb_path,
        output_root=args.output_root,
        keep_ignored_blocks=args.keep_ignored_blocks,
    )


if __name__ == "__main__":
    main()
