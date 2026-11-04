"""Throttled, cached Groq chat client for DriftBench.

Free tier: 8,000 tokens/min and 1,000 requests/day per model. Every call is
cached by sha256(model, messages, max_tokens, temperature) in
results/cache/<model>.jsonl, so reruns are free. The API key is injected by
the environment proxy; this file never reads or prints it.
"""
import hashlib, json, os, time, pathlib, urllib.request, urllib.error

URL = "https://api.groq.com/openai/v1/chat/completions"
ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
TPM = 7000          # stay under 8,000 tokens/min
_window = []        # (timestamp, tokens)
_mem = {}


def _cache_file(model):
    return CACHE / (model.replace("/", "_") + ".jsonl")


def _load(model):
    if model in _mem:
        return _mem[model]
    d = {}
    f = _cache_file(model)
    if f.exists():
        for line in f.open():
            try:
                r = json.loads(line); d[r["key"]] = r
            except Exception:
                pass
    _mem[model] = d
    return d


def _throttle(est):
    now = time.time()
    while _window and now - _window[0][0] > 60:
        _window.pop(0)
    used = sum(t for _, t in _window)
    if used + est > TPM and _window:
        time.sleep(max(0.0, 60 - (now - _window[0][0])) + 0.5)
        return _throttle(est)


def chat(model, messages, max_tokens=512, temperature=0.0, reasoning_effort="low"):
    """Return (text, usage dict). Cached; retries on 429/5xx."""
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens,
               "temperature": temperature}
    if model.startswith("openai/gpt-oss"):
        payload["reasoning_effort"] = reasoning_effort
    key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    cache = _load(model)
    if key in cache:
        return cache[key]["text"], cache[key]["usage"]
    est = sum(len(m["content"]) for m in messages) // 3 + max_tokens
    for attempt in range(6):
        _throttle(est)
        req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "driftbench/0.1 (curl-compatible)"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = json.loads(r.read())
            text = body["choices"][0]["message"].get("content") or ""
            usage = body.get("usage", {})
            _window.append((time.time(), usage.get("total_tokens", est)))
            rec = {"key": key, "model": model, "text": text, "usage": usage}
            with _cache_file(model).open("a") as f:
                f.write(json.dumps(rec) + "\n")
            cache[key] = rec
            return text, usage
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = float(e.headers.get("retry-after", 0) or 0) or 5 * (attempt + 1)
                if e.code == 429 and "requests per day" in e.read().decode(errors="ignore").lower():
                    raise RuntimeError(f"daily request limit reached for {model}")
                time.sleep(min(wait, 120))
                continue
            raise
    raise RuntimeError(f"Groq call failed after retries ({model})")


if __name__ == "__main__":
    t, u = chat("openai/gpt-oss-20b", [{"role": "user", "content": "Reply with the single word OK."}], max_tokens=50)
    print(repr(t), u.get("total_tokens"))
    t2, _ = chat("openai/gpt-oss-20b", [{"role": "user", "content": "Reply with the single word OK."}], max_tokens=50)
    print("cache hit:", t == t2)
