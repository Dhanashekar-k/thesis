from __future__ import annotations

import argparse
import gzip
import json
import math
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
WHITESPACE_RE = re.compile(r"\s+")


@dataclass
class RetrievalDoc:
    doc_id: str
    doc_type: str
    title: str
    text: str
    payload: Dict[str, Any]

    def to_json(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "doc_type": self.doc_type,
            "title": self.title,
            "text": self.text,
            "payload": self.payload,
        }


def norm_text(text: Any) -> str:
    return WHITESPACE_RE.sub(" ", str(text or "")).strip()


def unique_keep_order(values: Iterable[str]) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()
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


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_gzip_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


def read_gzip_json(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(norm_text(text))]


def truncate(text: str, max_chars: int) -> str:
    text = norm_text(text)
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " ... [truncated]"


def discover_phase1_root(phase2_root: Path, explicit_phase1_root: Optional[Path]) -> Optional[Path]:
    if explicit_phase1_root is not None:
        return explicit_phase1_root
    manifest_path = phase2_root / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = read_json(manifest_path)
    raw = manifest.get("phase1_root")
    if not raw:
        return None
    root = Path(raw)
    return root if root.exists() else None


def load_phase2_bundle(phase2_root: Path, phase1_root: Optional[Path]) -> Dict[str, Any]:
    bundle: Dict[str, Any] = {
        "phase2_root": str(phase2_root.resolve()),
        "evidence_units": read_jsonl(phase2_root / "evidence_units.jsonl"),
        "concept_nodes": read_jsonl(phase2_root / "concept_nodes.jsonl"),
        "semantic_edges": read_jsonl(phase2_root / "semantic_edges.jsonl"),
    }
    if phase1_root is not None and (phase1_root / "sections.jsonl").exists():
        bundle["sections"] = read_jsonl(phase1_root / "sections.jsonl")
    else:
        bundle["sections"] = []
    return bundle


def build_section_lookup(sections: List[dict], evidence_units: List[dict]) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for sec in sections:
        sid = norm_text(sec.get("section_id"))
        if sid:
            out[sid] = sec
    for ev in evidence_units:
        sid = norm_text(ev.get("section_id"))
        if sid and sid not in out:
            title = norm_text((ev.get("extra") or {}).get("section_title"))
            out[sid] = {
                "section_id": sid,
                "clause_id": None,
                "title": title or sid,
                "pages": sorted(set(int(p) for p in ev.get("page_indices", []) if p is not None)),
            }
    return out


def build_evidence_docs(
    evidence_units: List[dict],
    section_lookup: Dict[str, dict],
    max_raw_chars: int,
    max_context_chars: int,
) -> List[RetrievalDoc]:
    docs: List[RetrievalDoc] = []
    for ev in evidence_units:
        ev_id = norm_text(ev.get("evidence_id"))
        if not ev_id:
            continue
        section_id = norm_text(ev.get("section_id")) or None
        section_title = norm_text((ev.get("extra") or {}).get("section_title"))
        if not section_title and section_id in section_lookup:
            section_title = norm_text(section_lookup[section_id].get("title"))
        modality = norm_text(ev.get("modality")) or "unknown"
        classification = norm_text(ev.get("classification"))
        caption = norm_text(ev.get("caption"))
        proxy = norm_text(ev.get("proxy_description"))
        keywords = unique_keep_order(ev.get("keywords", []))
        concepts = unique_keep_order(c.get("name", "") for c in ev.get("concepts", []))
        requirements = unique_keep_order(ev.get("requirement_refs", []))
        raw_text = truncate(ev.get("raw_text", ""), max_raw_chars)
        context_text = truncate(ev.get("context_text", ""), max_context_chars)

        title = proxy or caption or section_title or ev_id
        parts = [f"DOC_TYPE: evidence", f"MODALITY: {modality}", f"TITLE: {title}"]
        if classification:
            parts.append(f"CLASSIFICATION: {classification}")
        if section_id:
            parts.append(f"SECTION_ID: {section_id}")
        if section_title:
            parts.append(f"SECTION_TITLE: {section_title}")
        if caption:
            parts.append(f"CAPTION: {caption}")
        if proxy:
            parts.append(f"PROXY_DESCRIPTION: {proxy}")
        if keywords:
            parts.append(f"KEYWORDS: {', '.join(keywords)}")
        if concepts:
            parts.append(f"CONCEPTS: {', '.join(concepts)}")
        if requirements:
            parts.append(f"REQUIREMENTS: {', '.join(requirements)}")
        if raw_text:
            parts.append(f"RAW_TEXT: {raw_text}")
        if context_text:
            parts.append(f"CONTEXT: {context_text}")

        docs.append(
            RetrievalDoc(
                doc_id=ev_id,
                doc_type="evidence",
                title=title,
                text="\n".join(parts),
                payload={
                    "doc_type": "evidence",
                    "modality": modality,
                    "section_id": section_id,
                    "section_title": section_title or None,
                    "page_indices": [int(p) for p in ev.get("page_indices", []) if p is not None],
                    "classification": classification or None,
                    "caption": caption or None,
                    "requirement_refs": requirements,
                    "concept_names": concepts,
                    "keyword_count": len(keywords),
                    "source_ids": list(ev.get("source_ids", [])),
                },
            )
        )
    return docs


def build_concept_docs(
    concept_nodes: List[dict],
    evidence_by_id: Dict[str, dict],
    max_evidence_snippets: int,
    max_snippet_chars: int,
) -> List[RetrievalDoc]:
    docs: List[RetrievalDoc] = []
    for concept in concept_nodes:
        concept_id = norm_text(concept.get("concept_id"))
        name = norm_text(concept.get("name"))
        if not concept_id or not name:
            continue
        aliases = unique_keep_order(concept.get("aliases", []))
        source_evidence_ids = unique_keep_order(concept.get("source_evidence_ids", []))
        definition_evidence_ids = unique_keep_order(concept.get("definition_evidence_ids", []))
        ctype = norm_text(concept.get("type")) or "other"

        definition_snippets: List[str] = []
        for ev_id in definition_evidence_ids[:max_evidence_snippets]:
            ev = evidence_by_id.get(ev_id)
            if not ev:
                continue
            definition_snippets.append(truncate(ev.get("proxy_description") or ev.get("raw_text") or "", max_snippet_chars))

        usage_snippets: List[str] = []
        for ev_id in source_evidence_ids[:max_evidence_snippets]:
            ev = evidence_by_id.get(ev_id)
            if not ev:
                continue
            usage_snippets.append(truncate(ev.get("proxy_description") or ev.get("raw_text") or "", max_snippet_chars))

        parts = [f"DOC_TYPE: concept", f"TITLE: {name}", f"CONCEPT_TYPE: {ctype}"]
        if aliases:
            parts.append(f"ALIASES: {', '.join(aliases)}")
        if definition_snippets:
            parts.append("DEFINITION_EVIDENCE: " + " | ".join(definition_snippets))
        if usage_snippets:
            parts.append("USAGE_EVIDENCE: " + " | ".join(usage_snippets))

        docs.append(
            RetrievalDoc(
                doc_id=concept_id,
                doc_type="concept",
                title=name,
                text="\n".join(parts),
                payload={
                    "doc_type": "concept",
                    "type": ctype,
                    "aliases": aliases,
                    "source_evidence_ids": source_evidence_ids,
                    "definition_evidence_ids": definition_evidence_ids,
                    "confidence": float(concept.get("confidence", 0.0) or 0.0),
                },
            )
        )
    return docs


def build_requirement_docs(
    evidence_units: List[dict],
    max_evidence_snippets: int,
    max_snippet_chars: int,
) -> List[RetrievalDoc]:
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for ev in evidence_units:
        for req in ev.get("requirement_refs", []):
            rid = norm_text(req).strip("[]")
            if rid:
                grouped[rid].append(ev)

    docs: List[RetrievalDoc] = []
    for rid, rows in grouped.items():
        section_titles = unique_keep_order((ev.get("extra") or {}).get("section_title", "") for ev in rows)
        evidence_ids = unique_keep_order(ev.get("evidence_id", "") for ev in rows)
        snippets = [truncate(ev.get("proxy_description") or ev.get("raw_text") or "", max_snippet_chars) for ev in rows[:max_evidence_snippets]]
        parts = [f"DOC_TYPE: requirement", f"TITLE: {rid}"]
        if section_titles:
            parts.append(f"SECTIONS: {', '.join(section_titles)}")
        if snippets:
            parts.append("EVIDENCE: " + " | ".join(snippets))
        docs.append(
            RetrievalDoc(
                doc_id=f"requirement:{rid}",
                doc_type="requirement",
                title=rid,
                text="\n".join(parts),
                payload={
                    "doc_type": "requirement",
                    "requirement_id": rid,
                    "section_titles": section_titles,
                    "evidence_ids": evidence_ids,
                },
            )
        )
    return docs


def build_section_docs(
    evidence_units: List[dict],
    section_lookup: Dict[str, dict],
    max_snippets: int,
    max_snippet_chars: int,
) -> List[RetrievalDoc]:
    by_section: Dict[str, List[dict]] = defaultdict(list)
    for ev in evidence_units:
        sid = norm_text(ev.get("section_id"))
        if sid:
            by_section[sid].append(ev)

    docs: List[RetrievalDoc] = []
    for section_id, rows in by_section.items():
        sec = section_lookup.get(section_id, {})
        title = norm_text(sec.get("title")) or norm_text((rows[0].get("extra") or {}).get("section_title")) or section_id
        clause_id = norm_text(sec.get("clause_id"))
        requirement_refs = unique_keep_order(req for ev in rows for req in ev.get("requirement_refs", []))
        concept_names = unique_keep_order(c.get("name", "") for ev in rows for c in ev.get("concepts", []))
        snippets = [truncate(ev.get("proxy_description") or ev.get("raw_text") or "", max_snippet_chars) for ev in rows[:max_snippets]]
        page_indices = sorted({int(p) for ev in rows for p in ev.get("page_indices", []) if p is not None})

        parts = [f"DOC_TYPE: section", f"TITLE: {title}"]
        if clause_id:
            parts.append(f"CLAUSE_ID: {clause_id}")
        parts.append(f"SECTION_ID: {section_id}")
        if requirement_refs:
            parts.append(f"REQUIREMENTS: {', '.join(requirement_refs)}")
        if concept_names:
            parts.append(f"CONCEPTS: {', '.join(concept_names[:50])}")
        if snippets:
            parts.append("EVIDENCE: " + " | ".join(snippets))

        docs.append(
            RetrievalDoc(
                doc_id=section_id,
                doc_type="section",
                title=title,
                text="\n".join(parts),
                payload={
                    "doc_type": "section",
                    "clause_id": clause_id or None,
                    "section_id": section_id,
                    "page_indices": page_indices,
                    "requirement_refs": requirement_refs,
                    "evidence_ids": unique_keep_order(ev.get("evidence_id", "") for ev in rows),
                },
            )
        )
    return docs


def build_retrieval_docs(
    bundle: Dict[str, Any],
    include_concepts: bool,
    include_requirements: bool,
    include_sections: bool,
    max_raw_chars: int,
    max_context_chars: int,
    max_evidence_snippets: int,
    max_snippet_chars: int,
) -> List[RetrievalDoc]:
    evidence_units = bundle["evidence_units"]
    concept_nodes = bundle["concept_nodes"]
    section_lookup = build_section_lookup(bundle.get("sections", []), evidence_units)
    evidence_by_id = {norm_text(ev.get("evidence_id")): ev for ev in evidence_units if norm_text(ev.get("evidence_id"))}

    docs: List[RetrievalDoc] = []
    docs.extend(build_evidence_docs(evidence_units, section_lookup, max_raw_chars, max_context_chars))

    if include_concepts:
        docs.extend(build_concept_docs(concept_nodes, evidence_by_id, max_evidence_snippets, max_snippet_chars))
    if include_requirements:
        docs.extend(build_requirement_docs(evidence_units, max_evidence_snippets, max_snippet_chars))
    if include_sections:
        docs.extend(build_section_docs(evidence_units, section_lookup, max_evidence_snippets, max_snippet_chars))

    deduped: Dict[str, RetrievalDoc] = {}
    for doc in docs:
        deduped[doc.doc_id] = doc
    return list(deduped.values())


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

    def build(self, docs: List[RetrievalDoc]) -> None:
        self.doc_ids = []
        self.doc_lengths = []
        self.doc_freqs = {}
        self.postings = {}
        self.doc_titles = {}
        self.doc_types = {}
        term_doc_counts: Counter[str] = Counter()

        for idx, doc in enumerate(docs):
            weighted_text = f"{doc.title} {doc.title} {doc.text}"
            tokens = tokenize(weighted_text)
            tf = Counter(tokens)
            self.doc_ids.append(doc.doc_id)
            self.doc_lengths.append(len(tokens))
            self.doc_titles[doc.doc_id] = doc.title
            self.doc_types[doc.doc_id] = doc.doc_type
            for term, freq in tf.items():
                self.postings.setdefault(term, []).append((idx, int(freq)))
            term_doc_counts.update(tf.keys())

        self.doc_freqs = dict(term_doc_counts)
        self.avgdl = (sum(self.doc_lengths) / len(self.doc_lengths)) if self.doc_lengths else 0.0

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
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            for doc_ix, tf in postings:
                dl = self.doc_lengths[doc_ix]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / avgdl))
                scores[doc_ix] += idf * ((tf * (self.k1 + 1.0)) / denom)

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

    def to_dict(self) -> dict:
        return {
            "k1": self.k1,
            "b": self.b,
            "doc_ids": self.doc_ids,
            "doc_lengths": self.doc_lengths,
            "avgdl": self.avgdl,
            "doc_freqs": self.doc_freqs,
            "postings": {term: [[doc_ix, tf] for doc_ix, tf in posting] for term, posting in self.postings.items()},
            "doc_titles": self.doc_titles,
            "doc_types": self.doc_types,
        }

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

    def recreate(self) -> None:
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def get_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, vectors: np.ndarray, docs: List[RetrievalDoc], batch_size: int = 128) -> None:
        collection = self.get_collection()
        for start in range(0, len(docs), batch_size):
            end = min(start + batch_size, len(docs))
            batch_docs = docs[start:end]
            batch_vectors = vectors[start:end]
            ids = [doc.doc_id for doc in batch_docs]
            embeddings = batch_vectors.astype(np.float32).tolist()
            metadatas = []
            documents = []
            for doc in batch_docs:
                meta = {
                    "doc_id": doc.doc_id,
                    "doc_type": doc.doc_type,
                    "title": doc.title,
                    "section_id": doc.payload.get("section_id") or "",
                    "section_title": doc.payload.get("section_title") or "",
                    "modality": doc.payload.get("modality") or "",
                    "page_indices": json.dumps(doc.payload.get("page_indices", []), ensure_ascii=False),
                }
                metadatas.append(meta)
                documents.append(doc.text)
            collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

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

    def encode_documents(self, texts: List[str]) -> np.ndarray:
        vectors = self.model.encode(
            self._apply_prefix(texts, self.doc_prefix),
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype=np.float32)

    def encode_query(self, query: str) -> np.ndarray:
        vectors = self.model.encode(
            self._apply_prefix([query], self.query_prefix),
            batch_size=1,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype=np.float32)[0]


class HybridRetriever:
    def __init__(self, index_root: Path) -> None:
        self.index_root = index_root
        self.manifest = read_json(index_root / "manifest.json")
        self.docstore = {row["doc_id"]: row for row in read_jsonl(index_root / "docstore.jsonl")}
        self.bm25 = BM25Index.from_dict(read_gzip_json(index_root / "bm25_index.json.gz"))
        self.graph = read_gzip_json(index_root / "graph_index.json.gz")
        emb = self.manifest["embedding"]
        self.embedder = TextEmbedder(
            model_name=emb["model_name"],
            device=emb.get("device") or None,
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
        seen_pairs: set[Tuple[str, int]] = set()

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
        allowed_doc_types: Optional[set[str]] = None,
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


def build_graph_index(semantic_edges: List[dict], docs: List[RetrievalDoc]) -> dict:
    out: Dict[str, List[dict]] = defaultdict(list)
    section_to_evidence: Dict[str, List[str]] = defaultdict(list)
    concept_to_evidence: Dict[str, List[str]] = defaultdict(list)

    for edge in semantic_edges:
        src = norm_text(edge.get("src"))
        rel = norm_text(edge.get("rel"))
        dst = norm_text(edge.get("dst"))
        if not src or not rel or not dst:
            continue
        out[src].append({"rel": rel, "dst": dst, "props": edge.get("props", {})})
        if src.startswith("evidence:") and dst.startswith("concept:") and rel in {"mentions_concept", "defines_concept"}:
            concept_to_evidence[dst].append(src)

    for doc in docs:
        if doc.doc_type == "section":
            for ev_id in doc.payload.get("evidence_ids", []):
                section_to_evidence[doc.doc_id].append(ev_id)
        if doc.doc_type == "concept":
            for ev_id in doc.payload.get("source_evidence_ids", []):
                concept_to_evidence[doc.doc_id].append(ev_id)

    return {
        "out": {k: v for k, v in out.items()},
        "section_to_evidence": {k: unique_keep_order(v) for k, v in section_to_evidence.items()},
        "concept_to_evidence": {k: unique_keep_order(v) for k, v in concept_to_evidence.items()},
    }


def cmd_build(args: argparse.Namespace) -> None:
    phase2_root = args.phase2_root.resolve()
    phase1_root = discover_phase1_root(phase2_root, args.phase1_root.resolve() if args.phase1_root else None)
    index_root = args.index_root.resolve()
    index_root.mkdir(parents=True, exist_ok=True)

    print("[Phase 3] Loading Phase 2 bundle...", flush=True)
    bundle = load_phase2_bundle(phase2_root, phase1_root)

    print("[Phase 3] Building retrieval documents...", flush=True)
    docs = build_retrieval_docs(
        bundle=bundle,
        include_concepts=not args.disable_concept_docs,
        include_requirements=not args.disable_requirement_docs,
        include_sections=not args.disable_section_docs,
        max_raw_chars=args.max_raw_chars,
        max_context_chars=args.max_context_chars,
        max_evidence_snippets=args.max_evidence_snippets,
        max_snippet_chars=args.max_snippet_chars,
    )
    docs = sorted(docs, key=lambda d: (d.doc_type, d.doc_id))
    if args.max_docs is not None:
        docs = docs[: args.max_docs]
    print(f"[Phase 3] Built {len(docs)} retrieval docs.", flush=True)

    docstore_rows = [doc.to_json() for doc in docs]
    write_jsonl(index_root / "docstore.jsonl", docstore_rows)

    print(f"[Phase 3] Building BM25 index over {len(docs)} docs...", flush=True)
    bm25 = BM25Index(k1=args.bm25_k1, b=args.bm25_b)
    bm25.build(docs)
    write_gzip_json(index_root / "bm25_index.json.gz", bm25.to_dict())

    print(f"[Phase 3] Encoding docs with {args.embedding_model}...", flush=True)
    embedder = TextEmbedder(
        model_name=args.embedding_model,
        device=args.device,
        trust_remote_code=args.trust_remote_code,
        batch_size=args.batch_size,
        doc_prefix=args.doc_prefix,
        query_prefix=args.query_prefix,
    )
    vectors = embedder.encode_documents([doc.text for doc in docs])
    print(f"[Phase 3] Dense vectors shape: {vectors.shape}", flush=True)

    print("[Phase 3] Writing Chroma persistent index...", flush=True)
    dense = ChromaDenseIndex(index_root=index_root, collection_name=args.collection_name)
    dense.recreate()
    dense.upsert(vectors=vectors, docs=docs, batch_size=args.chroma_batch_size)

    print("[Phase 3] Building graph sidecar...", flush=True)
    graph_index = build_graph_index(bundle["semantic_edges"], docs)
    write_gzip_json(index_root / "graph_index.json.gz", graph_index)

    manifest = {
        "phase": 3,
        "description": "Chroma dense vector index + lexical BM25 index + graph sidecar for hybrid retrieval.",
        "phase2_root": str(phase2_root),
        "phase1_root": str(phase1_root) if phase1_root else None,
        "index_root": str(index_root),
        "docstore": str((index_root / "docstore.jsonl").resolve()),
        "bm25_index": str((index_root / "bm25_index.json.gz").resolve()),
        "graph_index": str((index_root / "graph_index.json.gz").resolve()),
        "dense_index": {
            "backend": "chromadb-persistent",
            "chroma_path": str((index_root / "chroma").resolve()),
            "collection_name": args.collection_name,
            "distance": "cosine",
            "vector_size": int(vectors.shape[1]),
        },
        "embedding": {
            "model_name": args.embedding_model,
            "device": args.device,
            "trust_remote_code": bool(args.trust_remote_code),
            "batch_size": args.batch_size,
            "doc_prefix": args.doc_prefix,
            "query_prefix": args.query_prefix,
        },
        "bm25": {
            "k1": args.bm25_k1,
            "b": args.bm25_b,
        },
        "stats": {
            "doc_count": len(docs),
            "evidence_doc_count": sum(1 for d in docs if d.doc_type == "evidence"),
            "concept_doc_count": sum(1 for d in docs if d.doc_type == "concept"),
            "requirement_doc_count": sum(1 for d in docs if d.doc_type == "requirement"),
            "section_doc_count": sum(1 for d in docs if d.doc_type == "section"),
            "semantic_edge_count": len(bundle["semantic_edges"]),
        },
        "notes": [
            "No protocol-specific retrieval rules are hardcoded here; Phase 3 only consumes Phase 2 outputs.",
            "Dense retrieval uses ChromaDB while lexical retrieval uses a separate BM25 sidecar.",
            "Requirement and section docs are derived from existing metadata so later corpora can reuse the same pipeline.",
        ],
    }
    write_json(index_root / "manifest.json", manifest)
    print(json.dumps(manifest["stats"], indent=2), flush=True)
    print(f"Wrote Phase 3 manifest to {(index_root / 'manifest.json').resolve()}", flush=True)


def cmd_search(args: argparse.Namespace) -> None:
    retriever = HybridRetriever(args.index_root.resolve())
    allowed_doc_types = set(args.doc_types) if args.doc_types else None
    result = retriever.search(
        query=args.query,
        top_k=args.top_k,
        dense_k=args.dense_k,
        bm25_k=args.bm25_k,
        dense_weight=args.dense_weight,
        bm25_weight=args.bm25_weight,
        rrf_k=args.rrf_k,
        graph_hops=args.graph_hops,
        graph_alpha=args.graph_alpha,
        allowed_doc_types=allowed_doc_types,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 3: build a local Chroma + BM25 + graph retrieval index from Phase 2 outputs.")
    sub = p.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Build dense, lexical, and graph indices.")
    build.add_argument("--phase2-root", type=Path, required=True, help="Directory containing evidence_units.jsonl, concept_nodes.jsonl, semantic_edges.jsonl.")
    build.add_argument("--phase1-root", type=Path, default=None, help="Optional Phase 1 root. If omitted, Phase 3 tries to read it from Phase 2 manifest.json.")
    build.add_argument("--index-root", type=Path, required=True, help="Output directory for the Phase 3 retrieval index.")
    build.add_argument("--embedding-model", type=str, default=os.environ.get("PHASE3_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-8B"), help="SentenceTransformer-compatible embedding model name.")
    build.add_argument("--device", type=str, default=os.environ.get("PHASE3_DEVICE", "cuda"), help="Embedding device, for example cuda, cuda:0, or cpu.")
    build.add_argument("--trust-remote-code", action="store_true", default=True, help="Pass trust_remote_code=True to SentenceTransformer.")
    build.add_argument("--collection-name", type=str, default="phase3_hybrid", help="Chroma collection name.")
    build.add_argument("--batch-size", type=int, default=8, help="Embedding batch size.")
    build.add_argument("--chroma-batch-size", type=int, default=128, help="Batch size for inserting into Chroma.")
    build.add_argument("--bm25-k1", type=float, default=1.5, help="BM25 k1.")
    build.add_argument("--bm25-b", type=float, default=0.75, help="BM25 b.")
    build.add_argument("--max-raw-chars", type=int, default=4000, help="Max raw evidence characters kept per evidence doc.")
    build.add_argument("--max-context-chars", type=int, default=1500, help="Max context characters kept per evidence doc.")
    build.add_argument("--max-evidence-snippets", type=int, default=5, help="Max linked evidence snippets kept in concept/section/requirement docs.")
    build.add_argument("--max-snippet-chars", type=int, default=280, help="Max snippet length for derived docs.")
    build.add_argument("--doc-prefix", type=str, default="", help="Optional prefix prepended to every indexed document before embedding.")
    build.add_argument("--query-prefix", type=str, default="", help="Optional prefix prepended to every query before embedding.")
    build.add_argument("--disable-concept-docs", action="store_true", help="Skip concept retrieval docs.")
    build.add_argument("--disable-requirement-docs", action="store_true", help="Skip requirement retrieval docs.")
    build.add_argument("--disable-section-docs", action="store_true", help="Skip section retrieval docs.")
    build.add_argument("--max-docs", type=int, default=None, help="Optional limit for debugging.")

    search = sub.add_parser("search", help="Run hybrid retrieval against an existing Phase 3 index.")
    search.add_argument("--index-root", type=Path, required=True, help="Directory containing a built Phase 3 index.")
    search.add_argument("--query", type=str, required=True, help="User query.")
    search.add_argument("--top-k", type=int, default=12, help="Final number of results after fusion and graph expansion.")
    search.add_argument("--dense-k", type=int, default=30, help="Top-k dense hits before fusion.")
    search.add_argument("--bm25-k", type=int, default=30, help="Top-k BM25 hits before fusion.")
    search.add_argument("--dense-weight", type=float, default=1.0, help="Dense RRF weight.")
    search.add_argument("--bm25-weight", type=float, default=1.0, help="BM25 RRF weight.")
    search.add_argument("--rrf-k", type=int, default=60, help="RRF constant.")
    search.add_argument("--graph-hops", type=int, default=1, help="Optional graph expansion hops after dense+BM25 fusion.")
    search.add_argument("--graph-alpha", type=float, default=0.15, help="Graph expansion score decay factor.")
    search.add_argument("--doc-types", nargs="*", default=None, help="Optional doc type filter: evidence concept requirement section.")

    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "build":
        cmd_build(args)
    elif args.command == "search":
        cmd_search(args)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
