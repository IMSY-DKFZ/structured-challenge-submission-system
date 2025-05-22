# backend/BMC_API/src/api/application.py

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from BMC_API.src.api.exception_handlers import register_exception_handlers
from BMC_API.src.api.middleware.no_cache_middleware import NoCacheMiddleware
from BMC_API.src.api.routes.router import api_router
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.lifetime import lifespan
from BMC_API.src.core.logging.logging import configure_logging

API_PREFIX = settings.api_prefix

def custom_rate_limit_exceeded_handler(
    request: Request,
    exc: RateLimitExceeded,
) -> Response:
    """
    Handles rate limit exceeded exceptions by returning a custom JSON response.

    This function is used as an exception handler for RateLimitExceeded exceptions that hides the details of the rate limit.
    It returns a JSON response with a 429 status code and a message indicating that the rate limit has been exceeded.
    Inherited from "slowapi._rate_limit_exceeded_handler"

    Args:
        request (Request): The current request object.
        exc (RateLimitExceeded): The RateLimitExceeded exception that was raised.

    Returns:
        Response: A JSON response with a 429 status code and a message indicating that the rate limit has been exceeded.
    """

    return UJSONResponse({"error": "Rate limit exceeded."}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    # 1. Configure logging
    configure_logging()

    # 2. Define application parameters
    app = FastAPI(
        title="Challenge Submission System API",
        # version=metadata.version("BMC_API"),
        version="2.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )


    # 3. Register exception handlers
    register_exception_handlers(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix=API_PREFIX)

    # 4. Manage CORS (Cross-Origin Resource Sharing)

    origins = [
        "https://www.biomedical-challenges.org",
        "http://localhost:5000", # Allow access from local access to /api/docs
        "http://localhost:5173", # Allow access from local access to frontend
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=("Content-Disposition", "Content-Type", "X-Content-Filename"),
    )

    # 5. Disable caching to guarantee  serving latest version
    app.add_middleware(NoCacheMiddleware)

    # 6. Add global rate limiter
    """
    Do not forget to add request: Request to all endpoint functions.

    If you want to exempt a route from the global limit,
    put @limiter.exempt decorator between route decorator
    and function just like this:

    @app.route("/someroute")
    @limiter.exempt
    def t(request: Request):
        return PlainTextResponse("I'm unlimited")

    """
    limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)  # type: ignore
    app.add_middleware(SlowAPIMiddleware)

    return app
