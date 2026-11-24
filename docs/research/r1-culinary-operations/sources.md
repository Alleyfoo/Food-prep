# Sources

How these sources were used, plainly:

- **Operation definitions** (what julienne or monder is, what it is for) come
  from the standard references below and from general culinary knowledge.
  They are cited as the places where these definitions are standard, **not**
  with page numbers. Nobody checked a page this round.
- **Web sources** (`web_…`) were checked this round by a research agent:
  about 40 searches on 2026-11-24. Each URL appeared in its search results;
  most pages were judged from their snippets, not read in full. They support
  two things: whether a specific preparation is established practice, and the
  safety facts.
- **Applicability rules and property values** (`part_properties.yaml`) are
  culinary judgement by the author (Claude), informed by these sources. They
  are not cited facts.

## Reference works

| Id | Source | Used for |
| --- | --- | --- |
| `escoffier` | Auguste Escoffier, *Le Guide Culinaire* (1903); English *A Guide to Modern Cookery* (1907, public domain) | Classical French terms: cuts, glacer, monder, consommé, fouler, parer and parures |
| `larousse` | *Larousse Gastronomique* (various editions) | French terminology and definitions |
| `cia` | The Culinary Institute of America, *The Professional Chef* | Knife cuts, cooking methods, breading, standard preparations |
| `pepin` | Jacques Pépin, *La Technique* (1976) / *Jacques Pépin's Complete Techniques* | Peeling and trimming; already referenced in the S1 note |
| `mcgee` | Harold McGee, *On Food and Cooking* (2004 revision) | Mechanisms: browning, emulsions, gels, extraction, why vegetable peels are not zest |
| `modernist` | Myhrvold, Young and Bilet, *Modernist Cuisine* (2011) | Gels, smoking |
| `peterson` | James Peterson, *Sauces* | Liaisons, monter au beurre |
| `noma` | René Redzepi and David Zilber, *The Noma Guide to Fermentation* (2018) | Lacto-fermentation of vegetables |
| `steam_culinary` | Existing evidence source in tomato.yaml | Steaming and blanching green vegetables |
| `roast_culinary` | Existing evidence source in tomato.yaml | Roasting |
| `usda_tomato` | Existing evidence source in tomato.yaml (USDA home canning) | Canning |

## Safety and technique facts (checked this round)

| Id | Source | Fact |
| --- | --- | --- |
| `cdc_botulism` | CDC, botulism consumer guidance, https://www.cdc.gov/botulism/consumer.html ; Oregon State Extension, https://extension.oregonstate.edu/food/preservation/herbs-vegetables-oil-sp-50-701 | Homemade garlic, herb or vegetable oils: refrigerate and use within 4 days, or freeze. One OSU page said "up to 3 weeks"; the stricter 4 days is used |
| `nchfp` | National Center for Home Food Preservation | Pickling, fermentation and canning safety; low-acid vegetables need a pressure canner |
| `vt_fermentation` | Virginia Tech Extension FST-328, https://pubs.ext.vt.edu/FST/FST-328/FST-328.html ; Illinois Extension fermentation handout, https://extension.illinois.edu/sites/default/files/fermentation_handout_2020.pdf | Salt for fermentation: 2–3% is a practitioner norm; extension sources range from 1 to 5% (sauerkraut 2.25–2.5%). Below 2% risks spoilage |
| `poison_squash` | Poison Control, https://www.poison.org/articles/toxic-squash-syndrome-if-it-s-bitter-it-s-not-dinner ; PNW Handbooks, https://pnwhandbooks.org/plantdisease/host-disease/squash-cucurbita-spp-toxic-squash-toxic-zucchini | Very bitter courgette: spit out and discard the fruit; cooking does not destroy cucurbitacin |
| `avocado_seed` | UC ANR, https://ucanr.edu/node/99767 ; Healthline, https://www.healthline.com/nutrition/eating-avocado-seed | The avocado seed is not established as safe to eat |
| `carrot_greens` | https://gardenbetty.com/are-carrot-tops-toxic-the-short-answer-no/ ; FoodPrint, https://foodprint.org/?p=4851 | Carrot greens and broccoli leaves are edible. The risk is wild look-alikes (hemlock). Broccoli leaves have only blog and FoodPrint sources, nothing official |
| `wiki_knife_cuts` | https://en.wikipedia.org/wiki/List_of_culinary_knife_cuts ; https://www.webstaurantstore.com/article/796/types-of-knife-cuts.html ; https://rouxbe.com/tips-techniques/495-types-of-knife-cuts | Cut dimensions. Sources disagree on lengths and on bâtonnet thickness |

## Existing practice (checked this round)

Status, as the research agent judged it from what it found:

- **established:** widely documented;
- **niche:** documented in zero-waste, chef or blog sources but uncommon;
- **no evidence found:** after one or two searches;
- **contradicted:** sources say it fails.

| Id | Preparation | Status | Sources |
| --- | --- | --- | --- |
| `web_b1` | Broccoli stem, peeled, as noodles or ribbons | established | https://inspiralized.com/how-to-spiralize-broccoli-garlic-broccoli-noodles-with-toasted-pine-nuts/ |
| `web_b2` | Broccoli stem **peel** dried and ground | no evidence found (powders of whole stalks and leaves exist) | https://foodprint.org/?p=4851 ; CSIRO broccoli powder, https://www.foodnavigator.com/Article/2020/03/27/Broccoli-coffee-and-pills-CSIRO-and-Hort-Innovation-create-ingredient-from-edible-vegetable-waste/ |
| `web_b3` | Broccoli leaf chips | niche | https://www.motherearthnews.com/real-food/nutritious-snacks-zm0z13aszhun/ ; https://edibleventuracounty.ediblecommunities.com/recipes/roasted-brassica-leaves |
| `web_b4` | Pickled broccoli stems | established (as julienne: niche) | https://www.foodnetwork.com/recipes/food-network-kitchen/pickled-broccoli-stems-3363778 ; https://waresofknutsford.co.uk/pickled-broccoli-stems |
| `web_b5` | Blanched, puréed, sieved broccoli sauce | established | https://onceuponachef.com/?p=24385 |
| `web_b6` | Lacto-fermented broccoli stems | niche | https://www.myfermentation.com/vegetables-and-nuts/pickled-produce-stems-ends-recipes-zm0z20uzbut |
| `web_c1` | Carrot juice pulp crackers | established (crackers) | https://foodrevolution.org/recipes/dehydrated-juice-pulp-crackers/ ; https://recipes.excaliburdehydrator.com/recipe/carrot-pulp-crackers/ |
| `web_c2` | Carrot peel crisps | niche | https://lovefoodhatewaste.ca/messageboard/carrot-peel-chips/ ; Dan Barber's vegetable chips, https://www.tastingtable.com/687150/recipe-vegetable-chips-blue-hill-restaurant-dan-barber/ |
| `web_c3` | Carrot ribbons as pasta | established | https://food52.com/blog/17594-quick-cooking-carrot-ribbons-to-one-up-your-zucchini-noodles |
| `web_c4` | Carrot-top chimichurri or pesto | established | https://www.loveandlemons.com/carrot-greens-chimichurri/ |
| `web_c5` | Carrot juice reduced and mounted with butter | established (chef technique) | https://foragerchef.com/carrots-glazed-in-carrot-juice-with-wild-carrot-flowers-and-seeds/ ; https://www.gastronomixs.com/en/components/carrot-reduction |
| `web_c6` | Carrot peel powder | niche | https://www.healthycanning.com/carrot-peel-powder |
| `web_z1` | Courgette **skin** ribbons as a component of their own | no evidence found (the all-skin first strip is usually discarded) | https://www.thewickednoodle.com/zucchini-ribbons/ |
| `web_z2` | Grated courgette salted and squeezed | established | https://www.foodnetwork.com/recipes/food-network-kitchen/zucchini-fritters-13025807 |
| `web_z3` | Liquid from salted courgette as broth or drink | niche | https://www.sevendaysvt.com/food-drink/farmers-market-kitchen-nutty-carrot-zucchini-water-soup-2424257/ |
| `web_z4` | Courgette noodles | established | https://inspiralized.com/how-to-avoid-watery-and-soggy-zucchini-noodles/ |
| `web_z5` | Dried courgette chips | established | https://downshiftology.com/recipes/zucchini-chips/ |
| `web_z6` | Seedy core of large courgette as thickener | no evidence found; sources advise removing it | https://ask.metafilter.com/317993/What-are-your-favourite-marrow-recipes-The-vegetable-not-bone |
| `web_t1` | Tomato skin powder | niche, well documented | https://ucanr.edu/program/uc-master-food-preserver-program/article/making-and-using-dehydrated-tomato-skins-august ; https://brooklynfarmgirl.com/how-to-make-tomato-powder-out-of-tomato-skins |
| `web_t2` | Clear tomato water, tomato consommé | established (chef) | https://jamesbeard.org/recipes/heirloom-tomato-consomme-with-goat-cheese-ravioli ; https://lighter.rouxbe.com/recipes/5144-tomato-consomme |
| `web_t3` | Tomato seed gel as vinaigrette | niche (vinaigrettes with seeds exist; no dedicated technique) | https://www.americastestkitchen.com/lessons/articles/2330-the-science-of-why-tomato-gel-tastes-so-good |
| `web_t4` | Tomato skin crisps | niche | https://www.chowhound.com/1792772/tomato-skin-chips/ |
| `web_t5` | Stock from tomato cores and scraps | established (usually mixed scraps) | https://www.cspinet.org/recipe/vegetable-stock |
| `web_a1` | Avocado eggless "mayonnaise" | established (closer to a purée than an emulsion) | https://www.mydarlingvegan.com/vegan-avocado-mayo |
| `web_a2` | Quick-pickled firm avocado | established (must be very firm) | https://www.americastestkitchen.com/recipes/12233-pickled-avocado |
| `web_a3` | Grilled avocado | established | https://www.fifteenspatulas.com/grilled-avocado/ |
| `web_a4` | Breaded fried avocado | established | https://www.loveandlemons.com/avocado-fries ; https://en.wikipedia.org/wiki/Deep-fried_avocado |
| `web_a5` | Dried avocado | contradicted at home (bitter, rancid) | https://www.tastingtable.com/1172723/is-it-possible-to-make-dehydrated-avocado |

## Within the project

- `docs/research/s2-part-counts/README.md`: what RecipeNLG cooks do with each
  part (the `usually_discarded` values for broccoli leaves and tomato parts).
- `docs/research/s3-generated-possibilities/README.md` and
  `s4-family-analysis/README.md`: the family generator that operations now
  feed.
