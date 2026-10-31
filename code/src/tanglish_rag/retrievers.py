"""Retrievers: BM25 (word / char n-gram), dense multilingual-e5, hybrid RRF.
Mirrors ChunkLab's retrieval module (BM25, dense, hybrid RRF with k=60) as plain functions."""
from __future__ import annotations
import re
import numpy as np
from rank_bm25 import BM25Okapi

WORD = re.compile(r"[0-9A-Za-z\u0B80-\u0BFF]+")

def word_tokens(text: str) -> list[str]:
    return [t.lower() for t in WORD.findall(text)]

def char_ngrams(text: str, n: int = 3) -> list[str]:
    grams = []
    for w in word_tokens(text):
        w = f"#{w}#"
        grams += [w[i:i + n] for i in range(max(1, len(w) - n + 1))]
    return grams

class BM25:
    def __init__(self, docs: list[str], tokenizer=word_tokens):
        self.tok = tokenizer
        self.bm25 = BM25Okapi([tokenizer(d) for d in docs])
    def scores(self, query: str) -> np.ndarray:
        return self.bm25.get_scores(self.tok(query))

class Dense:
    """multilingual-e5 style encoder: 'query: ' / 'passage: ' prefixes, cosine via normalised dot."""
    def __init__(self, model_name: str = "intfloat/multilingual-e5-small"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name, device="cpu")
        self.e5 = "e5" in model_name
    def encode_queries(self, qs, bs=64):
        qs = [("query: " + q) if self.e5 else q for q in qs]
        return self.model.encode(qs, batch_size=bs, normalize_embeddings=True, show_progress_bar=False)
    def encode_docs(self, ds, bs=16):
        ds = [("passage: " + d) if self.e5 else d for d in ds]
        return self.model.encode(ds, batch_size=bs, normalize_embeddings=True, show_progress_bar=False)

def topk(scores: np.ndarray, k: int = 100) -> np.ndarray:
    k = min(k, len(scores))
    idx = np.argpartition(-scores, k - 1)[:k]
    return idx[np.argsort(-scores[idx], kind="stable")]

def topk_positive(scores: np.ndarray, k: int = 100) -> np.ndarray:
    """Top-k restricted to documents with a positive score.
    rank-bm25 gives every non-matching document a score of exactly 0; ranking those by
    array index (the argsort tie-break) is arbitrary and must not be fed into fusion."""
    idx = topk(scores, k)
    return idx[scores[idx] > 0]

def rrf(rank_lists: list[np.ndarray], k: int = 60, depth: int = 100) -> np.ndarray:
    fused: dict[int, float] = {}
    for ranks in rank_lists:
        for r, d in enumerate(ranks[:depth]):
            fused[int(d)] = fused.get(int(d), 0.0) + 1.0 / (k + r + 1)
    return np.array(sorted(fused, key=lambda d: -fused[d]))
