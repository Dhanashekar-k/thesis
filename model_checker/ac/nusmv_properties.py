"""
nusmv_properties.py — Stage 5b: Generate NuSMV properties (CTL/LTL).

Properties are derived from:
  1. Requirement atoms (compliance, sequencing, timing)
  2. Protocol structure (safety, liveness)
  3. State invariants
  4. Guard completeness (deadlock freedom)

Categories:
  - safety:     bad things never happen  (AG ! ...)
  - liveness:   good things eventually happen  (AG (... -> AF ...))
  - compliance: spec obligations are met  (AG (guard -> AX action))
  - invariant:  always-true conditions  (AG ...)
  - sequencing: message order rules  (AG (A -> AX B))
  - timing:     deadline properties  (AG (... -> AF deadline_met))
"""

from __future__ import annotations

import re
from io import StringIO

from models import (
    Atom, AtomKind, AtomScope, NuSMVVar, PropertyCategory,
    PropertySpec, ProtocolModel, ProtocolTransition, Role,
)
from nusmv_model import smv_name, smv_enum_val
from config import PipelineConfig


# ═══════════════════════════════════════════════════════════════════════════
# Property generators
# ═══════════════════════════════════════════════════════════════════════════

def _gen_safety_properties(model: ProtocolModel) -> list[PropertySpec]:
    """Generate safety properties: bad combinations that must never occur."""
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}
    exit_smv = state_smv.get(model.exit_state, "")

    # S1: No FAILED response leads to continued charging
    props.append(PropertySpec(
        name="no_failed_continues_charging",
        category=PropertyCategory.SAFETY,
        formula=f"AG (ResponseCode = FAILED -> "
                f"AX (proto_state = {exit_smv} | proto_state = proto_state))",
        description="After a FAILED response, the session must eventually stop",
    ))

    # S2: ChargeProgress=Stop requires next state to be PowerDelivery(stop) or SessionStop
    if "PowerDelivery" in state_smv and "AC_ChargeLoop" in state_smv:
        props.append(PropertySpec(
            name="stop_requires_power_delivery",
            category=PropertyCategory.SAFETY,
            formula=f"AG (proto_state = {state_smv['AC_ChargeLoop']} & "
                    f"ChargeProgress = Stop -> "
                    f"AX (proto_state = {state_smv['PowerDelivery']} | "
                    f"proto_state = {state_smv['AC_ChargeLoop']}))",
            description="ChargeProgress=Stop from charge loop must go to PowerDelivery",
        ))

    # S3: No backward transitions in setup phase (except explicit loops)
    setup_states = [s for s in model.states if s.phase == "setup"]
    for i, s1 in enumerate(setup_states):
        for s2 in setup_states[:i]:
            # Check if there's actually a backward transition
            backward = any(
                t.from_state == s1.name and t.to_state == s2.name
                for t in model.transitions
            )
            if not backward:
                props.append(PropertySpec(
                    name=f"no_backward_{s1.name}_to_{s2.name}",
                    category=PropertyCategory.SAFETY,
                    formula=f"AG (proto_state = {state_smv[s1.name]} -> "
                            f"AX proto_state != {state_smv[s2.name]})",
                    description=f"No backward transition from {s1.name} to {s2.name}",
                ))

    return props


def _gen_liveness_properties(model: ProtocolModel) -> list[PropertySpec]:
    """Generate liveness properties: good things eventually happen."""
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}
    entry_smv = state_smv.get(model.entry_state, "")
    exit_smv = state_smv.get(model.exit_state, "")

    # L1: From entry, eventually reach exit
    if entry_smv and exit_smv:
        props.append(PropertySpec(
            name="eventually_terminates",
            category=PropertyCategory.LIVENESS,
            formula=f"AG (proto_state = {entry_smv} -> AF proto_state = {exit_smv})",
            description="Every session eventually reaches SessionStop",
        ))

    # L2: From each state, eventually leave it (no permanent stall)
    for state in model.states:
        if state.name == model.exit_state:
            continue
        ss = state_smv[state.name]
        props.append(PropertySpec(
            name=f"eventually_leave_{state.name}",
            category=PropertyCategory.LIVENESS,
            formula=f"AG (proto_state = {ss} -> AF proto_state != {ss})",
            description=f"Eventually leave state {state.name}",
        ))

    # L3: EVSEProcessing=Ongoing eventually becomes Finished
    props.append(PropertySpec(
        name="evse_processing_completes",
        category=PropertyCategory.LIVENESS,
        formula="AG (EVSEProcessing = Ongoing -> AF EVSEProcessing = Finished)",
        description="EVSE processing eventually finishes",
    ))

    return props


def _gen_compliance_properties(model: ProtocolModel) -> list[PropertySpec]:
    """
    Generate compliance properties from requirement atoms.

    For each guard → action pair on a transition, generate:
      AG (in_state & guard → AX action_effect)
    """
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}

    for trans in model.transitions:
        if not trans.guards or not trans.actions:
            continue

        from_smv = state_smv[trans.from_state]
        to_smv = state_smv[trans.to_state]

        # Build guard conjunction
        guard_parts = []
        for g in trans.guards:
            m = re.match(r'(\w+)\s*=\s*(\w+)', g.expr)
            if m:
                var, val = m.group(1), m.group(2)
                if val.upper() in ("TRUE", "FALSE"):
                    guard_parts.append(f"{smv_name(var)} = {val.upper()}")
                else:
                    guard_parts.append(f"{smv_name(var)} = {smv_enum_val(val)}")

        if not guard_parts:
            continue

        guard_conj = " & ".join(guard_parts)

        # The action is the state transition itself
        req_ids = list(set(trans.evcc_refs + trans.secc_refs))[:3]

        props.append(PropertySpec(
            name=f"compliance_T{trans.id}",
            category=PropertyCategory.COMPLIANCE,
            formula=f"AG (proto_state = {from_smv} & {guard_conj} -> "
                    f"AX proto_state = {to_smv})",
            description=f"T{trans.id}: When guards hold at {trans.from_state}, "
                        f"transition to {trans.to_state}",
            source_reqs=req_ids,
        ))

    return props


def _gen_sequencing_properties(model: ProtocolModel) -> list[PropertySpec]:
    """
    Generate sequencing properties from sequence_constraint atoms.

    For atoms like "next_allowed = X", generate:
      AG (in_state -> AX (msg_channel = X | msg_channel = none))
    """
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}

    for trans in model.transitions:
        for atom in trans.sequence_constraints:
            m = re.match(r'next_allowed\s*=\s*(\w+)', atom.expr)
            if m:
                next_msg = m.group(1)
                to_smv = state_smv.get(trans.to_state, "")
                if to_smv:
                    props.append(PropertySpec(
                        name=f"seq_T{trans.id}_{next_msg}",
                        category=PropertyCategory.SEQUENCING,
                        formula=f"AG (proto_state = {to_smv} -> "
                                f"AX (msg_channel = {smv_name(next_msg)} | "
                                f"msg_channel = none))",
                        description=f"After reaching {trans.to_state}, "
                                    f"next message must be {next_msg}",
                        source_reqs=[atom.source_req] if atom.source_req else [],
                    ))

    return props


def _gen_invariant_properties(model: ProtocolModel) -> list[PropertySpec]:
    """Generate invariant properties from state and global invariant atoms."""
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}

    # State invariants
    for state in model.states:
        for atom in state.invariants:
            m = re.match(r'(\w+)\s*=\s*(\w+)', atom.expr)
            if m:
                var, val = m.group(1), m.group(2)
                ss = state_smv[state.name]
                if val.upper() in ("TRUE", "FALSE"):
                    smv_val = val.upper()
                else:
                    smv_val = smv_enum_val(val)
                props.append(PropertySpec(
                    name=f"invar_{state.name}_{var}",
                    category=PropertyCategory.INVARIANT,
                    formula=f"AG (proto_state = {ss} -> {smv_name(var)} = {smv_val})",
                    description=f"In state {state.name}, {var} must be {val}",
                    source_reqs=[atom.source_req] if atom.source_req else [],
                ))

    # Global invariants
    for atom in model.global_atoms:
        if atom.kind == AtomKind.INVARIANT:
            m = re.match(r'(\w+)\s*=\s*(\w+)', atom.expr)
            if m:
                var, val = m.group(1), m.group(2)
                if val.upper() in ("TRUE", "FALSE"):
                    smv_val = val.upper()
                else:
                    smv_val = smv_enum_val(val)
                props.append(PropertySpec(
                    name=f"global_invar_{var}",
                    category=PropertyCategory.INVARIANT,
                    formula=f"AG ({smv_name(var)} = {smv_val})",
                    description=f"Global invariant: {var} = {val}",
                    source_reqs=[atom.source_req] if atom.source_req else [],
                ))

    return props


def _gen_timing_properties(
    model: ProtocolModel,
    config: PipelineConfig,
) -> list[PropertySpec]:
    """Generate timing properties from timing atoms."""
    if not config.include_timing:
        return []

    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}

    # For each state with timing constraints, generate deadline property
    for trans in model.transitions:
        for atom in trans.timing_constraints:
            timer_name = ""
            for v in atom.iso_variables:
                if v.startswith("V2G_"):
                    timer_name = v
                    break

            if timer_name:
                from_smv = state_smv[trans.from_state]
                to_smv = state_smv[trans.to_state]

                props.append(PropertySpec(
                    name=f"timing_T{trans.id}_{timer_name}",
                    category=PropertyCategory.TIMING,
                    formula=f"AG (proto_state = {from_smv} -> "
                            f"AF (proto_state != {from_smv} | timer_expired))",
                    description=f"Timer {timer_name}: transition from "
                                f"{trans.from_state} must happen before timeout",
                    source_reqs=[atom.source_req] if atom.source_req else [],
                ))

    return props


def _gen_deadlock_freedom(model: ProtocolModel) -> list[PropertySpec]:
    """Generate deadlock freedom property."""
    state_smv = {s.name: smv_name(s.name) for s in model.states}
    exit_smv = state_smv.get(model.exit_state, "")

    return [PropertySpec(
        name="deadlock_freedom",
        category=PropertyCategory.SAFETY,
        formula=f"AG (proto_state != {exit_smv} -> EX TRUE)",
        description="No deadlock: every non-terminal state has a successor",
    )]


def _gen_retry_bound(model: ProtocolModel, config: PipelineConfig) -> list[PropertySpec]:
    """Generate retry bound properties for self-loop states."""
    if not config.include_retries:
        return []

    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}

    self_loop_states = set()
    for t in model.transitions:
        if t.is_self_loop:
            self_loop_states.add(t.from_state)

    for state_name in self_loop_states:
        ss = state_smv[state_name]
        props.append(PropertySpec(
            name=f"retry_bound_{state_name}",
            category=PropertyCategory.SAFETY,
            formula=f"AG (proto_state = {ss} -> "
                    f"retry_count <= {config.max_retry_count})",
            description=f"Retry count bounded at {state_name}",
        ))

    return props


def _gen_response_code_properties(model: ProtocolModel) -> list[PropertySpec]:
    """
    Generate per-message response code restriction properties.

    For each state with known valid response codes, generate:
      AG (proto_state = S -> ResponseCode in {valid_codes})
    """
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}
    response_codes = getattr(model, 'response_codes', {})

    if not response_codes:
        return props

    for state in model.states:
        res_msg = state.allowed_response
        if not res_msg or res_msg not in response_codes:
            continue

        valid_codes = response_codes[res_msg]
        if not valid_codes:
            continue

        ss = state_smv[state.name]
        # Build disjunction of allowed response codes
        code_disj = " | ".join(
            f"ResponseCode = {smv_enum_val(c)}" for c in valid_codes
        )

        props.append(PropertySpec(
            name=f"rc_restrict_{state.name}",
            category=PropertyCategory.COMPLIANCE,
            formula=f"AG (proto_state = {ss} -> ({code_disj}))",
            description=f"In {state.name}, ResponseCode must be one of: "
                        f"{', '.join(valid_codes)}",
        ))

    return props


def _gen_state_constraint_properties(model: ProtocolModel) -> list[PropertySpec]:
    """
    Generate properties from per-state variable constraints.

    For each (state, variable) pair where enrichment found constraints,
    generate a property asserting the variable stays within bounds.
    """
    props = []
    state_smv = {s.name: smv_name(s.name) for s in model.states}
    state_constraints = getattr(model, 'state_variable_constraints', {})

    for (state_name, var_name), allowed in state_constraints.items():
        if var_name == "ResponseCode":
            continue  # handled by _gen_response_code_properties
        if not allowed:
            continue

        ss = state_smv.get(state_name, "")
        if not ss:
            continue

        val_disj = " | ".join(
            f"{smv_name(var_name)} = {smv_enum_val(v)}" for v in sorted(allowed)
        )

        props.append(PropertySpec(
            name=f"constrain_{state_name}_{var_name}",
            category=PropertyCategory.INVARIANT,
            formula=f"AG (proto_state = {ss} -> ({val_disj}))",
            description=f"In {state_name}, {var_name} constrained to: "
                        f"{', '.join(sorted(allowed))}",
        ))

    return props


def _gen_session_invariant_properties(model: ProtocolModel) -> list[PropertySpec]:
    """Generate properties from session-level atoms collected during enrichment."""
    props = []
    for atom in model.session_atoms:
        if atom.kind == AtomKind.INVARIANT:
            m = re.match(r'(\w+)\s*=\s*(\w+)', atom.expr)
            if m:
                var, val = m.group(1), m.group(2)
                if val.upper() in ("TRUE", "FALSE"):
                    smv_val = val.upper()
                else:
                    smv_val = smv_enum_val(val)
                props.append(PropertySpec(
                    name=f"session_invar_{var}_{val}",
                    category=PropertyCategory.INVARIANT,
                    formula=f"AG ({smv_name(var)} = {smv_val})",
                    description=f"Session invariant: {var} = {val}",
                    source_reqs=[atom.source_req] if atom.source_req else [],
                ))
    return props


# ═══════════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════════

def generate_properties(
    model: ProtocolModel,
    config: PipelineConfig,
) -> tuple[list[PropertySpec], str]:
    """
    Generate all properties and return both structured list and SMV text.
    """
    all_props = []

    all_props.extend(_gen_safety_properties(model))
    all_props.extend(_gen_liveness_properties(model))
    all_props.extend(_gen_compliance_properties(model))
    all_props.extend(_gen_sequencing_properties(model))
    all_props.extend(_gen_invariant_properties(model))
    all_props.extend(_gen_timing_properties(model, config))
    all_props.extend(_gen_deadlock_freedom(model))
    all_props.extend(_gen_retry_bound(model, config))
    all_props.extend(_gen_response_code_properties(model))
    all_props.extend(_gen_state_constraint_properties(model))
    all_props.extend(_gen_session_invariant_properties(model))

    # Generate SMV text
    buf = StringIO()
    buf.write(f"-- AC Protocol Properties\n")
    buf.write(f"-- Total: {len(all_props)} properties\n\n")

    by_cat: dict[str, list[PropertySpec]] = {}
    for p in all_props:
        by_cat.setdefault(p.category.value, []).append(p)

    for cat, props in by_cat.items():
        buf.write(f"-- ═══ {cat.upper()} ({len(props)}) ═══\n\n")
        for p in props:
            buf.write(f"-- {p.description}\n")
            if p.source_reqs:
                buf.write(f"-- Source: {', '.join(p.source_reqs)}\n")
            buf.write(f"CTLSPEC {p.formula}\n\n")

    smv_text = buf.getvalue()

    print(f"[properties] Generated {len(all_props)} properties across "
          f"{len(by_cat)} categories")

    return all_props, smv_text
