"""Command: пакетний ingest потоку JSONL від генератора (bulk-запис для високого RPS)."""
from dataclasses import dataclass
from application.ports.document_repository import IDocumentRepository
from application.ports.search_repository import ISearchRepository
from application.ports.stats_service import IStatsService
from domain.models import Episode


@dataclass
class IngestBatchCommand:
    episodes: list[Episode]


class IngestBatchHandler:
    def __init__(self, documents: IDocumentRepository, search: ISearchRepository, stats: IStatsService):
        self._documents = documents
        self._search = search
        self._stats = stats

    async def handle(self, command: IngestBatchCommand) -> None:
        """bulk_save_episodes (Mongo) + bulk_index_episodes (ES), одним awaitable через asyncio.gather."""
        raise NotImplementedError("stub")
