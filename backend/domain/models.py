"""Domain Layer — чисті бізнес-моделі, без залежностей від БД чи FastAPI."""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Podcast:
    show_id: str
    show_title: str
    topics: list[str] = field(default_factory=list)  # напр. ["ml", "startups"]


@dataclass(frozen=True)
class Episode:
    episode_id: str
    show_id: str
    title: str
    duration_sec: int
    published: date
    language: str          # "uk" | "en"
    description: str       # об'ємний текст -> індексується в Elasticsearch


@dataclass(frozen=True)
class Person:
    """Єдиний пул осіб: та ж людина може бути ведучим одного шоу і гостем іншого епізоду."""
    person_id: str
    name: str


@dataclass(frozen=True)
class SearchQuery:
    text: str
    topic: Optional[str] = None
    language: Optional[str] = None
    page: int = 0
    size: int = 20

    def normalized_key(self) -> str:
        """lower-case + сортування слів -> єдиний ключ кешу Redis."""
        raise NotImplementedError("stub")


@dataclass(frozen=True)
class SearchHit:
    episode_id: str
    title: str
    score: float
    snippets: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GeneratorSettings:
    rate_per_second: int   # 10..5000
    running: bool


@dataclass(frozen=True)
class SystemStats:
    generated_total: int
    saved_to_mongo: int
    indexed_in_es: int
    search_total: int
    search_found: int
    search_empty: int
    write_rps: float
