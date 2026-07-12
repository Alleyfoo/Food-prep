"""Controlled culinary vocabulary shared by Cook and Scout.

The vocabulary is authored in YAML but validated here so callers receive clear
domain errors before values reach SQLite or reasoning code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import yaml


VOCABULARY_PATH = Path(__file__).with_name("data") / "vocabularies.yaml"


class VocabularyError(ValueError):
    """Raised when vocabulary data or a vocabulary reference is invalid."""


@dataclass(frozen=True)
class VocabularyTerm:
    id: str
    name: str
    definition: str
    metadata: Mapping[str, Any]


class Vocabulary:
    """Immutable, category-indexed collection of controlled terms."""

    def __init__(self, categories: Mapping[str, Mapping[str, VocabularyTerm]]):
        self._categories = MappingProxyType(
            {
                category: MappingProxyType(dict(terms))
                for category, terms in categories.items()
            }
        )

    @property
    def categories(self) -> tuple[str, ...]:
        return tuple(self._categories)

    def terms(self, category: str) -> tuple[VocabularyTerm, ...]:
        try:
            return tuple(self._categories[category].values())
        except KeyError as exc:
            raise VocabularyError(f"unknown vocabulary category: {category!r}") from exc

    def require(self, category: str, term_id: str) -> VocabularyTerm:
        try:
            terms = self._categories[category]
        except KeyError as exc:
            raise VocabularyError(f"unknown vocabulary category: {category!r}") from exc
        try:
            return terms[term_id]
        except KeyError as exc:
            raise VocabularyError(
                f"unknown {category} vocabulary value: {term_id!r}"
            ) from exc


def _validate_term(category: str, raw: Any, index: int) -> VocabularyTerm:
    if not isinstance(raw, dict):
        raise VocabularyError(f"{category}[{index}] must be a mapping")
    missing = [key for key in ("id", "name", "definition") if not raw.get(key)]
    if missing:
        raise VocabularyError(
            f"{category}[{index}] is missing required fields: {', '.join(missing)}"
        )
    term_id = raw["id"]
    if not isinstance(term_id, str) or term_id.strip() != term_id:
        raise VocabularyError(f"{category}[{index}].id must be a trimmed string")
    metadata = {k: v for k, v in raw.items() if k not in {"id", "name", "definition"}}
    return VocabularyTerm(term_id, raw["name"], raw["definition"], metadata)


def parse_vocabulary(data: Any) -> Vocabulary:
    if not isinstance(data, dict) or not data:
        raise VocabularyError("vocabulary document must be a non-empty mapping")

    categories: dict[str, dict[str, VocabularyTerm]] = {}
    for category, raw_terms in data.items():
        if not isinstance(raw_terms, list) or not raw_terms:
            raise VocabularyError(f"{category!r} must contain a non-empty list")
        terms: dict[str, VocabularyTerm] = {}
        for index, raw in enumerate(raw_terms):
            term = _validate_term(category, raw, index)
            if term.id in terms:
                raise VocabularyError(f"duplicate {category} vocabulary value: {term.id!r}")
            terms[term.id] = term
        categories[category] = terms
    return Vocabulary(categories)


def load_vocabulary(path: Path | str = VOCABULARY_PATH) -> Vocabulary:
    with open(path, "r", encoding="utf-8") as handle:
        return parse_vocabulary(yaml.safe_load(handle))
