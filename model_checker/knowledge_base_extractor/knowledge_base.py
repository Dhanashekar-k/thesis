"""
knowledge_base.py — Assemble and serialise the Stage 1 output.

The KnowledgeBase is the handoff artifact between Stage 1 (extraction) and
Stage 2 (requirement classification). It is serialised to JSON so later
stages can run independently without re-running the full 568-page OCR parse.

JSON schema
-----------
{
  "meta": {
    "total_pages": 568,
    "generated_at": "2024-01-15T10:30:00+00:00"
  },
  "sections": [
    {
      "clause_id":       "7.9.2.5",
      "title":           "Certificate installation",
      "pages":           [220, 221],
      "requirement_ids": ["V2G20-1576", "V2G20-1578"],
      "block_count":     14
    }
  ],
  "requirements": {
    "V2G20-1576": [
      { "text": "...", "page": 220, "section_id": "7.9.2.5" }
    ]
  },
  "tables": [
    {
      "table_id":   "T0012",
      "caption":    "AC_ChargeLoopReq — field definitions",
      "header":     ["Field", "Type", "M/O", "Description"],
      "rows":       [ { "cells": ["EVSEId", "string", "M", "..."] } ],
      "pages":      [310, 311],
      "section_id": "8.4.5"
    }
  ],
  "figures": [
    {
      "figure_id":  "Figure 215",
      "caption":    "AC message sequence diagram",
      "image_path": "imgs/img_in_image_box_100_200_900_1400.jpg",
      "page":       412,
      "bbox":       [100, 200, 900, 1400]
    }
  ],
  "stats": { ... }
}
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from models import Section, Requirement, Table, Figure


@dataclass
class KnowledgeBase:
    sections:     list[Section]                = field(default_factory=list)
    requirements: dict[str, list[Requirement]] = field(default_factory=dict)
    tables:       list[Table]                  = field(default_factory=list)
    figures:      list[Figure]                 = field(default_factory=list)
    total_pages:  int                          = 0

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add_requirement(self, req: Requirement) -> None:
        """
        Add a requirement occurrence. Multiple occurrences of the same ID
        are stored as a list so every textual context is available to Stage 2.
        Deduplication is by (page, text) so re-processing a block is safe.
        """
        if req.req_id not in self.requirements:
            self.requirements[req.req_id] = []
        existing = self.requirements[req.req_id]
        if not any(r.page == req.page and r.text == req.text for r in existing):
            existing.append(req)

    def lookup_requirement(self, req_id: str) -> list[Requirement]:
        """Return all occurrences of a V2G20-XXXX ID (empty list if absent)."""
        return self.requirements.get(req_id, [])

    def get_section(self, clause_id: str) -> Section | None:
        for s in self.sections:
            if s.clause_id == clause_id:
                return s
        return None

    def get_figure(self, figure_id: str) -> Figure | None:
        for f in self.figures:
            if f.figure_id.lower() == figure_id.lower():
                return f
        return None

    def get_requirements_for_section(self, clause_id: str) -> list[Requirement]:
        """Return all requirements whose section_id matches clause_id."""
        result = []
        for reqs in self.requirements.values():
            for r in reqs:
                if r.section_id == clause_id:
                    result.append(r)
        return result

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "meta": {
                "total_pages":  self.total_pages,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            "sections": [
                self._section_to_dict(s) for s in self.sections
            ],
            "requirements": {
                rid: [
                    {
                        "text":       r.text,
                        "page":       r.page,
                        "section_id": r.section_id,
                    }
                    for r in reqs
                ]
                for rid, reqs in sorted(self.requirements.items())
            },
            "tables":  [self._table_to_dict(t) for t in self.tables],
            "figures": [asdict(f) for f in self.figures],
            "stats": {
                "total_sections":     len(self.sections),
                "total_requirements": len(self.requirements),
                "total_tables":       len(self.tables),
                "total_figures":      len(self.figures),
                "multi_page_tables":  sum(
                    1 for t in self.tables if len(t.pages) > 1
                ),
            },
        }

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2, ensure_ascii=False)
        print(f"[kb] Saved knowledge base → {path}")

    @classmethod
    def load(cls, path: str) -> "KnowledgeBase":
        """
        Reconstruct a KnowledgeBase from a previously saved JSON file.
        content_blocks on Section objects are not re-populated (not serialised).
        Sufficient for all Stage 2+ consumption.
        """
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)

        kb = cls()
        kb.total_pages = d.get("meta", {}).get("total_pages", 0)

        for rid, occurrences in d.get("requirements", {}).items():
            for occ in occurrences:
                kb.add_requirement(Requirement(
                    req_id=rid,
                    text=occ["text"],
                    page=occ["page"],
                    section_id=occ.get("section_id"),
                ))

        for fd in d.get("figures", []):
            kb.figures.append(Figure(
                figure_id=fd["figure_id"],
                caption=fd["caption"],
                image_path=fd["image_path"],
                page=fd["page"],
                bbox=tuple(fd["bbox"]),
            ))

        for td in d.get("tables", []):
            from models import TableRow
            kb.tables.append(Table(
                table_id=td["table_id"],
                caption=td.get("caption"),
                header=td["header"],
                rows=[TableRow(cells=r["cells"]) for r in td.get("rows", [])],
                pages=td.get("pages", []),
                section_id=td.get("section_id"),
            ))

        for sd in d.get("sections", []):
            kb.sections.append(Section(
                clause_id=sd["clause_id"],
                title=sd["title"],
                pages=sd["pages"],
            ))

        return kb

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _section_to_dict(s: Section) -> dict:
        return {
            "clause_id":       s.clause_id,
            "title":           s.title,
            "pages":           s.pages,
            "requirement_ids": [r.req_id for r in s.requirements],
            "block_count":     len(s.content_blocks),
        }

    @staticmethod
    def _table_to_dict(t: Table) -> dict:
        return {
            "table_id":   t.table_id,
            "caption":    t.caption,
            "header":     t.header,
            "rows":       [{"cells": r.cells} for r in t.rows],
            "pages":      t.pages,
            "section_id": t.section_id,
        }