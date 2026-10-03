"""Вихідний адаптер: лічильники статистики (INCR) та журнал останніх пошукових запитів у Redis."""
from datetime import datetime
from application.ports.stats_service import IStatsService
from domain.models import SystemStats


class RedisStatsAdapter(IStatsService):
    def __init__(self, redis_client):
        self._redis = redis_client

    async def increment_generated(self, n: int = 1) -> None:
        raise NotImplementedError("stub")

    async def increment_saved(self, n: int = 1) -> None:
        raise NotImplementedError("stub")

    async def log_search(self, query_text: str, found: bool, at: datetime) -> None:
        raise NotImplementedError("stub")

    async def recent_searches(self, limit: int) -> list[tuple[str, bool, datetime]]:
        raise NotImplementedError("stub")

    async def snapshot(self) -> SystemStats:
        raise NotImplementedError("stub")
