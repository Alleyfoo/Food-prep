"""Deployment guards: one Streamlit pin, and no deprecated embedding API."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _streamlit_spec(lines):
    return next(l.strip().strip('",') for l in lines
                if re.match(r'\s*"?streamlit[<>=]', l))


def test_streamlit_is_pinned_the_same_everywhere():
    """Streamlit Cloud installs from requirements.txt; pip from pyproject."""
    req = _streamlit_spec((ROOT / "requirements.txt").read_text().splitlines())
    # Plain text, not tomllib: the project supports Python 3.10.
    pyproject = _streamlit_spec((ROOT / "pyproject.toml").read_text().splitlines())
    pyproject = pyproject.split('"')[0]
    assert req == pyproject
    assert "<" in req, "an unbounded Streamlit can break the app on a fresh install"


def test_app_does_not_use_components_html():
    """The Map moved to the vis-network custom component; keep it there."""
    for path in (ROOT / "src" / "foodprep" / "ui").glob("*.py"):
        assert "components.html(" not in path.read_text(encoding="utf-8"), path.name
