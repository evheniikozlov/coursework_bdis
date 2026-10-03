"""Вхідний адаптер: SSE-стрім статистики раз на секунду для веб-панелі моніторингу."""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from application.queries.get_stats_query import GetStatsQuery, GetStatsHandler

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/stream")
async def stats_stream(handler: GetStatsHandler = Depends()) -> StreamingResponse:
    """async generator: раз на секунду handler.handle(...) -> SSE 'data: {...}\n\n'."""
    raise NotImplementedError("stub")


@router.get("/searches/recent")
async def recent_searches():
    raise NotImplementedError("stub")
