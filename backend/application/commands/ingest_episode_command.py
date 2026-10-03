"""Command: прийом одного епізоду від генератора і паралельний запис у Mongo + ES + Neo4j."""
from dataclasses import dataclass
from application.ports.document_repository import IDocumentRepository
from application.ports.search_repository import ISearchRepository
from application.ports.graph_repository import IGraphRepository
from application.ports.stats_service import IStatsService
from domain.models import Episode, Person


@dataclass
class IngestEpisodeCommand:
    episode: Episode
    guest_ids: list[str]   # person_id гостей цього епізоду


class IngestEpisodeHandler:
    def __init__(
        self,
        documents: IDocumentRepository,
        search: ISearchRepository,
        graph: IGraphRepository,
        stats: IStatsService,
    ):
        self._documents = documents
        self._search = search
        self._graph = graph
        self._stats = stats

    async def handle(self, command: IngestEpisodeCommand) -> Episode:
        """1) save_episode (Mongo) 2) index_episode (ES) 3) link_guest для кожного гостя (Neo4j) 4) increment_saved."""
        raise NotImplementedError("stub")
