"""Command-line entry point for the dependency watcher."""

import argparse
import logging
from pathlib import Path

from .config import Config, load_config


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load GitHub dependency watcher configuration.")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON configuration file (defaults to config.json).",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config: Config = load_config(_parse_args().config)
    logging.info(
        "Loaded configuration for %s: %d manifest(s), polling every %d seconds.",
        config.repository,
        len(config.dependency_files),
        config.polling_interval_seconds,
    )


if __name__ == "__main__":
    main()
