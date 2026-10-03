"""Command: зміна швидкості генератора зі слайдера UI (10..5000 записів/сек)."""
from dataclasses import dataclass
from application.ports.stats_service import IStatsService
from domain.models import GeneratorSettings


@dataclass
class UpdateGeneratorRateCommand:
    rate_per_second: int
    running: bool


class UpdateGeneratorRateHandler:
    def __init__(self, stats: IStatsService):
        self._stats = stats

    async def handle(self, command: UpdateGeneratorRateCommand) -> GeneratorSettings:
        """Записує нове налаштування у Redis (shared state), яке читає скрипт-генератор перед кожним batch."""
        raise NotImplementedError("stub")
