"""
table_analyzer.py — Extract message schemas, timers, and response codes from OCR tables.

Key fixes over v1:
  1. Uses figure_title blocks (not just table_title/paragraph_title) to identify table names
     — OCR labels table captions as figure_title, which is why v1 found 0 message schemas
  2. Fuzzy classification using combined title + clause context + header row
  3. Per-message response code extraction from prose requirements
  4. Accepts ACRelevanceMap to scope table scanning to AC-relevant pages only
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

from models import (
    Cardinality, FieldDef, MessageSchema, TimerSpec,
    Provenance, Role,
)
from config import PipelineConfig
from normalization import normalize_text


# ═══════════════════════════════════════════════════════════════════════════
# HTML table parser
# ═══════════════════════════════════════════════════════════════════════════

class _TableHTMLParser(HTMLParser):
    """Minimal parser that extracts rows from an HTML table, handling rowspan."""

    def __init__(self):
        super().__init__()
        self.rows: list[list[str]] = []
        self._current_row: list[str] = []
        self._current_cell: list[str] = []
        self._in_cell = False
        # rowspan tracking: list of (remaining_rows, col_index, cell_text)
        self._rowspan_cells: list[list[int | str]] = []
        self._current_rowspan = 1
        self._col_idx = 0

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
            self._col_idx = 0
        elif tag in ("td", "th"):
            self._in_cell = True
            self._current_cell = []
            attr_dict = dict(attrs)
            self._current_rowspan = int(attr_dict.get("rowspan", "1"))

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self._in_cell = False
            cell_text = " ".join(self._current_cell).strip()
            self._current_row.append(cell_text)
            if self._current_rowspan > 1:
                self._rowspan_cells.append(
                    [self._current_rowspan - 1, self._col_idx, cell_text]
                )
            self._col_idx += 1
        elif tag == "tr":
            if self._current_row:
                self.rows.append(self._current_row)
            # Decrement rowspan counters; inject cells into next row
            still_active = []
            for entry in self._rowspan_cells:
                entry[0] -= 1
                if entry[0] > 0:
                    still_active.append(entry)
            self._rowspan_cells = still_active

    def handle_data(self, data):
        if self._in_cell:
            self._current_cell.append(data.strip())


def parse_html_table(html: str) -> list[list[str]]:
    """Parse an HTML table string into a list of rows (list of cell strings).

    After raw parsing, fills in cells omitted by rowspan so every row
    has the same number of columns.
    """
    parser = _TableHTMLParser()
    parser.feed(html)
    rows = parser.rows

    if not rows:
        return rows

    # Post-process: handle rowspan by filling omitted cells.
    # Re-parse to get rowspan info directly from HTML.
    return _fill_rowspan(html, rows)


def _fill_rowspan(html: str, raw_rows: list[list[str]]) -> list[list[str]]:
    """
    Fill cells omitted by HTML rowspan so every row has uniform columns.

    Strategy: parse the HTML again to extract rowspan metadata, then
    insert carried-over cells into the correct column positions.
    """
    # Quick regex scan for rowspan info in the HTML
    # Build a grid by tracking which cells span multiple rows
    from html.parser import HTMLParser as _HP

    class _SpanParser(_HP):
        def __init__(self):
            super().__init__()
            self.grid: list[list[tuple[str, int]]] = []  # (text, rowspan)
            self._row: list[tuple[str, int]] = []
            self._cell_parts: list[str] = []
            self._in_cell = False
            self._rspan = 1

        def handle_starttag(self, tag, attrs):
            if tag == "tr":
                self._row = []
            elif tag in ("td", "th"):
                self._in_cell = True
                self._cell_parts = []
                self._rspan = int(dict(attrs).get("rowspan", "1"))

        def handle_endtag(self, tag):
            if tag in ("td", "th"):
                self._in_cell = False
                text = " ".join(self._cell_parts).strip()
                self._row.append((text, self._rspan))
            elif tag == "tr" and self._row:
                self.grid.append(self._row)

        def handle_data(self, data):
            if self._in_cell:
                self._cell_parts.append(data.strip())

    sp = _SpanParser()
    sp.feed(html)
    grid = sp.grid

    if not grid:
        return raw_rows

    # Determine max columns
    max_cols = max(len(r) for r in grid) if grid else 0
    if max_cols == 0:
        return raw_rows

    # Build uniform grid with rowspan propagation
    # pending[col] = (remaining_rows, text)
    pending: dict[int, list] = {}
    result: list[list[str]] = []

    for row_cells in grid:
        out_row: list[str] = []
        cell_idx = 0
        col = 0
        while col < max_cols:
            # Check if a rowspan cell occupies this column
            if col in pending and pending[col][0] > 0:
                out_row.append(pending[col][1])
                pending[col][0] -= 1
                if pending[col][0] == 0:
                    del pending[col]
                col += 1
                continue
            # Take from current row's cells
            if cell_idx < len(row_cells):
                text, rspan = row_cells[cell_idx]
                out_row.append(text)
                if rspan > 1:
                    pending[col] = [rspan - 1, text]
                cell_idx += 1
            else:
                out_row.append("")
            col += 1
        result.append(out_row)

    return result


# ═══════════════════════════════════════════════════════════════════════════
# OCR block scanner — FIXED: figure_title is how OCR labels table captions
# ═══════════════════════════════════════════════════════════════════════════

def _find_table_blocks(
    ocr_json_dir: Path,
    pages: set[int] | None = None,
) -> list[dict]:
    """
    Scan OCR JSON files for table blocks.

    Returns list of {page, title, html, clause_context, bbox}.

    CRITICAL FIX: Table captions in the OCR appear as figure_title blocks
    immediately preceding the table block, NOT as table_title blocks.
    """
    results = []
    files = sorted(ocr_json_dir.glob("iso20_spec_*_res.json"),
                   key=lambda p: _page_num(p.name))

    for fpath in files:
        page = _page_num(fpath.name)
        if pages is not None and page not in pages:
            continue

        try:
            data = json.loads(fpath.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        blocks = data.get("parsing_res_list", [])
        pending_title = ""
        clause_context = ""

        for block in blocks:
            btype = block.get("block_label", "")
            text = block.get("block_content", "")

            if btype == "paragraph_title":
                clause_context = text
            elif btype == "figure_title":
                # Table titles appear as figure_title in OCR output
                pending_title = text
            elif btype == "table" and text.strip():
                results.append({
                    "page": page,
                    "title": pending_title,
                    "html": text,
                    "clause_context": clause_context,
                    "bbox": block.get("bbox"),
                })
                pending_title = ""  # consume

    return results


def _page_num(filename: str) -> int:
    """Extract page number from 'iso20_spec_42_res.json'."""
    m = re.search(r"iso20_spec_(\d+)_res", filename)
    return int(m.group(1)) if m else -1


# ═══════════════════════════════════════════════════════════════════════════
# Table classification — uses title + clause context + header row
# ═══════════════════════════════════════════════════════════════════════════

# All AC-relevant message names for matching
_MSG_TABLE_RE = re.compile(
    r'((?:AC_)?(?:ChargeParameterDiscovery|ChargeLoop)|'
    r'PowerDelivery|SessionSetup|AuthorizationSetup|Authorization|'
    r'ServiceDiscovery|ServiceDetail|ServiceSelection|ScheduleExchange|'
    r'SessionStop|CertificateInstallation|SupportedAppProtocol|'
    r'MeteringConfirmation)'
    r'(?:Req|Res)?',
    re.IGNORECASE,
)

_TIMING_TABLE_RE = re.compile(
    r'Table\s+215|Table\s+216|timing|timeout|performance\s+time|'
    r'sequence.*time|V2G_',
    re.IGNORECASE,
)
_RESPONSE_CODE_RE = re.compile(
    r'response\s*code|responseCodeType|valid.*response|error.*handling',
    re.IGNORECASE,
)
_SEMANTICS_RE = re.compile(
    r'[Ss]emantics\s+and\s+type|[Tt]ype\s+definition|[Ee]lement\s+[Nn]ame',
)


def classify_table(
    title: str,
    clause_context: str,
    rows: list[list[str]],
) -> tuple[str, str]:
    """
    Classify a table and identify what message it relates to.

    Returns (table_type, message_name).
    table_type: "message_fields", "timing", "response_codes", "enumeration", "other"
    message_name: identified message name or "" if not applicable
    """
    combined = f"{title} {clause_context}"

    # 1. Check for timing table first (Table 215/216 or timing keywords)
    if _TIMING_TABLE_RE.search(combined):
        # Confirm with header/content
        for row in rows[:5]:
            row_text = " ".join(row)
            if re.search(r'V2G_|timeout|timer|performance.*time', row_text, re.IGNORECASE):
                return "timing", ""
        # If title strongly says timing, trust it
        if re.search(r'Table\s+21[56]', title):
            return "timing", ""

    # 2. Check for response code table
    if _RESPONSE_CODE_RE.search(combined):
        return "response_codes", ""

    # 3. Check for message field definition table
    msg_match = _MSG_TABLE_RE.search(combined)
    msg_name = ""
    if msg_match:
        raw = msg_match.group(0)
        # Normalize: ensure proper Req/Res suffix
        if raw.endswith("Req") or raw.endswith("Res"):
            msg_name = raw
        elif "Req" in combined[msg_match.end():msg_match.end() + 10]:
            msg_name = raw + "Req"
        elif "Res" in combined[msg_match.end():msg_match.end() + 10]:
            msg_name = raw + "Res"
        else:
            msg_name = raw

    if _SEMANTICS_RE.search(combined) and msg_name:
        return "message_fields", msg_name

    # 4. Check header row for field-definition pattern
    if rows:
        header = " ".join(rows[0]).lower()
        if ("element" in header or "name" in header) and (
            "type" in header or "semantics" in header or "description" in header
        ):
            if msg_name:
                return "message_fields", msg_name
            # Try to get message from clause context
            cm = _MSG_TABLE_RE.search(clause_context)
            if cm:
                return "message_fields", cm.group(0)
            return "message_fields", ""

        # Timer table by header content
        if ("name" in header and "value" in header) or "timeout" in header:
            return "timing", ""

    # 5. Enumeration/value table
    if rows and len(rows) > 1:
        header = " ".join(rows[0]).lower()
        if "value" in header and "description" in header:
            return "enumeration", msg_name

    return "other", msg_name


# ═══════════════════════════════════════════════════════════════════════════
# Message field extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract_message_schema(
    title: str,
    msg_name: str,
    rows: list[list[str]],
    page: int,
) -> Optional[MessageSchema]:
    """
    Extract a MessageSchema from a message-field table.

    Expected table columns (may vary):
      | Element Name | Type | M/O/C | Semantics |
    """
    if not rows or not msg_name:
        return None

    direction = "request" if msg_name.endswith("Req") else "response"

    # Find header row
    header_idx = _find_header_row(rows)
    if header_idx < 0:
        return None

    header = [c.lower().strip() for c in rows[header_idx]]

    # Map column indices
    name_col = _find_col(header, ["element", "name", "field"])
    type_col = _find_col(header, ["type", "datatype", "data type"])
    card_col = _find_col(header, ["m/o", "m/o/c", "mandatory", "cardinality"])
    desc_col = _find_col(header, ["description", "semantics", "comment"])

    fields = []
    for row in rows[header_idx + 1:]:
        if len(row) <= max(name_col, 0):
            continue

        fname = row[name_col].strip() if name_col >= 0 and name_col < len(row) else ""
        if not fname or fname.lower() in ("", "-", "n/a"):
            continue
        # Skip "Header" field — common to all messages
        if fname == "Header":
            continue

        ftype = row[type_col].strip() if type_col >= 0 and type_col < len(row) else ""
        card_str = row[card_col].strip() if card_col >= 0 and card_col < len(row) else "M"
        desc = row[desc_col].strip() if desc_col >= 0 and desc_col < len(row) else ""

        cardinality = _parse_cardinality(card_str)

        # Extract value domain from type, name, or description
        domain = _extract_value_domain(fname, ftype, desc)

        fields.append(FieldDef(
            name=fname,
            field_type=ftype,
            cardinality=cardinality,
            semantics=desc,
            value_domain=domain,
            provenance=Provenance(
                page_span=[page],
                table_id=title,
                extraction_method="table_parse",
            ),
        ))

    if not fields:
        return None

    # Confidence based on column match quality
    col_found = sum(1 for c in [name_col, type_col, card_col, desc_col] if c >= 0)
    confidence = 0.4 + (col_found / 4) * 0.5  # 0.4-0.9 based on columns found

    schema = MessageSchema(
        message_name=msg_name,
        direction=direction,
        fields=fields,
        provenance=Provenance(
            page_span=[page],
            table_id=title,
            extraction_method="table_parse",
        ),
    )
    schema.confidence = confidence
    return schema


def _find_header_row(rows: list[list[str]]) -> int:
    """Find the header row (contains 'element', 'type', 'M/O', etc.)."""
    for i, row in enumerate(rows[:5]):
        combined = " ".join(c.lower() for c in row)
        if ("type" in combined or "element" in combined) and (
            "m/o" in combined or "mandatory" in combined or
            "description" in combined or "semantics" in combined
        ):
            return i
    return 0 if rows else -1


def _find_col(header: list[str], keywords: list[str]) -> int:
    for i, h in enumerate(header):
        for kw in keywords:
            if kw in h:
                return i
    return -1


def _parse_cardinality(s: str) -> Cardinality:
    s = s.strip().upper()
    if s.startswith("M"):
        return Cardinality.MANDATORY
    if s.startswith("O"):
        return Cardinality.OPTIONAL
    if s.startswith("C"):
        return Cardinality.CONDITIONAL
    return Cardinality.MANDATORY


def _extract_value_domain(name: str, field_type: str, desc: str) -> list[str]:
    """Extract known value domain from field name, type, or description."""
    # Normalize description text for req ID extraction
    desc = normalize_text(desc, context=f"table_field_{name}")

    # Well-known enumerations by field name / type
    if name == "ResponseCode" or "responseCodeType" in field_type:
        return ["OK", "FAILED", "FAILED_SequenceError", "WARNING"]
    if name in ("EVSEProcessing", "EVProcessing") or "processingType" in field_type.lower():
        return ["Ongoing", "Finished"]
    if name == "ChargeProgress" or "chargeProgressType" in field_type.lower():
        return ["Start", "Stop", "Standby", "Renegotiate", "ScheduleRenegotiate"]
    if name == "ChargingSession" or "chargingSessionType" in field_type.lower():
        return ["Pause", "Terminate", "ServiceRenegotiation"]
    if "eVSENotificationType" in field_type.lower() or name == "EVSENotification":
        return ["ServiceRenegotiation", "Terminate", "Pause"]

    # Generic enum extraction from description
    domain = []
    enum_match = re.findall(
        r'(OK(?:_\w+)?|FAILED(?:_\w+)?|WARNING(?:_\w+)?|Ongoing|Finished|'
        r'Start|Stop|Standby|Renegotiate|ScheduleRenegotiate|'
        r'Pause|Terminate|ServiceRenegotiation)',
        desc, re.IGNORECASE,
    )
    if enum_match:
        domain = list(dict.fromkeys(enum_match))
    return domain


# ═══════════════════════════════════════════════════════════════════════════
# Timing table extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract_timing_specs(title: str, rows: list[list[str]], page: int) -> list[TimerSpec]:
    """
    Extract timer specifications from a timing table.

    Expected columns:
      | Timer name | Value | Applicable to | Message |
    """
    timers = []

    header_idx = _find_header_row(rows)
    if header_idx < 0 and rows:
        header_idx = 0

    header = [c.lower().strip() for c in rows[header_idx]] if rows else []

    timer_col = _find_col(header, ["timer", "timeout", "name", "parameter"])
    value_col = _find_col(header, ["value", "time", "duration", "second"])
    msg_col = _find_col(header, ["message", "applicable", "apply", "request", "response"])

    # Track current timer name (for multi-row spans where name is in first row only)
    current_timer = ""

    for row in rows[header_idx + 1:]:
        cell0 = row[timer_col].strip() if timer_col >= 0 and timer_col < len(row) else ""

        # Check for V2G_ pattern in first column or anywhere in row
        timer_name = ""
        if cell0 and re.match(r'V2G_', cell0):
            timer_name = cell0
            current_timer = timer_name
        elif not cell0 and current_timer:
            timer_name = current_timer  # continuation row
        else:
            # Try to find V2G_ pattern anywhere in the row
            for cell in row:
                m = re.search(r'(V2G_\w+(?:_?Time(?:out)?)?)', cell)
                if m:
                    timer_name = m.group(1)
                    current_timer = timer_name
                    break

        if not timer_name:
            current_timer = ""  # reset on non-timer row
            continue

        value_str = row[value_col].strip() if value_col >= 0 and value_col < len(row) else ""
        msg_type = row[msg_col].strip() if msg_col >= 0 and msg_col < len(row) else ""

        value = _parse_timer_value(value_str)

        # Determine actor from timer name
        actor = Role.BOTH
        if "EVCC" in timer_name.upper():
            actor = Role.EVCC
        elif "SECC" in timer_name.upper():
            actor = Role.SECC

        timers.append(TimerSpec(
            name=timer_name,
            message_type=msg_type,
            value_seconds=value,
            applicable_to=actor,
            provenance=Provenance(
                page_span=[page],
                table_id=title,
                extraction_method="table_parse",
            ),
        ))

    return timers


def _parse_timer_value(s: str) -> float:
    """Parse a timer value string into seconds.

    Handles European decimal comma notation (0,5 = 0.5) used in ISO specs.
    """
    s = s.strip().lower()
    if not s:
        return 0.0
    # Replace European decimal comma with dot: "0,5" → "0.5", "0,25" → "0.25"
    s = re.sub(r'(\d),(\d)', r'\1.\2', s)
    # "2 s", "2s", "2000 ms", "2.0", "0.5"
    m = re.search(r'(\d+(?:\.\d+)?)\s*(s|ms|sec|second)?', s)
    if m:
        val = float(m.group(1))
        unit = m.group(2) or "s"
        if unit == "ms":
            val /= 1000.0
        return val
    return 0.0


# ═══════════════════════════════════════════════════════════════════════════
# Response code extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract_response_codes(title: str, rows: list[list[str]]) -> dict[str, list[str]]:
    """
    Extract valid response codes per message from response code tables.

    Returns dict[message_name, list[response_code_value]].
    """
    codes: dict[str, list[str]] = {}

    for row in rows:
        for cell in row:
            # Look for message name patterns
            msg_match = _MSG_TABLE_RE.search(cell)
            if msg_match:
                msg = msg_match.group(0)
                # Find response codes in same row
                for c2 in row:
                    rc_matches = re.findall(
                        r'(OK(?:_\w+)?|FAILED(?:_\w+)?|WARNING(?:_\w+)?)',
                        c2,
                    )
                    if rc_matches:
                        codes.setdefault(msg, []).extend(rc_matches)

    # Deduplicate
    return {k: list(dict.fromkeys(v)) for k, v in codes.items()}


# ═══════════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════════

def analyze_tables_from_chunks(
    section_chunks,
) -> tuple[list[MessageSchema], list[TimerSpec], dict[str, list[str]]]:
    """
    Analyze tables from pre-processed SectionChunks (new pipeline).

    Each SectionChunk has .tables: list[TableBlock] with .html and .title.
    This replaces the old analyze_tables() which read OCR JSON directly.

    Returns (message_schemas, timer_specs, response_codes).
    """
    schemas: list[MessageSchema] = []
    timers: list[TimerSpec] = []
    response_codes: dict[str, list[str]] = {}
    schema_names_seen: set[str] = set()
    total_tables = 0

    for chunk in section_chunks:
        for tb in chunk.tables:
            total_tables += 1
            rows = parse_html_table(tb.html)
            if not rows:
                continue

            ttype, msg_name = classify_table(
                tb.title, tb.clause_context, rows,
            )

            page = tb.page_span[0] if tb.page_span else 0

            if ttype == "message_fields":
                schema = extract_message_schema(tb.title, msg_name, rows, page)
                if schema and schema.message_name not in schema_names_seen:
                    schemas.append(schema)
                    schema_names_seen.add(schema.message_name)

            elif ttype == "timing":
                ts = extract_timing_specs(tb.title, rows, page)
                timers.extend(ts)

            elif ttype == "response_codes":
                codes = extract_response_codes(tb.title, rows)
                for msg, vals in codes.items():
                    response_codes.setdefault(msg, []).extend(vals)

    # Deduplicate response codes and timers
    response_codes = {k: list(dict.fromkeys(v)) for k, v in response_codes.items()}

    seen_timers: set[tuple[str, str]] = set()
    unique_timers = []
    for t in timers:
        key = (t.name, t.message_type)
        if key not in seen_timers:
            seen_timers.add(key)
            unique_timers.append(t)
    timers = unique_timers

    print(f"[table_analyzer] Analyzed {total_tables} tables from "
          f"{len(section_chunks)} sections")
    print(f"[table_analyzer] Extracted {len(schemas)} message schemas, "
          f"{len(timers)} timers, {len(response_codes)} response code sets")

    return schemas, timers, response_codes


def analyze_tables(
    config: PipelineConfig,
) -> tuple[list[MessageSchema], list[TimerSpec], dict[str, list[str]]]:
    """
    Legacy: analyze all tables from raw OCR (no pre-filtering).

    Returns (message_schemas, timer_specs, response_codes).
    """
    ocr_dir = config.resolve_path(config.ocr_base_dir) / "json"

    if not ocr_dir.exists():
        print(f"[table_analyzer] OCR directory not found: {ocr_dir}")
        return [], [], {}

    table_blocks = _find_table_blocks(ocr_dir)
    print(f"[table_analyzer] Found {len(table_blocks)} table blocks")

    schemas: list[MessageSchema] = []
    timers: list[TimerSpec] = []
    response_codes: dict[str, list[str]] = {}
    schema_names_seen: set[str] = set()

    for tb in table_blocks:
        rows = parse_html_table(tb["html"])
        if not rows:
            continue

        ttype, msg_name = classify_table(
            tb["title"], tb.get("clause_context", ""), rows,
        )

        if ttype == "message_fields":
            schema = extract_message_schema(tb["title"], msg_name, rows, tb["page"])
            if schema and schema.message_name not in schema_names_seen:
                schemas.append(schema)
                schema_names_seen.add(schema.message_name)

        elif ttype == "timing":
            ts = extract_timing_specs(tb["title"], rows, tb["page"])
            timers.extend(ts)

        elif ttype == "response_codes":
            codes = extract_response_codes(tb["title"], rows)
            for msg, vals in codes.items():
                response_codes.setdefault(msg, []).extend(vals)

    # Deduplicate response codes and timers
    response_codes = {k: list(dict.fromkeys(v)) for k, v in response_codes.items()}

    seen_timers: set[tuple[str, str]] = set()
    unique_timers = []
    for t in timers:
        key = (t.name, t.message_type)
        if key not in seen_timers:
            seen_timers.add(key)
            unique_timers.append(t)
    timers = unique_timers

    print(f"[table_analyzer] Extracted {len(schemas)} message schemas, "
          f"{len(timers)} timers, {len(response_codes)} response code sets")

    return schemas, timers, response_codes


# ═══════════════════════════════════════════════════════════════════════════
# Cache rebuild helpers (used by run.py when loading from cache)
# ═══════════════════════════════════════════════════════════════════════════

def _rebuild_schemas(data: list[dict]) -> list[MessageSchema]:
    """Rebuild MessageSchema list from cached JSON dicts."""
    schemas = []
    for d in data:
        fields = []
        for fd in d.get("fields", []):
            fields.append(FieldDef(
                name=fd["name"],
                field_type=fd.get("type", ""),
                cardinality=Cardinality(fd.get("cardinality", "mandatory")),
                semantics=fd.get("semantics", ""),
                value_domain=fd.get("value_domain", []),
                provenance=Provenance(
                    page_span=fd.get("page_span", []),
                    table_id=fd.get("table_id", ""),
                    extraction_method=fd.get("extraction_method", "cached"),
                ),
            ))
        schemas.append(MessageSchema(
            message_name=d["message_name"],
            direction=d.get("direction", ""),
            fields=fields,
            provenance=Provenance(
                page_span=d.get("page_span", []),
                table_id=d.get("table_id", ""),
                extraction_method="cached",
            ),
        ))
    return schemas


def _rebuild_timers(data: list[dict]) -> list[TimerSpec]:
    """Rebuild TimerSpec list from cached JSON dicts."""
    timers = []
    for d in data:
        actor = Role.BOTH
        actor_str = d.get("applicable_to", "BOTH")
        if actor_str == "EVCC":
            actor = Role.EVCC
        elif actor_str == "SECC":
            actor = Role.SECC
        timers.append(TimerSpec(
            name=d["name"],
            message_type=d.get("message_type", ""),
            value_seconds=d.get("value_seconds", 0.0),
            applicable_to=actor,
            provenance=Provenance(extraction_method="cached"),
        ))
    return timers
