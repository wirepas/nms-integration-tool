# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Install dependencies as a separate layer so they are cached on pyproject.toml changes
COPY pyproject.toml .
RUN uv sync --extra examples --no-dev --no-install-project

# Copy source and install the project
COPY src/ src/
COPY examples/ examples/
RUN uv sync --extra examples --no-dev

# Activate the venv for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "examples/scripts/data_import.py"]
