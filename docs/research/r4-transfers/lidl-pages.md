# Lidl Finland ingredient boundary (R4)

> Research notes of the Lidl catalogue check (R4 step 1), written by a research agent on 2026-11-24 and kept as the record. Summary and use: `catalogue.md`.

## Ids used by the R4 documents

Each id names the Lidl page(s) a statement in `catalogue.md`, `transfers.yaml`
or the ingredient notes rests on. "snippet" = seen only through a search
snippet (summarised); "browser" = read in full in the built-in browser.

| Id | Item | URL(s) | Read |
| --- | --- | --- | --- |
| L1 | Golden Sun organic split peas, chickpeas, lentils (campaign) | https://www.lidl.fi/c/edulliset-vihreat-valinnat/c2834 | snippet; 404 in browser |
| L2 | Kotimainen lehtikaali (offers) | https://www.lidl.fi/c/viikon-tarjoukset-19-22-8/c2239 ; https://www.lidl.fi/c/viikon-tarjoukset-15-18-9/c2802 ; https://www.lidl.fi/c/viikon-tarjoukset/c2854 | snippet |
| L3 | Kotimainen keräkaali (offer) | https://www.lidl.fi/c/viikon-tarjoukset/c2898 | snippet |
| L4 | Parsakaali, frozen 500 g | https://www.lidl.fi/p/parsakaali/p11151157 | browser |
| L5 | Kotimainen lanttu (offers) | https://www.lidl.fi/c/viikon-tarjoukset-9-12-12/c2406 ; https://www.lidl.fi/c/viikon-tarjoukset-29-9-2-10/c2820 | snippet |
| L6 | Potatoes | https://www.lidl.fi/p/kotimainen-jauhoinen-peruna/p11029473 ; https://www.lidl.fi/p/kotimainen-yleisperuna/p11029599 ; https://corporate.lidl.fi/vastuullisuus/vuoropuhelu/kotimaisuus | browser |
| L7 | Pohjolan Meijeri: milks, creams, butters | https://www.lidl.fi/c/pohjolan-meijeri/s10028593 | browser |
| L8 | Onions (mix bag, red onion) | https://www.lidl.fi/c/viikon-tarjoukset-9-12-9/c2269 ; https://www.lidl.fi/fi/c/viikon-tarjoukset-19-11-22-11/c1843/w1 | snippet |
| L9 | Kesäkurpitsa | https://www.lidl.fi/p/kesakurpitsa/p10034397 ; https://www.lidl.fi/p/kesakurpitsa/p10020430 | snippet; first 404 in browser |
| L10 | Eggs (recall notices) | https://www.lidl.fi/c/takaisinvedot/s10021744 | browser |
| L11 | Valikoima: about 3000 products, basic and extended ranges | https://www.lidl.fi/c/valikoima/s10021111 | browser |
| L12 | Kasvisruoka: Freshona and Golden Sun pulses | https://www.lidl.fi/c/kasvisruoka/s10021143 | browser |
| L13 | Press release 11.11.2026 (pulses, lentils, oats) | https://www.sttinfo.fi/tiedote/72493875/suomalaiset-hurahtivat-kuituun-someilmio-nakyy-myos-kaupassa?publisherId=69820360 | browser |
| L14 | Milbona juustoraaste 500 g | https://www.lidl.fi/p/milbona-juustoraaste/p10036865 | snippet; 404 in browser |
| L15 | Kotimainen porkkana 1 kg | https://www.lidl.fi/c/viikon-tarjoukset-28-31-10/c2347 | snippet |
| L16 | Myllykivi oat flakes | https://corporate.lidl.fi/vastuullisuus/vuoropuhelu/kotimaisuus/myllyn-paras | browser |
| L17 | Bergmann naudan jauheliha (batch) | https://www.lidl.fi/p/bergmann-naudan-jauheliha-xxl/p11210131 | browser |
| L18 | Lidl recipes using bagged kale | https://reseptit.lidl.fi/reseptit/lehtikaalikeitto ; https://reseptit.lidl.fi/reseptit/paistettua-naudan-ulkofileeta-paahdettuja-talvijuureksia-ja-rosmariini-bearnaise-kastiketta | browser |


Checked on 2026-11-24. The primary source is lidl.fi, together with reseptit.lidl.fi and corporate.lidl.fi, which are Lidl Finland's own sites, and Lidl Suomi's own press releases on sttinfo.fi.

## The main limit: lidl.fi does not list the regular range

- Lidl says the **vakiovalikoima has about 3000 products**. Some stores carry only the basic range and some carry an extended range ("osa Lidleistä tarjoaa perusvalikoiman, ja osa ... laajennetun valikoiman"). Source: https://www.lidl.fi/c/valikoima/s10021111, read 2026-11-24 in the browser.
- **lidl.fi has no regular-range catalogue.** The category pages (`/h/...`) and the site search (`/q/search?q=`) list only **current offer products**, which match the weekly flyer, plus a few non-food and bakery items. A search for "maito" returned no milk at all, and searches for "herne" and "kikherne" both returned "ei löytynyt tuloksia".
- **Product pages (`/p/...`) for offers are taken down after the offer ends (404).** All 8 historical `/p/` and `/c/viikon-tarjoukset` URLs I re-opened returned 404. The only evidence left of older offers is search-engine snippets of those pages, shown to me through a summarising WebSearch tool. These snippets are marked **"snippet"** below. They usually lack a year and should be treated as weaker evidence.
- So "not found on lidl.fi" is the normal outcome for regular-range staples and **does not mean Lidl doesn't sell the item**. The status column uses these labels:
  - **Confirmed (current)**: on lidl.fi today.
  - **Confirmed (Lidl statement)**: Lidl FI corporate text or a press release names the product or category.
  - **Past offer (snippet)**: seen on lidl.fi in the past, now 404.
  - **Recipe only**: reseptit.lidl.fi uses the ingredient. This is weak evidence, because recipes name generic ingredients, not products.
  - **Not found**: nothing on lidl.fi.

"Read how" values:
- **B**: built-in browser, full page text read by me.
- **S**: search-engine snippet through the summarising WebSearch tool. The page was not opened, and where tested it is now 404.
- **F**: WebFetch, which also summarises.

---

## Group 1: Dried peas and pulses

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Pulses in general (dried) | Confirmed (Lidl statement) | "Freshona- ja Golden Sun -palkokasvit" | Golden Sun = Lidl's own dry-goods brand (dried pulses, rice). Freshona = canned vegetables and pulses | not shown | https://www.lidl.fi/c/kasvisruoka/s10021143 | 2026-11-24 | B | Brand-level only. No individual products are named. |
| Pulses: sales trend | Confirmed (Lidl statement) | "Pavut ja linssit: Erityisesti säilykepalkokasvien menekki on kiihtynyt" | canned pulses, lentils | – | https://www.sttinfo.fi/tiedote/72493875/suomalaiset-hurahtivat-kuituun-someilmio-nakyy-myos-kaupassa?publisherId=69820360 (Lidl Suomi press release 11.11.2026) | 2026-11-24 | B | Confirms that Lidl sells beans and lentils, with canned pulses as the main format. No dried-pea SKU is named. |
| Whole dried yellow peas (keltaiset herneet) | **Not found** | – | – | – | site search https://www.lidl.fi/q/search?q=herne returned no results; WebSearch limited to lidl.fi found nothing | 2026-11-24 | B, S | No lidl.fi page, snippet or press release mentions whole dried yellow peas. I can't say Lidl doesn't sell them. |
| Whole dried green peas | **Not found** | – | – | – | as above | 2026-11-24 | B, S | "Kotimainen herne" p10035731 was **fresh peas in the pod**, a July 2026 seasonal item (snippet: 4,99 €, "Sesongin parasta", dated 10.07.2026). It is not dried peas and the page is now 404. |
| Split peas (halkaistut herneet) | **Occasional campaign (past offer, snippet)** | "Golden Sun Luomulinssit tai -herneet": kikherne, halkaistu herne, punainen linssi tai vihreä linssi | Golden Sun, organic, 500 g, dried, 2,29 € | not in snippet | https://www.lidl.fi/c/edulliset-vihreat-valinnat/c2834 ("Edulliset vihreät valinnat, alkaen torstai 6.10") | 2026-11-24 | S (page now 404, checked in browser) | No year is shown; the URL id range suggests around 2022. This was a themed "green choices" campaign, so the split peas cannot be confirmed as regular range. |
| Hernerouhe | **Not found** | – | – | – | – | 2026-11-24 | S | – |
| Dried chickpeas | **Occasional campaign (past offer, snippet)** | as above, in the same Golden Sun organic campaign ("kikherne") | Golden Sun, organic, 500 g, dried | – | https://www.lidl.fi/c/edulliset-vihreat-valinnat/c2834 | 2026-11-24 | S (404) | No regular-range evidence. |
| Canned chickpeas | **Very likely regular (Lidl statement plus snippet)** | "Freshona kikherneet suolavedessä" | Freshona, can, pack size not seen | – | product name in a snippet of the old page https://www.lidl.fi/fi/p/voimaa-vegestae/gold-green-nyhtoekaura/p4960 (404); brand confirmed on https://www.lidl.fi/c/kasvisruoka/s10021143 | 2026-11-24 | S, B | Lidl's recipes call for chickpeas by the can ("3 tlk kikherneitä", https://reseptit.lidl.fi/reseptit/kikhernepata, read with B). No tetra pack was seen. Pack size is unconfirmed (Freshona is typically 400 g / 240 g drained, but that was not seen on lidl.fi). |
| Chickpea flour (kikhernejauho) | **Not found** | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | Nothing on lidl.fi. It could appear in a themed week (for example an Indian week), but there is no evidence of that. |
| Dried fava beans (härkäpapu) | **Not found** | – | – | – | WebSearch limited to lidl.fi and an open search | 2026-11-24 | S | Only **Härkis** (Verso's cooked fava-bean product) appears, and only as an ingredient in a Lidl bakery pie (sttinfo press release 72247035, snippet) and in the recipe "Härkis-pizzavene". |
| Härkäpapurouhe | **Not found** | – | – | – | – | 2026-11-24 | S | – |
| Dried lentils | **Occasional campaign (past offer, snippet) plus Lidl statement** | "Golden Sun Luomulinssit" (punainen linssi, vihreä linssi) | Golden Sun, organic, 500 g, dried, 2,29 € | – | https://www.lidl.fi/c/edulliset-vihreat-valinnat/c2834 (404); press release 72493875 says lentils are sold | 2026-11-24 | S, B | The lentils are confirmed as sold (press release). The specific SKU and whether it is regular range are not confirmed. |

## Group 2: Kale and cabbages

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Kale (lehtikaali) | **Seasonal offers, past (snippet)** | "Kotimainen lehtikaali" | no brand; **packed by weight: 200 g (1,29 €, 6,45 €/kg) in one offer, 100 g in others**; "maks. 3 kpl/talous" | Finland ("kotimainen") | https://www.lidl.fi/c/viikon-tarjoukset-19-22-8/c2239 (19.–22.8.); https://www.lidl.fi/c/viikon-tarjoukset-15-18-9/c2802 (15.–18.9., -33 %, 1,19 €/100 g); https://www.lidl.fi/c/viikon-tarjoukset/c2854 (from 20.10, -27 %, 1,29 €/100 g) | 2026-11-24 | S (c2802 returned HTTP 404 through F) | The offers ran **August to October**, which fits a Finnish kale season. The year is not shown; the snippet-age metadata suggests 2021–2022. Not on lidl.fi in November 2026. |
| Kale form: bunch or bag | **Bag of leaves, inferred** | – | Lidl's recipe gives "1 pss lehtikaali" and says "Puhdista lehtikaalit ruodeista", i.e. a bag of whole leaves with stems, not chopped | – | https://reseptit.lidl.fi/reseptit/paistettua-naudan-ulkofileeta-paahdettuja-talvijuureksia-ja-rosmariini-bearnaise-kastiketta ; https://reseptit.lidl.fi/reseptit/lehtikaalikeitto ("200 g lehtikaalia ... Poista kaalista kova runko") | 2026-11-24 | B | The 100 g / 200 g weights in the offers also point to a bag. **No whole bunch was seen. No "lehtikaalisilppu" was found.** |
| Cavolo nero (mustakaali) | **Not found** | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | – |
| Savoy cabbage (kurttukaali) | **Not found** | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | – |
| White cabbage (keräkaali) | **Seasonal offer, past (snippet)** | "Kotimainen keräkaali" | loose, per kg, 0,79 €/kg (-24 % from 1,05), "maks. 3 kg/talous" | Finland | https://www.lidl.fi/c/viikon-tarjoukset/c2898 (17.11.–20.11.) | 2026-11-24 | S | No year shown; snippet metadata suggests about 2022. The November date fits the Finnish storage-cabbage season. Lidl's recipes (kaalilaatikko, kaalikääryleet) use it widely. Very likely sold for most of the year, but this is not confirmed. |

## Group 3: Rutabaga, potatoes, dairy

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Rutabaga (lanttu) | **Seasonal offers, past (snippet)** | "Kotimainen lanttu" (also a "Luomu" variant) | loose, per kg; 0,69 €/kg (-46 %) and 0,99 €/kg (-33 %); "maks. 3 kg/talous" | Finland | https://www.lidl.fi/c/viikon-tarjoukset-9-12-12/c2406 (9.–12.12.); https://www.lidl.fi/c/viikon-tarjoukset-29-9-2-10/c2820 (29.9.–2.10.) | 2026-11-24 | S | Autumn and Christmas season; the year is not shown. "Lanttulaatikko" (a ready-made casserole) is on offer 26.–29.11.2026 (https://www.lidl.fi/c/store/loppuviikon-tarjoukset/a10107698, B), but that is not the raw vegetable. |
| Potatoes: jauhoinen | **Confirmed (current)** | "Kotimainen jauhoinen peruna" | 2 kg bag, 1,49 € regular price, offer 1,19 € on 30.11.–2.12.2026 | Finland | https://www.lidl.fi/p/kotimainen-jauhoinen-peruna/p11029473 | 2026-11-24 | B | The 1,49 € regular price shows it is a standing product. The page gives no cultivar. |
| Potatoes: yleisperuna | **Confirmed (current)** | "Kotimainen yleisperuna" | 2 kg bag, 1,49 € regular price, offer 1,19 € (Lidl Plus) on 23.–25.11.2026 | Finland | https://www.lidl.fi/p/kotimainen-yleisperuna/p11029599 | 2026-11-24 | B | – |
| Potatoes: kiinteä | **Not seen now; a named waxy variety in a past offer** | "Kotimainen Jazzy-peruna" | – | Finland | https://www.lidl.fi/p/kotimainen-jazzy-peruna/p10029253 | 2026-11-24 | S (title only) | Jazzy is a firm (kiinteä) variety. No generic "kiinteä peruna" product was found on lidl.fi. |
| New potatoes (uudet perunat) | **Seasonal (Lidl statement)** | "Kotimainen varhaisperuna" | – | Finland (Nauvo grower) | https://corporate.lidl.fi/vastuullisuus/vuoropuhelu/kotimaisuus (links to the varhaisperunat story: potatoes "päätyvät Lidlin hyllyille jo toukokuussa") | 2026-11-24 | B | Season starts in May. |
| Milk | **Confirmed (Lidl statement), regular** | Pohjolan Meijeri milks, e.g. "Ilona-maito" | Pohjolan Meijeri (Lidl's own brand) | Finland, 100 % Finnish milk | https://www.lidl.fi/c/pohjolan-meijeri/s10028593 ("Tämän tuotemerkin alle on koottu kaikki Lidlissä myytävät kotimaiset maidot, piimät, **kermat, voit**, margariinit, jogurtit ja erilaiset juustot") | 2026-11-24 | B | "Ilona-maito" p10027049 is now 404 (checked with B). Fat grades and pack sizes were not seen. |
| Cream: ruokakerma | **Confirmed as a product (past page, snippet) plus brand statement** | "Pohjolan Meijeri Laktoositon ruokakerma" | 200 ml (snippet), Hyvää Suomesta | Finland | https://www.lidl.fi/p/pohjolan-meijeri-laktoositon-ruokakerma/p10025635 (404 when checked) | 2026-11-24 | S | Only the lactose-free variant was seen; regular ruokakerma is not confirmed. |
| Cream: kuohukerma / vispikerma | **Not found by name**; the cream category is confirmed | – | Pohjolan Meijeri "kermat" | Finland | https://www.lidl.fi/c/pohjolan-meijeri/s10028593 | 2026-11-24 | B | Lidl says all its Finnish creams are Pohjolan Meijeri, so whipping cream almost certainly exists, but the exact name, fat % and size were not seen. Vispikerma (a vegetable-fat blend) was not seen at all. |
| Grated cheese (juustoraaste) | **Past product page (snippet)** | "Milbona juustoraaste" (packaging shows "Gratin Cheese Mix") | Milbona, 500 g bag, 4,49 € | not in snippet | https://www.lidl.fi/p/milbona-juustoraaste/p10036865 (404 when checked) | 2026-11-24 | S | The price suggests a regular item, but the page is gone. The Pohjolan Meijeri brand page says Finnish cheeses are under that brand, but no Pohjolan Meijeri raaste was seen. Current dairy offers include Milbona edamviipaleet (sliced cheese), not grated. |
| Butter | **Confirmed (current)** | "Pohjolan Meijeri Laktoositon voi" | Pohjolan Meijeri, 500 g, 4,49 € regular price, offer 3,49 € on 30.11.–2.12.2026 | Finland | https://www.lidl.fi/h/juustot-maitotuotteet-ja-kananmunat/h10095761 (tile with link to /p/pohjolan-meijeri-laktoositon-voi/p11214834) | 2026-11-24 | B | Lactose-free butter. Lidl's brand statement covers "voit" in general. |

## Group 4: Broccoli and carrots

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Broccoli, frozen | **Confirmed (current)** | "Parsakaali" (category: Pakastemarjat ja -vihannekset) | no brand shown, 500 g frozen, 1,69 € regular price, offer 1,39 € on 23.–25.11.2026 | **Spain** ("alkuperämaa: Espanja") | https://www.lidl.fi/p/parsakaali/p11151157 | 2026-11-24 | B | Florets are presumed but the page does not say so. The regular price shows a standing product. |
| Broccoli, fresh whole head | **Not found** | – | – | – | WebSearch limited to lidl.fi; current produce offers | 2026-11-24 | B, S | No fresh broccoli product or offer was found on lidl.fi, only recipes. It is common in Finnish stores, but I can't confirm Lidl sells it from lidl.fi. |
| Carrots | **Past offers (snippet), probably regular** | "Kotimainen porkkana" | 1 kg bag; offers 0,69 €/kg (-30 % from 0,99), 0,79 €; "maks. 3 pkt/talous" | Finland | https://www.lidl.fi/c/viikon-tarjoukset-28-31-10/c2347 ; https://www.lidl.fi/c/viikon-tarjoukset-9-12-12/c2406 ; https://www.lidl.fi/c/viikon-tarjoukset-9-12-9/c2269 | 2026-11-24 | S | The year is not shown. A 0,99 € regular price in the snippet implies a standing product. |

## Group 5: Onions and courgette

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Yellow onion (keltasipuli) | **Past offer (snippet), as a mix** | "Kotimainen sipuli-mix, pakkauksessa kelta- ja punasipuleita" | 1 kg bag, 1,19 € | Finland | https://www.lidl.fi/c/viikon-tarjoukset-9-12-9/c2269 | 2026-11-24 | S | A snippet also mentions "kotimainen luomusipuli 500 g". A plain keltasipuli SKU was not seen. |
| Large / jumbo onion | **Not found** | – | – | – | – | 2026-11-24 | S | – |
| Red onion (punasipuli) | **Past offers (snippet)** | "Kotimainen punasipuli" | 500 g, 0,85 € ("TUORETTA"); also 0,59 € (-33 %) | Finland | https://www.lidl.fi/fi/c/viikon-tarjoukset-19-11-22-11/c1843/w1 ; https://www.lidl.fi/c/viikon-tarjoukset-28-31-10/c2347 | 2026-11-24 | S | The year is not shown. "TUORETTA" without a discount suggests the normal price. |
| Shallot (salottisipuli) | **Not found** (recipes only) | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | Only appears in recipes such as Broileria Cacciatore. |
| Courgette (kesäkurpitsa) | **Past offers (snippet), spring/summer** | "Kesäkurpitsa" | loose, per kg; 1,49 €/kg (-25 %, regular 1,99 €/kg) dated 15.05.2026; 1,69 €/kg (-22 %); 1,29 €/kg (-50 %) on 22.4.–25.4. | **Spain** in two of the snippets | https://www.lidl.fi/p/kesakurpitsa/p10034397 (404 when checked); https://www.lidl.fi/p/kesakurpitsa/p10020430 ; https://www.lidl.fi/fi/c/yksi-akku-monta-laitetta/c2038 | 2026-11-24 | S | A regular price of 1,99 €/kg suggests a standing item. It is imported, so it is not Finnish-seasonal. |

## Group 6: Staples

| item | status | Lidl product name | brand, pack, form | origin | URL read | date | read how | note |
|---|---|---|---|---|---|---|---|---|
| Eggs | **Confirmed regular (Lidl statement plus lidl.fi recall notices)** | "Kot-Kot-Kotimaiset vapaan kanan kananmuna M10 / L15"; "Laitilan Kanatarhan Vapaan kanan kananmuna M15"; earlier "Kieku vapaan kanan munia" | free-range or organic only, M10 / L15 / M15 boxes | Finland ("Kaikki Suomessa myymämme tuoreet kananmunat ovat lattia- ja luomukanaloista, ja lisäksi ne ovat kotimaisia") | https://www.lidl.fi/c/takaisinvedot/s10021744 (recalls 23.6. and 18.8.2026); https://corporate.lidl.fi/vastuullisuus/reilu-toiminta/elainten-hyvinvointi | 2026-11-24 | B | Strongest evidence of any staple. |
| Breadcrumbs (korppujauho) | **Not found** as a product | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | Appears only as an ingredient in Lidl bakery items and recipes. |
| Wheat flour (vehnäjauho) | **Not found** as a named product | – | – | – | WebSearch limited to lidl.fi; corporate Myllyn Paras article | 2026-11-24 | S, B | The Myllyn Paras article mentions flour sales rising at Lidl during COVID but names no SKU. A Belbake gluten-free flour mix is mentioned in an old snippet. Almost certainly regular, but not confirmed. |
| Potato starch (perunajauho) | **Not found** | – | – | – | – | 2026-11-24 | S | Recipes only. |
| Oat flakes (kaurahiutaleet) | **Confirmed regular (Lidl statement)** | "Myllykiven kaurahiutaleita ja pikakaurahiutaleita, Kaurahiutale+kuitu" | Myllykivi (Lidl's own brand, made by Myllyn Paras) | Finland (Hyvinkää mill) | https://corporate.lidl.fi/vastuullisuus/vuoropuhelu/kotimaisuus/myllyn-paras (article from 03/2023); press release 72493875 (11.11.2026: "Kaurahiutaleet, pikapuurot ja leseet: Myynti on kasvanut ... 19 %") | 2026-11-24 | B | Pack size was not seen. |
| Porridge rice (puuroriisi) | **Past offer (snippet), Christmas** | "Myllyn Paras Puuroriisi" | Myllyn Paras, 1 kg, 2,89 € | rice is imported (Myllyn Paras: "Ainoastaan durum-vehnä ja riisi hankitaan ulkomailta") | https://www.lidl.fi/p/myllyn-paras-puuroriisi/p10029709 ("Myymälässä 18.12. - 24.12.") | 2026-11-24 | S | The year is not shown. It may be Christmas-only or a Christmas offer on a regular item. |
| Long-grain rice | **Past product page (snippet)** | "Ben's Original Pitkäjyväinen riisi" | Ben's Original, around 3,79 €/kg | – | https://www.lidl.fi/p/ben-s-original-pitkajyvainen-riisi/p10027070 | 2026-11-24 | S | Golden Sun basmati is named in a Lidl recipe (https://reseptit.lidl.fi/reseptit/curry-lohipyorykat-ja-mangosalsa, snippet). |
| Barley (ohra / ohrasuurimo) | **Not found** | – | – | – | WebSearch limited to lidl.fi | 2026-11-24 | S | – |
| Minced meat (jauheliha) | **Confirmed (current), batch offer** | "Bergmann Naudan jauheliha XXL" | Bergmann, 1 kg, 18 % fat, "Erä" (limited batch), 10,99 € on 26.–29.11.2026 | **Germany** ("lihan alkuperämaa: Saksa") | https://www.lidl.fi/p/bergmann-naudan-jauheliha-xxl/p11210131 | 2026-11-24 | B | This is a batch item. Lidl says its **Reilu** fresh meat is always Finnish (corporate kotimaisuus page), but no Reilu jauheliha SKU was seen. Regular Finnish mince is very likely but not confirmed on lidl.fi. |
| Baking powder (leivinjauhe) | **Not found** | – | – | – | – | 2026-11-24 | S | Recipes only. |
| Fresh parsley / coriander | **Past offer (snippet)** | "Kotimaiset ruukkuyrtit" (including coriander and parsley) | potted | Finland | https://www.lidl.fi/fi/c/viikon-tarjoukset-29-3-7-4/c2021/w1 | 2026-11-24 | S | The snippet is old (about 2020–21). Lidl recipes use "1 ruukku korianteria / lehtipersiljaa". |
| Garlic | **Not found** as a product | – | – | – | – | 2026-11-24 | S | Recipes only. Almost certainly stocked, but not evidenced. |
| Ground cumin (juustokumina) | **Not found** | – | – | – | – | 2026-11-24 | S | Lidl recipes use juustokumina (for example https://reseptit.lidl.fi/reseptit/linssikeitto, read with B), but no product was found. |
| Dark syrup (tumma siirappi) | **Not found** | – | – | – | – | 2026-11-24 | S | Christmas baking season; it may appear in a Christmas baking campaign. A snippet for "Parhaan joulun ainekset" (c2912) did not show syrup. |

---

## Pages that failed

All of these were reached through search results and are now gone.
- https://www.lidl.fi/p/kotimainen-herne/p10035731: HTTP 404 (browser)
- https://www.lidl.fi/c/edulliset-vihreat-valinnat/c2834: HTTP 404 ("Hups! Sivua ei ole olemassa", browser)
- https://www.lidl.fi/p/voimaa-vegestae/findus-quorn-kuutiot/p4949: redirected to /404 (browser)
- https://www.lidl.fi/p/milbona-juustoraaste/p10036865: 404 (browser)
- https://www.lidl.fi/p/pohjolan-meijeri-laktoositon-ruokakerma/p10025635: 404 (browser)
- https://www.lidl.fi/p/pohjolan-meijeri-ilona-maito/p10027049: 404 (browser)
- https://www.lidl.fi/p/kesakurpitsa/p10034397: 404 (browser)
- https://www.lidl.fi/c/viikon-tarjoukset-15-18-9/c2802: HTTP 404 (WebFetch)

I did not re-open the other snippet URLs in the tables. They are probably also 404, because expired offers are removed.

Other failures:
- WebFetch of https://www.lidl.fi/q/search?q=herne returned an empty product grid ("The browser is not supported"). The site is client-rendered, so I used the browser instead.
- A same-origin request to lidl.fi's internal search API from the browser was blocked by the session's permission classifier. I did not pursue it and used only visible pages.
- No captcha appeared. I declined non-essential cookies on lidl.fi ("HYLKÄÄ") and on sttinfo.fi ("Hylkää kaikki").

## Method

**Tools.** I used the built-in browser (navigate, get_page_text, and in-page JavaScript that only scrolls to load lazy tiles and reads the rendered text) for every page marked B. I used WebSearch, mostly limited to lidl.fi, to find historical lidl.fi pages; those are marked S, because the tool returns a model-written summary of the index snippets, not the page.

**lidl.fi structure.**
- `/h/<category>/h…` are product-category pages. They show **only current offers**: for example, Kuivatuotteet had 7 products and Öljyt, mausteet ja kastikkeet had 2.
- `/c/store/<campaign>/a…` are offer collections: alkuviikon tarjoukset, loppuviikon tarjoukset, Lidl Plus -tarjoukset, Uutta valikoimassa, Maukas joulu.
- `/q/search?q=` is the site search, over the same offer set.
- `/p/<slug>/p<id>` are product pages. They give the price, pack size, offer dates, sometimes origin ("alkuperämaa"), and a breadcrumb that tells frozen from fresh.
- `/c/<topic>/s…` are text pages. The useful ones were Valikoima, Kasvisruoka, Pohjolan Meijeri, Myllykivi and Takaisinvedot.
- `/l/fi/tarjouslehdet/...` are image flyers. I checked the 26.–29.11. hevi spread visually; it matched the `/h/` offer tiles.
- reseptit.lidl.fi recipes list generic ingredients and rarely brands.
- corporate.lidl.fi has the brand and sourcing statements.

**Search terms.**
- On-site search: herne, kikherne, maito.
- WebSearch limited to lidl.fi: kuivatut herneet, kikherneet, kikhernejauho, härkäpapu, Golden Sun herneet/linssit, Freshona kikherneet, lehtikaali (with kotimainen and tarjous), keräkaali kurttukaali, lanttu kotimainen, parsakaali tuore, porkkana, sipuli/punasipuli/salottisipuli, kesäkurpitsa, kuohukerma/ruokakerma Pohjolan Meijeri, juustoraaste, kananmunat, vehnäjauho Myllyn Paras, korppujauho/perunajauho/leivinjauhe, puuroriisi/kaurahiutaleet/ohrasuurimo, pitkäjyväinen riisi, siirappi, juustokumina, persilja/korianteri.
- Open-web searches for secondary sources (Open Food Facts, news, forums) found nothing Finland-specific for dried peas, fava, chickpea flour or kale.

**Limits.**
1. The regular range of about 3000 products is not published online, so most staples can only be shown through brand statements, recalls, or past offers.
2. Past-offer snippets usually lack a year, and their wording comes from a summarising tool, so prices and pack sizes in rows marked S should be checked in store.
3. Some products are only in extended-range stores.
4. Seasonality is inferred from offer dates (kale Aug–Oct, lanttu Sept–Dec, cabbage Nov, new potatoes from May) and is not stated by Lidl, except for new potatoes.

**Best next step:** a shelf check at one store, or a look in the Lidl Plus app, which may show more of the range. That would settle dried yellow and green peas, kikhernejauho, kale form in November, fresh broccoli, cream types, and the baking staples.
