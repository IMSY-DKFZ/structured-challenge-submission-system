import enum
import os
from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())
ROOT_DIR = Path(__file__).resolve().parents[3]


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "localhost"
    port: int = 5000
    base_url: str = "localhost"
    api_prefix: str = "/api/v2"
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = True

    # Current environment
    environment: str = "dev"
    root_dir: str = str(ROOT_DIR)

    # log_level: LogLevel = LogLevel.INFO
    log_level: LogLevel = LogLevel.DEBUG
    log_folder: str = os.path.join(ROOT_DIR, "logs")

    submissions_folder: str = os.path.join(ROOT_DIR, "outputs", "generatedPdfs")
    backup_folder: str = os.path.join(ROOT_DIR, "backups")

    # Periodic tasks
    db_file_backup_period_in_sec: int # Defined in .env file
    db_file_backups_clean_period_in_sec: int # Defined in .env file
    db_file_backups_age_limit_in_day: int # Defined in .env file


    # Variables for the database
    db_file: Path =  "./database/database.sqlite3"
    
    db_echo: bool = False

    # Rate limiter value
    rate_limit: str # Defined in .env file

    # Variables for Redis
    redis_host: str = "localhost"  # --> testing on local machine
    # redis_host: str = "host.docker.internal"  # --> Production setting
    redis_port: int = 6379
    redis_user: str | None = None
    redis_pass: str | None = None
    redis_base: str | None = None

    # Secret information. All of them are defined in .env file
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    DEFAULT_ADMIN_NAME: str
    DEFAULT_ADMIN_PASSWORD: str
    DEFAULT_TEST_USER_NAME: str
    DEFAULT_TEST_USER_PASSWORD: str

    # Email service. All of them are defined in .env file
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    # Grpc endpoint for opentelemetry.
    # E.G. http://localhost:4317
    opentelemetry_endpoint: str | None = None

    @property
    def db_file_abs(self) -> Path:
        return Path(ROOT_DIR).joinpath(self.db_file).resolve()

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        
        return URL.build(
            scheme="sqlite+aiosqlite",
            path="/" + str(self.db_file_abs),
            encoded=True,
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, ".env"),  # find_dotenv(".env")
        env_prefix="BMC_API_",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings():
    settings = Settings()

    # Check if .env file available
    env_file = settings.model_config.get("env_file")
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"{env_file} not found")

    # Check if .env file is readable
    if not os.access(env_file, os.R_OK):
        raise PermissionError(f"{env_file} is not readable")

    return settings


settings = get_settings()
