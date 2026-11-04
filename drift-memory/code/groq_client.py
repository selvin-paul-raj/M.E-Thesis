"""Throttled, cached Groq chat client for DriftBench.

Free tier: 8,000 tokens/min and 1,000 requests/day per model. Every call is
cached by sha256(model, messages, max_tokens, temperature) in
results/cache/<model>.jsonl, so reruns are free. The API key is injected by
the environment proxy; this file never reads or prints it.
"""
import hashlib, json, os, time, pathlib, threading, urllib.request, urllib.error

URL = "https://api.groq.com/openai/v1/chat/completions"
NV_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
_FALLBACK = set()  # models switched to NVIDIA after Groq daily cap
ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
TPM = 7000          # stay under 8,000 tokens/min
_windows = {}       # model -> [(timestamp, tokens)]  (limits are per model)
_lock = threading.Lock()
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


def _throttle(model, est):
    while True:
        with _lock:
            w = _windows.setdefault(model, [])
            now = time.time()
            while w and now - w[0][0] > 60:
                w.pop(0)
            used = sum(t for _, t in w)
            if used + est <= TPM or not w:
                slot = [now, est]  # reserve; corrected to real usage after the call
                w.append(slot)
                return slot
            wait = max(0.0, 60 - (now - w[0][0])) + 0.5
        time.sleep(wait)


def _retry_secs(msg):
    """Parse Groq's 'try again in 5m44.3s' into seconds (None if absent)."""
    import re as _r
    m = _r.search(r"try again in (?:(\d+)h)?(?:(\d+)m)?(?:([\d.]+)s)?", msg)
    if not m or not any(m.groups()): return None
    h, mi, se = (float(x) if x else 0.0 for x in m.groups())
    return h * 3600 + mi * 60 + se


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
    for attempt in range(10):
        slot = _throttle(model, est)
        url = NV_URL if model in _FALLBACK else URL
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "driftbench/0.1 (curl-compatible)"})
        try:
            with urllib.request.urlopen(req, timeout=90 if model in _FALLBACK else 300) as r:
                body = json.loads(r.read())
            text = body["choices"][0]["message"].get("content") or ""
            import re as _re; text = _re.sub(r"<think>.*?</think>", "", text, flags=_re.S).strip()
            usage = body.get("usage", {})
            slot[1] = usage.get("total_tokens", est)
            rec = {"key": key, "model": model, "text": text, "usage": usage, "provider": "nvidia" if model in _FALLBACK else "groq"}
            with _lock, _cache_file(model).open("a") as f:
                f.write(json.dumps(rec) + "\n")
            cache[key] = rec
            return text, usage
        except (ConnectionError, TimeoutError, urllib.error.URLError) as e:
            if isinstance(e, urllib.error.HTTPError): raise_http = e
            else:
                time.sleep(min(10 * (attempt + 1), 60)); continue
            e = raise_http
            if e.code == 429 or e.code >= 500:
                wait = float(e.headers.get("retry-after", 0) or 0) or 5 * (attempt + 1)
                msg = e.read().decode(errors="ignore") if e.code == 429 else ""
                if e.code == 429 and model not in _FALLBACK and ("per day" in msg.lower()):
                    w = _retry_secs(msg)
                    if w is not None and w <= 900:   # short TPD refill: wait on Groq instead of the fallback
                        time.sleep(w + 5); continue
                    if os.environ.get("NO_FALLBACK"):
                        raise RuntimeError(f"daily limit (tokens per day) reached for {model}; retry in {w}s")
                    _FALLBACK.add(model); continue
                time.sleep(min(wait, 120)); continue
            raise
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = float(e.headers.get("retry-after", 0) or 0) or 5 * (attempt + 1)
                msg = e.read().decode(errors="ignore") if e.code == 429 else ""
                if e.code == 429 and model not in _FALLBACK and ("per day" in msg.lower()):
                    w = _retry_secs(msg)
                    if w is not None and w <= 900:   # short TPD refill: wait on Groq instead of the fallback
                        time.sleep(w + 5); continue
                    if os.environ.get("NO_FALLBACK"):
                        raise RuntimeError(f"daily limit (tokens per day) reached for {model}; retry in {w}s")
                    _FALLBACK.add(model); continue
                if e.code == 429 and model in _FALLBACK and attempt > 8:
                    raise RuntimeError(f"daily limit (requests or tokens per day) reached for {model}")
                time.sleep(min(wait, 120))
                continue
            raise
    raise RuntimeError(f"LLM call failed after retries ({model})")


if __name__ == "__main__":
    t, u = chat("openai/gpt-oss-20b", [{"role": "user", "content": "Reply with the single word OK."}], max_tokens=50)
    print(repr(t), u.get("total_tokens"))
    t2, _ = chat("openai/gpt-oss-20b", [{"role": "user", "content": "Reply with the single word OK."}], max_tokens=50)
    print("cache hit:", t == t2)
