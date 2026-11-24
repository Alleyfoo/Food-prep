# Sources

## How the evidence was gathered

- **Web recipes (step 1).** On 2026-11-24 three research agents each searched
  one group of traditions in the traditions' own languages and **opened and
  read** every page they cite (127 pages). A URL appears below only if the
  page was read; pages that failed (HTTP 403/404/410, captcha, a wrong
  recipe behind a URL) are listed (here, or for E under "Gaps and caveats (E)"
  in `recipes.md`) and not used. Pages were read through a
  fetch tool that renders and summarises a page; the recipe paraphrases in
  `recipes.md` rest on that rendering, and one quantity it rendered
  implausibly (M13a flour) is marked unverified there.
- **Independence.** Several pages are not independent witnesses, and are
  counted as one: M19b copies M19a; A2b closely follows A2a; three
  karnıyarık recipes (M5) come from one site; several Mawdoo3 pages share a
  house style; acarajé (A18c) descends historically from akara (A18a-b), so
  it is diffusion, not convergence. Some sources are user-submitted
  (smaker.pl, 10000recipe, food.com) or SEO-style sites (hurbra.se); they are
  marked in `recipes.md`.
- **Corpus (step 1, second witness).** RecipeNLG `full_dataset.csv`
  (2,231,142 recipes; Bień et al. 2020, non-commercial research licence),
  read locally by `count_construction.py`. Only counts are committed; the
  sampled sentences for the hand check stay in the gitignored corpus folder.
  It is mostly North American, so it shows one tradition's practice in bulk
  (see `recipenlg.md`).
- **Model files read, not cited as evidence:** `src/foodprep/data/
  part_properties.yaml`, `operations.yaml` (R1) and `tomato.yaml`
  (transformations, `input_component`, `byproducts`, `uses`).
- **Physical explanations** in `mechanisms.md` (starch gelatinisation and
  retrogradation, protein coagulation, osmosis) are general food science
  (McGee, *On Food and Cooking*, cited as `mcgee` in R1 `sources.md`), used
  only to name what the recipes do. Where a recipe states its own reason it is
  quoted; where only the science explains a step, the text says so.

Ids: **E-n**, **M-n**, **A-n** are the page numbers of each region's table
below. Recipe ids such as E5a (in `recipes.md`) name the recipe; each
region's table says which recipes a page supports.

## E: Northern, Central and Eastern Europe, Ashkenazi

| Id | URL | Language | Used for |
|---|---|---|---|
| E-1 | https://gaultmillau.ch/rezepte/caminadas-rosti-tipp-lassen-sie-sich-zeit-312616 | German (CH) | 1a, 1b |
| E-2 | https://www.blick.ch/life/essen/genuss/kochbuchautor-weiss-wie-es-geht-meine-roesti-wird-immer-matschig-was-mache-ich-falsch-id19868794.html | German (CH) | 1c |
| E-3 | https://austria-forum.org/af/AustriaWiki/R%C3%B6sti | German | 1d |
| E-4 | https://de.wikibooks.org/wiki/Kochbuch/_Kartoffelpuffer | German | 2a |
| E-5 | https://www.koeln.de/?p=76323 | German | 2b |
| E-6 | https://smaker.pl/przepisy-dania-glowne/przepis-placki-ziemniaczane-wg-magdy-gessler,115549,futka.html | Polish | 3a |
| E-7 | https://smaker.pl/przepisy-dania-glowne/przepis-chrupiace-placki-ziemniaczane,169717,bryssska.html | Polish | 3b |
| E-8 | https://www.kipa.co.il/אוכל/1216594-0/ | Hebrew | 4a |
| E-9 | https://www.maariv.co.il/food/article-613596 | Hebrew | 4b |
| E-10 | https://t-j.ru/draniki/ | Russian | 5a |
| E-11 | https://aif.ru/food/world/glavnoe_skorost_kak_prigotovit_idealnye_draniki | Russian | 5b |
| E-12 | https://tsn.ua/other/iak-pryhotuvaty-smachni-zolotavi-deruny-z-khrumkoiu-skorynkoiu-bez-muky-ta-iayets-sposib-nashykh-babus-3163451.html | Ukrainian | 5c |
| E-13 | https://www.koket.se/filip_fasten/varmratter/gronsaker__potatis_och_andra_rotfrukter/raggmunk_med_lingon_och_flask | Swedish | 6a |
| E-14 | https://visitsweden.com/what-to-do/food-drink/recipes/potato-pancakes-aka-raggmunk-recipe/ | English (second witness) | 6b |
| E-15 | https://hurbra.se/?p=51854 | Swedish | 7a |
| E-16 | https://www.martha.fi/recept/rarakor-med-norsrom | Swedish (FI) | 7b |
| E-17 | https://www.koket.se/niclas_wahlgren/varmratter/_/mormor_janes_kroppkakor | Swedish | 8a |
| E-18 | https://alkas.lt/2021/11/02/keletas-gudrybiu-gaminant-cepelinus | Lithuanian | 9a |
| E-19 | https://www.tv3.lt/receptas/421/cepelinai | Lithuanian | 9b |
| E-20 | https://www.kuechengoetter.de/rezepte/download/Thueringer-Kloesse-2240.pdf | German | 10a |
| E-21 | https://www.t-online.de/leben/essen-und-trinken/rezepte/id_100272192/thueringer-kloesse-traditionelles-rezept-mit-kartoffeln.html | German | 10b |
| E-22 | https://www.oekotest.de/essen-trinken/kartoffelkloesse-selbst-machen-beliebte-rezepte-und-hilfreiche-tipps_602208_1.html?preview=true | German | 10c |
| E-23 | https://www.lecker.de/klassische-semmelknoedel-selber-machen-so-gehts-78561.html | German | 11a |
| E-24 | https://ooe.lfi.at/pdf+30000+2688384 | German (AT) | 11b |
| E-25 | https://www.mtvuutiset.fi/artikkeli/5-9-kaalikaaryleet/3216332 | Finnish | 12a |
| E-26 | https://yle.fi/a/7-557673 | Swedish (FI) | 12b |
| E-27 | https://smaker.pl/przepisy-dania-glowne/przepis-babcine-golabki,1923515,smaker.html | Polish | 13a |
| E-28 | https://www.mtvuutiset.fi/artikkeli/kaalilaatikko-ja-uuniomenat-27-9-1999/3216814 | Finnish | 14a |
| E-29 | https://www.mtvuutiset.fi/makuja/artikkeli/kaikkien-aikojen-paras-kaalilaatikko-rouva-kasvis-paljastaa-valmistustavan-jolla-saa-lyomattoman-lopputuloksen/6579806 | Finnish | 14b |
| E-30 | https://www.mtvuutiset.fi/artikkeli/8-2-karjalanpiirakat/3216082 | Finnish | 15a |
| E-31 | https://www.kaleva.fi/ruistaikinasta-suussa-sulavat-herkut/1681736 | Finnish | 15b |
| E-32 | https://smaker.pl/przepisy-dania-glowne/przepis-prawdziwe-ruskie-pierogi-przepis-babci-irenki,117909,agnieszkacrow.html | Polish | 16a |
| E-33 | https://media.halvacard.ru/food/vareniki-s-kartoskoi | Russian | 16b |
| E-34 | https://www.mtvuutiset.fi/makuja/reseptit/resepti/lanttu-ja-porkkanalaatikko/5678748 | Finnish | 17a |
| E-35 | https://kotiliesi.fi/resepti/porkkanalaatikko/ | Finnish | 17b |
| E-36 | https://www.k-ruoka.fi/reseptit/perinteinen-porkkanalaatikko | Finnish | 17c |
| E-37 | https://www.martha.fi/recept/morots-halloumibiffar-med-pesto-och-morotspasta | Swedish (FI) | 18a |
| E-38 | https://ingmar.app/blogg/morots-och-halloumibiffar | Swedish | 18b |
| E-39 | https://www.knatteplock.se/blogs/enkla-recept-for-barn-familj/zucchini-och-morotsbiffar-med-halloumi | Swedish | 18c |
| E-40 | https://www.mtvuutiset.fi/makuja/reseptit/resepti/porkkanapihvit-kermassa-haudutettujen-mustajuurien-kera/5650684 | Finnish | 18d |
| E-41 | https://www.lecker.de/zucchinipuffer-74266.html | German | 19a |
| E-42 | https://smaker.pl/przepisy-dodatki/przepis-placki-z-cukinii,174841,anetap.html | Polish | 19b |

## M: Mediterranean, Middle East, Iberia, France

| Id | URL | Language |
|---|-----|----------|
| M-1 | https://mawdoo3.com/طريقة_عمل_الطعمية_المصرية | Arabic |
| M-2 | https://mawdoo3.com/طريقة_عمل_الطعمية_المصرية_مثل_المطاعم | Arabic |
| M-3 | https://julienjulia.blogspot.com/2014/05/taameya-egyptian-falafel.html | Arabic + English |
| M-4 | https://mawdoo3.com/طريقة_عمل_الفلافل_الشامية | Arabic |
| M-5 | https://mawdoo3.com/طريقة_عمل_عجينة_الفلافل | Arabic |
| M-6 | https://yemek.com/tarif/kabak-mucveri-2/ | Turkish |
| M-7 | https://www.posta.com.tr/galeri/evde-kabagi-olan-hemen-denesin-asla-dagilmiyor-tam-kivaminda-oluyor-2982761 | Turkish |
| M-8 | https://www.argiro.gr/recipe/kolokythokeftedes/ | Greek |
| M-9 | https://www.sbs.com.au/language/greek/el/podcast-episode/zucchini-fritters-kolokithokeftedes/apz0l1iku | Greek intro, English recipe |
| M-10 | https://yemek.com/tarif/karniyarik/ | Turkish |
| M-11 | https://yemek.com/tarif/firinda-karniyarik-8/ | Turkish |
| M-12 | https://yemek.com/tarif/kiymali-klasik-karniyarik/ | Turkish |
| M-13 | https://yemek.com/tarif/tam-olculu-zeytinyagli-yaprak-sarma/ | Turkish |
| M-14 | https://www.milliyet.com.tr/yemek/yaprak-sarmasi-lokum-gibi-oluyor-ve-asla-dagilmiyor-sert-yapraklari-yumusacik-yapan-taktik-7065529 | Turkish |
| M-15 | https://www.parapolitika.gr/gefsis/article/1008164/gemista-opos-tis-mamas/ | Greek |
| M-16 | https://www.tovima.gr/2015/08/15/gefsignostis/ge-ista-katsarolas-3/amp/ | Greek |
| M-17 | https://www.parapolitika.gr/gefsis/article/1087783/lahtaristi-spitiki-spanakopita/ | Greek |
| M-18 | https://yemek.com/tarif/cigden-ispanakli-borek/ | Turkish |
| M-19 | https://www.dissapore.com/cucina/come-fare-la-perfetta-parmigiana-di-melanzane/index.php | Italian |
| M-20 | https://blog.giallozafferano.it/saporediarianna/ricetta-parmigiana-di-melanzane-siciliana-tradizionale/ | Italian |
| M-21 | https://www.balarm.it/news/facili-morbide-dentro-e-croccanti-fuori-come-fare-le-polpette-di-melanzane-alla-siciliana-169720 | Italian |
| M-22 | https://www.ricettedalmondo.it/polpette-di-melanzane-alla-siciliana.html | Italian |
| M-23 | https://www.dissapore.com/ricette/arancini-ricetta-autentica/ | Italian |
| M-24 | https://www.dissapore.com/ricette/suppli-mozzarella-e-pomodoro/ | Italian |
| M-25 | https://realacademiadegastronomia.com/recetas/tortilla-de-patata/ | Spanish |
| M-26 | https://www.directoalpaladar.com/2008/10/13-receta-de-mi-tortilla-de-patatas | Spanish |
| M-27 | https://andaluciainforma.es/?p=14348 | Spanish |
| M-28 | https://www.directoalpaladar.com/recetas-de-aperitivos/croquetas-jamon-iberico-huevo-duro-receta-clasica-que-nunca-falla | Spanish |
| M-29 | https://www.directoalpaladar.com/ingredientes-y-alimentos/arguinano-tiene-clave-croquetas-no-se-te-rompan-al-freirlas-no-esta-rebozado | Spanish |
| M-30 | https://www.e-konomista.pt/pasteis-de-bacalhau/ | Portuguese (PT) |
| M-31 | https://postal.pt/nacional/aprenda-a-fazer-pasteis-de-bacalhau-a-moda-antiga-com-receita-original-de-1904/ | Portuguese (PT) |
| M-32 | https://teleculinaria.pt/receitas/pasteis-de-bacalhau-no-forno-tradicional | Portuguese (PT) |
| M-33 | https://www.alpes-isere.com/decouvrir-lisere/gratin-dauphinois | French |
| M-34 | https://meilleurduchef.com/fr/recette/gratin-dauphinois.html | French |
| M-35 | https://www.jours-de-marche.fr/specialites/petits-farcis-nicois.html | French |
| M-36 | https://lefooding.com/recettes/farcis-nicois-vegetariens | French |
| M-37 | https://www.gustoblog.it/2023/08/12/zucchine-ripiene-alla-ligure-la-ricetta-originale | Italian |
| M-38 | https://blog.giallozafferano.it/renatabriano/verdure-ripiene-alla-genovese/ | Italian |
| M-39 | https://stephanelarue.com/ces-beignets-de-courgettes-croustillants-se-preparent-en-25-minutes/ | French |
| M-40 | https://www.corsenetinfos.corsica/A-table-les-beignets-de-courgettes-de-Francoise_a43148.html | French |
| M-41 | https://www.directoalpaladar.com/recetas-de-aperitivos/pimientos-rellenos-bacalao-gambas-receta-clasico-que-siempre-triunfa | Spanish |
| M-42 | https://www.lacomarca.net/pimientos-rellenos-de-bacalao/ | Spanish (syndicated copy of 41) |
| M-43 | https://www.dissapore.com/ricette/ricetta-frittata-di-zucchine/ | Italian |

Tried and failed (not cited as evidence): parianostypos.gr kolokythokeftedes (HTTP 403), slate.fr
gratin dauphinois (HTTP 403), visitportugal.com codfish cakes (bot-protection page, no content).

## A: South and East Asia, Latin America, Africa

| Id | URL | Language | Dish |
|---|-----|----------|------|
| A-1 | https://hebbarskitchen.com/hi/onion-pakoda-recipe-kanda-bhaji/ | Hindi | onion pakoda |
| A-2 | https://www.aajtak.in/lifestyle/news/story/how-to-make-aloo-pyaz-bhajiya-recipe-at-home-ghar-pe-banayen-aloo-pyaz-bhajiya-tvisp-dskc-2613339-2026-08-01 | Hindi | aloo pyaz bhajiya |
| A-3 | https://hebbarskitchen.com/hi/aloo-tikki-recipe-aloo-ki-tikki/ | Hindi | aloo tikki |
| A-4 | https://www.aajtak.in/lifestyle/kitchen/story/aloo-tikki-recipe-market-style-crispy-potato-snacks-at-home-bazar-jaisa-nasta-ghar-par-tmovx-dskc-2579083-2026-06-15 | Hindi | aloo tikki |
| A-5 | https://hebbarskitchen.com/hi/medu-vada-recipe-medhu-vadai/ | Hindi | medu vada |
| A-6 | https://ranveerbrar.com/recipes/medu-vada/ | English | medu vada |
| A-7 | https://macaro-ni.jp/37027 | Japanese | tempura |
| A-8 | https://tokubai.co.jp/news/articles/2074 | Japanese | tempura |
| A-9 | https://delishkitchen.tv/articles/58 | Japanese | kakiage |
| A-10 | https://tokubai.co.jp/news/articles/2224 | Japanese | korokke |
| A-11 | https://macaro-ni.jp/82670 | Japanese | okonomiyaki |
| A-12 | https://delishkitchen.tv/recipes/518539166141645953 | Japanese | okonomiyaki |
| A-13 | https://macaro-ni.jp/85847 | Japanese | okonomiyaki |
| A-14 | https://www.mitsubishielectric.co.jp/club-me/knowledge/washoku03/04katsuobushi/recipes04.html | Japanese | chawanmushi |
| A-15 | https://macaro-ni.jp/41221?page=2 | Japanese | chawanmushi (partial) |
| A-16 | https://www.10000recipe.com/recipe/6903842 | Korean | hobak-jeon |
| A-17 | https://www.10000recipe.com/recipe/6855442 | Korean | hobak-jeon |
| A-18 | https://www.10000recipe.com/recipe/6850115 | Korean | gamja-jeon |
| A-19 | https://www.10000recipe.com/recipe/7057502 | Korean | gamja-jeon |
| A-20 | https://post.smzdm.com/p/ak852x3r/ | Chinese | courgette dumplings |
| A-21 | https://www.toutiao.com/zixun/7529720838241929216 | Chinese | courgette xianbing |
| A-22 | https://m.bendibao.com/show734563.html | Chinese | zha qie he |
| A-23 | https://omnivorescookbook.com/fried-stuffed-eggplant/ | English | zha qie he |
| A-24 | https://vnexpress.net/cha-gio-tom-gion-thom-4358785.html | Vietnamese | chả giò |
| A-25 | https://vtcnews.vn/meo-lam-nem-khong-bi-chay-nuoc-ar972331.html | Vietnamese | nem rán |
| A-26 | https://hoanghamobile.com/tin-tuc/cach-lam-cha-gio-nem-ran/ | Vietnamese | chả giò / nem rán |
| A-27 | https://www.excelsior.com.mx/recetas/receta-chiles-rellenos-capeados | Spanish | chiles rellenos |
| A-28 | https://www.univision.com/delicioso/receta-de-chiles-rellenos | Spanish | chiles rellenos |
| A-29 | https://grupoanimal.mx/gastronomia/recetas/3-trucos-para-capear-chiles-rellenos-a-la-perfeccion-como-los-de-mama | Spanish | capeado (partial) |
| A-30 | https://www.directoalpaladar.com/otros/este-truco-chef-zahie-tellez-para-preparar-claras-hacer-capeado-perfecto | Spanish | capeado (partial) |
| A-31 | https://grupoanimal.mx/gastronomia/recetas/masa-para-tamales-desde-cero | Spanish | tamales |
| A-32 | https://www.directoalpaladar.com/recetas-de-panes/tamales-mexicanos-como-hacerlos-casa-paso-a-paso | Spanish | tamales |
| A-33 | https://www.receiteria.com.br/imprimir/?id=366042 | Portuguese | pão de queijo |
| A-34 | https://www.tudogostoso.com.br/receita/187044-pao-de-queijo-verdadeiro.html | Portuguese | pão de queijo |
| A-35 | https://www.tudogostoso.com.br/noticias/bolinho-de-abobrinha-como-fazer-a2252.htm | Portuguese | bolinho de abobrinha |
| A-36 | https://www.tudogostoso.com.br/receita/99535-bolinho-de-abobrinha.html | Portuguese | bolinho de abobrinha |
| A-37 | https://ounjealadun.com/2015/03/14/secret-to-great-akara-balls/ | English | akara |
| A-38 | https://cheflolaskitchen.com/akara-acaraje/ | English | akara |
| A-39 | https://www.tudogostoso.com.br/noticias/como-fazer-acaraje-a1506.htm | Portuguese | acarajé |
| A-40 | https://cheflolaskitchen.com/make-moin-moin-moi-moi/ | English | moin moin |
| A-41 | https://kitchenbutterfly.com/2010/moin-moin-steamed-nigerian-bean-cake | English | moin moin |
| A-42 | https://www.food.com/recipe/vegan-yeshimbra-assa-ethiopian-chickpea-fritters-132544 | English | yeshimbra asa |

Not covered from the starting list: arepas, bánh xèo, pajeon, tamagoyaki, spring rolls (Chinese), 酿青椒. No Amharic source was found or read.
