"""Thin runner: print the five-flow demo without the CLI.

Usage:  python scripts/demo.py

Builds an in-memory db from the curated YAML and walks the five demo flows.
For the CLI equivalent, see `foodprep demo`.
"""

from foodprep.db import connect
from foodprep.demo import run_demo


def main() -> int:
    conn = connect(":memory:")
    from foodprep.loader import build
    build(conn)
    run_demo(conn)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())