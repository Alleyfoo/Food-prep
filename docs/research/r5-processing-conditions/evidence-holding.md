# Evidence: holding intermediates and packet instructions

Date read: 2026-11-25. Method: WebSearch to find, WebFetch to read; PDFs that WebFetch
could not parse were converted locally with `pdftotext` from the copy WebFetch saved, and
read as raw text (marked "raw text (pdftotext)"). Search languages: Finnish, Swedish,
Norwegian (one page), German, English. Evidence ids Q500-Q551.

Traps:
- Several Ruokavirasto pages on cooling (Q502, Q503, Q504) are written for **food businesses**,
  not households. They are recorded because they are the only Ruokavirasto pages that give a
  cooling time; their audience is stated on each source.
- Q504 is a **consultation draft** (file sits under `lausuntopyynnot/`, named `sushiohjeluonnos`),
  although its own header says "Ohje".
- Q521 (NHS) is a **baby-food** page; its numbers are recorded but its audience is narrower.
- Retail pages (S-kaupat, K-Ruoka) were often **truncated** by WebFetch; a truncated page is
  recorded as "instructions not visible", never as "no instructions".
- No source read states how long **soaked, uncooked** pulses keep, or how long **blanched
  (not frozen)** vegetables keep. These are reported as not found, not filled in from general
  leftover rules.
- One WebSearch call that named the rice bacterium in Finnish failed with a tool error; later
  searches worked.

## Sources

### Q500 — https://www.ruokavirasto.fi/globalassets/tietoa-meista/julkaisut/esitteet/elintarvikkeet/nikseja_ja_neuvoja_kevyt.pdf
- Finnish, Finland. Public body (Evira, now Ruokavirasto; easy-read consumer leaflet "Niksejä ja neuvoja turvalliseen ruoanlaittoon", printed 2013).
- Read: raw text (pdftotext).
- Leftovers (d, e, f): cool leftover food quickly and put it in the fridge. Faster cooling: stand the dish in cold water for a while, or split the food into smaller dishes. Do not put food in the fridge while too warm.
- Room temperature: throw away food that has been warm (kept out) for over two hours; do not serve it again.
- "Valmiit ruoat" and "pilkotut kasvikset" (cut vegetables) are listed as easily perishable; keep in the coldest part of the fridge (lowest shelves, at the back). (g)
- Reheat until steaming hot.
- No number of days and no fridge temperature in this leaflet.

### Q501 — https://www.ruokavirasto.fi/en/foodstuffs/instructions-for-consumers/news/many-foods-can-be-a-risk-if-hygiene-fails--finnish-food-authority-reminds-of-the-importance-of-good-kitchen-hygiene/
- English, Finland. Public body (Ruokavirasto news for consumers), 7 May 2025.
- Read: WebFetch summary.
- Serve at once or chill quickly; no cooling time given. Perishables in the fridge at +2 to +6 °C. Reheat thoroughly. Warns against slow cooling and leaving food at room temperature. No days, nothing rice- or pulse-specific.

### Q502 — https://www.ruokavirasto.fi/en/foodstuffs/food-sector/hygienic-actions/production-and-handling/cooling/
- English, Finland. Public body (Ruokavirasto, guidance for food businesses), updated 15.11.2024.
- Read: WebFetch summary.
- Cooling (d, e, f): start at once if not served; reach storage temperature within **four hours at most**. Layer **under 10 cm, preferably about 5 cm**; cut, slice or split into shallower dishes. Closed containers in cold water with ice, or under running cold water. Ordinary fridges and cold cabinets are generally **not enough** to cool hot food. Measure at the thickest part. Move to cold storage as soon as cooled. Cold-stored foods below +6 °C where required.
- No days, nothing rice-specific.

### Q503 — https://www.ruokavirasto.fi/globalassets/tietoa-meista/asiointi/oppaat-ja-lomakkeet/yritykset/elintarvikeala/elintarvikehuoneistot/jaahdyttaminen.pdf
- Finnish, Finland. Public body (Ruokavirasto one-page "Ravintolahygieniaa: Jäähdyttäminen", for restaurants; PDF metadata 2018, modified 2021).
- Read: raw text (pdftotext).
- Cool food to **+6 °C or below within at most 4 hours**; never cool at room temperature; small amounts can be cooled in a cold room or water bath, larger amounts best in a blast cabinet; move cooled food at once to cold room or freezer. Danger zone +6 to +60 °C. Measure the food, not the cabinet.

### Q504 — https://www.ruokavirasto.fi/globalassets/tietoa-meista/ajankohtaista/lausuntopyynnot/sushiohjeluonnos.pdf
- Finnish, Finland. Public body (Ruokavirasto guidance on sushi in registered food businesses, Dnro 4502/04.02.00.01/2026; consultation draft by its location).
- Read: raw text (pdftotext), sections on rice.
- Cooked rice (d): cool **immediately after cooking so it falls to at most +6 °C within four hours**; keep cooked rice at most +6 °C before sale. Rice is best rinsed before cooking. Rice may be shaped while still cooling, provided total cooling time stays within four hours. Sales/serving fixtures must not be used for cooling. Acidifying (pH) improves keeping but does not replace cooling.
- No home fridge days.

### Q505 — https://www.ruokavirasto.fi/en/foodstuffs/food-sector/food-information/labelling/instructions-for-use-and-warning/beans/
- English, Finland. Public body (Ruokavirasto, labelling requirement for dried beans), updated 19.3.2026.
- Read: WebFetch summary.
- Soaking (a): soak **overnight, at least 12 hours**, rinse, then boil at least 30 min (or a bean-specific time from Q506). No soaking temperature. Poisoning possible if beans are eaten raw, **only soaked**, or under-heated; heating only to +80 °C can raise toxicity. Applies to beans and broad beans; **peas and chickpeas are not mentioned** on this page.

### Q506 — https://www.ruokavirasto.fi/globalassets/tietoa-meista/asiointi/oppaat-ja-lomakkeet/yritykset/elintarvikeala/pakkausmerkinnat/luettelo_pavuista_ja_niiden_suositelluista_keittoajoista_1.pdf
- Finnish/Swedish, Finland. Public body (Ruokavirasto list "Luettelo pavuista ja niiden suositelluista keittoajoista", dried pulses), PDF dated 24.1.2019.
- Read: raw text (pdftotext, `-raw` and `-table` modes, cross-checked).
- Recommended cooking times (contrast role on pairs 1, 2, 4; these are **cooking** times, not soaking): yellow or green pea (herne) **1 h**; chickpea (kikherne) **45 min - 1 h 15 min**; cowpea / black-eyed bean (lehmänpapu, mustasilmäpapu) **30-45 min**; kidney bean 45 min - 1 h; small-seeded broad bean 30 min, large-seeded 1 h; lentils 20 min; soy 1 h 30 min. No soaking times in the list.

### Q507 — https://www.ruokavirasto.fi/elintarvikkeet/ohjeita-kuluttajille/ruokamyrkytykset/ruokamyrkytyksia-aiheuttavia-bakteereja/bacillus-cereus/
- Finnish, Finland. Public body (Ruokavirasto consumer page), updated 13.9.2023.
- Read: WebFetch summary.
- Rice (d): typical vehicles are meat and rice dishes, dairy, vegetables. Food not kept hot (at least +60 °C) must be cooled **immediately, within four hours to +6 °C**, then kept at **+4 to +6 °C**. Reheat right through to **over +70 °C just before serving**. No days; no rule on how many times to reheat.

### Q508 — https://www.ruokavirasto.fi/elintarvikkeet/ohjeita-kuluttajille/ruokamyrkytykset/usein-kysyttya-ruokamyrkytyksista/
- Finnish, Finland. Public body (Ruokavirasto consumer FAQ), updated 13.9.2023.
- Read: WebFetch summary.
- Keep cold cold and hot hot; danger zone +6 to +60 °C; slow cooling of hot food listed as a cause of food poisoning. No days, nothing on rice or pulses.

### Q509 — https://ruokavirasto.fi/henkiloasiakkaat/tietoa-elintarvikkeista/kasittely-ja-sailyttaminen/lampotila/tietoa-elintarvikkeiden-sailytysajoista
- Finnish, Finland. Public body (Ruokavirasto consumer page on storage temperatures), updated 23.9.2025.
- Read: WebFetch summary.
- Fridge **+2 to +6 °C**; hot food above +60 °C or cooled quickly to fridge temperature; reheat well. Potatoes stored too cold go watery (raw potatoes). Use a thermometer, read it in the morning. **No storage days**, no cooling time.

### Q510 — https://www.martat.fi/ruoka/sailonta/pakastaminen/kasvikset-ja-sienet/
- Finnish, Finland. Home-economics association (Marttaliitto, "Kasvisten pakastus"), no date.
- Read: WebFetch summary, read twice (second pass asked for the table rows as text).
- Blanching **for freezing** (c): most vegetables are blanched before freezing to stop enzyme activity; time depends on the vegetable **and piece size**; counted **from when the water returns to the boil** after the vegetables go in; then cool as fast as possible in running cold water, drain well, pack in single-portion packs. Table (vegetable | preparation | time): broccoli | cut in pieces, small florets whole | **3-5 min**; cauliflower | pieces | 4-6 min; rutabaga (lanttu) | peel, cube and cook, or cut in wedges, cook soft and mash | **2-3 min** (the time sits in the blanching-time column; the preparation text also mentions cooking, so the row is ambiguous); kohlrabi 2-3 min; Brussels sprouts 3-4 min; carrot | pieces, cooked and mashed, or grated raw with lemon juice | 3-5 min; parsnip, celeriac 3-5 min; peas 1-2 min; fresh beans 2-4 min; spinach, nettle 2-3 min; new potatoes 3-5 min.
- **Not in the table**: white cabbage, napa cabbage, courgette, onion. White cabbage: freezing not recommended because it softens and goes watery on thawing; but one may try freezing a **whole head** and using the thawed cabbage for cabbage rolls (c, f).
- Grated raw carrot can be frozen as is, a little lemon juice for flavour (g).
- Frozen without blanching: dill, parsley, chives, leek, bell pepper, rhubarb.

### Q511 — https://www.martat.fi/ruoka/ruoanvalmistus/ruokaa-turvallisesti/kylma-kylmana-ja-kuuma-kuumana/
- Finnish, Finland. Home-economics association (Marttaliitto), no date.
- Read: WebFetch summary.
- Danger zone +6..+60 °C. Food left on the table at room temperature for **over two hours** must be thrown away. If more than two hours remain before the meal, cool the food. Speed cooling by smaller portions, slicing, or standing the dish in a sink of cold water. **Do not put hot food in the fridge** (it warms the fridge). Cover before refrigerating. Reheat quickly to boiling hot just before serving. No days.

### Q512 — https://www.martat.fi/teemat/junnukokki/keittiossa/ruokailun-jalkeen/tahteet-talteen/
- Finnish, Finland. Home-economics association (Marttaliitto, children's cooking pages), no date.
- Read: WebFetch summary.
- Leftovers (d, e, f): let hot food **cool properly** before the fridge, e.g. dish in cold water in the sink, or outside in winter. Cover with lid or film. Food keeps **2-3 days in the fridge if well packed**. Freeze part if there is a lot; label with name and date.

### Q513 — https://www.martat.fi/ruoka/ruoanvalmistus/ruokaa-turvallisesti/elintarvikkeiden-sailyvyys/
- Finnish, Finland. Home-economics association (Marttaliitto), no date.
- Read: WebFetch summary.
- Gives fridge days only for raw fish, meat, milk, eggs; dry rice and pasta up to a year in the pantry. **No days for cooked food, potatoes, rice or vegetables.** Recorded as a negative.

### Q514 — https://www.martat.fi/marttakoulu/ruoka/sailonta/pakastaminen/
- Finnish, Finland. Home-economics association (Marttaliitto, Marttakoulu), no date.
- Read: WebFetch summary.
- Freezer (f): home-made dishes **such as soups and casseroles (laatikot) 1-3 months**; vegetables 10-12 months. Cool before freezing; store at -18 °C or colder; flat single-portion packs, air removed, label and date; thaw quickly and use at once; do not refreeze thawed products.

### Q515 — https://www.martat.fi/teemat/kodin-juhlat/joulu/jouluruoka/nain-sailytat-jouluruokia/
- Finnish, Finland. Home-economics association (Marttaliitto), no date.
- Read: WebFetch summary.
- Casseroles (f): no days stated. Cool hot food quickly (dish in cold water); do not mix old and new food (leftover casseroles named as the example); heat all warm-served food thoroughly; at 0 to +6 °C outdoors food may be kept on a balcony, protected.

### Q516 — https://www.livsmedelsverket.se/en/food-habits-health-and-environment/food-loss-and-waste/plan-wisely-and-use-leftovers/forvara-maten-ratt/
- English, Sweden. Public body (Livsmedelsverket), reviewed 30.9.2026.
- Read: WebFetch summary.
- Fridge **4 °C**, freezer -18 °C. Vegetables can be blanched before freezing (brief boil, then rinse in cold water; no times). Frozen vegetables keep a year or more. **No cooling rules, no leftover days.**

### Q517 — https://www.livsmedelsverket.se/globalassets/publikationsdatabas/rapporter/2017/riskhanteringsrapport-tillvaxt-av-bakterier-vid-avsvalning-forvaring-och-upptining-livsmedelsverkets-rapportserie-2-2017-del-1.pdf
- Swedish, Sweden. Public body (Livsmedelsverket report L 2017 nr 02 del 1, risk management; updated Sept 2025).
- Read: raw text (pdftotext), consumer-advice sections.
- Consumer cooling advice (d, e, f): food **over half a litre** should be cooled in a cold water bath, or outdoors if a few degrees above zero; then into the fridge or freezer **once cooled**. Alternative: split into smaller containers to cool faster at room temperature. Modelling: 4 L pea soup cooled first at room temperature then at 7 °C took **over 30 h** to fall below 10 °C at the warmest point; in 0.5 L portions about 11 h; 0.5 L in an ice-water bath about 2 h. Consumer fridges lack capacity for large hot volumes.
- Business guidance cited: heat-treated food to be held cold should be cooled in under 4 h; large-kitchen handbook: 4 h to below 8 °C.
- Holding: put leftovers in the fridge as soon as possible; revised advice for chilled goods left out: at most **4 h at ≤20 °C, 3 h at ≤25 °C, 2 h at 26-30 °C** (older advice: 2 h). Store at about 4 °C. No leftover days.

### Q518 — https://mattilsynet.no/mat-og-drikke/forbrukere/kokt-ris-og-pasta-som-star-fremme-kan-lage-giftstoffer
- Norwegian, Norway. Public body (Mattilsynet, consumer page), 14.8.2023.
- Read: WebFetch summary.
- Cooked rice and pasta (d): do **not** keep at room temperature (defined as above 10 °C); cook only what is needed; leftovers cooled **as fast as possible**, then fridge. Reheating does not make the toxins harmless. No cooling time, no days, no reheat-once rule.

### Q519 — https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker
- English, UK. Public body (Food Standards Agency "Home food fact checker"; publication 2.6.2020, updated 21.8.2026). Reached via redirect from https://www.food.gov.uk/safety-hygiene/home-food-fact-checker.
- Read: WebFetch summary.
- Cooked rice (d): chill **as quickly as possible, ideally within one hour**; don't leave it in the cooker, steamer or pan to cool; smaller portions help. Fridge **no more than one day** until reheating. **Never reheat more than once**; steaming hot all through. Freeze within an hour of cooking (cool quickly first, e.g. container in cold water); defrost in the fridge.
- Potatoes (e): cooked potatoes, or potatoes parboiled (boiled 5 min), and leftover cooked potatoes can be frozen; roast from frozen until steaming hot. No fridge days for cooked potatoes.

### Q520 — https://www.foodstandards.gov.scot:443/consumers/food-safety/at-home/rice
- English, UK (Scotland). Public body (Food Standards Scotland), no date.
- Read: WebFetch summary.
- Cooked rice (d): chill as quickly as possible, ideally within 1 hour; take it out of the cooker or pan; divide into smaller portions; once at room temperature, straight into the fridge; **no longer than 24 hours** before eating; cold rice is fine if cooled quickly, refrigerated and eaten within 24 h; reheat steaming hot; **never reheat more than once**.

### Q521 — https://www.nhs.uk/start-for-life/baby/weaning/safe-weaning/storing-and-reheating-food/
- English, UK. Public body (NHS Start for Life, **baby-food page**), no date.
- Read: WebFetch summary.
- Batch-cooked food cooled ideally within **1 to 2 hours**, then fridge or freezer; rice cooled **within 1 hour**, straight into fridge or freezer. Fridge food used within **2 days**; rice within **24 hours**. Quick cooling: airtight container under cold running water, stirring. Reheat once only; rice never more than once. Defrost in fridge; eat within 24 h of defrosting.

### Q522 — https://www.bfr.bund.de/assets/01_Ver%C3%B6ffentlichungen/FAQ_deutsch/faq-vorkochen-fuer-mehrere-tage.pdf
- German, Germany. Public body (BfR FAQ "Vorkochen für mehrere Tage", meal prep), 8.7.2025.
- Read: raw text (pdftotext).
- Holding cooked components (d, e, f): no blanket figure possible, but heated meals best eaten **within 2-3 days** or frozen; meals **with raw components** at the latest **one day** after preparation (g). Fridge **max 7 °C, better 5 °C**; bottom shelf at the back is usually coldest. Cool dishes before they go into the freezer. Pack raw components (vegetables, salads) separately from cooked ones (e.g. cooked pulses). Airtight, meal-sized containers.
- Reheat so that every point is **above 70 °C for at least 2 minutes**; thaw frozen dishes in the fridge (e.g. overnight).
- Freezer at -18 °C: vegetables 6-12 months, **up to 12 months if cooked or blanched** (c).
- Spores survive heating; surviving germs multiply between 10 and 60 °C; pass through that range quickly when cooling.

### Q523 — https://www.bfr.bund.de/cm/350/verbrauchertipps-schutz-vor-lebensmittelbedingten-erkrankungen-durch-bakterielle-toxine.pdf
- German, Germany. Public body (BfR Verbrauchertipps on bacterial toxins), 2020 edition.
- Read: raw text (pdftotext).
- Cooked rice and pasta (d): toxin-related vomiting is linked mainly to starchy cooked foods such as rice or noodles kept wrongly after heating; keep rice and pasta leftovers **in the fridge**. General: product temperatures between **7 and 60 °C must be avoided** during holding; cool quickly to **below 7 °C**, larger amounts in **several shallow dishes**, store at that temperature, reheat just before eating to **at least 70 °C for at least 2 min** at all points. In dishes mixing raw and cooked parts, cool the cooked parts first. No days.

### Q524 — https://www.fsai.ie/Consumer-Advice/Food-Safety-and-Hygiene/Advice-on-eating-legumes
- English, Ireland. Public body (Food Safety Authority of Ireland), no date.
- Read: WebFetch summary.
- Dried beans (a): follow the packet first; otherwise soak **at least 12 hours**, **discard the soaking water**, boil at least 30 min in fresh water. No soaking temperature. Chickpeas not mentioned; peas named only among fresh legumes. No storage of soaked or cooked legumes.

### Q525 — https://extension.colostate.edu/resource/cooking-dry-beans/
- English, USA. University extension (Colorado State University; publicly funded), reviewed Oct 2025.
- Read: WebFetch summary.
- Soaking (a): cover by several inches of water, several hours or overnight; **refrigerate if soaking longer than 12 hours**. Quick soak: boil 3 min, stand 1 h. Drain, rinse, cook in fresh water. Salt in soak water may shorten cooking and limit splitting.
- Cooked beans: serve or refrigerate **within 2 hours**; fridge **3-5 days** at 35-40 °F in sealed containers; freezer 6-8 months at 0 °F.
- How long soaked uncooked beans keep: **not stated**.

### Q526 — https://www.ndsu.edu/agriculture/sites/default/files/2024-08/fn1939.pdf
- English, USA. University extension (North Dakota State University FN1939, reviewed July 2024).
- Read: raw text (pdftotext).
- Soaking (a): traditional soak overnight or **at least eight hours in the refrigerator**; hot soak (boil 2-3 min, soak up to 4 h); quick soak (boil 2-3 min, soak at least 1 h). **When soaking longer than four hours, put the container in the refrigerator**; beans may carry bacteria that grow or make toxin at room temperature. Change soak water several times and discard it (for gas-causing sugars). Pressure-cooked garbanzo (chickpea) 15-25 min.

### Q527 — https://www.onceuponachef.com/recipes/falafel.html
- English, USA. Cooking site (recipe author's site), updated 18.8.2026.
- Read: WebFetch summary.
- Raw falafel (b): dried chickpeas soaked 24 h (intro: overnight or at least 8 h), topping up water; **not cooked**, should still be raw inside. Shaped uncooked patties: up to **one day ahead** in the fridge on a lined tray, fried straight from the fridge; or frozen on a tray until solid, then bagged, **up to three months**, fried from frozen with a little extra time. No soaking temperature.

### Q528 — https://www.verbraucherzentrale.de/kartoffeln-richtig-aufbewahren-28230
- German, Germany. Consumer organisation (Verbraucherzentrale), dated 6.11.2026.
- Read: WebFetch summary.
- Raw potatoes only (4-8 °C, dark, dry). **No statement on cooked potatoes.** Recorded as a negative for (e).

### Q540 — https://www.s-kaupat.fi/tuote/kotimaista-kuivattu-suomalainen-herne-500-g/6415712002114
- Finnish, Finland. Retailer product page (S-kaupat), brand Kotimaista, 500 g dried pea. **Not Lidl.**
- Read: WebFetch summary.
- Says the instructions are on the package; none visible on the page (storage section truncated). Whole or split not stated.

### Q541 — https://www.s-kaupat.fi/tuote/papuska-keltainen-herne-500g/6410191020451
- Finnish, Finland. Retailer product page (S-kaupat), Papuska keltainen herne 500 g (Mausteaitta Oy). **Not Lidl.**
- Read: WebFetch summary.
- No soaking or cooking instructions visible; description truncated.

### Q542 — https://www.s-kaupat.fi/tuote/bazar-kikherne-500g/4032549042605
- Finnish, Finland. Retailer product page, Bazar Kikherne 500 g. **Not Lidl.**
- Read: WebFetch summary.
- Only "store dry and cool"; no cooking instructions visible; description truncated.

### Q543 — https://www.s-kaupat.fi/tuote/foodin-kikherne-luomu-500g/6430055215908
- Finnish, Finland. Retailer product page (packet text reproduced), Foodin Kikherne luomu 500 g. **Not Lidl.**
- Read: WebFetch summary.
- Chickpeas (pairs 2, 20-type packet step): **soak 10-12 h, rinse, boil 60 min until soft**. Warning: must not be eaten unprocessed ("Ei saa syödä käsittelemättömänä"). No water amount, no soak temperature.

### Q544 — https://www.k-ruoka.fi/kauppa/tuote/milletti-500g-keltainen-ruokaherne-6420613630557
- Finnish, Finland. Retailer product page (K-Ruoka), Milletti 500 g keltainen **kokonainen** (whole) kuivattu ruokaherne. **Not Lidl.**
- Read: WebFetch summary; page truncated after the title, instructions not visible.

### Q545 — https://www.s-kaupat.fi/tuote/kymppi-suomalainen-kuivattu-herne-500-g/6420260891103
- Finnish, Finland. Retailer product page (packet recipe reproduced), Kymppi suomalainen kuivattu herne 500 g (Kymppi-Maukkaat Oy). **Not Lidl.**
- Read: WebFetch summary.
- Peas (pair 1, soup contrast role): rinse, **soak in cold water overnight**, pick out debris; **simmer in the soaking water** about 1 h, then add meat and onion and cook about another hour; done when the peas are **soft**. Whole or split not stated. No soak temperature.

### Q546 — https://www.s-kaupat.fi/tuote/ylistalon-herneita-kuivattu-500g/6418319085016
- Finnish, Finland. Retailer product page, Ylistalon herneitä kuivattu 500 g (green). **Not Lidl.**
- Read: WebFetch summary; no instructions visible, description truncated.

### Q547 — https://www.s-kaupat.fi/tuote/bens-original-pitkajyvainen-riisi-1kg/5410673005861
- Finnish, Finland. Retailer product page (packet text reproduced), Ben's Original Pitkäjyväinen riisi 1 kg, **parboiled**. **Not a Lidl page**, but the same product name was seen in a past lidl.fi snippet (R4 `lidl-pages.md`, long-grain rice row, p10027070, now 404: see Failed pages).
- Read: WebFetch summary.
- Rice (pair 20): method 1, bring plenty of water to the boil, add rice, cover, cook **about 10 min**, drain well. Method 2, **1 part rice to 2 parts water**, bring to the boil, cover, low heat **until all water is absorbed, about 10 min**. No salt, no rest. No storage advice for cooked rice.

### Q548 — https://www.k-ruoka.fi/kauppa/tuote/pirkka-pitkajyvainen-riisi-1kg-6410402014347
- Finnish, Finland. Retailer product page (K-Ruoka), Pirkka pitkäjyväinen riisi 1 kg. **Not Lidl.**
- Read: WebFetch summary; truncated after the title. The search snippet (20 min covered on low, then 5 min off the heat, parboiled) is **snippet-only**, not evidence.

### Q549 — https://www.myllynparas.fi/tuotteet/puuroriisi-1-kg
- Finnish, Finland. Manufacturer product page (Myllyn Paras), Puuroriisi 1 kg, round-grain polished. **Not a Lidl page**, but Lidl sold this product as a Christmas offer (R4 `lidl-pages.md`, porridge-rice row, p10029709, now 404).
- Read: WebFetch summary.
- Porridge (rice in porridge role, not pair 20 directly): boil 3 dl water, add 1½ dl rice and let it absorb the water, add 7 dl milk, simmer covered about **40 min**, stirring now and then. Swells about 2½ times. No salt amount, no endpoint wording, nothing on storing cooked porridge.

### Q550 — https://www.k-ruoka.fi/kauppa/tuote/foodin-kikherne-500g-luomu-6430055215908
- Finnish, Finland. Retailer product page (K-Ruoka), Foodin Luomu Kikherne 500 g. **Not Lidl.**
- Read: WebFetch summary; truncated, instructions not visible (the same product's text is in Q543).

### Q551 — https://www.lidl.fi/q/search?q=riisi
- Finnish, Finland. Retailer (Lidl Finland) site search.
- Read: WebFetch summary. Reports 5 results, but no product names, sizes or instructions were in the captured page. Consistent with R4's finding that lidl.fi search shows only current offers.

## Failed pages and snippet-only

| URL or query | why |
| --- | --- |
| https://www.lidl.fi/p/myllyn-paras-puuroriisi/p10029709 | HTTP 404 (Lidl product page; product text read instead at the manufacturer, Q549) |
| https://www.lidl.fi/p/ben-s-original-pitkajyvainen-riisi/p10027070 | HTTP 404 (same product read at S-kaupat, Q547) |
| lidl.fi pages for dried peas / chickpeas (Golden Sun campaign c2834) | Not re-fetched; R4 `lidl-pages.md` already records 404 and empty searches for "herne", "kikherne" |
| WebSearch "lidl.fi Golden Sun riisi OR herneet OR kikherneet valmistusohje" | Only lidl.de and Open Food Facts results, no Finnish packet text |
| https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety | HTTP 403. Snippet said 3-4 days fridge, 3-4 months freezer, refrigerate within 2 h, reheat to 165 °F: **snippet-only** |
| https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/steps-keep-food-safe | HTTP 403 (snippet: shallow containers, 3-4 days: snippet-only) |
| https://www.foodsafety.gov/blog/leftovers-gift-keeps-giving | HTTP 403 |
| https://www.verbraucherzentrale.nrw/sites/default/files/2023-05/lagerungsabc_vznrw.pdf | Too large for WebFetch (over 10 MB); not read |
| https://www.themediterraneandish.com/how-to-make-falafel/ | HTTP 403 (snippets of comment pages: mixture 1-2 days in fridge, snippet-only) |
| https://www.k-ruoka.fi/kauppa/tuote/risetti-ruokaherne-1kg-kuivattu-6418510000894 | HTTP 404 |
| https://www.s-kaupat.fi/tuote/kuivattu-herne/7027510202338 | HTTP 404 |
| https://foedevarestyrelsen.dk/Media/639038232508593824/Liste over kogetider af bælgfrugter og bønner.pdf | Redirect to cdn2.gopublic.dk not followed; not read (Finnish equivalent Q506 read) |
| https://www.gov.uk/government/publications/home-food-fact-checker | Landing page only; content read at the HTML sub-page (Q519) |
| mtvuutiset.fi "kotiruoka säilyy jääkaapissa vain 2-4 päivää" | Snippet-only (news, 2-4 days) |
| mtvuutiset.fi "Säilötään kasviksia" | Snippet-only: blanching for freezing broccoli 3-6 min, cabbage strips 4-5 min, rutabaga cubes 2-4 min. Not read, not evidence; conflicts with Q510 would need a read |
| hurbra.se (cooked food several days to a week at 4 °C) | Snippet-only |
| Coventry / Torbay council rice pages; NSW Food Authority; NZ MPI (rice 2 days) | Snippet-only |
| fitbook.de citing Verbraucherzentrale Bayern (cooked potatoes max 4 days) | Snippet-only |
| apotheken-umschau.de, oekotest.de, heidelberg24.de on rice (Verbraucherzentrale: rice within a day) | Snippet-only |
| taenk.dk chickpeas (soak 10-12 h in the fridge) | Snippet-only |
| NC State Extension (refrigerate while soaking) | Snippet-only |
| Sainsbury's dried chickpeas 500 g label (soak 12 h, boil 10 min then simmer 85 min) | Snippet-only, UK, not Finnish |
| touchoffinland.com Myllyn Paras porridge rice | Snippet-only (same text read at Q549) |
| WebSearch naming the rice bacterium with Ruokavirasto in Finnish | Tool error; rephrased |

## Searches

| language | query | useful? |
| --- | --- | --- |
| fi | Ruokavirasto ruoan jäähdytys säilytys jääkaappi kuluttaja ruokamyrkytys | yes (Q500, Q502, Q503) |
| fi | Ruokavirasto keitetty riisi [bacterium] säilytys | failed (tool error) |
| fi | ruokavirasto.fi kuluttajille ruoan säilyttäminen jääkaapissa ruoantähteet jäähdyttäminen | partly |
| fi | ruokavirasto riisi jäähdytä nopeasti uudelleenlämmitys kerran | yes (Q504) |
| fi | Ruokavirasto kuivatut pavut liotus keittäminen raa'at pavut ohje kuluttaja | yes (Q505, Q506, Q524) |
| fi | Ruokavirasto idut idättäminen kotona ohje | no (producer material only) |
| fi | martat.fi kasvisten pakastaminen ryöppäysajat lanttu kaali parsakaali kesäkurpitsa | snippet only |
| fi | Martat ruoan säilyvyys jääkaapissa tähteet kuinka kauan | snippet only |
| fi (martat.fi) | kasvisten pakastaminen ryöppäys | yes (Q510) |
| fi (martat.fi) | ruoan säilytys jääkaappi jäähdyttäminen ruoantähteet | yes (Q511, Q512) |
| sv | Livsmedelsverket kokt ris förvaring kylskåp kyla ner snabbt | yes (Q516, Q517, Q518) |
| sv | Livsmedelsverket matrester hur länge kylskåp kyla ner mat | partly |
| sv | Livsmedelsverket torkade bönor ärtor kikärtor blötlägga koka | no Livsmedelsverket times |
| en | food.gov.uk cooked rice cool within one hour fridge eat within 24 hours reheat once | yes (Q519, Q520) |
| en | NHS leftovers how long fridge cooked food 2 days rice reheat | yes (Q521) |
| en | USDA FSIS leftovers food safety 3 to 4 days refrigerate within 2 hours shallow containers | snippets; pages 403 |
| en (fsis.usda.gov etc.) | fsis.usda.gov leftovers and food safety shallow containers 3 to 4 days | snippets; pages 403 |
| en (fsis.usda.gov) | FSIS "Leftovers and Food Safety" fact sheet | page 403 |
| de | BfR gekochter Reis aufbewahren abkühlen Kühlschrank Verbraucher | yes (Q522, Q523) |
| en | soak dried beans overnight in refrigerator food safety extension room temperature ferment | yes (Q525, Q526) |
| fi | herneiden liotus jääkaapissa vai huoneenlämmössä kuinka kauan liotetut herneet säilyvät | no |
| fi (ruokavirasto.fi, martat.fi) | elintarvikkeiden säilyvyys keitetyt perunat jääkaapissa vuorokautta | yes (Q509, Q513), no potato days |
| fi (martat.fi) | valmisruokien pakastaminen laatikkoruoat kaalikääryleet säilyvyys pakkasessa | yes (Q514, Q515) |
| fi | porkkanaraaste säilyy jääkaapissa kuinka kauan raaste valmiiksi | no |
| en | falafel mixture make ahead refrigerate up to days freeze uncooked falafel | yes (Q527) |
| en | blanched vegetables store in refrigerator how many days before cooking extension food safety | no |
| de | Verbraucherzentrale Kartoffeln gekocht aufbewahren Kühlschrank Tage Reste | partly (Q528 negative; rest snippets) |
| fi (ruokavirasto.fi) | ruokavirasto henkiloasiakkaat ruokamyrkytykset riisi jäähdyttäminen kotona | yes (Q507, Q508) |
| fi | lidl.fi Golden Sun riisi OR herneet OR kikherneet valmistusohje | no |
| fi | tokmanni cloudinary et1.pdf kuivatut herneet liotus keittoaika | no |
| fi | Pirkka kuivatut kikherneet 500g valmistusohje liota | no |
| fi | Myllyn Paras puuroriisi valmistusohje vesi maito keittoaika | snippet; led to Q549 |
| fi | kuivatut keltaiset herneet pakkaus ohje liota yön yli keitä s-kaupat OR k-ruoka | no |
| fi (s-kaupat, k-ruoka, foodie) | kikherneet kuivattu 500 g | yes (Q542, Q543, Q550) |
| fi (s-kaupat, k-ruoka, foodie) | keltaiset herneet kuivattu pussi | yes (Q540, Q541, Q544, Q545, Q546) |
| fi (s-kaupat, k-ruoka) | pitkäjyväinen riisi 1 kg valmistusohje | yes (Q547, Q548) |
| fi (s-kaupat, k-ruoka, myllynparas) | Myllyn Paras puuroriisi 1 kg | yes (Q549) |
| fi | Risenta kikherneet kuivatut valmistus liotus keittoaika | snippets only |

## Synthesis per intermediate (a-g)

General holding rules that apply to every cooked intermediate (kept separate, not averaged):
- Cooling time: Ruokavirasto **+6 °C within 4 h** (Q503, Q507; business Q502, Q504). FSA/FSS/NHS: rice **ideally within 1 h** (Q519, Q520, Q521); NHS batch food 1-2 h (Q521). Colorado State: cooked beans refrigerated within 2 h (Q525). BfR: quickly to below 7 °C, no hours (Q523). Livsmedelsverket consumer advice: method, not hours (water bath over 0.5 L) (Q517).
- Cooling method: shallow layers / split into small or shallow dishes (Q500, Q502, Q511, Q517, Q519, Q520, Q523); layer under 10 cm, ideally 5 cm (Q502); dish in cold water (Q500, Q511, Q512, Q515, Q517, Q521); outdoors when cold (Q512, Q515, Q517).
- Hot food into the fridge: **conflict**. Martat: do not put hot food in the fridge, let it cool properly first (Q511, Q512); Ruokavirasto: not "too warm" (Q500) and ordinary fridges cannot cool hot food (Q502); Livsmedelsverket: into the fridge once cooled, room-temperature cooling in small containers is an accepted alternative (Q517). FSS: rice into the fridge once at room temperature (Q520). Against these, FSIS (403, snippet-only) says to refrigerate immediately: not evidence here.
- Time out at room temperature: discard after 2 h (Q500, Q511); Livsmedelsverket revised 4 h at ≤20 °C, 3 h at ≤25 °C, 2 h at 26-30 °C (Q517).
- Fridge temperature: +2 to +6 °C (Q501, Q509); +4 to +6 °C (Q507); 4 °C (Q516, Q517); max 7 °C, better 5 °C (Q522); 35-40 °F (Q525).
- Days in the fridge, cooked food in general: 2-3 days if well packed (Q512, Martat); heated meals within 2-3 days (Q522, BfR); 2 days (Q521, NHS baby food); cooked beans 3-5 days (Q525). Ruokavirasto gives **no days** on any page read (Q500-Q509).
- Reheating: right through above +70 °C just before serving (Q507); above 70 °C for at least 2 min at every point (Q522, Q523); steaming hot (Q500, Q519, Q520, Q521); reheat once (Q521; rice Q519, Q520).
- Freezing cooked dishes: 1-3 months (Q514); cool first (Q514, Q522).

### a. Soaked dried pulses (peas, chickpeas) before cooking or grinding
- Soak time stated: beans overnight, at least 12 h (Q505, Q524); chickpeas 10-12 h (Q543 packet); peas overnight in cold water (Q545 packet); beans overnight or at least 8 h (Q526); chickpeas 24 h for falafel (Q527).
- Temperature during soak: **conflict on the threshold**. NDSU: refrigerate if soaking **longer than 4 h**; traditional soak in the fridge (Q526). Colorado State: refrigerate if **longer than 12 h** (Q525). Ruokavirasto, FSAI, Foodin, Kymppi: no temperature stated (Q505, Q524, Q543, Q545); Kymppi says cold water (Q545).
- Soak water: discard and cook in fresh water (Q524, Q525, Q526); Kymppi packet cooks the peas **in the soaking water** (Q545). Conflict kept.
- Safety framing: Ruokavirasto, beans only: never eat raw or **only soaked**; soaking alone does not destroy the lectin (Q505). Peas and chickpeas are not covered on that page; chickpeas carry their own "must not be eaten unprocessed" warning on the Foodin packet (Q543). This is the documented tension with raw-soaked falafel (pairs 1, 2, 5, 6): none of the bodies read addresses soaked-but-uncooked pulses that are then deep-fried.
- Cooking times if cooked (contrast role): pea 1 h, chickpea 45 min - 1 h 15 min, black-eyed 30-45 min (Q506); chickpea 60 min (Q543); peas about 1 h before other ingredients, then soft (Q545).
- How long soaked uncooked pulses keep: **not found** (looked in Q505, Q524, Q525, Q526; Q525 explicitly silent).
- Container: not stated beyond "plenty of water" / water covering by several inches (Q525, Q526).
- Confidence: soak length documented as established (3+ sources at overnight / 8-12 h); fridge-during-soak **conflicting** (4 h vs 12 h thresholds, others silent); keeping time **not found**.
- Gaps: no Finnish or Nordic authority gives a soak temperature; no source gives a keeping time for soaked pulses; no source on sprouting pulses at home (BfR Q522 only says raw sprouts should be heated).

### b. Raw ground pulse paste (falafel mix)
- No food-safety body read says anything about raw pulse paste. **Not found** from authorities.
- Nearest authority rule: meals **with raw components** eaten at the latest one day after preparation (Q522, BfR; general, not pulse-specific).
- Cooking site: shaped uncooked patties up to **1 day** in the fridge on a lined tray, or frozen on a tray then bagged **up to 3 months**, fried from frozen (Q527). R2 M1c (Egyptian taameya): portioning and freezing the batter is optional.
- Confidence: documented (1 non-authority source plus 1 R2 source); authority: not found.

### c. Blanched vegetables kept for later cooking
- Fridge keeping of blanched (not frozen) vegetables: **not found** in any source read.
- Blanching then cooling for freezing: cool as fast as possible in running cold water, drain well, single-portion packs (Q510); brief boil then rinse in cold water (Q516). See the blanching table below.
- Freezer life: vegetables 10-12 months (Q514); 6-12 months, up to 12 if cooked or blanched (Q522); a year or more (Q516).
- White cabbage: freezing not recommended (softens, watery); a whole head can be frozen and thawed for cabbage rolls (Q510). This is an alternative to blanching the head (pair 17), stated as "you may try".
- Confidence: freezing route documented (Q510, Q514, Q516, Q522); fridge holding not found.

### d. Cooked rice
- Cooling: within 1 h (Q519, Q520, Q521); within 4 h to +6 °C (Q504, Q507). **Conflict** (1 h UK vs 4 h Finland; the Finnish figure is a general cooked-food rule applied to rice).
- Method: out of the pan or cooker, small portions (Q519, Q520); shallow dishes (Q523); rice may be shaped while still cooling within the 4 h (Q504, business).
- Room temperature: do not keep above 10 °C (Q518).
- Fridge: **no more than 1 day / 24 h** (Q519, Q520, Q521). Ruokavirasto, Mattilsynet, BfR: fridge, no days (Q504, Q507, Q518, Q523). BfR general heated-meal rule is 2-3 days (Q522), not rice-specific.
- Reheat: once only (Q519, Q520, Q521); steaming hot (Q519, Q520); above 70 °C (Q507, Q523). Reheating does not remove toxin (Q518).
- Freezing: within an hour of cooking, after quick cooling; defrost in the fridge (Q519).
- Relevance: R2 kaalikääryleet "rice can be done the day before" (pair 20) sits inside the UK 24 h limit only if the rolls are made the next day; no Finnish source gives a day count.
- Confidence: established for the UK 1 h / 24 h / reheat-once rule (3 UK sources, one is baby-food); conflicting with Nordic sources on cooling time; Nordic day count not found.

### e. Boiled potatoes
- Fridge days for boiled potatoes: **not found** from any authority (looked in Q509, Q513, Q519, Q528). VZ Bayern "max 4 days" is snippet-only.
- General cooked-food rules apply only by inference (2-3 days Q512, Q522), not stated for potatoes.
- Freezing: cooked, parboiled (boiled 5 min) and leftover cooked potatoes can be frozen; roast from frozen (Q519).
- R2 evidence (practice, not safety): E1a refrigerates boiled potatoes until the next day; E1c keeps them more than a day and calls it decisive for crisp Rösti.
- Confidence: not found (authority); documented as practice (R2 E1a, E1c).

### f. Cooked dish: gratin, cabbage rolls (leftovers)
- Fridge: 2-3 days well packed (Q512); heated meals 2-3 days (Q522); 2 days (Q521). No dish-specific figure for gratin or cabbage rolls.
- Freezer: home-made soups and casseroles 1-3 months (Q514); cool first (Q514, Q522).
- Cooling and depth: layer under 10 cm, ideally 5 cm, or split into shallower dishes (Q502, business); dish in cold water (Q511, Q515).
- Do not mix leftover casserole with fresh food (Q515).
- R2 M15b: gratin dauphinois preferably chilled overnight, then cut and reheated (practice, not safety). R4 O3 (Ligurian stuffed vegetables): freezes well, keeps 2 days.
- Confidence: documented (Martat, BfR agree at 2-3 days; NHS 2 days); dish-specific not found.

### g. Grated raw vegetables (salted courgette, grated carrot)
- Fridge days: **not found**.
- Cut vegetables are listed as easily perishable, coldest part of the fridge (Q500). Meals with raw components: within 1 day (Q522). Pack raw components separately from cooked ones (Q522).
- Grated raw carrot can be frozen as is, a little lemon juice (Q510).
- Salted, drained courgette: nothing found in any food-safety source.
- Confidence: not found for days; documented that cut vegetables are perishable (Q500) and raw-component meals 1 day (Q522).

## Synthesis: blanching times for freezing (vegetable, piece, time, ids)

**These are blanching times before FREEZING, from a home-economics source. They are not
times for blanching before cooking a dish (pairs 10, 15, 17, 18), and should not be used as
those endpoints.** Time counted from when the water returns to the boil; cool at once in
running cold water (Q510).

| vegetable | piece | time | ids |
| --- | --- | --- | --- |
| rutabaga (lanttu) | peeled, cubed (row also mentions cooking and mashing: ambiguous) | 2-3 min | Q510 |
| broccoli | pieces; small florets whole | 3-5 min | Q510 |
| cauliflower | pieces | 4-6 min | Q510 |
| carrot | pieces | 3-5 min | Q510 |
| parsnip, celeriac | peeled, cubed | 3-5 min | Q510 |
| kohlrabi | peeled, cubed | 2-3 min | Q510 |
| Brussels sprouts | whole | 3-4 min | Q510 |
| new potatoes | small, even-sized | 3-5 min | Q510 |
| white cabbage | not blanched; freezing not recommended, whole head may be frozen for rolls | none | Q510 |
| napa cabbage | not listed | not found | Q510 |
| courgette | not listed | not found | Q510 |
| onion | not listed | not found | Q510 |

Conflicting snippet-only figures (MTV: broccoli 3-6 min, cabbage strips 4-5 min, rutabaga
cubes 2-4 min) were not read and are not evidence.

## Synthesis: packet instructions (product, brand, Lidl or not, soak, cook, endpoint, ids)

No Lidl Finland page with packet text was readable: the two known Lidl product pages are 404,
and lidl.fi search shows only current offers (Q551; R4 `lidl-pages.md`). All rows below are
**not Lidl pages**; two are products Lidl has sold (marked).

| product | brand | Lidl? | soak | cook | endpoint | ids |
| --- | --- | --- | --- | --- | --- | --- |
| dried chickpeas, organic, 500 g | Foodin | not Lidl | 10-12 h, then rinse | boil 60 min | until soft (paraphrase); must not be eaten unprocessed | Q543 (Q550 truncated) |
| dried Finnish peas, 500 g (whole/split not stated) | Kymppi | not Lidl | cold water overnight, pick over | simmer in the soak water about 1 h, then about 1 h more as soup | peas soft | Q545 |
| dried peas, 500 g | Kotimaista | not Lidl | instructions "on the package", not visible | - | - | Q540 |
| yellow peas, 500 g | Papuska | not Lidl | not visible (truncated) | - | - | Q541 |
| whole yellow peas, 500 g | Milletti | not Lidl | not visible (truncated) | - | - | Q544 |
| green peas, dried, 500 g | Ylistalo | not Lidl | not visible (truncated) | - | - | Q546 |
| chickpeas, 500 g | Bazar | not Lidl | not visible (truncated) | - | - | Q542 |
| long-grain rice, parboiled, 1 kg | Ben's Original | not a Lidl page; same product name in a past lidl.fi snippet | none | (1) plenty of boiling water, covered, about 10 min, drain; (2) 1:2 rice:water, covered, low heat about 10 min | (2) all water absorbed | Q547 |
| long-grain rice, 1 kg | Pirkka | not Lidl | - | not visible (truncated) | - | Q548 |
| porridge rice, round-grain, 1 kg | Myllyn Paras | not a Lidl page; seen as a Christmas offer in a past lidl.fi snippet (R4) | none | 3 dl water boiled, 1½ dl rice absorbs it, 7 dl milk, covered about 40 min, stir now and then | none stated; swells about 2½ times | Q549 |

Packet keeping text: Ben's Original and Myllyn Paras give storage only for the dry product
(dry, room temperature / cool, dry, 8-month best-before) (Q547, Q549). No packet read says
anything about storing soaked pulses or cooked rice.
