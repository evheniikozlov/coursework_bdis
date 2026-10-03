"""Query: профіль особи (ведучий і/або гість) та всі епізоди, де вона фігурує."""
from dataclasses import dataclass
from application.ports.graph_repository import IGraphRepository
from application.ports.document_repository import IDocumentRepository
from domain.models import Person, Episode


@dataclass
class PersonProfile:
    person: Person
    episodes: list[Episode]


@dataclass
class GetPersonProfileQuery:
    person_id: str


class GetPersonProfileHandler:
    def __init__(self, graph: IGraphRepository, documents: IDocumentRepository):
        self._graph = graph
        self._documents = documents

    async def handle(self, query: GetPersonProfileQuery) -> PersonProfile:
        """graph.get_episodes_of_person -> documents.get_episode для кожного id."""
        raise NotImplementedError("stub")
