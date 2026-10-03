"""Вихідний порт: повнотекстовий пошук (реалізує Elasticsearch/OpenSearch-адаптер)."""
from abc import ABC, abstractmethod
from domain.models import Episode, SearchQuery, SearchHit


class ISearchRepository(ABC):
    @abstractmethod
    async def index_episode(self, episode: Episode) -> None: ...

    @abstractmethod
    async def bulk_index_episodes(self, episodes: list[Episode]) -> None: ...

    @abstractmethod
    async def search(self, query: SearchQuery) -> list[SearchHit]:
        """Пошук з підсвічуванням (highlight/snippets) по інвертованому індексу."""
        ...

    @abstractmethod
    async def delete_episode(self, episode_id: str) -> None: ...
