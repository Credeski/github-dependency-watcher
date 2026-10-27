"""Configuration loading and validation for the dependency watcher."""

import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Config:
    """Validated settings used by the watcher."""

    repository: str
    polling_interval_seconds: int
    dependency_files: tuple[str, ...]
    github_token: str | None = None


def load_config(config_path: str | Path | None = None) -> Config:
    """Load settings from JSON and the optional project .env file."""
    load_dotenv(PROJECT_ROOT / ".env")

    path = Path(config_path) if config_path is not None else PROJECT_ROOT / "config.json"
    with path.open(encoding="utf-8") as config_file:
        raw_config = json.load(config_file)

    if not isinstance(raw_config, dict):
        raise ValueError("Configuration must be a JSON object.")

    repository = raw_config.get("repository")
    if (
        not isinstance(repository, str)
        or repository.count("/") != 1
        or any(not part.strip() for part in repository.split("/"))
    ):
        raise ValueError("'repository' must be in 'owner/name' format.")

    interval = raw_config.get("polling_interval_seconds")
    if isinstance(interval, bool) or not isinstance(interval, int) or interval <= 0:
        raise ValueError("'polling_interval_seconds' must be a positive integer.")

    dependency_files = raw_config.get("dependency_files")
    if (
        not isinstance(dependency_files, list)
        or not dependency_files
        or any(not isinstance(item, str) or not item.strip() for item in dependency_files)
    ):
        raise ValueError("'dependency_files' must be a non-empty list of paths.")

    return Config(
        repository=repository,
        polling_interval_seconds=interval,
        dependency_files=tuple(dependency_files),
        github_token=os.environ.get("GITHUB_TOKEN") or None,
    )
