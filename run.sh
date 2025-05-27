#!/bin/sh

# Exit if any command fails
set -e

# Start BentoML service on port 3000 if not already running
if ! lsof -i:3000 >/dev/null; then
  PYTHONPATH=src bentoml serve src.bento_service:svc &
  BENTO_PID=$!
  echo "Started BentoML (PID $BENTO_PID)"
else
  echo "Port 3000 already in use, BentoML not started."
fi

# Start FastAPI on port 8000 if not already running
if ! lsof -i:8000 >/dev/null; then
  uvicorn src.api_fastapi:app --reload &
  FASTAPI_PID=$!
  echo "Started FastAPI (PID $FASTAPI_PID)"
else
  echo "Port 8000 already in use, FastAPI not started."
fi

# Start Streamlit on port 8501 if not already running
if ! lsof -i:8501 >/dev/null; then
  streamlit run src/ui_streamlit.py &
  STREAMLIT_PID=$!
  echo "Started Streamlit (PID $STREAMLIT_PID)"
else
  echo "Port 8501 already in use, Streamlit not started."
fi

# Wait for all background processes
wait