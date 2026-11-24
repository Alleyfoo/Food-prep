"""Sentence-level precision for the RecipeNLG probe, plus used-vs-removed classes.

For each query: fetch up to 100 matching rows, split directions and ingredient
lines into sentences, and check whether one sentence carries the pattern.
"""
import json
import re
import sys

sys.path.insert(0, ".")
_src = open("nlg_probe.py", encoding="utf-8").read().split("def main")[0]
exec(_src)  # QUERIES and get()

# A single sentence must match this for the row to count.
SENTENCE = {
    "tomato: 'concasse'": r"concass",
    "tomato: blanch + tomato in directions": r"(blanch|scald|boiling water).*tomato|tomato.*(blanch|scald|boiling water)",
    "tomato: score an X": r"tomato.*\b(an|small|shallow) ['\"]?x['\"]?\b|\bx\b.*tomato|x-shaped",
    "tomato: peel tomatoes (directions)": r"(peel|skin)(ed)? (the )?tomato|tomato(es)?,? peel",
    "tomato: peeled tomatoes (ingredients)": r"peeled.*tomato|tomato.*peeled",
    "tomato: seeded (ingredients)": r"seeded.*tomato|tomato.*seeded",
    "tomato: cored": r"\bcore(d)?\b.*tomato|tomato.*\bcored?\b",
    "tomato: 'tomato skin(s)'": r"tomato skin",
    "tomato: grate (skin left behind)": r"grate.*tomato.*skin|tomato.*grate.*skin|grat.*(discard|left).*skin",
    "broccoli: stems/stalks": r"broccoli (stem|stalk)|(stem|stalk)s? of (the )?broccoli",
    "broccoli: stems peeled": r"peel.*(stem|stalk)",
    "broccoli: stems discarded": r"discard.*(stem|stalk)|(stem|stalk).*discard|(stem|stalk)s? for another use",
    "broccoli: leaves": r"broccoli lea",
}

# What happens to the part in the matched sentence.
REMOVED = re.compile(r"discard|throw away|remove|peel (away|off)|slip off|cut (off|out)|trim off|squeeze out|scoop out", re.I)
CANNED = re.compile(r"\bcans?\b|canned|\boz\b|ounce|\bpkg\b|package", re.I)


def sentences(row):
    text = row["directions"] + " " + row["ingredients"]
    parts = re.split(r'",\s*"|\["|"\]|(?<=[.;])\s+', text)
    return [p.strip() for p in parts if p.strip()]


out = {}
for name, pat in SENTENCE.items():
    d = get(QUERIES[name], length=100)
    if "error" in d:
        print(name, "ERROR", d["error"])
        continue
    rx = re.compile(pat, re.I)
    hits, removed, canned, examples = 0, 0, 0, []
    for r in d["rows"]:
        m = [s for s in sentences(r["row"]) if rx.search(s)]
        if not m:
            continue
        hits += 1
        s = m[0]
        removed += bool(REMOVED.search(s))
        canned += bool(CANNED.search(s))
        if len(examples) < 8:
            examples.append(f"{r['row']['title']} | {s[:220]}")
    n = len(d["rows"])
    prec = hits / n if n else 0
    out[name] = {"rows_total": d["num_rows_total"], "sampled": n, "precision": round(prec, 2),
                 "estimated_true": round(d["num_rows_total"] * prec),
                 "share_removed": round(removed / hits, 2) if hits else None,
                 "share_canned": round(canned / hits, 2) if hits else None,
                 "examples": examples}
    print(f"{name:45} total {d['num_rows_total']:7}  precision {prec:.2f}  ~{out[name]['estimated_true']:6}"
          f"  removed {out[name]['share_removed']}  canned {out[name]['share_canned']}", flush=True)
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
