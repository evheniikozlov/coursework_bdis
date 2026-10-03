"""Вихідний порт: лічильники та лог пошуків для панелі моніторингу UI."""
from abc import ABC, abstractmethod
from datetime import datetime
from domain.models import SystemStats


class IStatsService(ABC):
    @abstractmethod
    async def increment_generated(self, n: int = 1) -> None: ...

    @abstractmethod
    async def increment_saved(self, n: int = 1) -> None: ...

    @abstractmethod
    async def log_search(self, query_text: str, found: bool, at: datetime) -> None: ...

    @abstractmethod
    async def recent_searches(self, limit: int) -> list[tuple[str, bool, datetime]]: ...

    @abstractmethod
    async def snapshot(self) -> SystemStats: ...
