
# backend/BMC_API/src/core/lifetime.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_utilities import repeat_every
from loguru import logger
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    TELEMETRY_SDK_LANGUAGE,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from BMC_API.src.core.config.settings import settings
from BMC_API.src.infrastructure.external_services.redis.lifetime import (
    init_redis,
    shutdown_redis,
)
from BMC_API.src.infrastructure.persistence.dependencies import (
    backup_database,
    clean_database_backups,
)
from BMC_API.src.initial_data import create_initial_data


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(
        str(settings.db_url), echo=settings.db_echo, echo_pool=False
    )
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def setup_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    tracer_provider = TracerProvider(
        resource=Resource(
            attributes={
                SERVICE_NAME: "backend",
                TELEMETRY_SDK_LANGUAGE: "python",
                DEPLOYMENT_ENVIRONMENT: settings.environment,
            },
        ),
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=settings.opentelemetry_endpoint,
                insecure=True,
            ),
        ),
    )

    excluded_endpoints = [
        app.url_path_for("health_check"),
        app.url_path_for("openapi"),
        app.url_path_for("swagger_ui_html"),
        app.url_path_for("swagger_ui_redirect"),
        app.url_path_for("redoc_html"),
    ]

    FastAPIInstrumentor().instrument_app(
        app,
        tracer_provider=tracer_provider,
        excluded_urls=",".join(excluded_endpoints),
    )
    RedisInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
    SQLAlchemyInstrumentor().instrument(
        tracer_provider=tracer_provider,
        engine=app.state.db_engine.sync_engine,
    )

    set_tracer_provider(tracer_provider=tracer_provider)


def stop_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Disables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    FastAPIInstrumentor().uninstrument_app(app)
    RedisInstrumentor().uninstrument()
    SQLAlchemyInstrumentor().uninstrument()


@repeat_every(seconds=settings.db_file_backup_period_in_sec, logger=logger)
async def backup_database_task():
    logger.info("backup_database (periodic job) started.")
    await backup_database()
    logger.info("backup_database (periodic job) completed.")

@repeat_every(seconds=settings.db_file_backups_clean_period_in_sec, logger=logger)
async def clean_database_backups_task():
    logger.info("clean_database_backups (periodic job) started.")
    await clean_database_backups(age_limit=settings.db_file_backups_age_limit_in_day)
    logger.info("clean_database_backups (periodic job) completed.")
    


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Actions to run on application startup.
    startup and shutdown events deprecated.
    These events updated according to latest FastAPI docs
    https://fastapi.tiangolo.com/advanced/events/
    """
    # 1. Startup actions
    logger.info(f"Server starting on root folder: {settings.root_dir}")
    _setup_db(app)
    await create_initial_data(app)
    setup_opentelemetry(app)
    init_redis(app)
    await backup_database_task()
    await clean_database_backups_task()
    logger.info("Server started successfully")
    yield
    # 2. Shutdown actions
    await app.state.db_engine.dispose()
    await shutdown_redis(app)
    stop_opentelemetry(app)
    logger.info("Server shutdown successfully")

# def register_startup_event(
#     app: FastAPI,
# ) -> Callable[[], Awaitable[None]]:  # pragma: no cover
#     """
#     Actions to run on application startup.

#     This function uses fastAPI app to store data
#     in the state, such as db_engine.

#     :param app: the fastAPI application.
#     :return: function that actually performs actions.
#     """

#     @app.on_event("startup")
#     async def _startup() -> None:  # noqa: WPS430
#         _setup_db(app)
#         await create_initial_data(app)
#         setup_opentelemetry(app)
#         init_redis(app)
#         await backup_database_task()
#         logger.info("Server started successfully")
#         pass  # noqa: WPS420

#     return _startup


# def register_shutdown_event(
#     app: FastAPI,
# ) -> Callable[[], Awaitable[None]]:  # pragma: no cover
#     """
#     Actions to run on application's shutdown.

#     :param app: fastAPI application.
#     :return: function that actually performs actions.
#     """

#     @app.on_event("shutdown")
#     async def _shutdown() -> None:  # noqa: WPS430
#         await app.state.db_engine.dispose()
#         await shutdown_redis(app)
#         stop_opentelemetry(app)
#         logger.info("Server shutdown successfully")
#         pass  # noqa: WPS420

#     return _shutdown
