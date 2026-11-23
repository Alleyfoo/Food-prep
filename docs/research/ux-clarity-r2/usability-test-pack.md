# Usability test pack — 3 to 5 new users

**For:** people who cook at home and have **never seen** Ingredient Foundry.
**Length:** 35–45 minutes per participant.
**Build:** `experimental/ux-shared-context` (E1), or whatever build is being
tested. Write the commit hash on every results sheet.

**Results:** none yet. This pack contains **no results**, and none should be
written in until a session has been run.

---

## 1. Setup (moderator, before each session)

1. Copy the tastings file and point the app at the copy, so T5 cannot touch
   the real record:

   ```powershell
   Copy-Item src\foodprep\data\tastings.yaml $env:TEMP\tastings-test.yaml
   ```

   ```powershell
   $env:FOODPREP_TASTINGS_PATH = "$env:TEMP\tastings-test.yaml"; py -3.11 -m streamlit run app.py --server.port 8510
   ```

2. Open a **new private browser window** at `http://localhost:8510` (or the
   port shown). A fresh session is the default state: Cook › Ingredient
   Explorer, broccoli, nothing on hand.
3. Window size: a laptop screen (about 1400 px wide). If you test phone
   width, record it as a separate condition.
4. Recording: screen and audio with consent, or a second person taking
   notes.
5. Between tasks, **reload the page with no query string**
   (`http://localhost:8510/`), so each task starts from the default.

## 2. Neutral introduction (read aloud, word for word)

> "Thanks for helping. We're testing the app, not you, so nothing you do can
> be wrong. If something is confusing, that's exactly what we need to hear.
> I'll give you a few situations from a normal kitchen. Please think aloud:
> say what you're looking at, what you expect, and what you're unsure about.
> I won't help or explain while you work, though you can ask questions and
> I'll answer them at the end. You can stop at any time."

**Do not** describe what the app does, name any section or tab, or explain
any term.

## 3. First look (2 minutes, before any task)

**Prompt:** "Take a minute to look at this screen without clicking. What do
you think this app is for? What would you do first?"

Record their words verbatim. Then ask: "What do you think 'Cook', 'Explore'
and 'Experiment' each contain?"

## 4. Tasks

Read the **prompt only**. Give each task at most 4 minutes. Stop at 4
minutes, or when they say they're done or that they give up.

| # | Prompt (read exactly) | Complete when they… | Not complete if… |
| --- | --- | --- | --- |
| T1 | "You have broccoli, plain yogurt, lemon and garlic at home. Use the app to find something to make with the broccoli." | say a broccoli preparation **and** at least one of yogurt / lemon / garlic to go with it, **having entered** what they have | they name a dish without entering ingredients, or name something the screen doesn't say |
| T2 | "Tonight's dinner is potato gratin with a fried egg. It feels heavy. Use the app to find what would help, and what you should not add more of." (Changed from the original script so the preloaded example plate does not answer it. Checked against `query.plate_balance_detail`: heavy, gaps salt / acid / herb / crunch, avoid more richness.) | name an acid, herb or crunch to add **and** that they should avoid more fat or cream | they read the example plate's result without changing the plate |
| T3 | "You roasted a tray of tomatoes yesterday. What could you do with them today?" | name a use (pasta, toast, soup, pizza…) **and** one thing to add | — |
| T4 | "You often make roasted cabbage and you're bored of it. Find something unusual to try with it, and how to try it without wasting a whole tray." | name an untested pairing **and** its small test (one piece + small amount) | they name a Cook suggestion as "unusual" |
| T5 | "Say you tried brown butter on roasted broccoli and it worked. Record that in the app." | the entry appears in the trial history | they stop at the review step |
| Q | "Without using the app, which part would you use to find a tasty idea you can make right now?" | — (answer only) | — |

### Optional comparison (participants 4–5): question-first entry

Before T1–T4, hand the participant a printed card with these questions and
say "You can start from this card if you like". Each question is a link
(the moderator types it in on request):

| Question | Link |
| --- | --- |
| What can I make with what I have? | `/?tab=ingredient-explorer` |
| What can I do with something I already cooked? | `/?tab=component-explorer` |
| My plate feels off — what's missing? | `/?tab=plate-balance` |
| Something new to try | `/?tab=scout` |
| I tried something — record it | `/?tab=scout` |

Compare their time to the right tool, and their wrong clicks, with
participants 1–3.

## 5. Observer notes

For each task, note:

- **Path:** every section, tab, picker and button, in order.
- **Hesitations:** see section 6.
- **Wrong turns:** a view entered and left without using it.
- **Terms they ask about or misread.** Watch especially for: branch, Raw
  Assemble, HIGH, component, hard gaps, soft flags, transformed state,
  hypothesis, corpus, append-only, "Commit that file".
- **Attempts to click non-clickable things**, such as chips, journey text or
  map nodes.
- **Whether they look at the context strip** ("INVESTIGATING … AVAILABLE …").
  Note if they read it aloud or point at it.
- **Whether they notice** the card marked "● The dish you are investigating".
- **Errors** (wrong answer given confidently) vs **failures** (gave up).

## 6. Capturing hesitation

A **hesitation** is any of:
- a pause of more than 5 s with no input;
- a "hmm", "where…?" or "what's…?";
- cursor wandering over three or more targets without clicking;
- scrolling down and back up.

Write the time, the screen and what was on it, with their words verbatim.
Do not interpret hesitations during the session.

## 7. After each task (ask, 1 minute)

1. "How sure are you of your answer?" (not / somewhat / very)
2. "Was anything on that screen confusing or surprising?"
3. "Where did you expect to find it first?"

## 8. After all tasks (5 minutes)

1. "In one sentence, what is this app for?"
2. "What would you call the three top buttons, if you named them?"
3. "Was there a moment you felt lost? Where?"
4. Show the Map (`/?tab=map`): "What is this for? Would you use it to find
   something, or to look around?"
5. Show Taste Circle: "What would you click first here?"
6. "Did you notice the line starting 'Investigating'? What does it tell
   you?"
7. "Anything you expected to be clickable that wasn't?"

## 9. Results template (one per participant)

```
Participant: P_   Date:            Build (commit):        Width: ____ px
Cooking experience (self-described):
First look — "what is it for?" (verbatim):
First look — Cook / Explore / Experiment guesses:

| Task | Outcome (complete / error / failed / timed out) | Time | Path | Hesitations (time · screen · words) | Terms misread | Confidence (n/s/v) |
| T1 | | | | | | |
| T2 | | | | | | |
| T3 | | | | | | |
| T4 | | | | | | |
| T5 | | | | | | |
| Q  | answer: | | | | | |

Context strip noticed?   yes / no / after prompt
Investigated-dish marker noticed?   yes / no
Clicked non-clickable elements (which):
Map: find / look around / neither — words:
Post-session answers (1–7):
Moderator notes (observations only, no interpretations):
```

## 10. Aggregation (after all sessions)

Report counts, not percentages; with 3–5 people a percentage means nothing.
Example: "2 of 4 completed T1".

For each prediction in [task-evaluation.md](task-evaluation.md) and
[research-reconciliation.md](research-reconciliation.md) (N1–N12, S1–S5),
mark it **confirmed**, **not seen** or **contradicted**, citing participant
IDs. A prediction seen in one participant only is a lead, not a finding.

Restore afterwards: close the app and delete
`$env:TEMP\tastings-test.yaml`. The real file was never used.
