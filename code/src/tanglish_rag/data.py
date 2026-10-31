"""Build the evaluation subset from nlpctx/tamil-english-retrieval."""
from __future__ import annotations
import json, random
from pathlib import Path
import pandas as pd

VARIANTS = {"en": "query_en", "ta": "query_ta", "rom": "query_ta_romanized", "cm": "query_ta_codemix"}

def load_raw(cache_dir: str = "data") -> pd.DataFrame:
    from huggingface_hub import hf_hub_download
    p = hf_hub_download("nlpctx/tamil-english-retrieval", "final_dataset.parquet",
                        repo_type="dataset", local_dir=cache_dir)
    return pd.read_parquet(p)

def build_subset(df: pd.DataFrame, n_docs: int = 500, seed: int = 42):
    """Sample n_docs documents (seeded) and keep every query row generated for them.
    Each query has exactly one relevant document (its source doc_id)."""
    doc_ids = sorted(df.doc_id.unique())
    random.Random(seed).shuffle(doc_ids)
    keep = set(doc_ids[:n_docs])
    sub = df[df.doc_id.isin(keep)].reset_index(drop=True)
    corpus = (sub.drop_duplicates("doc_id")[["doc_id", "text", "english_doc", "char_count"]]
              .rename(columns={"text": "text_ta", "english_doc": "text_en"}).reset_index(drop=True))
    queries = sub[["doc_id", *VARIANTS.values(), "answer_text"]].copy()
    queries.insert(0, "qid", [f"q{i:05d}" for i in range(len(queries))])
    return corpus, queries

def save_jsonl(df: pd.DataFrame, path: str | Path):
    with open(path, "w", encoding="utf-8") as f:
        for r in df.to_dict("records"):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def load_jsonl(path: str | Path) -> pd.DataFrame:
    return pd.read_json(path, lines=True)
