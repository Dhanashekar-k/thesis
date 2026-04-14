# LLM-Driven Security Attack Generation for ISO 15118-20 protocol

This project uses LLMs and formal methods to automatically generate security attacks against the ISO 15118-20 electric vehicle charging protocol. The pipeline has four main stages:

1. **Model Checker** — Extract protocol semantics from the specification and generate a formal NuSMV model *(done)*
2. **CVE Digest** — *(TODO)*
3. **Vector DB for ISO Spec** — *(TODO)*
4. **Agentic Security Attack Generation** — *(TODO)*

Before all stages, the ISO specification PDF is preprocessed with OCR and a knowledge base is built.

## Prerequisites

- Python 3.10+
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (for OCR preprocessing)
- [vLLM](https://github.com/vllm-project/vllm) (for serving the VLM)
- [NuSMV](https://nusmv.fbk.eu/) (for running the generated `.smv` models)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Preprocessing

### 1. OCR the ISO Specification

Extract text and structure from the ISO 15118-20 PDF using PaddleOCR:

```bash
python ocr_extract.py
```

This produces per-page JSON and Markdown files under `OCR_output_1.5/`.

### 2. Message Sequence Diagram

> **Note:** The image quality of the AC message sequence diagram in the PDF is too poor for reliable automated extraction. The FSM was **manually extracted** and placed in `message_sequence_diagram/AC_FSM.json`.

### 3. Serve the VLM

The pipeline uses **Qwen2.5-VL-72B-Instruct** as a VLM/LLM backend via an OpenAI-compatible API. Start the server with vLLM:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-VL-72B-Instruct \
    --tensor-parallel-size 8 \
    --host 127.0.0.1 \
    --port 8000 \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.8 \
    --max-model-len 8192 \
    --max-num-seqs 1 \
    --enforce-eager \
    --trust-remote-code
```

Keep this running in a separate terminal before proceeding to the stages below.

---

## Stage 1: Knowledge Base Extractor

The knowledge base pipeline (located in `model_checker/knowledge_base_extractor/`) reads the OCR outputs, parses sections, stitches multi-page tables, catalogs figures, extracts requirement IDs, and produces `knowledge_base.json`.

```bash
cd model_checker/knowledge_base_extractor
python run.py --input-dir ../../OCR_output_1.5 --output ../knowledge_base.json
```

---

## Stage 2: Model Checker

Extracts protocol semantics from the OCR'd specification and generates a formal NuSMV model via a 12-stage pipeline.

From the `model_checker/ac/` directory:

```bash
cd model_checker/ac
python run.py --use-vlm
```

**Options:**

| Flag | Description |
|---|---|
| `--use-vlm` | Enable VLM-based multimodal extraction (requires the vLLM server) |
| `--no-cache` | Force re-run all stages (ignore cached results) |
| `--from-stage N` | Resume from stage N (1–12) |

Without `--use-vlm`, the pipeline uses regex-only extraction (no VLM calls).

**The 12-stage pipeline:**

1. Load FSM JSON and knowledge base
2. Process all sections (markdown + JSON)
3. VLM multimodal extraction
4. AC relevance filtering
5. Requirement decomposition
6. Table analysis
7. Build protocol model
8. Enrichment (bind atoms, constrain variables)
9. Validation (consistency checks)
10. Generate NuSMV `.smv` model
11. Generate CTL/LTL properties
12. Write outputs

Output artifacts (`.smv` model and property files) are written to `model_checker/ac/`.

---

## Stage 3: CVE Digest

*TODO*

## Stage 4: Vector DB for ISO Spec (Multimodal Graph RAG Pipeline)

This stage builds a **hybrid multimodal Graph RAG system** over the ISO 15118-20 specification.  
The goal is to convert a large, complex, multimodal PDF (text, tables, figures) into a **retrievable structured knowledge system**.

The pipeline is divided into **4 phases**, each progressively adding structure, semantics, and retrieval capability.

---

## Phase 1: Document Canonicalization (Structure Graph)

### Goal
Convert raw OCR output into a **clean, structured, graph-based representation** of the document.

### Input
- OCR outputs (Markdown + JSON + images)
- Extracted pages, blocks, figures, tables

### What it does
- Parses document into:
  - sections
  - pages
  - text blocks
  - figures
  - tables
- Builds structural relationships:
  - section → page
  - page → blocks
  - block → next block
  - block → figure/table references

### Output
- `sections.jsonl`
- `pages.jsonl`
- `blocks.jsonl`
- `text_units.jsonl`
- `figures.jsonl`
- `tables.jsonl`
- `edges.jsonl`
- `knowledge_base.json`

### Why this phase exists
- Raw OCR is **unstructured and noisy**
- This phase creates a **deterministic, navigable document graph**
- No LLM usage -> reproducible and fast

---

## Phase 2: Semantic Enrichment (Evidence + Concept Graph)

### Goal
Convert raw document nodes into **semantic units and relationships**.

### Input
- Phase 1 outputs

### What it does
1. Creates **evidence units**:
   - text evidence
   - table evidence
   - figure evidence

2. Enriches each unit using LLM/VLM:
   - proxy description
   - classification
   - keywords
   - concepts
   - relations

3. Builds a **concept graph**:
   - concept nodes
   - semantic edges:
     - evidence → concept
     - concept → concept
     - evidence → requirement

### Output
- `evidence_units.jsonl`
- `concept_nodes.jsonl`
- `semantic_edges.jsonl`
- `manifest.json`

### Command
```bash
python phase2.py --phase1-root /path/to/phase1 --output-root /path/to/phase2 --api-base http://127.0.0.1:8000/v1 --model Qwen/Qwen2.5-VL-72B-Instruct --concurrency 4

## Stage 5: Agentic Security Attack Generation

*TODO*

Output artifacts are written to `model_checker/ac/` including the `.smv` model and property files.
