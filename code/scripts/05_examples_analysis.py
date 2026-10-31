"""Query statistics, transliteration vocabulary coverage, and example query -> retrieved-doc outputs."""
import sys, pathlib, json
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from tanglish_rag.retrievers import word_tokens, BM25, char_ngrams, topk
from tanglish_rag.normalise import is_english
corpus = pd.read_json("data/corpus.jsonl", lines=True); q = pd.read_json("data/queries.jsonl", lines=True)
vocab = set(w for t in corpus.text_ta for w in word_tokens(t))
stats = []
for name, c in [("English", "query_en"), ("Tamil script", "query_ta"), ("Romanised", "query_ta_romanized"),
                ("Code-mixed", "query_ta_codemix"), ("Rom -> ITRANS", "rom_itrans"), ("Rom -> rules", "rom_rules"),
                ("CM -> ITRANS", "cm_itrans"), ("CM -> rules", "cm_rules")]:
    toks = [word_tokens(x) for x in q[c]]
    flat = [t for ts in toks for t in ts]
    latin = [t for t in flat if t.isascii() and t.isalpha()]
    tamil = [t for t in flat if any("\u0B80" <= ch <= "\u0BFF" for ch in t)]
    stats.append({"query_set": name, "avg_tokens": np.mean([len(t) for t in toks]),
                  "pct_latin_tokens": 100 * len(latin) / len(flat),
                  "pct_latin_detected_english": 100 * np.mean([is_english(t) for t in latin]) if latin else 0,
                  "pct_tamil_tokens_in_corpus_vocab": 100 * np.mean([t in vocab for t in tamil]) if tamil else float("nan")})
st = pd.DataFrame(stats).round(1); st.to_csv("results/query_stats.csv", index=False); print(st.to_string())
cs = corpus.text_ta.str.len(); print("doc chars mean/median/max", cs.mean().round(1), cs.median(), cs.max())
pd.DataFrame([{"docs": len(corpus), "queries_per_variant": len(q), "doc_chars_mean": round(cs.mean(), 1),
               "doc_chars_median": cs.median(), "doc_chars_max": cs.max()}]).to_csv("results/dataset_stats.csv", index=False)

# examples: dense e5 + BM25-char3 top-3 for chosen queries
D = np.load("results/cache/multilingual-e5-small/docs_ta.npy")
QE = {s: np.load(f"results/cache/multilingual-e5-small/{s}.npy") for s in ("en", "ta", "rom", "cm", "rom_rules", "cm_rules")}
bc = BM25(corpus.text_ta.tolist(), char_ngrams)
pq = pd.read_csv("results/per_query.csv")
d_rom = pq[(pq.corpus == "ta") & (pq.query_set == "rom") & (pq.retriever == "Dense-e5")].set_index("qid")["rank"]
d_rr = pq[(pq.corpus == "ta") & (pq.query_set == "rom_rules") & (pq.retriever == "Dense-e5")].set_index("qid")["rank"]
# pick: 2 where normalisation rescued, 1 where it still failed (seeded), short queries for readability
q["len"] = q.query_ta_romanized.str.len()
short = q[q.len < 60]
rescued = short[short.qid.map(lambda x: d_rom[x] == -1 and d_rr[x] == 1)].sample(2, random_state=3)
failed = short[short.qid.map(lambda x: d_rr[x] == -1)].sample(1, random_state=3)
ex = []
def snip(t, n=110): return t[:n].replace("\n", " ") + ("…" if len(t) > n else "")
for _, r in pd.concat([rescued, failed]).iterrows():
    i = int(r.name); gold = r.doc_id
    item = {"qid": r.qid, "gold_doc_en_gloss": snip(corpus.set_index("doc_id").text_en[gold], 140), "variants": []}
    for s, c in [("en", "query_en"), ("ta", "query_ta"), ("rom", "query_ta_romanized"), ("rom_rules", "rom_rules"),
                 ("cm", "query_ta_codemix"), ("cm_rules", "cm_rules")]:
        top = topk(D @ QE[s][i], 3)
        item["variants"].append({"set": s, "query": r[c], "dense_top3": [
            {"rank": k + 1, "correct": corpus.doc_id[j] == gold, "doc_ta": snip(corpus.text_ta[j], 70)} for k, j in enumerate(top)],
            "dense_rank_of_gold": int(pq[(pq.corpus=="ta")&(pq.query_set==s)&(pq.retriever=="Dense-e5")&(pq.qid==r.qid)]["rank"].iloc[0])})
    ex.append(item)
json.dump(ex, open("results/examples.json", "w"), ensure_ascii=False, indent=1)
for e in ex:
    print("\n==", e["qid"], "|", e["gold_doc_en_gloss"])
    for v in e["variants"]:
        print(f"  [{v['set']}] {v['query']}  -> gold rank {v['dense_rank_of_gold']}; top1 correct={v['dense_top3'][0]['correct']}")

# how "code-mixed" are the code-mixed queries?
def n_tamil_tokens(s): return sum(1 for t in word_tokens(s) if t.isascii() and t.isalpha() and not is_english(t))
same = (q.query_ta_codemix.str.lower().str.strip() == q.query_en.str.lower().str.strip()).mean()
zero = (q.query_ta_codemix.map(n_tamil_tokens) == 0).mean()
cmq = pd.DataFrame([{"cm_identical_to_en_pct": round(100 * same, 1), "cm_with_no_tamil_token_pct": round(100 * zero, 1),
                     "cm_mean_tamil_tokens": round(q.query_ta_codemix.map(n_tamil_tokens).mean(), 2),
                     "rom_mean_tamil_tokens": round(q.query_ta_romanized.map(n_tamil_tokens).mean(), 2)}])
cmq.to_csv("results/codemix_audit.csv", index=False); print(cmq.to_string())
