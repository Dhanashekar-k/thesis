"""
ac_relevance.py — Post-extraction AC relevance classifier.

This module runs AFTER VLM extraction, not before.
It classifies every extracted element into:
  - AC:              directly used in AC flow
  - shared_relevant: from shared sections but used by AC
  - unrelated:       DC/WPT/ACDP-only → discard

The AC message sequence diagram (FSM) provides the backbone:
  - states → which messages are AC-relevant
  - transitions → which requirement IDs are AC-relevant
  - message names → which schemas/fields/guards matter

NOTHING is filtered before extraction. Everything is extracted first,
then classified here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Classification result
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RelevanceResult:
    """Classification of a single extracted element."""
    is_ac_relevant: bool
    relevance_type: str       # "AC" | "shared_relevant" | "unrelated"
    linked_messages: list[str] = field(default_factory=list)
    linked_states: list[str] = field(default_factory=list)
    reason: str = ""


# ═══════════════════════════════════════════════════════════════════════════
# AC backbone from FSM
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ACBackbone:
    """The AC protocol backbone derived from the FSM."""
    ac_states: list[str] = field(default_factory=list)
    ac_messages: set[str] = field(default_factory=set)
    fsm_req_ids: set[str] = field(default_factory=set)
    ac_message_base_names: set[str] = field(default_factory=set)  # without Req/Res suffix


def build_ac_backbone(fsm_data: dict) -> ACBackbone:
    """
    Build the AC backbone from the FSM JSON.

    Extracts:
    - All state labels → AC states
    - State labels + Req/Res suffixes → AC messages
    - All V2G20 refs from transitions → FSM requirement IDs (normalized)
    """
    from normalization import normalize_req_id_bare

    backbone = ACBackbone()

    state_label_map = {}
    for s in fsm_data.get("states", []):
        label = s["label"]
        state_label_map[s["id"]] = label
        backbone.ac_states.append(label)
        backbone.ac_message_base_names.add(label)
        backbone.ac_messages.add(f"{label}Req")
        backbone.ac_messages.add(f"{label}Res")

    # Collect all requirement refs from FSM — normalize each one
    for t in fsm_data.get("transitions", []):
        for ref in t.get("evcc_refs", []):
            backbone.fsm_req_ids.add(normalize_req_id_bare(ref, context="fsm_transition"))
        for ref in t.get("secc_refs", []):
            backbone.fsm_req_ids.add(normalize_req_id_bare(ref, context="fsm_transition"))

    for key in ("entry_point", "exit_point"):
        pt = fsm_data.get(key, {})
        for ref in pt.get("evcc_refs", []):
            backbone.fsm_req_ids.add(normalize_req_id_bare(ref, context=f"fsm_{key}"))
        for ref in pt.get("secc_refs", []):
            backbone.fsm_req_ids.add(normalize_req_id_bare(ref, context=f"fsm_{key}"))

    return backbone


# ═══════════════════════════════════════════════════════════════════════════
# DC/WPT/ACDP exclusion patterns
# ═══════════════════════════════════════════════════════════════════════════

_DC_ONLY_RE = re.compile(
    r'\b(DC_|BPT_DC|DC_ChargeParameter|DC_ChargeLoop|DC_WeldingDetection|'
    r'DC_CableCheck|DC_PreCharge)\w*',
    re.IGNORECASE,
)

_WPT_ONLY_RE = re.compile(
    r'\b(WPT_|WPT_ChargeParameter|WPT_ChargeLoop|WPT_FinePositioning|'
    r'WPT_AlignmentCheck|WPT_PairingCheck)\w*',
    re.IGNORECASE,
)

_ACDP_ONLY_RE = re.compile(
    r'\b(ACDP_|ACDP_SystemStatus|ACDP_Connect|ACDP_Disconnect|'
    r'ACDP_VehiclePositioning)\w*',
    re.IGNORECASE,
)

# Shared protocol elements that are relevant to ALL modes including AC
_SHARED_RELEVANT_PATTERNS = re.compile(
    r'(SessionSetup|Authorization|CertificateInstallation|'
    r'ServiceDiscovery|ServiceDetail|ServiceSelection|'
    r'ScheduleExchange|PowerDelivery|SessionStop|'
    r'SupportedAppProtocol|ResponseCode|EVSEProcessing|'
    r'ChargeProgress|ChargingSession|EVSENotification|'
    r'Header|V2G_|Timer|Timeout|Performance)',
    re.IGNORECASE,
)

# AC-relevant ISO variable names (used as additional signal)
_AC_VARIABLE_NAMES = {
    "ResponseCode", "EVSEProcessing", "EVProcessing",
    "ChargeProgress", "ChargingSession", "EVSENotification",
    "CertificateInstallationService", "ServiceRenegotiationSupported",
    "CertificateInstallIntent", "ServiceName",
    "EVWantsStop", "EVWantsContinue", "EVWantsStandby", "EVWantsPause",
}

# Timer name pattern — timers are globally relevant
_TIMER_NAME_RE = re.compile(r'V2G_(?:EVCC|SECC)_\w+', re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════════
# Element classifier
# ═══════════════════════════════════════════════════════════════════════════

def classify_element(
    element: dict,
    category: str,
    backbone: ACBackbone,
) -> RelevanceResult:
    """
    Classify a single extracted element for AC relevance.

    Parameters
    ----------
    element : dict from VLM extraction (guard, action, field_def, etc.)
    category : which extraction category this came from
    backbone : AC backbone from FSM

    Returns
    -------
    RelevanceResult with classification
    """
    # Gather all text from the element for pattern matching
    text = _element_text(element)

    # Check for DC/WPT/ACDP-only patterns → unrelated
    if _DC_ONLY_RE.search(text) and not _has_ac_ref(text):
        return RelevanceResult(
            is_ac_relevant=False,
            relevance_type="unrelated",
            reason="DC-only element",
        )
    if _WPT_ONLY_RE.search(text) and not _has_ac_ref(text):
        return RelevanceResult(
            is_ac_relevant=False,
            relevance_type="unrelated",
            reason="WPT-only element",
        )
    if _ACDP_ONLY_RE.search(text) and not _has_ac_ref(text):
        return RelevanceResult(
            is_ac_relevant=False,
            relevance_type="unrelated",
            reason="ACDP-only element",
        )

    # Check for direct AC references
    linked_msgs = _find_linked_messages(element, backbone)
    linked_states = _find_linked_states(element, backbone)

    if re.search(r'\bAC_\w+', text):
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="AC",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason="AC-specific element",
        )

    # Check if references FSM requirement IDs
    req_ref = element.get("source_req", "")
    if req_ref and req_ref in backbone.fsm_req_ids:
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="AC",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason=f"References FSM requirement {req_ref}",
        )

    # Check if references AC messages
    if linked_msgs:
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="AC" if any("AC_" in m for m in linked_msgs) else "shared_relevant",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason=f"References AC messages: {', '.join(linked_msgs[:3])}",
        )

    # Check if references AC-relevant ISO variable names
    for var_name in _AC_VARIABLE_NAMES:
        if var_name in text:
            return RelevanceResult(
                is_ac_relevant=True,
                relevance_type="shared_relevant",
                linked_messages=linked_msgs,
                linked_states=linked_states,
                reason=f"References AC-relevant variable: {var_name}",
            )

    # Check if references timer names (globally relevant)
    if _TIMER_NAME_RE.search(text):
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="shared_relevant",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason="References V2G timer",
        )

    # Check for shared protocol elements
    if _SHARED_RELEVANT_PATTERNS.search(text):
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="shared_relevant",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason="Shared protocol element used by AC",
        )

    # Default: keep as shared_relevant if it mentions any protocol concept
    if re.search(r'\b(EVCC|SECC|V2G|message|response|request|session)\b', text, re.IGNORECASE):
        return RelevanceResult(
            is_ac_relevant=True,
            relevance_type="shared_relevant",
            linked_messages=linked_msgs,
            linked_states=linked_states,
            reason="General protocol element",
        )

    return RelevanceResult(
        is_ac_relevant=False,
        relevance_type="unrelated",
        reason="No AC or shared protocol reference",
    )


def _element_text(element: dict) -> str:
    """Extract all text from an element for pattern matching."""
    parts = []
    for key in ("expr", "name", "field", "message", "timer_name",
                 "type_name", "description", "current_message",
                 "source_req"):
        v = element.get(key, "")
        if isinstance(v, str):
            parts.append(v)
    for key in ("applies_to_messages", "applies_to", "next_allowed",
                 "valid_codes", "allowed_values", "values"):
        v = element.get(key, [])
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)


def _has_ac_ref(text: str) -> bool:
    """Check if text also references AC alongside DC/WPT/ACDP."""
    return bool(re.search(r'\bAC_\w+|\bAC\b', text))


def _find_linked_messages(element: dict, backbone: ACBackbone) -> list[str]:
    """Find AC messages referenced by this element."""
    linked = []
    text = _element_text(element)
    for msg in backbone.ac_messages:
        if msg in text:
            linked.append(msg)
    # Also check applies_to_messages directly
    for msg in element.get("applies_to_messages", []):
        if msg in backbone.ac_messages and msg not in linked:
            linked.append(msg)
    return linked


def _find_linked_states(element: dict, backbone: ACBackbone) -> list[str]:
    """Find AC states referenced by this element."""
    linked = []
    text = _element_text(element)
    for state in backbone.ac_states:
        if state in text:
            linked.append(state)
    return linked


# ═══════════════════════════════════════════════════════════════════════════
# Batch filter
# ═══════════════════════════════════════════════════════════════════════════

def filter_extraction_results(
    vlm_results: dict,
    backbone: ACBackbone,
) -> tuple[dict, dict]:
    """
    Filter VLM extraction results for AC relevance.

    Returns (ac_results, filter_log).
    - ac_results: same structure as vlm_results but only AC-relevant items
    - filter_log: per-category counts (kept, discarded, reasons)
    """
    from multimodal_extractor import ALL_CATEGORIES

    ac_results = {cat: [] for cat in ALL_CATEGORIES}
    filter_log = {}

    for cat in ALL_CATEGORIES:
        items = vlm_results.get(cat, [])
        kept = 0
        discarded = 0
        discarded_items = []

        for item in items:
            result = classify_element(item, cat, backbone)
            if result.is_ac_relevant:
                # Annotate with classification
                item["_ac_type"] = result.relevance_type
                item["_ac_reason"] = result.reason
                item["_linked_messages"] = result.linked_messages
                item["_linked_states"] = result.linked_states
                ac_results[cat].append(item)
                kept += 1
            else:
                discarded += 1
                discarded_items.append({
                    "item_summary": _element_text(item)[:200],
                    "reason": result.reason,
                })

        filter_log[cat] = {
            "total": len(items),
            "kept": kept,
            "discarded": discarded,
            "discarded_items": discarded_items,
        }

    return ac_results, filter_log
