"""Answer-first summary for the Ingredient Explorer (UX experiment E3, variant B).

The summary is *derived*, never invented: every word comes from data the
detailed cards already show (the branch card, its flavour routes, and the
availability partition), so the answer and the card cannot disagree.

Presentation rule (deterministic, documented in docs/research/ux-answer-first):

* The answer is always about the prepared ingredient being investigated
  (the shared context's state). If none is chosen for this ingredient, the
  answer says so instead of picking one.
* With items on hand: the first flavour route, in the order
  ``query.flavour_routes_for_component`` already returns (most required
  elements on hand, then route id), that uses at least one on-hand item.
  Failing that, the single pairings on hand (``available_filter``), and
  failing that, an honest "nothing you have is paired with it yet".
* With nothing on hand: the first route in the query's own order
  (attestation, then name), else the roles the state usually needs with the
  first curated filler for each, else a "little is recorded" message.
* Risks of the state (and of the chosen route) are always shown.
* "Other ways to use what you have" lists the other preparations of the same
  ingredient, in the cards' existing rank, whose routes use an on-hand item.

Nothing here ranks or scores; the order is the query layer's own.
"""
from __future__ import annotations

from html import escape as _esc
from typing import Any


def _r(name: str) -> str:
    return (name or "").replace("_component", "").replace("_", " ").strip()


def card_anchor(component: str) -> str:
    """The id a detailed card carries, so the answer can link to it."""
    return "card-" + (component or "").replace("_", "-")


def _first_route_using(routes: list[dict] | None) -> dict | None:
    for r in routes or []:
        if r.get("available_elements"):
            return r
    return None


def _role_needs(card: dict, limit: int = 4) -> list[tuple[str, str | None]]:
    """(role, first curated filler or None) for the roles the state misses."""
    fillers = card.get("fillers_by_role") or {}
    out = []
    for m in card.get("missing") or []:
        role = m["role_name"]
        first = (fillers.get(role) or [{}])[0].get("filler")
        out.append((role, first))
    return out[:limit]


def explorer_answer(ingredient: str, card: dict | None,
                    routes: list[dict] | None,
                    partition: dict | None,
                    have: list[str] | None,
                    others: list[tuple[dict, list[dict]]] | None = None
                    ) -> dict[str, Any]:
    """The summary as data. *routes* and *partition* must be the same objects
    the detailed card is drawn from."""
    have = list(have or [])
    if card is None:
        return {"kind": "no_state", "ingredient": ingredient,
                "headline": f"Choose how the {_r(ingredient)} is prepared",
                "lines": [("", "Suggestions depend on the preparation: roasted "
                           "and raw lead to different things. Pick one under "
                           "“Prepared ingredient”, or read the "
                           "preparations below.")],
                "watch": [], "state": None, "others": []}

    state = card["component"]
    watch = [_r(x) for x in card.get("risks") or []]
    lines: list[tuple[str, str]] = []
    result: dict[str, Any] = {"state": state, "ingredient": ingredient,
                              "watch": watch, "others": []}

    route = _first_route_using(routes) if have else None
    if route:
        got = [e["ingredient"] for e in route["available_elements"]]
        need = [e["ingredient"] for e in route.get("missing_required") or []]
        optional = [e for e in route.get("elements") or []
                    if e["optionality"] != "required" and e["ingredient"] not in got]
        result.update(kind="route", route_id=route["route_id"], have=got,
                      need=need, optional=[e["ingredient"] for e in optional])
        result["headline"] = f"Try {_r(state)}: {route['name'].lower()}"
        lines.append(("You have", ", ".join(_r(g) for g in got)))
        lines.append(("Still needed", ", ".join(_r(n) for n in need)
                      if need else "nothing else — you have what it needs"))
        if optional:
            lines.append(("Optional", "; ".join(
                f"{_r(e['ingredient'])} ({e['contribution'].lower()})"
                for e in optional)))
        if route.get("fit_reason") or route.get("description"):
            lines.append(("Why", " ".join(x for x in (route.get("description"),
                                                    route.get("fit_reason")) if x)))
        if route.get("risks"):
            watch.append(route["risks"])
    elif have and partition and partition.get("available_now"):
        now = partition["available_now"]
        result.update(kind="pairings", have=[g["filler"] for g in now])
        names = [_r(g["filler"]) for g in now]
        joined = (", ".join(names[:-1]) + " and " + names[-1]
                  if len(names) > 1 else names[0])
        result["headline"] = f"Add {joined} to {_r(state)}"
        lines.append(("You have", "; ".join(
            f"{_r(g['filler'])} ({', '.join(g['roles'])})" for g in now)))
        miss = [m for m in partition.get("missing_but_useful") or []]
        if miss:
            lines.append(("Still missing", "; ".join(
                f"{m['role']}" + (f" (e.g. {_r(m['fillers'][0])})" if m["fillers"] else "")
                for m in miss)))
        lines.append(("Why", "These are single pairings recorded for "
                      f"{_r(state)}. No flavour route here uses what you have."))
    elif have:
        result.update(kind="no_match", have=[])
        result["headline"] = f"Nothing you have is paired with {_r(state)} yet"
        needs = _role_needs(card)
        if needs:
            lines.append(("It usually needs", "; ".join(
                role + (f" (e.g. {_r(f)})" if f else "") for role, f in needs)))
        lines.append(("Note", "“Not paired yet” means nobody has "
                      "recorded the pairing, not that it clashes."))
    else:
        recorded = (routes or [None])[0]
        if recorded:
            req = [e["ingredient"] for e in recorded["elements"]
                   if e["optionality"] == "required"]
            opt = [e["ingredient"] for e in recorded["elements"]
                   if e["optionality"] != "required"]
            result.update(kind="recorded_route", route_id=recorded["route_id"])
            result["headline"] = f"One way with {_r(state)}: {recorded['name'].lower()}"
            lines.append(("Needs", ", ".join(_r(x) for x in req)
                          + (f" (optional: {', '.join(_r(x) for x in opt)})" if opt else "")))
            if recorded.get("fit_reason"):
                lines.append(("Why", recorded["fit_reason"]))
            if recorded.get("risks"):
                watch.append(recorded["risks"])
        else:
            needs = _role_needs(card)
            if any(f for _, f in needs):
                result.update(kind="needs")
                result["headline"] = f"What {_r(state)} usually needs"
                lines.append(("Add", "; ".join(
                    role + (f": {_r(f)}" if f else "") for role, f in needs)))
                lines.append(("Note", "No flavour route is written for "
                              f"{_r(state)} yet; these are single pairings."))
            else:
                result.update(kind="limited")
                result["headline"] = f"Little is recorded for {_r(state)} yet"
                roles = ", ".join(role for role, _ in needs)
                lines.append(("Known", (f"It tends to lack {roles}, " if roles else "")
                              + "but no pairing or flavour route has been written "
                              "for it. Nothing here is a recommendation."))
        lines.append(("Next", "Enter what you have above to see what you can "
                      "make now."))

    if have:
        for other, oroutes in others or []:
            r = _first_route_using(oroutes)
            if r and other["component"] != state:
                result["others"].append((other["component"], r["name"]))
    result["lines"] = lines
    return result


def answer_html(a: dict[str, Any]) -> str:
    """The answer panel. Plain sentences first, then a link to the evidence."""
    parts = ['<section class="answer-first" aria-label="Suggested next step">',
             '<div class="answer-kicker">Suggested next step</div>',
             f'<div class="answer-headline">{_esc(a["headline"])}</div>']
    if a.get("lines"):
        parts.append('<dl class="answer-lines">')
        for label, text in a["lines"]:
            if label:
                parts.append(f'<dt>{_esc(label)}</dt><dd>{_esc(text)}</dd>')
            else:
                parts.append(f'<dd class="answer-wide">{_esc(text)}</dd>')
        parts.append('</dl>')
    if a.get("watch"):
        parts.append('<div class="answer-watch"><span class="answer-watch-lbl">'
                     'Watch for</span> ' + " · ".join(_esc(w) for w in a["watch"])
                     + '</div>')
    links = []
    if a.get("state"):
        links.append(f'<a href="#{card_anchor(a["state"])}">See the full '
                     f'{_esc(_r(a["state"]))} card ↓</a>')
    if a.get("others"):
        links.append('Other ways to use what you have: ' + ", ".join(
            f'<a href="#{card_anchor(c)}">{_esc(_r(c))}</a> ({_esc(name.lower())})'
            for c, name in a["others"]))
    if links:
        parts.append('<div class="answer-links">' + "<br>".join(links) + "</div>")
    parts.append("</section>")
    return "".join(parts)
