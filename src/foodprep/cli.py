"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .db import DEFAULT_DB_PATH, connect
from .loader import DATA_PATH, build
from . import corpus, export, query


def _parse_csv(s: str | None) -> list[str] | None:
    """Comma-separated --available value -> list of stripped names. None/empty
    -> None so the engine takes the current (unfiltered) path."""
    if not s:
        return None
    items = [x.strip() for x in s.split(",") if x.strip()]
    return items or None


def _emit_markdown(md: str, out: str | None) -> int:
    """Write Markdown to --out (UTF-8) or print to stdout."""
    if out:
        Path(out).write_text(md, encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print(md)
    return 0


def _db_has(conn, table: str) -> bool:
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
    ).fetchone()
    if exists is None:
        return False
    return conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] > 0


def cmd_build(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    build(conn, args.data)
    print(f"Built {args.db} from {args.data}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    if conn.execute("SELECT count(*) FROM transformations").fetchone()[0] == 0:
        print("Database is empty. Run `foodprep build` first.")
        return 1
    print(query.answer(conn, args.prompt))
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    rows = query.batch_prep(conn, args.ingredient)
    print(f"Batch-prep from {args.ingredient} (high/very-high reuse):")
    for r in rows:
        print(f"  - {r['technique']} -> {r['component']}  "
              f"(batch={r['batch_prep_value']}, freezes={bool(r['freezes_well'])}, "
              f"conf={r['confidence']})")
    return 0


def cmd_hub(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    print(query.hub_explained(conn, args.ingredient))
    return 0


def cmd_scout(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    print(query.scout(conn, args.technique))
    return 0


def cmd_journey(args: argparse.Namespace) -> int:
    """Render complete Cook journeys for an ingredient."""
    conn = connect(args.db)
    if not _db_has(conn, "journeys"):
        print("Database is empty or has no journeys. Run `foodprep build` first.")
        return 1
    result = query.render_ingredient_journeys(conn, args.ingredient, args.slug)
    print(result)
    return 1 if result.startswith("No journey") else 0


def cmd_plate(args: argparse.Namespace) -> int:
    """Plate Balance Engine — Cook mode (separate from Scout)."""
    conn = connect(args.db)
    if conn.execute("SELECT count(*) FROM component_profiles").fetchone()[0] == 0:
        print("Database is empty. Run `foodprep build` first.")
        return 1
    print(query.plate_balance(conn, args.prompt, args.destination))
    return 0


def cmd_filler(args: argparse.Namespace) -> int:
    """Filler profile — the five questions (roles / repairs / avoid / availability / Cook-or-Scout)."""
    conn = connect(args.db)
    if conn.execute("SELECT count(*) FROM ingredients").fetchone()[0] == 0:
        print("Database is empty. Run `foodprep build` first.")
        return 1
    print(query.filler_profile(conn, args.name))
    return 0


def cmd_backfill(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    if conn.execute("SELECT count(*) FROM pairings").fetchone()[0] == 0:
        print("Database is empty. Run `foodprep build` first.")
        return 1
    summary = corpus.backfill(conn, args.dir, verbose=args.verbose)
    print(f"Backfill from {args.dir}: "
          f"{summary['updated']} pairings gained corpus evidence, "
          f"{summary['zero']} resolved to no co-occurrence, "
          f"{summary['skipped']} skipped (no target transformation).")
    print("Curated confidence and curated_role_fit are untouched "
          "(corpus is evidence, not truth).")
    return 0


def cmd_export_branch(args: argparse.Namespace) -> int:
    """Export one ingredient/technique branch as Markdown."""
    conn = connect(args.db)
    if not _db_has(conn, "transformations"):
        print("Database is empty. Run `foodprep build` first.")
        return 1
    available = _parse_csv(args.available)
    md = export.branch_markdown(conn, args.ingredient, args.technique, available)
    if md is None:
        print(f"No transformation for {args.ingredient}/{args.technique}.")
        return 1
    return _emit_markdown(md, args.out)


def cmd_export_component(args: argparse.Namespace) -> int:
    """Export a component card as Markdown."""
    conn = connect(args.db)
    if not _db_has(conn, "components"):
        print("Database is empty. Run `foodprep build` first.")
        return 1
    available = _parse_csv(args.available)
    md = export.component_markdown(conn, args.name, available)
    if md is None:
        print(f"No component named {args.name}.")
        return 1
    return _emit_markdown(md, args.out)


def cmd_export_plate(args: argparse.Namespace) -> int:
    """Export a plate balance as Markdown. Plate items are joined with ' and '
    so the phrase parser sees them as separate items (matching the UI's text
    construction), e.g. `mashed_potatoes chickpea_patty` -> two items."""
    conn = connect(args.db)
    if not _db_has(conn, "component_profiles"):
        print("Database is empty. Run `foodprep build` first.")
        return 1
    available = _parse_csv(args.available)
    text = " and ".join(args.items)
    md = export.plate_markdown(conn, text, available)
    return _emit_markdown(md, args.out)


def cmd_export_scout(args: argparse.Namespace) -> int:
    """Export experimental (Scout) pairings as Markdown, disclaimer included."""
    conn = connect(args.db)
    if not _db_has(conn, "pairings"):
        print("Database is empty. Run `foodprep build` first.")
        return 1
    md = export.scout_markdown(conn, ingredient=args.ingredient,
                               technique=args.technique)
    return _emit_markdown(md, args.out)


def cmd_demo(args: argparse.Namespace) -> int:
    """Print the five-flow demo (tomato / component / plate / cabbage / scout)."""
    from .demo import run_demo
    conn = connect(args.db)
    if conn.execute("SELECT count(*) FROM transformations").fetchone()[0] == 0:
        # Work out of the box on a fresh clone: build in memory rather than
        # demanding a prior `foodprep build`. No file is written.
        conn = connect(":memory:")
        build(conn)
    run_demo(conn)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="foodprep", description=__doc__ or "food-prep CLI")
    p.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite path")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build", help="Build SQLite db from YAML ontology")
    pb.add_argument("--data", default=str(DATA_PATH), help="YAML ontology path")
    pb.set_defaults(func=cmd_build)

    pa = sub.add_parser("ask", help="Ask a free-text question")
    pa.add_argument("prompt", nargs="+", help="the question")
    pa.set_defaults(func=cmd_ask)

    pbat = sub.add_parser("batch", help="What can I batch-prep from an ingredient?")
    pbat.add_argument("ingredient", nargs="?", default="tomato")
    pbat.set_defaults(func=cmd_batch)

    ph = sub.add_parser("hub", help="Which ingredient unlocks the most transformations?")
    ph.add_argument("ingredient", nargs="?", default="tomato")
    ph.set_defaults(func=cmd_hub)

    psc = sub.add_parser("scout", help="Experimental / uncommon pairings")
    psc.add_argument("technique", nargs="?", default=None,
                     help="limit to a technique, e.g. roast")
    psc.set_defaults(func=cmd_scout)

    pj = sub.add_parser("journey", help="Complete Cook paths for an ingredient")
    pj.add_argument("ingredient", nargs="?", default="broccoli")
    pj.add_argument("slug", nargs="?", default=None,
                    help="optional path id, e.g. steamed_cold_side")
    pj.set_defaults(func=cmd_journey)

    ppl = sub.add_parser("plate",
                         help="Plate Balance Engine (Cook mode) — what is missing?")
    ppl.add_argument("prompt", nargs="+",
                     help="plate items, e.g. 'mashed potatoes and chickpea patties'")
    ppl.add_argument("--destination", default="complete_savoury_plate",
                     help="destination profile: complete_savoury_plate, side_dish, soup")
    ppl.set_defaults(func=cmd_plate)

    pfl = sub.add_parser("filler",
                         help="Filler profile — roles / repairs / avoid / availability / Cook-or-Scout")
    pfl.add_argument("name", help="filler name or alias, e.g. lemon, pickled cucumber, rye breadcrumbs")
    pfl.set_defaults(func=cmd_filler)

    pbf = sub.add_parser("backfill",
                         help="Attach CulinaryDB co-occurrence evidence to pairings")
    pbf.add_argument("dir", help="CulinaryDB directory with the 4 CSVs")
    pbf.add_argument("--verbose", action="store_true", help="print each pairing")
    pbf.set_defaults(func=cmd_backfill)

    pdm = sub.add_parser("demo",
                         help="Print the five-flow demo (the concept in ~60 seconds)")
    pdm.set_defaults(func=cmd_demo)

    # ---- export (Markdown) ----
    pe = sub.add_parser("export",
                        help="Export a result as Markdown (branch/component/plate/scout)")
    pe_sub = pe.add_subparsers(dest="export_what", required=True)

    peb = pe_sub.add_parser("branch", help="One ingredient/technique branch")
    peb.add_argument("ingredient", help="e.g. broccoli")
    peb.add_argument("technique", help="e.g. steam")
    peb.add_argument("--available", default=None,
                     help="comma-separated on-hand ingredients, e.g. yogurt,pickles,bread")
    peb.add_argument("--out", default=None, help="write to file (default: stdout)")
    peb.set_defaults(func=cmd_export_branch)

    pec = pe_sub.add_parser("component", help="A component card")
    pec.add_argument("name", help="e.g. roasted_tomato_component")
    pec.add_argument("--available", default=None,
                     help="comma-separated on-hand ingredients")
    pec.add_argument("--out", default=None, help="write to file (default: stdout)")
    pec.set_defaults(func=cmd_export_component)

    pep = pe_sub.add_parser("plate", help="A plate balance")
    pep.add_argument("items", nargs="+", help="plate items, e.g. mashed_potatoes chickpea_patty")
    pep.add_argument("--available", default=None,
                     help="comma-separated on-hand ingredients")
    pep.add_argument("--out", default=None, help="write to file (default: stdout)")
    pep.set_defaults(func=cmd_export_plate)

    pes = pe_sub.add_parser("scout", help="Experimental (Scout) pairings")
    pes.add_argument("--ingredient", default=None, help="limit to an ingredient")
    pes.add_argument("--technique", default=None, help="limit to a technique")
    pes.add_argument("--out", default=None, help="write to file (default: stdout)")
    pes.set_defaults(func=cmd_export_scout)

    return p


def main(argv: list[str] | None = None) -> int:
    # Windows console defaults to cp1252; force UTF-8 so the arrow/em-dash render.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    parser = build_parser()
    args = parser.parse_args(argv)
    # join multi-word prompt
    if hasattr(args, "prompt") and isinstance(args.prompt, list):
        args.prompt = " ".join(args.prompt)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
