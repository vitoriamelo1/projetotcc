FROM node:24-bookworm-slim AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build:css

FROM ghcr.io/astral-sh/uv:0.9.5-python3.12-bookworm AS runner


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_COMPILE_BYTECODE 1
ENV UV_LINK_MODE copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

COPY --from=builder /app/static /app/static
COPY --from=builder /app/static/css/style.css /app/static/css/style.css

RUN rm /app/static/css/_style.css
RUN uv run manage.py collectstatic --noinput
EXPOSE 8000

ENTRYPOINT []

# CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "core.wsgi:application"]