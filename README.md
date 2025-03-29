# Hali-rant

Collect Buildathon 1

29 March 2025

### Getting Started

1. Install uv astral `curl -LsSf https://astral.sh/uv/install.sh | less`
2. Install python `uv python install`
3. Sync dependencies `uv sync --directory backend`
4. Run main `uv run backend/main.py`



### Generate mock data

1. `uv run app/models/models.py > mock.json`

### Running api websever

1. `cd backend/app`
2. `uv run fastapi dev main.py`

### Running database

1. `uv run gel project init`
2. `uv run gel extension install postgis`
3. `uv run gel instance restart`
4. `uv run gel migrate`


### Running full app:

This will spin up a local environment with the database, front-end and back-end:

1. Install Docker (<https://www.docker.com/>)
2. Under root of repo: `docker compose up --build`. Hit Ctrl+C to stop it.
Alternatively it can be launched in detached mode: `docker compose up -d --build`, then call `docker compose down` later (from root folder of repo) to stop everything.
