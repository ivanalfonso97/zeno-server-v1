#!/bin/bash
set -e

# Activate the virtual environment
source "${VENV_ROOT}/bin/activate"

# Start the FastAPI app with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"