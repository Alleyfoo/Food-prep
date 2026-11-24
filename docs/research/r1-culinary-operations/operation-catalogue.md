# Operation catalogue

Generated from `src/foodprep/data/operations.yaml` by `run.py`; edit the YAML, not this file. Source ids are explained in `sources.md`.

95 operations; 82 used by the sequence generator. Categories are not exclusive: an operation lists every mechanism family it belongs to, and is filed here under its first.

## Geometry

### julienne — julienne (matchsticks) (`julienne`)

| Field | Value |
| --- | --- |
| Aliases | allumette, matchstick |
| Categories | geometry |
| Produces preparation | `julienne` |
| Requires | shape cylindrical/round/irregular (a solid body to square off; not branched, leafy or feathery); cut False (already cut: one cut per sequence); firmness >=medium (firm enough to hold a narrow strip); liquid False (a liquid cannot be cut); piece >=medium (starts larger than a matchstick) |
| Conditional | peel first: the outer layer is too tough to cut fine |
| Equipment | knife |
| Effort | 2 |
| Parameters | about 3 x 3 mm x 4-6 cm; fine julienne 1.5 mm; Escoffier longer |
| Property changes | Far more surface: cooks in seconds, takes dressing, stays crisp raw |
| Applications | slaws, garnish, stir-fries, consomme garnish |
| Limitations | soft or leafy materials tear instead of cutting clean |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root, broccoli.stems, courgette.fruit |
| Evidence | `escoffier`, `cia`, `wiki_knife_cuts` |
| Confidence | established |

### brunoise — brunoise (fine dice) (`brunoise`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `brunoise` |
| Requires | shape cylindrical/round/irregular (a solid body to square off; not branched, leafy or feathery); cut False (already cut: one cut per sequence (brunoise refines julienne)); firmness >=medium (holds a 3 mm cube); liquid False (a liquid cannot be cut); piece small/medium/large/whole (cut from julienne or a larger piece) |
| Conditional | peel first: tough skin breaks a 3 mm cube |
| Equipment | knife |
| Effort | 2 |
| Parameters | about 3 mm cubes (fine brunoise 1.5 mm), cut across julienne |
| Property changes | Disperses through a sauce or garnish; softens almost at once |
| Applications | garnish, sauce bases, mirepoix-like seasoning |
| Limitations | only firm materials; watery ones bleed |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit |
| Evidence | `escoffier`, `cia`, `wiki_knife_cuts` |
| Confidence | established |

### bâtonnet — baton (`batonnet`)

| Field | Value |
| --- | --- |
| Aliases | baton |
| Categories | geometry |
| Produces preparation | `batonnet` |
| Requires | shape cylindrical/round/irregular (a solid body to square off; not branched, leafy or feathery); cut False (already cut: one cut per sequence); firmness >=medium (holds a stick shape); liquid False (a liquid cannot be cut); piece >=medium (starts larger than a stick) |
| Equipment | knife |
| Effort | 2 |
| Parameters | about 6 x 6 mm x 5-6 cm; sources disagree (some 1 cm thick) |
| Property changes | Even sticks that cook evenly; enough mass to stay tender inside |
| Applications | crudites, fries, glazed vegetables |
| Limitations | needs a long enough piece |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit |
| Evidence | `cia`, `wiki_knife_cuts` |
| Confidence | established |

### macédoine — small dice (`macedoine`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `macedoine` |
| Requires | shape cylindrical/round/irregular (a solid body to square off; not branched, leafy or feathery); cut False (already cut: one cut per sequence); firmness >=medium (holds a cube); liquid False (a liquid cannot be cut); piece >=medium (starts larger than a cube) |
| Equipment | knife |
| Effort | 2 |
| Parameters | about 5 mm cubes (one source 4 mm) |
| Property changes | Bite-size cubes; even cooking |
| Applications | vegetable salads (macedoine), soups, fillings |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit |
| Evidence | `escoffier`, `wiki_knife_cuts` |
| Confidence | established |

### paysanne — paysanne (thin flat pieces) (`paysanne`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `paysanne` |
| Requires | shape cylindrical/round/irregular (a solid body to square off; not branched, leafy or feathery); cut False (already cut: one cut per sequence); firmness >=medium (holds a thin flat piece); liquid False (a liquid cannot be cut); piece >=medium (starts larger than the piece) |
| Equipment | knife |
| Effort | 2 |
| Parameters | about 12 x 12 x 3 mm; square, round or triangular by source |
| Property changes | Thin and flat: quick, even cooking in soups |
| Applications | rustic soups (potage paysanne) |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root |
| Evidence | `escoffier`, `wiki_knife_cuts` |
| Confidence | established |

### chiffonnade — chiffonade (fine ribbons of leaves) (`chiffonade`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `chiffonade` |
| Requires | cut False (already cut: one cut per sequence); leafy True (needs a leaf); shape flat (the leaf must be a continuous sheet that can be rolled); flexible True (rolled before slicing) |
| Equipment | knife |
| Effort | 1 |
| Parameters | leaves stacked, rolled and cut 1-3 mm across |
| Property changes | Fine ribbons that wilt instantly in heat |
| Applications | garnish, soups, quick sautes of greens |
| Limitations | feathery or tiny leaves cannot be rolled; chop them instead |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | broccoli.leaves |
| Evidence | `cia`, `wiki_knife_cuts` |
| Confidence | established |

### tourner (légumes tournés) — tourne (turned) (`tourner`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `tourne` |
| Requires | cut False (already cut: one cut per sequence); firmness >=high (carved with a paring knife into a seven-sided barrel); shape cylindrical/round (needs a solid body to carve); piece >=medium (starts larger than the barrel) |
| Equipment | knife |
| Effort | 3 |
| Parameters | about 5 cm long, 7 faces, 2 cm wide |
| Property changes | Identical pieces that cook evenly and glaze well; leaves many trimmings |
| Applications | classical garnish, glazed carrots |
| Limitations | wasteful; skill-heavy |
| Mechanisms | shape_uniformity |
| Outputs | main (geometry); trimmings (fraction) |
| Documented on | carrot.root |
| Evidence | `escoffier`, `cia`, `wiki_knife_cuts` |
| Confidence | established |

### rondelles — rounds (coins) (`rondelles`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `rondelles` |
| Requires | cut False (already cut: one cut per sequence); shape cylindrical (a round cross-section); firmness >=medium (holds a disc) |
| Equipment | knife |
| Effort | 1 |
| Parameters | 2-10 mm discs across a cylinder |
| Property changes | Discs that stay juicy; thin slices are emincer |
| Applications | sautes, chips (thin), steaming |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit, broccoli.stems |
| Evidence | `cia` |
| Confidence | established |

### émincer — slice thinly (`emincer`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Ontology technique | `slice` |
| Produces preparation | `sliced` |
| Requires | cut False (already cut: one cut per sequence); firmness >=low (holds a slice); liquid False (a liquid cannot be cut) |
| Equipment | knife |
| Effort | 1 |
| Parameters | thin slices, 1-3 mm |
| Property changes | Thin slices that cook fast and brown at the edges |
| Applications | sautes, stir-fries, carpaccio-style salads |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | broccoli.stems, courgette.fruit, carrot.root |
| Evidence | `cia`, `larousse` |
| Confidence | established |

### hacher — chop (`hacher`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `chopped` |
| Requires | cut False (already cut: one cut per sequence); liquid False (a liquid cannot be chopped) |
| Equipment | knife |
| Effort | 1 |
| Parameters | irregular pieces, coarse to fine |
| Property changes | Irregular fine pieces; releases juice and aroma |
| Applications | herb pastes, salsas, fillings |
| Mechanisms | surface_area_increase, cell_rupture |
| Outputs | main (geometry) |
| Documented on | carrot.greens, broccoli.leaves |
| Evidence | `cia`, `larousse` |
| Confidence | established |

### ciseler — finely mince (shallots, herbs) (`ciseler`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `finely_chopped` |
| Requires | cut False (already cut: one cut per sequence); leafy True (herbs and leaves are sliced fine without bruising) |
| Equipment | knife |
| Effort | 1 |
| Parameters | very fine, clean cuts that do not bruise |
| Property changes | Fine pieces that stay fresh instead of bruised and dark |
| Applications | herb garnish, sauces |
| Limitations | classically for shallots and herbs; alliums are outside this set |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | carrot.greens |
| Evidence | `larousse`, `cia` |
| Confidence | established |

### concasser — rough-chop (concassé) (`concasser`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Ontology technique | `crush` |
| Produces preparation | `crushed` |
| Requires | cut False (already cut: one cut per sequence); firmness <=medium (classically soft flesh (tomato) or brittle seeds); liquid False (a liquid cannot be chopped) |
| Equipment | knife |
| Effort | 1 |
| Parameters | rough pieces about 5-10 mm |
| Property changes | Rough pieces; for tomato, peeled and seeded flesh that holds its shape |
| Applications | tomato concasse, sauces |
| Mechanisms | cell_rupture |
| Outputs | main (geometry) |
| Documented on | tomato.flesh |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### râper — grate (`raper`)

| Field | Value |
| --- | --- |
| Categories | geometry, mechanical |
| Ontology technique | `grate` |
| Produces preparation | `grated` |
| Requires | cut False (already cut: one cut per sequence); firmness >=medium (must resist the grater); liquid False (a liquid cannot be grated) |
| Conditional | peel first: the tough layer shreds into strings |
| Equipment | grater |
| Effort | 1 |
| Parameters | coarse or fine grater |
| Property changes | Shreds that release juice; watery materials weep |
| Applications | slaws, fritters, cakes |
| Mechanisms | surface_area_increase, cell_rupture |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit |
| Evidence | `cia` |
| Confidence | established |

### tailler en rubans — ribbons (`rubans`)

| Field | Value |
| --- | --- |
| Aliases | spiralise |
| Categories | geometry |
| Produces preparation | `ribbons` |
| Requires | cut False (already cut: one cut per sequence); sheetable True (must give long continuous strips without breaking); firmness >=medium (a peeler or spiraliser needs resistance) |
| Conditional | peel first: ribbons with a tough edge stay stringy |
| Equipment | peeler |
| Effort | 1 |
| Parameters | peeler or mandoline ribbons 1-2 mm thick; spiraliser for noodles |
| Property changes | Long flexible ribbons: eaten raw, blanched, or as noodles |
| Applications | vegetable noodles, salads, wraps |
| Mechanisms | shape_transformation |
| Outputs | main (geometry) |
| Documented on | courgette.fruit, carrot.root, broccoli.stems |
| Evidence | `cia`, `web_b1`, `web_c3`, `web_z4` |
| Confidence | established |

### tailler en quartiers — wedges (`quartiers`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `wedges` |
| Requires | cut False (already cut: one cut per sequence); shape round/cylindrical (a body to cut lengthwise into wedges); piece >=medium (starts larger than a wedge); liquid False (a liquid cannot be cut) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Large pieces with a cut face to brown and a skin side to hold |
| Applications | roasting, grilling |
| Mechanisms | shape_transformation |
| Outputs | main (geometry) |
| Documented on | avocado.flesh, courgette.fruit |
| Evidence | `cia` |
| Confidence | established |

### tailler en tronçons — chunks (sections) (`troncons`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `troncons` |
| Requires | cut False (already cut: one cut per sequence); shape cylindrical (an elongated body to cut across); piece >=large (starts long) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Thick sections for long cooking or stuffing |
| Applications | braises, stuffed sections |
| Mechanisms | shape_transformation |
| Outputs | main (geometry) |
| Documented on | carrot.root, courgette.fruit |
| Evidence | `larousse` |
| Confidence | established |

### inciser (ciseler la surface) — score (`inciser`)

| Field | Value |
| --- | --- |
| Categories | geometry |
| Produces preparation | `scored` |
| Requires | piece >=medium (a surface to score); firmness >=low (holds a shallow cut) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Shallow cuts let heat and seasoning in; cut faces brown |
| Applications | grilled avocado, roasted halves |
| Limitations | changes little on its own |
| Mechanisms | surface_area_increase |
| Outputs | main (geometry) |
| Documented on | avocado.flesh |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | changes little on its own; a detail of grilling or roasting halves |

### détailler en bouquets — cut into florets (`detailler_bouquets`)

| Field | Value |
| --- | --- |
| Categories | geometry, separation |
| Requires | cut False (already cut: one cut per sequence); shape tree (a branched head) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Small florets that cook evenly |
| Applications | steaming, roasting, stir-frying |
| Mechanisms | shape_transformation |
| Outputs | main (geometry) |
| Documented on | broccoli.florets |
| Evidence | `cia` |
| Confidence | established |

## Separation

### éplucher — peel (with a peeler or knife) (`eplucher`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Ontology technique | `peel` |
| Requires | has_outer_layer True (needs an outer layer that is not a part of its own); firmness >=medium (a peeler needs a firm body); cut False (peel before cutting, not each piece after); cooked False (a peeler works on raw produce; skin cooked produce with peler) |
| Equipment | peeler |
| Effort | 1 |
| Property changes | Two materials: the peeled body (often more tender) and the peel |
| Applications | broccoli stems before slicing, carrots for a smooth finish |
| Limitations | a peel is only a residue if nothing is done with it |
| Mechanisms | layer_separation |
| Outputs | inner (state, from self); peel (fraction, from outer_layer) |
| Documented on | broccoli.stems, carrot.root |
| Evidence | `cia`, `pepin` |
| Confidence | established |

### peler — skin (after cooking or blanching) (`peler`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | has_outer_layer True (needs a skin); cooked True (the skin slips off only after heat) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Removes a skin loosened by heat |
| Applications | roasted peppers, beetroot, cooked carrots |
| Mechanisms | layer_separation |
| Outputs | inner (state, from self); skin (fraction, from outer_layer) |
| Evidence | `larousse` |
| Confidence | established |

### monder — blanch and skin (`monder`)

| Field | Value |
| --- | --- |
| Categories | separation, thermal |
| Requires | skin_slips_when_blanched True (a skin that loosens after seconds in boiling water) |
| Equipment | pot |
| Effort | 1 |
| Parameters | 10-30 s in boiling water, then iced |
| Property changes | Clean skinning without cooking the flesh |
| Applications | tomatoes, peaches, almonds |
| Limitations | needs the whole fruit: in this model tomato skin and flesh are already parts |
| Mechanisms | layer_separation |
| Outputs | inner (state); skin (fraction, from outer_layer) |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### parer — trim (`parer`)

| Field | Value |
| --- | --- |
| Categories | separation, geometry |
| Ontology technique | `trim` |
| Requires | firmness >=medium (trimmed to a neat shape); piece >=medium (large enough to trim) |
| Equipment | knife |
| Effort | 1 |
| Property changes | A neat piece plus trimmings (parures) for stock or puree |
| Applications | classical prep; parures go to stocks and purees |
| Mechanisms | shape_uniformity |
| Outputs | trimmed (state); trimmings (fraction) |
| Documented on | broccoli.stems, carrot.root |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### épépiner — deseed (`epepiner`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Ontology technique | `deseed` |
| Requires | has_seed_core True (needs a seed region to remove) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Drier flesh that holds its shape; a seed fraction |
| Applications | large courgettes, cucumbers, tomatoes |
| Mechanisms | layer_separation |
| Outputs | flesh (state); seeds (fraction, from seed_core) |
| Documented on | courgette.fruit |
| Evidence | `larousse` |
| Confidence | established |

### évider — hollow out (core) (`evider`)

| Field | Value |
| --- | --- |
| Categories | separation, geometry |
| Ontology technique | `core` |
| Requires | has_seed_core True (needs a soft centre to scoop); firmness >=medium (the shell must stand up); cut False (hollow the whole fruit or halves before cutting) |
| Equipment | spoon |
| Effort | 1 |
| Property changes | A shell to fill and a soft core |
| Applications | stuffed courgettes (courgettes farcies) |
| Mechanisms | layer_separation |
| Outputs | shell (state); core (fraction, from seed_core) |
| Documented on | courgette.fruit |
| Evidence | `larousse`, `escoffier` |
| Confidence | established |

### équeuter — de-stem, remove the midrib (`equeuter`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | leafy True (a leaf with a stalk or rib); shape flat (a broad leaf with a rib) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Tender leaf blades and the crunchy ribs |
| Applications | kale, chard, broccoli leaves |
| Mechanisms | layer_separation |
| Outputs | blades (state); ribs (fraction) |
| Documented on | broccoli.leaves |
| Evidence | `cia`, `web_b3` |
| Confidence | established |

### effeuiller — strip leaves from stalks (`effeuiller`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | leafy True (leaves on stalks); shape feathery (small leaves or fronds on thin stalks) |
| Equipment | knife |
| Effort | 1 |
| Property changes | Tender fronds; fibrous stalks for stock |
| Applications | herbs, carrot tops |
| Mechanisms | layer_separation |
| Outputs | fronds (state); stalks (fraction) |
| Documented on | carrot.greens |
| Evidence | `cia` |
| Confidence | established |

### écosser — shell (pods) (`ecosser`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | podded True (seeds in a pod) |
| Effort | 1 |
| Applications | peas, broad beans |
| Limitations | nothing in this research set grows in a pod |
| Mechanisms | layer_separation |
| Outputs | seeds (state) |
| Evidence | `larousse` |
| Confidence | established |

### dénoyauter — stone, pit (`denoyauter`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Ontology technique | `stone` |
| Requires | has_stone True (a single stone inside) |
| Equipment | knife |
| Effort | 1 |
| Applications | avocados, olives, stone fruit |
| Limitations | in this model the avocado stone is already a part of its own |
| Mechanisms | layer_separation |
| Outputs | flesh (state) |
| Evidence | `larousse` |
| Confidence | established |

### zester — zest (`zester`)

| Field | Value |
| --- | --- |
| Categories | separation, extraction |
| Requires | zestable True (a thin rind full of aromatic oil (citrus)) |
| Equipment | grater |
| Effort | 1 |
| Applications | citrus |
| Limitations | vegetable peels are not zest: they hold no aromatic oil glands |
| Mechanisms | oil_release |
| Outputs | zest (fraction) |
| Evidence | `larousse`, `mcgee` |
| Confidence | established |

### lever les suprêmes — segment (supremes) (`lever_supremes`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | segmented True (fruit in membrane-bound segments) |
| Equipment | knife |
| Effort | 2 |
| Applications | citrus |
| Limitations | nothing in this research set is segmented |
| Mechanisms | layer_separation |
| Outputs | segments (state) |
| Evidence | `larousse` |
| Confidence | established |

### égrainer — remove grains or kernels (`egrainer`)

| Field | Value |
| --- | --- |
| Categories | separation |
| Requires | has_kernels True (kernels or arils to free) |
| Effort | 1 |
| Applications | pomegranate, corn, grapes |
| Limitations | nothing in this research set has kernels |
| Mechanisms | layer_separation |
| Outputs | kernels (state) |
| Evidence | `larousse` |
| Confidence | established |

## Extraction

### presser — press, juice (`presser`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | water >=high (enough free water to give juice); liquid False (already a liquid); gelled False (needs plant tissue, not a gel); firmness >=low (solid tissue to press) |
| Conditional | grate first, or use a juicer |
| Equipment | grater, cloth |
| Effort | 2 |
| Property changes | Juice with the colour and sugar; pulp with the fibre |
| Applications | juices, reductions; pulp in crackers and fritters |
| Mechanisms | fractionation |
| Outputs | juice (fraction); pulp (fraction) |
| Documented on | carrot.root |
| Evidence | `cia`, `web_c1`, `web_c5` |
| Confidence | established |

### filtrer — strain, filter (`filtrer`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | liquid True (filters a liquid); clear False (already clear) |
| Equipment | sieve, cloth |
| Effort | 1 |
| Property changes | A clear liquid |
| Applications | tomato water, clarified juices |
| Mechanisms | fractionation |
| Outputs | filtered (state) |
| Documented on | tomato.seeds_and_gel |
| Evidence | `web_t2` |
| Confidence | established |

### tamiser (passer au tamis) — sieve, sift (`tamiser`)

| Field | Value |
| --- | --- |
| Categories | extraction, mechanical |
| Requires | piece powder (sifts a ground powder; wet purees go through the chinois); water <=low (sifts dry material); liquid False (use passer au chinois for liquids) |
| Equipment | sieve |
| Effort | 1 |
| Property changes | An even powder or puree, and a coarse fraction to regrind |
| Applications | powders, flours, fine purees |
| Mechanisms | fractionation |
| Outputs | fine (state); coarse (fraction) |
| Evidence | `escoffier`, `cia` |
| Confidence | established |

### passer au chinois — pass through a conical sieve (`passer_chinois`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | smooth True (a puree or sauce) |
| Equipment | sieve |
| Effort | 1 |
| Property changes | A silky sauce and a fibrous residue |
| Applications | veloutes, green purees, coulis |
| Mechanisms | fractionation |
| Outputs | passed (state); residue (fraction) |
| Documented on | broccoli.florets |
| Evidence | `escoffier`, `web_b5` |
| Confidence | established |

### fouler — press through a sieve with a ladle (`fouler`)

| Field | Value |
| --- | --- |
| Categories | extraction, mechanical |
| Requires | cooked True (softened first); liquid False (pushes solids, not a liquid); water >=medium (moist enough to push through; crisp material only crumbles); firmness <=low (soft enough to push through) |
| Equipment | sieve, ladle |
| Effort | 1 |
| Property changes | A coulis without skins or seeds |
| Applications | tomato coulis, fruit coulis |
| Mechanisms | fractionation |
| Outputs | coulis (state); residue (fraction) |
| Evidence | `escoffier` |
| Confidence | established |

### dégorger — salt and drain (`degorger`)

| Field | Value |
| --- | --- |
| Categories | extraction, chemical |
| Ontology technique | `salt_and_drain` |
| Requires | water >=high (draws out free water); liquid False (a liquid cannot be drained); smooth False (needs intact pieces, not a puree); gelled False (needs plant tissue, not a gel); piece <=medium (cut first so salt reaches the cells) |
| Adds | salt |
| Equipment | colander, towel |
| Effort | 1 |
| Parameters | salt 1-2% of weight, 10-30 min, then squeeze |
| Property changes | Firmer, less watery pieces and a salty vegetable water |
| Applications | courgette fritters, tomato water, cucumber salads |
| Mechanisms | osmosis |
| Outputs | drained (state); vegetable_water (fraction) |
| Documented on | courgette.fruit, tomato.flesh |
| Evidence | `web_z2`, `web_z3`, `web_t2` |
| Confidence | established |

### égoutter — drain (`egoutter`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Equipment | colander |
| Effort | 1 |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | a step inside other operations; changes no property worth a step |

### clarifier — clarify (`clarifier`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Ontology technique | `clarify` |
| Requires | liquid True (clarifies a liquid); clear False (already clear) |
| Adds | egg_white_or_agar |
| Equipment | pot, cloth |
| Effort | 3 |
| Parameters | egg-white raft, or agar gel then drained (gel filtration) |
| Property changes | A brilliant clear liquid (consomme) |
| Applications | consommes, clear tomato water |
| Mechanisms | fractionation, protein_coagulation |
| Outputs | clarified (state) |
| Documented on | tomato.seeds_and_gel |
| Evidence | `escoffier`, `web_t2` |
| Confidence | established |

### écumer — skim (`ecumer`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | liquid True (skims a liquid) |
| Equipment | ladle |
| Effort | 1 |
| Evidence | `escoffier` |
| Confidence | established |
| Not generated | keeps a simmering liquid clean; no new material |

### décanter — decant, let settle (`decanter`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | liquid True (settles a liquid) |
| Equipment | jar |
| Effort | 1 |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | same outcome as filtrer for these materials |

### infuser — infuse, steep (`infuser`)

| Field | Value |
| --- | --- |
| Categories | extraction |
| Requires | liquid False (steeps a solid); smooth False (a puree is strained, not steeped); gelled False (a gel is not steeped); water <=medium (dry or aromatic material flavours the liquid; watery pieces only dilute it); fat <=low (fat-rich flesh does not give its flavour to water); piece <=small (small or dried pieces give flavour quickly) |
| Adds | hot_water_or_oil |
| Equipment | pot, sieve |
| Effort | 1 |
| Property changes | A flavoured liquid; the solids give up their flavour |
| Applications | teas, broths, flavoured oils and vinegars |
| Safety | Fresh low-acid vegetables in oil can carry botulism: refrigerate and use within 4 days (CDC) |
| Mechanisms | extraction |
| Outputs | infusion (fraction); spent (fraction) |
| Evidence | `mcgee`, `cdc_botulism` |
| Confidence | established |

### décocter — decoct (simmer to extract) (`decocter`)

| Field | Value |
| --- | --- |
| Categories | extraction, thermal |
| Requires | heat_sensitive False (turns bitter with long heat); liquid False (simmers a solid); fibre >=medium (tough, fibrous material gives flavour only to long simmering) |
| Adds | water |
| Equipment | pot, sieve |
| Effort | 2 |
| Property changes | A vegetable broth from parts too tough to eat |
| Applications | vegetable stocks from scraps |
| Mechanisms | extraction |
| Outputs | decoction (fraction); spent (fraction) |
| Documented on | tomato.core |
| Evidence | `escoffier`, `web_t5` |
| Confidence | established |

## Mechanical

### écraser — crush, mash (`ecraser`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Ontology technique | `mash` |
| Requires | firmness <=medium (soft or cooked enough to crush); liquid False (already liquid) |
| Equipment | fork |
| Effort | 1 |
| Property changes | A coarse mash with texture left in |
| Applications | guacamole, crushed vegetables |
| Mechanisms | cell_rupture |
| Outputs | main (state) |
| Documented on | avocado.flesh |
| Evidence | `cia` |
| Confidence | established |

### réduire en purée — puree (`reduire_puree`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | toughness <=low (soft enough to puree); coated False (a coated piece is fried or baked, not pureed) |
| Equipment | blender |
| Effort | 1 |
| Property changes | Smooth and spoonable |
| Applications | purees, soups, spreads |
| Mechanisms | cell_rupture, dispersion |
| Outputs | main (state) |
| Documented on | broccoli.florets, avocado.flesh |
| Evidence | `cia`, `escoffier` |
| Confidence | established |
| Family generator state | `puree` |

### mixer — blend (`mixer`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Ontology technique | `blend` |
| Requires | water >=medium (enough water to blend, or add liquid); liquid False (already liquid); coated False (a coated piece is fried or baked, not blended) |
| Equipment | blender |
| Effort | 1 |
| Property changes | A smooth blend, raw or cooked |
| Applications | raw purees, pestos, drinks |
| Mechanisms | dispersion |
| Outputs | main (state) |
| Documented on | carrot.greens, avocado.flesh |
| Evidence | `cia`, `web_c4` |
| Confidence | established |

### broyer — grind coarsely (`broyer`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | firmness >=low (solid enough to grind); liquid False (already liquid); smooth False (already smooth) |
| Equipment | food_processor |
| Effort | 1 |
| Property changes | Coarse crumbs or paste |
| Applications | crumbs, rice-like grains (riced vegetables) |
| Mechanisms | particle_size_reduction |
| Outputs | main (state) |
| Evidence | `cia` |
| Confidence | established |

### piler — pound (mortar) (`piler`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | piece <=small (pounded in small pieces); liquid False (already liquid) |
| Equipment | mortar |
| Effort | 2 |
| Property changes | A coarse aromatic paste; pounding releases more aroma than blades |
| Applications | pesto, herb pastes |
| Mechanisms | cell_rupture, oil_release |
| Outputs | main (state) |
| Evidence | `larousse`, `mcgee` |
| Confidence | established |

### émietter — crumble (`emietter`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | crisp True (only brittle material crumbles) |
| Effort | 1 |
| Property changes | Crisp crumbs to scatter |
| Applications | toppings, coatings |
| Mechanisms | particle_size_reduction |
| Outputs | main (state) |
| Evidence | `larousse` |
| Confidence | established |

### moudre — grind to a powder (`moudre`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | water <=low (only dry, brittle material becomes powder); crisp True (brittle enough to shatter); fat <=medium (fat-rich material turns to paste instead of powder) |
| Equipment | spice_grinder |
| Effort | 1 |
| Property changes | A powder that disperses flavour and colour |
| Applications | spice blends, vegetable powders |
| Mechanisms | particle_size_reduction |
| Outputs | main (state) |
| Documented on | tomato.skin |
| Evidence | `web_t1`, `web_c6` |
| Confidence | established |

### abaisser — roll out (`abaisser`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Equipment | rolling_pin |
| Effort | 2 |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | works on doughs; outside the vegetable materials |

### laminer — laminate, sheet (`laminer`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Equipment | pasta_machine |
| Effort | 3 |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | works on doughs; outside the vegetable materials |

### malaxer — knead, work (`malaxer`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Effort | 2 |
| Evidence | `larousse` |
| Confidence | established |
| Not generated | works on doughs and butter; masser covers leaves |

### fouetter — whisk (`fouetter`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Equipment | whisk |
| Effort | 1 |
| Evidence | `mcgee` |
| Confidence | established |
| Not generated | needs a protein or fat foam former (egg, cream) |

### foisonner — aerate, increase volume (`foisonner`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Equipment | whisk |
| Effort | 2 |
| Evidence | `mcgee` |
| Confidence | established |
| Not generated | needs a foam former; outside the vegetable materials |

### émulsionner — emulsify (`emulsionner`)

| Field | Value |
| --- | --- |
| Categories | mechanical |
| Requires | smooth True (a smooth base to carry the emulsion); fat >=medium (fat to disperse; or a pectin-rich base that holds added oil) |
| Adds | oil_or_water |
| Equipment | blender |
| Effort | 1 |
| Property changes | A creamy sauce that holds fat in suspension |
| Applications | mayonnaise-like sauces |
| Limitations | an avocado 'mayonnaise' is closer to a puree than a true emulsion (web_a1) |
| Mechanisms | emulsification |
| Outputs | main (state) |
| Documented on | avocado.flesh |
| Evidence | `mcgee`, `web_a1` |
| Confidence | established |

### masser — massage (leaves) (`masser`)

| Field | Value |
| --- | --- |
| Categories | mechanical, chemical |
| Ontology technique | `massage` |
| Requires | leafy True (a leaf); toughness >=medium (only sturdy leaves need it); raw_ok True (eaten raw after) |
| Adds | salt, oil |
| Equipment | bowl |
| Effort | 1 |
| Property changes | Raw leaves that soften and darken without heat |
| Applications | kale salads |
| Mechanisms | cell_rupture, osmosis |
| Outputs | main (state) |
| Documented on | broccoli.leaves |
| Evidence | `web_b3` |
| Confidence | established |
| Family generator state | `massage` |

## Thermal

### cru — raw (no operation) (`servir_cru`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `raw_assemble` |
| Requires | raw_ok True (pleasant to eat raw) |
| Evidence | `cia` |
| Confidence | established |
| Not generated | eating raw is the starting state, not a transformation |
| Family generator state | `raw` |

### blanchir — blanch (`blanchir`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | liquid False (blanches a solid); cooked False (already cooked); crisp False (dried or crisp material would only rehydrate); smooth False (blanches pieces, not a puree) |
| Equipment | pot |
| Effort | 1 |
| Parameters | seconds to 2 min in boiling salted water, then iced |
| Property changes | Brighter green, slightly softer, pliable; enzymes stopped |
| Applications | before freezing, purees, wraps from leaves |
| Mechanisms | enzyme_inactivation, colour_fixing, cell_softening |
| Outputs | main (state) |
| Documented on | broccoli.florets, carrot.root |
| Evidence | `cia`, `steam_culinary` |
| Confidence | established |

### cuire à la vapeur — steam (`cuire_vapeur`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `steam` |
| Requires | heat_sensitive False (turns bitter with long heat); cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (steams a solid); fibre >=medium (holds together in steam); toughness <=medium (tender enough to steam through) |
| Equipment | pot |
| Effort | 1 |
| Property changes | Tender-crisp, flavour kept in |
| Applications | side dishes |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Documented on | broccoli.florets, carrot.root |
| Evidence | `cia`, `steam_culinary` |
| Confidence | established |
| Family generator state | `steam` |

### pocher — poach (`pocher`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | heat_sensitive False (turns bitter with long heat); liquid False (poaches a solid); cooked False (already cooked) |
| Adds | stock_or_water |
| Equipment | pot |
| Effort | 1 |
| Property changes | Gently cooked in a flavoured liquid it absorbs |
| Applications | delicate vegetables, fruit |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Evidence | `escoffier` |
| Confidence | established |

### étuver — stew in own juices (covered) (`etuver`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | heat_sensitive False (turns bitter with long heat); water >=medium (cooks in its own water); liquid False (stews a solid); cooked False (already cooked) |
| Adds | butter |
| Equipment | pan |
| Effort | 1 |
| Property changes | Soft, concentrated, pale |
| Applications | courgettes, leeks, greens |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Documented on | courgette.fruit |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### suer — sweat (`suer`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | heat_sensitive False (turns bitter with long heat); piece <=small (small pieces release water); liquid False (sweats a solid); cooked False (already cooked) |
| Adds | fat |
| Equipment | pan |
| Effort | 1 |
| Property changes | Soft and sweet without colour |
| Applications | soup and sauce bases |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `cia` |
| Confidence | established |

### sauter — saute (`sauter`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `saute` |
| Requires | liquid False (sautes a solid); piece <=medium (pieces small enough to toss); cooked False (already cooked) |
| Adds | fat |
| Equipment | pan |
| Effort | 1 |
| Property changes | Lightly browned outside, tender-crisp inside |
| Applications | side dishes |
| Mechanisms | maillard, dehydration_surface |
| Outputs | main (state) |
| Documented on | broccoli.leaves, courgette.fruit |
| Evidence | `cia` |
| Confidence | established |

### sauter au wok — stir-fry (`sauter_wok`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `stir_fry` |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (stir-fries a solid); toughness <=medium (tender enough for fast heat) |
| Adds | fat |
| Equipment | pan |
| Effort | 1 |
| Property changes | Browned edges, crisp-tender |
| Applications | stir-fries |
| Mechanisms | maillard |
| Outputs | main (state) |
| Documented on | broccoli.florets, broccoli.stems |
| Evidence | `cia` |
| Confidence | established |
| Family generator state | `stir_fry` |

### rissoler — brown (shallow-fry to colour) (`rissoler`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (browns a solid); water <=high (too much water steams instead of browning); piece <=medium (pieces small enough to colour all over) |
| Adds | fat |
| Equipment | pan |
| Effort | 1 |
| Property changes | A brown crust |
| Applications | potatoes, roots |
| Mechanisms | maillard |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### rôtir — roast (`rotir`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `roast` |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (roasts a solid); water <=high (too watery to brown) |
| Adds | fat |
| Equipment | oven |
| Effort | 1 |
| Property changes | Browned, concentrated, soft inside; thin pieces crisp |
| Applications | side dishes |
| Mechanisms | maillard, caramelisation, dehydration_surface |
| Outputs | main (state) |
| Documented on | broccoli.florets, carrot.root |
| Evidence | `cia`, `roast_culinary` |
| Confidence | established |
| Family generator state | `roast` |

### griller — grill, char (`griller`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `char` |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (grills a solid); piece >=small (small pieces fall through the grill); firmness >=low (holds together on the grill) |
| Adds | fat |
| Equipment | pan |
| Effort | 1 |
| Property changes | Charred stripes and smoke |
| Applications | grilled vegetables, grilled avocado |
| Mechanisms | maillard, pyrolysis |
| Outputs | main (state) |
| Documented on | avocado.flesh, courgette.fruit |
| Evidence | `web_a3` |
| Confidence | established |

### frire — deep-fry (`frire`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `fry` |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (fries a solid); water <=medium (dry enough to crisp; or coated, or cut thin); smooth False (a puree needs binding or a batter first) |
| Adds | oil |
| Equipment | pot |
| Effort | 2 |
| Property changes | Crisp, golden, fat-rich |
| Applications | chips, fritters, fries |
| Safety | Hot oil: never leave unattended; dry the material well |
| Mechanisms | dehydration_surface, maillard |
| Outputs | main (state) |
| Documented on | carrot.root, tomato.skin |
| Evidence | `cia`, `web_t4`, `web_a4` |
| Confidence | established |
| Family generator state | `fry` |

### braiser — braise (`braiser`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `braise` |
| Requires | heat_sensitive False (turns bitter with long heat); cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (braises a solid); fibre >=medium (fibrous enough to need slow cooking) |
| Adds | stock_or_water |
| Equipment | pot |
| Effort | 2 |
| Property changes | Soft, savoury, glossy |
| Applications | root vegetables, greens |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `escoffier` |
| Confidence | established |
| Family generator state | `braise` |

### mijoter — simmer (`mijoter`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `simmer` |
| Requires | heat_sensitive False (turns bitter with long heat); cooked False (already cooked: one primary cooking per sequence (blanching does not count)) |
| Adds | stock_or_water |
| Equipment | pot |
| Effort | 2 |
| Property changes | Soft, and it flavours its liquid |
| Applications | sauces, soups |
| Mechanisms | cell_softening, extraction |
| Outputs | main (state) |
| Documented on | tomato.flesh |
| Evidence | `escoffier` |
| Confidence | established |
| Family generator state | `simmer` |

### cuire à l'anglaise — boil in salted water (`cuire_anglaise`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `boil` |
| Requires | heat_sensitive False (turns bitter with long heat); liquid False (boils a solid); cooked False (already cooked) |
| Adds | salted_water |
| Equipment | pot |
| Effort | 1 |
| Property changes | Soft; some flavour leaches into the water |
| Applications | plain vegetables, before puree |
| Mechanisms | cell_softening |
| Outputs | main (state) |
| Documented on | carrot.root, broccoli.florets |
| Evidence | `escoffier` |
| Confidence | established |

### cuire au four — bake (`cuire_four`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `bake` |
| Requires | heat_sensitive False (turns bitter with long heat); cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (bakes a solid or set mixture) |
| Equipment | oven |
| Effort | 1 |
| Property changes | Cooked through in dry heat, less browned than roasting |
| Applications | gratins, stuffed vegetables, crackers |
| Mechanisms | dehydration_surface |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `cia` |
| Confidence | established |

### glacer (à blanc, à brun) — glaze (`glacer`)

| Field | Value |
| --- | --- |
| Categories | thermal, chemical |
| Requires | cooked False (already cooked: one primary cooking per sequence (blanching does not count)); firmness >=medium (holds its shape while the liquid reduces); piece <=medium (pieces small enough to coat); liquid False (glazes a solid) |
| Adds | butter, sugar, water |
| Equipment | pan |
| Effort | 2 |
| Property changes | Tender pieces in a shiny buttery glaze |
| Applications | carottes glacees, turnips, pearl onions |
| Mechanisms | reduction, coating |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `escoffier`, `larousse` |
| Confidence | established |

### gratiner — gratinate (`gratiner`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `gratin` |
| Requires | cooked True (browns a cooked dish); liquid False (needs a surface) |
| Adds | cheese_or_crumbs |
| Equipment | oven |
| Effort | 1 |
| Property changes | A browned crust on top |
| Applications | gratins |
| Mechanisms | maillard |
| Outputs | main (state) |
| Evidence | `escoffier` |
| Confidence | established |

### confire — confit (slow-cook in fat or sugar) (`confire`)

| Field | Value |
| --- | --- |
| Categories | thermal, chemical |
| Requires | heat_sensitive False (turns bitter with long heat); cooked False (already cooked: one primary cooking per sequence (blanching does not count)); liquid False (confits a solid); firmness >=low (holds together through long cooking) |
| Adds | fat_or_syrup |
| Equipment | pot |
| Effort | 3 |
| Property changes | Meltingly soft, concentrated, preserved in fat or sugar |
| Applications | tomato confit, candied peel (sugar) |
| Safety | Vegetables kept in oil: refrigerate and use within 4 days, or freeze (CDC) |
| Mechanisms | cell_softening, osmosis |
| Outputs | main (state) |
| Documented on | tomato.flesh |
| Evidence | `larousse`, `cdc_botulism` |
| Confidence | established |

### réduire — reduce (`reduire`)

| Field | Value |
| --- | --- |
| Categories | thermal, extraction |
| Ontology technique | `reduce` |
| Requires | liquid True (reduces a liquid); concentrated False (already reduced) |
| Equipment | pan |
| Effort | 2 |
| Parameters | simmer until reduced by half or more |
| Property changes | Concentrated and syrupy: a glaze or sauce |
| Applications | carrot juice glaze, tomato water reduction |
| Mechanisms | evaporation, concentration |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `escoffier`, `web_c5` |
| Confidence | established |

### dessécher — dry out over heat (`dessecher`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | heat_sensitive False (turns bitter with long heat); smooth True (dries a puree in the pan) |
| Equipment | pan |
| Effort | 2 |
| Property changes | A stiff, concentrated puree |
| Applications | duchesse-style purees, pastes |
| Mechanisms | evaporation |
| Outputs | main (state) |
| Evidence | `escoffier` |
| Confidence | established |

### déshydrater — dry, dehydrate (`deshydrater`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `dry` |
| Requires | thin True (only thin pieces dry through); water <=medium (too watery to dry; unless sliced thin) |
| Unsafe when | fat-rich flesh turns bitter and rancid when dried at home (web_a5) |
| Equipment | oven |
| Effort | 2 |
| Parameters | oven 100-120 C for 1-2 h, or a dehydrator 55-60 C for hours |
| Property changes | Brittle, shelf-stable, concentrated |
| Applications | chips, powders |
| Mechanisms | evaporation, concentration |
| Outputs | main (state) |
| Documented on | tomato.skin, courgette.fruit, carrot.root |
| Evidence | `web_t1`, `web_z5`, `web_c6` |
| Confidence | established |
| Family generator state | `dry` |

### torréfier — toast (dry) (`torrefier`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Requires | water <=low (toasts dry material); browned False (already toasted) |
| Equipment | pan |
| Effort | 1 |
| Property changes | Deeper, nuttier aroma |
| Applications | seeds, spices, powders |
| Mechanisms | maillard |
| Outputs | main (state) |
| Evidence | `mcgee` |
| Confidence | established |

### caraméliser — caramelise (`caramelliser`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `caramelize` |
| Requires | heat_sensitive False (turns bitter with long heat); sugar >=medium (needs sugar to caramelise); browned False (already browned) |
| Equipment | pan |
| Effort | 2 |
| Property changes | Sweet, bitter-edged, dark |
| Applications | onions, roots, glazes |
| Mechanisms | caramelisation |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `mcgee` |
| Confidence | established |

### fumer — smoke (`fumer`)

| Field | Value |
| --- | --- |
| Categories | thermal, chemical |
| Requires | smoked False (already smoked) |
| Equipment | smoker |
| Effort | 3 |
| Property changes | Smoke aroma; hot smoking also cooks |
| Applications | smoked vegetables, smoked salts |
| Safety | Use food-safe wood; smoke aroma is strong, so test small |
| Mechanisms | smoke_deposition |
| Outputs | main (state) |
| Evidence | `modernist` |
| Confidence | established |

### congeler — freeze (`congeler`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `freeze` |
| Equipment | freezer |
| Effort | 1 |
| Evidence | `nchfp` |
| Confidence | established |
| Not generated | preservation; ice crystals soften texture but create no new use here |

### appertiser — can (heat-process in jars) (`appertiser`)

| Field | Value |
| --- | --- |
| Categories | thermal |
| Ontology technique | `can` |
| Unsafe when | low-acid vegetables canned without a pressure canner risk botulism (NCHFP) |
| Equipment | pressure_canner |
| Effort | 3 |
| Evidence | `nchfp`, `usda_tomato` |
| Confidence | established |
| Not generated | preservation; low-acid vegetables need a pressure canner and a tested recipe |

## Chemical

### mariner — marinate (`mariner`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid False (marinates a solid) |
| Adds | acid, oil, aromatics |
| Equipment | bowl |
| Effort | 1 |
| Property changes | Seasoned through; acid softens slightly |
| Applications | raw vegetable salads, before grilling |
| Mechanisms | diffusion |
| Outputs | main (state) |
| Evidence | `cia` |
| Confidence | established |

### macérer — macerate (`macerer`)

| Field | Value |
| --- | --- |
| Categories | chemical, extraction |
| Requires | sugar >=medium (sugar draws juice into a syrup); liquid False (macerates a solid) |
| Adds | sugar_or_alcohol |
| Equipment | bowl |
| Effort | 1 |
| Property changes | Softened pieces in their own syrup |
| Applications | fruit; sweet roots |
| Mechanisms | osmosis |
| Outputs | macerated (state); syrup (fraction) |
| Evidence | `larousse` |
| Confidence | established |

### saumurer — brine (`saumurer`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid False (brines a solid); firmness >=medium (stays firm in brine) |
| Adds | brine |
| Equipment | jar |
| Effort | 1 |
| Property changes | Seasoned through, firm |
| Applications | before fermenting or cooking |
| Mechanisms | osmosis, diffusion |
| Outputs | main (state) |
| Evidence | `nchfp` |
| Confidence | established |

### fermenter (lacto-fermentation) — ferment (`fermenter`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Ontology technique | `ferment` |
| Requires | liquid False (ferments a solid in its brine); sugar >=low (bacteria need some sugar); firmness >=medium (soft material turns to mush) |
| Adds | salt |
| Equipment | jar |
| Effort | 3 |
| Parameters | salt about 2-3% of weight (extension sources range 1-5%), 4-14 days |
| Property changes | Sour, funky, preserved, still crunchy |
| Applications | sauerkraut, fermented stems |
| Safety | Weigh the salt (below 2% invites spoilage); keep under brine; discard if slimy or mouldy beyond surface yeast |
| Mechanisms | lactic_fermentation |
| Outputs | main (state) |
| Documented on | broccoli.stems, carrot.root |
| Evidence | `noma`, `nchfp`, `vt_fermentation`, `web_b6` |
| Confidence | established |

### acidifier (pickles rapides) — quick-pickle (`acidifier`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Ontology technique | `pickle` |
| Requires | liquid False (pickles a solid); firmness >=medium (stays crunchy in acid) |
| Adds | vinegar, salt, sugar |
| Equipment | jar |
| Effort | 1 |
| Property changes | Crunchy, sour, keeps a week in the fridge |
| Applications | pickled stems, pickled carrots |
| Safety | A fridge pickle. Shelf-stable pickling needs a tested recipe; broccoli is not recommended for home canning |
| Mechanisms | acidification, osmosis |
| Outputs | main (state) |
| Documented on | broccoli.stems, carrot.root, avocado.flesh |
| Evidence | `nchfp`, `web_b4`, `web_a2` |
| Confidence | established |

### gélifier — set as a gel (`gelifier`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid True (sets a liquid) |
| Adds | agar_or_gelatin |
| Equipment | pot |
| Effort | 2 |
| Property changes | A sliceable or spoonable gel |
| Applications | tomato water gel, vegetable jellies |
| Mechanisms | gelation |
| Outputs | main (state) |
| Evidence | `modernist`, `mcgee` |
| Confidence | established |

### lier — thicken, bind (`lier`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid True (thickens a liquid); thickened False (already thickened) |
| Adds | starch_or_yolk_or_butter |
| Equipment | pot, whisk |
| Effort | 1 |
| Property changes | A coating sauce |
| Applications | sauces from juices and broths |
| Mechanisms | starch_gelatinisation |
| Outputs | main (state) |
| Evidence | `escoffier`, `peterson` |
| Confidence | established |

### monter au beurre — mount with butter (`monter_beurre`)

| Field | Value |
| --- | --- |
| Categories | chemical, mechanical |
| Requires | liquid True (finishes a liquid); concentrated True (a reduction, so the butter emulsifies) |
| Adds | butter |
| Equipment | whisk |
| Effort | 1 |
| Property changes | A glossy emulsified sauce |
| Applications | beurre blanc, juice reductions |
| Limitations | splits if boiled after the butter goes in |
| Mechanisms | emulsification |
| Outputs | main (state) |
| Documented on | carrot.root |
| Evidence | `peterson`, `web_c5` |
| Confidence | established |

### enrober — coat (batter, glaze) (`enrober`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid False (coats a solid); cooked False (coat before cooking; blanched is fine); smooth False (batter clings to pieces, not to a puree); coated False (already coated) |
| Adds | batter |
| Equipment | bowl |
| Effort | 1 |
| Property changes | A coating that protects in the fryer |
| Applications | tempura, fritters |
| Mechanisms | coating |
| Outputs | main (state) |
| Evidence | `cia` |
| Confidence | established |

### paner (à l'anglaise) — bread (flour, egg, crumbs) (`paner`)

| Field | Value |
| --- | --- |
| Categories | chemical |
| Requires | liquid False (breads a solid); cooked False (bread before cooking; blanched is fine); smooth False (crumbs coat pieces, not a puree); firmness >=low (holds the coating); coated False (already coated); piece small/medium/large (pieces to coat) |
| Adds | flour, egg, crumbs |
| Equipment | bowl |
| Effort | 2 |
| Property changes | A crumb coat that crisps in fat or oven |
| Applications | avocado fries, courgette fries |
| Mechanisms | coating |
| Outputs | main (state) |
| Documented on | avocado.flesh, courgette.fruit |
| Evidence | `cia`, `web_a4` |
| Confidence | established |

### déglacer — deglaze (`deglacer`)

| Field | Value |
| --- | --- |
| Categories | chemical, extraction |
| Equipment | pan |
| Effort | 1 |
| Evidence | `escoffier` |
| Confidence | established |
| Not generated | dissolves a pan fond, which is not a material of the part |
