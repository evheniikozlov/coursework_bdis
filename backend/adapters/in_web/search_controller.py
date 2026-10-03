"""Вхідний адаптер: Query API — обслуговує UI (Рис.1: 'Query API GET /search')."""
from fastapi import APIRouter, Depends
from adapters.in_web.dto import (
    SearchRequestDTO, SearchResultDTO, RecommendationRequestDTO, PodcastCardDTO,
)
from application.queries.search_episodes_query import SearchEpisodesQuery, SearchEpisodesHandler
from application.queries.get_recommendations_query import GetRecommendationsQuery, GetRecommendationsHandler
from application.queries.get_podcast_card_query import GetPodcastCardQuery, GetPodcastCardHandler

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search", response_model=list[SearchResultDTO])
async def search_episodes(
    req: SearchRequestDTO = Depends(),
    handler: SearchEpisodesHandler = Depends(),
):
    raise NotImplementedError("stub")


@router.get("/episodes/{episode_id}/recommendations", response_model=list[SearchResultDTO])
async def recommendations(
    episode_id: str,
    limit: int = 5,
    handler: GetRecommendationsHandler = Depends(),
):
    raise NotImplementedError("stub")


@router.get("/podcasts/{show_id}", response_model=PodcastCardDTO)
async def podcast_card(
    show_id: str,
    handler: GetPodcastCardHandler = Depends(),
):
    raise NotImplementedError("stub")
