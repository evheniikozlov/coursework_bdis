"""Query: рекомендації на основі перетину гостей (графові запити Neo4j)."""
from dataclasses import dataclass
from application.ports.graph_repository import IGraphRepository
from application.ports.document_repository import IDocumentRepository
from domain.models import Episode


@dataclass
class GetRecommendationsQuery:
    episode_id: str
    limit: int = 5


class GetRecommendationsHandler:
    def __init__(self, graph: IGraphRepository, documents: IDocumentRepository):
        self._graph = graph
        self._documents = documents

    async def handle(self, query: GetRecommendationsQuery) -> list[Episode]:
        """graph.recommend_by_shared_guests -> documents.get_episode для кожного id."""
        raise NotImplementedError("stub")
