"""
validator.py — Stage 4b: Validate the enriched protocol model.

Checks for:
  1. Transitions with no guards (UNKNOWN guard status)
  2. Duplicate / contradictory atoms on same transition
  3. Missing message schemas for states with allowed_request/response
  4. Variable domain completeness
  5. Unreachable states or dead-end states
  6. Self-loop transitions without distinguishing guards
"""

from __future__ import annotations

from collections import Counter

from models import (
    AtomKind, DiagnosticItem, DiagnosticSeverity, GuardStatus,
    ProtocolModel,
)
from config import PipelineConfig


def validate_model(model: ProtocolModel, config: PipelineConfig) -> list[DiagnosticItem]:
    """Run all validation checks on the enriched model."""
    diagnostics = []

    diagnostics.extend(_check_guardless_transitions(model))
    diagnostics.extend(_check_duplicate_atoms(model))
    diagnostics.extend(_check_missing_schemas(model))
    diagnostics.extend(_check_reachability(model))
    diagnostics.extend(_check_self_loops(model))
    diagnostics.extend(_check_exit_path(model))
    diagnostics.extend(_check_junk_variables(model))
    diagnostics.extend(_check_true_guards(model))
    diagnostics.extend(_check_missing_required_fields(model))
    diagnostics.extend(_check_unbound_response_codes(model))
    diagnostics.extend(_check_no_value_timers(model))
    diagnostics.extend(_check_coverage_gaps(model))

    errors = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.ERROR)
    warnings = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.WARNING)
    print(f"[validator] {errors} errors, {warnings} warnings, "
          f"{len(diagnostics) - errors - warnings} info")

    model.diagnostics.extend(diagnostics)
    return diagnostics


def _check_guardless_transitions(model: ProtocolModel) -> list[DiagnosticItem]:
    """Flag transitions with no guards (besides entry/self-loops)."""
    diags = []
    for t in model.transitions:
        if t.guard_status == GuardStatus.UNKNOWN and not t.guards:
            # Entry transition is OK without guards
            if t.from_state == model.entry_state and t.id == 1:
                continue
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.WARNING,
                stage="validator",
                message=f"Transition {t.id} ({t.from_state} → {t.to_state}) "
                        f"has no extracted guards",
                related_transition=t.id,
            ))
    return diags


def _check_duplicate_atoms(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check for duplicate atoms on the same transition."""
    diags = []
    for t in model.transitions:
        exprs = Counter(a.expr for a in t.guards)
        for expr, count in exprs.items():
            if count > 1:
                diags.append(DiagnosticItem(
                    severity=DiagnosticSeverity.INFO,
                    stage="validator",
                    message=f"Transition {t.id}: guard '{expr}' appears {count} times",
                    related_transition=t.id,
                ))
    return diags


def _check_missing_schemas(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check that each state's messages have corresponding schemas."""
    diags = []
    schema_names = {m.message_name for m in model.messages}

    for state in model.states:
        for msg in [state.allowed_request, state.allowed_response]:
            if msg and msg not in schema_names:
                diags.append(DiagnosticItem(
                    severity=DiagnosticSeverity.INFO,
                    stage="validator",
                    message=f"No schema found for message '{msg}' "
                            f"(used in state {state.name})",
                    related_state=state.name,
                ))
    return diags


def _check_reachability(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check for unreachable or dead-end states."""
    diags = []
    reachable = set()
    has_outgoing = set()

    for t in model.transitions:
        reachable.add(t.to_state)
        has_outgoing.add(t.from_state)

    # Entry state is always reachable
    reachable.add(model.entry_state)

    for state in model.states:
        if state.name not in reachable:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.ERROR,
                stage="validator",
                message=f"State '{state.name}' is unreachable",
                related_state=state.name,
            ))
        if state.name not in has_outgoing and state.name != model.exit_state:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.WARNING,
                stage="validator",
                message=f"State '{state.name}' has no outgoing transitions "
                        f"(dead-end, not exit state)",
                related_state=state.name,
            ))

    return diags


def _check_self_loops(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check that self-loop transitions have distinguishing guards."""
    diags = []
    for t in model.transitions:
        if t.is_self_loop and not t.guards:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.WARNING,
                stage="validator",
                message=f"Self-loop transition {t.id} on '{t.from_state}' "
                        f"has no guards to distinguish it from exit transitions",
                related_transition=t.id,
                related_state=t.from_state,
            ))
    return diags


def _check_exit_path(model: ProtocolModel) -> list[DiagnosticItem]:
    """Verify there's a path from entry to exit state."""
    diags = []
    # Simple BFS
    adj: dict[str, set[str]] = {}
    for t in model.transitions:
        adj.setdefault(t.from_state, set()).add(t.to_state)

    visited = set()
    queue = [model.entry_state]
    while queue:
        s = queue.pop(0)
        if s in visited:
            continue
        visited.add(s)
        for n in adj.get(s, set()):
            if n not in visited:
                queue.append(n)

    if model.exit_state and model.exit_state not in visited:
        diags.append(DiagnosticItem(
            severity=DiagnosticSeverity.ERROR,
            stage="validator",
            message=f"No path from entry '{model.entry_state}' "
                    f"to exit '{model.exit_state}'",
        ))

    return diags


def _check_junk_variables(model: ProtocolModel) -> list[DiagnosticItem]:
    """Flag variables with domain size <= 1 (junk, provide no information)."""
    diags = []
    for var in model.variables:
        if var.domain != ["boolean"] and len(var.domain) <= 1:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.WARNING,
                stage="validator",
                message=f"Variable '{var.iso_name}' has domain size {len(var.domain)} "
                        f"({var.domain}) — provides no discrimination",
                related_state="",
            ))
    return diags


def _check_true_guards(model: ProtocolModel) -> list[DiagnosticItem]:
    """Flag transitions that will get unconstrained TRUE guards in NuSMV."""
    diags = []
    for t in model.transitions:
        # Skip entry transition (T1 is typically the entry)
        if t.from_state == model.entry_state and t.id <= 1:
            continue
        if not t.guards and t.guard_status == GuardStatus.UNKNOWN:
            # Check if this transition has outgoing siblings that DO have guards
            siblings = [
                t2 for t2 in model.transitions
                if t2.from_state == t.from_state and t2.id != t.id and t2.guards
            ]
            if siblings:
                diags.append(DiagnosticItem(
                    severity=DiagnosticSeverity.WARNING,
                    stage="validator",
                    message=f"Transition {t.id} ({t.from_state} → {t.to_state}) "
                            f"will get TRUE guard in NuSMV — {len(siblings)} siblings "
                            f"have proper guards",
                    related_transition=t.id,
                ))
    return diags


def _check_missing_required_fields(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check that mandatory schema fields have known domains."""
    diags = []
    for schema in model.messages:
        for field in schema.fields:
            if field.cardinality.value == "mandatory" and not field.field_type:
                diags.append(DiagnosticItem(
                    severity=DiagnosticSeverity.INFO,
                    stage="validator",
                    message=f"Mandatory field '{field.name}' in {schema.message_name} "
                            f"has no type specified",
                ))
    return diags


def _check_unbound_response_codes(model: ProtocolModel) -> list[DiagnosticItem]:
    """Check for states whose response messages lack response code sets."""
    diags = []
    response_codes = getattr(model, 'response_codes', {})
    for state in model.states:
        if state.allowed_response and state.allowed_response not in response_codes:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.INFO,
                stage="validator",
                message=f"No response code set found for '{state.allowed_response}' "
                        f"in state {state.name}",
                related_state=state.name,
            ))
    return diags


def _check_no_value_timers(model: ProtocolModel) -> list[DiagnosticItem]:
    """Flag timers that have no value (0.0 seconds)."""
    diags = []
    for timer in model.timers:
        if timer.value_seconds == 0.0:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.WARNING,
                stage="validator",
                message=f"Timer '{timer.name}' has no value (0.0s) — "
                        f"extracted from {timer.provenance.extraction_method if timer.provenance else 'unknown'}",
            ))
    return diags


def _check_coverage_gaps(model: ProtocolModel) -> list[DiagnosticItem]:
    """Report coverage gaps: states with no atoms bound at all."""
    diags = []
    for state in model.states:
        outgoing = [t for t in model.transitions if t.from_state == state.name]
        total_atoms = sum(len(t.all_atoms) for t in outgoing)
        if total_atoms == 0 and state.name != model.entry_state:
            diags.append(DiagnosticItem(
                severity=DiagnosticSeverity.INFO,
                stage="validator",
                message=f"State '{state.name}' has no atoms bound to any "
                        f"of its {len(outgoing)} outgoing transitions — coverage gap",
                related_state=state.name,
            ))
    return diags
