# Limitations

## Found in this experiment, unresolved (pre-existing, Streamlit 1.50)
1. **Tab out of a selectbox shows the wrong value.** One Tab out of a picker
   flips its displayed value to the first option ("apricot compote"), while
   the context, content and URL stay correct. The picker misleads until the
   next change. **Reproduced on unchanged `main`** (separate worktree), so E1
   did not cause it. A likely fix (re-keyed pickers with `index=`) would change
   every picker key the tests and trace rely on, so it was left for a focused
   follow-up.
2. **Escape clears the "What do I have" list.** With its menu closed, Escape
   empties every pick (Streamlit/BaseWeb multiselect; no option to disable).
   The context strip now makes the loss visible ("nothing entered"), and a
   reload does not bring it back.
3. **Stale frame after a rapid double save.** Two clicks within one rerun
   wrote exactly one entry, but the screen briefly kept the old form and lost
   the "Saved" message until the next interaction.
4. **A transient frame on reload** can show two section pills highlighted for
   a moment before the rail settles.

## Implementation constraints
- **Back/forward:** Streamlit replaces the URL instead of adding history
  entries, so browser Back leaves the app rather than stepping back. That
  avoids contradictory states; it gives no undo.
- **One tasting per pairing per day:** the existing duplicate guard keys on
  (hypothesis, state, date), so a genuine second attempt the same day is
  refused, now with a plain message. Unchanged from before.
- **Graph canvases aren't keyboard-operable.** vis-network keyboard mode binds
  to the whole window, so it wasn't enabled. Taste Circle's Cards view is the
  keyboard route; the Map has none.
- **Dish reset:** changing the state still clears a built Taste Circle dish,
  silently. That's existing behaviour, now reachable from any view.

## Left untouched on purpose
E2 (rejected Scout reasons, untested-idea markers in Cook), D12 colour meaning,
D22 rail wrapping, D5/D11, Map focus/legend/inspect (R1 R3), E1a variant.

## Not established
No real users have tried any of this. The before/after counts are mechanical.
