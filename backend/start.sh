#!/bin/sh

# PyAssistant Analytics - production start script
# Container starts here (railway.json -> "sh backend/start.sh").
# Dependencies are installed at BUILD time by the Dockerfile,
# so this script only configures env and boots gunicorn.

export PYTHONUNBUFFERED=1
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8080}"

exec gunicorn main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind "${HOST}:${PORT}" \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile -
