"""Вихідний порт: шар кешування пошукових результатів (реалізує Redis-адаптер)."""
from abc import ABC, abstractmethod
from typing import Optional
from domain.models import SearchHit


class ICacheService(ABC):
    @abstractmethod
    async def get_search_result(self, normalized_key: str) -> Optional[list[SearchHit]]: ...

    @abstractmethod
    async def put_search_result(self, normalized_key: str, hits: list[SearchHit], ttl_seconds: int) -> None: ...

    @abstractmethod
    async def invalidate(self, normalized_key: str) -> None: ...
