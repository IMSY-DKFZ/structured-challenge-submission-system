"""backend models."""

import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="BMC_API.src.domain.entities.",
    )
    for module in modules:
        __import__(module.name)  # noqa: WPS421


load_all_models()
