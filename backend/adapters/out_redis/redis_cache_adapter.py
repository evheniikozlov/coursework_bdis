"""Вихідний адаптер: Redis Async Adapter (Рис.1) — шар кешування пошукових результатів."""
from typing import Optional
from application.ports.cache_service import ICacheService
from domain.models import SearchHit


class RedisCacheAdapter(ICacheService):
    def __init__(self, redis_client):
        self._redis = redis_client  # redis.asyncio.Redis
        self._key_prefix = "search:"

    async def get_search_result(self, normalized_key: str) -> Optional[list[SearchHit]]:
        raise NotImplementedError("stub")

    async def put_search_result(self, normalized_key: str, hits: list[SearchHit], ttl_seconds: int) -> None:
        raise NotImplementedError("stub")

    async def invalidate(self, normalized_key: str) -> None:
        raise NotImplementedError("stub")
