"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .db import DEFAULT_DB_PATH, connect
from .loader import DATA_PATH, build
from . import query


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
    rows = query.batch_prep(conn)
    print("Batch-prep from tomatoes (high/very-high reuse):")
    for r in rows:
        print(f"  - {r['technique']} -> {r['component']}  "
              f"(batch={r['batch_prep_value']}, freezes={bool(r['freezes_well'])}, "
              f"conf={r['confidence']})")
    return 0


def cmd_hub(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    rows = query.hub_ingredients(conn)
    print("Ingredients that unlock the most tomato transformations:")
    for r in rows[:10]:
        print(f"  - {r['filler']}: {r['transformations_covered']} transformations, "
              f"{r['roles_filled']} roles")
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

    pbat = sub.add_parser("batch", help="What can I batch-prep from tomatoes?")
    pbat.set_defaults(func=cmd_batch)

    ph = sub.add_parser("hub", help="Which ingredient unlocks the most transformations?")
    ph.set_defaults(func=cmd_hub)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    # join multi-word prompt
    if hasattr(args, "prompt") and isinstance(args.prompt, list):
        args.prompt = " ".join(args.prompt)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())