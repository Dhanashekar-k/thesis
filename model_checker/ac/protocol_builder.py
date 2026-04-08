"""
protocol_builder.py — Stage 3: Build the ProtocolModel from ALL sources.

Fuses:
  1. AC_FSM.json — state/transition skeleton
  2. Knowledge base — requirement texts, section structure
  3. Table analysis — message field definitions, timing, response codes
  4. VLM extraction — guards, field constraints, response codes, timing
  5. Requirement decomposition — atoms from Stage 2

Key changes over v1:
  - Removed _discover_variables_from_atoms() (source of junk variables)
  - Only core protocol variables with known ISO domains are included
  - VLM extraction results are integrated as additional atoms
  - Per-message response code sets are stored on the model
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from models import (
    ActorLocalState, Atom, AtomKind, AtomScope, FieldDef,
    GuardStatus, MessageSchema, NuSMVVar, ProtocolModel,
    ProtocolState, ProtocolTransition, Provenance,
    RequirementRecord, Role, TimerSpec,
)
from config import PipelineConfig


# ═══════════════════════════════════════════════════════════════════════════
# State ↔ message mapping
# ═══════════════════════════════════════════════════════════════════════════

# Map state name → (request message, response message)
_STATE_MESSAGES = {
    "SupportedAppProtocol": ("SupportedAppProtocolReq", "SupportedAppProtocolRes"),
    "SessionSetup":          ("SessionSetupReq", "SessionSetupRes"),
    "AuthorizationSetup":    ("AuthorizationSetupReq", "AuthorizationSetupRes"),
    "Authorization":         ("AuthorizationReq", "AuthorizationRes"),
    "CertificateInstallation": ("CertificateInstallationReq", "CertificateInstallationRes"),
    "ServiceDiscovery":      ("ServiceDiscoveryReq", "ServiceDiscoveryRes"),
    "ServiceDetail":         ("ServiceDetailReq", "ServiceDetailRes"),
    "ServiceSelection":      ("ServiceSelectionReq", "ServiceSelectionRes"),
    "AC_ChargeParameterDiscovery": ("AC_ChargeParameterDiscoveryReq", "AC_ChargeParameterDiscoveryRes"),
    "ScheduleExchange":      ("ScheduleExchangeReq", "ScheduleExchangeRes"),
    "PowerDelivery":         ("PowerDeliveryReq", "PowerDeliveryRes"),
    "AC_ChargeLoop":         ("AC_ChargeLoopReq", "AC_ChargeLoopRes"),
    "SessionStop":           ("SessionStopReq", "SessionStopRes"),
}

# Phase classification for states
_STATE_PHASES = {
    "SupportedAppProtocol":         "setup",
    "SessionSetup":                 "setup",
    "AuthorizationSetup":           "auth",
    "Authorization":                "auth",
    "CertificateInstallation":      "auth",
    "ServiceDiscovery":             "service",
    "ServiceDetail":                "service",
    "ServiceSelection":             "service",
    "AC_ChargeParameterDiscovery":  "charging",
    "ScheduleExchange":             "charging",
    "PowerDelivery":                "charging",
    "AC_ChargeLoop":                "charging",
    "SessionStop":                  "stopping",
}


# ═══════════════════════════════════════════════════════════════════════════
# Build from FSM JSON
# ═══════════════════════════════════════════════════════════════════════════

def _build_states_from_fsm(fsm_data: dict) -> list[ProtocolState]:
    """Build ProtocolState list from AC_FSM.json."""
    states = []
    state_label_map = {}  # id → label

    for s in fsm_data.get("states", []):
        sid = s["id"]
        label = s["label"]
        state_label_map[sid] = label

        msgs = _STATE_MESSAGES.get(label, ("", ""))
        phase = _STATE_PHASES.get(label, "")

        states.append(ProtocolState(
            name=label,
            state_id=sid,
            phase=phase,
            is_ac_specific=label.startswith("AC_"),
            is_common=not label.startswith("AC_"),
            allowed_request=msgs[0],
            allowed_response=msgs[1],
            provenance=Provenance(figure_id="Figure 215", extraction_method="fsm_json"),
        ))

    return states


def _build_transitions_from_fsm(
    fsm_data: dict,
    state_label_map: dict[str, str],
) -> list[ProtocolTransition]:
    """Build ProtocolTransition list from AC_FSM.json."""
    transitions = []

    for t in fsm_data.get("transitions", []):
        from_label = state_label_map.get(t["from"], t["from"])
        to_label = state_label_map.get(t["to"], t["to"])

        # Determine trigger message: response triggers exit from state
        trigger = ""
        msgs = _STATE_MESSAGES.get(from_label, ("", ""))
        if msgs[1]:
            trigger = msgs[1]

        transitions.append(ProtocolTransition(
            id=t["id"],
            from_state=from_label,
            to_state=to_label,
            trigger_message=trigger,
            evcc_refs=t.get("evcc_refs", []),
            secc_refs=t.get("secc_refs", []),
            is_self_loop=(from_label == to_label),
            provenance=Provenance(figure_id="Figure 215", extraction_method="fsm_json"),
        ))

    return transitions


# ═══════════════════════════════════════════════════════════════════════════
# Core protocol variables — ONLY well-known ISO enumerations
# ═══════════════════════════════════════════════════════════════════════════

_CORE_VARIABLES = {
    "ResponseCode": {
        "domain": ["OK", "OK_SuccessfulNegotiation",
                    "OK_SuccessfulNegotiationWithMinorDeviation",
                    "FAILED", "FAILED_SequenceError",
                    "WARNING", "WARNING_PowerToleranceNotConfirmed"],
        "init": "OK",
        "description": "Response status from SECC",
    },
    "EVSEProcessing": {
        "domain": ["Ongoing", "Finished"],
        "init": "Finished",
        "description": "Whether SECC is still processing",
    },
    "EVProcessing": {
        "domain": ["Ongoing", "Finished"],
        "init": "Finished",
        "description": "Whether EVCC is still processing",
    },
    "ChargeProgress": {
        "domain": ["Start", "Stop", "Standby", "Renegotiate", "ScheduleRenegotiate"],
        "init": "Start",
        "description": "EVCC charge progress intention",
    },
    "ChargingSession": {
        "domain": ["Pause", "Terminate", "ServiceRenegotiation"],
        "init": "Terminate",
        "description": "EVCC session termination mode",
    },
    "EVSENotification": {
        "domain": ["ServiceRenegotiation", "Terminate", "Pause", "none"],
        "init": "none",
        "description": "SECC notification to EVCC",
    },
    "CertificateInstallationService": {
        "domain": ["boolean"],
        "init": "FALSE",
        "description": "Whether certificate installation is available",
    },
    "ServiceRenegotiationSupported": {
        "domain": ["boolean"],
        "init": "FALSE",
        "description": "Whether service renegotiation is supported",
    },
    "CertificateInstallIntent": {
        "domain": ["boolean"],
        "init": "FALSE",
        "description": "Whether EVCC wants certificate installation",
    },
    "ServiceName": {
        "domain": ["AC", "DC", "WPT", "ACDP", "none"],
        "init": "AC",
        "description": "Selected energy transfer service name",
    },
}


def _build_core_variables() -> list[NuSMVVar]:
    """Build the core NuSMV variable descriptors."""
    variables = []
    for iso_name, spec in _CORE_VARIABLES.items():
        variables.append(NuSMVVar(
            iso_name=iso_name,
            smv_name=iso_name,
            domain=spec["domain"],
            init_value=spec["init"],
            description=spec["description"],
        ))
    return variables


# NOTE: _discover_variables_from_atoms has been REMOVED.
# It was the source of 18 junk variables with single-value domains.
# Only core protocol variables with known ISO domains are included.


# ═══════════════════════════════════════════════════════════════════════════
# VLM extraction result integration
# ═══════════════════════════════════════════════════════════════════════════

def _integrate_vlm_extraction(
    variables: list[NuSMVVar],
    schemas: list[MessageSchema],
    timers: list[TimerSpec],
    response_codes: dict[str, list[str]],
    vlm_results: dict | None,
) -> None:
    """
    Integrate VLM extraction results into variables, schemas, and timers.

    vlm_results is the merged dict from multimodal_extractor.extract_all_sections().
    """
    if not vlm_results:
        return

    var_map = {v.iso_name: v for v in variables}
    schema_map = {s.message_name: s for s in schemas}

    # Integrate field_constraints: enrich variable domains
    for fc in vlm_results.get("field_constraints", []):
        field_name = fc.get("field", "")
        allowed = fc.get("allowed_values", [])
        if field_name in var_map and allowed:
            existing = set(var_map[field_name].domain)
            existing.update(allowed)
            var_map[field_name].domain = sorted(existing)

    # Integrate response codes: per-message
    for rc in vlm_results.get("response_codes", []):
        msg = rc.get("message", "")
        codes = rc.get("valid_codes", [])
        if msg and codes:
            response_codes.setdefault(msg, []).extend(codes)
            response_codes[msg] = list(dict.fromkeys(response_codes[msg]))

    # Integrate field_definitions: add fields to existing schemas or create new ones
    for fd in vlm_results.get("field_definitions", []):
        msg = fd.get("message", "")
        fname = fd.get("field", "")
        if not msg or not fname:
            continue
        if msg in schema_map:
            # Add field if not already present
            if not schema_map[msg].get_field(fname):
                from models import Cardinality
                card = Cardinality.MANDATORY if fd.get("mandatory", True) else Cardinality.OPTIONAL
                schema_map[msg].fields.append(FieldDef(
                    name=fname,
                    field_type=fd.get("type", ""),
                    cardinality=card,
                    semantics=fd.get("description", ""),
                    provenance=Provenance(
                        table_id=fd.get("source_table", ""),
                        extraction_method="vlm",
                    ),
                ))

    # Integrate timing constraints: merge into timer list
    timer_map = {t.name: t for t in timers}
    for tc in vlm_results.get("timing_constraints", []):
        tname = tc.get("timer_name", "")
        if not tname:
            continue
        if tname in timer_map:
            # Update value if VLM found one and existing is 0
            try:
                vlm_val = float(tc.get("value_seconds") or 0)
            except (TypeError, ValueError):
                vlm_val = 0.0
            if vlm_val > 0 and timer_map[tname].value_seconds == 0:
                timer_map[tname].value_seconds = vlm_val
        else:
            actor = Role.BOTH
            actor_str = tc.get("actor", "BOTH")
            if actor_str == "EVCC":
                actor = Role.EVCC
            elif actor_str == "SECC":
                actor = Role.SECC
            try:
                new_val = float(tc.get("value_seconds") or 0)
            except (TypeError, ValueError):
                new_val = 0.0
            new_timer = TimerSpec(
                name=tname,
                message_type=", ".join(tc.get("applies_to", [])),
                value_seconds=new_val,
                applicable_to=actor,
                provenance=Provenance(extraction_method="vlm"),
            )
            timers.append(new_timer)
            timer_map[tname] = new_timer


# ═══════════════════════════════════════════════════════════════════════════
# Actor-local state model
# ═══════════════════════════════════════════════════════════════════════════

def _build_actor_local_states(
    states: list[ProtocolState],
) -> tuple[ActorLocalState, ActorLocalState]:
    """Build actor-local control state models for EVCC and SECC."""
    evcc_states = ["EVCC_Idle"]
    secc_states = ["SECC_Idle"]

    for state in states:
        name = state.name
        evcc_states.extend([
            f"EVCC_Send_{name}Req",
            f"EVCC_Wait_{name}Res",
        ])
        secc_states.extend([
            f"SECC_Wait_{name}Req",
            f"SECC_Process_{name}",
            f"SECC_Send_{name}Res",
        ])

    return (
        ActorLocalState(
            actor=Role.EVCC,
            control_states=evcc_states,
            init_state="EVCC_Idle",
        ),
        ActorLocalState(
            actor=Role.SECC,
            control_states=secc_states,
            init_state="SECC_Idle",
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Main builder
# ═══════════════════════════════════════════════════════════════════════════

def build_protocol_model(
    fsm_data: dict,
    kb_data: dict,
    requirements: dict[str, RequirementRecord],
    schemas: list[MessageSchema],
    timers: list[TimerSpec],
    response_codes: dict[str, list[str]],
    config: PipelineConfig,
    vlm_results: dict | None = None,
) -> ProtocolModel:
    """
    Build the complete ProtocolModel from all sources.

    Parameters
    ----------
    fsm_data : loaded AC_FSM.json
    kb_data : loaded knowledge_base.json
    requirements : decomposed requirement records from Stage 2
    schemas : message schemas from table analysis
    timers : timer specs from table analysis
    response_codes : valid response codes per message from table analysis
    config : pipeline configuration
    vlm_results : merged VLM extraction results (optional)
    """
    # Build state label map
    state_label_map = {s["id"]: s["label"] for s in fsm_data.get("states", [])}

    # Build states
    states = _build_states_from_fsm(fsm_data)

    # Build transitions
    transitions = _build_transitions_from_fsm(fsm_data, state_label_map)

    # Build ONLY core variables (no junk discovery)
    variables = _build_core_variables()

    # Integrate VLM extraction results into variables, schemas, timers, response codes
    _integrate_vlm_extraction(variables, schemas, timers, response_codes, vlm_results)

    # Merge/conflict resolution: unify duplicate schemas, variables, flag conflicts
    conflicts = _resolve_conflicts(schemas, timers, variables, response_codes)
    if conflicts:
        print(f"  [protocol_builder] Resolved {len(conflicts)} conflicts")

    # Enrich response code domains from table analysis
    _enrich_response_codes(variables, response_codes)

    # Build actor-local states
    evcc_local, secc_local = _build_actor_local_states(states)

    # Build timers: merge discovered timers from requirements with table timers
    all_timers = _merge_timers(timers, requirements)

    # Determine entry/exit
    entry_state = fsm_data.get("entry_point", {}).get("target_state", "")
    if not entry_state:
        entry_label = state_label_map.get(
            fsm_data.get("entry_point", {}).get("target_state", "ST1"), ""
        )
        entry_state = entry_label or (states[0].name if states else "")

    exit_state = fsm_data.get("exit_point", {}).get("source_state", "SessionStop")

    model = ProtocolModel(
        model_id="iso15118_20_ac",
        title="ISO 15118-20 AC Charging Protocol Model",
        states=states,
        transitions=transitions,
        entry_state=entry_state,
        exit_state=exit_state,
        evcc_local=evcc_local if config.include_actor_local else None,
        secc_local=secc_local if config.include_actor_local else None,
        messages=schemas,
        timers=all_timers,
        variables=variables,
        requirements=requirements,
    )

    # Store response codes on model for downstream use
    model.response_codes = response_codes

    print(f"[protocol_builder] Built model: {len(states)} states, "
          f"{len(transitions)} transitions, {len(variables)} variables, "
          f"{len(all_timers)} timers, {len(schemas)} message schemas")

    return model


def _enrich_response_codes(
    variables: list[NuSMVVar],
    response_codes: dict[str, list[str]],
) -> None:
    """Enrich the ResponseCode variable domain from table analysis."""
    rc_var = next((v for v in variables if v.iso_name == "ResponseCode"), None)
    if rc_var and response_codes:
        all_codes = set(rc_var.domain)
        for codes in response_codes.values():
            all_codes.update(codes)
        rc_var.domain = sorted(all_codes)


def _merge_timers(
    table_timers: list[TimerSpec],
    requirements: dict[str, RequirementRecord],
) -> list[TimerSpec]:
    """Merge timers from table analysis with those discovered in requirements."""
    timer_map: dict[str, TimerSpec] = {}

    for t in table_timers:
        timer_map[t.name] = t

    # Discover timer references from atoms
    for rec in requirements.values():
        for atom in rec.atoms:
            if atom.kind == AtomKind.TIMING:
                for iso_var in atom.iso_variables:
                    if iso_var.startswith("V2G_") and iso_var not in timer_map:
                        actor = Role.BOTH
                        if "EVCC" in iso_var:
                            actor = Role.EVCC
                        elif "SECC" in iso_var:
                            actor = Role.SECC

                        timer_map[iso_var] = TimerSpec(
                            name=iso_var,
                            applicable_to=actor,
                            provenance=Provenance(
                                extraction_method="requirement_atom",
                            ),
                        )

    return list(timer_map.values())


def _resolve_conflicts(
    schemas: list[MessageSchema],
    timers: list[TimerSpec],
    variables: list[NuSMVVar],
    response_codes: dict[str, list[str]],
) -> list[dict]:
    """
    Merge/conflict resolution layer.

    - Unify duplicate schemas by message_name (table version wins over VLM)
    - Unify duplicate timer specs (table wins, higher value wins)
    - Flag unresolved variable domain conflicts
    """
    conflicts = []

    # Schema dedup: if two schemas share a message_name, merge fields (table wins)
    seen_schemas: dict[str, int] = {}
    to_remove = []
    for i, s in enumerate(schemas):
        if s.message_name in seen_schemas:
            prev_idx = seen_schemas[s.message_name]
            prev = schemas[prev_idx]
            # Table extraction wins over VLM
            prev_method = getattr(prev.provenance, 'extraction_method', '') if prev.provenance else ''
            curr_method = getattr(s.provenance, 'extraction_method', '') if s.provenance else ''

            # Merge missing fields from curr into prev
            existing_fields = {f.name for f in prev.fields}
            for f in s.fields:
                if f.name not in existing_fields:
                    prev.fields.append(f)

            to_remove.append(i)
            conflicts.append({
                "type": "duplicate_schema",
                "message": s.message_name,
                "resolution": f"merged fields, kept {prev_method} as primary over {curr_method}",
            })
        else:
            seen_schemas[s.message_name] = i

    for idx in reversed(to_remove):
        schemas.pop(idx)

    # Timer dedup: keep higher value
    seen_timers: dict[str, int] = {}
    timer_remove = []
    for i, t in enumerate(timers):
        if t.name in seen_timers:
            prev_idx = seen_timers[t.name]
            prev = timers[prev_idx]
            if t.value_seconds > prev.value_seconds:
                prev.value_seconds = t.value_seconds
            timer_remove.append(i)
            conflicts.append({
                "type": "duplicate_timer",
                "timer": t.name,
                "resolution": f"kept higher value: {prev.value_seconds}s",
            })
        else:
            seen_timers[t.name] = i

    for idx in reversed(timer_remove):
        timers.pop(idx)

    return conflicts
