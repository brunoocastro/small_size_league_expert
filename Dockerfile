FROM ghcr.io/astral-sh/uv:python3.9-alpine

WORKDIR /app

COPY . /app/.

RUN uv sync --all-groups

RUN pip install --no-cache-dir --upgrade fastapi[standard]

CMD ["fastapi", "run", "api.py", "--port", "80"]