"""Query: картка подкасту + список ведучих + список епізодів."""
from dataclasses import dataclass
from application.ports.document_repository import IDocumentRepository
from application.ports.graph_repository import IGraphRepository
from domain.models import Podcast, Person, Episode


@dataclass
class PodcastCard:
    podcast: Podcast
    hosts: list[Person]
    episodes: list[Episode]


@dataclass
class GetPodcastCardQuery:
    show_id: str
    page: int = 0
    size: int = 20


class GetPodcastCardHandler:
    def __init__(self, documents: IDocumentRepository, graph: IGraphRepository):
        self._documents = documents
        self._graph = graph

    async def handle(self, query: GetPodcastCardQuery) -> PodcastCard:
        raise NotImplementedError("stub")
