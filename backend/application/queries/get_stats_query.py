"""Query: знімок статистики для SSE-панелі моніторингу UI."""
from dataclasses import dataclass
from application.ports.stats_service import IStatsService
from domain.models import SystemStats


@dataclass
class GetStatsQuery:
    pass


class GetStatsHandler:
    def __init__(self, stats: IStatsService):
        self._stats = stats

    async def handle(self, query: GetStatsQuery) -> SystemStats:
        raise NotImplementedError("stub")
