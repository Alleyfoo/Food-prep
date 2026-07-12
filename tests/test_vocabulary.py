from pathlib import Path

import pytest
import yaml

from foodprep.vocabulary import (
    VOCABULARY_PATH,
    VocabularyError,
    load_vocabulary,
    parse_vocabulary,
)


def test_project_vocabulary_has_shared_cook_scout_categories():
    vocabulary = load_vocabulary()

    assert set(vocabulary.categories) == {
        "preparations",
        "transformation_categories",
        "flavours",
        "textures",
        "corrections",
        "destinations",
        "confidence",
        "uncertainty",
    }
    assert vocabulary.require("destinations", "side_dish").name == "Side dish"
    assert vocabulary.require("flavours", "fermented_funky").definition


def test_unknown_vocabulary_value_is_rejected():
    vocabulary = load_vocabulary()

    with pytest.raises(VocabularyError, match="unknown destinations"):
        vocabulary.require("destinations", "generic_balanced_plate")


def test_duplicate_vocabulary_value_is_rejected():
    data = {
        "flavours": [
            {"id": "sour", "name": "Sour", "definition": "Acidity."},
            {"id": "sour", "name": "Tart", "definition": "Also acidity."},
        ]
    }

    with pytest.raises(VocabularyError, match="duplicate flavours"):
        parse_vocabulary(data)


def test_every_term_has_name_and_definition():
    vocabulary = load_vocabulary()

    for category in vocabulary.categories:
        for term in vocabulary.terms(category):
            assert term.name.strip()
            assert term.definition.strip()


def test_vocabulary_yaml_is_packaged_project_data():
    assert VOCABULARY_PATH == Path(VOCABULARY_PATH)
    assert yaml.safe_load(VOCABULARY_PATH.read_text(encoding="utf-8"))
