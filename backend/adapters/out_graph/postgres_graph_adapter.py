"""Альтернативний вихідний адаптер: реляційна реалізація IGraphRepository (asyncpg),
якщо замість Neo4j обрано PostgreSQL зі звичайними FK та індексами (описано в звіті як 'альтернатива')."""
from application.ports.graph_repository import IGraphRepository
from domain.models import Person


class PostgresGraphAdapter(IGraphRepository):
    def __init__(self, pool):
        self._pool = pool  # asyncpg.Pool

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
        """SELECT ... через self-join таблиці guest_episode за спільним person_id (важчий за Neo4j-запит)."""
        raise NotImplementedError("stub")
