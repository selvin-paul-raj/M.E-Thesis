"""Encode corpus + every query set with a dense model; cache to results/cache/<model>/<name>.npy.
Usage: python scripts/02_encode_dense.py [model] [set ...]   (sets: docs_ta docs_en en ta rom cm rom_itrans ...)"""
import sys, pathlib, time
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from tanglish_rag.retrievers import Dense
torch.set_num_threads(2)
model = sys.argv[1] if len(sys.argv) > 1 else "intfloat/multilingual-e5-small"
cache = pathlib.Path("results/cache") / model.split("/")[-1]; cache.mkdir(parents=True, exist_ok=True)
corpus = pd.read_json("data/corpus.jsonl", lines=True); q = pd.read_json("data/queries.jsonl", lines=True)
COL = {"en": "query_en", "ta": "query_ta", "rom": "query_ta_romanized", "cm": "query_ta_codemix",
       "rom_itrans": "rom_itrans", "rom_rules": "rom_rules", "cm_itrans": "cm_itrans", "cm_rules": "cm_rules"}
sets = sys.argv[2:] or ["docs_ta", "docs_en", *COL]
enc = Dense(model)
for s in sets:
    f = cache / f"{s}.npy"
    if f.exists():
        print("cached", s); continue
    t = time.time()
    if s.startswith("docs_"):
        E = enc.encode_docs(corpus[f"text_{s[5:]}"].tolist())
    else:
        E = enc.encode_queries(q[COL[s]].tolist())
    np.save(f, E.astype(np.float32)); print(s, E.shape, f"{time.time()-t:.1f}s", flush=True)
