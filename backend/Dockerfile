FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY ./pyproject.toml ./poetry.lock* /app/

RUN uv pip install --system --no-deps .
RUN uv pip install --system uvicorn[standard]
# FIXME: Hack workaround for import error
RUN uv pip install --system fastapi
RUN uv sync

COPY ./ /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
