"""Вхідний адаптер: панель керування швидкістю генератора (слайдер UI)."""
from fastapi import APIRouter, Depends
from adapters.in_web.dto import GeneratorSettingsDTO
from application.commands.update_generator_rate_command import (
    UpdateGeneratorRateCommand, UpdateGeneratorRateHandler,
)

router = APIRouter(prefix="/api/generator", tags=["generator"])


@router.put("", response_model=GeneratorSettingsDTO)
async def update_rate(
    settings: GeneratorSettingsDTO,
    handler: UpdateGeneratorRateHandler = Depends(),
):
    raise NotImplementedError("stub")


@router.get("", response_model=GeneratorSettingsDTO)
async def current_rate():
    raise NotImplementedError("stub")
