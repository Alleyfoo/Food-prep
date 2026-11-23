"""Where the CulinaryDB corpus is found, and how its location is recorded.

The corpus does not ship with the app. resolve_corpus_dir looks in one fixed
order (command line, $FOODPREP_CORPUS_DIR, data/corpus/culinarydb/), and the
committed novelty.yaml must never carry a machine's own path.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from foodprep import cli, corpus
from foodprep.loader import NOVELTY_PATH


def _fake_corpus(folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    for name in corpus.CORPUS_FILES:
        (folder / name).write_text("", encoding="utf-8")
    return folder


@pytest.fixture
def default_dir(tmp_path, monkeypatch):
    target = tmp_path / "repo" / "data" / "corpus" / "culinarydb"
    monkeypatch.setattr(corpus, "DEFAULT_CORPUS_DIR", target)
    monkeypatch.setattr(corpus, "REPO_ROOT", tmp_path / "repo")
    return target


def test_command_line_path_wins(tmp_path, default_dir):
    given = _fake_corpus(tmp_path / "given")
    env = {corpus.CORPUS_ENV: str(_fake_corpus(tmp_path / "env"))}
    _fake_corpus(default_dir)
    assert corpus.resolve_corpus_dir(given, env=env) == given


def test_environment_variable_comes_next(tmp_path, default_dir):
    env_dir = _fake_corpus(tmp_path / "env")
    _fake_corpus(default_dir)
    assert corpus.resolve_corpus_dir(env={corpus.CORPUS_ENV: str(env_dir)}) == env_dir


def test_repository_folder_is_the_fallback(default_dir):
    _fake_corpus(default_dir)
    assert corpus.resolve_corpus_dir(env={}) == default_dir


def test_a_named_folder_without_the_files_is_an_error_not_a_fall_through(tmp_path, default_dir):
    _fake_corpus(default_dir)
    empty = tmp_path / "typo"
    empty.mkdir()
    with pytest.raises(corpus.CorpusNotFound, match="missing 01_Recipe_Details.csv"):
        corpus.resolve_corpus_dir(empty, env={})
    with pytest.raises(corpus.CorpusNotFound, match=corpus.CORPUS_ENV):
        corpus.resolve_corpus_dir(env={corpus.CORPUS_ENV: str(empty)})


def test_nothing_found_says_where_to_put_the_files(default_dir):
    with pytest.raises(corpus.CorpusNotFound) as err:
        corpus.resolve_corpus_dir(env={})
    message = str(err.value)
    assert str(default_dir) in message and corpus.CORPUS_ENV in message
    assert all(name in message for name in corpus.CORPUS_FILES)


def test_recorded_location_is_portable(tmp_path, default_dir):
    inside = _fake_corpus(default_dir)
    assert corpus.portable_source(inside) == "data/corpus/culinarydb"
    outside = _fake_corpus(tmp_path / "elsewhere" / "CulinaryDB")
    assert corpus.portable_source(outside) == "outside the repository (CulinaryDB)"


def test_committed_novelty_cache_carries_no_local_path():
    data = yaml.safe_load(NOVELTY_PATH.read_text(encoding="utf-8"))
    for row in data["corpora"]:
        src = row.get("source_path") or ""
        assert ":\\" not in src and ":/" not in src and not src.startswith("/"), src


def test_corpus_folder_is_ignored_by_git():
    gitignore = (Path(__file__).resolve().parents[1] / ".gitignore").read_text(encoding="utf-8")
    assert "data/corpus/" in gitignore.splitlines()


@pytest.mark.parametrize("argv", [["novelty", "roasted_broccoli_component"], ["backfill"]])
def test_cli_needs_no_path_and_explains_a_missing_corpus(argv, default_dir, monkeypatch,
                                                         tmp_path, capsys):
    monkeypatch.delenv(corpus.CORPUS_ENV, raising=False)
    db = tmp_path / "f.sqlite"
    assert cli.main(["--db", str(db), "build"]) == 0
    capsys.readouterr()
    assert cli.main(["--db", str(db), *argv]) == 1
    assert "No CulinaryDB corpus found" in capsys.readouterr().out
