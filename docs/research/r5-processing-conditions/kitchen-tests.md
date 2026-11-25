# R5: the R4 kitchen tests, with completion and failure checks

R4's kitchen tests (`../r4-transfers/kitchen-tests.md`, unchanged) say what to
compare and how to taste. This page adds what R5 documented for each step:
the **done-when** check, the **failed-if** check, and whether each step is
**readiness** or **doneness**. Times are guides, given as the sources give
them; the check decides.

The order is unchanged: gratin first. When a test runs, record the result in
`transfers.yaml` (as R4 says). Also record each member's endpoint where this
page says the evidence stops: the kitchen is the first source there.

`foodprep conditions transfer:<id>` prints the full sequence for each test.

---

## 1. Potato and rutabaga gratin (`transfer:rutabaga_gratin`)

| Step | Kind | Time guide | Done when | Failed if |
| --- | --- | --- | --- | --- |
| Slice potato and rutabaga | readiness | - | 2-3 mm; potato sliced last and **not rinsed** (its starch thickens the cream) (Q231, Q235) | - |
| Blanch the rutabaga only | **readiness** | 3-5 min in salted boiling water, rinse cold, pat dry (Q231, Q232, Q233) | "crisp-tender": a little softer, clearly not cooked (Q231, Q232) | - |
| Layer, cream over | (join) | - | potato on the top and bottom layers (G7, G15) | - |
| Bake | **doneness** | 190 C covered 30 min, then 200 C uncovered 25-30 min (Q231) | a knife meets no resistance in the **potato** (Q234, Q232); top golden and bubbling (Q231, Q232, Q233) | burnt top, raw inside (uncovered too early) (Q201); grainy, watery liquid (milk only, no starch) (Q219) |
| Bake: the rutabaga inside | doneness, per member | - | **decide which version you get**: "some give, al dente" (Q231) or "no resistance" (Q232, Q233, Q234) | **still crunchy when the potato is done**: the R4 stop condition (G20, G21) |
| Rest | finishing | a few minutes to 25 min (Q231, Q234) | the cream has set; a square holds (Q202, Q200) | slumps and weeps (R4's judge) |

- **Why the blanch:** rutabaga is denser and needs longer than potato in the
  same bake (Q231, Q234).
- **Control (c), raw rutabaga:** if it is tender when the potato is done, A2
  and the `skipped` failure in the sequence are wrong for this oven and
  thickness. Record that.
- **Not documented, so judge it here:** what the cream should look like at the
  end (no rutabaga source states it); over-blanched slices breaking up.

## 2. Hollowed onion vessel (`transfer:onion_vessel`), beside courgettes (`zucchine_ripiene/blanched_flesh`)

| Step | Kind | Time guide | Done when | Failed if |
| --- | --- | --- | --- | --- |
| Blanch onion halves | **readiness** | about 10 min in salted boiling water (O5, M16a, Q336) | **still firm, lightly crisp** (Q326, Q335) | **layers tear or fall apart; slippery to handle** (O12, O15, O10) |
| Blanch whole courgettes | **readiness** | 5-10 min (M17b, M17a, Q330) | "only half-cooked", drained while still firm (Q330, M17a) | - |
| Hollow | readiness | - | onion: two or three outer layers, about 1 cm wall (O5, Q327, Q336); courgette: 5-8 mm wall (Q333) | a hole in the onion base (patch it with a leaf) (Q327); courgette wall too thin breaks, too thick stays raw (Q333) |
| Chop and sweat the onion insides | readiness | 3-4 min (Q336) | softened, then cooled (Q336) | - |
| Bake | **doneness** | 180 C, 30 min (O5) to 45-50 min (Q327, Q336) | the **vessel** takes a knife easily and is tender without collapsing (Q336); top gratinated (M16a) | tops brown early: foil (Q327, Q336); **onion still undercooked when the filling is done** (Q325); soggy filling from courgette water (Q333) |

- **Why the blanch:** the vessel and the filling need different times
  (Q334); blanching also makes hollowing easier (Q336).
- **Not documented, so judge it here:** whether the egg in the filling has
  set, and whether it is hot through (no source gives a test).

## 3. Napa-cabbage rolls (`transfer:napa_cabbage_rolls`), beside kaalikaaryleet (`kaalikaaryleet/trimmed_rib`)

| Step | Kind | Time guide | Done when | Failed if |
| --- | --- | --- | --- | --- |
| Cook the rice | **readiness** | per packet, stopped early (Q317); porridge rice 10 min, drained (Q301) | slightly al dente, because it finishes in the oven; then cooled (Q317, Q311) | raw rice: dry filling, split leaves (Q313) |
| Napa leaves off | readiness | - | pulled off raw one at a time, untorn (Q317) | - |
| Blanch napa leaves | **readiness** | 1.5-2 min salted boiling water (Q317), or microwave 3-5 min (N1, N4) | "flexible but not cooked" (Q317); the rib turns translucent (Q318) | **too soft, falls apart when rolled; mushy** (Q317, N12) |
| Shave the rib | readiness | - | shaved flat, shavings into the filling (N3) | tough fibres in the roll if not shaved (N2) |
| White cabbage head | **readiness** | boil cored, peel leaves as they soften (Q300-Q302) | leaves come away easily and bend without falling apart (Q301, Q313) | too soft, tear (Q308); too stiff: dip again (Q313) |
| Bake | **doneness** | Finnish: hot start 225-250 C to colour, then 150-175 C, basted (Q300-Q303); napa elsewhere: 180 C **covered**, broth to cover, about 60 min (Q317) | rolls coloured on top (Q302, Q303); the leaf soft (Q312-Q314) | **dry rolls (too little liquid)** (Q317); **cabbage still hard** (Q313); top browns too fast (Q313) |
| Bake: the filling inside | doneness, per member | - | a pork filling's core reaches at least 71 C (Q313, white-cabbage golabki) | - |

- **The open question stays open:** nobody bakes napa rolls the Finnish way
  (syrup, uncovered). No Finnish source states covering at all. Bake the napa
  dish covered for the first half, as R4 planned. Note whether the edges dry
  or scorch: no source names that failure for napa.

## 4. Pea falafel (`transfer:pea_falafel`), beside chickpea falafel (`falafel/raw_soaked`)

| Step | Kind | Time guide | Done when | Failed if |
| --- | --- | --- | --- | --- |
| Soak | **readiness** | peas: overnight to 12 h, 1:3 water (P3, P4, P15); chickpeas: overnight to 24 h (M2a, M2b, Q111) | chickpeas: about doubled, chop easily with a knife, still firm and mealy (Q109, Q111). **Peas: no documented check; time only** | chickpeas still hard inside (Q111) |
| Never cook them | - | - | swollen, not cooked (Q108) | **cooked or canned pulses: the balls fall apart or turn mushy** (Q108, Q109, Q114, Q115) |
| Grind with onion and herbs | readiness | pulse and scrape | **holds together when squeezed in the hand** (Q109, Q111, Q120); peas: coarse, a mouldable batter (P4, P15) | too smooth: falls apart (Q108); over-processed: wet, hard to handle (Q116); peas ground fine: dense (P4) |
| Rest, chilled | readiness | at least 15 min (P4); 30 min to 2 h (Q113, Q114, Q110) | firmer, shapes easily (Q108, Q114) | skipped: falls apart in the oil (Q114, Q115) |
| Shape | readiness | - | small, firmly packed (Q109, Q113); peas pressed, not rolled (P2) | loose or large: breaks or cooks unevenly (Q108, Q113) |
| Fry | **doneness** | 170-180 C, 2-5 min, batches of 5-6 (P4, Q110, Q111) | golden to deep brown; crisp outside, fluffy and cooked inside (Q108, Q111, Q116); a test ball golden in about 2 min (P4) | greasy (oil too cool); charred outside, raw centre (too hot) (Q113); **dry and hard: yellow pea** (P15) |

- **Before you start:** a 1-ball test fry is documented practice (Q107, P4).
- **Not documented, so judge it here:** whether the pea interior is cooked
  through; any raw-pea taste. Whether frying counts as the treatment that pea
  and chickpea packets ask for (Q102, Q543) is not stated by any authority
  read (`limitations.md`).

## 5. Broccoli-stem patties (`transfer:broccoli_stem_patties`), beside carrot patties (`carrot_patties/crumbs`)

| Step | Kind | Time guide | Done when | Failed if |
| --- | --- | --- | --- | --- |
| Peel the stem | **readiness** | - | **whitish flesh exposed all the way round; the fibrous ring cut away** (Q428, Q424) | unpeeled: tough, fibrous, stringy shreds (Q426, Q427, B1) |
| Grate stem and carrot | readiness | - | coarse, raw, not squeezed (B1, B20, E18a) | large stem pieces: the patty crumbles (B6) |
| Mix and shape | readiness | - | thick, slightly sticky, firm enough to shape with oiled hands (Q431, E18a); thin patties (B1, Q412) | loose mass, hard to turn (Q414) |
| Bake or fry | **doneness** | oven 250 C, 15-20 min (E18a); pan 2-5 min a side (B1, B21, Q431) | turn only when the underside is firm and golden (Q411, M3b); golden on both sides (B1, Q405) | **falls apart when turned too early** (Q411, M3b); greasy (pan too cool); burnt outside, raw inside (too hot) (Q401, M4b) |
| The stem inside | doneness, per member | - | **not documented**: one writer liked it still crisp after 8 min (B7) | **stringy or raw-tasting in a patty that is otherwise done**: the R4 stop condition |

- **Why thin:** so the stem cooks through (B1).
- **Not documented, so judge it here:** the R4 stop condition itself. No
  source checks a grated stem inside a done patty.
