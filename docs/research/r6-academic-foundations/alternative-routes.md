# Keeping alternative routes apart (Q4)

How can several documented ways to the same dish be represented without
accidentally combining incompatible instructions? This file synthesises:
- `evidence-recipe-graphs.md`: cross-recipe alignment, Y503 and Y506;
- `evidence-cbr-workflows.md`: case bases, generalisation and stream
  combination, Y300-Y303;
- `evidence-foon-robotics.md`: union merge and retrieval, Y201-Y206;
- `evidence-industrial-process.md`: ISA-88 recipe types and trial,
  Y602-Y604; validity rules, Y608;
- `evidence-substitution.md`: several minimal repairs, Y402.

"Inferred" marks a reading made in R6.

## Short answer

Every approach that **combines** documented steps from different sources
would produce Food-prep's unverified combinations K1-x and K2-x and present
them as ordinary results:
- FOON's merged network with retrieval;
- Trier's stream composition and generalised workflows;
- the aggregation goal of recipe alignment.

None of them attaches a status saying that the result was never
documented. The combinations come from:
- FOON: retrieval across the merged network (Y201 VI-A, presented as a
  strength);
- Trier: generalisation, which turns 61 sandwich recipes into about
  9·10^21 (Y300), and stream composition, whose interfaces check ingredient
  names, not states (Y302);
- recipe alignment: transitive closure (Y503 §4.1).

The one tradition that treats a new combination as unvalidated by default
is industrial. Under ISA-88:
- an edited general recipe is a new version;
- it must be validated in **trial** before it becomes a master recipe
  (Y603 4.3.2-4.3.3);
- recipe-management systems keep separate recipes with **validity rules**
  that say when each applies (Y608).

So Food-prep's existing rule is supported, and it is stronger than the
academic cooking literature on this point:
- documented routes and R5 `alternatives` are kept apart, each with its
  sources;
- conflicts are kept as versions;
- nothing is merged.

What the literature adds is **structure inside the separation**. Three
concepts are worth taking:
1. **Step-level correspondence** between a route and its alternatives,
   allowing "none" and many-to-one (Y503, Y506). It shows where two routes
   differ, but never licenses composing them.
2. **What compensates for a missing step**: the long covered bake replaces
   the blanch. No paper represents this. It is the gap that makes action
   alignment unable to tell K8's working route from its failing one, and
   R5 already holds the evidence as text (G7, G8).
3. **The level a value belongs to** (ISA-88: general, master, control).
   - Some values belong to the dish in general: blanch the rutabaga, because
     the bake alone is too slow.
   - Some belong to one kitchen: 55 minutes in this oven, in this dish.
   - Some belong to one cooking: tonight's 62 minutes, the knife met some
     give.

## Three kinds of difference, kept apart

The user asked to distinguish recipe variants, different finished products
and unverified combinations. The evidence supports four distinctions.
Industrial practice adds one: the same route in another kitchen.

| Kind | Definition used in R6 | How the literature handles it | Food-prep now | Example |
| --- | --- | --- | --- | --- |
| **Version of a step** | the same route; sources differ on one value (time, cover, fineness) | conflicts in parameters are not modelled in cooking work; ISA-88 holds parameter ranges in the formula (Y602) | R5 `conflicts`, each version with its sources (43) | rutabaga blanch 3-5 min against about 10 min (K1) |
| **Alternative route** | the same dish; sources split the work differently (other steps or another order) | separate cases (CBR, Y300), separate graphs (r-FG, Y501), separate master recipes or versions (Y602, Y603) | R3 `routes`; R5 `alternatives`, 31 as cited one-line text | K1's four routes; K7 boiled rice against risotto rice |
| **Different product** | another dish name, or an analog that keeps the structure | Y401 "analog" against "substitute"; Y402 dish-identity constraints | separate R3 dishes; R4 transfers carry a base dish | falafel against *vatana vada*; gratin against *lanttulaatikko* |
| **Unverified combination** | each part is documented in some route, the whole is not | not distinguished by any cooking approach read; ISA-88: a new version needs trial (Y603) | named in R6 as K1-x and K2-x; R5 lists alternatives, not combinations | K1-x: a 10-min blanch, then a 90-min covered bake; K2-x: a 5-min boil as the soak of a raw-soaked falafel |
| **Same route, another kitchen** (from ISA-88) | the general route bound to one oven, pot and dish | master recipe (Y602) | not distinguished; R5 times are per source, and each assumes someone's equipment | the bake time in a deep dish against a shallow one |

## Why combination is dangerous here, and how the literature misses it

**K1-x.** Lay the gratin's routes side by side as an action alignment
(`evidence-recipe-graphs.md`, approach D):
- every route aligns "bake" with "bake";
- the raw long bake and the failing raw short bake differ only in a
  duration and a cover, which action alignment discards (Y503 §3.4);
- the blanch aligns with "none" in the long-bake route, and nothing says
  that the long covered bake is what compensates.

Compose the 10-min "almost tender" blanch (G16, G18) with the long covered
bake (G7, G8), and each step has a source. The result has none, and the
likely failure (over-soft rutabaga) has no documented check (R5
limitations: no over-blanch failure found).

**K2-x.**
- A "quick soak" by boiling 5 min (Q109) and an overnight soak align as
  corresponding hydration actions.
- The prohibition that matters is that the paste must stay raw so that it
  sets in the oil (Q114). It belongs to the route's later grinding and
  frying, not to the soak.
- No alignment or stream interface represents a prohibition tied to a
  later state.
- Trier's streams match by ingredient name ("chickpeas" in, "chickpeas"
  out) and would accept the swap (Y302).
- FOON identifies a node by name and state, so "soaked chickpeas" from
  either history is the same node (Y201).

**K8.** The false positive (raw short bake accepted before A2) and the
false negative (raw long covered bake rejected after A2) are both a
procedure judged without its parameters. That is exactly the error ISA-88
separates out by keeping the formula (parameters) apart from the procedure
(Y602; `evidence-industrial-process.md` approach A, inferred).

## What Food-prep already does right

- R5 `alternatives` keep each documented split with its sources, and the
  rejected route is listed as such (`processing_conditions.yaml`, gratin
  sequence).
- Conflicts are versions, never averages.
- R4 transfers are derived from **one** documented base route, never
  assembled from several.
- `from_state` lists the documented routes passing through a state. It does
  not compose a new route from that state.

None of the approaches read has all four. The closest are ISA-88's recipe
versions with trial (Y603) and Y402's set of minimal repairs, which are
kept as separate solutions.

## What to extend (data, a later round; not done in R6)

1. **Promote the alternatives that matter to whole routes** with steps, so
   that they can be walked and compared step by step. R5 limitations name
   this: alternatives that are not R3 routes are text. The gratin's long
   covered bake is the first candidate, because the model currently rejects
   it.
2. **Correspondence between routes of one dish**: for each step, the step
   it corresponds to in the main route, or `none`, with an optional
   `compensated_by` naming the step that does its job ("long covered bake
   instead of the blanch", G7, G8). This is for reading only: the validator
   must never build a route from correspondences.
3. **A status for a combination** when someone asks for it (the interface
   will be asked "can I blanch and then bake long?"): *each part documented,
   the combination not*, listing the sources of each part. This is a
   computed label, never a route.
4. **The value's level**: a route-level fact (blanch the rutabaga) against
   a per-source time that assumes equipment. Most cooks' sources do not
   state their equipment (an open question in `evidence-industrial-process.md`),
   so the marking can only be "stated" or "not stated", never inferred.
5. **The kitchen test as the control record**: one cooking, with the actual
   values and the observed endpoint, written back as evidence on the route.
   It is never merged into the route's documented values (ISA-88's control
   recipe and batch record, Y602, Y604).

## What not to do

- No generalised workflow and no stream or operator combination: the
  mechanism that creates unverified routes at scale (Y300, Y302).
- No merged "universal" network for retrieval (Y201, Y202).
- No preference ranking among valid recipes (Oracle's validity-rule
  preference, Y608). Validity conditions ("when it applies") are useful;
  a preference order is a score.
- No alignment-based aggregation into one "canonical" route (Y503 §6, Y506).
