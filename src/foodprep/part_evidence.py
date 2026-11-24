"""RecipeNLG practice evidence for ingredient parts (ADR 0002, S1 follow-up).

For each part of an ingredient (broccoli stems, tomato skin, ...), this reads
RecipeNLG's ingredient lines and directions one sentence at a time and sorts
each sentence that talks about the part into a class:

  used      the part goes into the dish ("peel the stalks, cut into coins")
  trimmed   only its ends or tough outer layer come off; the part stays
  removed   the part leaves the dish ("discard the stems", "peeled tomatoes")
  cue       the part is a cooking signal only ("until the skins split")
  canned    the step was bought, not done ("1 can peeled tomatoes")
  unclear   the part is named but the sentence says nothing about its fate

Each recipe then gets the strongest class it shows for the part, in the order
above, so one "discard the stems" line does not outvote a recipe that cooks
the stems in the next step.

What the counts can and cannot say (the S1 verdict still holds):

  * They are **practice**, mostly American home cooking. Rare means "not
    popular here", never "not food". Edibility stays hand-curated.
  * The rules are keywords on one sentence. They miss sentences that say
    "peel" without naming the tomato, and they guess at "remove" in a mixed
    sentence. The hand check in docs/research/s2-part-counts/ gives their
    accuracy. Read the numbers as sizes, not exact figures.
  * RecipeNLG's terms allow non-commercial research and educational use only.
    Only counts are written to the repository, never recipe text.

The corpus does not ship with the app. `resolve_csv` looks for it in a path
given on the command line, then $FOODPREP_RECIPENLG, then
data/corpus/recipenlg/full_dataset.csv in the repository (ignored by git).
"""

from __future__ import annotations

import csv
import json
import os
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator

from .corpus import REPO_ROOT, portable_source

RECIPENLG_ENV = "FOODPREP_RECIPENLG"
DEFAULT_CSV = REPO_ROOT / "data" / "corpus" / "recipenlg" / "full_dataset.csv"
EVIDENCE_PATH = Path(__file__).with_name("data") / "part_evidence.yaml"
RULES_VERSION = 1

CLASSES = ("used", "trimmed", "removed", "cue", "canned", "unclear")
# The recipe-level class is the first of these the recipe shows.
PRECEDENCE = CLASSES


class RecipeNLGNotFound(FileNotFoundError):
    """No RecipeNLG CSV where we looked."""


def resolve_csv(explicit: Path | str | None = None, *,
                env: dict[str, str] | None = None) -> Path:
    env = os.environ if env is None else env
    for source, value in (("the path given", explicit),
                          (f"${RECIPENLG_ENV}", env.get(RECIPENLG_ENV))):
        if value:
            path = Path(value).expanduser()
            if not path.is_file():
                raise RecipeNLGNotFound(f"{source} ({path}) is not a file.")
            return path
    if DEFAULT_CSV.is_file():
        return DEFAULT_CSV
    raise RecipeNLGNotFound(
        f"No RecipeNLG corpus found. Put full_dataset.csv from the official "
        f"download in {DEFAULT_CSV.parent} (ignored by git), set "
        f"{RECIPENLG_ENV}, or pass the file on the command line.")


# ---- rules -----------------------------------------------------------------

def _rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.I)


@dataclass(frozen=True)
class Ingredient:
    name: str
    # Does a recipe's ingredient list hold this ingredient at all?
    listed: re.Pattern[str]
    # Is the ingredient named in a sentence?
    named: re.Pattern[str]


# Broccoli rabe, broccolini and Chinese broccoli (gai lan) are other
# vegetables; they do not count as broccoli.
NOT_BROCCOLI = r"(?!\s*(rabe|raab|ni\b|flower|di rap|spigarello))"
_BROCCOLI = rf"(?<!chinese )(?<!chinese-style )broccoli{NOT_BROCCOLI}"

INGREDIENTS = {
    "tomato": Ingredient("tomato", _rx(r"tomato"), _rx(r"\btomato(e?s)?\b")),
    "broccoli": Ingredient("broccoli", _rx(_BROCCOLI), _rx(rf"\b{_BROCCOLI}\b")),
    "avocado": Ingredient("avocado", _rx(r"avocado(?!\s+oil)"),
                          _rx(r"\bavocado(e?s)?\b(?!\s+oil)")),
}

# A processed tomato product, not the fruit: these never have parts to remove.
TOMATO_PRODUCT = _rx(r"tomato(es)? (sauce|paste|juice|soup|ketchup|pur[eé]e|catsup|"
                     r"bouillon|powder|vegetable juice)|\bketchup\b|\bv-?8\b|salsa")


@dataclass(frozen=True)
class PartRule:
    ingredient: str
    part: str
    # The part's own words in a sentence.
    mention: re.Pattern[str]
    # Other ingredients with the same part word. If the recipe lists one of
    # these, a bare mention only counts when the sentence names our ingredient.
    # A part word right after one of them ("fennel seed", "bay leaf") is never ours.
    confusers: re.Pattern[str] | None = None
    # Sentences about the ingredient that remove the part without naming it:
    # "2 tomatoes, peeled" removes the skin.
    implicit_removed: re.Pattern[str] | None = None
    # Sentences that keep the part on purpose: "unpeeled tomatoes".
    implicit_kept: re.Pattern[str] | None = None
    # Only the ends or a tough layer come off, the part stays.
    trim: re.Pattern[str] | None = None
    # Part-specific cooking cues.
    cue: re.Pattern[str] | None = None
    # Does a "peel" verb on this part mean the part itself is gone? True for
    # skin; False for broccoli stems, where peeling prepares the stem.
    peel_removes: bool = False
    # Can a cook buy this step done ("canned peeled tomatoes")? Only the skin.
    can_be_canned: bool = False
    # The part a recipe means by default (florets, flesh). Cutting it off the
    # rest separates it for use; only an explicit discard removes it.
    default_part: bool = False

    @property
    def owner(self) -> re.Pattern[str] | None:
        """Text ending in another ingredient's name ("... fennel ")."""
        if self.confusers is None:
            return None
        return _rx(rf"(?:{self.confusers.pattern})[\w-]*\W+(?:[\w-]+\W+)?$")


HERBS = (r"parsley|cilantro|coriander|thyme|rosemary|dill|basil|mint|sage|tarragon|"
         r"oregano|marjoram|lemongrass|chives?")
SWEET_PEPPER = r"(bell|green|red|yellow|orange|sweet|roasted|anaheim|poblano) peppers?\b(?! flakes)"
CHILE = r"chil[ie]s?\b|chillies|jalape|serrano|poblano|habanero|chipotle"
OTHER_BRASSICA = r"cauliflower|romanesco|broccolini|broccoflower|rabe|raab|rapini|bok cho|pak cho|chinese broccoli|gai lan|spigarello|treviso"

RULES: tuple[PartRule, ...] = (
    PartRule(
        "broccoli", "florets",
        mention=_rx(r"\b(florets?|flowerets?|flowerettes?|flowers?|crowns?|tops)\b"),
        confusers=_rx(OTHER_BRASSICA),
        default_part=True,
    ),
    PartRule(
        "broccoli", "stems",
        mention=_rx(r"\b(stems?|stalks?)\b"),
        confusers=_rx(rf"{HERBS}|{OTHER_BRASSICA}|kale|chard|collard|spinach|mushroom|"
                      r"asparagus|celery|rhubarb|cherr|strawberr|grape|"
                      r"scallion|green onion|fennel|watercress|arugula"),
        trim=_rx(r"\bends?\b|bottoms?\b|\bbase\b|tough|outer (skin|layer|peel)|"
                 r"\b(outside|exterior|outer)\b|fibrous|woody|\bskin\b|"
                 r"\d+/?\d* ?inch|\bpeel|\bpare|\btrim|\bsplit"),
    ),
    PartRule(
        "broccoli", "leaves",
        mention=_rx(r"\b(leaves|leaf|leafy)\b(?! (shapes?|lettuce|parsley|spinach|lard))"),
        confusers=_rx(rf"{HERBS}|{OTHER_BRASSICA}|bay|lettuce|romaine|spinach|kale|"
                      r"cabbage|celery|lime|lemon|curry|banana|grape|fig|shiso|chard|"
                      r"collard|arugula|endive|radicchio|watercress|greens|kaffir|"
                      r"tea\b|nori|seaweed|pastry|phyllo|filo|herb"),
    ),
    PartRule(
        "tomato", "flesh",
        mention=_rx(r"\bflesh\b"),
        confusers=_rx(rf"fish|salmon|cod\b|chicken|avocado|mango|melon|eggplant|"
                      rf"aubergine|zucchini|courgette|garlic|onion|lemon|lime|orange|"
                      rf"squash|pumpkin|potato|peach|plum|{SWEET_PEPPER}|{CHILE}"),
        default_part=True,
    ),
    PartRule(
        "tomato", "seeds_and_gel",
        mention=_rx(r"\b(seeds?|seeded|deseed(ed)?|de-seed(ed)?|gel|"
                    r"seedy (pulp|center|part))\b"),
        confusers=_rx(rf"{SWEET_PEPPER}|{CHILE}|cucumber|sesame|poppy|mustard|"
                      r"celery|cl?ery|cumin|fennel|coriander|caraway|anise|cardamom|"
                      r"melon|squash|pumpkin|sunflower|pomegranate|flax|chia|"
                      r"vanilla|cherr|grape|papaya|lemon|lime|orange|nigella|"
                      r"dill|gelatin|jell-?o|eggplant|okra|pepper|bagel|\bbuns?\b|bread|"
                      r"\brolls?\b|watermelon|carraway"),
        implicit_removed=_rx(r"\b(seeded|deseeded|de-seeded|deseed|de-seed)\b|"
                             r"\bseed\b(?=\s*(,|&|and\b|the\b|them\b|tomato|\w+ tomato))|"
                             r"^\W*seed\b|\band seed\b|\bseed\b(?=\s*([.;]|$))|"
                             r"(remove|take out|scoop( out)?|discard) (the |all |any )?seeds|"
                             r"squeeze (\w+ ){0,3}out|\b(no|without|avoid( any)?) seeds"),
        implicit_kept=_rx(r"\bunseeded\b|leav\w* (\w+ ){0,2}seeds|"
                          r"no need to (\w+ ){0,4}(seed|get rid)|(do not|don't|nor|not) seed|"
                          r"(reserv|sav|keep)\w* (\w+ ){0,3}seeds"),
    ),
    PartRule(
        "tomato", "skin",
        mention=_rx(r"\bskins?\b|\bpeels\b"),
        confusers=_rx(rf"potato|{SWEET_PEPPER}|{CHILE}|peach|apricot|plum|"
                      r"nectarine|eggplant|onion|garlic|shallot|chicken|duck|"
                      r"turkey|pork|fish|salmon|sardine|almond|hazelnut|peanut|sausage|"
                      r"apple|pear\b|pears\b|cucumber|squash|zucchini|kiwi|mango|"
                      r"lemon|lime|orange|citrus|chickpea|fava|tortilla|beet|"
                      r"carrot|ginger|banana|avocado"),
        implicit_removed=_rx(r"\bpe[ea]l(ed|ing)?\b|\bskinned\b|"
                             r"\bskin\b(?=\s*(,|&|and\b|the\b|them\b|tomato|\w+ tomato))|"
                             r"^\W*skin\b|\bconcass"),
        implicit_kept=_rx(r"\bunpeeled\b|skins? on\b|with (the )?skins?\b(?! removed| off)|"
                          r"(leav|keep)\w* (\w+ ){0,5}skins?|skin salt|"
                          r"(do not|don't|no need to|nor|not) peel"),
        cue=_rx(r"until (the )?(\w+ )?skins? (\w+ )?(split|blister|burst|loosen|wrinkl|crack|"
                r"char|blacken|pop|shrivel|begin|start|break|pucker|is|are)|"
                r"\b(slit|pierce|prick|score)\w* (\w+ ){0,3}skins?|"
                r"skins? (\w+ )?(are|is|have|begin|start|will) (\w+ )?"
                r"(blister|char|split|burst|blacken|wrinkl|loosen|crack|to|pop)|"
                r"\b(an|shallow|small) ['\"]*x['\"]*|x[- ]shaped"),
        peel_removes=True,
        can_be_canned=True,
    ),
    PartRule(
        "tomato", "core",
        mention=_rx(r"\b(cores?|cored|coring)\b"),
        confusers=_rx(rf"apple|pear\b|pears\b|quince|pineapple|cabbage|lettuce|"
                      rf"{SWEET_PEPPER}|cauliflower|fennel|{CHILE}|zucchini|"
                      r"cucumber|iceberg|romaine|onion|radicchio|endive|spaghetti|pasta"),
        implicit_removed=_rx(r"\bcored\b|(?<!the )(?<!a )(?<!through )(?<!of )(?<!its )"
                             r"\bcor(e|ing)\b(?! of)|"
                             r"(remove|cut out) (the )?(stems?|cores?)"),
        implicit_kept=_rx(r"leav\w* (\w+ ){0,3}cores?|through (the )?core|"
                          r"fill\w* (\w+ ){0,2}cores?"),
    ),
    PartRule(
        "avocado", "flesh",
        mention=_rx(r"\b(flesh|pulp|meat)\b"),
        confusers=_rx(rf"fish|salmon|crab|lobster|shrimp|chicken|beef|pork|turkey|"
                      rf"\bmeat\b|sausage|mango|melon|papaya|tomato|eggplant|squash|"
                      rf"pumpkin|potato|coconut|lime|lemon|orange|{SWEET_PEPPER}|{CHILE}"),
        default_part=True,
    ),
    PartRule(
        "avocado", "skin",
        mention=_rx(r"\b(skins?|peels?(?!ed)|shells?|rinds?)\b"),
        confusers=_rx(rf"tomato|potato|{SWEET_PEPPER}|{CHILE}|onion|garlic|chicken|"
                      r"fish|salmon|lemon|lime|orange|citrus|mango|cucumber|tortilla|"
                      r"taco|tostad|potsticker|wonton|dumpling|mask|pie|tart|pastry|egg|"
                      r"shrimp|crab|lobster|nut|almond|"
                      r"pistachio|peanut|kiwi|banana|apple|pear\b|peach"),
        implicit_removed=_rx(r"\bpeel(ed|ing)?\b|\bskinned\b|"
                             r"scoop(ed)? (\w+ ){0,4}(out|from)|"
                             r"\bspoon(ed)? (\w+ ){0,3}(out|from)|"
                             r"\b(skin|shell)\b(?=\s*(,|&|and\b|the\b|them\b|avocado|\w+ avocado))|"
                             r"^\W*(skin|shell)\b|\b(and|,)\s*(skin|shell)\b(?! side)"),
        implicit_kept=_rx(r"(reserv|sav|keep|use)\w* (\w+ ){0,3}(shells?|skins?)|"
                          r"\b(into|in|fill|stuff)\w* (\w+ ){0,3}(shells?|skins?)|"
                          r"(shells?|skins?) (as|for) (\w+ ){0,2}(bowls?|cups?|serving|containers?|boats?)"),
        cue=_rx(r"(score|cut|slice|cross-?hatch)\w* (\w+ ){0,8}(to|through|thru|until|til|reach)\w* "
                r"(\w+ ){0,3}skin|not (to )?cut (through|thru) (the )?skin|in (its|the) skin"),
    ),
    PartRule(
        "avocado", "stone",
        mention=_rx(r"\b(pits?|stones?|seeds?)\b"),
        confusers=_rx(rf"peach|cherr|olive|date|mango|apricot|plum|nectarine|"
                      rf"pomegranate|sesame|poppy|mustard|cumin|fennel|coriander|"
                      rf"caraway|celery|sunflower|pumpkin|chia|flax|tomato|cucumber|"
                      rf"melon|papaya|grape|{SWEET_PEPPER}|{CHILE}|pepper|bagel|bread|"
                      r"stone[- ]ground|stoneware|fire|bbq|barbecue|grill"),
        implicit_removed=_rx(r"\b(pitted|seeded|stoned|de-?pitted|de-?stoned)\b|"
                             r"(?<!the )(?<!a )(?<!its )(?<!of )"
                             r"\b(pit|seed|stone)\b(?=\s*(,|&|and\b|the\b|them\b|avocado|\w+ avocado|[.;]|$))|"
                             r"^\W*(pit|seed|stone)\b|\b(and|,)\s*(pit|seed|stone)\b|"
                             r"pry\w* (\w+ ){0,2}(pits?|stones?|seeds?)|pops? out"),
        implicit_kept=_rx(r"(leav|keep|place|put|add|insert|bury|push|set)\w* "
                          r"(\w+ ){0,3}(pits?|stones?|seeds?) (\w+ ){0,3}(in|into|on|back)"),
    ),
)

RULES_BY_KEY = {(r.ingredient, r.part): r for r in RULES}

REMOVED = _rx(r"discard|throw (them |it )?(away|out)|\bremov(e|ed|ing)\b|"
              r"(cut|trim|break|snap|pull|pick|slice|tear|rub|slip|pinch|take|"
              r"twist|scrape|strip)(ped|med|ping|ming|ing|s|ed|n)? (\w+ ){0,2}(off|away|out)\b|"
              r"\bno (\w+ )?(skins?|pits?|seeds?|stones?|peel|cores?)\b|slides? off|(don.t|do not|never|not) use\b|(spoon|push)\w* (\w+ ){0,3}out|get rid of|\bto loosen|"
              r"slip(ped|s)? (the |their )?skins?|\bdetach|\beliminat|"
              r"squeeze(d)? (\w+ ){0,3}out|scoop(ed)? (\w+ ){0,3}out|strain(ed)? (\w+ ){0,3}out|"
              r"press(ed)? (\w+ ){0,3}out|shake (\w+ ){0,3}out|"
              r"(reserve|save|keep) (\w+ ){0,4}for (another|other|a different|later) "
              r"(use|dish|recipe|purpose)|compost|\bwithout (the |their )?"
              r"(stems?|stalks?|skins?|seeds?|cores?|leaves|peel)")
# Only these take a default part (florets, flesh) out of the dish.
_OTHER_OBJECT = (r"(?!\w*\s+(\w+\s+){0,2}(stems?|stalks?|leaves|seeds?|skins?|cores?|"
                 r"pits?|stones?|peels?|shells?|bones?|membranes?|rinds?)\b)")
DISCARD = _rx(rf"discard{_OTHER_OBJECT}|throw (them |it )?(away|out){_OTHER_OBJECT}|compost|"
              r"for (another|other|a different|later) (use|dish|recipe|purpose)")
OTHER_PART = _rx(r"\b(stems?|stalks?|leaves|seeds?|skins?|cores?|pulp|water|juices?|"
                 r"pips|roots|peels?|them|pits?|stones?|shells?|bones?|membranes?|rinds?)\b")
# "Remove from the heat" moves the pot, it does not take the part away.
NOT_REMOVAL = _rx(r"^\W*(\w+ ){0,4}from (the )?(heat|pan|oven|skillet|pot|water|wok|grill|"
                  r"burner|stove|broiler|bowl|baking|sheet|steamer|microwave|liquid|fire)")
WINDOW = 45  # characters between a removal verb and the part it acts on


def _owned(sentence: str, start: int, owner: re.Pattern[str] | None) -> bool:
    """Is the word at `start` another ingredient's part ("fennel seed")?"""
    return bool(owner and owner.search(sentence[max(0, start - 40):start]))


def _near(a: re.Pattern[str], b: re.Pattern[str], sentence: str,
          skip_after: re.Pattern[str] | None = None,
          blocker: re.Pattern[str] | None = None,
          owner: re.Pattern[str] | None = None) -> bool:
    """Does a match of `a` sit within WINDOW characters of a match of `b`?

    `skip_after` drops a match of `a` whose following text matches it
    ("remove from the heat"). `blocker` drops a pair with another noun between
    them ("peel the onions and add the tomatoes"). `owner` drops a match of
    either that belongs to another ingredient ("fennel seed")."""
    spans_b = [m.span() for m in b.finditer(sentence)
               if not _owned(sentence, m.start(), owner)]
    for m in a.finditer(sentence):
        if skip_after and skip_after.search(sentence[m.end():]):
            continue
        if _owned(sentence, m.start(), owner):
            continue
        for s0, s1 in spans_b:
            if not (m.start() - WINDOW <= s1 and s0 <= m.end() + WINDOW):
                continue
            between = sentence[min(m.end(), s1):max(m.start(), s0)]
            if blocker and blocker.search(between):
                continue
            return True
    return False


PEEL_OFF = _rx(r"\bpe[ea]l(ed|ing|s)?\b")
USED = _rx(r"\b(add|adding|added|cook|chop|chopped|slice|sliced|dice|diced|"
           r"cut\b[^.;]{0,40}\b(into|in)|"
           r"julienne|matchstick|shred|grate|mince|stir|toss|steam|boil|blanch|parboil|"
           r"simmer|saut[eé]e?d?|roast|split|quarter|spears?|planks?|slices?|bake|grill|fry|fried|puree|pur[eé]e|blend|mix|"
           r"combine|place|arrange|serve|use|include|reserve|keep|tender|crisp|"
           r"garnish|dry|dried|dehydrat|powder|grind|ground|pulveri[sz]e|coins?|rounds|"
           r"pieces|cubes?|together|with|scoop|mash|smash|chuck|wash|rinse|separate|break|divide|spread|lay|"
           r"put|set aside|drain|squeeze|pour|sprinkle|top|season|drizzle|layer|"
           r"transfer|return|reheat|heat|warm|thaw|cool|process|measure|brown)\b")
CANNED_WORD = _rx(r"\b(cans?|canned|tins?|tinned|jars?|cartons?|pkg|packages?|"
                  r"solid[- ]pack)\b")


def _canned(sentence: str) -> bool:
    """An ingredient line for a bought product. "4 tomatoes, peeled (or 1 can)"
    is fresh with a canned alternative, so a can after an "or" does not count;
    weights ("6 oz. each") are not cans."""
    m = CANNED_WORD.search(sentence)
    return bool(m) and not re.search(r"\bor\b", sentence[:m.start()], re.I)

# How a used part is cooked, mapped onto our technique ids.
TECHNIQUES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("stir_fry", _rx(r"stir[- ]?fr|\bwok\b")),
    ("steam", _rx(r"\bsteam")),
    ("roast", _rx(r"\broast")),
    ("saute", _rx(r"saut[eé]")),
    ("boil", _rx(r"\b(boil|blanch|parboil|simmer)")),
    ("bake", _rx(r"\bbak(e|ed|ing)\b|casserole|gratin")),
    ("grill", _rx(r"\bgrill|broil")),
    ("fry", _rx(r"(?<!stir[- ])\bfr(y|ied)\b|tempura|batter")),
    ("soup", _rx(r"\bsoup|puree|pur[eé]e|\bblend")),
    ("raw", _rx(r"\braw\b|slaw|salad")),
    ("dry", _rx(r"\bdr(y|ied)\b(?! (white|red|wine|sherry|mustard|vermouth))|"
                r"dehydrat|powder|\bgrind|ground\b")),
)


# ---- reading ---------------------------------------------------------------

_SENT_SPLIT = re.compile(r"(?<=[.;!?])\s+")


@dataclass
class Recipe:
    source: str
    ingredients: list[str]
    directions: list[str]

    def sentences(self) -> Iterator[tuple[str, str]]:
        """(kind, sentence) for every ingredient line and direction sentence."""
        for line in self.ingredients:
            yield "ingredient", line
        for step in self.directions:
            for s in _SENT_SPLIT.split(step):
                if s.strip():
                    yield "direction", s.strip()


def read_recipes(path: Path | str, keep: re.Pattern[str]) -> Iterator[Recipe]:
    """Recipes whose ingredient lines match `keep`. The CSV is 2.2 million rows,
    so the filter runs on the raw field before any JSON is parsed."""
    csv.field_size_limit(2**31 - 1)
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        idx = {h: i for i, h in enumerate(header)}
        for missing in ("ingredients", "directions", "source"):
            if missing not in idx:
                raise ValueError(f"{path} is not a RecipeNLG CSV: no {missing!r} column")
        i_ing, i_dir, i_src = idx["ingredients"], idx["directions"], idx["source"]
        for row in reader:
            if not keep.search(row[i_ing]):
                continue
            yield Recipe(row[i_src], json.loads(row[i_ing]), json.loads(row[i_dir]))


def count_rows(path: Path | str) -> Counter[str]:
    """Total recipes per source, for the scope line."""
    csv.field_size_limit(2**31 - 1)
    totals: Counter[str] = Counter()
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        i_src = next(reader).index("source")
        for row in reader:
            totals[row[i_src]] += 1
    return totals


# ---- classifying -----------------------------------------------------------

def _mentions_part(rule: PartRule, ing: Ingredient, sentence: str,
                   recipe_has_confuser: bool) -> bool:
    owner = rule.owner
    if not any(not _owned(sentence, m.start(), owner)
               for m in rule.mention.finditer(sentence)):
        return False
    if ing.named.search(sentence):
        return True
    return not recipe_has_confuser


STALK_UNIT = _rx(r"^\W*([\d/.,½¼¾-]+\s*|a\s+|one\s+|two\s+|three\s+|several\s+|few\s+)"
                 r"(\(?[^)]*\)\s*)?(small|medium|large|lrg|big|fresh|whole|bunch(es)?\s+of)?\s*"
                 r"(stalks?|stems?|spears?)\s+(of\s+)?(fresh\s+|raw\s+|chopped\s+)?broccoli")


@lru_cache(maxsize=None)
def _taken_from(rule: PartRule) -> re.Pattern[str]:
    """ "Cut the cores from the tomatoes", "trim large leaves from broccoli":
    a verb, the part as its object, then from/out/off."""
    return _rx(rf"\b(cut|take|trim|scoop|pry|pop|pull|spoon|push|tear)\w*\s+"
               rf"(\w+\s+){{0,2}}(?:{rule.mention.pattern})\s+(\w+\s+)?(from|out|off|away)\b")


def classify(rule: PartRule, sentence: str, kind: str,
             recipe_has_confuser: bool) -> str | None:
    """The class of one sentence for one part, or None if it is not about the part."""
    ing = INGREDIENTS[rule.ingredient]
    if rule.ingredient == "tomato" and TOMATO_PRODUCT.search(sentence) \
            and not re.search(r"\btomato(e?s)?\b(?! (sauce|paste|juice|soup|pur))", sentence, re.I):
        return None
    owner = rule.owner
    if rule.part == "stems" and STALK_UNIT.search(sentence) \
            and len(rule.mention.findall(sentence)) == 1:
        # "2 stalks broccoli" measures whole spears; it says nothing about stems.
        return None
    explicit = _mentions_part(rule, ing, sentence, recipe_has_confuser)
    implicit = (not explicit and ing.named.search(sentence) is not None
                and rule.implicit_removed is not None)
    if not explicit and not implicit:
        return None

    def gone() -> str:
        if kind == "ingredient" and rule.can_be_canned and _canned(sentence):
            return "canned"
        return "removed"

    # "Fill the taco shell": a part word owned by another ingredient cannot
    # make the sentence keep ours, so blank those words before the keep check.
    unowned = rule.mention.sub(
        lambda m: "#" * len(m.group(0)) if _owned(m.string, m.start(), owner) else m.group(0),
        sentence)
    if rule.implicit_kept and any(
            _near(rule.implicit_kept, target, unowned, blocker=rule.confusers, owner=owner)
            for target in (rule.mention, ing.named)):
        return "used"
    one_word_removal = rule.implicit_removed is not None and any(
        _near(rule.implicit_removed, target, sentence, blocker=rule.confusers, owner=owner)
        for target in ((ing.named,) if implicit else (rule.mention, ing.named)))
    if implicit:
        return gone() if one_word_removal else None

    # The part is named in the sentence. "Seeded" and "cored" name the part
    # and remove it in one word.
    if one_word_removal:
        return gone()
    removed = _near(REMOVED, rule.mention, sentence, NOT_REMOVAL, owner=owner) or (
        rule.peel_removes and _near(PEEL_OFF, rule.mention, sentence, owner=owner))
    removed = removed or bool(_taken_from(rule).search(sentence))
    if removed and rule.default_part:
        # Cutting florets off the stalk separates them for use. Only a discard
        # that is not about another part ("stems discarded") removes them.
        removed = any(
            not OTHER_PART.search(sentence[max(0, m.start() - 25):m.start()])
            and _near(re.compile(re.escape(m.group(0)), re.I), rule.mention, sentence,
                      blocker=OTHER_PART, owner=owner)
            for m in DISCARD.finditer(sentence))
        if not removed:
            return "used"
    if removed and rule.trim and rule.trim.search(sentence) \
            and not re.search(r"discard (the |all )?(stems?|stalks?)\b|"
                              r"(stems?|stalks?) (for another|for other)", sentence, re.I):
        return "trimmed"
    if removed:
        return gone()
    if rule.cue and rule.cue.search(sentence):
        return "cue"
    if rule.trim and rule.trim.search(sentence) and PEEL_OFF.search(sentence):
        # "Peel the stems": the stem is prepared, not thrown away.
        return "trimmed"
    if kind == "ingredient":
        # A part listed as an ingredient goes into the dish.
        return "used"
    if USED.search(sentence):
        return "used"
    return "unclear"


def techniques_in(sentence: str) -> list[str]:
    return [name for name, rx in TECHNIQUES if rx.search(sentence)]


@dataclass
class PartTally:
    ingredient: str
    part: str
    recipes: Counter[str] = field(default_factory=Counter)
    by_source: dict[str, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    sentences: Counter[str] = field(default_factory=Counter)
    techniques: Counter[str] = field(default_factory=Counter)

    @property
    def mentioning(self) -> int:
        return sum(self.recipes.values())


@dataclass
class Sample:
    """A sentence kept for the hand check. Stays in the gitignored corpus folder."""
    ingredient: str
    part: str
    cls: str
    kind: str
    sentence: str


def tally(recipes: Iterable[Recipe], rules: Iterable[PartRule] = RULES, *,
          sample_per_class: int = 0, seed: int = 7
          ) -> tuple[dict[tuple[str, str], PartTally], Counter[str], list[Sample]]:
    """Count every part across the recipes.

    Returns the tallies, the number of recipes listing each ingredient (as
    'tomato', 'tomato:fresh', 'broccoli'), and a reservoir sample of classified
    sentences per part and class for the hand check."""
    rules = list(rules)
    tallies = {(r.ingredient, r.part): PartTally(r.ingredient, r.part) for r in rules}
    baselines: Counter[str] = Counter()
    rng = random.Random(seed)
    reservoirs: dict[tuple[str, str, str], list[Sample]] = defaultdict(list)
    seen: Counter[tuple[str, str, str]] = Counter()

    for recipe in recipes:
        ing_text = "\n".join(recipe.ingredients)
        active = []
        for name, ing in INGREDIENTS.items():
            if ing.listed.search(ing_text):
                baselines[name] += 1
                if name == "tomato" and any(
                        ing.named.search(l) and not TOMATO_PRODUCT.search(l)
                        for l in recipe.ingredients):
                    baselines["tomato:fresh"] += 1
                active.append(name)
        if not active:
            continue
        for rule in rules:
            if rule.ingredient not in active:
                continue
            has_confuser = bool(rule.confusers and rule.confusers.search(ing_text))
            found: set[str] = set()
            for kind, sentence in recipe.sentences():
                cls = classify(rule, sentence, kind, has_confuser)
                if cls is None:
                    continue
                found.add(cls)
                t = tallies[(rule.ingredient, rule.part)]
                t.sentences[cls] += 1
                if cls in ("used", "trimmed"):
                    t.techniques.update(techniques_in(sentence))
                if sample_per_class:
                    key = (rule.ingredient, rule.part, cls)
                    seen[key] += 1
                    s = Sample(rule.ingredient, rule.part, cls, kind, sentence[:300])
                    box = reservoirs[key]
                    if len(box) < sample_per_class:
                        box.append(s)
                    else:
                        j = rng.randrange(seen[key])
                        if j < sample_per_class:
                            box[j] = s
            if found:
                best = next(c for c in PRECEDENCE if c in found)
                t = tallies[(rule.ingredient, rule.part)]
                t.recipes[best] += 1
                t.by_source[recipe.source][best] += 1

    samples = [s for box in reservoirs.values() for s in box]
    return tallies, baselines, samples


# ---- evidence level --------------------------------------------------------

RARE_SHARE = 0.01   # used in fewer than 1% of the ingredient's recipes
MIN_USED = 30       # ... or fewer than 30 recipes in all


def evidence_level(t: PartTally, ingredient_recipes: int, *, default_part: bool = False) -> str:
    """default / used / rarely_used / removed / not_found: practice only, never
    edibility. A default part (florets, flesh) is what the ingredient's name
    already means, so recipes seldom name it and rarity says nothing."""
    if default_part and t.recipes["removed"] <= t.recipes["used"] + t.recipes["trimmed"]:
        return "default"
    if t.mentioning == 0:
        return "not_found"
    kept = t.recipes["used"] + t.recipes["trimmed"]
    gone = t.recipes["removed"]
    if gone > kept:
        return "removed"
    if kept < MIN_USED or kept < RARE_SHARE * ingredient_recipes:
        return "rarely_used"
    return "used"


def to_record(t: PartTally, baselines: Counter[str]) -> dict:
    base = baselines["tomato:fresh"] if t.ingredient == "tomato" else baselines[t.ingredient]
    return {
        "ingredient": t.ingredient,
        "part": t.part,
        "evidence_level": evidence_level(
            t, base, default_part=RULES_BY_KEY[(t.ingredient, t.part)].default_part),
        "recipes_mentioning": t.mentioning,
        "recipes": {c: t.recipes[c] for c in CLASSES},
        "by_source": {src: {c: n[c] for c in CLASSES}
                      for src, n in sorted(t.by_source.items())},
        "sentences": {c: t.sentences[c] for c in CLASSES},
        "techniques_when_used": dict(t.techniques.most_common()),
    }


def build_evidence(csv_path: Path | str, totals: Counter[str],
                   tallies: dict[tuple[str, str], PartTally],
                   baselines: Counter[str], *, search_date: str,
                   hand_check: dict | None = None) -> dict:
    return {
        "corpus": {
            "corpus_id": "recipenlg",
            "name": "RecipeNLG",
            "scope": f"{sum(totals.values())} recipes in full_dataset.csv",
            "recipes_by_source": dict(sorted(totals.items())),
            "source_path": portable_source(Path(csv_path).parent),
            "terms": "non-commercial research and educational use only; counts only, no recipe text",
            "search_date": search_date,
            "rules_version": RULES_VERSION,
        },
        "baselines": {
            "tomato": baselines["tomato"],
            "tomato_fruit": baselines["tomato:fresh"],
            "broccoli": baselines["broccoli"],
            "avocado": baselines["avocado"],
        },
        "thresholds": {"rare_share": RARE_SHARE, "min_used": MIN_USED},
        "parts": [to_record(tallies[(r.ingredient, r.part)], baselines) for r in RULES],
    }


HEADER = """\
# Corpus practice per ingredient part (ADR 0002): GENERATED, do not hand-edit.
#
# Regenerate: py -3.11 scripts/count_part_evidence.py [path-to-full_dataset.csv]
#
# What each part's sentences say happens to it in RecipeNLG, one sentence at a
# time: used, trimmed (only ends or tough skin off), removed, cue (a cooking
# signal only), canned (bought already done) or unclear. `recipes` counts each
# recipe once, under the strongest class it shows (in that order).
#
# This is practice, mostly American home cooking. A part that is removed or
# rarely used here can still be food; edibility is curated in tomato.yaml.
# The keyword rules' accuracy is in docs/research/s2-part-counts/README.md.
#
# RecipeNLG's terms allow non-commercial research and educational use only.
# Only counts are kept here, never recipe text.
"""


def write_evidence(evidence: dict, path: Path = EVIDENCE_PATH) -> None:
    import yaml
    path.write_text(HEADER + yaml.safe_dump(evidence, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")


def load_evidence(path: Path = EVIDENCE_PATH) -> dict[tuple[str, str], dict]:
    """Part records keyed by (ingredient, part); empty when the file is absent."""
    if not path.is_file():
        return {}
    import yaml
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {(p["ingredient"], p["part"]): p for p in data.get("parts", [])}


def write_samples(samples: list[Sample], path: Path) -> None:
    """Hand-check sheet. Holds recipe text, so it belongs in the gitignored
    corpus folder, never in the repository."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ingredient", "part", "class", "kind", "sentence", "agree"])
        for s in sorted(samples, key=lambda s: (s.ingredient, s.part, s.cls)):
            w.writerow([s.ingredient, s.part, s.cls, s.kind, s.sentence, ""])
