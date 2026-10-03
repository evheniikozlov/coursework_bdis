"""Composition Root: збирає FastAPI app, монтує контролери, конфігурує DI (порти -> адаптери)."""
from fastapi import FastAPI
from adapters.in_web import (
    ingest_controller, search_controller, person_controller,
    generator_controller, stats_controller,
)

app = FastAPI(title="Podcast Platform API")

app.include_router(ingest_controller.router)
app.include_router(search_controller.router)
app.include_router(person_controller.router)
app.include_router(generator_controller.router)
app.include_router(stats_controller.router)

# TODO: DI-контейнер (dependency-injector / FastAPI Depends override) -> прив'язати
# MongoDocumentAdapter, ElasticsearchSearchAdapter, Neo4jGraphAdapter, RedisCacheAdapter/RedisStatsAdapter
# до відповідних портів і command/query handlers.
