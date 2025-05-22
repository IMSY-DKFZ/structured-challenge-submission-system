import platform

import uvicorn

from BMC_API.src.core.config.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    if settings.reload or platform.system() == "Windows":
        uvicorn.run(
            "BMC_API.src.api.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doesn't work with Uvicorn workers.
        from BMC_API.src.api.gunicorn_runner import GunicornApplication

        GunicornApplication(
            "BMC_API.src.api.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',  # noqa: WPS323
        ).run()


if __name__ == "__main__":
    # import cProfile, pstats

    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.dump_stats("API_profile")
