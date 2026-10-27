"""Tests for dependency watcher configuration."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.dependency_watcher.config import load_config


class LoadConfigTests(unittest.TestCase):
    def write_config(self, directory: str, values: dict[str, object]) -> Path:
        path = Path(directory) / "config.json"
        path.write_text(json.dumps(values), encoding="utf-8")
        return path

    def test_loads_valid_config_and_environment_token(self) -> None:
        values = {
            "repository": "octocat/hello-world",
            "polling_interval_seconds": 600,
            "dependency_files": ["requirements.txt", "package.json"],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, values)
            with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
                config = load_config(path)

        self.assertEqual(config.repository, "octocat/hello-world")
        self.assertEqual(config.polling_interval_seconds, 600)
        self.assertEqual(config.dependency_files, ("requirements.txt", "package.json"))
        self.assertEqual(config.github_token, "test-token")

    def test_token_is_optional(self) -> None:
        values = {
            "repository": "octocat/hello-world",
            "polling_interval_seconds": 600,
            "dependency_files": ["requirements.txt"],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, values)
            with patch.dict(os.environ, {}, clear=True):
                config = load_config(path)

        self.assertIsNone(config.github_token)

    def test_rejects_invalid_repository(self) -> None:
        values = {
            "repository": "not-a-repository",
            "polling_interval_seconds": 600,
            "dependency_files": ["requirements.txt"],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, values)
            with self.assertRaisesRegex(ValueError, "owner/name"):
                load_config(path)

    def test_rejects_non_positive_polling_interval(self) -> None:
        values = {
            "repository": "octocat/hello-world",
            "polling_interval_seconds": 0,
            "dependency_files": ["requirements.txt"],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, values)
            with self.assertRaisesRegex(ValueError, "positive integer"):
                load_config(path)

    def test_rejects_empty_dependency_file_list(self) -> None:
        values = {
            "repository": "octocat/hello-world",
            "polling_interval_seconds": 600,
            "dependency_files": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_config(directory, values)
            with self.assertRaisesRegex(ValueError, "non-empty list"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
