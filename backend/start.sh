#!/bin/bash

# Render startup script for Smart Factory Energy Optimizer Backend
echo "Starting Smart Factory Energy Optimizer Backend..."

# Set default port if not provided
export PORT=${PORT:-8000}

# Set default host
export HOST=${HOST:-0.0.0.0}

# Print environment info
echo "Python version: $(python --version)"
echo "Starting server on $HOST:$PORT"

# Start the FastAPI application
exec uvicorn app_precomputed:app --host $HOST --port $PORT --workers 1