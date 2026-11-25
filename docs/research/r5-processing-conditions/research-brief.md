# R5 research brief for evidence agents (shared part)

Project: Food-prep, a local Python culinary knowledge model. Research round R5
asks: for the steps that documented dishes use, what do you actually need to
do: under which conditions, for how long (elapsed AND active work), how you
know it is done, and how you know it failed. We record documented practice;
we do not predict or simulate.

Repo (read-only for you except your one output file):
C:\Users\pertt\food-prep\.claude\worktrees\r5-processing-conditions-e51e0f
- docs/research/r5-processing-conditions/pair-selection.md: the 25 pairs.
- Earlier evidence you may cite instead of re-reading (already contains
  conditions): docs/research/r2-construction-patterns/recipes.md (R2 ids like
  E1a, M2b, A3a), docs/research/r4-transfers/evidence-*.md (R4 ids like P4,
  G7, N10, O5, B1). Use them; do not re-fetch those URLs unless you need a
  detail they lack.

## Rules
1. Multilingual. Search in the original language of each dish tradition and
   in Finnish (Finnish home sources: Kotikokki, K-Ruoka, Valio, Yhteishyvä/
   S-kaupat, Marttaliitto/martat.fi, Kotiliesi, Maku; Swedish: ICA, Arla,
   Coop; German: Chefkoch is blocked for fetch, use others). English-only
   search creates false gaps.
2. Read pages. Use WebSearch to find, then WebFetch (or the web-fetch agent)
   to read. A page seen only as a search snippet is NOT evidence; list it as
   failed/snippet-only. Never invent or guess a URL. Record every URL you
   actually read, and every page that failed (404, blocked, paywall, empty).
3. Paraphrase. No recipe text copied. Quotes at most 15 words, and only for
   the endpoint wording (e.g. the exact "crushes between fingers" phrase),
   marked as quotes.
4. What to extract, per source, only where it is stated:
   - starting state (whole/split/sliced/grated thickness; dry/soaked);
   - medium and heat (boiling salted water, simmer, oven C, covered/uncovered,
     oil temperature, pan heat);
   - elapsed time as stated (ranges as given);
   - active work: is it hands-on continuously, regular attention (stirring,
     turning), occasional (change water once), or none (waiting)? only if the
     source makes it clear (e.g. "leave overnight", "stir constantly");
   - what shifts the time (age, variety, piece size, soaking, altitude, hard
     water, salt) as the source says;
   - OBSERVABLE completion conditions (primary; time is only a guide):
     e.g. "a knife meets slight resistance", "crushes between the fingers",
     "doubled in size", "floats", "water comes out";
   - OBSERVABLE failure conditions and their stated cause: hard centre,
     layers slip, mushy, falls apart in oil, dry crumbly, burnt edges;
   - how long an intermediate keeps and how (fridge, covered, frozen), if
     the page states it.
5. Keep conflicts. If two sources disagree, record both with ids. Do not
   average or reconcile.
6. Do not use your own culinary knowledge as evidence. If nothing is found,
   say "not found" and list the searches tried (query + language).
7. Every source gets an id from YOUR range, a heading line exactly like:
   `### Q101 — https://example.org/page`
   followed by bullet lines: language and country; publisher type
   (public body, magazine, brand/packet, cooking school, personal blog,
   user-submitted); date if shown; how read (WebFetch summary / raw text);
   then the extracted conditions with the pair id(s) they support.
8. Date read: 2026-11-25.

## Output file structure (write exactly this, in your one file)
# Evidence: <title>
(date, method, search languages, any traps)
## Sources
### Qnnn — URL
- ...
## Failed pages and snippet-only
| URL or query | why |
## Searches
| language | query | useful? |
## Synthesis per pair
For each pair in your group:
### <pair id>
- steps: (from pair-selection.md)
- start: particle / moisture
- medium and heat: versions with ids
- elapsed: versions with ids (keep each source's own range)
- active: kind (continuous | regular | occasional | none) with ids, or unknown
- shifts: factor: effect [ids]
- completion: each observable condition [ids]
- failure: each observable condition + stated cause [ids]
- by role: if the same part+operation has a different endpoint in another
  dish role, say so [ids]
- conflicts: the disagreement, each side with ids
- keeps: how long the resulting intermediate keeps and how [ids], or not found
- confidence: established (3+ independent sources agree) | documented (1-2) |
  conflicting | not found
- gaps: what you looked for and could not find

When done, reply with a short summary (pairs covered, how many sources,
biggest conflicts, what was not found). Keep the reply under 300 words.
