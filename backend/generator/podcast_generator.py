"""Python Генератор — 'Вхідна точка' на Рис.1. Не входить у гексагональне ядро:
окремий процес, що стрімить JSONL на POST /api/ingest/episodes/batch.
Метод: шаблонна інжекція ключових слів із тематичних словників (без Faker/Markov)."""
from dataclasses import dataclass

TOPIC_DICTIONARIES: dict[str, list[str]] = {
    "ml": ["нейронна мережа", "трансформер", "градієнтний спуск"],
    "startups": ["піч-дек", "раунд інвестицій", "MVP"],
    "science": ["гіпотеза", "експеримент", "публікація"],
}

FIRST_NAMES = ["Олег", "Ірина", "Андрій", "Марія"]
LAST_NAMES = ["Коваленко", "Шевченко", "Бондаренко"]


@dataclass
class GeneratedEpisode:
    episode_id: str
    show_id: str
    title: str
    duration_sec: int
    published: str
    language: str
    description: str
    guest_ids: list[str]


class PodcastTextGenerator:
    """Генерує show_title/title/description методом шаблонної інжекції; year/show_id -> шардінг-ключ."""

    def __init__(self, rate_per_second: int = 10):
        self.rate_per_second = rate_per_second  # змінюється зі слайдера UI через /api/generator

    def generate_episode(self) -> GeneratedEpisode:
        raise NotImplementedError("stub")

    async def stream(self, sink) -> None:
        """Безкінечний цикл: await asyncio.sleep(1/self.rate_per_second) -> sink(batch)."""
        raise NotImplementedError("stub")
