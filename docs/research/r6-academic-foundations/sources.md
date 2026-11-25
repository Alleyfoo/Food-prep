# R6 sources: verified bibliography and evidence register

Every source cited in R6 has an id (Y100-Y799, one range per area). The full
entry is in its area's evidence file:
- the citation details, each marked "not verified" where they could not be
  checked;
- which version was read;
- what the source represents and what it shows;
- section pointers.

The table below is an index of those entries, extracted from the evidence
files (`py -3.11 -I` over the `### Ynnn` headings). Read the evidence file
before citing a source. Date read: 2026-11-25.

## Rules the agents followed

Set in `research-brief.md`, before reading:
- read the full text where accessible, and say which version was read;
- a page seen only as a search snippet is not evidence;
- never invent a URL, DOI or citation detail;
- paraphrase, with quotes under 15 words;
- follow citations backward and forward;
- search in the languages where the work exists.

## Counts

| How read | Entries |
| --- | --- |
| full text (publisher, PMC, arXiv, repository or author PDF) | 51 |
| full text, through the fetch tool's summarising digest (details less certain) | 17 |
| in part (named sections, chapters, previews of standards, documentation) | 28 |
| abstract, landing or catalogue page only | 17 |
| **entries** | **113** |
| **distinct works** (three read twice under two ids, see below) | **110** |

The 17 entries read only as an abstract, landing page or catalogue:
- Y117, Y207, Y214;
- Y219: the PDF was obtained, but its Japanese text did not decode;
- Y420;
- Y509-Y516;
- Y600: the ISA catalogue page;
- Y609, Y610, Y616.

No conclusion in R6 rests on one of these alone. Where one is mentioned,
the text says "abstract".

**Read twice under two ids** (the same work reached from two areas; both
entries are kept, and they agree):
- Y105 = Y401: Ławrynowicz et al. 2022, the substitution ontology design
  pattern;
- Y113 = Y403: Bikakis et al. 2023, the graphical formalism, arXiv
  2306.09042;
- Y406 = Y701: Teng, Lin and Adamic 2012, ingredient networks, arXiv
  1111.3919.

**Failed pages:** 107 rows across the seven "Failed pages and
abstract-only" tables, each with the fallback tried. Recurring blocks:
- ResearchGate (403);
- HAL (a bot wall: every French HAL deposit);
- core.ac.uk and some DFKI pages (403);
- MDPI (403);
- ScienceDirect full text (paywall);
- FAO (403; the Codex PDF was read from a university mirror, Y611);
- Semantic Scholar (429, so forward-citation search relied on the papers'
  own citing lists and Google Scholar where readable).

**Starting sources from the brief, and the version actually read:**

| Brief's starting source | Read as | Id |
| --- | --- | --- |
| Food Process Ontology Requirements (SWJ) | accepted manuscript PDF on the journal site, in full | Y100 |
| Ontological How and Why (PMC10352767) | Europe PMC full-text XML, in full | Y101 |
| FOON (USF digital commons) | arXiv v4, in full (the USF record has no PDF) | Y201 |
| Approximate Task Tree Retrieval (arXiv 2207.03693) | arXiv v1, in full | Y206 |
| RiCoRecA (Frontiers 2025) | publisher HTML through the fetch digest | Y502 |
| CookingCAKE (ResearchGate, 403) | CEUR-WS Vol-1520 PDF, in full | Y300 |
| ProCAKE publications | the list page (titles and venues only) | Y313 |
| Substitution ODP (PMC8837940) | PMC full text, in full | Y105, Y401 |
| Commonsense reasoning for substitution (UCL) | UCL repository PDF of the published DKE article, in full | Y402 |
| English Recipe Flow Graph Corpus | ACL Anthology PDF, in full | Y500 |
| ISA-88 (isa.org) | catalogue page; the standard's content from Johnsson's 1999 Lund thesis (Y602) and the IEC 61512-3/-4 previews (Y603, Y604) | Y600, Y602-Y604 |
| Recipe classes in food industry (EJOR, ScienceDirect) | abstract only; Houba et al. 2000, EJOR 122(2) | Y609 |

## Index

## Ontologies (`evidence-ontologies.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y100 | https://www.semantic-web-journal.net/system/files/swj3096.pdf | Damion Dooley, Magalie Weber, Liliana Ibanescu, Matthew Lange, Lauren Chan, Larisa Soldatova, Chen Yang, Robert Warren, Cogan Shimizu, Hande K. McGinty, William Hsiao. "Food Process Ontology Requirements". Semantic Web 1… | accepted manuscript PDF from the journal's site (36 pp.), read in full. The typeset IOS/SAGE version was not read. |
| Y101 | https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1137961/full | Damion Dooley, Tarini Naravane, 2023, "Ontological how and why: action and objective of planned processes in the food domain", Frontiers in Artificial Intelligence 6: 1137961. DOI 10.3389/frai.2023.1137961. PMC10352767. … | Europe PMC full-text XML (PMC10352767), read in full; the Frontiers HTML was also read (via fetch digest). The PMC page itself was blocked. |
| Y102 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10477341/fullTextXML | Magalie Weber, Patrice Buche, Liliana Ibanescu, Stephane Dervaux, Herve Guillemin, Julien Cufi, Michel Visalli, Elisabeth Guichard, Caroline Penicaud, 2023, "PO2/TransformON, an ontology for data integration on food, fee… | Europe PMC full-text XML, read in full. nature.com and link.springer.com redirected to a login. |
| Y103 | https://ceur-ws.org/Vol-3637/paper11.pdf | Magalie Weber, Patrice Buche, Liliana Ibanescu, Stephane Dervaux, 2023, "PO2/TransformON: A New Domain Ontology for Integrating Food, Feed, Bio-products and Waste in a Circular and Sustainable Approach", IFOW 2023 (JOWO … | repository PDF (CEUR), read in full. |
| Y104 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6550238/fullTextXML | Damion M. Dooley, Emma J. Griffiths, Gurinder S. Gosal, Pier L. Buttigieg, Robert Hoehndorf, Matthew C. Lange, Lynn M. Schriml, Fiona S. L. Brinkman, William W. L. Hsiao, 2018, "FoodOn: a harmonized food ontology to incr… | Europe PMC full-text XML; read in parts (sections on food products, product relations, analogs, counts), not cover to cover. |
| Y105 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8837940/fullTextXML | Agnieszka Lawrynowicz, Anna Wroblewska, Weronika T. Adrian, Bartosz Kulczynski, Anna Gramza-Michalowska, 2022, "Food Recipe Ingredient Substitution Ontology Design Pattern", Sensors 22(3): 1095. DOI 10.3390/s22031095. PM… | Europe PMC full-text XML, read in full. |
| Y106 | https://www.semantic-web-journal.net/system/files/swj3534.pdf | Charalampos Chelmis, Bedirhan Gergin, "A Knowledge Graph for Semantic-Driven Healthiness Evaluation of Online Recipes" (RecipeKG), Semantic Web journal submission 3534, header "Semantic Web 0 (2022)"; final publication s… | submitted manuscript PDF from the journal site; read in parts (abstract, related work, sec. 3.3 on RDF representation). |
| Y107 | https://schema.org/Recipe | schema.org, "Recipe" type definition. Read 2026-11-25; version not recorded. | standard web page (via fetch digest). HowToStep and HowToSection pages were not read. |
| Y108 | http://ceur-ws.org/Vol-2195/research_paper_1.pdf | Cogan Shimizu, Leah McEwen, Quinn Hirt, 2018, "Towards a Pattern-Based Ontology for Chemical Laboratory Procedures", WOP@ISWC 2018, CEUR Vol-2195, pp. 40-51 (authors and pages as cited in Y100; author names also on the P… | repository PDF (CEUR), read in parts (sec. 2 pattern axioms, worked example, conclusion). |
| Y109 | https://www.semantic-web-journal.net/system/files/swj1303.pdf | Charles Vardeman II, Adila Krisnadhi, Michelle Cheatham, Krzysztof Janowicz, Holly Ferguson, Pascal Hitzler, Aimee P. C. Buccellato, 2017, "An Ontology Design Pattern and Its Use Case for Modeling Material Transformation… | accepted manuscript PDF from the journal site; read in parts (sec. 1-3 including the cake example; sec. 4 skimmed). |
| Y110 | https://arxiv.org/html/2509.04159v1 | Aarush Kumbhakern, Saransh Kumar Gupta, Lipika Dey, Partha Pratim Das, 2025, "Towards an Action-Centric Ontology for Cooking Procedures Using Temporal Graphs", arXiv:2509.04159v1. Venue: none listed. | arXiv HTML v1 (via fetch digest). |
| Y111 | https://iieta.org/download/file/fid/27490 (landing page https://iieta.org/node/5083) | Sylvie Despres, "Construction d'une ontologie modulaire. Application au domaine de la cuisine numerique", Revue d'Intelligence Artificielle (RIA) 30, pp. 509-532, DOI 10.3166/RIA.30.509-532. Year not verified (volume 30)… | publisher PDF (IIETA repository), in French; read in parts (abstract, sec. 2 knowledge models, sec. 3 modules and OWL profile). |
| Y112 | http://www.ontobee.org/browser/rdf.php?o=IAO&iri=http://purl.obolibrary.org/obo/IAO_0000005 | Information Artifact Ontology, term IAO_0000005 "objective specification" (Ontobee record, imported from OBI). | ontology term record (via fetch digest). |
| Y113 | https://arxiv.org/html/2306.09042v1 | Antonis Bikakis, Aissatou Diallo, Luke Dickens, Anthony Hunter, Rob Miller, 2023, "A Graphical Formalism for Commonsense Reasoning with Recipes", arXiv:2306.09042v1 (10 pp., no venue listed). Found as a forward citation … | arXiv HTML v1 (via fetch digest); abstract page also read. |
| Y114 | https://foodkg.github.io/ (also /foodkg.html and /subs.html) | FoodKG project documentation (Rensselaer). The ISWC 2019 paper (Haussmann et al., DOI 10.1007/978-3-030-30796-7_10) was not read. | implementation documentation pages (via fetch digest). |
| Y115 | https://pfia23.icube.unistra.fr/conferences/ic/presentations/session2/IC_2023_Ibanescu.pdf | Liliana Ibanescu (presenter), "Besoins ontologiques pour la transformation des aliments", slides, IC 2023 (Journees francophones d'Ingenierie des Connaissances, PFIA 2023). French presentation of Y100. | slide PDF, read in full (little text). |
| Y116 | https://ceur-ws.org/Vol-4176/ifow-1.pdf | Magalie Weber, Florian Duclos, Herve Guillemin, Stephane Dervaux, Julien Cufi, Michel Visalli, 2025, ConsomON (consumer food-choice ontology), JOWO 2025 / IFOW, CEUR Vol-4176 (title line not extracted; the abstract names… | repository PDF, read in part (abstract, sec. 1-2). |
| Y117 | https://arxiv.org/abs/2509.23776 | Ebrahim Norouzi, Sven Hertling, Jorg Waitelonis, Harald Sack, 2025, "Semantic Representation of Processes with Ontology Design Patterns", arXiv:2509.23776v1 (SeMatS@ISWC per Semantic Scholar; not verified). | abstract only. |

## FOON and robotics (`evidence-foon-robotics.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y201 | https://arxiv.org/pdf/1902.01537 (record: https://digitalcommons.usf.edu/esb_facpub/81/) | D. Paulius, Y. Huang, R. Milton, W. D. Buchanan, J. Sam, Y. Sun, 2016, "Functional Object-Oriented Network for Manipulation Learning", IEEE/RSJ IROS 2016, pp. 2655-2662, DOI 10.1109/IROS.2016.7759413 (venue, pages and DO… | arXiv v4 (28 Nov 2020), full text. The USF record has no PDF. |
| Y202 | https://arxiv.org/pdf/1807.02189v2 | D. Paulius, A. B. Jelodar, Y. Sun, 2018, "Functional Object-Oriented Network: Construction & Expansion", IEEE ICRA 2018, pp. 5935-5941 (venue and pages as cited in Y206 and Y204); DOI not verified. | arXiv v2 (31 Jul 2020), full text. |
| Y203 | https://arxiv.org/pdf/1905.00502v4.pdf | D. Paulius, K. S. P. Dong, Y. Sun, 2021, "Task Planning with a Weighted Functional Object-Oriented Network", IEEE ICRA 2021 (as cited in Y204, Y206); DOI 10.1109/ICRA48506.2021.9561680 per a Crossref search result, not o… | arXiv v4 (25 Mar 2021), read in part (abstract, weight and path-tree sections, searched in the extracted text). |
| Y204 | https://arxiv.org/pdf/2106.00158 | D. Paulius, A. Agostini, Y. Sun, D. Lee, 2021, "A Road-map to Robot Task Execution with the Functional Object-Oriented Network", arXiv 2106.00158 (Y205 and Y206 say featured at UR 2021; not verified). | arXiv v1, full text. |
| Y205 | https://arxiv.org/pdf/2106.00728 | M. S. Sakib, H. Baez, D. Paulius, Y. Sun, 2021, "Evaluating Recipes Generated from Functional Object-Oriented Network", arXiv 2106.00728 (featured at UR 2021 per Y206; not verified). | arXiv v1, full text. |
| Y206 | https://arxiv.org/pdf/2207.03693 | M. S. Sakib, D. Paulius, Y. Sun, 2022, "Approximate Task Tree Retrieval in a Knowledge Network for Robotic Cooking", IEEE Robotics and Automation Letters (preprint header: accepted June 2022); arXiv DOI 10.48550/arXiv.22… | arXiv v1, full text. |
| Y207 | https://arxiv.org/abs/2112.02433 | M. S. Sakib, D. Paulius, Y. Sun, 2021, "Functional Task Tree Generation from a Knowledge Graph to Solve Unseen Problems", arXiv. | abstract only (earlier form of Y206). |
| Y208 | https://arxiv.org/pdf/2207.05800v4.pdf | D. Paulius, A. Agostini, D. Lee, 2022/2023, "Long-Horizon Task Planning and Execution with Functional Object-Oriented Networks", arXiv v4 26 Jan 2023; Semantic Scholar lists IEEE RA-L 2022 (not verified). | arXiv v4, full text (extracted). |
| Y209 | https://arxiv.org/pdf/2309.09181 | M. S. Sakib, Y. Sun, 2023, "From Cooking Recipes to Robot Task Trees - Improving Planning Correctness and Task Efficiency by Leveraging LLMs with a Knowledge Network", arXiv 2309.09181 v1; Semantic Scholar lists ICRA (no… | arXiv v1, full text (extracted). |
| Y210 | https://arxiv.org/pdf/2401.07868v1.pdf | M. S. Sakib, Y. Sun, 2024, "Consolidating Trees of Robotic Plans Generated Using Large Language Models to Improve Reliability", arXiv v1; header names International Journal of Artificial Intelligence and Robotics Researc… | arXiv v1, read in part (method and results sections searched in the extracted text). |
| Y211 | https://arxiv.org/html/2409.12262v3 | D. Paulius, A. Agostini, B. Quartey, G. Konidaris, "Bootstrapping Object-level Planning with Large Language Models", arXiv v3 (Mar 2025); Semantic Scholar lists ICRA 2024 (not verified). | arXiv HTML, read via fetch summary. |
| Y212 | https://arxiv.org/html/2503.21564v1 | R. Takebayashi, V. H. Isume, T. Kiyokawa, W. Wan, K. Harada, 2025, "Cooking Task Planning using LLM and Verified by Graph Network", arXiv v1 (Osaka); Semantic Scholar lists IEEE CASE (not verified). | arXiv HTML, read via fetch summary. |
| Y213 | https://github.com/davidpaulius/foon_api and https://raw.githubusercontent.com/davidpaulius/foon_api/master/FOON-111/0039-crispy_hash_browns.txt | D. Paulius, M. S. Sakib, foon_api repository (GPL-3.0), accessed 2026-11-25; folder FOON-111. | README and one subgraph file, via fetch summary. |
| Y214 | https://arxiv.org/abs/1805.06956 | A. B. Jelodar, M. S. Salekin, Y. Sun, 2018, "Identifying Object States in Cooking-Related Images", arXiv (v3 Oct 2018). | abstract only. |
| Y215 | https://ar5iv.labs.arxiv.org/html/1807.02192 | D. Paulius, Y. Sun, 2019, "A Survey of Knowledge Representation in Service Robotics", Robotics and Autonomous Systems 118:13-30 (as cited in Y204, Y205). | ar5iv HTML, first 100k of 131k characters, via fetch summary. |
| Y216 | https://ai.uni-bremen.de/papers/beetz18knowrob.pdf | M. Beetz, D. Bessler, A. Haidu, M. Pomarlan, A. K. Bozcuoglu, G. Bartels, 2018, "KnowRob 2.0 - A 2nd Generation Knowledge Processing Framework for Cognition-enabled Robotic Agents", IEEE ICRA 2018, pp. 512-519, DOI 10.11… | university repository PDF, read in part (introduction to inner-world simulation, about the first half). |
| Y217 | https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1682031/full | M. Kuempel, M. Scheibl, J.-P. Toeberg, V. Hassouna, P. Cimiano, B. Wrede, M. Beetz, 2025, "Everything robots need to know about cooking actions: creating actionable knowledge graphs to support robotic meal preparation", … | publisher full text HTML (open access), via fetch summary (first 100k of 102.5k characters). |
| Y218 | https://arxiv.org/html/2410.02874v2 | N. Kanazawa, K. Kawaharazuka, Y. Obinata, K. Okada, M. Inaba, 2024, "Real-World Cooking Robot System from Recipes Based on Food State Recognition Using Foundation Models and PDDL", arXiv v2; journal (Advanced Robotics pe… | arXiv HTML, read via fetch summary. |
| Y219 | https://www.anlp.jp/proceedings/annual_meeting/2024/pdf_dir/E1-3.pdf | Kanazawa et al. (JSK, University of Tokyo), NLP2024 (30th annual meeting of the Association for Natural Language Processing, Japan), March 2024, pp. 127-; Japanese title concerns a real-world cooking robot from recipe te… | PDF obtained; body text did not decode (CID fonts). Treated as abstract only; the English Y218 was read instead. |

## CBR and workflows (`evidence-cbr-workflows.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y300 | https://ceur-ws.org/Vol-1520/paper23.pdf | Müller, G., Bergmann, R. (2015). CookingCAKE: A Framework for the adaptation of cooking recipes represented as workflows. In: Kendall-Morwick, J. (ed.), Workshop Proceedings of ICCBR 2015 (Computer Cooking Contest), Fran… | CEUR-WS PDF, full text, 12 pages. The ResearchGate copy named in the task returned 403; the CEUR copy replaced it. |
| Y301 | https://www.wi2.uni-trier.de/shared/publications/2014_MuellerBergmannCCC.pdf | Müller, G., Bergmann, R. (2014). Compositional Adaptation of Cooking Recipes using Workflow Streams. Computer Cooking Contest, ICCBR 2014 workshop. Venue as listed on Y313; no page numbers or DOI verified. | repository PDF, full text, 8 pages. |
| Y302 | https://www.wi2.uni-trier.de/shared/publications/2014_MuellerBergmannICCBR.pdf | Müller, G., Bergmann, R. (2014). Workflow Streams: A Means for Compositional Adaptation in Process-Oriented CBR. In: Lamontagne, L., Plaza, E. (eds.), ICCBR 2014, Cork. LNCS 8765, pp. 315-329, Springer. Volume and pages … | repository PDF, full text, 15 pages. |
| Y303 | http://www.wi2.uni-trier.de/publications/2015_MuellerBergmannFLAIRS.pdf | Müller, G., Bergmann, R. (2015). Generalization of Workflows in Process-Oriented Case-Based Reasoning. 28th International FLAIRS Conference, Hollywood (Florida), AAAI Press, pp. 391-396. Pages come from Y306's reference … | repository "technical report" version of the accepted paper, full text, 14 pages. |
| Y304 | https://ceur-ws.org/Vol-1815/paper29.pdf | Müller, G. (2016). Workflow Modelling Assistance by Means of Process-oriented Case-based Reasoning. Proceedings of the ICCBR 2016 Workshops, Atlanta, pp. 272-276. CEUR volume number taken from the URL. DOI: none. | CEUR-WS PDF, full text, 5 pages. |
| Y305 | http://www.wi2.uni-trier.de/publications/2010_MinorEtalICCBR.pdf | Minor, M., Bergmann, R., Görg, S., Walter, K. (2010). Towards Case-Based Adaptation of Workflows. ICCBR 2010, LNAI 6176, pp. 421-435, Springer. Volume and pages confirmed by Y300 and Y306. DOI not verified. | repository PDF, full text, 15 pages. |
| Y306 | https://www.wi2.uni-trier.de/shared/publications/2024_ICCBR_RuleBasedAdaptation_MalburgEtAl.pdf | Malburg, L., Hotz, M., Bergmann, R. (2024). Improving Complex Adaptations in Process-Oriented Case-Based Reasoning by Applying Rule-Based Adaptation. ICCBR 2024, LNCS 14775, pp. 50-66, Springer. DOI 10.1007/978-3-031-636… | repository PDF (author version), full text, 17 pages. |
| Y307 | https://ijcai.org/proceedings/2018/762.md | Zeyen, C., Müller, G., Bergmann, R. (2018). A Conversational Approach to Process-oriented Case-based Reasoning. IJCAI 2018, pp. 5404-5408. DOI not verified. | the publisher's Markdown full text, read through the fetch tool's summariser. It was not quoted. |
| Y308 | http://www.wi2.uni-trier.de/publications/2012_WWW_SchumacherEtal.pdf | Schumacher, P., Minor, M., Walter, K., Bergmann, R. (2012). Extraction of Procedural Knowledge from the Web: A comparison of two workflow extraction approaches. WWW'12 Workshop, Lyon. Pages and DOI not verified. | repository PDF, full text, 7 pages. |
| Y309 | https://www.ijcai.org/Proceedings/13/Papers/445.pdf | Dufour-Lussier, V., Le Ber, F., Lieber, J., Martin, L. (2013). Case Adaptation with Qualitative Algebras. IJCAI 2013, pp. 3002-3006. This is an extended abstract of the ICCBR 2012 best paper, "Adapting spatial and tempor… | publisher PDF, full text, 5 pages. |
| Y310 | https://arxiv.org/pdf/1304.3879.pdf | Dufour-Lussier, V., Le Ber, F., Lieber, J., Nauer, E. (2013). Automatic Case Acquisition From Texts for Process-Oriented Case-Based Reasoning. arXiv:1304.3879v1, a preprint submitted to Information Systems. Final publica… | arXiv v1, sections 1-5 read, 27 pages. Section 6 was skimmed. |
| Y311 | https://iieta.org/download/file/fid/5259 | Gaillard, E., Lieber, J., Nauer, E. (2017). TAAABLE : un système de raisonnement à partir de cas qui adapte des recettes de cuisine. Revue d'intelligence artificielle 31(1-2), 207-235. DOI 10.3166/RIA.31.207-235. In Fren… | publisher PDF (IIETA). Sections 1-4, 5.1-5.3 and 6-7 read, 30 pages. |
| Y312 | https://www-live.dfki.de/fileadmin/user_upload/import/5324_cookiis2010.pdf | Newo, R., Bach, K., Hanft, A., Althoff, K.-D. (2010). On-Demand Recipe Processing based on CBR. CookIIS entry, Computer Cooking Contest 2010, University of Hildesheim. Venue and pages not verified; the text calls itself … | DFKI PDF, full text, 10 pages. |
| Y313 | https://procake.uni-trier.de/publications/ | ProCAKE publication list, University of Trier. Read in two parts, about 51 entries from 2005 to 2026. | web page. |

## Substitution (`evidence-substitution.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y401 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8837940/ | Ławrynowicz A., Wróblewska A., Adrian W. T., Kulczyński B., Gramza-Michałowska A. (2022). Food Recipe Ingredient Substitution Ontology Design Pattern. *Sensors* 22(3):1095. DOI 10.3390/s22031095. | PMC full text. |
| Y402 | https://discovery.ucl.ac.uk/id/eprint/10220617/1/dke-substitution-logic.pdf | Bikakis A., Diallo A., Dickens L., Hunter A., Miller R. (2026). A commonsense reasoning framework for substitution in cooking. *Data & Knowledge Engineering* 163:102558. DOI 10.1016/j.datak.2026.102558 (received 2024-02-… | repository PDF of the published article (39 pp.), full text. |
| Y403 | https://arxiv.org/pdf/2306.09042 (abstract page https://arxiv.org/abs/2306.09042) | Bikakis A., Diallo A., Dickens L., Hunter A., Miller R. (2023). A Graphical Formalism for Commonsense Reasoning with Recipes. arXiv 2306.09042 v1 (no venue listed). | arXiv v1 PDF, full text. |
| Y404 | https://discovery.ucl.ac.uk/id/eprint/10211668/1/Hunter_18606_pub.pdf (landing page https://jair.org/index.php/jair/article/view/18606) | Bikakis A., D'Asaro F. A., Diallo A., Dickens L., Hunter A., Miller R. (2025). A Graphical Formalism for Reasoning about Substitution in Resource Transforming Procedures. *Journal of Artificial Intelligence Research* 84,… | repository PDF of the published article (45 pp.), full text skimmed by section, §5.1 and §10 read closely. (The JAIR PDF link itself returned no text.) |
| Y405 | https://pubdb.vislab.is.i.nagoya-u.ac.jp/~murase/pdf/376-pdf.pdf | Shidochi Y., Takahashi T., Ide I., Murase H. (2009). Finding Replaceable Materials in Cooking Recipe Texts Considering Characteristic Cooking Actions. Proc. ACM Multimedia 2009 Workshop on Multimedia for Cooking and Eati… | author PDF (Nagoya University), full text. Japanese-language versions (JSAI 2008; a journal article "Finding Replaceable Materials by Cooking Recipe Mining") we… |
| Y406 | https://arxiv.org/pdf/1111.3919v3 (abstract https://arxiv.org/abs/1111.3919) | Teng C.-Y., Lin Y.-R., Adamic L. A. (2012). Recipe recommendation using ingredient networks. Proc. 4th ACM Web Science Conference (WebSci '12), pp. 298-307 (venue and pages from arXiv record and Y402's references). | arXiv v3 PDF, full text. |
| Y407 | https://arxiv.org/pdf/1607.08807 (abstract https://arxiv.org/abs/1607.08807) | Achananuparp P., Weber I. (2016). Extracting Food Substitutes From Food Diary via Distributional Similarity. arXiv 1607.08807 v1; "to appear at HealthRecSys'16" (venue publication not verified). | arXiv v1 PDF, full text. |
| Y408 | https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2020.621766/pdf | Shirai S. S., Seneviratne O., Gordon M. E., Chen C.-H., McGuinness D. L. (2021). Identifying Ingredient Substitutions Using a Knowledge Graph of Food. *Frontiers in Artificial Intelligence* 3:621766. DOI 10.3389/frai.202… | publisher PDF, full text (PMC copy blocked by a browser check). |
| Y409 | https://www.scitepress.org/Papers/2021/102020/102020.pdf | Pellegrini C., Özsoy E., Wintergerst M., Groh G. (2021). Exploiting Food Embeddings for Ingredient Substitution. Proc. 14th Int. Joint Conf. on Biomedical Engineering Systems and Technologies (BIOSTEC 2021), Vol. 5: HEAL… | publisher PDF, full text. |
| Y410 | https://arxiv.org/pdf/2302.07960 (abstract https://arxiv.org/abs/2302.07960) | Fatemi B., Duval Q., Girdhar R., Drozdzal M., Romero-Soriano A. (2023). Learning to Substitute Ingredients in Recipes. arXiv 2302.07960 v1 (no peer-reviewed venue listed). | arXiv v1 PDF, full text. |
| Y411 | https://ceur-ws.org/Vol-4196/paper_20.pdf | Loesch J., Schimmel D., Erdem F., Kalkavan D., Bilgin Z., Celebi R. (2025). Enhancing GISMo: Integrating Recipe Contexts into a Graph-Based Ingredient Substitution Module. SWAT4HCLS 2025, CEUR Workshop Proceedings Vol. 4… | CEUR PDF, full text. |
| Y412 | https://arxiv.org/pdf/2105.08185v2 (abstract https://arxiv.org/abs/2105.08185) | Li S., Li Y., Ni J., McAuley J. (2022). SHARE: a System for Hierarchical Assistive Recipe Editing. EMNLP 2022 (per arXiv record); arXiv 2105.08185 v2. | arXiv v2 PDF, full text skimmed, evaluation and limitations read closely. |
| Y413 | https://arxiv.org/pdf/0912.0132 (abstract https://arxiv.org/abs/0912.0132) | Badra F., Cordier A., Lieber J. (2009). Opportunistic Adaptation Knowledge Discovery. ICCBR 2009, Seattle (per arXiv record); arXiv 0912.0132 v1. | arXiv v1 PDF, full text. |
| Y414 | https://arxiv.org/pdf/2501.01958 (abstract https://arxiv.org/abs/2501.01958) | Kim H., Venkataramanan R., Sheth A. (2024). A Survey on Food Ingredient Substitutions. arXiv 2501.01958 v1 (submitted 2024-10-25). | arXiv v1 PDF, full text skimmed by section. |
| Y420 | https://arxiv.org/abs/2412.04922 (abstract only) | Senath T., Athukorala K., Costa R., Ranathunga S., Kaur R. (2024). Large Language Models for Ingredient Substitution in Food Recipes using Supervised Fine-tuning and Direct Preference Optimization. arXiv 2412.04922 v1. | abstract only. |

## Recipe graphs (`evidence-recipe-graphs.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y500 | https://aclanthology.org/2020.lrec-1.638.pdf (landing page https://aclanthology.org/2020.lrec-1.638/) | Yoko Yamakata, Shinsuke Mori, John Carroll, 2020, "English Recipe Flow Graph Corpus", Proceedings of LREC 2020, Marseille, pp. 5187-5194, ELRA. DOI: none listed on the Anthology page. | repository PDF (ACL Anthology), read in full (8 pages). |
| Y501 | https://aclanthology.org/L14-1594.pdf (landing page https://aclanthology.org/L14-1594/) | Shinsuke Mori, Hirokuni Maeta, Yoko Yamakata, Tetsuro Sasada, 2014, "Flow Graph Corpus from Recipe Texts", Proceedings of LREC 2014, Reykjavik, pp. 2370-2377, ELRA. DOI: none listed. | repository PDF (ACL Anthology), read in full (8 pages). |
| Y502 | https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1550604/full | Filippos Ventirozos, Mauricio Jacobo-Romero, Haifa Alrdahi, Sarah Clinch, Riza Batista-Navarro, "RiCoRecA: rich cooking recipe annotation schema", Frontiers in Artificial Intelligence vol. 8 (2025), published 12 January … | publisher HTML full text (via fetch digest), two passes (body; then reference list). Some body details may be lost in the digest. |
| Y503 | https://aclanthology.org/2021.emnlp-main.554.pdf (landing page https://aclanthology.org/2021.emnlp-main.554) | Lucia Donatelli, Theresa Schmidt, Debanjali Biswas, Arne Köhn, Fangzhou Zhai, Alexander Koller, 2021, "Aligning Actions Across Recipe Graphs", Proceedings of EMNLP 2021, pp. 6930-6942. DOI 10.18653/v1/2021.emnlp-main.554… | repository PDF, read in full (13 pages incl. appendix). |
| Y504 | https://aclanthology.org/D15-1114.pdf (landing page https://aclanthology.org/D15-1114/) | Chloé Kiddon, Ganesa Thandavam Ponnuraj, Luke Zettlemoyer, Yejin Choi, 2015, "Mise en Place: Unsupervised Interpretation of Instructional Recipes", Proceedings of EMNLP 2015, Lisbon, pp. 982-992. DOI 10.18653/v1/D15-1114… | repository PDF, read in full. |
| Y505 | https://aclanthology.org/D15-1090.pdf (landing page https://aclanthology.org/D15-1090/) | Jermsak Jermsurawong, Nizar Habash, 2015, "Predicting the Structure of Cooking Recipes", Proceedings of EMNLP 2015, Lisbon, pp. 781-786. DOI 10.18653/v1/D15-1090. | repository PDF, read in full. |
| Y506 | https://ar5iv.labs.arxiv.org/html/2005.09606 (abstract page https://arxiv.org/abs/2005.09606 also read) | Angela Lin, Sudha Rao, Asli Celikyilmaz, Elnaz Nouri, Chris Brockett, Debadeepta Dey, Bill Dolan, 2020, "A Recipe for Creating Multimodal Aligned Datasets for Sequential Tasks", Proceedings of ACL 2020, pp. 4871-4884. DO… | HTML full text via ar5iv (via fetch digest); arXiv abstract page shows v1 (19 May 2020). Which arXiv version ar5iv rendered: not verified. |
| Y507 | https://arxiv.org/html/2507.17232v2 | Mashiro Toyooka, Kiyoharu Aizawa, Yoko Yamakata, 2025, "A Highly Clean Recipe Dataset with Ingredient States Annotation for State Probing Task", arXiv:2507.17232v2 (28 Aug 2025). Venue: not verified (template text on the… | arXiv HTML v2 (via fetch digest). |
| Y508 | https://ar5iv.labs.arxiv.org/html/2209.05840 (Anthology entry https://aclanthology.org/2022.coling-1.315 seen in search only) | Keisuke Shirai, Atsushi Hashimoto, Taichi Nishimura, Hirotaka Kameko, Shuhei Kurita, Yoshitaka Ushiku, Shinsuke Mori, 2022, "Visual Recipe Flow: A Dataset for Learning Visual State Changes of Objects with Recipe Flows", … | HTML full text via ar5iv (via fetch digest). |
| Y509 | https://www.jstage.jst.go.jp/article/tjsai/32/1/32_WII-F/_article/-char/en | Yoko Yamakata, Hirokuni Maeta, Takuya Kadowaki, Tetsuro Sasada, Shinji Imahori, Shinsuke Mori, 2017, "Cooking Recipe Search by Pairs of Ingredient and Action — Word Sequence v.s. Flow-graph Representation", Transactions … | abstract only (J-STAGE English abstract). |
| Y510 | https://aclanthology.org/2023.findings-acl.261/ | Yi Fan, Anthony Hunter, 2023, "Understanding the Cooking Process with English Recipe Text", Findings of ACL 2023, pp. 4244-4264. DOI 10.18653/v1/2023.findings-acl.261. | abstract only (Anthology page). |
| Y511 | https://arxiv.org/abs/2406.15823 | Yash Kumar Lal, Vanya Cohen, Nathanael Chambers, Niranjan Balasubramanian, Raymond Mooney, "CaT-Bench: Benchmarking Language Model Understanding of Causal and Temporal Dependencies in Plans", EMNLP 2024 (accepted per arX… | abstract only. |
| Y512 | https://arxiv.org/abs/2210.11431 | Xiao Liu, Yansong Feng, Jizhi Tang, Chengang Hu, Dongyan Zhao, 2022, "Counterfactual Recipe Generation: Exploring Compositional Generalization in a Realistic Scenario", EMNLP 2022 (per arXiv page), arXiv:2210.11431v1. | abstract only. |
| Y513 | https://arxiv.org/abs/1711.05313 | Antoine Bosselut, Omer Levy, Ari Holtzman, Corin Ennis, Dieter Fox, Yejin Choi, "Simulating Action Dynamics with Neural Process Networks", arXiv:1711.05313v2 (15 May 2018). Venue: not shown on the page; not verified. | abstract only. |
| Y514 | https://arxiv.org/abs/2205.12420 | Te-Lin Wu, Caiqi Zhang, Qingyuan Hu, Alex Spangher, Nanyun Peng, "Learning Action Conditions from Instructional Manuals for Instruction Understanding", arXiv:2205.12420v2 (3 Jul 2024). Venue: not verified. | abstract only. |
| Y515 | https://www.cs.cmu.edu/~ark/CURD | CURD 1.0 (Carnegie Mellon University Recipe Database), 260 English recipes annotated in MILK, released 2 June 2008; cite as Dan Tasse, Noah A. Smith, "SOUR CREAM: Toward Semantic Processing of Recipes", Technical Report … | dataset landing page only. The technical report was not read; MILK's command set is known here only through Y505's description (MILK has create_tool, combine, p… |
| Y516 | https://arxiv.org/abs/2608.24369 | Lei Jiang, "Do Recipes Have Personas? Characterizing and Generating Creator Style in Attributed Procedural Graphs", arXiv:2608.24369v1 (25 Aug 2026), stated accepted at Discovery Science 2026. | abstract only. |

## Industrial process (`evidence-industrial-process.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y600 | https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards | ISA (International Society of Automation), "ISA-88 Standards" catalogue page, n.d. (accessed 2026-11-25). | publisher web page (catalogue only). |
| Y601 | https://en.wikipedia.org/wiki/ISA-88 | Wikipedia contributors, "ISA-88", n.d. (accessed 2026-11-25). | web page. |
| Y602 | https://lup.lub.lu.se/search/files/4689442/8840032.pdf | Johnsson, Charlotta, 1999, *A Graphical Language for Batch Control*, doctoral thesis (monograph), Department of Automatic Control, Lund Institute of Technology, Lund University. ISRN LUTFD2/TFRT-1051-SE, ISSN 0280-5316. … | repository PDF (Lund University Publications, "publisher's PDF, version of record"). Read: contents; ch. 3.1 (Grafcet steps, transitions, receptivities, pp. 33-… |
| Y603 | https://cdn.standards.iteh.ai/samples/13990/b459f27e02f74751b01fb3998f41d3d0/IEC-PAS-61512-3-2004.pdf | IEC/PAS 61512-3:2004, *Batch control - Part 3: General and site recipe models and representation*, first edition 2004-11; text identical in this preview to ANSI/ISA-88.00.03-2003. Publisher IEC (copyright ISA 2003, IEC 2… | publisher's free preview (iTeh Standards), 14 pages: table of contents, introduction, clauses 1 (scope), 3 (definitions), 4.1-4.3.3. The normative clauses 5-8 (… |
| Y604 | https://cdn.standards.iteh.ai/samples/16242/38071704ea2d42d3bce8183bd2310574/IEC-PAS-61512-4-2007.pdf | IEC/PAS 61512-4:2007, *Batch control - Part 4: Batch production records*. Superseded by IEC 61512-4:2009 (not read). | publisher's free preview (iTeh Standards): scope, normative references, definitions 3.1-3.5, clause 4.2 (pp. 8-12). |
| Y605 | https://lin.engin.umich.edu/wp-content/uploads/sites/551/2021/10/Mixed-Integer-Linear-Programming-in-Process-Scheduling.pdf | Floudas, Christodoulos A.; Lin, Xiaoxia, 2005, "Mixed Integer Linear Programming in Process Scheduling: Modeling, Algorithms, and Applications", *Annals of Operations Research* 139, 131-162. DOI not verified (not printed… | repository PDF (author's group site), publisher layout. Read: abstract, sec. 1.1 (problem components, process representation, Figs. 1-2), the storage-policy par… |
| Y606 | https://jckantor.github.io/ND-Pyomo-Cookbook/notebooks/04.05-Scheduling-Multipurpose-Batch-Processes-using-State-Task_Networks.html | Kantor, Jeffrey C., n.d., "Scheduling Multipurpose Batch Processes using State-Task Networks", *ND Pyomo Cookbook* (Jupyter notebook). | web page (full). |
| Y607 | https://zenodo.org/records/3987973/files/On%20the%20Optimization%20of%20Production%20Scheduling%20in%20Industrial%20Food%20Processing%20Facilities.pdf | Georgiadis, Georgios P.; Ziogou, Chrysovalantou; Kopanos, Georgios; Mariño Pampín, Borja; Cabo, Daniel; Lopez, Miguel; Georgiadis, Michael C., 2019, "On the Optimization of Production Scheduling in Industrial Food Proces… | repository PDF (Zenodo), publisher layout, full (6 pp.). |
| Y608 | https://docs.oracle.com/cd/E18727_01/doc.121/e13091/T320995T321003.htm | Oracle, *Oracle Process Manufacturing Product Development User's Guide*, chapter "Recipes". Release not verified (path suggests 12.1). | vendor documentation web page; the first 100,000 of 126,838 characters. |
| Y609 | https://www.iaorifors.com/paper/31320 (abstract only) | Houba, Iris H. G.; Hartog, Rob J. M.; Top, Jan L.; Beulens, Adrie J. M.; van Berkel, Linda N., 2000, "Using recipe classes for supporting detailed planning in food industry: A case study", *European Journal of Operationa… | abstract only (IAOR paraphrase; ScienceDirect 403). |
| Y610 | https://research.tue.nl/en/publications/evaluation-of-three-production-planning-procedures-for-the-use-of/ (abstract only) | Bertrand, J. W. M.; Rutten, W. G. M. M., 1999, "Evaluation of three production planning procedures for the use of recipe flexibility", *European Journal of Operational Research* 115(1), 179-194. DOI 10.1016/S0377-2217(98… | abstract only (TU/e portal). |
| Y611 | https://wbmoodle.hswt.de/mod/resource/view.php?id=167518 | FAO and WHO, 2023, *General Principles of Food Hygiene*, Codex Alimentarius Code of Practice CXC 1-1969 (adopted 1969, amended 1999, revised 1997, 2003, 2020, 2022), Rome. DOI 10.4060/cc6125en (printed in the document). | publisher PDF (FAO/WHO 2023 printing) served from a university course mirror (Hochschule Weihenstephan-Triesdorf Moodle), because FAO's repository returned 403.… |
| Y612 | https://www.fda.gov/media/71976/download | U.S. Food and Drug Administration, 2006 (April), *Managing Food Safety: A Manual for the Voluntary Use of HACCP Principles for Operators of Food Service and Retail Establishments*. Landing page: https://www.fda.gov/food/… | publisher PDF (86 pp.); read ch. 2 (pp. 13-20) and the glossary entries for danger zone and process approach. |
| Y613 | https://www.ruokavirasto.fi/globalassets/tietoa-meista/asiointi/oppaat-ja-lomakkeet/yritykset/elintarvikeala/elintarvikehuoneistot/omavalvonta-fin-2-jaahdytys.pdf | Ruokavirasto (Finnish Food Authority), 2021, "Näin huolehdit omavalvonnasta ravintolassa: Jäähdytys" (How to do self-monitoring in a restaurant: Cooling), leaflet, PDF metadata dated 2021-04-22. Produced in a project fun… | publisher PDF, full (one page, Finnish). |
| Y614 | https://ceur-ws.org/Vol-3998/paper02.pdf | Wellershaus, Finn (as printed; e-mail and ORCID give Janne); Köhler-Bußmeier, Michael; Sudeikat, Jan, 2025, "Modelling and Analysis of Self-Adaptive Systems using Petri Nets: A Robot Kitchen Case Study", PNSE'25 Internat… | publisher PDF (CEUR); read abstract, sec. 1-2 and Table 1; sec. 3 (MAPE loop) skimmed by search. |
| Y615 | https://www.scitepress.org/publishedPapers/2024/129430/pdf/index.html | Rennane, Fatma Zohra; Meziane, Abdelkrim, 2024, "Leveraging Ontologies for Handicraft Business Process Modeling: Application for the Pastry-Making Domain", WEBIST 2024, pp. 226-233. DOI 10.5220/0012943000003825. | publisher PDF (SciTePress), via WebFetch reading. |
| Y616 | https://arxiv.org/abs/2101.08886 (abstract only) | Zallio, M.; Kelly, P.; Cryan, B.; Berry, D., 2021, "A co-Design approach to develop a smart cooking appliance. Applying a Domain Specific Language for a community supported appliance", arXiv:2101.08886v3. | abstract only (arXiv abstract page). |

## Visualisation (`evidence-visualisation.md`)

| Id | URL read | Citation | Version read |
| --- | --- | --- | --- |
| Y700 | https://recipescape.kixlab.org/RecipeScape_CHI_2018__Camera_Ready_.pdf | Minsuk Chang, Léonore V. Guillain, Hyeungshik Jung, Vivian M. Hare, Juho Kim, Maneesh Agrawala. 2018. *RecipeScape: An Interactive Tool for Analyzing Cooking Instructions at Scale.* CHI 2018, Montréal. DOI 10.1145/317357… | the authors' camera-ready PDF, linked from the project page https://recipescape.kixlab.org/. The page gives the link as a relative path, resolved against that p… |
| Y701 | https://arxiv.org/pdf/1111.3919v2 | Chun-Yuen Teng, Yu-Ru Lin, Lada A. Adamic. *Recipe recommendation using ingredient networks.* WebSci 2012, pp. 298–307. Publisher DOI not verified (dblp lists the venue); arXiv 1111.3919. | arXiv v2 PDF, full text (extracted locally). |
| Y702 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3240947 | Yong-Yeol Ahn, Sebastian E. Ahnert, James P. Bagrow, Albert-László Barabási. 2011. *Flavor network and the principles of food pairing.* Scientific Reports 1:196. DOI 10.1038/srep00196. | PMC full text (read through the fetch tool's summary of the full page). |
| Y703 | https://etheses.whiterose.ac.uk/id/eprint/5158/1/Lucy%20Buykx%20accepted%20thesis.pdf | Lucy Buykx. 2013. *Interactive recipe instructions: supporting cooks with better designs.* PhD thesis, University of York. Record page: https://etheses.whiterose.ac.uk/id/eprint/5158/. | repository PDF. Read in part: - the abstract and table of contents; - Ch. 6 limitations (§6.4.4); - Ch. 7 study design (§7.1–7.2), the overview screen flow (Fig… |
| Y704 | https://arxiv.org/pdf/2112.04788v2 | Alexander Frummet, David Elsweiler, Bernd Ludwig. *"What can I cook with these ingredients?" – Understanding cooking-related information needs in conversational search.* ACM Transactions on Information Systems (2022). DO… | arXiv v2 PDF. Read in part: abstract, method (§3), taxonomy definitions (Table 2), conversational cues (§4.2), comparison with earlier taxonomies (§6). The clas… |
| Y705 | https://arxiv.org/pdf/1709.00293.pdf (served as v1) | Mershack Okoe, Radu Jianu, Stephen Kobourov. *Revisited Experimental Comparison of Node-Link and Matrix Representations.* arXiv:1709.00293v1, 2017. | arXiv v1, full text (extracted locally). |
| Y706 | https://www.cmu.edu/joss/content/articles/volume5/McGrathBlythe/MBNoJava.html | Cathleen McGrath, Jim Blythe. *Do you see what I want you to see? The effects of motion and spatial layout on viewers' perceptions of graph structure.* Journal of Social Structure. Volume 5 is taken from the URL path; th… | journal HTML (non-Java version), through the fetch tool's summary of the full page. |
| Y707 | https://arxiv.org/pdf/2009.00192v1 | Sehi L'Yi, Jaemin Jo, Jinwook Seo. 2020. *Comparative Layouts Revisited: Design Space, Guidelines, and Future Directions.* arXiv:2009.00192. Listed as IEEE VIS (InfoVis) 2020; the TVCG DOI was not verified. | arXiv v1 PDF. Guidelines (§5.2), limitations and conclusion read in full; §1–4 skimmed. |
| Y708 | https://pure.uva.nl/ws/files/149990210/Examining_the_user_evaluation_of_multi-list_recommender_interfaces.pdf | Alain D. Starke, Edis Asotic, Christoph Trattner, Ellen J. Van Loo. 2023. *Examining the user evaluation of multi-list recommender interfaces in the context of healthy recipe choices.* ACM Transactions on Recommender Sys… | the final published PDF from the University of Amsterdam repository. Read in part: abstract, introduction, Study 1 design and results (§3), Study 2 results (§4.… |
| Y709 | https://ubi-naist.github.io/paper/IPSJ/202006_DICOMO_nakabe_paracook.pdf | 中部 仁, 水本 旭洋, 諏訪 博彦, 安本 慶一 (Jin Nakabe, Teruhiro Mizumoto, Hirohiko Suwa, Keiichi Yasumoto). 2020. 複数レシピで並行調理する際の調理環境に応じた最適調理手順作成法と評価 (*Minimizing cooking time for multiple parallel recipes under arbitrary cooking environ… | the lab's repository PDF, in Japanese. Abstract, introduction, related work and problem formulation (§1–4) read; the evaluation was read through the abstract. |
| Y710 | https://www.ipa.go.jp/archive/files/000005836.pdf | 浜田 玲子 (Reiko Hamada). 平成15年度 (FY2003) 未踏ソフトウェア創造事業 (IPA Mitou programme) report, 家庭におけるマルチメディア調理支援 (*Multimedia cooking support in the home*). | publisher PDF (IPA), one page, read in full. |
| Y711 | https://star.rcast.u-tokyo.ac.jp/old/content/files/pdf/conference/full_paper/17. panavi.pdf | Daisuke Uriu, Mizuki Namai, Satoru Tokuhisa, Ryo Kashiwagi, Masahiko Inami, Naohito Okude. *panavi: Recipe Medium with a Sensors-Embedded Pan for Domestic Users to Master Professional Culinary Arts.* CHI 2012, Austin. DO… | repository PDF (University of Tokyo RCAST). Abstract, related work, design process and user study read; the implementation was skimmed. |
| Y712 | https://arxiv.org/pdf/2108.01427 | Arngeir Berge, Vegard Velle Sjøen, Alain D. Starke, Christoph Trattner. 2021. *Changing Salty Food Preferences with Visual and Textual Explanations in a Search Interface.* Joint Proceedings of the ACM IUI 2021 Workshops … | arXiv PDF, full text (extracted locally). |
