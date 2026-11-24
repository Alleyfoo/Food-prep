"""Count and sample RecipeNLG rows for part-level phrases via the HF filter API.

Read-only survey through a public mirror (Mahimas/recipenlg, 2,231,142 rows).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://datasets-server.huggingface.co/filter?dataset=Mahimas/recipenlg&config=default&split=train"
OUT = sys.argv[1] if __name__ == "__main__" else None

D = '"directions"'
I = '"ingredients"'

QUERIES = {
    # ---- tomato ----
    "tomato: in ingredients (baseline)": f"{I} ILIKE '%tomato%'",
    "tomato: 'concasse'": f"{D} ILIKE '%concass%' OR {I} ILIKE '%concass%'",
    "tomato: blanch + tomato in directions": f"{D} ILIKE '%blanch%' AND {D} ILIKE '%tomato%'",
    "tomato: score an X": f"{D} ILIKE '%tomato%' AND ({D} ILIKE '%an x %' OR {D} ILIKE '%an ''x''%' OR {D} ILIKE '%an \"x\"%' OR {D} ILIKE '%x-shaped%' OR {D} ILIKE '%shallow x%')",
    "tomato: 'tomato skin(s)'": f"{D} ILIKE '%tomato skin%' OR {I} ILIKE '%tomato skin%'",
    "tomato: peel tomatoes (directions)": f"{D} ILIKE '%peel the tomato%' OR {D} ILIKE '%peel tomato%' OR {D} ILIKE '%skin the tomato%' OR {D} ILIKE '%tomatoes peel%'",
    "tomato: peeled tomatoes (ingredients)": f"{I} ILIKE '%peeled%tomato%' OR {I} ILIKE '%tomato%peeled%'",
    "tomato: seeded (ingredients)": f"{I} ILIKE '%tomato%seeded%' OR {I} ILIKE '%seeded%tomato%'",
    "tomato: seed/deseed in directions": f"{D} ILIKE '%seed the tomato%' OR {D} ILIKE '%seed tomato%' OR {D} ILIKE '%tomato seeds%' OR {D} ILIKE '%squeeze out the seeds%'",
    "tomato: cored": f"{D} ILIKE '%core the tomato%' OR {D} ILIKE '%core tomato%' OR {I} ILIKE '%tomato%cored%' OR {I} ILIKE '%cored%tomato%'",
    "tomato: 'tomato water'": f"{D} ILIKE '%tomato water%' OR {I} ILIKE '%tomato water%'",
    "tomato: seeds/pulp/gel kept": f"{D} ILIKE '%reserve%seeds%' OR {D} ILIKE '%reserve the tomato%juice%' OR {D} ILIKE '%tomato pulp%' OR {D} ILIKE '%tomato gel%'",
    "tomato: skins dried or used": f"{D} ILIKE '%tomato skin%' AND ({D} ILIKE '%dehydrat%' OR {D} ILIKE '%powder%' OR {D} ILIKE '%crisp%' OR {D} ILIKE '%dry the skin%' OR {D} ILIKE '%rose%')",
    "tomato: grate (skin left behind)": f"{D} ILIKE '%grate%tomato%' AND {D} ILIKE '%skin%'",
    # ---- broccoli ----
    "broccoli: in ingredients (baseline)": f"{I} ILIKE '%broccoli%'",
    "broccoli: florets": f"{I} ILIKE '%broccoli floret%' OR {D} ILIKE '%broccoli floret%' OR {I} ILIKE '%broccoli flower%'",
    "broccoli: stems/stalks": f"{I} ILIKE '%broccoli stem%' OR {I} ILIKE '%broccoli stalk%' OR {D} ILIKE '%broccoli stem%' OR {D} ILIKE '%broccoli stalk%'",
    "broccoli: stems peeled": f"{D} ILIKE '%broccoli%' AND ({D} ILIKE '%peel the stem%' OR {D} ILIKE '%peel stem%' OR {D} ILIKE '%peel the stalk%' OR {D} ILIKE '%peel stalk%')",
    "broccoli: stems discarded": f"{D} ILIKE '%broccoli%' AND ({D} ILIKE '%discard%stem%' OR {D} ILIKE '%discard%stalk%' OR {D} ILIKE '%stems for another use%' OR {D} ILIKE '%reserve stems%' OR {D} ILIKE '%save the stems%')",
    "broccoli: 'broccoli slaw'": f"{I} ILIKE '%broccoli slaw%' OR {D} ILIKE '%broccoli slaw%'",
    "broccoli: leaves": f"{I} ILIKE '%broccoli lea%' OR {D} ILIKE '%broccoli lea%'",
    "broccoli: stems cooked first/longer": f"{D} ILIKE '%broccoli%' AND ({D} ILIKE '%stems first%' OR {D} ILIKE '%add the florets%' OR {D} ILIKE '%stalks first%')",
}


def get(where, length=8):
    url = f"{BASE}&where={urllib.parse.quote(where)}&length={length}"
    for attempt in range(40):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            d = json.loads(e.read() or b"{}")
        except Exception as e:  # noqa: BLE001
            d = {"error": str(e)}
        if "error" not in d:
            return d
        if "loading" in d["error"] or "timed out" in d["error"].lower():
            time.sleep(15)
            continue
        return d
    return {"error": "gave up"}


def sentence(text, keys):
    for s in re.split(r'",\s*"|\[\"|\"\]', text):
        if all(k in s.lower() for k in keys):
            return s.strip()[:260]
    return text[:200]


def main():
  out = {}
  for name, where in QUERIES.items():
    d = get(where)
    if "error" in d:
        out[name] = {"error": d["error"]}
        print(name, "ERROR", d["error"], flush=True)
        continue
    keys = [w for w in ("tomato", "broccoli") if w in name.split(":")[0]]
    samples = [{"title": r["row"]["title"],
                "line": sentence(r["row"]["directions"] + r["row"]["ingredients"], keys)}
               for r in d["rows"]]
    out[name] = {"count": d["num_rows_total"], "samples": samples}
    print(f"{name:45} {d['num_rows_total']:8}", flush=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
