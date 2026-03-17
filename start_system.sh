#!/bin/bash

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_PYTHON="$(which python3)"

# Function to kill process on a specific port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ -n "$pid" ]; then
        echo "Stopping process on port $port (PID: $pid)..."
        kill -9 $pid
    fi
}

echo "🚀 Deploying Smart Test Case Generator..."

# Load .env if exists
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

# 1. Cleanup existing ports
echo "Checking ports..."
kill_port $BACKEND_PORT
kill_port $FRONTEND_PORT

# 2. Check LLM Provider
if [ "$LLM_PROVIDER" = "ollama" ] || [ -z "$LLM_PROVIDER" ]; then
    if ! pgrep -x "ollama" > /dev/null; then
        echo "⚠️  Ollama is not running. Starting Ollama serve..."
        ollama serve &
        sleep 5
    else
        echo "✅ Ollama is running."
    fi
else
    echo "✅ Using cloud LLM provider: $LLM_PROVIDER"
fi

# 3. Start Backend
echo "Starting Backend on port $BACKEND_PORT..."
cd "$BACKEND_DIR"
nohup $VENV_PYTHON -m uvicorn app:app --host 0.0.0.0 --port $BACKEND_PORT > "$PROJECT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID). Logs: backend.log"

# 4. Start Frontend
echo "Starting Frontend on port $FRONTEND_PORT..."
cd "$FRONTEND_DIR"
nohup $VENV_PYTHON -m http.server $FRONTEND_PORT > "$PROJECT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID). Logs: frontend.log"

echo ""
echo "🎉 System Deployed!"
echo "➡️  Frontend: http://localhost:$FRONTEND_PORT"
echo "➡️  Backend:  http://localhost:$BACKEND_PORT/health"
echo ""
echo "To stop servers, run: lsof -ti:$BACKEND_PORT -ti:$FRONTEND_PORT | xargs kill -9"
