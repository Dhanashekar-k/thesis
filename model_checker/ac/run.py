"""
run.py — Pipeline orchestrator for the AC protocol model checker v3.

Architecture:
  - Process EVERYTHING first, filter AFTER extraction
  - .md for semantic content, JSON for structural metadata
  - Section-by-section processing (not page-by-page)
  - Stage caching: each stage saves results, skips if cache exists
  - VLM extracts ALL semantics; AC filtering is post-extraction

Stages:
  1. Load inputs        (FSM JSON, knowledge base)
  2. Process sections   (all sections → SectionChunks with .md + JSON)
  3. VLM extraction     (SectionChunks → structured protocol semantics)
  4. AC relevance filter(post-extraction classification)
  5. Requirement decomp (regex + LLM decomposition of V2G20 requirements)
  6. Table analysis     (regex-based schema/timer/response code extraction)
  7. Build protocol     (fuse all → ProtocolModel)
  8. Enrich             (bind atoms, constrain variables)
  9. Validate           (consistency checks)
 10. NuSMV model        (generate .smv)
 11. NuSMV properties   (generate CTL/LTL)
 12. Write outputs

Usage:
    python run.py --use-vlm              # full pipeline with VLM
    python run.py                        # regex-only (no VLM calls)
    python run.py --use-vlm --no-cache   # force re-run all stages
    python run.py --from-stage 4         # resume from stage 4
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import PipelineConfig
from llm_client import create_client, MockInferenceClient
from models import ProtocolModel
from normalization import reset_normalization_log, get_normalization_log, normalize_req_id_bare


# ═══════════════════════════════════════════════════════════════════════════
# Stage cache helpers
# ═══════════════════════════════════════════════════════════════════════════

def _cache_dir(config: PipelineConfig) -> Path:
    d = config.resolve_path(config.cache_dir)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _save_stage(config: PipelineConfig, name: str, data) -> None:
    """Save stage output to cache."""
    path = _cache_dir(config) / f"{name}.json"
    # Handle different data types
    if hasattr(data, 'to_dict'):
        serializable = data.to_dict()
    elif isinstance(data, list) and data and hasattr(data[0], 'to_dict'):
        serializable = [d.to_dict() for d in data]
    elif isinstance(data, dict):
        serializable = _make_serializable(data)
    else:
        serializable = data
    path.write_text(json.dumps(serializable, indent=2, ensure_ascii=False, default=str))
    print(f"  Cache saved: {path}")


def _load_stage(config: PipelineConfig, name: str):
    """Load stage output from cache. Returns None if not found."""
    path = _cache_dir(config) / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


def _stage_cached(config: PipelineConfig, name: str) -> bool:
    """Check if a stage has cached output."""
    return (_cache_dir(config) / f"{name}.json").exists()


def _make_serializable(obj):
    """Recursively make an object JSON-serializable."""
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_serializable(v) for v in obj]
    elif isinstance(obj, set):
        return sorted(list(obj))
    elif hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return obj


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════
# Pipeline
# ═══════════════════════════════════════════════════════════════════════════

def run_pipeline(config: PipelineConfig, no_cache: bool = False,
                 from_stage: int = 1) -> ProtocolModel:
    """Execute the full pipeline and return the enriched model."""
    out_dir = Path(__file__).parent
    use_cache = not no_cache

    # Reset normalization log for this run
    reset_normalization_log()

    def should_run(stage_num: int, name: str) -> bool:
        if stage_num < from_stage:
            return False
        if use_cache and _stage_cached(config, name):
            print(f"  (cached, skipping)")
            return False
        return True

    # ══════════════════════════════════════════════════════════════════
    # Stage 1: Load inputs
    # ══════════════════════════════════════════════════════════════════
    print("═══ Stage 1: Load inputs ═══")

    fsm_path = config.resolve_path(config.fsm_path)
    kb_path = config.resolve_path(config.kb_path)

    fsm_data = load_json(fsm_path)
    print(f"  FSM: {len(fsm_data.get('states', []))} states, "
          f"{len(fsm_data.get('transitions', []))} transitions")

    kb_data = load_json(kb_path)
    sections = kb_data.get("sections", [])
    requirements_kb = kb_data.get("requirements", {})
    figures_kb = kb_data.get("figures", [])
    print(f"  KB: {len(requirements_kb)} requirements, "
          f"{len(sections)} sections, {len(figures_kb)} figures")

    # Build AC backbone from FSM (needed for post-extraction filtering)
    from ac_relevance import build_ac_backbone
    backbone = build_ac_backbone(fsm_data)
    print(f"  AC backbone: {len(backbone.ac_states)} states, "
          f"{len(backbone.ac_messages)} messages, "
          f"{len(backbone.fsm_req_ids)} FSM req refs")

    # ══════════════════════════════════════════════════════════════════
    # Stage 2: Process ALL sections
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 2: Process all sections ═══")

    section_chunks = None
    if should_run(2, "stage2_sections"):
        from section_processor import process_all_sections

        ocr_base = config.resolve_path(config.ocr_base_dir)
        section_chunks = process_all_sections(
            kb_data, ocr_base,
            excluded_pages=config.excluded_pages,
        )

        # Save section metadata (not the full text, just structure)
        _save_stage(config, "stage2_sections",
                    [c.to_dict() for c in section_chunks])

        # Log per-section stats
        non_empty = [c for c in section_chunks if c.merged_text.strip()]
        with_tables = [c for c in section_chunks if c.tables]
        with_images = [c for c in section_chunks if c.images]
        total_reqs = sum(len(c.requirement_ids) for c in section_chunks)
        print(f"  Non-empty sections: {len(non_empty)}/{len(section_chunks)}")
        print(f"  Sections with tables: {len(with_tables)}")
        print(f"  Sections with images: {len(with_images)}")
        print(f"  Total requirement refs: {total_reqs}")
    else:
        # Need to re-process since we can't serialize SectionChunks fully
        from section_processor import process_all_sections
        ocr_base = config.resolve_path(config.ocr_base_dir)
        section_chunks = process_all_sections(
            kb_data, ocr_base,
            excluded_pages=config.excluded_pages,
        )

    # ══════════════════════════════════════════════════════════════════
    # Stage 3: VLM multimodal extraction (ALL sections)
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 3: VLM multimodal extraction ═══")

    vlm_results = None
    vlm_client = None

    if config.use_vlm:
        if should_run(3, "stage3_vlm_extraction"):
            from multimodal_extractor import extract_all_sections

            print(f"  Creating VLM client: {config.vlm.model_name} @ {config.vlm.base_url}")
            vlm_client = create_client(config.vlm, enabled=True)

            t0 = time.time()
            vlm_results = extract_all_sections(section_chunks, vlm_client)
            elapsed = time.time() - t0

            _save_stage(config, "stage3_vlm_extraction", vlm_results)
            n_items = sum(len(v) for v in vlm_results.values() if isinstance(v, list))
            print(f"  VLM extracted {n_items} items in {elapsed:.1f}s")
        else:
            vlm_results = _load_stage(config, "stage3_vlm_extraction")
            if vlm_results:
                n_items = sum(len(v) for v in vlm_results.values() if isinstance(v, list))
                print(f"  Loaded {n_items} cached VLM items")
    else:
        print("  (VLM disabled, skipping)")

    # ══════════════════════════════════════════════════════════════════
    # Stage 4: AC relevance filtering (POST-extraction)
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 4: AC relevance filtering ═══")

    ac_results = vlm_results  # default: pass through if no VLM
    filter_log_data = None
    if vlm_results:
        if should_run(4, "stage4_ac_filtered"):
            from ac_relevance import filter_extraction_results

            ac_results, filter_log_data = filter_extraction_results(vlm_results, backbone)

            _save_stage(config, "stage4_ac_filtered", ac_results)
            _save_stage(config, "stage4_filter_log", filter_log_data)

            # Print filter summary
            for cat, stats in filter_log_data.items():
                if stats["total"] > 0:
                    print(f"  {cat}: {stats['kept']}/{stats['total']} kept, "
                          f"{stats['discarded']} discarded")
        else:
            ac_results = _load_stage(config, "stage4_ac_filtered")
            if ac_results:
                n_items = sum(len(v) for v in ac_results.values() if isinstance(v, list))
                print(f"  Loaded {n_items} cached AC-filtered items")

    # ══════════════════════════════════════════════════════════════════
    # Stage 5: Requirement decomposition
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 5: Requirement decomposition ═══")

    requirements = None
    if should_run(5, "stage5_requirements"):
        from requirement_decomposer import decompose_all_requirements

        # Use LLM client if enabled (same server as VLM)
        llm_client = vlm_client
        if config.use_llm and not llm_client:
            llm_client = create_client(config.llm, enabled=True)

        # Target: ALL requirements from KB — FSM is anchor, not filter
        # FSM-referenced + section-found IDs get priority, but we process everything
        target_reqs = None  # None means process ALL requirements in KB
        # Log what FSM references for diagnostics
        fsm_refs = set(backbone.fsm_req_ids)
        for chunk in section_chunks:
            fsm_refs.update(chunk.requirement_ids)
        fsm_refs = {normalize_req_id_bare(r, context="stage5_target") for r in fsm_refs}
        print(f"  FSM + section refs: {len(fsm_refs)} requirement IDs (processing ALL)")

        requirements = decompose_all_requirements(
            kb_data, config,
            llm_client=llm_client,
            target_req_ids=target_reqs,  # None = process ALL KB requirements
        )

        _save_stage(config, "stage5_requirements",
                    {k: v.to_dict() for k, v in requirements.items()})
        print(f"  Decomposed {len(requirements)} requirements, "
              f"{sum(len(r.atoms) for r in requirements.values())} atoms")
    else:
        cached = _load_stage(config, "stage5_requirements")
        if cached:
            from requirement_decomposer import _rebuild_requirements
            requirements = _rebuild_requirements(cached)
            print(f"  Loaded {len(requirements)} cached requirements")
        else:
            from requirement_decomposer import decompose_all_requirements
            requirements = decompose_all_requirements(kb_data, config, target_req_ids=None)

    # ══════════════════════════════════════════════════════════════════
    # Stage 6: Table analysis (regex-based, from section chunks)
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 6: Table analysis ═══")

    schemas, timers, response_codes = [], [], {}
    if should_run(6, "stage6_tables"):
        from table_analyzer import analyze_tables_from_chunks

        schemas, timers, response_codes = analyze_tables_from_chunks(section_chunks)

        _save_stage(config, "stage6_tables", {
            "schemas": [s.to_dict() for s in schemas],
            "timers": [t.to_dict() for t in timers],
            "response_codes": response_codes,
        })
        print(f"  {len(schemas)} schemas, {len(timers)} timers, "
              f"{len(response_codes)} response code sets")
    else:
        cached = _load_stage(config, "stage6_tables")
        if cached:
            from table_analyzer import _rebuild_schemas, _rebuild_timers
            schemas = _rebuild_schemas(cached.get("schemas", []))
            timers = _rebuild_timers(cached.get("timers", []))
            response_codes = cached.get("response_codes", {})
            print(f"  Loaded {len(schemas)} schemas, {len(timers)} timers")
        else:
            from table_analyzer import analyze_tables_from_chunks
            schemas, timers, response_codes = analyze_tables_from_chunks(section_chunks)

    # ══════════════════════════════════════════════════════════════════
    # Stage 7: Build protocol model
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 7: Build protocol model ═══")

    from protocol_builder import build_protocol_model

    model = build_protocol_model(
        fsm_data, kb_data, requirements,
        schemas, timers, response_codes, config,
        vlm_results=ac_results,
    )

    # ══════════════════════════════════════════════════════════════════
    # Stage 8: Enrich model
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 8: Enrich model ═══")

    from enrichment import enrich_model

    diagnostics = enrich_model(model, config, vlm_results=ac_results)

    # ══════════════════════════════════════════════════════════════════
    # Stage 9: Validate model
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 9: Validate model ═══")

    from validator import validate_model

    val_diagnostics = validate_model(model, config)

    # ══════════════════════════════════════════════════════════════════
    # Stage 10: Generate NuSMV model
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 10: Generate NuSMV model ═══")

    from nusmv_model import generate_smv_model

    smv_model = generate_smv_model(model, config)
    smv_path = out_dir / config.output_smv
    smv_path.write_text(smv_model)
    print(f"  Written: {smv_path} ({len(smv_model.splitlines())} lines)")

    # ══════════════════════════════════════════════════════════════════
    # Stage 11: Generate properties
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 11: Generate properties ═══")

    from nusmv_properties import generate_properties

    properties, props_smv = generate_properties(model, config)
    props_path = out_dir / config.output_properties
    props_path.write_text(props_smv)
    print(f"  Written: {props_path} ({len(properties)} properties)")

    # ══════════════════════════════════════════════════════════════════
    # Stage 12: Write outputs
    # ══════════════════════════════════════════════════════════════════
    print("\n═══ Stage 12: Write outputs ═══")

    # Model JSON
    model_json_path = out_dir / config.output_model_json
    model_json_path.write_text(
        json.dumps(model.to_dict(), indent=2, ensure_ascii=False)
    )
    print(f"  Written: {model_json_path}")

    # Diagnostics
    all_diags = diagnostics + val_diagnostics
    diag_path = out_dir / config.output_diagnostics
    diag_path.write_text(json.dumps(
        [d.to_dict() for d in all_diags], indent=2
    ))
    print(f"  Written: {diag_path} ({len(all_diags)} items)")

    # Normalization log
    norm_log = get_normalization_log().summary()
    norm_log_path = _cache_dir(config) / "normalization_log.json"
    norm_log_path.write_text(json.dumps(norm_log, indent=2, ensure_ascii=False))
    print(f"  Written: {norm_log_path} ({norm_log['total_normalizations']} normalizations)")

    # Properties JSON
    props_json_path = out_dir / "ac_properties.json"
    props_json_path.write_text(json.dumps(
        [p.to_dict() for p in properties], indent=2
    ))
    print(f"  Written: {props_json_path}")

    # Validation log — per-section processing stats
    if section_chunks:
        val_log_path = _cache_dir(config) / "validation_log.json"
        val_log = _build_validation_log(
            section_chunks, ac_results, model,
            vlm_results=vlm_results,
            filter_log=filter_log_data,
        )
        val_log_path.write_text(json.dumps(val_log, indent=2, default=str))
        print(f"  Written: {val_log_path}")

    # Summary
    print(f"\n═══ Pipeline complete ═══")
    stats = model.to_dict().get("stats", {})
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Close clients
    if vlm_client and not isinstance(vlm_client, MockInferenceClient):
        vlm_client.close()

    return model


# ═══════════════════════════════════════════════════════════════════════════
# Validation log builder
# ═══════════════════════════════════════════════════════════════════════════

def _build_validation_log(
    section_chunks,
    ac_results: dict | None,
    model: ProtocolModel,
    vlm_results: dict | None = None,
    filter_log: dict | None = None,
) -> dict:
    """Build a comprehensive audit log covering all sections processed."""
    log = {
        "sections_processed": len(section_chunks),
        "total_pages": len(set(p for c in section_chunks for p in c.pages)),
        "total_tables": sum(len(c.tables) for c in section_chunks),
        "total_images": sum(len(c.images) for c in section_chunks),
        "total_requirements_found": len(set(
            r for c in section_chunks for r in c.requirement_ids
        )),
        "model_states": len(model.states),
        "model_transitions": len(model.transitions),
        "model_variables": len(model.variables),
        "model_timers": len(model.timers),
        "model_schemas": len(model.messages),
        "vlm_extraction": {},
        "ac_filtering": {},
        "normalization": get_normalization_log().summary(),
    }

    # VLM extraction totals (pre-filtering)
    if vlm_results:
        for cat in vlm_results:
            items = vlm_results.get(cat, [])
            if isinstance(items, list):
                log["vlm_extraction"][cat] = len(items)

    # AC filtering — before vs after with discarded items
    if filter_log:
        log["ac_filtering"] = filter_log
    elif ac_results:
        for cat in ac_results:
            items = ac_results.get(cat, [])
            if isinstance(items, list):
                log["vlm_extraction"][cat] = len(items)

    # Coverage stats
    log["coverage"] = {
        "states_with_guards": sum(
            1 for s in model.states
            if any(t.guards for t in model.transitions if t.from_state == s.name)
        ),
        "total_states": len(model.states),
        "transitions_with_guards": sum(1 for t in model.transitions if t.guards),
        "total_transitions": len(model.transitions),
        "total_atoms_bound": sum(len(t.all_atoms) for t in model.transitions),
        "total_unresolved": sum(len(t.unresolved_items) for t in model.transitions),
        "requirements_decomposed": len(model.requirements),
        "total_atoms": sum(len(r.atoms) for r in model.requirements.values()),
    }

    # Per-section log
    log["per_section"] = []
    for chunk in section_chunks:
        log["per_section"].append({
            "clause_id": chunk.clause_id,
            "title": chunk.title,
            "pages": chunk.pages,
            "text_length": len(chunk.merged_text),
            "tables": len(chunk.tables),
            "images": len(chunk.images),
            "requirement_ids": chunk.requirement_ids[:10],  # first 10
        })

    return log


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="AC Protocol Model Checker Pipeline v3"
    )
    parser.add_argument("--use-llm", action="store_true",
                        help="Enable LLM for requirement decomposition")
    parser.add_argument("--use-vlm", action="store_true",
                        help="Enable VLM for multimodal extraction")
    parser.add_argument("--no-cache", action="store_true",
                        help="Force re-run all stages, ignore cached results")
    parser.add_argument("--from-stage", type=int, default=1,
                        help="Resume pipeline from this stage number")
    parser.add_argument("--no-timing", action="store_true",
                        help="Disable timer variables in NuSMV model")
    parser.add_argument("--no-retries", action="store_true",
                        help="Disable retry counter in NuSMV model")
    parser.add_argument("--no-actor-local", action="store_true",
                        help="Disable actor-local control states")
    parser.add_argument("--strict", action="store_true",
                        help="Only use guards with high confidence")

    args = parser.parse_args()

    config = PipelineConfig(
        use_llm=args.use_llm,
        use_vlm=args.use_vlm,
        include_timing=not args.no_timing,
        include_retries=not args.no_retries,
        include_actor_local=not args.no_actor_local,
        strict_guards=args.strict,
    )

    run_pipeline(config, no_cache=args.no_cache, from_stage=args.from_stage)


if __name__ == "__main__":
    main()
