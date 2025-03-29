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