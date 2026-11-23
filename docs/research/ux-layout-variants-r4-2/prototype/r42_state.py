"""R4.2: R4.1's URL context plus two VARIANT keys for layout validation.

VARIANT     ov     overview cell encoding: a = compact code (R4), b = labelled
                   summary (R4.1, default), c = named roles with status words
            sheet  fact-sheet density: full (R4.1, default) or dense
            pal    colour world: white (default), cool, or peach (the
                   previous food-coloured palette, kept as the reference)
            -> set by the facilitator in the URL; every link and "reset all"
               keeps them, so a participant stays in one condition.

CIRCLE      pane=circle opens the product's Taste Circle builder around the
            record in detail. Its dish is LOCAL and URL-held too:
            tc   locked dimensions, "dimension:filler" in the order chosen
            tcx  the dimension whose fillers are fanned out
            tcp  page of that fan
            tcb  the record the dish was built around; when rec changes,
                 reconcile() starts a fresh circle

Everything below is R4.1's state module, unchanged:


Forked from R4 (docs/research/ux-integrated-r4/prototype/r4_state.py).
Only change: one more LOCAL key, `graph` (trace pane: show a graph that is
collapsed by default because it has more than GRAPH_LIMIT relationships).
The model module is R4's, unchanged.

Three scopes (documented in workspace-design.md):

GLOBAL      ingredient, have, filters (has / paired / gap), hide
            -> change what every pane shows (availability, greyed rows,
               "excluded by filter" notes in detail, compare and trace)
SELECTION   rec (the record in the fact sheet), cmp (pinned compare set,
            up to 3), trace (the traced entity, "kind:name")
            -> shared by all panes; opening another pane never clears them
LOCAL       pane (which right-hand pane is open), cols (overview column set),
            depth (trace step), diff (compare: differences only), answer
            (E3 summary, off by default)
            -> only change their own pane

Every click is a link to a new URL, so the browser's Back button restores
the previous context, and any state can be shared or captured.
"""
from __future__ import annotations

from typing import Any, Mapping
from urllib.parse import urlencode

from r4_model import of, pretty, route_ids

LIST_KEYS = ("have", "has", "paired", "gap", "cmp", "tc")
DEFAULTS: dict[str, Any] = {
    "ingredient": "broccoli", "have": [], "has": [], "paired": [], "gap": [],
    "hide": False, "rec": "", "cmp": [], "trace": "", "pane": "",
    "cols": "summary", "depth": 1, "diff": False, "answer": False,
    "graph": False, "ov": "b", "sheet": "full",
    "tc": [], "tcx": "", "tcp": 0, "tcb": "", "pal": "white",
}
GLOBAL = ("ingredient", "have", "has", "paired", "gap", "hide")
SELECTION = ("rec", "cmp", "trace")
LOCAL = ("pane", "cols", "depth", "diff", "answer", "graph", "tc", "tcx", "tcp", "tcb")
VARIANT = ("ov", "sheet", "pal")
OV = {"a": "compact code", "b": "labelled summary", "c": "named roles"}
SHEETS = {"full": "full", "dense": "dense"}
PALS = ("peach", "white", "cool")      # colour world, see r42_palette

HAS = {"route": "a flavour route", "idea": "a Scout idea", "tested": "a tasting",
       "onhand": "a curated pairing on hand"}
GAP = {"unpaired": "a need with no curated pairing", "noroute": "no flavour route",
       "nosource": "a pairing with no source", "noprofile": "no sensory profile"}
COLS = {"summary": "Summary", "sensory": "Sensory", "matrix": "Needs × roles",
        "evidence": "Evidence"}
PANES = ("detail", "compare", "trace", "circle")
TRACE_KINDS = ("state", "ingredient", "route", "source")


def parse(params: Mapping[str, str]) -> dict[str, Any]:
    st = dict(DEFAULTS)
    for k, v in params.items():
        if k not in DEFAULTS:
            continue
        if k in LIST_KEYS:
            st[k] = [x for x in str(v).split(",") if x]
        elif k in ("hide", "diff", "answer", "graph"):
            st[k] = str(v) == "1"
        elif k == "depth":
            st[k] = max(1, min(3, int(v))) if str(v).isdigit() else 1
        elif k == "tcp":
            st[k] = min(int(v), 50) if str(v).isdigit() else 0
        else:
            st[k] = str(v)
    st["cmp"] = st["cmp"][:3]
    if st["cols"] not in COLS:
        st["cols"] = "summary"
    if st["pane"] not in PANES:
        st["pane"] = ""
    if st["ov"] not in OV:
        st["ov"] = "b"
    if st["sheet"] not in SHEETS:
        st["sheet"] = "full"
    if st["pal"] not in PALS:
        st["pal"] = "white"
    return st


def to_params(st: Mapping[str, Any]) -> dict[str, str]:
    out = {}
    for k, d in DEFAULTS.items():
        v = st.get(k, d)
        if v == d or v in ("", [], None):
            if k == "ingredient":          # always explicit, for shareable URLs
                out[k] = str(v or d)
            continue
        if isinstance(v, bool):
            out[k] = "1"
        elif isinstance(v, list):
            out[k] = ",".join(v)
        else:
            out[k] = str(v)
    return out


def href(st: Mapping[str, Any], **changes: Any) -> str:
    new = dict(st)
    new.update(changes)
    return "?" + urlencode(to_params(new), safe=",:")


def toggle(lst: list[str], item: str, limit: int = 3) -> list[str]:
    if item in lst:
        return [x for x in lst if x != item]
    return (lst + [item])[-limit:]


def pin(st: Mapping[str, Any], comp: str) -> dict[str, Any]:
    """URL changes for the ☐ on an overview row.

    Pinning the first row while another record is selected compares the two
    (the selected record is the natural reference). The Compare pane opens
    only once two records are pinned; unpinning never changes the pane
    unless fewer than two remain while Compare is open."""
    if comp in st["cmp"]:
        new = [c for c in st["cmp"] if c != comp]
        pane_ = "detail" if st["pane"] == "compare" and len(new) < 2 else st["pane"]
        return {"cmp": new, "pane": pane_}
    if not st["cmp"] and st["rec"] and st["rec"] != comp:
        new = [st["rec"], comp]
    else:
        new = toggle(st["cmp"], comp)
    return {"cmp": new, "pane": "compare" if len(new) >= 2 else st["pane"]}


def compare_letter(st: Mapping[str, Any], comp: str) -> str:
    """A, B, C: the same letter names a pinned record in the overview, the
    compare header, the context bar and the Compare tab."""
    return "ABC"[st["cmp"].index(comp)] if comp in st["cmp"] else ""


def pane(st: Mapping[str, Any]) -> str:
    """Which right-hand pane is open when the URL doesn't say."""
    if st["pane"]:
        return st["pane"]
    if st["trace"] and not st["rec"]:
        return "trace"
    if st["rec"]:
        return "detail"
    if st["cmp"]:
        return "compare"
    return "detail"


def trace_focus(st: Mapping[str, Any]) -> tuple[str, str] | None:
    if ":" not in st.get("trace", ""):
        return None
    kind, name = st["trace"].split(":", 1)
    return (kind, name) if kind in TRACE_KINDS and name else None


def reconcile(st: dict[str, Any], m: dict) -> dict[str, Any]:
    """Drop selections that don't exist for the current ingredient (after an
    ingredient change). An ingredient or source trace survives: tracing lemon
    across broccoli and then cabbage is a legitimate investigation."""
    comps = {s["component"] for s in m["states"]}
    routes = {r["route_id"] for r in of(m, kind="route_fit")}
    st = dict(st)
    if st["rec"] and st["rec"] not in comps:
        st["rec"] = ""
    if st.get("tcb", "") != st["rec"] or not st["rec"]:   # a new subject: a fresh circle
        st.update(tc=[], tcx="", tcp=0, tcb="")
    st["cmp"] = [c for c in st["cmp"] if c in comps]
    f = trace_focus(st)
    if f and ((f[0] == "state" and f[1] not in comps)
              or (f[0] == "route" and f[1] not in routes)):
        st["trace"] = ""
    return st


# ---------------------------------------------------------------------------
# global filters: the reasons a row does not match, kept visible (Qlik grey)
# ---------------------------------------------------------------------------

def filter_options(m: dict) -> dict[str, list[str]]:
    fillers = sorted({r["ingredient"] for r in of(m, kind="pairing")})
    return {"has": list(HAS), "paired": fillers, "gap": list(GAP)}


def exclusion(m: dict, comp: str, st: Mapping[str, Any]) -> list[str]:
    """Why state *comp* fails the active global filters ([] = it matches)."""
    why = []
    pairs = of(m, comp, "pairing")
    ideas = of(m, comp, "idea")
    for h in st.get("has", []):
        if h == "route" and not route_ids(m, comp):
            why.append("no flavour route")
        elif h == "idea" and not ideas:
            why.append("no Scout idea")
        elif h == "tested" and not any(i["testing"]["status"] == "tested" for i in ideas):
            why.append("no tasting recorded")
        elif h == "onhand" and not any(p["knowledge"] == "curated"
                                       and p["availability"] == "on hand" for p in pairs):
            why.append("no curated pairing on hand")
    for f in st.get("paired", []):
        if not any(p["ingredient"] == f for p in pairs):
            why.append(f"no pairing with {pretty(f)}")
    for g in st.get("gap", []):
        if g == "unpaired" and not any(r["coverage"] == "not recorded"
                                       for r in of(m, comp, "need")):
            why.append("every need has a curated pairing")
        elif g == "noroute" and route_ids(m, comp):
            why.append("has a flavour route")
        elif g == "nosource" and not any(not p["evidence"]["sources"] for p in pairs):
            why.append("every pairing has a source")
        elif g == "noprofile":
            from r4_model import state_by
            if state_by(m, comp)["profile"]:
                why.append("has a sensory profile")
    return why


def active_filters(st: Mapping[str, Any]) -> list[tuple[str, str, str]]:
    """(key, value, label) for every active global filter."""
    out = [("has", h, "has " + HAS[h]) for h in st.get("has", []) if h in HAS]
    out += [("paired", f, "paired with " + pretty(f)) for f in st.get("paired", [])]
    out += [("gap", g, "has " + GAP[g]) for g in st.get("gap", []) if g in GAP]
    return out
