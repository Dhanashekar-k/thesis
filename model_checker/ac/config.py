"""
config.py — Pipeline configuration for the AC model checker.

Centralizes paths, LLM/VLM endpoints, mode flags, and tuning parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LLMConfig:
    """Configuration for an LLM or VLM inference endpoint (vLLM OpenAI-compatible)."""
    base_url:       str = "http://localhost:8000/v1"
    model_name:     str = "Qwen/Qwen2.5-VL-72B-Instruct"
    api_key:        str = "EMPTY"     # vLLM default
    max_tokens:     int = 4096
    temperature:    float = 0.1       # low temp for structured extraction
    timeout:        int = 120         # seconds


@dataclass
class PipelineConfig:
    """Master configuration for the full pipeline."""

    # ── Paths ─────────────────────────────────────────────────────────
    fsm_path:          str = "../../message_sequence_diagram/AC_FSM.json"
    kb_path:           str = "../knowledge_base.json"
    ocr_base_dir:      str = "../../OCR_output_1.5"
    output_smv:        str = "ac_protocol.smv"
    output_properties: str = "ac_properties.smv"
    output_model_json: str = "ac_protocol_model.json"
    output_diagnostics:str = "ac_diagnostics.json"
    cache_dir:         str = "cache"          # intermediate results stored here

    # ── LLM / VLM endpoint (single Qwen2.5-VL-72B serves both) ──────
    llm: LLMConfig = field(default_factory=lambda: LLMConfig(
        base_url="http://127.0.0.1:8000/v1",
        model_name="Qwen/Qwen2.5-VL-72B-Instruct",
        max_tokens=4096,
    ))
    vlm: LLMConfig = field(default_factory=lambda: LLMConfig(
        base_url="http://127.0.0.1:8000/v1",
        model_name="Qwen/Qwen2.5-VL-72B-Instruct",
        max_tokens=4096,
    ))

    # ── Mode flags ────────────────────────────────────────────────────
    use_llm:           bool = True    # use LLM for requirement decomposition
    use_vlm:           bool = True    # use VLM for multimodal extraction
    strict_guards:     bool = False   # strict mode: only validated guards
    include_timing:    bool = True    # include timer variables in NuSMV model
    include_retries:   bool = True    # include retry counters
    include_actor_local: bool = True  # include actor-local control states

    # ── Tuning ────────────────────────────────────────────────────────
    confidence_threshold: float = 0.5  # below this, atoms go to unresolved
    max_retry_count:      int = 3      # NuSMV retry counter bound
    timer_abstraction:    int = 5      # abstract timer ticks (0..N)

    # ── Page exclusions ───────────────────────────────────────────────
    # Pages to skip (e.g. message sequence diagrams provided separately)
    excluded_pages: list[int] = field(default_factory=lambda:
        list(range(443, 448))  # pages 443-447: AC sequence diagrams
    )

    def resolve_path(self, relative: str) -> Path:
        """Resolve a path relative to this config file's directory."""
        return Path(__file__).parent / relative
