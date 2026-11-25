# R4 step 5: kitchen tests

One short test for each transfer worth cooking. Each compares the transfer
with the documented dish it came from, cooked side by side, and asks three
things: does it hold, is it cooked right, and **is it worth eating**. Taste
decides; a transfer that holds but tastes dull has failed. Each test has a
stop condition: if it is met, record the result in `transfers.yaml` (the
candidate's `evidence_says` and `verdict`, with the date) and stop.

Nothing was cooked in this round. Suggested order, by what is in the shop
now (late November) and what needs checking first:

1. **Potato and rutabaga gratin.** Everything is at Lidl now, and rutabaga is
   in season.
2. **Hollowed onion vessel.** Needs a courgette for the comparison
   (imported, spring offers at Lidl).
3. **Napa-cabbage rolls.** First check whether Lidl has *kiinankaali*.
4. **Pea falafel.** First check whether Lidl has dried split peas (L1);
   otherwise buy them elsewhere and record that.
5. **Broccoli-stem patties.** Whenever a fresh head is bought.

---

## 1. Potato and rutabaga gratin

- **Compare.** Two small dishes in the same oven. (a) All-potato gratin, the
  base. (b) Potato and rutabaga 1:1, **rutabaga only** blanched 4 min. Same
  2-3 mm slices, same cream and milk with garlic, 160-170 C until a knife
  meets no resistance in the potato. Optional (c): as (b) with the rutabaga
  raw, the control the model now rejects.
- **Judge.** At the moment the potato is done, test the rutabaga with a knife.
  After 20-25 min of rest, does a square hold or slump and weep?
- **Taste.** Is the rutabaga sweet and nutty, or sharp and sulphurous next to
  the cream? Would you make (b) instead of (a)? If it tastes flat, try a
  teaspoon of mustard in the cream next time (G7, G10).
- **Stop if** the blanched rutabaga is still firm when the potato is done, or
  the flavour is unpleasant even with mustard.
- **Also tests the model:** if (c) turns out tender, A2's requirement is
  wrong for this thickness and oven, and the control's `evidence_says` must
  change.

## 2. Hollowed onion vessel

- **Compare.** One tray, as in Nice (O5): two onion halves and two courgette
  halves, the same filling (egg, Parmesan, breadcrumbs or soaked bread,
  herbs, and each vegetable's own chopped insides). Onions peeled, halved
  across, blanched 8-10 min, hollowed to two outer layers. 180 C 30 min.
- **Judge.** Do the onion shells stay whole when lifted out of the water and
  out of the tray? Is the onion tender at 30 min?
- **Taste.** Is the onion vessel sweet and soft, or sharp and chewy? Which
  vessel would you make again?
- **Stop if** the layers slip apart in handling, or the onion is still crunchy
  when the filling is done.

## 3. Napa-cabbage rolls

- **Compare.** Kaalikääryleet with white cabbage (the base) and with napa
  leaves, same rice-and-mince filling. Napa: outer leaves peeled off raw,
  blanched 1-2 min or microwaved, the thick rib shaved and minced into the
  filling (N3). Both packed tightly with a little water, **covered for the
  first half** of the bake, syrup over at the end.
- **Judge.** Time to prepare the leaves. Do the napa rolls hold when lifted?
  Are the edges dry or scorched? Can a fork cut through the leaf?
- **Taste.** Is the napa wrapper tender and sweet, or watery and limp next to
  the cabbage? Which would you make on a weeknight?
- **Stop if** the napa leaves turn to mush, or the edges burn even when
  covered. (Nobody bakes napa rolls the Finnish way; this test is the first
  evidence.)

## 4. Pea falafel

- **Compare.** Split-pea falafel against chickpea falafel, same day: same
  onion, parsley, garlic, cumin and a little bicarbonate; both soaked 12-16 h,
  drained well, pulsed **coarse**; pressed into balls; fried in small batches
  at about 175 C. If dried chickpeas are not available either, compare peas
  soaked 12 h with peas soaked 24 h (P15 found soak time drives water uptake).
- **Judge.** Does the pea paste shape and survive the oil? Cut one: cooked
  through; interior moist or crumbly-dry? Crust after 5 minutes.
- **Taste.** Blind, warm, with yogurt or tahini sauce. Which is more pleasant;
  any raw-pea or pea-soup taste; is the pea version dry in the mouth?
- **Stop if** the pea falafel is clearly drier and harder than the chickpea
  batch even with aromatics in it: P15 confirmed in a home kitchen.

## 5. Broccoli-stem patties

- **Compare.** Carrot patties (the base: grated carrot, egg, breadcrumbs,
  grated cheese) against patties of half peeled, coarsely grated broccoli stem
  and half carrot, same binder, same pan, about 1 cm thick.
- **Judge.** Do they hold when turned? Is the stem cooked through, or
  stringy?
- **Taste.** Is the stem noticeable; is it pleasant (sweet, kohlrabi-like)
  or cabbagey? Would you save stems for this?
- **Stop if** the stem stays stringy or tastes raw in a patty that is
  otherwise done.
