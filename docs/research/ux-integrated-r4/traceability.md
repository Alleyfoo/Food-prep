# Evidence traceability and relationship navigation

## What the database actually records

From the built database, read-only:

| | Links | Claim scope recorded | Notes |
| --- | --- | --- | --- |
| Transformation → source | 75 | **75 of 75** | For example, steamed broccoli is backed by *steam_culinary*, scope "steamed broccoli with butter/lemon/cheese" |
| Pairing → source | 288 | **0 of 288** | `pairing_evidence.claim_scope` is empty on every row |
| Route → source | no table | n/a | Routes carry an `attestation` level instead |
| Experimental pairings → source | 0 | n/a | None of the 16 has a source |

There are 12 sources:
- **Datasets:** recipedb, mmres, flavordb.
- **Official:** nchfp, usda_tomato.
- **Culinary references:** caprese, pico, pappa, pomodoro, roast_culinary, steam_culinary, nordic_root.

Each source has a title, a type, a licence and a short `citation_text`.
Pairing links use 9 of them; recipedb accounts for 189 of the 288.

**Consequence:** for a pairing, the most the data can say is **"this source was cited for this pairing"**. It cannot say what the source claims about it. R4 shows exactly that and no more.

## The path, as the workspace shows it

**Prepared ingredient → role → pairing → source → claim scope**, for lemon on roasted broccoli:

| Step | Where | What is shown |
| --- | --- | --- |
| Prepared ingredient | Overview row *roasted broccoli* → Detail | Sheet heading, with step confidence *high* |
| Role | Section 3, *Needed culinary roles* | acid · priority medium · note "lemon/sherry vinegar" · 1 curated, 1 experimental |
| Pairing | Section 4, *Recorded pairings* | acid · **lemon** · curated · medium · application unspecified · ● on hand |
| Source | Same row, *Source · claim scope* | **roast_culinary** (culinary) |
| Claim scope | Same cell | **scope: not recorded** |
| Source detail | Section 6, *Sources for the pairings* | roast_culinary · culinary · linked pairings *fat: olive oil, salt: sea salt, acid: lemon* · claim scope "not recorded for these links" · the source describes itself as "roasting concentrates & jams; charring adds smoke" |
| Reverse | Click *roast_culinary* → Trace (source) | Every step and pairing it backs within broccoli, each edge labelled with its recorded scope or "scope not recorded" |

Every step is on one screen pane, or one click away, without leaving the overview.

## Wording rules

- **Step sources and pairing sources are separate tables** in section 6. A step source's scope ("slow roasting jams & concentrates") is about the transformation. It is never shown next to a pairing.
- **A source's own description is labelled as such.** The column is headed *The source describes itself as*, with the note: "the source's own description, not a claim about these pairings". roast_culinary's description does not mention lemon, so presenting it as the reason for lemon would overstate it.
- **Missing provenance is explicit:**
  - "no source recorded" (hatched), on each of the 16 experimental pairings;
  - "scope: not recorded", under every pairing source;
  - "no source for any pairing", as a row gap, where it applies.
- **Recipe co-occurrence is not shown as a number.** The sheet explains that the count is 0 for every pairing because the column has not been backfilled, and that 0 does not mean the pairing never occurs. A test checks that no "0 recipes" wording appears.
- **Nothing is invented.** No source titles, citations or explanations are generated. The *why* the workspace can offer is limited to what is recorded:
  - the role note;
  - the route's *why it fits*;
  - the source's title, type and description;
  - for ideas, the analogy's shared function and difference.

## What this means for K4 ("why is lemon associated with roasted broccoli?")

The workspace now shows everything the data holds:
- the role and its note;
- the named source and its type;
- the missing claim scope;
- two routes in which lemon is a **required** element, with their fit reasons.

**It does not show a claim that ties roast_culinary to lemon, because none is recorded.** The limit is in the data, not in the presentation. Filling `pairing_evidence.claim_scope` is a data task, logged in recommendations.

## Relationship navigation

| From | Click | Opens |
| --- | --- | --- |
| Any ingredient name (matrix cell, sheet, compare, trace table, graph node) | the name | Trace focused on that ingredient |
| Any route name | the name | Trace focused on the route: elements with optionality, and the preparations it fits |
| Any source title | the title | Trace focused on the source: every step and pairing it backs within the ingredient, with scope |
| ⇄ on an overview row | ⇄ | Trace focused on that preparation |
| A preparation in the trace table or graph | the name | Its fact sheet; the trace stays in the Trace tab |

At step 2, a **route trace** also shows the pairings of the route's elements in the fitted preparations, labelled "separate pairing record". The route element and the pairing are related (the same ingredient) but are not the same claim.
