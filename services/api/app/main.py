from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import HealthResponse
from .routers import ops, public
from .routers.payments import ops_router as payment_ops, public_router as payment_public, webhook_router
from .routers.availability import ops_router as availability_ops, public_router as availability_public
from .routers.bookings import public_router as booking_public, ops_router as booking_ops

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

app.include_router(public.router)
app.include_router(ops.router)
app.include_router(booking_public)
app.include_router(booking_ops)
app.include_router(availability_ops)
app.include_router(availability_public)
app.include_router(payment_ops)
app.include_router(payment_public)
app.include_router(webhook_router)


@app.get('/', response_model=HealthResponse)
async def root() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')


@app.get('/health', response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')
