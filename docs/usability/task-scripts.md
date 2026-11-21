# Usability task scripts

Five things a cook actually tries to do. Run them with someone who has not seen
the app: read them the **situation** only, never the steps, and ask them to
think aloud. Note every hesitation, wrong click and "huh?". Stop a task after
three minutes and count it as failed.

Each task is also an automated check in `tests/test_usability_tasks.py`. Those
checks prove the answer can be reached; only a person can tell you whether it
can be **found**.

Start every task from a fresh page load (`streamlit run app.py`).

---

## T1 · What's for dinner from what I have?

**Situation:** "You have broccoli, plain yogurt, lemon and garlic at home.
Find something to make with the broccoli."

**Success:** they name a broccoli preparation *and* at least one thing they
have that goes with it, and they found it by telling the app what they have.

**Watch for:**
- Do they find the "What do I have right now?" box without help?
- After filling it in, do they notice the cards change ("Available now" and
  "Missing but useful")?
- Yogurt: does the app ever say what to do with it?

## T2 · My plate feels heavy

**Situation:** "Dinner is mashed potatoes and a chickpea patty. It feels
stodgy. What would fix it, and what should you not add?"

**Success:** they name an acid, herb or crunch to add, and that they should
not add more fat or cream.

**Watch for:**
- Do they find Plate Balance under Cook?
- Is the starting plate (mashed potatoes and chickpea patty) already filled in,
  and do they realise it is an example?
- Do they read "Hard gaps" or "May want more" as the answer?

## T3 · Leftovers from yesterday

**Situation:** "You roasted a tray of tomatoes yesterday. What can you do with
them today?"

**Success:** they name a use (pasta, toast, soup and so on) and something to
add.

**Watch for:**
- Do they go to Ingredient Explorer (tomato → roast) or Component Explorer
  (roasted tomato)? Either is fine. Do they get stuck in between?
- Do they understand "component" and "after-state"?

## T4 · Something new to try

**Situation:** "You make roasted cabbage often and you're bored of it. Find
something unusual to try with it, and how to try it without wasting a whole
tray."

**Success:** they name an untested pairing and its smallest test (a ratio on
one piece).

**Watch for:**
- Do they find Scout under Experiment?
- Do they understand that Scout ideas are untested, not recipes?
- Do they read Compatibility and Novelty as two separate claims, or as a
  score?

## T5 · I tried it — keep a record

**Situation:** "You tried brown butter on roasted broccoli and it worked.
Record that."

**Success:** the trial appears in the card's trial history, saved from the
*Record a tasting* form.

**Watch for:**
- Do they find *Record a tasting* under the hypothesis?
- Do they understand the verdict words, and what "append-only" means for a
  second, disagreeing attempt?
- Do they tick the safety confirmation without reading it?
