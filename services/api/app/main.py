from __future__ import annotations

from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .internal_auth import require_ops
from .routers.internal import router as internal_ops, login_router
from . import audit  # register transactional audit/task listeners
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
    application.state.config = config
    @application.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError):
        # FastAPI normally echoes invalid input, including password fields.
        return JSONResponse(status_code=422,content={'detail':[{'loc':list(e['loc']),'msg':e['msg'],'type':e['type']} for e in error.errors()]})
    @application.middleware('http')
    async def internal_headers(request, call_next):
        response = await call_next(request)
        if request.url.path.startswith('/ops'):
            response.headers['Cache-Control']='no-store'
            response.headers['X-Content-Type-Options']='nosniff'
        return response
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
    # Hosted Operations remains an explicit deployment opt-in.
    if config.environment == 'development' or config.ops_enabled:
        application.include_router(login_router)
        for router in (internal_ops, foundation_ops, ops.router, booking_ops, availability_ops, payment_ops):
            application.include_router(router, dependencies=[Depends(require_ops)])
    application.add_api_route('/', health, response_model=HealthResponse, methods=['GET'])
    application.add_api_route('/health', health, response_model=HealthResponse, methods=['GET'])
    return application


async def health() -> HealthResponse:
    return HealthResponse(status='ok', service='volcan-vacations-api')


app = create_app()
