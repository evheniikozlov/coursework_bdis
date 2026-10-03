"""Command: реєстрація нового подкасту та його ведучих."""
from dataclasses import dataclass
from application.ports.document_repository import IDocumentRepository
from application.ports.graph_repository import IGraphRepository
from domain.models import Podcast


@dataclass
class IngestPodcastCommand:
    podcast: Podcast
    host_ids: list[str]


class IngestPodcastHandler:
    def __init__(self, documents: IDocumentRepository, graph: IGraphRepository):
        self._documents = documents
        self._graph = graph

    async def handle(self, command: IngestPodcastCommand) -> Podcast:
        raise NotImplementedError("stub")
