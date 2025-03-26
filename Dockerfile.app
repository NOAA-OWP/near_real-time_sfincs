FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/src

RUN apt-get update && apt-get install -y \
    libexpat1 \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY pyproject.toml ./
COPY README.md ./

RUN pip install uv
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH
