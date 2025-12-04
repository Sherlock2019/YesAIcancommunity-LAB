#!/usr/bin/env bash
set -e

###########################################
# YES AI CAN — CLEAN START SCRIPT
###########################################

ROOT="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT/.logs"
mkdir -p "$LOG_DIR"

API_LOG="$LOG_DIR/api_$(date +%Y%m%d-%H%M%S).log"
UI_LOG="$LOG_DIR/ui_$(date +%Y%m%d-%H%M%S).log"
OLLAMA_LOG="$LOG_DIR/ollama_$(date +%Y%m%d-%H%M%S).log"

API_PORT=8090
UI_PORT=8502

echo "------------------------------------------------------"
echo "Cleaning old processes..."
echo "------------------------------------------------------"

pkill -f "uvicorn" 2>/dev/null || true
pkill -f "streamlit" 2>/dev/null || true

echo "[OK] Old processes terminated"


###########################################################
# PYTHON ENVIRONMENT
###########################################################
echo "------------------------------------------------------"
echo "[INFO] Activating virtual environment..."
echo "------------------------------------------------------"

source "$ROOT/.venv/bin/activate"
echo "[INFO] Python: $(python3 --version)"
echo "[INFO] Pip: $(pip --version)"


###########################################################
# OLLAMA
###########################################################
echo "------------------------------------------------------"
echo "[INFO] Starting Ollama (if not already running)..."
echo "------------------------------------------------------"

if ! pgrep -x "ollama" >/dev/null; then
    ollama serve >>"$OLLAMA_LOG" 2>&1 &
    sleep 3
fi

echo "[INFO] Warming model gemma2:9b..."
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model":"gemma2:9b","prompt":"ping"}' >/dev/null 2>&1 \
  || echo "[WARN] Could not warm gemma2:9b yet."

echo "[OK] Ollama ready → logs: $OLLAMA_LOG"


###########################################################
# START API (NO RELOAD)
###########################################################
echo "------------------------------------------------------"
echo "[INFO] Starting API..."
echo "------------------------------------------------------"

nohup uvicorn services.api.main:app \
    --host 0.0.0.0 \
    --port "$API_PORT" \
    --log-level info \
    >> "$API_LOG" 2>&1 &

sleep 3

echo "[INFO] API log → $API_LOG"


###########################################################
# START STREAMLIT UI (NO WATCH MODE)
###########################################################
echo "------------------------------------------------------"
echo "[INFO] Starting Streamlit UI..."
echo "------------------------------------------------------"

nohup streamlit run services/ui/app.py \
    --server.port "$UI_PORT" \
    --browser.gatherUsageStats false \
    --server.headless true \
    >> "$UI_LOG" 2>&1 &

sleep 5

echo "[INFO] UI log → $UI_LOG"


###########################################################
# HEALTH CHECKS
###########################################################
echo "------------------------------------------------------"
echo "Checking health..."
echo "------------------------------------------------------"

API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$API_PORT/docs)
UI_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$UI_PORT)

if [[ "$API_STATUS" == "200" || "$API_STATUS" == "307" ]]; then
    echo "✅ API OK → http://localhost:$API_PORT/docs"
else
    echo "❌ API failed → status=$API_STATUS"
    echo "Check → $API_LOG"
fi

if [[ "$UI_STATUS" == "200" || "$UI_STATUS" == "307" ]]; then
    echo "🌐 UI OK → http://localhost:$UI_PORT"
else
    echo "❌ UI failed → status=$UI_STATUS"
    echo "Check → $UI_LOG"
fi

echo "------------------------------------------------------"
echo "🎉 ALL DONE — Your YES AI CAN LAB is ready!"
echo "------------------------------------------------------"
