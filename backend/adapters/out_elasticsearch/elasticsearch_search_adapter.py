"""Вихідний адаптер: Elasticsearch Async Adapter (Рис.1).
Індекс: episodes_text (поле description, analyzer з підтримкою укр./англ.), highlight -> snippets.
"""
from application.ports.search_repository import ISearchRepository
from domain.models import Episode, SearchQuery, SearchHit


class ElasticsearchSearchAdapter(ISearchRepository):
    def __init__(self, client, index_name: str = "episodes_text"):
        self._client = client  # elasticsearch.AsyncElasticsearch
        self._index = index_name

    async def index_episode(self, episode: Episode) -> None:
        raise NotImplementedError("stub")

    async def bulk_index_episodes(self, episodes: list[Episode]) -> None:
        raise NotImplementedError("stub")

    async def search(self, query: SearchQuery) -> list[SearchHit]:
        raise NotImplementedError("stub")

    async def delete_episode(self, episode_id: str) -> None:
        raise NotImplementedError("stub")
