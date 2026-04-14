from __future__ import annotations

import argparse
import gzip
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, TypedDict

import chromadb
import numpy as np
import requests
from langgraph.graph import END, START, StateGraph
from sentence_transformers import SentenceTransformer

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
WHITESPACE_RE = re.compile(r"\s+")

REFLECTION_SYSTEM_PROMPT = """You are a reflection node in a retrieval pipeline.
You are given a user query and retrieved evidence snippets.
Your job is to decide whether the retrieved context is sufficient and, if not, how to improve the next retrieval round.
Return strict JSON only.

Output schema:
{
  "sufficient": true,
  "reason": "brief explanation",
  "missing_aspects": ["..."],
  "rewritten_query": "improved next query",
  "suggested_doc_types": ["evidence", "concept", "requirement", "section"],
  "suggested_graph_hops": 1,
  "suggested_dense_k": 30,
  "suggested_bm25_k": 30,
  "suggested_top_k": 12
}

Rules:
- Base your decision only on the provided context.
- If the current results already cover the query well, keep rewritten_query close to the current query.
- If the query is too broad, narrow it to the most relevant technical/security terms.
- Prefer concrete protocol/security wording.
- Do not invent facts or claim coverage that is not present.
- suggested_doc_types can be empty if no change is needed.
- Only use these doc types: evidence, concept, requirement, section.
"""

IMAGE_GROUNDING_SYSTEM_PROMPT = """You are grounding a user-supplied image into retrieval-friendly text.
Describe only what is visually supported and useful for later document retrieval.
Focus on message flows, actors, identifiers, fields, certificates, authentication, authorization, network/protocol details, timers, state transitions, or other protocol/security-relevant elements.
Do not speculate beyond the visible content.
"""

ANSWER_SYSTEM_PROMPT = """You are answering using only the retrieved context bundle.
Write a grounded answer that summarizes what the retrieved material says.
If the context is incomplete, say so clearly.
Do not invent missing protocol facts.
"""


def norm_text(text: Any) -> str:
    return WHITESPACE_RE.sub(" ", str(text or "")).strip()



def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(norm_text(text))]



def truncate(text: str, max_chars: int) -> str:
    text = norm_text(text)
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " ... [truncated]"



def unique_keep_order(values: Iterable[str]) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for value in values:
        value = norm_text(value)
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out



def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)



def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)



def read_jsonl(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows



def read_gzip_json(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)



def safe_json_loads(text: str) -> Optional[dict]:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None
    return None



def save_graph_png(compiled_graph, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    png_bytes = compiled_graph.get_graph().draw_mermaid_png()
    output_path.write_bytes(png_bytes)
    print(f"Saved graph PNG to {output_path.resolve()}", flush=True)



def save_graph_jpg(compiled_graph, output_path: Path) -> None:
    if Image is None:
        raise RuntimeError("Pillow is required for JPG export. Install pillow first.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    png_bytes = compiled_graph.get_graph().draw_mermaid_png()
    with Image.open(BytesIO(png_bytes)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=95)
    print(f"Saved graph JPG to {output_path.resolve()}", flush=True)


@dataclass
class RetrievalDoc:
    doc_id: str
    doc_type: str
    title: str
    text: str
    payload: Dict[str, Any]


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = float(k1)
        self.b = float(b)
        self.doc_ids: List[str] = []
        self.doc_lengths: List[int] = []
        self.avgdl: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.postings: Dict[str, List[Tuple[int, int]]] = {}
        self.doc_titles: Dict[str, str] = {}
        self.doc_types: Dict[str, str] = {}

    def search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        if not self.doc_ids:
            return []
        q_tokens = tokenize(query)
        if not q_tokens:
            return []
        scores: Dict[int, float] = defaultdict(float)
        n_docs = len(self.doc_ids)
        avgdl = self.avgdl or 1.0

        for term in q_tokens:
            postings = self.postings.get(term)
            if not postings:
                continue
            df = self.doc_freqs.get(term, 0)
            idf = np.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            for doc_ix, tf in postings:
                dl = self.doc_lengths[doc_ix]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / avgdl))
                scores[doc_ix] += float(idf) * ((tf * (self.k1 + 1.0)) / denom)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            {
                "doc_id": self.doc_ids[doc_ix],
                "score": float(score),
                "title": self.doc_titles.get(self.doc_ids[doc_ix], self.doc_ids[doc_ix]),
                "doc_type": self.doc_types.get(self.doc_ids[doc_ix]),
            }
            for doc_ix, score in ranked
        ]

    @classmethod
    def from_dict(cls, payload: dict) -> "BM25Index":
        obj = cls(k1=float(payload["k1"]), b=float(payload["b"]))
        obj.doc_ids = list(payload["doc_ids"])
        obj.doc_lengths = [int(x) for x in payload["doc_lengths"]]
        obj.avgdl = float(payload["avgdl"])
        obj.doc_freqs = {str(k): int(v) for k, v in payload["doc_freqs"].items()}
        obj.postings = {str(term): [(int(doc_ix), int(tf)) for doc_ix, tf in posting] for term, posting in payload["postings"].items()}
        obj.doc_titles = {str(k): str(v) for k, v in payload.get("doc_titles", {}).items()}
        obj.doc_types = {str(k): str(v) for k, v in payload.get("doc_types", {}).items()}
        return obj


class ChromaDenseIndex:
    def __init__(self, index_root: Path, collection_name: str) -> None:
        self.index_root = index_root
        self.collection_name = collection_name
        self.chroma_path = index_root / "chroma"
        self.client = chromadb.PersistentClient(path=str(self.chroma_path))

    def get_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def search(self, query_vector: np.ndarray, top_k: int) -> List[Dict[str, Any]]:
        collection = self.get_collection()
        res = collection.query(
            query_embeddings=[query_vector.astype(np.float32).tolist()],
            n_results=top_k,
            include=["metadatas", "documents", "distances"],
        )
        ids = (res.get("ids") or [[]])[0]
        metadatas = (res.get("metadatas") or [[]])[0]
        distances = (res.get("distances") or [[]])[0]
        out: List[Dict[str, Any]] = []
        for doc_id, meta, distance in zip(ids, metadatas, distances):
            meta = meta or {}
            sim = 1.0 / (1.0 + float(distance))
            out.append(
                {
                    "doc_id": doc_id,
                    "score": float(sim),
                    "distance": float(distance),
                    "title": meta.get("title") or doc_id,
                    "doc_type": meta.get("doc_type"),
                }
            )
        return out


class TextEmbedder:
    def __init__(
        self,
        model_name: str,
        device: Optional[str],
        trust_remote_code: bool,
        batch_size: int,
        doc_prefix: str = "",
        query_prefix: str = "",
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.trust_remote_code = trust_remote_code
        self.batch_size = batch_size
        self.doc_prefix = doc_prefix
        self.query_prefix = query_prefix
        self.model = SentenceTransformer(model_name, device=device, trust_remote_code=trust_remote_code)

    def _apply_prefix(self, texts: List[str], prefix: str) -> List[str]:
        if not prefix:
            return texts
        return [f"{prefix}{text}" for text in texts]

    def encode_query(self, query: str) -> np.ndarray:
        vectors = self.model.encode(
            self._apply_prefix([query], self.query_prefix),
            batch_size=1,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype=np.float32)[0]


class ArtifactHybridRetriever:
    def __init__(self, index_root: Path, embedding_device_override: Optional[str] = None) -> None:
        self.index_root = index_root
        self.manifest = read_json(index_root / "manifest.json")
        self.docstore = {row["doc_id"]: row for row in read_jsonl(index_root / "docstore.jsonl")}
        self.bm25 = BM25Index.from_dict(read_gzip_json(index_root / "bm25_index.json.gz"))
        self.graph = read_gzip_json(index_root / "graph_index.json.gz")

        emb = self.manifest["embedding"]
        self.embedder = TextEmbedder(
            model_name=emb["model_name"],
            device=embedding_device_override or emb.get("device") or None,
            trust_remote_code=bool(emb.get("trust_remote_code", True)),
            batch_size=int(emb.get("batch_size", 8)),
            doc_prefix=emb.get("doc_prefix", ""),
            query_prefix=emb.get("query_prefix", ""),
        )
        self.dense = ChromaDenseIndex(index_root=index_root, collection_name=self.manifest["dense_index"]["collection_name"])

    def dense_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        qvec = self.embedder.encode_query(query)
        return self.dense.search(qvec, top_k)

    def bm25_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        return self.bm25.search(query, top_k)

    @staticmethod
    def rrf_fuse(
        dense_hits: List[Dict[str, Any]],
        bm25_hits: List[Dict[str, Any]],
        dense_weight: float,
        bm25_weight: float,
        rrf_k: int,
    ) -> List[Dict[str, Any]]:
        scores: Dict[str, dict] = {}
        for rank, hit in enumerate(dense_hits, start=1):
            doc_id = hit["doc_id"]
            row = scores.setdefault(doc_id, {"doc_id": doc_id, "dense_rank": None, "bm25_rank": None, "dense_score": None, "bm25_score": None, "fused_score": 0.0})
            row["dense_rank"] = rank
            row["dense_score"] = float(hit["score"])
            row["fused_score"] += float(dense_weight) * (1.0 / (rrf_k + rank))
        for rank, hit in enumerate(bm25_hits, start=1):
            doc_id = hit["doc_id"]
            row = scores.setdefault(doc_id, {"doc_id": doc_id, "dense_rank": None, "bm25_rank": None, "dense_score": None, "bm25_score": None, "fused_score": 0.0})
            row["bm25_rank"] = rank
            row["bm25_score"] = float(hit["score"])
            row["fused_score"] += float(bm25_weight) * (1.0 / (rrf_k + rank))
        return sorted(scores.values(), key=lambda x: x["fused_score"], reverse=True)

    def expand_with_graph(
        self,
        fused_hits: List[Dict[str, Any]],
        max_hops: int,
        graph_alpha: float,
    ) -> List[Dict[str, Any]]:
        if max_hops <= 0:
            return fused_hits
        score_map: Dict[str, dict] = {row["doc_id"]: dict(row) for row in fused_hits}
        doc_meta = self.docstore
        out_edges = self.graph.get("out", {})
        concept_to_evidence = self.graph.get("concept_to_evidence", {})
        section_to_evidence = self.graph.get("section_to_evidence", {})

        frontier = [(row["doc_id"], float(row["fused_score"]), 0) for row in fused_hits]
        seen_pairs: Set[Tuple[str, int]] = set()

        while frontier:
            current_id, seed_score, hop = frontier.pop(0)
            if hop >= max_hops:
                continue
            doc = doc_meta.get(current_id, {})
            neighbors: List[str] = []

            for edge in out_edges.get(current_id, []):
                dst = edge.get("dst")
                if dst:
                    neighbors.append(dst)
                    if dst.startswith("concept:"):
                        neighbors.extend(concept_to_evidence.get(dst, []))

            if doc.get("doc_type") == "concept":
                neighbors.extend(concept_to_evidence.get(current_id, []))
            if doc.get("doc_type") == "section":
                neighbors.extend(section_to_evidence.get(current_id, []))

            for neighbor_id in unique_keep_order(neighbors):
                if neighbor_id not in doc_meta:
                    continue
                pair = (neighbor_id, hop + 1)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                bonus = seed_score * float(graph_alpha) / float(hop + 1)
                row = score_map.setdefault(
                    neighbor_id,
                    {
                        "doc_id": neighbor_id,
                        "dense_rank": None,
                        "bm25_rank": None,
                        "dense_score": None,
                        "bm25_score": None,
                        "fused_score": 0.0,
                    },
                )
                row["fused_score"] += bonus
                row.setdefault("graph_expanded", True)
                frontier.append((neighbor_id, bonus, hop + 1))

        return sorted(score_map.values(), key=lambda x: x["fused_score"], reverse=True)

    def search(
        self,
        query: str,
        top_k: int,
        dense_k: int,
        bm25_k: int,
        dense_weight: float,
        bm25_weight: float,
        rrf_k: int,
        graph_hops: int,
        graph_alpha: float,
        allowed_doc_types: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        dense_hits = self.dense_search(query, dense_k)
        bm25_hits = self.bm25_search(query, bm25_k)
        fused = self.rrf_fuse(dense_hits, bm25_hits, dense_weight, bm25_weight, rrf_k)
        fused = self.expand_with_graph(fused, graph_hops, graph_alpha)

        enriched: List[dict] = []
        for row in fused:
            doc = self.docstore.get(row["doc_id"])
            if not doc:
                continue
            if allowed_doc_types and doc.get("doc_type") not in allowed_doc_types:
                continue
            payload = dict(row)
            payload["doc_type"] = doc.get("doc_type")
            payload["title"] = doc.get("title")
            payload["snippet"] = truncate(doc.get("text", ""), 700)
            payload["payload"] = doc.get("payload", {})
            enriched.append(payload)
            if len(enriched) >= top_k:
                break

        return {
            "query": query,
            "config": {
                "top_k": top_k,
                "dense_k": dense_k,
                "bm25_k": bm25_k,
                "dense_weight": dense_weight,
                "bm25_weight": bm25_weight,
                "rrf_k": rrf_k,
                "graph_hops": graph_hops,
                "graph_alpha": graph_alpha,
                "allowed_doc_types": sorted(allowed_doc_types) if allowed_doc_types else None,
            },
            "results": enriched,
        }


class OpenAICompatVLM:
    def __init__(
        self,
        api_base: str,
        model: str,
        api_key: str = "EMPTY",
        temperature: float = 0.0,
        timeout: int = 180,
        max_tokens: int = 1024,
    ) -> None:
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.session = requests.Session()

    def _post(self, payload: dict) -> dict:
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = self.session.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _build_user_content(self, user_text: str, image_paths: Optional[List[str]]) -> Any:
        if not image_paths:
            return user_text
        content: List[dict] = [{"type": "text", "text": user_text}]
        for path in image_paths:
            if not path:
                continue
            p = Path(path)
            if not p.exists():
                continue
            suffix = p.suffix.lower()
            mime = "image/png" if suffix == ".png" else "image/jpeg"
            import base64
            b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
            content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}})
        return content

    def chat_text(self, system_prompt: str, user_text: str, image_paths: Optional[List[str]] = None) -> str:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self._build_user_content(user_text, image_paths)},
            ],
        }
        res = self._post(payload)
        return res["choices"][0]["message"]["content"]

    def chat_json(self, system_prompt: str, user_text: str, image_paths: Optional[List[str]] = None) -> dict:
        text = self.chat_text(system_prompt=system_prompt, user_text=user_text, image_paths=image_paths)
        payload = safe_json_loads(text)
        if payload is None:
            raise ValueError(f"Model did not return valid JSON. Raw output: {text[:1200]}")
        return payload


class GraphState(TypedDict, total=False):
    original_query: str
    current_query: str
    query_image_paths: List[str]
    image_grounding: str
    retrieval_rounds: List[dict]
    latest_results: List[dict]
    latest_context: str
    latest_query_used: str
    reflection: dict
    reflection_history: List[dict]
    rewritten_query: str
    iteration: int
    max_reflections: int
    base_retrieval_cfg: dict
    active_retrieval_cfg: dict
    final_context_bundle: dict
    answer: str
    final_output: dict



def sanitize_doc_types(values: Any) -> Optional[Set[str]]:
    allowed = {"evidence", "concept", "requirement", "section"}
    if not values:
        return None
    cleaned = {norm_text(v) for v in values if norm_text(v) in allowed}
    return cleaned or None



def clamp_int(value: Any, default: int, lower: int, upper: int) -> int:
    try:
        value = int(value)
    except Exception:
        return default
    return max(lower, min(upper, value))



def build_context_string(results: List[dict], max_docs: int = 10, max_chars_per_doc: int = 900) -> str:
    chunks: List[str] = []
    for idx, row in enumerate(results[:max_docs], start=1):
        payload = row.get("payload", {}) or {}
        chunks.append(
            "\n".join(
                [
                    f"[Doc {idx}]",
                    f"doc_id: {row.get('doc_id')}",
                    f"doc_type: {row.get('doc_type')}",
                    f"title: {row.get('title')}",
                    f"score: {row.get('fused_score')}",
                    f"snippet: {truncate(row.get('snippet', ''), max_chars_per_doc)}",
                    f"payload: {json.dumps(payload, ensure_ascii=False)}",
                ]
            )
        )
    return "\n\n".join(chunks)


class ReflectionWorkflow:
    def __init__(
        self,
        retriever: ArtifactHybridRetriever,
        model: OpenAICompatVLM,
        generate_answer: bool,
        answer_context_docs: int,
        answer_context_chars: int,
    ) -> None:
        self.retriever = retriever
        self.model = model
        self.generate_answer = generate_answer
        self.answer_context_docs = answer_context_docs
        self.answer_context_chars = answer_context_chars
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(GraphState)
        graph.add_node("ground_image", self.ground_image_node)
        graph.add_node("retrieve", self.retrieve_node)
        graph.add_node("reflect", self.reflect_node)
        graph.add_node("rewrite", self.rewrite_node)
        graph.add_node("finalize", self.finalize_node)

        graph.add_edge(START, "ground_image")
        graph.add_edge("ground_image", "retrieve")
        graph.add_edge("retrieve", "reflect")
        graph.add_conditional_edges("reflect", self.route_after_reflect, {"rewrite": "rewrite", "finalize": "finalize"})
        graph.add_edge("rewrite", "retrieve")
        graph.add_edge("finalize", END)
        return graph.compile()

    def ground_image_node(self, state: GraphState) -> GraphState:
        image_paths = list(state.get("query_image_paths", []))
        if not image_paths:
            return {"image_grounding": ""}
        user_text = (
            f"User query: {state.get('original_query', '')}\n\n"
            "Describe the image in retrieval-friendly technical terms."
        )
        grounded = self.model.chat_text(
            system_prompt=IMAGE_GROUNDING_SYSTEM_PROMPT,
            user_text=user_text,
            image_paths=image_paths,
        )
        return {"image_grounding": norm_text(grounded)}

    def retrieve_node(self, state: GraphState) -> GraphState:
        query = norm_text(state.get("current_query") or state.get("original_query") or "")
        image_grounding = norm_text(state.get("image_grounding", ""))
        query_used = query if not image_grounding else f"{query}\n\nIMAGE_GROUNDING: {image_grounding}"
        cfg = dict(state.get("active_retrieval_cfg", {}))
        result = self.retriever.search(
            query=query_used,
            top_k=int(cfg["top_k"]),
            dense_k=int(cfg["dense_k"]),
            bm25_k=int(cfg["bm25_k"]),
            dense_weight=float(cfg["dense_weight"]),
            bm25_weight=float(cfg["bm25_weight"]),
            rrf_k=int(cfg["rrf_k"]),
            graph_hops=int(cfg["graph_hops"]),
            graph_alpha=float(cfg["graph_alpha"]),
            allowed_doc_types=cfg.get("allowed_doc_types"),
        )
        latest_results = result["results"]
        latest_context = build_context_string(latest_results, max_docs=12, max_chars_per_doc=900)
        rounds = list(state.get("retrieval_rounds", []))
        rounds.append({
            "iteration": int(state.get("iteration", 0)),
            "query_used": query_used,
            "retrieval_config": {
                **cfg,
                "allowed_doc_types": sorted(cfg.get("allowed_doc_types")) if cfg.get("allowed_doc_types") else None,
            },
            "result_count": len(latest_results),
            "results": latest_results,
        })
        return {
            "latest_query_used": query_used,
            "latest_results": latest_results,
            "latest_context": latest_context,
            "retrieval_rounds": rounds,
        }

    def reflect_node(self, state: GraphState) -> GraphState:
        user_text = (
            f"Original query:\n{state.get('original_query', '')}\n\n"
            f"Current query:\n{state.get('current_query', '')}\n\n"
            f"Retrieved context:\n{state.get('latest_context', '')}"
        )
        reflection = self.model.chat_json(
            system_prompt=REFLECTION_SYSTEM_PROMPT,
            user_text=user_text,
        )

        base_cfg = dict(state.get("base_retrieval_cfg", {}))
        next_cfg = dict(state.get("active_retrieval_cfg", {}))
        suggested_doc_types = sanitize_doc_types(reflection.get("suggested_doc_types"))
        if suggested_doc_types is not None:
            next_cfg["allowed_doc_types"] = suggested_doc_types
        next_cfg["graph_hops"] = clamp_int(reflection.get("suggested_graph_hops"), int(base_cfg["graph_hops"]), 0, 3)
        next_cfg["dense_k"] = clamp_int(reflection.get("suggested_dense_k"), int(base_cfg["dense_k"]), 1, 200)
        next_cfg["bm25_k"] = clamp_int(reflection.get("suggested_bm25_k"), int(base_cfg["bm25_k"]), 1, 200)
        next_cfg["top_k"] = clamp_int(reflection.get("suggested_top_k"), int(base_cfg["top_k"]), 1, 50)

        reflection_history = list(state.get("reflection_history", []))
        reflection_history.append(
            {
                "iteration": int(state.get("iteration", 0)),
                "reflection": reflection,
                "next_retrieval_cfg": {
                    **next_cfg,
                    "allowed_doc_types": sorted(next_cfg.get("allowed_doc_types")) if next_cfg.get("allowed_doc_types") else None,
                },
            }
        )
        return {
            "reflection": reflection,
            "rewritten_query": norm_text(reflection.get("rewritten_query") or state.get("current_query") or state.get("original_query") or ""),
            "active_retrieval_cfg": next_cfg,
            "reflection_history": reflection_history,
        }

    def route_after_reflect(self, state: GraphState) -> str:
        reflection = state.get("reflection", {}) or {}
        sufficient = bool(reflection.get("sufficient", False))
        iteration = int(state.get("iteration", 0))
        max_reflections = int(state.get("max_reflections", 0))
        if sufficient or iteration >= max_reflections:
            return "finalize"
        return "rewrite"

    def rewrite_node(self, state: GraphState) -> GraphState:
        new_iteration = int(state.get("iteration", 0)) + 1
        rewritten = norm_text(state.get("rewritten_query") or state.get("current_query") or state.get("original_query") or "")
        return {
            "iteration": new_iteration,
            "current_query": rewritten,
        }

    def finalize_node(self, state: GraphState) -> GraphState:
        final_context_bundle = {
            "original_query": state.get("original_query"),
            "final_query": state.get("current_query"),
            "query_used_last_round": state.get("latest_query_used"),
            "image_grounding": state.get("image_grounding", ""),
            "retrieval_rounds": state.get("retrieval_rounds", []),
            "reflection_history": state.get("reflection_history", []),
            "latest_results": state.get("latest_results", []),
            "latest_context": state.get("latest_context", ""),
        }
        answer = ""
        if self.generate_answer:
            answer_context = build_context_string(
                list(state.get("latest_results", [])),
                max_docs=self.answer_context_docs,
                max_chars_per_doc=self.answer_context_chars,
            )
            user_text = (
                f"User query:\n{state.get('original_query', '')}\n\n"
                f"Retrieved context bundle:\n{answer_context}"
            )
            answer = self.model.chat_text(
                system_prompt=ANSWER_SYSTEM_PROMPT,
                user_text=user_text,
            )

        final_output = {
            "original_query": state.get("original_query"),
            "final_query": state.get("current_query"),
            "image_grounding": state.get("image_grounding", ""),
            "iteration": int(state.get("iteration", 0)),
            "reflection": state.get("reflection", {}),
            "reflection_history": state.get("reflection_history", []),
            "retrieval_rounds": state.get("retrieval_rounds", []),
            "final_context_bundle": final_context_bundle,
            "answer": answer,
        }
        return {
            "final_context_bundle": final_context_bundle,
            "answer": answer,
            "final_output": final_output,
        }

    def invoke(self, state: GraphState) -> GraphState:
        return self.graph.invoke(state, config={"recursion_limit": max(8, int(state.get("max_reflections", 0)) * 3 + 8)})



def build_initial_state(args: argparse.Namespace, base_retrieval_cfg: dict) -> GraphState:
    return {
        "original_query": args.query,
        "current_query": args.query,
        "query_image_paths": [str(p) for p in (args.query_image or [])],
        "image_grounding": "",
        "retrieval_rounds": [],
        "latest_results": [],
        "latest_context": "",
        "latest_query_used": "",
        "reflection": {},
        "reflection_history": [],
        "rewritten_query": "",
        "iteration": 0,
        "max_reflections": args.max_reflections,
        "base_retrieval_cfg": base_retrieval_cfg,
        "active_retrieval_cfg": dict(base_retrieval_cfg),
        "final_context_bundle": {},
        "answer": "",
        "final_output": {},
    }



def cmd_run(args: argparse.Namespace) -> None:
    retriever = ArtifactHybridRetriever(
        index_root=args.index_root.resolve(),
        embedding_device_override=args.embedding_device,
    )

    model = OpenAICompatVLM(
        api_base=args.api_base,
        model=args.model,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=args.timeout,
        max_tokens=args.max_tokens,
    )

    base_retrieval_cfg = {
        "top_k": args.top_k,
        "dense_k": args.dense_k,
        "bm25_k": args.bm25_k,
        "dense_weight": args.dense_weight,
        "bm25_weight": args.bm25_weight,
        "rrf_k": args.rrf_k,
        "graph_hops": args.graph_hops,
        "graph_alpha": args.graph_alpha,
        "allowed_doc_types": set(args.doc_types) if args.doc_types else None,
    }

    workflow = ReflectionWorkflow(
        retriever=retriever,
        model=model,
        generate_answer=args.generate_answer,
        answer_context_docs=args.answer_context_docs,
        answer_context_chars=args.answer_context_chars,
    )

    if args.graph_png:
        save_graph_png(workflow.graph, args.graph_png.resolve())
    if args.graph_jpg:
        save_graph_jpg(workflow.graph, args.graph_jpg.resolve())

    state = build_initial_state(args, base_retrieval_cfg)
    result = workflow.invoke(state)
    final_output = result.get("final_output", result)

    if args.output_json:
        write_json(args.output_json.resolve(), final_output)

    print(json.dumps(final_output, ensure_ascii=False, indent=2))



def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 4: LangGraph reflection loop over a built Phase 3 index.")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run retrieve -> reflect -> rewrite -> retrieve over the Phase 3 artifacts.")
    run.add_argument("--index-root", type=Path, required=True, help="Directory containing the built phase_3 outputs.")
    run.add_argument("--query", type=str, required=True, help="User query.")
    run.add_argument("--query-image", type=Path, nargs="*", default=None, help="Optional query image path(s) for VL grounding.")
    run.add_argument("--api-base", type=str, default=os.environ.get("PHASE4_API_BASE", "http://127.0.0.1:8000/v1"), help="OpenAI-compatible base URL for the local vLLM server.")
    run.add_argument("--api-key", type=str, default=os.environ.get("PHASE4_API_KEY", "EMPTY"), help="API key for the OpenAI-compatible endpoint.")
    run.add_argument("--model", type=str, default=os.environ.get("PHASE4_MODEL", "Qwen/Qwen2.5-VL-72B-Instruct"), help="Model name exposed by the vLLM server.")
    run.add_argument("--temperature", type=float, default=0.0, help="Generation temperature.")
    run.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds.")
    run.add_argument("--max-tokens", type=int, default=1024, help="Max generation tokens per model call.")
    run.add_argument("--max-reflections", type=int, default=2, help="Max reflection-driven rewrites before finalizing.")
    run.add_argument("--embedding-device", type=str, default=None, help="Optional override for the query embedding device, for example cuda:0 or cpu. By default, the phase_3 manifest value is used.")

    run.add_argument("--top-k", type=int, default=12, help="Final number of retrieval results after fusion and graph expansion.")
    run.add_argument("--dense-k", type=int, default=30, help="Top-k dense hits before fusion.")
    run.add_argument("--bm25-k", type=int, default=30, help="Top-k BM25 hits before fusion.")
    run.add_argument("--dense-weight", type=float, default=1.0, help="Dense RRF weight.")
    run.add_argument("--bm25-weight", type=float, default=1.0, help="BM25 RRF weight.")
    run.add_argument("--rrf-k", type=int, default=60, help="RRF constant.")
    run.add_argument("--graph-hops", type=int, default=1, help="Graph expansion hops.")
    run.add_argument("--graph-alpha", type=float, default=0.15, help="Graph expansion score decay factor.")
    run.add_argument("--doc-types", nargs="*", default=None, help="Optional doc type filter: evidence concept requirement section")

    run.add_argument("--generate-answer", action="store_true", help="Generate a grounded final answer using the last retrieval bundle.")
    run.add_argument("--answer-context-docs", type=int, default=10, help="How many retrieved docs to pass into final answer generation.")
    run.add_argument("--answer-context-chars", type=int, default=900, help="Max chars per retrieved doc in final answer context.")
    run.add_argument("--graph-png", type=Path, default=None, help="Optional path to save the LangGraph workflow as a PNG.")
    run.add_argument("--graph-jpg", type=Path, default=None, help="Optional path to save the LangGraph workflow as a JPG.")
    run.add_argument("--output-json", type=Path, default=None, help="Optional JSON output path.")

    return p



def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        cmd_run(args)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
