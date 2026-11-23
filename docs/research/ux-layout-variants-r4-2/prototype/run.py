"""Start the R4.2 workspace with Streamlit's theme taken from the palette.

    py -3.11 docs/research/ux-layout-variants-r4-2/prototype/run.py [--server.port 8543]

Streamlit draws its own labels, placeholders, icons and checkboxes from the
theme. The repository's .streamlit/config.toml belongs to the product app,
so the prototype passes its theme as command-line flags instead, built from
r42_palette: the same seed-tinted ink, page and fill as the workspace, and
no grey. Extra arguments are passed on to Streamlit.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import r42_palette as P  # noqa: E402

# Streamlit's theme is per process, so it takes the default world; app.py
# recolours the page and the filter controls for the world in the URL.
THEME = P.theme(P.DEFAULT_WORLD)


def argv(extra: list[str]) -> list[str]:
    args = ["streamlit", "run", str(HERE / "app.py")]
    for k, v in THEME.items():
        args += [f"--{k}", v]
    if not any(a.startswith("--server.port") for a in extra):
        args += ["--server.port", "8543"]
    return args + extra


if __name__ == "__main__":
    from streamlit.web import cli
    sys.argv = argv(sys.argv[1:])
    sys.exit(cli.main())
