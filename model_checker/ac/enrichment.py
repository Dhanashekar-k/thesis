"""
enrichment.py — Stage 4: Attach atoms to protocol elements and resolve constraints.

After the ProtocolModel skeleton is built and requirements are decomposed,
this stage:
  1. Binds atoms to transitions by matching req IDs
  2. Binds atoms to states by scope
  3. Builds per-state variable constraint map (the key new feature)
  4. Integrates VLM-extracted guards and sequence constraints
  5. Classifies transition guard completeness
  6. Collects session-level and global-level atoms

Key improvement: _build_per_state_variable_constraints() creates a dict
mapping (state_name, variable_name) → set of allowed values, derived from
the guard conditions on outgoing transitions from that state. This is used
by nusmv_model.py to constrain next() per state rather than allowing free
nondeterminism globally.
"""

from __future__ import annotations

import re
from typing import Optional

from models import (
    Atom, AtomKind, AtomScope, DiagnosticItem, DiagnosticSeverity,
    GuardStatus, NuSMVVar, ProtocolModel, ProtocolTransition,
    RequirementRecord, Role,
)
from config import PipelineConfig


# ═══════════════════════════════════════════════════════════════════════════
# Atom → Transition binding
# ═══════════════════════════════════════════════════════════════════════════

def _bind_atoms_to_transitions(model: ProtocolModel) -> list[DiagnosticItem]:
    """
    Bind atoms from requirement records to transitions via V2G20 refs.

    Each transition has evcc_refs and secc_refs listing the V2G20 IDs
    that govern it.  We attach atoms from those requirements to the
    appropriate atom list on the transition.
    """
    diagnostics = []
    requirements = model.requirements

    # Normalize all requirement refs on transitions
    _normalize_transition_refs(model)

    for trans in model.transitions:
        all_refs = set(trans.evcc_refs + trans.secc_refs)

        for ref in all_refs:
            rec = requirements.get(ref)
            if rec is None:
                diagnostics.append(DiagnosticItem(
                    severity=DiagnosticSeverity.WARNING,
                    stage="enrichment",
                    message=f"Requirement {ref} referenced by transition {trans.id} "
                            f"({trans.from_state} → {trans.to_state}) not found in KB",
                    related_req=ref,
                    related_transition=trans.id,
                ))
                continue

            # Determine actor for this ref
            actor = Role.BOTH
            if ref in trans.evcc_refs and ref not in trans.secc_refs:
                actor = Role.EVCC
            elif ref in trans.secc_refs and ref not in trans.evcc_refs:
                actor = Role.SECC

            for atom in rec.atoms:
                # Override actor if the transition gives clearer info
                bound_atom = _clone_atom(atom)
                if bound_atom.actor == Role.BOTH and actor != Role.BOTH:
                    bound_atom.actor = actor

                # Route atom to appropriate list based on kind
                if atom.scope == AtomScope.TRANSITION:
                    _route_atom_to_transition(bound_atom, trans)
                elif atom.scope == AtomScope.STATE:
                    _route_atom_to_transition(bound_atom, trans)
                elif atom.scope in (AtomScope.SESSION, AtomScope.GLOBAL):
                    # These go to model-level, handled separately
                    pass
                else:
                    _route_atom_to_transition(bound_atom, trans)

        # Also bind atoms by message name match (not just req ID)
        trigger = trans.trigger_message
        if trigger:
            for rec in requirements.values():
                for atom in rec.atoms:
                    if trigger in atom.applies_to_messages:
                        # Check if already bound via req ID
                        if not any(g.expr == atom.expr and g.source_req == atom.source_req
                                   for g in trans.guards + trans.actions + trans.timing_constraints):
                            bound_atom = _clone_atom(atom)
                            bound_atom.notes = (bound_atom.notes or "") + f" [bound via message:{trigger}]"
                            _route_atom_to_transition(bound_atom, trans)

        # Classify guard completeness
        _classify_transition_guards(trans, model.config_threshold)

    # Deduplicate guards per transition
    _dedup_transition_guards(model)

    return diagnostics


def _dedup_transition_guards(model: ProtocolModel) -> None:
    """
    Deduplicate guard atoms on each transition.

    When the same variable appears in multiple guard atoms with different
    values (e.g. EVSEProcessing=Finished AND EVSEProcessing=Ongoing from
    different requirements), keep only the unique values. These represent
    alternative conditions, not a conjunction.

    The NuSMV emitter will combine same-variable guards into disjunctions.
    """
    for trans in model.transitions:
        if not trans.guards:
            continue
        seen_exprs: set[str] = set()
        deduped: list[Atom] = []
        for g in trans.guards:
            if g.expr not in seen_exprs:
                seen_exprs.add(g.expr)
                deduped.append(g)
        trans.guards = deduped


def _route_atom_to_transition(atom: Atom, trans: ProtocolTransition) -> None:
    """Route an atom to the correct list on a transition."""
    if atom.kind == AtomKind.GUARD:
        trans.guards.append(atom)
    elif atom.kind == AtomKind.ACTION:
        trans.actions.append(atom)
    elif atom.kind == AtomKind.TIMING:
        trans.timing_constraints.append(atom)
    elif atom.kind == AtomKind.FIELD_CONSTRAINT:
        trans.field_constraints.append(atom)
    elif atom.kind == AtomKind.SEQUENCE_CONSTRAINT:
        trans.sequence_constraints.append(atom)
    elif atom.kind == AtomKind.INVARIANT:
        trans.invariants.append(atom)
    elif atom.kind == AtomKind.ASSUMPTION:
        trans.guards.append(atom)  # assumptions act like guards
    else:
        trans.unresolved_items.append(atom)


def _classify_transition_guards(trans: ProtocolTransition, threshold: float) -> None:
    """Classify the guard completeness of a transition."""
    if not trans.guards:
        trans.guard_status = GuardStatus.UNKNOWN
    elif all(g.guard_status == GuardStatus.KNOWN and g.confidence >= threshold
             for g in trans.guards):
        trans.guard_status = GuardStatus.KNOWN
    else:
        trans.guard_status = GuardStatus.PARTIAL


def _clone_atom(atom: Atom) -> Atom:
    """Create a shallow copy of an atom."""
    return Atom(
        kind=atom.kind,
        actor=atom.actor,
        scope=atom.scope,
        expr=atom.expr,
        applies_to_transitions=list(atom.applies_to_transitions),
        applies_to_states=list(atom.applies_to_states),
        applies_to_messages=list(atom.applies_to_messages),
        source_req=atom.source_req,
        confidence=atom.confidence,
        guard_status=atom.guard_status,
        iso_variables=list(atom.iso_variables),
        notes=atom.notes,
        provenance=atom.provenance,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Requirement ref normalization (replaces old OCR typo fix)
# ═══════════════════════════════════════════════════════════════════════════

def _normalize_transition_refs(model: ProtocolModel) -> None:
    """Normalize all requirement ID references on transitions using normalization module."""
    from normalization import normalize_req_id_bare
    for trans in model.transitions:
        trans.evcc_refs = [normalize_req_id_bare(r, context=f"trans_{trans.id}_evcc") for r in trans.evcc_refs]
        trans.secc_refs = [normalize_req_id_bare(r, context=f"trans_{trans.id}_secc") for r in trans.secc_refs]


# ═══════════════════════════════════════════════════════════════════════════
# Session/Global atom collection
# ═══════════════════════════════════════════════════════════════════════════

def _collect_scope_atoms(model: ProtocolModel) -> None:
    """Collect session-level and global-level atoms from requirements."""
    for rec in model.requirements.values():
        for atom in rec.atoms:
            if atom.scope == AtomScope.SESSION:
                model.session_atoms.append(atom)
            elif atom.scope == AtomScope.GLOBAL:
                model.global_atoms.append(atom)


# ═══════════════════════════════════════════════════════════════════════════
# Variable domain constraining
# ═══════════════════════════════════════════════════════════════════════════

def _constrain_variable_domains(model: ProtocolModel) -> list[DiagnosticItem]:
    """
    Build per-state variable constraint map.

    For each state, inspect outgoing transitions' guard atoms to determine
    which variable values are meaningful in that state. Store the result
    on model.state_variable_constraints as:
        dict[ (state_name, var_name) ] → set[allowed_values]

    This is the key data structure that nusmv_model.py uses to generate
    state-specific next() case branches instead of unconstrained nondeterminism.
    """
    diagnostics = []
    var_map = {v.iso_name: v for v in model.variables}

    # Initialize the constraint map on the model
    if not hasattr(model, 'state_variable_constraints'):
        model.state_variable_constraints = {}

    for state in model.states:
        outgoing = model.get_transitions_from(state.name)
        state_guard_values: dict[str, set[str]] = {}

        for trans in outgoing:
            for guard in trans.guards:
                if guard.kind == AtomKind.GUARD:
                    m = re.match(r'(\w+)\s*=\s*(\w+)', guard.expr)
                    if m:
                        vname, vval = m.group(1), m.group(2)
                        if vname in var_map:
                            state_guard_values.setdefault(vname, set()).add(vval)

            # Also check field_constraints for response code restrictions
            for fc in trans.field_constraints:
                m = re.match(r'(\w+)\s*=\s*(\w+)', fc.expr)
                if m:
                    vname, vval = m.group(1), m.group(2)
                    if vname in var_map:
                        state_guard_values.setdefault(vname, set()).add(vval)

        # Store constraints
        for vname, values in state_guard_values.items():
            key = (state.name, vname)
            model.state_variable_constraints[key] = values

            # Also record on the NuSMVVar for diagnostics
            var = var_map.get(vname)
            if var:
                var.constrained_by.append(f"{state.name}: {sorted(values)}")

    # Also integrate per-message response code constraints
    response_codes = getattr(model, 'response_codes', {})
    if response_codes:
        for state in model.states:
            res_msg = state.allowed_response
            if res_msg and res_msg in response_codes:
                key = (state.name, "ResponseCode")
                if key not in model.state_variable_constraints:
                    model.state_variable_constraints[key] = set()
                model.state_variable_constraints[key].update(response_codes[res_msg])

    # Add message-specific variable constraints from schemas
    for state in model.states:
        for msg_name in [state.allowed_request, state.allowed_response]:
            if not msg_name:
                continue
            for schema in model.messages:
                if schema.message_name != msg_name:
                    continue
                for fd in schema.fields:
                    if fd.value_domain and fd.name in var_map:
                        key = (state.name, fd.name)
                        if key not in model.state_variable_constraints:
                            model.state_variable_constraints[key] = set()
                        model.state_variable_constraints[key].update(fd.value_domain)

    return diagnostics


# ═══════════════════════════════════════════════════════════════════════════
# State invariant attachment
# ═══════════════════════════════════════════════════════════════════════════

def _attach_state_invariants(model: ProtocolModel) -> None:
    """Attach invariant atoms to states."""
    for rec in model.requirements.values():
        for atom in rec.atoms:
            if atom.kind == AtomKind.INVARIANT and atom.scope == AtomScope.STATE:
                for state_name in atom.applies_to_states:
                    state = model.get_state(state_name)
                    if state:
                        state.invariants.append(atom)


# ═══════════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════════

def enrich_model(
    model: ProtocolModel,
    config: PipelineConfig,
    vlm_results: dict | None = None,
) -> list[DiagnosticItem]:
    """
    Enrich the protocol model by binding atoms to transitions and states.

    Modifies the model in-place. Returns diagnostics.

    Parameters
    ----------
    model : the protocol model to enrich
    config : pipeline configuration
    vlm_results : merged VLM extraction results (optional)
    """
    model.config_threshold = config.confidence_threshold  # temp attribute

    all_diagnostics = []

    # 1. Bind atoms to transitions
    diags = _bind_atoms_to_transitions(model)
    all_diagnostics.extend(diags)

    # 1b. Integrate VLM-extracted guards and sequence constraints
    if vlm_results:
        _integrate_vlm_guards(model, vlm_results)

    # 2. Collect session/global atoms
    _collect_scope_atoms(model)

    # 3. Attach state invariants
    _attach_state_invariants(model)

    # 4. Constrain variable domains per state
    diags = _constrain_variable_domains(model)
    all_diagnostics.extend(diags)

    # Clean up temp attribute
    if hasattr(model, 'config_threshold'):
        del model.config_threshold

    # Stats
    total_bound = sum(
        len(t.all_atoms) for t in model.transitions
    )
    unresolved = sum(
        len(t.unresolved_items) for t in model.transitions
    )
    constrained_pairs = len(getattr(model, 'state_variable_constraints', {}))

    print(f"[enrichment] Bound {total_bound} atoms to transitions "
          f"({unresolved} unresolved), "
          f"{len(model.session_atoms)} session atoms, "
          f"{len(model.global_atoms)} global atoms, "
          f"{constrained_pairs} state-variable constraint pairs")

    model.diagnostics.extend(all_diagnostics)
    return all_diagnostics


def _integrate_vlm_guards(model: ProtocolModel, vlm_results: dict) -> None:
    """
    Integrate VLM-extracted guards and sequence constraints into transitions.

    VLM results contain guards like:
      {"expr": "ResponseCode = OK", "actor": "EVCC", "applies_to_messages": [...], "source_req": "..."}
    Sequence constraints like:
      {"condition": "...", "current_message": "AuthorizationRes", "next_allowed": ["ServiceDiscoveryReq"], ...}
    """
    # Build message → state mapping
    msg_to_state = {}
    for state in model.states:
        if state.allowed_request:
            msg_to_state[state.allowed_request] = state.name
        if state.allowed_response:
            msg_to_state[state.allowed_response] = state.name

    # Process VLM guards
    for guard_data in vlm_results.get("guards", []):
        expr = guard_data.get("expr", "")
        if not expr:
            continue

        actor_str = guard_data.get("actor", "BOTH")
        actor = Role.BOTH
        if actor_str == "EVCC":
            actor = Role.EVCC
        elif actor_str == "SECC":
            actor = Role.SECC

        applies_to = guard_data.get("applies_to_messages", [])

        atom = Atom(
            kind=AtomKind.GUARD,
            actor=actor,
            scope=AtomScope.TRANSITION,
            expr=expr,
            source_req=guard_data.get("source_req", ""),
            confidence=0.7,
            guard_status=GuardStatus.KNOWN,
            iso_variables=_extract_iso_vars(expr),
            applies_to_messages=applies_to,
            notes="vlm_extracted",
        )

        # Find matching transitions
        for msg in applies_to:
            state_name = msg_to_state.get(msg, "")
            if state_name:
                for trans in model.get_transitions_from(state_name):
                    # Avoid duplicates
                    if not any(g.expr == expr for g in trans.guards):
                        trans.guards.append(atom)

    # Process VLM sequence constraints
    for sc in vlm_results.get("sequence_constraints", []):
        current_msg = sc.get("current_message", "")
        next_allowed = sc.get("next_allowed", [])
        condition = sc.get("condition", "")

        if not current_msg or not next_allowed:
            continue

        state_name = msg_to_state.get(current_msg, "")
        if not state_name:
            continue

        for next_msg in next_allowed:
            atom = Atom(
                kind=AtomKind.SEQUENCE_CONSTRAINT,
                actor=Role.EVCC,
                scope=AtomScope.STATE,
                expr=f"next_allowed = {next_msg}",
                source_req=sc.get("source_req", ""),
                confidence=0.7,
                iso_variables=[next_msg],
                applies_to_messages=[next_msg],
                notes=f"condition: {condition}" if condition else "vlm_extracted",
            )

            for trans in model.get_transitions_from(state_name):
                if not any(s.expr == atom.expr for s in trans.sequence_constraints):
                    trans.sequence_constraints.append(atom)


def _extract_iso_vars(expr: str) -> list[str]:
    """Extract ISO variable names from an expression like 'ResponseCode = OK'."""
    m = re.match(r'(\w+)\s*=', expr)
    return [m.group(1)] if m else []
