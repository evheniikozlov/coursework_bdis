"""Вихідний адаптер: MongoDB Async Adapter (Рис.1) на базі motor.
Колекції: podcasts, episodes. Шардінг: shard key = show_id (або year), 3 ноди.
"""
from typing import Optional
from application.ports.document_repository import IDocumentRepository
from domain.models import Podcast, Episode


class MongoDocumentAdapter(IDocumentRepository):
    def __init__(self, client):
        self._db = client  # motor.motor_asyncio.AsyncIOMotorDatabase

    async def save_podcast(self, podcast: Podcast) -> Podcast:
        raise NotImplementedError("stub")

    async def get_podcast(self, show_id: str) -> Optional[Podcast]:
        raise NotImplementedError("stub")

    async def list_podcasts(self, topic: Optional[str], page: int, size: int) -> list[Podcast]:
        raise NotImplementedError("stub")

    async def delete_podcast(self, show_id: str) -> None:
        raise NotImplementedError("stub")

    async def save_episode(self, episode: Episode) -> Episode:
        raise NotImplementedError("stub")

    async def get_episode(self, episode_id: str) -> Optional[Episode]:
        raise NotImplementedError("stub")

    async def list_episodes_by_show(self, show_id: str, page: int, size: int) -> list[Episode]:
        raise NotImplementedError("stub")

    async def bulk_save_episodes(self, episodes: list[Episode]) -> None:
        """insert_many(..., ordered=False) для максимальної швидкості запису."""
        raise NotImplementedError("stub")

    async def delete_episode(self, episode_id: str) -> None:
        raise NotImplementedError("stub")
