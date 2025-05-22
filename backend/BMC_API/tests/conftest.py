from datetime import datetime
from typing import Any, AsyncGenerator

import pytest
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from fastapi_mail import FastMail
from httpx import ASGITransport, AsyncClient
from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from BMC_API.src.api.application import get_app
from BMC_API.src.application.interfaces.password_hasher_impl import BcryptPasswordHasher
from BMC_API.src.core.config.settings import settings
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.infrastructure.external_services.email.email_service import (
    conf,
    get_fast_mail,
)
from BMC_API.src.infrastructure.external_services.redis.dependency import get_redis_pool
from BMC_API.src.infrastructure.persistence.dependencies import get_db_session
from BMC_API.src.infrastructure.persistence.utils import create_database, drop_database


# Fixtures defined here for general usage
@pytest.fixture(scope="session")
def database_url() -> str:
    """
    Get database url.

    :return: database url.
    """
    # DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    DATABASE_URL = str(settings.db_url)
    return DATABASE_URL


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="function")
async def _engine(database_url: Any) -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from BMC_API.src.domain.entities import load_all_models  # noqa: WPS433
    from BMC_API.src.infrastructure.persistence.meta import meta  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    # await create_initial_data()

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database(database_url)


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    # trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        # await session.rollback()
        await connection.close()


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


# Arrange test mail setup
@pytest.fixture(scope="session")
def fast_mail_mock():
    fm = FastMail(conf)
    fm.config.SUPPRESS_SEND = 1
    return fm


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
    fast_mail_mock: FastMail,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    application.dependency_overrides[get_fast_mail] = lambda: fast_mail_mock
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.
    """
    # Create a test transport that works with FastAPI directly
    app = fastapi_app
    base_url = "http://test"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url,
    ) as ac:
        yield ac


@pytest.fixture
def login_user_factory(fastapi_app, client, dbsession, confirmed_user):
    """
    Factory fixture that returns a function to log in any user and return an access token.
    Ensures user is created in DB with email confirmed.
    """

    async def _login_user(user_dto):
        password_hasher = BcryptPasswordHasher()
        hashed_password = password_hasher.hash(user_dto.password)

        user_data = user_dto.model_dump()
        user_data["password"] = hashed_password

        user = UserModel.create_new(**user_data)
        user.created_time = datetime.now()
        user.modified_time = datetime.now()

        dbsession.add(user)
        await dbsession.commit()
        await dbsession.refresh(user)

        login_data = {"username": user.email, "password": user_dto.password}
        login_url = fastapi_app.url_path_for("login_route")
        login_response = await client.post(login_url, data=login_data)

        assert login_response.status_code == 200, login_response.text
        return login_response.json()["access_token"]

    return _login_user
