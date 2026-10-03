"""Вхідний адаптер: профілі людей (ведучі/гості) для переходу з картки епізоду/подкасту."""
from fastapi import APIRouter, Depends
from adapters.in_web.dto import PersonDTO, EpisodeDTO
from application.queries.get_person_profile_query import GetPersonProfileQuery, GetPersonProfileHandler

router = APIRouter(prefix="/api/people", tags=["people"])


@router.get("/{person_id}")
async def person_profile(
    person_id: str,
    handler: GetPersonProfileHandler = Depends(),
):
    raise NotImplementedError("stub")
