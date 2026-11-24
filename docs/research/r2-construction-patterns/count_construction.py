"""R2: count how RecipeNLG cooks build combined preparations.

For dishes picked by title (rosti, latkes, courgette fritters, falafel,
stuffed vegetables, cabbage rolls, dumplings, layered bakes, set egg
dishes ...), count how many recipes show each step: moisture removal
(squeezing, salting and draining, patting dry), additions that might hold
the mass together (egg, flour, crumbs, starch, cheese), coatings, shell
preparation, what happens to scooped-out flesh, pre-cooking, chilling, and
the final thermal step.

Counts only are written to `recipenlg-counts.yaml` and `recipenlg-counts.md`
next to this script. Sampled direction sentences for the hand check go to
`r2_construction_check.tsv` next to the corpus (gitignored: recipe text).

Run:  py -3.11 docs/research/r2-construction-patterns/count_construction.py PATH/full_dataset.csv

Without a path it uses $FOODPREP_RECIPENLG, then data/corpus/recipenlg/ in
the repository. Every pattern is a rough text rule; the hand-check sheet is
there to estimate how rough (see recipenlg.md).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RULES_VERSION = 1


def rx(p: str) -> re.Pattern[str]:
    return re.compile(p, re.I)


# ---- dishes, chosen by title ---------------------------------------------

@dataclass(frozen=True)
class Dish:
    key: str
    label: str
    title: re.Pattern[str]
    exclude: re.Pattern[str] | None = None
    # The material that has to be prepared before it is combined, for the
    # "pre-cooked" and "shell" features.
    main: re.Pattern[str] | None = None


SAVOURY_ONLY = r"|apple|pumpkin pie|chocolate|cinnamon|banana|sweet roll|dessert|cookie"

DISHES = [
    Dish("rosti", "Rosti / hash browns (not casseroles)",
         rx(r"\br(ö|o|oe)sti\b|hash[- ]?browns?\b|hashbrowns?\b"),
         rx(r"casserole|quiche|bake|soup|crust|egg cups?|breakfast pizza|stuffed|muffin|waffle|omelet|gratin|scallop|cream|chees|hot ?dish|pie|crock|slow cooker|skillet meal|frittata"),
         rx(r"potato")),
    Dish("latke", "Latkes / potato pancakes",
         rx(r"\blatkes?\b|potato pancakes?|kartoffelpuffer|reibekuchen|draniki|boxty|\bplacki\b"),
         rx(r"sweet potato|zucchini|apple" + SAVOURY_ONLY), rx(r"potato")),
    Dish("courgette_fritter", "Courgette / zucchini fritters and pancakes",
         rx(r"(zucchini|courgettes?)[\w\s,&-]{0,20}(fritters?|pancakes?|patties|cakes|latkes?|tots|rounds)|m[üu]cver|kolokithokeftedes"),
         rx(r"bread|muffin|chocolate|cake mix|cupcake|loaf"), rx(r"zucchini|courgette")),
    Dish("veg_fritter", "Other vegetable fritters (not corn)",
         rx(r"(carrot|cauliflower|broccoli|spinach|onion|vegetable|veggie|cabbage|sweet potato|eggplant|\bpea|parsnip|beet|kale|leek|squash)[\w\s,&-]{0,15}(fritters?|pancakes?|patties|latkes?)"),
         rx(r"zucchini|courgette|corn|potato pancake|peanut" + SAVOURY_ONLY)),
    Dish("corn_fritter", "Corn fritters",
         rx(r"\bcorn[\w\s,&-]{0,10}fritters?"), rx(r"apple|banana")),
    Dish("pakora", "Pakora / bhaji",
         rx(r"pakora|pakoda|bhaji|bhajia|bhajee")),
    Dish("falafel", "Falafel",
         rx(r"falaf+el|ta'?amia|ta'?ameya"), rx(r"salad|wrap|pita|sandwich|bowl|sauce|pizza|taco"),
         rx(r"chick ?peas?|garbanzos?|fava|broad beans?")),
    Dish("legume_patty", "Bean, lentil and veggie burgers / patties",
         rx(r"(bean|lentil|chickpea|garbanzo|veggie|vegetable|vegetarian|vegan|quinoa|tofu|mushroom)[\w\s,&-]{0,15}(burgers?|patties|patty)"),
         rx(r"soup|salad|casserole|chili|falafel"), rx(r"beans?|lentils?|chick ?peas?|garbanzos?")),
    Dish("potato_cake", "Mashed-potato cakes and croquettes",
         rx(r"potato (cakes?|croquettes?|patties|puffs)|croquetas? de patata|korokke|aloo tikki|\btikki\b|mashed potato (cakes?|patties|pancakes?)|leftover mashed potato"),
         rx(r"sweet potato|casserole|soup|bread|rolls?|doughnuts?|salad|pie\b"), rx(r"potato")),
    Dish("stuffed_pepper", "Stuffed peppers",
         rx(r"stuffed[\w\s]{0,10}peppers?|pimientos? rellenos?|biber dolma"),
         rx(r"soup|casserole|chili|jalape|poppers?|cherry|banana pepper|dip|chiles? rellenos?"),
         rx(r"peppers?")),
    Dish("chile_relleno", "Chiles rellenos",
         rx(r"chil[ei]s? rellenos?"), rx(r"casserole|bake|quiche|squares|soup|dip"), rx(r"chil[ie]s?|poblano|peppers?")),
    Dish("stuffed_courgette", "Stuffed courgette, squash, aubergine",
         rx(r"stuffed[\w\s]{0,10}(zucchini|courgettes?|summer squash|yellow squash|eggplants?|aubergines?)|(zucchini|eggplant) boats?|karn[ıi]yar[ıi]k|imam bay"),
         rx(r"soup|casserole"), rx(r"zucchini|courgettes?|squash|eggplants?|aubergines?")),
    Dish("stuffed_tomato", "Stuffed tomatoes",
         rx(r"stuffed[\w\s]{0,10}tomato"), rx(r"cherry|soup|casserole"), rx(r"tomato")),
    Dish("cabbage_roll", "Cabbage rolls",
         rx(r"cabbage rolls?|stuffed cabbage|go[lł][aą]bki|golumpki|halupki|holubtsi|\bsarma\b|kaalik[aä][aä]ryle"),
         rx(r"soup|casserole|lazy|unstuffed|skillet|in a bowl"), rx(r"cabbage|leaves|leaf")),
    Dish("stuffed_leaves", "Stuffed vine leaves",
         rx(r"dolma|dolmades|dolmathes|stuffed grape ?leaves|stuffed vine leaves|warak enab"),
         rx(r"soup|casserole|dip"), rx(r"leaves|leaf")),
    Dish("pierogi", "Pierogi / vareniki",
         rx(r"pierog|pirog(i|ies)|perog(i|ies|y)|varenyky|vareniki"), rx(r"casserole|lasagna|soup|lazy|bake")),
    Dish("asian_dumpling", "Potstickers, gyoza, jiaozi, wontons, mandu",
         rx(r"potstickers?|pot stickers?|gyoza|jiaozi|won ?tons?|shu ?mai|siu mai|\bmandu\b|chinese dumplings?"),
         rx(r"soup|casserole|chips|cups?|salad|nachos|lasagna")),
    Dish("spring_roll", "Egg rolls / spring rolls (fried)",
         rx(r"egg ?rolls?|spring rolls?|lumpia|ch[aả] gi[oò]"), rx(r"in a bowl|unrolled|soup|casserole|salad|fresh spring|summer rolls?|lasagna")),
    Dish("filled_pastry", "Empanadas, samosas, knishes, pasties",
         rx(r"empanad|samosa|knish|\bpast(y|ies)\b|piroshk|pirozhk|b[oö]rek|burek|spanakopita|spinach pie|tyropita|calzone"),
         rx(r"apple|cherry|peach|fruit|pumpkin|sweet potato pie|dessert|chocolate|casserole|dip|soup")),
    Dish("aubergine_parm", "Aubergine parmigiana",
         rx(r"(eggplant|aubergine)[\w\s]{0,10}parm|parmigiana|melanzane"), rx(r"chicken|veal|soup|sandwich|pizza|dip"),
         rx(r"eggplant|aubergine")),
    Dish("moussaka", "Moussaka", rx(r"moussaka"), None, rx(r"eggplant|aubergine|potato")),
    Dish("gratin", "Potato gratin / scalloped potatoes",
         rx(r"scalloped potato|potato(es)? (au )?gratin|gratin (de |of )?potato|au gratin potato|dauphinois|escalloped potato"),
         rx(r"pork|chop|ham|sausage|chicken|fish|seafood|crab|beef|hamburger|sweet potato"),
         rx(r"potato")),
    Dish("frittata", "Frittata / Spanish tortilla",
         rx(r"frittata|spanish tortilla|tortilla (espa|de patata)"), rx(r"cups?|muffins?|bites?\b")),
    Dish("quiche", "Quiche (incl. crustless)", rx(r"quiche"), rx(r"cups?|muffins?|bites?\b|mini")),
    Dish("veg_custard_bake", "Vegetable casseroles set with egg (squash casserole, corn pudding, souffle)",
         rx(r"(squash|zucchini)[\w\s]{0,10}casserole|corn[\w\s]{0,6}(pudding|casserole|souffl[eé])|(spinach|broccoli|carrot|cauliflower|squash|zucchini|vegetable)[\w\s]{0,6}souffl[eé]|potato kugel"),
         rx(r"noodle|bread pudding|chicken|beef|turkey|ham|sausage|tuna|shrimp|hamburger|ground|pork|cake mix|sweet potato|cornbread|dessert"),
         ),
    Dish("tempura", "Tempura / kakiage", rx(r"tempura|kakiage"), rx(r"sushi|roll|udon|soba|sauce|dipping|flakes|bits|crunch")),
    Dish("breaded_veg", "Breaded or battered vegetable pieces",
         rx(r"(fried|breaded|battered|crispy|crunchy|oven[- ]fried)[\w\s]{0,8}(zucchini|courgettes?|eggplant|aubergine|green tomatoes|okra|cauliflower|mushrooms|onion rings|squash|broccoli|pickles)|onion rings|zucchini (sticks|fries|chips)|eggplant (sticks|fries)"),
         rx(r"rice|salad|soup|casserole|pasta|noodle|chicken|steak|burger|dip\b|stuffed")),
]

# ---- features --------------------------------------------------------------

# Ingredient lines: things added to the mass.
INGREDIENT_FEATURES = {
    "egg": rx(r"\beggs?\b|egg (whites?|yolks?|substitute|beaters)|egg beaters"),
    "flour": rx(r"\bflours?\b|\bbesan\b|\bmaida\b|bisquick|baking mix|pancake mix"),
    "crumbs": rx(r"crumbs?\b|panko|matzo|matzah|matza|cracker|bread cubes|stuffing mix|\bbread\b(?! flour)|rusks?|zwieback"),
    "oats": rx(r"\boats?\b|oatmeal"),
    "starch": rx(r"corn ?starch|potato starch|tapioca|arrowroot|cornflour|katakuriko"),
    "cheese": rx(r"cheese|parmesan|parmigiano|feta|ricotta|mozzarella|cheddar|romano|gruy[eè]re|paneer"),
    "cornmeal": rx(r"cornmeal|corn meal|polenta|masa"),
    "leavening": rx(r"baking powder|baking soda|bicarbonate|self[- ]rising|self[- ]raising|bisquick|\byeast\b|club soda|soda water|sparkling water|beer\b"),
    "rice_raw": rx(r"\b(uncooked|raw|long[- ]grain|short[- ]grain|minute|instant)\b[^,;]{0,25}\brice\b(?!\s*(vinegar|wine|paper|noodle))|\brice\b[^,;]{0,10}\b(uncooked|raw)\b"),
    "rice_cooked": rx(r"\bcooked\b[^,;]{0,25}\brice\b|\brice\b,?\s*(cooked|leftover)|leftover rice|cooked white rice|cooked brown rice"),
    "legume_canned": rx(r"(\bcans?\b|canned|\btins?\b|tinned|\d+\s*oz)[^;]{0,40}(beans?|chick ?peas?|garbanzos?|lentils?)|(beans?|chick ?peas?|garbanzos?|lentils?)[^;]{0,20}(canned|\bcans?\b)"),
    "legume_dried": rx(r"\bdried\b[^;]{0,25}(beans?|chick ?peas?|garbanzos?|fava|lentils?)|(beans?|chick ?peas?|garbanzos?|fava|lentils?)[^;]{0,25}\b(dried|soaked|uncooked)"),
    "frozen_potato": rx(r"frozen[^;]{0,25}(hash ?browns?|shredded potato|potato(es)?|tater)|hash ?browns?,? frozen|refrigerated[^;]{0,20}(hash|potato)"),
    "potato_flakes": rx(r"instant (mashed )?potato|potato flakes|potato buds|mashed potato flakes"),
    "leftover_mash": rx(r"(leftover|cold|cooked)[^;]{0,15}mashed potato|mashed potato(es)?,?\s*(cold|leftover|cooked)"),
}

# Direction sentences. Each recipe counts once per feature.
SQUEEZE = rx(r"\b(squeez|wring|wrung|press)\w*\b[^.;]{0,80}\b(liquid|moisture|water|juices?|dry|excess)\b"
             r"|\b(squeez|wring|wrung)\w*\b[^.;]{0,60}\b(towel|cloth|cheesecloth|sieve|strainer|hands?)\b"
             r"|\b(towel|cloth|cheesecloth)\b[^.;]{0,60}\b(squeez|wring|twist)\w*")
SALT_REST = rx(r"\bsalt(ed)?\b[^.;]{0,100}\b(let (it |them |mixture )?(stand|sit|rest|drain|sweat)|stand for|sit for|rest for|colander|sweat|drain(ing)? for|for \d+\s*(to \d+\s*)?(min|hour))"
               r"|\b(sprinkle|toss|layer)\w*[^.;]{0,40}\bsalt\b[^.;]{0,60}\b(colander|drain|stand|sit|sweat|liquid|moisture|water|bitter)")
PAT_DRY = rx(r"\bpat(ted|ting|s)?\b[^.;]{0,40}\bdry\b|\bblot\w*\b(?![^.;]{0,30}\b(grease|oil|fat|excess oil))")
DRAIN_LIQ = rx(r"\bdrain\w*\b(?![^.;]{0,40}\b(on|onto)\b[^.;]{0,20}\b(paper|towel|rack|brown paper|absorbent))")
CHILL = rx(r"\b(refrigerat|chill|freez)\w*")
STARCH_SETTLE = rx(r"\bstarch\b[^.;]{0,120}\b(bottom|settl|reserve|left|remain|pour off|keep)|\b(pour|tip|drain)\w* off[^.;]{0,80}\bstarch|\bsettle\w*\b")
DREDGE = rx(r"\b(dredg|coat|roll|dip|dust|bread)\w*\b[^.;]{0,60}\b(flour|crumbs?|egg|panko|batter|cornmeal|meal|cracker|seasoned)")
BATTER = rx(r"\bbatter\b")
SCOOP = rx(r"\b(scoop|hollow|spoon|scrape|carve)\w*\b[^.;]{0,40}\b(out|pulp|flesh|insides?|seeds|meat|centers?|centres?|shells?)")
PULP = r"(pulp|flesh|insides?|scooped|scrapings|removed (portion|part)|what you (scooped|removed))"
REUSE = rx(rf"\b(chop|dice|mince|reserve|add|mix|combine|saute|sauté|cook|stir)\w*\b[^.;]{{0,60}}\b{PULP}\b"
           rf"|\b{PULP}\b[^.;]{{0,40}}\b(chop|dice|mince|reserve|add|mix|combine|saute|sauté|stir)\w*")
DISCARD_PULP = rx(rf"\b(discard|throw (away|out))\w*\b[^.;]{{0,50}}\b({PULP}|seeds)\b|\b({PULP}|seeds)\b[^.;]{{0,30}}\bdiscard")
SHELL_PRECOOK = rx(r"\b(parboil|blanch|boil|steam|microwave|simmer|precook|pre-cook|cook|bake|roast)\w*\b[^.;]{0,60}\b(shells?|peppers?|halves|cases|boats?|leaves|cabbage|head)\b"
                   r"|\b(shells?|peppers?|halves|boats?|leaves|cabbage|head)\b[^.;]{0,50}\b(parboil|blanch|boil|steam|microwave|simmer|soften|wilt|freez)\w*")
FREEZE_LEAVES = rx(r"\bfreez\w*\b[^.;]{0,60}\b(cabbage|head|leaves)|\b(cabbage|head)\b[^.;]{0,60}\bfreez")
FILLING_PRECOOK = rx(r"\b(brown|saute|sauté|fry|cook|stir[- ]fry)\w*\b[^.;]{0,60}\b(filling|meat|beef|onions?|mushrooms|spinach|vegetables?|potato(es)?|cabbage|sauerkraut|mixture)")
SAUCE_OVER = rx(r"\b(pour|spoon|ladle|cover)\w*\b[^.;]{0,40}\b(sauce|tomato|soup|juice|broth|stock|water)\b[^.;]{0,30}\b(over|on top|around)|\b(sauce|tomato|soup|juice|broth|stock)\b[^.;]{0,20}\bover\b")
LAYER = rx(r"\blayer\w*\b|\balternat\w*\b")
SEAL = rx(r"\b(seal|pinch|crimp|fold|press)\w*\b[^.;]{0,40}\b(edges?|closed?|shut|together|over)\b")
REST_DOUGH = rx(r"\b(let|allow)\b[^.;]{0,30}\b(rest|stand|sit|set|firm|cool)\b")

DIRECTION_FEATURES = {
    "squeeze": SQUEEZE, "salt_rest": SALT_REST, "pat_dry": PAT_DRY, "drain_liquid": DRAIN_LIQ,
    "chill": CHILL, "starch_settle": STARCH_SETTLE, "dredge": DREDGE, "batter": BATTER,
    "scoop": SCOOP, "reuse_pulp": REUSE, "discard_pulp": DISCARD_PULP,
    "shell_precook": SHELL_PRECOOK, "freeze_leaves": FREEZE_LEAVES,
    "filling_precook": FILLING_PRECOOK, "sauce_over": SAUCE_OVER, "layer": LAYER,
    "seal": SEAL, "rest_set": REST_DOUGH,
}

# Final thermal step: the last thermal word in the directions.
THERMAL = {
    "deep_fry": rx(r"deep[- ]?fr\w*|deep fat|\b\d+\s*(inch|in\.|cm)\w* (of )?(oil|fat|shortening)|until (they )?float"),
    "pan_fry": rx(r"\bfr(y|ied|ies|ying)\b|skillet|griddle|frying pan|saut[eé]\w*"),
    "bake": rx(r"\bbak(e|ed|es|ing)\b|\boven\b|\bbroil\w*"),
    "boil_steam": rx(r"\bboil(ing)? water\b|\bsimmer\w*|\bsteam\w*|\bpoach\w*|drop[^.;]{0,30}into[^.;]{0,20}(boiling|water)"),
    "microwave": rx(r"microwave"),
    "grill": rx(r"\bgrill\w*|barbecue"),
    "none": rx(r"$^"),
}


def precooked_main(dish: Dish, text: str) -> bool:
    """Is the dish's main material cooked before it is shaped or combined?
    The first sentence cooking it must come before the first shaping word."""
    if dish.main is None:
        return False
    cook = rx(rf"\b(boil|parboil|blanch|steam|microwave|bake|roast|cook|simmer)\w*\b[^.;]{{0,50}}\b({dish.main.pattern})"
              rf"|\b({dish.main.pattern})\b[^.;]{{0,30}}\b(boil|parboil|blanch|steam|microwave|bake|roast|cook|simmer)\w*")
    shape = rx(r"\b(grate|shred|form|shape|stuff|fill|roll|mash|combine|mix|patties|balls)\w*")
    m = cook.search(text)
    if not m:
        return False
    s = shape.search(text)
    return s is None or m.start() < s.start()


def final_thermal(text: str) -> str:
    best, pos = "none", -1
    for name, pat in THERMAL.items():
        for m in pat.finditer(text):
            if m.start() > pos:
                best, pos = name, m.start()
    return best


# ---- reading ---------------------------------------------------------------

def resolve_csv(explicit: str | None) -> Path:
    for v in (explicit, os.environ.get("FOODPREP_RECIPENLG"),
              str(REPO / "data" / "corpus" / "recipenlg" / "full_dataset.csv")):
        if v and Path(v).is_file():
            return Path(v)
    raise SystemExit("RecipeNLG full_dataset.csv not found: pass its path.")


def classify_title(title: str) -> str | None:
    for d in DISHES:
        if d.title.search(title) and not (d.exclude and d.exclude.search(title)):
            return d.key
    return None


@dataclass
class Tally:
    n: int = 0
    features: Counter = field(default_factory=Counter)
    final: Counter = field(default_factory=Counter)
    combos: Counter = field(default_factory=Counter)


def analyse(dish: Dish, ingredients: list[str], directions: list[str]) -> tuple[set[str], str, dict[str, str]]:
    ing = " ; ".join(ingredients)
    text = " ".join(directions)
    found: set[str] = {k for k, p in INGREDIENT_FEATURES.items() if p.search(ing)}
    hits: dict[str, str] = {}
    sentences = [s.strip() for step in directions for s in re.split(r"(?<=[.;!?])\s+", step) if s.strip()]
    for k, p in DIRECTION_FEATURES.items():
        for s in sentences:
            if p.search(s):
                found.add(k)
                hits[k] = s
                break
    if precooked_main(dish, text):
        found.add("main_precooked")
    if not found & {"egg", "flour", "crumbs", "oats", "starch", "cornmeal", "potato_flakes"}:
        found.add("no_added_binder")
    if found & {"squeeze", "salt_rest", "pat_dry"}:
        found.add("any_moisture_removal")
    return found, final_thermal(text), hits


COMBOS = {
    "moisture_removal_and_egg": {"any_moisture_removal", "egg"},
    "moisture_removal_no_binder": {"any_moisture_removal", "no_added_binder"},
    "egg_and_flour": {"egg", "flour"},
    "scoop_and_reuse": {"scoop", "reuse_pulp"},
    "scoop_and_discard": {"scoop", "discard_pulp"},
}


def run(path: Path, sample: int, seed: int = 0) -> tuple[dict[str, Tally], int, dict]:
    csv.field_size_limit(2**31 - 1)
    tallies: dict[str, Tally] = defaultdict(Tally)
    samples: dict[tuple[str, str], list] = defaultdict(list)
    seen: dict[tuple[str, str], int] = Counter()
    rng = random.Random(seed)
    by_key = {d.key: d for d in DISHES}
    total = 0
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_t, i_i, i_d = header.index("title"), header.index("ingredients"), header.index("directions")
        for row in reader:
            total += 1
            key = classify_title(row[i_t])
            if key is None:
                continue
            dish = by_key[key]
            found, fin, hits = analyse(dish, json.loads(row[i_i]), json.loads(row[i_d]))
            t = tallies[key]
            t.n += 1
            t.features.update(found)
            t.final[fin] += 1
            for name, need in COMBOS.items():
                if need <= found:
                    t.combos[name] += 1
            for feat, sentence in hits.items():  # reservoir sample per (dish, feature)
                k = (key, feat)
                seen[k] += 1
                bucket = samples[k]
                if len(bucket) < sample:
                    bucket.append((row[i_t], sentence))
                else:
                    j = rng.randrange(seen[k])
                    if j < sample:
                        bucket[j] = (row[i_t], sentence)
    return tallies, total, samples


# ---- output ----------------------------------------------------------------

def pct(a: int, n: int) -> str:
    return f"{100 * a / n:.0f}%" if n else "-"


FEATURE_ORDER = (list(INGREDIENT_FEATURES) + ["no_added_binder", "main_precooked", "any_moisture_removal"]
                 + list(DIRECTION_FEATURES))


def write_outputs(tallies: dict[str, Tally], total: int, path: Path) -> None:
    import yaml  # PyYAML is a project dependency

    out = {
        "generated_by": "docs/research/r2-construction-patterns/count_construction.py",
        "rules_version": RULES_VERSION,
        "date": date.today().isoformat(),
        "corpus": {"name": "RecipeNLG full_dataset.csv", "recipes_scanned": total,
                   "licence": "non-commercial research; counts only, no recipe text"},
        "note": "Each recipe counts once per feature. Text rules are rough; see recipenlg.md for the hand check.",
        "dishes": {},
    }
    for d in DISHES:
        t = tallies.get(d.key, Tally())
        out["dishes"][d.key] = {
            "label": d.label, "recipes": t.n,
            "features": {k: t.features.get(k, 0) for k in FEATURE_ORDER},
            "combinations": {k: t.combos.get(k, 0) for k in COMBOS},
            "final_thermal": {k: t.final.get(k, 0) for k in THERMAL},
        }
    (HERE / "recipenlg-counts.yaml").write_text(
        "# Generated: do not edit by hand.\n" + yaml.safe_dump(out, sort_keys=False, allow_unicode=True),
        encoding="utf-8")

    cols = [("egg", "egg"), ("flour", "flour"), ("crumbs", "crumbs/bread"), ("starch", "starch"),
            ("cheese", "cheese"), ("no_added_binder", "none of egg/flour/crumbs/oats/starch/meal"),
            ("any_moisture_removal", "moisture removed"), ("squeeze", "squeeze"),
            ("salt_rest", "salt+rest"), ("pat_dry", "pat dry"), ("drain_liquid", "drain (any)"), ("main_precooked", "main pre-cooked"),
            ("chill", "chill/freeze")]
    lines = ["# RecipeNLG construction counts (generated)", "",
             f"Generated {date.today().isoformat()} by `count_construction.py` (rules v{RULES_VERSION}) "
             f"over {total:,} recipes. Dishes are chosen by title. Percentages are of the dish's recipes. "
             "Rough text rules: read `recipenlg.md` for the hand check before quoting a number.", "",
             "## Additions and moisture", "",
             "| Dish | n | " + " | ".join(c[1] for c in cols) + " |",
             "| --- | ---: | " + " | ".join("---:" for _ in cols) + " |"]
    for d in DISHES:
        t = tallies.get(d.key, Tally())
        lines.append(f"| {d.label} | {t.n:,} | " + " | ".join(pct(t.features.get(c, 0), t.n) for c, _ in cols) + " |")
    cols2 = [("dredge", "dredge/coat"), ("batter", "batter"), ("scoop", "scoop/hollow"),
             ("reuse_pulp", "scooped flesh reused"), ("discard_pulp", "flesh/seeds discarded"),
             ("shell_precook", "shell pre-cooked"), ("freeze_leaves", "leaves frozen"),
             ("filling_precook", "filling pre-cooked"), ("rice_raw", "raw rice"), ("rice_cooked", "cooked rice"),
             ("sauce_over", "liquid poured over"), ("layer", "layered"), ("seal", "sealed/crimped"),
             ("starch_settle", "starch settled"), ("legume_canned", "canned legume"),
             ("legume_dried", "dried legume"), ("frozen_potato", "frozen potato"),
             ("leftover_mash", "leftover mash"), ("leavening", "leavening/soda")]
    lines += ["", "## Structure steps", "",
              "| Dish | n | " + " | ".join(c[1] for c in cols2) + " |",
              "| --- | ---: | " + " | ".join("---:" for _ in cols2) + " |"]
    for d in DISHES:
        t = tallies.get(d.key, Tally())
        lines.append(f"| {d.label} | {t.n:,} | " + " | ".join(pct(t.features.get(c, 0), t.n) for c, _ in cols2) + " |")
    lines += ["", "## Final thermal step (last thermal word in the directions)", "",
              "| Dish | n | " + " | ".join(THERMAL) + " |",
              "| --- | ---: | " + " | ".join("---:" for _ in THERMAL) + " |"]
    for d in DISHES:
        t = tallies.get(d.key, Tally())
        lines.append(f"| {d.label} | {t.n:,} | " + " | ".join(pct(t.final.get(c, 0), t.n) for c in THERMAL) + " |")
    lines += ["", "## Combinations", "",
              "| Dish | n | " + " | ".join(COMBOS) + " |", "| --- | ---: | " + " | ".join("---:" for _ in COMBOS) + " |"]
    for d in DISHES:
        t = tallies.get(d.key, Tally())
        lines.append(f"| {d.label} | {t.n:,} | " + " | ".join(pct(t.combos.get(c, 0), t.n) for c in COMBOS) + " |")
    (HERE / "recipenlg-counts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_samples(samples: dict, sheet: Path) -> None:
    with open(sheet, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["dish", "feature", "title", "sentence", "correct (y/n)"])
        for (dish, feat), rows in sorted(samples.items()):
            for title, sentence in rows:
                w.writerow([dish, feat, title, sentence, ""])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--sample", type=int, default=12, help="sentences per dish and feature for the hand check")
    args = ap.parse_args()
    path = resolve_csv(args.csv)
    t0 = time.time()
    tallies, total, samples = run(path, args.sample)
    write_outputs(tallies, total, path)
    sheet = path.parent / "r2_construction_check.tsv"
    write_samples(samples, sheet)
    for d in DISHES:
        print(f"{d.key:20} {tallies.get(d.key, Tally()).n:6}")
    print(f"{total} recipes scanned in {time.time() - t0:.0f} s; hand-check sheet {sheet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
