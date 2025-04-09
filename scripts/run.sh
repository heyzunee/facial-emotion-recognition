#!/bin/sh

# Set default worker timeout to 160 seconds if not provided
WORKER_TIMEOUT="${WORKER_TIMEOUT:-300}"

# Start the Uvicorn server with specified options
uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 9000 \
    --workers 1 \
    --timeout-keep-alive "$WORKER_TIMEOUT" \
    --log-level "info"