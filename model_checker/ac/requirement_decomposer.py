"""
requirement_decomposer.py — Stage 2: Extract and decompose V2G20 requirements into atoms.

Two extraction modes:
  1. Rule-based (regex) — always available, fast, deterministic
  2. LLM-assisted — richer decomposition when LLM is available

The rule-based path handles the common ISO 15118-20 patterns:
  - "After receiving X with ResponseCode = OK and EVSEProcessing = Finished, ..."
  - "the EVCC shall send Y within V2G_EVCC_Sequence_Performance_Timeout"
  - "the next allowed request shall be Z"
  - "shall respond with ... within V2G_SECC_Msg_Performance_Time"

The LLM path sends the full requirement text and gets structured atom JSON.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from models import (
    Atom, AtomKind, AtomScope, GuardStatus, Provenance,
    RequirementRecord, Role,
)
from config import PipelineConfig
from llm_client import InferenceClient, MockInferenceClient
from normalization import normalize_text, normalize_req_id_bare


def _dedup_atoms_across_requirements(records: dict[str, RequirementRecord]) -> None:
    """Deduplicate identical atoms across requirements.

    When the same expr+kind appears in multiple requirements, keep the one
    with the highest confidence and annotate with all source reqs.
    """
    seen: dict[str, tuple[str, float]] = {}  # (kind:expr) → (req_id, confidence)
    for req_id, rec in records.items():
        deduped = []
        for atom in rec.atoms:
            key = f"{atom.kind.value}:{atom.expr}"
            prev = seen.get(key)
            if prev is None:
                seen[key] = (req_id, atom.confidence)
                deduped.append(atom)
            elif prev[0] == req_id:
                # Same requirement — skip intra-requirement dup
                if atom.expr not in {a.expr for a in deduped}:
                    deduped.append(atom)
            else:
                # Cross-requirement dup — keep higher confidence, annotate
                if atom.confidence > prev[1]:
                    seen[key] = (req_id, atom.confidence)
                    deduped.append(atom)
                # Either way, keep the original in its requirement
        rec.atoms = deduped

# ═══════════════════════════════════════════════════════════════════════════
# Regex patterns for ISO 15118-20 requirement text
# ═══════════════════════════════════════════════════════════════════════════

# ResponseCode = <value>
_RESPONSE_CODE_RE = re.compile(
    r'["\u201c]?ResponseCode\s*[=:]\s*'
    r'(OK_SuccessfulNegotiation(?:WithMinorDeviation)?|OK|FAILED(?:_\w+)?|WARNING(?:_\w+)?)'
    r'["\u201d]?',
    re.IGNORECASE,
)

# EVSEProcessing set to "Ongoing" | "Finished"
_EVSE_PROCESSING_RE = re.compile(
    r'EVSEProcessing\s+(?:set\s+to|=|equal\s+to)\s*["\u201c]?(Ongoing|Finished)["\u201d]?',
    re.IGNORECASE,
)

# EVProcessing set to "Ongoing" | "Finished"
_EV_PROCESSING_RE = re.compile(
    r'EVProcessing\s+(?:set\s+to|=|equal\s+to)\s*["\u201c]?(Ongoing|Finished)["\u201d]?',
    re.IGNORECASE,
)

# ChargeProgress = Start | Stop | Standby | Renegotiate | ScheduleRenegotiate
_CHARGE_PROGRESS_RE = re.compile(
    r'ChargeProgress\s*[=:]+\s*["\u201c]?(Start|Stop|Standby|Renegotiate|ScheduleRenegotiate)["\u201d]?',
    re.IGNORECASE,
)

# ServiceName = AC | AC_BPT | ...
_SERVICE_NAME_RE = re.compile(
    r'ServiceName\s*=\s*(AC(?:_BPT|_ACDP|_ACD_BPT)?|DC(?:_BPT)?|WPT|ACDP)',
    re.IGNORECASE,
)

# "shall send a <MessageName>" — extract the action message
_SHALL_SEND_RE = re.compile(
    r'shall\s+send\s+(?:a|an)\s+(\w+(?:Req|Res))\b',
    re.IGNORECASE,
)

# "shall respond with" — extract response message
_SHALL_RESPOND_RE = re.compile(
    r'shall\s+respond\s+with\s+(?:a|an)?\s*(\w+(?:Req|Res))\b',
    re.IGNORECASE,
)

# Timer references: "within V2G_EVCC_Sequence_Performance_Timeout"
_TIMER_RE = re.compile(
    r'within\s+(V2G_(?:EVCC|SECC)_\w+(?:_Time(?:out)?)?)',
    re.IGNORECASE,
)

# "the next allowed request shall be X"
_NEXT_ALLOWED_RE = re.compile(
    r'next\s+allowed\s+request\s+shall\s+be\s+(\w+(?:Req)?)',
    re.IGNORECASE,
)

# "V2G_SECC_Sequence_Timeout is set according to Table ..."
_TIMEOUT_SET_RE = re.compile(
    r'(V2G_\w+Timeout)\s+is\s+set\s+(?:to|according)',
    re.IGNORECASE,
)

# ChargingSession = Pause | Terminate | ServiceRenegotiation
_CHARGING_SESSION_RE = re.compile(
    r'ChargingSession\s+(?:set\s+to|=)\s*["\u201c]?(Pause|Terminate|ServiceRenegotiation)["\u201d]?',
    re.IGNORECASE,
)

# CertificateInstallationService
_CERT_INSTALL_RE = re.compile(
    r'CertificateInstallationService\s+(?:set\s+to|=)\s*["\u201c]?(true|false|not\s+available)["\u201d]?',
    re.IGNORECASE,
)

# ServiceRenegotiationSupported
_SERVICE_RENEGO_RE = re.compile(
    r'ServiceRenegotiationSupported\s+(?:set\s+to|=)\s*["\u201c]?(true|false)["\u201d]?',
    re.IGNORECASE,
)

# EVSENotification
_EVSE_NOTIFICATION_RE = re.compile(
    r'EVSENotification\s+(?:in\s+EVSEStatus\s+)?(?:is\s+equal\s+to|=)\s*'
    r'["\u201c]?(ServiceRenegotiation|Terminate|Pause)["\u201d]?',
    re.IGNORECASE,
)

# "After receiving the <Message>" — identifies the trigger
_AFTER_RECEIVING_RE = re.compile(
    r'[Aa]fter\s+receiving\s+(?:the\s+)?(\w+(?:Req|Res))\b',
)

# Actor detection
_EVCC_ACTOR_RE = re.compile(r'\bEVCC\s+shall\b', re.IGNORECASE)
_SECC_ACTOR_RE = re.compile(r'\bSECC\s+shall\b', re.IGNORECASE)

# Table reference: "according to Table 215"
_TABLE_REF_RE = re.compile(r'(?:according\s+to|see)\s+Table\s+(\d+)', re.IGNORECASE)

# "intends to install or update a contract certificate"
_CERT_INTENT_RE = re.compile(
    r'intends?\s+to\s+(?:install|update)\s+.*?contract\s+certificate',
    re.IGNORECASE,
)

# "wants to stop/continue/enter standby"
_WANTS_STOP_RE = re.compile(r'wants?\s+to\s+stop\s+(?:the\s+)?energy\s+transfer', re.IGNORECASE)
_WANTS_CONTINUE_RE = re.compile(r'wants?\s+to\s+continue\s+(?:the\s+)?energy\s+transfer', re.IGNORECASE)
_WANTS_STANDBY_RE = re.compile(r'wants?\s+to\s+enter\s+(?:a\s+)?standby', re.IGNORECASE)
_WANTS_PAUSE_RE = re.compile(r'wants?\s+to\s+start\s+with\s+(?:a\s+)?pause', re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════════
# Rule-based decomposition
# ═══════════════════════════════════════════════════════════════════════════

def decompose_requirement_rulebased(
    req_id: str,
    text: str,
    clause_id: Optional[str] = None,
    page: Optional[int] = None,
) -> RequirementRecord:
    """
    Decompose a single requirement into atoms using regex rules.

    Returns a RequirementRecord with all extracted atoms.
    """
    provenance = Provenance(
        clause_id=clause_id,
        page_span=[page] if page else [],
        extraction_method="regex",
    )
    record = RequirementRecord(
        req_id=req_id,
        text=text,
        source=provenance,
    )

    # Detect actor
    actor = Role.BOTH
    if _EVCC_ACTOR_RE.search(text):
        actor = Role.EVCC
    elif _SECC_ACTOR_RE.search(text):
        actor = Role.SECC

    # Detect trigger message
    trigger_msg = ""
    m = _AFTER_RECEIVING_RE.search(text)
    if m:
        trigger_msg = m.group(1)

    # ── Guard atoms ────────────────────────────────────────────────────
    _extract_guard_atoms(record, text, req_id, actor, trigger_msg)

    # ── Action atoms ───────────────────────────────────────────────────
    _extract_action_atoms(record, text, req_id, actor)

    # ── Timing atoms ───────────────────────────────────────────────────
    _extract_timing_atoms(record, text, req_id, actor)

    # ── Sequence constraint atoms ──────────────────────────────────────
    _extract_sequence_atoms(record, text, req_id, actor)

    # Set overall confidence based on how many atoms were extracted
    if not record.atoms:
        record.confidence = 0.1  # nothing extracted
    elif any(a.kind == AtomKind.GUARD and a.guard_status == GuardStatus.KNOWN for a in record.atoms):
        record.confidence = 0.7
    else:
        record.confidence = 0.4

    return record


def _extract_guard_atoms(
    record: RequirementRecord,
    text: str,
    req_id: str,
    actor: Role,
    trigger_msg: str,
) -> None:
    """Extract guard (precondition) atoms from requirement text."""

    # ResponseCode guard
    m = _RESPONSE_CODE_RE.search(text)
    if m:
        rc_val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"ResponseCode = {rc_val}",
            source_req=req_id,
            confidence=0.9,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["ResponseCode"],
            notes=f"trigger: {trigger_msg}" if trigger_msg else "",
        ))

    # EVSEProcessing guard
    m = _EVSE_PROCESSING_RE.search(text)
    if m:
        val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"EVSEProcessing = {val}",
            source_req=req_id,
            confidence=0.9,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["EVSEProcessing"],
        ))

    # EVProcessing guard
    m = _EV_PROCESSING_RE.search(text)
    if m:
        val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"EVProcessing = {val}",
            source_req=req_id,
            confidence=0.9,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["EVProcessing"],
        ))

    # ChargeProgress guard
    m = _CHARGE_PROGRESS_RE.search(text)
    if m:
        val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"ChargeProgress = {val}",
            source_req=req_id,
            confidence=0.9,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["ChargeProgress"],
        ))

    # ServiceName guard
    m = _SERVICE_NAME_RE.search(text)
    if m:
        val = m.group(1).upper()
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"ServiceName = {val}",
            source_req=req_id,
            confidence=0.85,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["ServiceName"],
        ))

    # CertificateInstallationService guard
    m = _CERT_INSTALL_RE.search(text)
    if m:
        val = m.group(1).lower().replace(" ", "_")
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"CertificateInstallationService = {val}",
            source_req=req_id,
            confidence=0.8,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["CertificateInstallationService"],
        ))

    # ChargingSession guard
    m = _CHARGING_SESSION_RE.search(text)
    if m:
        val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"ChargingSession = {val}",
            source_req=req_id,
            confidence=0.9,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["ChargingSession"],
        ))

    # ServiceRenegotiationSupported guard
    m = _SERVICE_RENEGO_RE.search(text)
    if m:
        val = m.group(1).lower()
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.SESSION,
            expr=f"ServiceRenegotiationSupported = {val}",
            source_req=req_id,
            confidence=0.85,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["ServiceRenegotiationSupported"],
        ))

    # EVSENotification guard
    m = _EVSE_NOTIFICATION_RE.search(text)
    if m:
        val = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"EVSENotification = {val}",
            source_req=req_id,
            confidence=0.8,
            guard_status=GuardStatus.KNOWN,
            iso_variables=["EVSENotification"],
        ))

    # Intent guards (boolean)
    for pattern, iso_var, desc in [
        (_CERT_INTENT_RE, "CertificateInstallIntent", "EVCC intends cert install"),
        (_WANTS_STOP_RE, "EVWantsStop", "EV wants to stop energy transfer"),
        (_WANTS_CONTINUE_RE, "EVWantsContinue", "EV wants to continue energy transfer"),
        (_WANTS_STANDBY_RE, "EVWantsStandby", "EV wants to enter standby"),
        (_WANTS_PAUSE_RE, "EVWantsPause", "EV wants to start with pause"),
    ]:
        if pattern.search(text):
            record.atoms.append(Atom(
                kind=AtomKind.GUARD,
                actor=actor,
                scope=AtomScope.TRANSITION,
                expr=f"{iso_var} = TRUE",
                source_req=req_id,
                confidence=0.7,
                guard_status=GuardStatus.KNOWN,
                iso_variables=[iso_var],
                notes=desc,
            ))


def _extract_action_atoms(
    record: RequirementRecord,
    text: str,
    req_id: str,
    actor: Role,
) -> None:
    """Extract action atoms (shall send / shall respond)."""

    m = _SHALL_SEND_RE.search(text)
    if m:
        msg = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.ACTION,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"send({msg})",
            source_req=req_id,
            confidence=0.85,
            iso_variables=[msg],
            applies_to_messages=[msg],
        ))

    m = _SHALL_RESPOND_RE.search(text)
    if m:
        msg = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.ACTION,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"respond({msg})",
            source_req=req_id,
            confidence=0.85,
            iso_variables=[msg],
            applies_to_messages=[msg],
        ))


def _extract_timing_atoms(
    record: RequirementRecord,
    text: str,
    req_id: str,
    actor: Role,
) -> None:
    """Extract timing constraint atoms."""

    m = _TIMER_RE.search(text)
    if m:
        timer_name = m.group(1)
        # Check for table reference
        table_ref = ""
        mt = _TABLE_REF_RE.search(text)
        if mt:
            table_ref = f"Table {mt.group(1)}"

        record.atoms.append(Atom(
            kind=AtomKind.TIMING,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"timer({timer_name})",
            source_req=req_id,
            confidence=0.8,
            iso_variables=[timer_name],
            notes=f"reference: {table_ref}" if table_ref else "",
        ))

    m = _TIMEOUT_SET_RE.search(text)
    if m:
        timer_name = m.group(1)
        record.atoms.append(Atom(
            kind=AtomKind.TIMING,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=f"set_timer({timer_name})",
            source_req=req_id,
            confidence=0.75,
            iso_variables=[timer_name],
        ))


def _extract_sequence_atoms(
    record: RequirementRecord,
    text: str,
    req_id: str,
    actor: Role,
) -> None:
    """Extract sequence constraint atoms."""

    m = _NEXT_ALLOWED_RE.search(text)
    if m:
        next_msg = m.group(1)
        if not next_msg.endswith("Req"):
            next_msg += "Req"
        record.atoms.append(Atom(
            kind=AtomKind.SEQUENCE_CONSTRAINT,
            actor=actor,
            scope=AtomScope.STATE,
            expr=f"next_allowed = {next_msg}",
            source_req=req_id,
            confidence=0.85,
            iso_variables=[next_msg],
            applies_to_messages=[next_msg],
        ))


# ═══════════════════════════════════════════════════════════════════════════
# LLM-assisted decomposition
# ═══════════════════════════════════════════════════════════════════════════

_LLM_SYSTEM_PROMPT = """\
You are an expert in ISO 15118-20 EV charging protocol formal verification.

Given a V2G20-XXXX normative requirement, decompose it into a list of formal atoms.

Each atom is one of:
- guard: a precondition (field = value) that must hold
- action: something the actor shall do (send message, set field)
- timing: a timer/deadline constraint (within V2G_XXX_Timeout)
- field_constraint: a message field rule (type, mandatory/optional, domain)
- sequence_constraint: an ordering rule (next allowed request, etc.)
- invariant: a condition that must always hold
- assumption: an environment assumption

Output JSON:
{
  "atoms": [
    {
      "kind": "guard|action|timing|field_constraint|sequence_constraint|invariant|assumption",
      "actor": "EVCC|SECC|BOTH",
      "scope": "transition|state|message|session|global",
      "expr": "formal expression using ISO variable names",
      "iso_variables": ["ResponseCode", "EVSEProcessing"],
      "applies_to_messages": ["AC_ChargeLoopReq"],
      "confidence": 0.9,
      "notes": ""
    }
  ]
}

Use ISO 15118-20 variable names exactly as they appear in the spec.
"""


def decompose_requirement_llm(
    req_id: str,
    text: str,
    clause_id: Optional[str],
    page: Optional[int],
    llm_client: InferenceClient,
) -> RequirementRecord:
    """Decompose a requirement using LLM, with regex fallback."""
    provenance = Provenance(
        clause_id=clause_id,
        page_span=[page] if page else [],
        extraction_method="llm",
    )

    prompt = f"Decompose this ISO 15118-20 requirement into formal atoms:\n\nRequirement ID: {req_id}\nText: {text}\nSection: {clause_id or 'unknown'}"

    try:
        result = llm_client.complete_json(prompt, system=_LLM_SYSTEM_PROMPT)
        atoms = _parse_llm_atoms(result, req_id)
        if atoms:
            record = RequirementRecord(
                req_id=req_id, text=text, source=provenance, atoms=atoms,
                confidence=sum(a.confidence for a in atoms) / len(atoms),
            )
            return record
    except Exception as e:
        print(f"[decomposer] LLM failed for {req_id}: {e}, falling back to regex")

    # Fallback to regex
    record = decompose_requirement_rulebased(req_id, text, clause_id, page)
    record.source.extraction_method = "regex_fallback"
    return record


def _parse_llm_atoms(result: dict, req_id: str) -> list[Atom]:
    """Parse atom list from LLM JSON response."""
    atoms = []
    for ad in result.get("atoms", []):
        try:
            kind = AtomKind(ad.get("kind", "guard"))
            actor = Role(ad.get("actor", "BOTH"))
            scope = AtomScope(ad.get("scope", "transition"))
        except ValueError:
            continue

        atoms.append(Atom(
            kind=kind,
            actor=actor,
            scope=scope,
            expr=ad.get("expr", ""),
            source_req=req_id,
            confidence=float(ad.get("confidence", 0.6)),
            guard_status=GuardStatus.KNOWN if float(ad.get("confidence", 0)) >= 0.7 else GuardStatus.PARTIAL,
            iso_variables=ad.get("iso_variables", []),
            applies_to_messages=ad.get("applies_to_messages", []),
            notes=ad.get("notes", ""),
        ))
    return atoms


# ═══════════════════════════════════════════════════════════════════════════
# Batch decomposition
# ═══════════════════════════════════════════════════════════════════════════

def decompose_all_requirements(
    kb_data: dict,
    config: PipelineConfig,
    llm_client: InferenceClient | MockInferenceClient | None = None,
    target_req_ids: set[str] | None = None,
) -> dict[str, RequirementRecord]:
    """
    Decompose all (or targeted) requirements from the knowledge base.

    Parameters
    ----------
    kb_data : loaded knowledge_base.json
    config  : pipeline config
    llm_client : LLM client (None = use regex only)
    target_req_ids : if set, only decompose these req IDs

    Returns
    -------
    dict mapping req_id → RequirementRecord
    """
    requirements = kb_data.get("requirements", {})
    records: dict[str, RequirementRecord] = {}

    use_llm = config.use_llm and llm_client and not isinstance(llm_client, MockInferenceClient)

    for req_id, occurrences in requirements.items():
        # Normalize the requirement ID itself
        norm_req_id = normalize_req_id_bare(req_id, context="decomposer_batch")
        if target_req_ids and norm_req_id not in target_req_ids:
            continue

        # Use first occurrence (most complete text typically)
        occ = occurrences[0]
        text = normalize_text(occ["text"], context=f"req_{norm_req_id}")
        clause_id = occ.get("section_id")
        page = occ.get("page")

        if use_llm:
            # LLM-first: try LLM, fall back to regex
            record = decompose_requirement_llm(
                norm_req_id, text, clause_id, page, llm_client
            )
        else:
            record = decompose_requirement_rulebased(
                norm_req_id, text, clause_id, page
            )

        # Ensure provenance on every atom
        for atom in record.atoms:
            if not atom.provenance:
                atom.provenance = Provenance(
                    clause_id=clause_id,
                    page_span=[page] if page else [],
                    extraction_method=record.source.extraction_method,
                )

        records[norm_req_id] = record

    # Atom dedup: merge duplicate atoms across requirements
    _dedup_atoms_across_requirements(records)

    total_atoms = sum(len(r.atoms) for r in records.values())
    print(f"[decomposer] Decomposed {len(records)} requirements → {total_atoms} atoms")
    return records


# ═══════════════════════════════════════════════════════════════════════════
# Cache rebuild helper (used by run.py when loading from cache)
# ═══════════════════════════════════════════════════════════════════════════

def _rebuild_requirements(data: dict) -> dict[str, RequirementRecord]:
    """Rebuild RequirementRecord dict from cached JSON."""
    records: dict[str, RequirementRecord] = {}
    for req_id, d in data.items():
        atoms = []
        for ad in d.get("atoms", []):
            try:
                kind = AtomKind(ad.get("kind", "guard"))
                actor = Role(ad.get("actor", "BOTH"))
                scope = AtomScope(ad.get("scope", "transition"))
            except ValueError:
                continue
            atoms.append(Atom(
                kind=kind,
                actor=actor,
                scope=scope,
                expr=ad.get("expr", ""),
                applies_to_transitions=ad.get("applies_to_transitions", []),
                applies_to_states=ad.get("applies_to_states", []),
                applies_to_messages=ad.get("applies_to_messages", []),
                source_req=ad.get("source_req", req_id),
                confidence=float(ad.get("confidence", 0.0)),
                guard_status=GuardStatus(ad.get("guard_status", "unknown")),
                iso_variables=ad.get("iso_variables", []),
                notes=ad.get("notes", ""),
            ))

        source_data = d.get("source", {})
        provenance = Provenance(
            clause_id=source_data.get("clause", ""),
            page_span=source_data.get("page_span", []),
            table_id=source_data.get("table_id", ""),
            figure_id=source_data.get("figure_id", ""),
            extraction_method="cached",
        )

        records[req_id] = RequirementRecord(
            req_id=req_id,
            text=d.get("text", ""),
            source=provenance,
            atoms=atoms,
            confidence=float(d.get("confidence", 0.0)),
            notes=d.get("notes", ""),
        )

    print(f"[decomposer] Rebuilt {len(records)} requirements from cache")
    return records
