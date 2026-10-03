"""Вихідний адаптер: Graph Async Adapter (Рис.1) на базі neo4j (AsyncDriver).
Вузли: Person, Podcast, Episode. Ребра: (Person)-[:VEDE]->(Podcast), (Person)-[:VYSTUPYV_U]->(Episode).
"""
from application.ports.graph_repository import IGraphRepository
from domain.models import Person


class Neo4jGraphAdapter(IGraphRepository):
    def __init__(self, driver):
        self._driver = driver  # neo4j.AsyncDriver

    async def upsert_person(self, person: Person) -> Person:
        raise NotImplementedError("stub")

    async def link_host(self, person_id: str, show_id: str) -> None:
        raise NotImplementedError("stub")

    async def link_guest(self, person_id: str, episode_id: str) -> None:
        raise NotImplementedError("stub")

    async def get_hosts_of_show(self, show_id: str) -> list[Person]:
        raise NotImplementedError("stub")

    async def get_guests_of_episode(self, episode_id: str) -> list[Person]:
        raise NotImplementedError("stub")

    async def get_episodes_of_person(self, person_id: str) -> list[str]:
        raise NotImplementedError("stub")

    async def recommend_by_shared_guests(self, episode_id: str, limit: int) -> list[str]:
        """MATCH (e1:Episode {episode_id:$id})<-[:VYSTUPYV_U]-(p)-[:VYSTUPYV_U]->(e2) RETURN e2 ..."""
        raise NotImplementedError("stub")
