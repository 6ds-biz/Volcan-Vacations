from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import HealthResponse

app = FastAPI(
    title='Volcan Vacations API',
    description='Backend API for the Volcan Vacations platform.',
    version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_origin_regex=settings.allowed_origin_regex or None,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
)


@app.get('/', response_model=HealthResponse)
async def root() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')


@app.get('/health', response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')
