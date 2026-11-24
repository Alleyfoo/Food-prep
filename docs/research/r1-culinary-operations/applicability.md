# Applicability: ingredient-level findings

Every operation's status for every starting part, with its reasons, is in
`applicability-tables.md` (generated). This page picks out what matters for
each ingredient: the useful operations, what they produce, and the parts and
residues cooks usually throw away.

Try it: `foodprep applicability broccoli --part stems`.

## Summary

| Part | applicable | conditional | inapplicable | unknown | unsafe |
| --- | ---: | ---: | ---: | ---: | ---: |
| broccoli florets | 34 | 0 | 48 | 0 | 0 |
| broccoli stems | 36 | 4 | 42 | 0 | 0 |
| broccoli leaves | 29 | 0 | 53 | 0 | 0 |
| carrot root | 36 | 1 | 45 | 0 | 0 |
| carrot greens | 28 | 0 | 54 | 0 | 0 |
| courgette fruit | 34 | 3 | 45 | 0 | 0 |
| tomato flesh | 26 | 1 | 55 | 0 | 0 |
| tomato seeds and gel | 8 | 0 | 74 | 0 | 0 |
| tomato skin | 27 | 0 | 55 | 0 | 0 |
| tomato core | 2 | 0 | 80 | 0 | 0 |
| avocado flesh | 16 | 0 | 65 | 0 | 1 |
| avocado skin | 0 | 0 | 82 | 0 | 0 |
| avocado stone | 0 | 0 | 0 | 0 | 82 |

Counts are over the 82 operations the generator may use, copied from
`applicability-tables.md`.

- **"Unknown" never occurred.** Every property an operation asks about is
  stated for these 13 parts. That shows the property set is complete for this
  catalogue on this set. It does not show it is complete for other
  ingredients (see `evaluation.md`).
- **The brief's examples behave as specified:**
  - julienne on carrot: applicable, "firm enough to hold a narrow strip";
  - chiffonade on broccoli florets: inapplicable, "needs a leaf";
  - chiffonade on broccoli leaves: applicable;
  - chiffonade on carrot greens: inapplicable, "the leaf must be a continuous
    sheet that can be rolled". Carrot tops are feathery.
- **Tomato core has two applicable operations, both stock-making:** simmering
  and decoction. That comes from the curated `only_techniques` (edible only in
  a stock or sieved sauce), plus `only_operations: [decocter]`. The first
  version of the engine ignored the restriction and let 31 operations through;
  a test now holds it.
- **The avocado stone is unsafe for every operation; the skin is
  inapplicable.** The curated reasons decide this: "not established as safe"
  against "tough and bitter".

## Broccoli

| Part | Operation | Conditions | Primary output | Secondary output | Resulting properties | Established use | Experimental use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| stems | éplucher (peel) | firm body; before cutting or cooking | peeled stem | **stem peel** (fraction) | inner toughness high → low, fibre high → medium | peeled stems for slicing (`cia`, `pepin`) | the peel as a material of its own |
| stems | julienne, rubans | **conditional: peel first** | strips, ribbons | — | thin, flexible ribbons | stem noodles (`web_b1`) | pickled ribbons |
| stem peel | déshydrater → moudre | thin; dry enough | powder | — | water none, brittle, then powder | none found for the peel alone (`web_b2`) | seasoning or colouring powder |
| stem peel | décocter | fibrous | broth | spent solids (end) | liquid, infused | scrap stocks in general | peel-only broth |
| leaves | équeuter | broad leaf with a rib | leaf blades | **ribs** | blades more tender; ribs firm strips | kale and chard practice | ribs as a crunchy pickle |
| leaves | chiffonade | rollable leaf | fine ribbons | — | fine, thin | `cia` | — |
| leaves | rôtir | thin | crisp leaves | — | crisp, no longer pliable | leaf chips (`web_b3`) | crushed as a crisp topping |
| leaves | blanchir | fresh | pliable leaves | — | flexible, brighter | collard-style wraps | broccoli-leaf wraps |
| florets | détailler en bouquets | branched head | small florets | — | smaller pieces | `cia` | — |
| florets | blanchir → purée → passer au chinois | — | silky sauce | fibrous residue | smooth | green purée (`web_b5`) | — |

The usually discarded broccoli materials are the leaves (S2: removed in 130
of 206 recipes naming them), the stem peel, and the leaf ribs.

## Carrot

| Part | Operation | Conditions | Primary output | Secondary output | Resulting properties | Established use | Experimental use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| root | éplucher | before cutting or cooking | peeled root | **carrot peel** | — | standard | peel as crisps or powder |
| root | every classical cut | very firm, cylindrical | julienne, brunoise, bâtonnet, rondelles, tourné... | tourné leaves trimmings | geometry | `escoffier`, `cia` | — |
| root | râper → presser | grate first, or use a juicer | **juice** | **pulp** | juice liquid with the sugar and colour; pulp fibrous, damp, binds | juice; pulp crackers (`web_c1`) | pulp as a crisp or structure without added binder |
| juice | réduire → monter au beurre | a reduction | glaze or sauce | — | concentrated, then emulsified | chef technique (`web_c5`) | — |
| root | glacer | cut first (pieces ≤ medium) | glazed carrots | — | shiny, sweet | carottes glacées (`escoffier`) | — |
| greens | effeuiller | feathery fronds on stalks | fronds | **stalks** | — | `cia` | stalks in broth |
| greens | hacher → piler | chop first: the mortar needs small pieces | herb paste | — | smooth paste | carrot-top pesto, chimichurri (`web_c4`) | — |
| greens | chiffonade | — | — | — | inapplicable: feathery, not a sheet | — | — |

The usually discarded carrot materials are the greens, the peel and the
juice pulp.

## Courgette

| Part | Operation | Conditions | Primary output | Secondary output | Resulting properties | Established use | Experimental use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fruit | éplucher | firm enough for a peeler | peeled fruit | **courgette skin** | skin: thin, flexible, ribbon-shaped | the skin is usually eaten on the fruit | **skin ribbons as a component of their own** (`web_z1`: no evidence found) |
| fruit | rubans | sheetable, firm | ribbons | — | flexible noodles | zoodles (`web_z4`) | — |
| fruit (cut) | dégorger | watery, cut first | drained pieces | **courgette water** | pieces firmer and salted; water salty, liquid | fritters (`web_z2`); the water is niche (`web_z3`) | courgette water reduced as a seasoning |
| fruit | évider, épépiner | **conditional: only large courgettes have a distinct seedy core** | shell (an edible vessel) | **seed core** | — | stuffed courgettes (`larousse`) | the core as a thickener (`web_z6`: sources advise against) |
| fruit | émincer → déshydrater | thin slices dry despite high water (waiver) | chips | — | crisp | courgette chips (`web_z5`) | salting before drying |

The courgette needs a safety note on every operation: taste a tiny raw piece
first and discard a very bitter fruit (cucurbitacin; cooking does not remove
it, `poison_squash`). The model carries it as the fruit's `note`.

## Tomato

| Part | Operation | Conditions | Primary output | Secondary output | Resulting properties | Established use | Experimental use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| skin | déshydrater → moudre | thin | powder | — | brittle, then powder | tomato skin powder (`web_t1`; the curated skin path) | — |
| skin | frire | thin | crisps | — | crisp | tomato skin crisps (`web_t4`) | — |
| seeds and gel | filtrer, clarifier | liquid | clear tomato water | — | clear | tomato consommé (`web_t2`) | — |
| seeds and gel | gélifier | liquid; adds agar or gelatin | gel | — | set, acid | — | an acid gel (links to the S3 tomato-gel acid idea) |
| seeds and gel | purée → émulsionner | pectin holds added oil (waiver) | emulsified dressing | — | emulsified | vinaigrettes with seeds (`web_t3`, niche) | gel as the whole acid of a vinaigrette |
| core | mijoter, décocter | curated: only in a stock | broth | spent solids | liquid | scrap stock (`web_t5`) | core-only stock |
| whole fruit | monder | — | — | — | inapplicable: tomato skin and flesh are already separate parts | — | — |

## Avocado

| Part | Operation | Conditions | Primary output | Resulting properties | Established use | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| flesh | griller, quartiers | short heat only | grilled wedges | browned, smoky | grilled avocado (`web_a3`) | The model has no function for "a grilled component", so it never ranks this (`evaluation.md`) |
| flesh | paner → frire | bread before frying | fries | crisp | avocado fries (`web_a4`) | — |
| flesh | purée → émulsionner | emulsifies | creamy sauce | emulsified | avocado "mayonnaise" (`web_a1`) | closer to a purée than a true emulsion |
| flesh | acidifier | **inapplicable for ripe flesh** | — | — | pickled firm avocado (`web_a2`) | The model has no ripeness property. Firm, underripe avocado would pass. A missing property |
| flesh | braiser, mijoter, confire... | **inapplicable: turns bitter with long heat** | — | — | — | `heat_sensitive` |
| flesh | déshydrater | **unsafe: turns bitter and rancid when dried at home** | — | — | contradicted (`web_a5`) | A negative finding the model now encodes |
| skin | all | not food | — | — | — | — |
| stone | all | unsafe: not established as safe to eat | — | — | — | `avocado_seed` |
