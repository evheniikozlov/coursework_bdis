"""Вхідний адаптер: Command API — приймає дані від генератора (Рис.1: 'Command API POST /ingest')."""
from fastapi import APIRouter, Depends
from adapters.in_web.dto import IngestEpisodeRequest, IngestBatchRequest, EpisodeDTO, PodcastDTO
from application.commands.ingest_episode_command import IngestEpisodeCommand, IngestEpisodeHandler
from application.commands.ingest_batch_command import IngestBatchCommand, IngestBatchHandler
from application.commands.ingest_podcast_command import IngestPodcastCommand, IngestPodcastHandler

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/episode", response_model=EpisodeDTO)
async def ingest_episode(
    request: IngestEpisodeRequest,
    handler: IngestEpisodeHandler = Depends(),
):
    raise NotImplementedError("stub")


@router.post("/episodes/batch")
async def ingest_batch(
    request: IngestBatchRequest,
    handler: IngestBatchHandler = Depends(),
):
    raise NotImplementedError("stub")


@router.post("/podcast", response_model=PodcastDTO)
async def ingest_podcast(
    podcast: PodcastDTO,
    host_ids: list[str],
    handler: IngestPodcastHandler = Depends(),
):
    raise NotImplementedError("stub")
