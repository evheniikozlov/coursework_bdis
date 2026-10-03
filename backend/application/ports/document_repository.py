"""Вихідний порт: CRUD доступ до основного сховища метаданих (реалізує MongoDB-адаптер)."""
from abc import ABC, abstractmethod
from typing import Optional
from domain.models import Podcast, Episode


class IDocumentRepository(ABC):
    # --- Podcasts ---
    @abstractmethod
    async def save_podcast(self, podcast: Podcast) -> Podcast: ...

    @abstractmethod
    async def get_podcast(self, show_id: str) -> Optional[Podcast]: ...

    @abstractmethod
    async def list_podcasts(self, topic: Optional[str], page: int, size: int) -> list[Podcast]: ...

    @abstractmethod
    async def delete_podcast(self, show_id: str) -> None: ...

    # --- Episodes ---
    @abstractmethod
    async def save_episode(self, episode: Episode) -> Episode: ...

    @abstractmethod
    async def get_episode(self, episode_id: str) -> Optional[Episode]: ...

    @abstractmethod
    async def list_episodes_by_show(self, show_id: str, page: int, size: int) -> list[Episode]: ...

    @abstractmethod
    async def bulk_save_episodes(self, episodes: list[Episode]) -> None:
        """Пакетний запис (bulk insert) для потоку від генератора."""
        ...

    @abstractmethod
    async def delete_episode(self, episode_id: str) -> None: ...
