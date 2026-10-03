"""Мапінг DTO <-> domain-моделі (межа презентаційного шару)."""
from domain.models import Podcast, Episode, Person, SearchQuery, SearchHit, GeneratorSettings, SystemStats
from adapters.in_web.dto import (
    PodcastDTO, EpisodeDTO, PersonDTO, SearchRequestDTO, SearchResultDTO,
    GeneratorSettingsDTO, StatsDTO,
)


def episode_to_dto(episode: Episode) -> EpisodeDTO:
    raise NotImplementedError("stub")


def dto_to_episode(dto: EpisodeDTO) -> Episode:
    raise NotImplementedError("stub")


def podcast_to_dto(podcast: Podcast) -> PodcastDTO:
    raise NotImplementedError("stub")


def person_to_dto(person: Person) -> PersonDTO:
    raise NotImplementedError("stub")


def search_request_to_query(req: SearchRequestDTO) -> SearchQuery:
    raise NotImplementedError("stub")


def hit_to_dto(hit: SearchHit) -> SearchResultDTO:
    raise NotImplementedError("stub")


def settings_to_dto(settings: GeneratorSettings) -> GeneratorSettingsDTO:
    raise NotImplementedError("stub")


def stats_to_dto(stats: SystemStats) -> StatsDTO:
    raise NotImplementedError("stub")
