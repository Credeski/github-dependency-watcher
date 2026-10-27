# GitHub Dependency Watcher

A Python starter project for configuring a watcher of dependency manifests in a
GitHub repository.

## Setup

Use Python 3.10 or later:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GITHUB_TOKEN` in `.env` to a GitHub personal access token if authenticated
API access is needed. Keep `.env` out of source control.

## Configuration

Edit [config.json](config.json):

- `repository`: GitHub repository in `owner/name` format.
- `polling_interval_seconds`: positive interval for future polling.
- `dependency_files`: repository-relative paths to dependency manifests.

The CLI validates and displays the effective configuration:

```powershell
py -m src.dependency_watcher.main
```

Pass a different configuration file with `--config path\to\config.json`.
The current entry point is a configuration/bootstrap scaffold; repository
polling and dependency-change detection are not implemented yet.

## Tests

```powershell
pytest
```
