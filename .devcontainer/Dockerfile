FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt

WORKDIR /workspaces/CTET-EXAM-PREP-APP
