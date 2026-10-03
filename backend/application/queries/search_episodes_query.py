"""Query: повнотекстовий пошук з нормалізацією ключа та Redis-кешем."""
from dataclasses import dataclass
from application.ports.search_repository import ISearchRepository
from application.ports.cache_service import ICacheService
from application.ports.stats_service import IStatsService
from domain.models import SearchQuery, SearchHit


@dataclass
class SearchEpisodesQuery:
    query: SearchQuery


class SearchEpisodesHandler:
    def __init__(self, search: ISearchRepository, cache: ICacheService, stats: IStatsService):
        self._search = search
        self._cache = cache
        self._stats = stats

    async def handle(self, query: SearchEpisodesQuery) -> list[SearchHit]:
        """normalize -> cache.get -> (hit: return) / (miss: search.search -> cache.put) -> stats.log_search."""
        raise NotImplementedError("stub")
