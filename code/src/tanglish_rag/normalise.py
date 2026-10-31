"""Tanglish query normalisation: romanised Tamil -> Tamil script.

Two transliterators are compared:
  * itrans : off-the-shelf `indic-transliteration` (ITRANS scheme -> Tamil). Designed for a
             formal Sanskrit-style romanisation, not for how people actually type Tanglish.
  * rules  : a small hand-written Tanglish rule mapper (this project), encoding common
             informal conventions: zh->ழ, th/dh->த, tr->ற்ற, ndr->ன்ற, word-initial n->ந,
             medial n->ன, doubled consonants -> geminate with pulli, ee->ீ, oo->ூ, ai->ை, etc.

For code-mixed queries only the tokens judged to be Tamil are transliterated; tokens judged
to be English (frequent English words per `wordfreq`, minus a list of Tanglish particles)
are kept as they are.
"""
from __future__ import annotations
import re
from functools import lru_cache

# ---------------------------------------------------------------- language id per token
TANGLISH_FUNCTION_WORDS = {
    # particles / case markers / common verbs that collide with English or are short
    "la", "le", "ku", "kku", "ah", "a", "o", "nu", "na", "oda", "ode", "um", "dhan", "than",
    "thaan", "enna", "yen", "en", "epdi", "eppadi", "eppo", "enga", "engae", "yaar", "yaaru",
    "pathi", "patthi", "panni", "pannu", "panna", "pannanum", "irukku", "iruku", "illa",
    "illai", "sonnaru", "sonnar", "kudukka", "kuduthathu", "evlo", "evvalavu", "edhu", "ethu",
    "romba", "ana", "aana", "vandhu", "poi", "po", "va", "vaa", "kidaikkum", "mudiyum",
    "venum", "vendum", "nalla", "pesunathu", "kitta", "kooda", "mattum", "ellam",
}

@lru_cache(maxsize=None)
def is_english(token: str) -> bool:
    t = token.lower()
    if not re.fullmatch(r"[a-z]+", t):
        return False  # digits, punctuation, mixed -> leave to caller
    if t in TANGLISH_FUNCTION_WORDS:
        return False
    from wordfreq import zipf_frequency
    return zipf_frequency(t, "en") >= 3.0

# ---------------------------------------------------------------- ITRANS baseline
def itrans_word(word: str) -> str:
    from indic_transliteration import sanscript
    return sanscript.transliterate(word.lower(), sanscript.ITRANS, sanscript.TAMIL)

# ---------------------------------------------------------------- rule-based Tanglish mapper
PULLI = "\u0BCD"
INDEP = {"aa": "ஆ", "ii": "ஈ", "ee": "ஈ", "uu": "ஊ", "oo": "ஊ", "ai": "ஐ", "au": "ஔ",
         "ae": "ஏ", "a": "அ", "i": "இ", "u": "உ", "e": "எ", "o": "ஒ"}
SIGN = {"aa": "ா", "ii": "ீ", "ee": "ீ", "uu": "ூ", "oo": "ூ", "ai": "ை", "au": "ௌ",
        "ae": "ே", "a": "", "i": "ி", "u": "ு", "e": "ெ", "o": "ொ"}
VOWELS = sorted(SIGN, key=len, reverse=True)
# consonant clusters, longest first. Value is Tamil consonant(s) WITHOUT a final pulli;
# inner pullis are explicit.
CONS = [
    ("ndr", "ன்ற"), ("nth", "ந்த"), ("ndh", "ந்த"), ("nch", "ஞ்ச"), ("ngk", "ங்க"),
    ("tch", "ட்ச"), ("ksh", "க்ஷ"),
    ("zh", "ழ"), ("sh", "ஷ"), ("ch", "ச"), ("th", "த"), ("dh", "த"), ("tr", "ற்ற"),
    ("rr", "ற்ற"), ("nn", "ன்ன"), ("ng", "ங்க"), ("nj", "ஞ்ச"), ("ny", "ஞ"), ("nd", "ண்ட"),
    ("nt", "ண்ட"), ("kh", "க"), ("gh", "க"), ("bh", "ப"), ("ph", "ப"), ("x", "க்ஸ"),
    ("k", "க"), ("g", "க"), ("c", "க"), ("q", "க"), ("j", "ஜ"), ("s", "ச"), ("h", "ஹ"),
    ("t", "ட"), ("d", "ட"), ("p", "ப"), ("b", "ப"), ("f", "ப"), ("m", "ம"), ("y", "ய"),
    ("r", "ர"), ("l", "ல"), ("v", "வ"), ("w", "வ"), ("z", "ஜ"), ("n", "ன"),
]

def rules_word(word: str) -> str:
    w = word.lower()
    out, i, prev_cons = [], 0, False
    while i < len(w):
        ch = w[i]
        if not ch.isalpha():
            if prev_cons:
                out.append(PULLI)
            out.append(ch); prev_cons = False; i += 1
            continue
        # vowel
        v = next((v for v in VOWELS if w.startswith(v, i)), None)
        if v is not None:
            out.append(SIGN[v] if prev_cons else INDEP[v])
            prev_cons = False; i += len(v)
            continue
        if prev_cons:
            out.append(PULLI)
        # doubled single consonant -> geminate (kk, pp, tt, mm, ll, ss, cc ...)
        if i + 1 < len(w) and w[i + 1] == ch and ch not in "rn":
            base = dict(CONS).get(ch, ch)
            out.append(base + PULLI + base); i += 2; prev_cons = True
            continue
        pat, tam = next(((p, t) for p, t in CONS if w.startswith(p, i)), (ch, ch))
        if pat == "n" and i == 0:
            tam = "ந"                     # word-initial n is dental
        if pat in ("nd", "nt") and i == 0:
            tam = "ந்த"
        out.append(tam); i += len(pat); prev_cons = True
    if prev_cons:
        out.append(PULLI)
    return "".join(out)

# ---------------------------------------------------------------- query-level API
TOKEN = re.compile(r"[A-Za-z]+|[^A-Za-z]+")

def normalise(query: str, scheme: str = "rules", keep_english: bool = True) -> str:
    """Transliterate the Tamil (romanised) tokens of a query to Tamil script.
    keep_english=True keeps tokens detected as English (for code-mixed queries)."""
    fn = rules_word if scheme == "rules" else itrans_word
    parts = []
    for tok in TOKEN.findall(query):
        if tok[0].isalpha() and not (keep_english and is_english(tok)):
            parts.append(fn(tok))
        else:
            parts.append(tok)
    return "".join(parts)

if __name__ == "__main__":
    for q in ["Kizhaku maagana payitrapatta aasiriyar tharam 3 paritchai nilai",
              "scholarship ku last date enna?", "Israel Hamas conflict ku yaar responsible",
              "Annamalai palkalaikazhagam kurithu uyarkalvithurai amaichar Ponmudi",
              "karbhinigal seyarkai kulirpanangal kudikkalama"]:
        print(q, "\n  rules :", normalise(q, "rules"), "\n  itrans:", normalise(q, "itrans"))
