from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, settings
from .schemas import HealthResponse
from .routers import ops, public
from .routers.foundation import router as foundation_ops
from .routers.payments import ops_router as payment_ops, public_router as payment_public, webhook_router
from .routers.availability import ops_router as availability_ops, public_router as availability_public
from .routers.bookings import public_router as booking_public, ops_router as booking_ops

def create_app(config: Settings = settings) -> FastAPI:
    application = FastAPI(
        title='Volcan Vacations API',
        description='Backend API for the Volcan Vacations platform.',
        version='0.1.0',
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins_list,
        allow_origin_regex=config.allowed_origin_regex or None,
        allow_credentials=config.environment == 'development',
        allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['Content-Type', 'Authorization'],
    )
    application.include_router(public.router)
    application.include_router(booking_public)
    application.include_router(availability_public)
    application.include_router(payment_public)
    application.include_router(webhook_router)
    # CORS is not authentication. Do not mount private data or mutation routes
    # on the internet-facing API until Operations authentication is implemented.
    if config.environment == 'development':
        application.include_router(foundation_ops)
        application.include_router(ops.router)
        application.include_router(booking_ops)
        application.include_router(availability_ops)
        application.include_router(payment_ops)
    application.add_api_route('/', health, response_model=HealthResponse, methods=['GET'])
    application.add_api_route('/health', health, response_model=HealthResponse, methods=['GET'])
    return application


async def health() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')


app = create_app()
