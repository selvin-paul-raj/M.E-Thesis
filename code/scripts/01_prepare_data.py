"""Download nlpctx/tamil-english-retrieval, sample 500 docs (seed 42), normalise Tanglish queries."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from tanglish_rag.data import load_raw, build_subset, save_jsonl
from tanglish_rag.normalise import normalise

out = pathlib.Path("data"); out.mkdir(exist_ok=True)
df = load_raw(str(out / "hf"))
corpus, q = build_subset(df, n_docs=int(sys.argv[1]) if len(sys.argv) > 1 else 500)
t = time.time()
for src in ("query_ta_romanized", "query_ta_codemix"):
    tag = "rom" if "roman" in src else "cm"
    for scheme in ("itrans", "rules"):
        q[f"{tag}_{scheme}"] = [normalise(x, scheme) for x in q[src]]
norm_ms = (time.time() - t) / (4 * len(q)) * 1000
save_jsonl(corpus, out / "corpus.jsonl"); save_jsonl(q, out / "queries.jsonl")
print(f"docs={len(corpus)} queries={len(q)} full_dataset_docs={df.doc_id.nunique()} rows={len(df)}")
print(f"mean normalisation time per query: {norm_ms:.3f} ms")
(pathlib.Path("results") / "normalisation_latency_ms.txt").write_text(f"{norm_ms:.4f}\n")
