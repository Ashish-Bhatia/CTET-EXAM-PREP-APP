FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt

WORKDIR /workspaces/CTET-EXAM-PREP-APP
