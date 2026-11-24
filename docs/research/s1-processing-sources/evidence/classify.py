import re, sys
exec(open("nlg_probe.py",encoding="utf-8").read().split("def main")[0])
for name, rx in (("tomato: 'tomato skin(s)'", r"tomato skin"), ("broccoli: leaves", r"broccoli lea"), ("broccoli: stems/stalks", r"broccoli (stem|stalk)")):
    d = get(QUERIES[name], length=100)
    sents=[]
    for r in d["rows"]:
        t=r["row"]["directions"]+" "+r["row"]["ingredients"]
        for s in re.split(r'",\s*"|\["|"\]|(?<=[.;])\s+', t):
            if re.search(rx,s,re.I): sents.append(s.strip()); break
    cls={"removed":r"remov|discard|peel|slip|\boff\b|pull|trim",
         "cooking cue":r"split|blister|wrinkl|crack|burst|char|blacken|loosen",
         "used":r"rose|garnish|with skin|skin on|^\d|chopped|diced|slic|cook|saute|add|steam|stir|toss"}
    print("##",name,len(sents))
    counts={k:0 for k in cls}; other=[]
    for s in sents:
        for k,p in cls.items():
            if re.search(p,s,re.I): counts[k]+=1; break
        else: other.append(s)
    print(counts, "other", len(other))
    for s in other[:5]: print("   other:", s[:160])
