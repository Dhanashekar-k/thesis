"""
models.py — Core data models for the AC protocol formal verification pipeline.

Schema overview:

  Provenance          — where something came from in the spec
  AtomKind / Scope    — classification enums for requirement atoms
  Atom                — a single normalized obligation extracted from spec text
  RequirementRecord   — a V2G20-XXXX with source info + list of decomposed atoms
  FieldDef            — a message field from a spec table
  MessageSchema       — request/response message structure
  TimerSpec           — a named timer with its bound
  ProtocolState       — a state in the protocol FSM
  ProtocolTransition  — a transition with attached atoms
  ActorLocalState     — actor-specific (EVCC/SECC) control substates
  ProtocolModel       — the complete enriched protocol model
  PropertySpec        — a formal property (CTL/LTL) to verify
  DiagnosticItem      — a validation warning or ambiguity
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any


# ═══════════════════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════════════════

class AtomKind(Enum):
    """Classification of a normalized obligation atom."""
    GUARD              = "guard"               # precondition for a transition
    ACTION             = "action"              # what must happen (send message, set field)
    TIMING             = "timing"              # timer / deadline constraint
    FIELD_CONSTRAINT   = "field_constraint"    # message field rule (type, M/O, value domain)
    SEQUENCE_CONSTRAINT= "sequence_constraint" # allowed next message / message order rule
    INVARIANT          = "invariant"           # must hold globally or in a state
    ASSUMPTION         = "assumption"          # environment assumption


class AtomScope(Enum):
    """Where does this atom apply?"""
    TRANSITION = "transition"
    STATE      = "state"
    MESSAGE    = "message"
    SESSION    = "session"
    GLOBAL     = "global"


class Role(Enum):
    EVCC = "EVCC"
    SECC = "SECC"
    BOTH = "BOTH"


class GuardStatus(Enum):
    """Confidence level for extracted guard conditions."""
    KNOWN   = "known"    # fully parsed with high confidence
    PARTIAL = "partial"  # some fields extracted but ambiguous parts remain
    UNKNOWN = "unknown"  # requirement referenced but guard not extractable


class Cardinality(Enum):
    """Message field mandatory/optional classification."""
    MANDATORY = "M"
    OPTIONAL  = "O"
    CONDITIONAL = "C"


# ═══════════════════════════════════════════════════════════════════════════
# Provenance — where something came from in the spec
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Provenance:
    """Tracks exactly where a piece of information was extracted from."""
    clause_id:    Optional[str] = None    # e.g. "8.6.4.5.3.2"
    page_span:    list[int] = field(default_factory=list)  # [419, 420]
    table_id:     Optional[str] = None    # e.g. "Table 215"
    figure_id:    Optional[str] = None    # e.g. "Figure 215"
    row_index:    Optional[int] = None    # row within a table
    source_text:  Optional[str] = None    # the text span
    image_path:   Optional[str] = None    # cropped figure image
    bbox:         Optional[tuple[int,int,int,int]] = None  # image region
    extraction_method: str = "unknown"    # "regex", "llm", "vlm", "table_parse", "manual"


# ═══════════════════════════════════════════════════════════════════════════
# Atoms — normalized obligations extracted from requirements
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Atom:
    """
    A single normalized obligation extracted from a V2G20-XXXX requirement.

    One requirement may decompose into multiple atoms.  Each atom has:
    - kind: what type of obligation (guard, action, timing, etc.)
    - actor: who must satisfy it (EVCC, SECC, BOTH)
    - scope + binding: where it applies
    - expr: the normalized formal expression
    - confidence: how reliable the extraction is (0.0–1.0)
    - provenance: source in the spec
    """
    kind:       AtomKind
    actor:      Role
    scope:      AtomScope
    expr:       str                # normalized formal expression

    # Binding: where this atom applies
    applies_to_transitions: list[int] = field(default_factory=list)
    applies_to_states:      list[str] = field(default_factory=list)
    applies_to_messages:    list[str] = field(default_factory=list)

    # Metadata
    source_req:     str   = ""         # V2G20-XXXX that produced this
    confidence:     float = 0.0
    guard_status:   GuardStatus = GuardStatus.UNKNOWN
    iso_variables:  list[str] = field(default_factory=list)  # ISO names referenced
    notes:          str   = ""
    provenance:     Optional[Provenance] = None

    def to_dict(self) -> dict:
        return {
            "kind": self.kind.value,
            "actor": self.actor.value,
            "scope": self.scope.value,
            "expr": self.expr,
            "applies_to_transitions": self.applies_to_transitions,
            "applies_to_states": self.applies_to_states,
            "applies_to_messages": self.applies_to_messages,
            "source_req": self.source_req,
            "confidence": self.confidence,
            "guard_status": self.guard_status.value,
            "iso_variables": self.iso_variables,
            "notes": self.notes,
        }


# ═══════════════════════════════════════════════════════════════════════════
# RequirementRecord — a V2G20-XXXX with decomposed atoms
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RequirementRecord:
    """
    A single normative requirement from the ISO spec.

    The key change from the old model: a requirement decomposes into
    multiple atoms, each with its own kind/scope/binding.
    """
    req_id:     str                         # "V2G20-1437"
    text:       str                         # full original text
    source:     Provenance
    atoms:      list[Atom] = field(default_factory=list)
    confidence: float      = 0.0           # overall confidence
    notes:      str        = ""

    def to_dict(self) -> dict:
        return {
            "req_id": self.req_id,
            "text": self.text,
            "source": {
                "clause": self.source.clause_id,
                "page_span": self.source.page_span,
                "table_id": self.source.table_id,
                "figure_id": self.source.figure_id,
            },
            "atoms": [a.to_dict() for a in self.atoms],
            "confidence": self.confidence,
            "notes": self.notes,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Message schema — field definitions from spec tables
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class FieldDef:
    """A single field within a message, from a spec table row."""
    name:         str                        # ISO name: "ResponseCode"
    field_type:   str                        # "simpleType:responseCodeType"
    cardinality:  Cardinality = Cardinality.MANDATORY
    semantics:    str = ""                   # description from table
    value_domain: list[str] = field(default_factory=list)  # allowed values
    provenance:   Optional[Provenance] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.field_type,
            "cardinality": self.cardinality.value,
            "semantics": self.semantics,
            "value_domain": self.value_domain,
        }


@dataclass
class MessageSchema:
    """
    A request or response message definition extracted from spec tables.

    Example: AC_ChargeLoopReq has fields like Header, EVProcessing,
    CLReqControlMode, etc.
    """
    message_name: str                        # "AC_ChargeLoopReq"
    direction:    str = "request"             # "request" or "response"
    fields:       list[FieldDef] = field(default_factory=list)
    provenance:   Optional[Provenance] = None

    def get_field(self, name: str) -> Optional[FieldDef]:
        for f in self.fields:
            if f.name == name:
                return f
        return None

    def to_dict(self) -> dict:
        return {
            "message_name": self.message_name,
            "direction": self.direction,
            "fields": [f.to_dict() for f in self.fields],
        }


# ═══════════════════════════════════════════════════════════════════════════
# Timers — timing constraints from spec tables and text
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TimerSpec:
    """A named timer with its value and applicability."""
    name:          str              # "V2G_EVCC_Msg_Timeout"
    message_type:  str = ""         # which message it applies to
    value_seconds: float = 0.0     # timeout value
    applicable_to: Role = Role.BOTH
    provenance:    Optional[Provenance] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "message_type": self.message_type,
            "value_seconds": self.value_seconds,
            "applicable_to": self.applicable_to.value,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Protocol FSM elements
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ProtocolState:
    """
    A state in the protocol, with actor-local semantics.

    Unlike the old model which only had high-level FSM states, this
    also tracks what each actor does within the state.
    """
    name:            str                     # "AC_ChargeParameterDiscovery"
    state_id:        str = ""                # "ST9"
    phase:           str = ""                # "setup" | "auth" | "service" | "charging" | "stopping"
    is_ac_specific:  bool = False
    is_common:       bool = True
    allowed_request: str = ""                # message sent in this state
    allowed_response:str = ""                # response expected
    invariants:      list[Atom] = field(default_factory=list)
    provenance:      Optional[Provenance] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "state_id": self.state_id,
            "phase": self.phase,
            "is_ac_specific": self.is_ac_specific,
            "allowed_request": self.allowed_request,
            "allowed_response": self.allowed_response,
        }


@dataclass
class ProtocolTransition:
    """
    A transition in the protocol FSM, enriched with atoms.

    Each transition carries:
    - guard atoms (preconditions)
    - action atoms (what happens)
    - timing atoms (deadline constraints)
    - field constraint atoms
    - sequence constraint atoms
    - unresolved items
    """
    id:              int
    from_state:      str
    to_state:        str
    trigger_message: str = ""                 # request/response that triggers this

    # Atoms by kind (attached during enrichment)
    guards:              list[Atom] = field(default_factory=list)
    actions:             list[Atom] = field(default_factory=list)
    timing_constraints:  list[Atom] = field(default_factory=list)
    field_constraints:   list[Atom] = field(default_factory=list)
    sequence_constraints:list[Atom] = field(default_factory=list)
    invariants:          list[Atom] = field(default_factory=list)

    # Unresolved
    unresolved_items:    list[Atom] = field(default_factory=list)

    # Source requirement refs
    evcc_refs: list[str] = field(default_factory=list)
    secc_refs: list[str] = field(default_factory=list)

    # Metadata
    is_self_loop:    bool = False
    is_error_exit:   bool = False
    guard_status:    GuardStatus = GuardStatus.UNKNOWN
    description:     str = ""
    provenance:      Optional[Provenance] = None

    @property
    def all_atoms(self) -> list[Atom]:
        return (self.guards + self.actions + self.timing_constraints +
                self.field_constraints + self.sequence_constraints +
                self.invariants + self.unresolved_items)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from": self.from_state,
            "to": self.to_state,
            "trigger_message": self.trigger_message,
            "guards": [a.to_dict() for a in self.guards],
            "actions": [a.to_dict() for a in self.actions],
            "timing_constraints": [a.to_dict() for a in self.timing_constraints],
            "field_constraints": [a.to_dict() for a in self.field_constraints],
            "sequence_constraints": [a.to_dict() for a in self.sequence_constraints],
            "invariants": [a.to_dict() for a in self.invariants],
            "unresolved_items": [a.to_dict() for a in self.unresolved_items],
            "evcc_refs": self.evcc_refs,
            "secc_refs": self.secc_refs,
            "is_self_loop": self.is_self_loop,
            "is_error_exit": self.is_error_exit,
            "guard_status": self.guard_status.value,
            "description": self.description,
        }


# ═══════════════════════════════════════════════════════════════════════════
# NuSMV variable descriptor
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class NuSMVVar:
    """
    A variable in the NuSMV model, preserving ISO naming.
    """
    iso_name:       str                      # "ResponseCode" (as in spec)
    smv_name:       str                      # "ResponseCode" (same if valid)
    domain:         list[str]                # enum values or ["boolean"]
    init_value:     str                      # initial value
    description:    str = ""
    constrained_by: list[str] = field(default_factory=list)  # states where domain is restricted
    source_reqs:    list[str] = field(default_factory=list)   # V2G20 refs

    def to_dict(self) -> dict:
        return {
            "iso_name": self.iso_name,
            "smv_name": self.smv_name,
            "domain": self.domain,
            "init_value": self.init_value,
            "description": self.description,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Actor-local state
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ActorLocalState:
    """
    Actor-specific control states for EVCC or SECC.

    The protocol is not lock-step at the wire level.  Each actor has:
    - a control state (idle, send_req, wait_res, process, send_res, etc.)
    - retry counters
    - timer state
    """
    actor:          Role
    control_states: list[str] = field(default_factory=list)
    init_state:     str = ""


# ═══════════════════════════════════════════════════════════════════════════
# The complete protocol model
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ProtocolModel:
    """
    The complete AC protocol model, ready for NuSMV code generation.

    This is the central artifact produced by the pipeline.
    """
    # Identity
    model_id:    str = "iso15118_20_ac"
    title:       str = "ISO 15118-20 AC Charging Protocol Model"

    # Protocol FSM
    states:      list[ProtocolState] = field(default_factory=list)
    transitions: list[ProtocolTransition] = field(default_factory=list)
    entry_state: str = ""
    exit_state:  str = ""

    # Actor-local models
    evcc_local:  Optional[ActorLocalState] = None
    secc_local:  Optional[ActorLocalState] = None

    # Message schemas
    messages:    list[MessageSchema] = field(default_factory=list)

    # Timers
    timers:      list[TimerSpec] = field(default_factory=list)

    # Variables for NuSMV
    variables:   list[NuSMVVar] = field(default_factory=list)

    # All requirement records
    requirements: dict[str, RequirementRecord] = field(default_factory=dict)

    # Global / session-level atoms (not bound to specific transitions)
    session_atoms: list[Atom] = field(default_factory=list)
    global_atoms:  list[Atom] = field(default_factory=list)

    # Diagnostics
    diagnostics: list[Any] = field(default_factory=list)

    def get_state(self, name: str) -> Optional[ProtocolState]:
        for s in self.states:
            if s.name == name:
                return s
        return None

    def get_message(self, name: str) -> Optional[MessageSchema]:
        for m in self.messages:
            if m.message_name == name:
                return m
        return None

    def get_transitions_from(self, state: str) -> list[ProtocolTransition]:
        return [t for t in self.transitions if t.from_state == state]

    def get_transitions_to(self, state: str) -> list[ProtocolTransition]:
        return [t for t in self.transitions if t.to_state == state]

    def state_names(self) -> list[str]:
        return [s.name for s in self.states]

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id,
            "title": self.title,
            "states": [s.to_dict() for s in self.states],
            "transitions": [t.to_dict() for t in self.transitions],
            "entry_state": self.entry_state,
            "exit_state": self.exit_state,
            "messages": [m.to_dict() for m in self.messages],
            "timers": [t.to_dict() for t in self.timers],
            "variables": [v.to_dict() for v in self.variables],
            "requirements": {k: v.to_dict() for k, v in self.requirements.items()},
            "session_atoms": [a.to_dict() for a in self.session_atoms],
            "global_atoms": [a.to_dict() for a in self.global_atoms],
            "stats": {
                "total_states": len(self.states),
                "total_transitions": len(self.transitions),
                "total_messages": len(self.messages),
                "total_timers": len(self.timers),
                "total_variables": len(self.variables),
                "total_requirements": len(self.requirements),
                "total_atoms": sum(
                    len(r.atoms) for r in self.requirements.values()
                ),
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# Property specifications
# ═══════════════════════════════════════════════════════════════════════════

class PropertyCategory(Enum):
    SAFETY     = "safety"
    LIVENESS   = "liveness"
    COMPLIANCE = "compliance"
    INVARIANT  = "invariant"
    SEQUENCING = "sequencing"
    TIMING     = "timing"


@dataclass
class PropertySpec:
    """
    A formal property (CTL/LTL) to verify against the protocol model.
    """
    name:        str                          # short identifier
    category:    PropertyCategory
    formula:     str                          # NuSMV CTL/LTL formula
    description: str                          # human-readable explanation
    source_reqs: list[str] = field(default_factory=list)  # V2G20 refs
    uses_monitor: bool = False                # needs auxiliary/history variable
    monitor_var: str = ""                     # if uses_monitor, the variable name
    provenance:  Optional[Provenance] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category.value,
            "formula": self.formula,
            "description": self.description,
            "source_reqs": self.source_reqs,
            "uses_monitor": self.uses_monitor,
            "monitor_var": self.monitor_var,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Diagnostics
# ═══════════════════════════════════════════════════════════════════════════

class DiagnosticSeverity(Enum):
    INFO    = "info"
    WARNING = "warning"
    ERROR   = "error"


@dataclass
class DiagnosticItem:
    """A validation warning, ambiguity, or error in the pipeline."""
    severity:    DiagnosticSeverity
    stage:       str                          # which pipeline stage
    message:     str
    context:     str = ""                     # additional context
    related_req: str = ""                     # V2G20-XXXX if applicable
    related_state: str = ""
    related_transition: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "severity": self.severity.value,
            "stage": self.stage,
            "message": self.message,
            "context": self.context,
            "related_req": self.related_req,
        }
