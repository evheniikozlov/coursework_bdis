"""Вихідний порт: зв'язки та рекомендації (реалізує Neo4j-адаптер, або SQL-альтернативу)."""
from abc import ABC, abstractmethod
from domain.models import Person


class IGraphRepository(ABC):
    @abstractmethod
    async def upsert_person(self, person: Person) -> Person: ...

    @abstractmethod
    async def link_host(self, person_id: str, show_id: str) -> None:
        """(Person)-[:ВЕДЕ]->(Podcast)"""
        ...

    @abstractmethod
    async def link_guest(self, person_id: str, episode_id: str) -> None:
        """(Person)-[:ВИСТУПИВ_У]->(Episode)"""
        ...

    @abstractmethod
    async def get_hosts_of_show(self, show_id: str) -> list[Person]: ...

    @abstractmethod
    async def get_guests_of_episode(self, episode_id: str) -> list[Person]: ...

    @abstractmethod
    async def get_episodes_of_person(self, person_id: str) -> list[str]:
        """Усі episode_id, де ця особа була гостем чи ведучим."""
        ...

    @abstractmethod
    async def recommend_by_shared_guests(self, episode_id: str, limit: int) -> list[str]:
        """Епізоди, що мають спільних гостей з даним (перетин сутностей)."""
        ...
