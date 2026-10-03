"""DTO (pydantic-моделі) для FastAPI — межа Presentation <-> Application."""
from datetime import date, datetime
from pydantic import BaseModel


class PodcastDTO(BaseModel):
    show_id: str
    show_title: str
    topics: list[str]


class EpisodeDTO(BaseModel):
    episode_id: str
    show_id: str
    title: str
    duration_sec: int
    published: date
    language: str
    description: str


class PersonDTO(BaseModel):
    person_id: str
    name: str


class PodcastCardDTO(BaseModel):
    podcast: PodcastDTO
    hosts: list[PersonDTO]
    episodes: list[EpisodeDTO]


class IngestEpisodeRequest(BaseModel):
    """Тіло POST /ingest від скрипта-генератора (один JSONL-рядок)."""
    episode: EpisodeDTO
    guest_ids: list[str]


class IngestBatchRequest(BaseModel):
    episodes: list[EpisodeDTO]


class SearchRequestDTO(BaseModel):
    q: str
    topic: str | None = None
    language: str | None = None
    page: int = 0
    size: int = 20


class SearchResultDTO(BaseModel):
    episode_id: str
    title: str
    score: float
    snippets: list[str]


class RecommendationRequestDTO(BaseModel):
    episode_id: str
    limit: int = 5


class GeneratorSettingsDTO(BaseModel):
    rate_per_second: int   # 10..5000
    running: bool


class StatsDTO(BaseModel):
    generated_total: int
    saved_to_mongo: int
    indexed_in_es: int
    search_total: int
    search_found: int
    search_empty: int
    write_rps: float
