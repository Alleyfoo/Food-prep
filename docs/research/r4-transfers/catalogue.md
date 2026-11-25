# R4 step 1: the Lidl Finland ingredient boundary

**Checked 2026-11-24** on Lidl Finland's own sites: lidl.fi (offers,
product, brand and assortment pages), reseptit.lidl.fi, corporate.lidl.fi,
and Lidl Suomi's own press releases on sttinfo.fi. The page-by-page record,
with every URL, how it was read and the pages that failed, is
`lidl-pages.md`. The ids L1-L18 below are cited by `transfers.yaml` and
`sources.md`.

## Method, and the limit that shapes every answer

- **lidl.fi does not publish the regular range.** Lidl says the
  *vakiovalikoima* is about 3000 products, and that some stores carry a basic
  range and others an extended one (L11). The category pages, the site search
  and the product pages show **current offers only**; a search for *maito*
  returns no milk, *herne* and *kikherne* return nothing (`lidl-pages.md`).
- **Offer pages are removed when the offer ends** (8 of 8 old product and
  offer URLs re-opened returned 404). Past offers survive only as
  search-engine snippets, read through a summarising search tool and mostly
  without a year. They are marked *snippet*: weaker evidence.
- So **"not found on lidl.fi" does not mean "not sold"**, and for most
  staples it is the expected outcome. Status labels:
  - **regular**: a current product page with a standing (non-offer) price, a
    Lidl statement naming the product or brand range, or recall notices;
  - **seasonal**: offers that recur in a season (dates from snippets);
  - **campaign**: seen once, in a themed campaign;
  - **not found**: nothing on Lidl's sites. Unknown, not absent.
- Pages read in the built-in browser were read in full; WebFetch and
  WebSearch return summaries (said per row in `lidl-pages.md`). Cookies:
  non-essential declined; nothing signed in.

**The settling check is a shelf visit or the Lidl Plus app.** Until then the
transfers below carry their availability as a stated condition, not a fact.

## What the transfers need, by status

| Id | Item | Status | What Lidl's pages show |
| --- | --- | --- | --- |
| L1 | Dried split peas, dried chickpeas, lentils | **campaign** | "Golden Sun Luomulinssit tai -herneet": chickpea, *halkaistu herne*, red or green lentil, organic, 500 g, in an "Edulliset vihreät valinnat" campaign (snippet, year not shown, page 404). Lidl's own pulse brands are Golden Sun (dry) and Freshona (canned) (L12); lentils are sold (L13) |
| L1 | Whole dried yellow or green peas, *hernerouhe* | **not found** | No page, snippet or press release. "Kotimainen herne" (July 2026) is fresh peas in the pod |
| L12 | Canned chickpeas | regular (very likely) | "Freshona kikherneet suolavedessä" (snippet); Freshona brand confirmed; Lidl recipes call for chickpeas by the can |
| - | Chickpea flour, dried fava, *härkäpapurouhe* | not found | Only Härkis (cooked fava product) inside a Lidl bakery pie |
| L2 | Kale (*lehtikaali*) | **seasonal, Aug-Oct** | "Kotimainen lehtikaali", **curly, 100 g or 200 g bags** of loose leaves; offers 19-22.8, 15-18.9, from 20.10 (snippets, no year). Lidl recipes: "1 pss lehtikaali", "Puhdista lehtikaalit ruodeista" (L18). No bunch, no *silppu* seen |
| - | Cavolo nero (*mustakaali*), savoy (*kurttukaali*) | not found | - |
| L3 | White cabbage (*keräkaali*) | seasonal (Nov offer seen) | "Kotimainen keräkaali", loose per kg (snippet). Lidl recipes for kaalikääryleet and kaalilaatikko use it |
| L5 | Rutabaga (*lanttu*) | **seasonal, Sept-Dec** | "Kotimainen lanttu" (also organic), loose per kg; offers 29.9-2.10 and 9-12.12 (snippets) |
| L6 | Potatoes, floury and all-purpose | **regular** | "Kotimainen jauhoinen peruna", "Kotimainen yleisperuna", 2 kg, 1,49 € standing price (current product pages). Waxy only as a named variety (Jazzy) in a past offer. New potatoes from May |
| L7 | Milk, cream, butter | **regular** (brand statement) | All Lidl FI milks, creams and butters are Pohjolan Meijeri (L7); lactose-free butter 500 g on a current page; only lactose-free *ruokakerma* seen by name; *kuohukerma* not named |
| L14 | Grated cheese | regular (probably) | "Milbona juustoraaste" 500 g (snippet, page 404) |
| L4 | Broccoli | **frozen regular; fresh head not found** | "Parsakaali", frozen, 500 g, Spain, 1,69 € standing price (current page): florets, so **no stems**. No fresh head on any Lidl page |
| L15 | Carrots | regular (probably) | "Kotimainen porkkana" 1 kg, 0,99 € standing price in snippets |
| L8 | Onions | regular (probably), as a mix | "Kotimainen sipuli-mix" 1 kg yellow and red (snippet); red onion 500 g. Large or jumbo onions: not found |
| L9 | Courgette | spring-summer offers | "Kesäkurpitsa", Spain, per kg, standing price 1,99 €/kg in a May 2026 snippet |
| L10 | Eggs | **regular** | All fresh eggs are Finnish free-range or organic; recall notices name M10, L15, M15 boxes |
| L16 | Oat flakes | regular | Myllykivi (Lidl's own brand) |
| L17 | Minced meat | current batch offer | Bergmann beef mince 1 kg (Germany); Finnish mince very likely, not seen |
| - | Wheat flour, breadcrumbs, potato starch, baking powder, garlic, ground cumin, dark syrup, barley | **not found** | Recipes only. Almost certainly stocked; nothing on Lidl's pages shows them |

## What this means for the five candidates

| Candidate | Main ingredient at Lidl FI | Consequence |
| --- | --- | --- |
| Pea falafel | dried split peas: campaign only; whole dried peas not found | Availability is the first thing a kitchen test must settle. Canned chickpeas, the usual Lidl pulse, cannot make a raw-paste falafel (R2) |
| Kale rolls | curly kale, small bags, Aug-Oct only | The form does not match the documented practice (flat, large leaves); out of season now |
| Potato-rutabaga gratin | rutabaga in season now (Sept-Dec); potatoes, milk, cream regular | The best-matched candidate to Lidl's range |
| Broccoli-stem patties | fresh broccoli not found; frozen broccoli is florets | The overlooked part exists only if a fresh head is bought (Lidl shelf, or elsewhere) |
| Hollowed onion | onions regular, in a mixed 1 kg bag; no large onions seen | Medium onions: halves, as in Nice and Liguria |

## What changed in the ingredient data

Only what the transfers need (no catalogue expansion):
- `tomato.yaml`: a `dried_peas` ingredient (availability *occasional*, with
  the Lidl note); the Lidl findings appended to the FI availability notes of
  rutabaga, kale and broccoli. No availability class was changed.
- `part_properties.yaml` `staged_parts`: `rutabaga.root`, `kale.leaves`,
  `dried_peas.dried_seed` (and `napa_cabbage` if its transfer is kept, see
  `candidates.md`), each with the evidence ids its properties rest on.

R3 reported that 40 of 56 construction additions and 5 of 10 staged parts
were uncatalogued. This round confirms that the catalogue gap is mostly a
*visibility* gap: lidl.fi cannot show the regular range at all, so the
catalogue cannot be completed from Lidl's website.
