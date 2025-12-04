#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"
API_PORT=8100
UI_PORT=8054

log()  { echo -e "[INFO] $*"; }
warn() { echo -e "\033[33m[WARN] $*\033[0m"; }
err()  { echo -e "\033[31m[ERROR] $*\033[0m"; }

echo ""
echo "🚀 YESAICAN Sandbox Starter"
echo "─────────────────────────────────────"

# ---------------------------------------------
# 1. Kill existing processes
# ---------------------------------------------
log "Stopping existing API/UI processes…"
pkill -f "uvicorn services.api.main:app" 2>/dev/null || true
pkill -f "streamlit run app.py" 2>/dev/null || true

log "Freeing ports…"
fuser -k "$API_PORT/tcp" 2>/dev/null || true
fuser -k "$UI_PORT/tcp" 2>/dev/null || true

# ---------------------------------------------
# 2. Ensure python3-venv present
# ---------------------------------------------
log "Checking python3-venv…"
if ! dpkg -s python3-venv >/dev/null 2>&1; then
    warn "Installing python3-venv…"
    sudo apt-get update -y
    sudo apt-get install -y python3-venv python3.10-venv
fi

# ---------------------------------------------
# 3. FORCE Create or Repair VENV
# ---------------------------------------------
log "Creating or repairing virtual environment…"

# If venv folder exists but broken → delete
if [[ -d "$VENV" && ! -f "$VENV/bin/activate" ]]; then
    warn "Existing venv is incomplete → deleting…"
    rm -rf "$VENV"
fi

# Try to create venv
if [[ ! -d "$VENV" ]]; then
    warn "Creating venv fresh…"
    python3 -m venv "$VENV" || true
fi

# If activate still missing → install ensurepip + rebuild
if [[ ! -f "$VENV/bin/activate" ]]; then
    warn "ensurepip missing → repairing Python venv tools…"
    sudo apt-get install -y python3.10-distutils python3.10-dev
    python3 -m venv "$VENV" || true
fi

# One more hard check
if [[ ! -f "$VENV/bin/activate" ]]; then
    err "Venv is STILL missing. Forcing ensurepip fallback…"
    python3 -m ensurepip --upgrade || true
    python3 -m venv "$VENV"
fi

# Final fail-proof catch
if [[ ! -f "$VENV/bin/activate" ]]; then
    err "❌ CRITICAL: venv cannot be created. Python is corrupted."
    echo "Run: sudo apt install --reinstall python3.10 python3.10-venv"
    exit 1
fi

# ---------------------------------------------
# 4. ACTIVATE VENV (will always succeed now)
# ---------------------------------------------
log "Activating virtual environment…"
source "$VENV/bin/activate"

# ---------------------------------------------
# 5. INSTALL DEPENDENCIES
# ---------------------------------------------
log "Upgrading pip + wheel…"
pip install -q --upgrade pip wheel setuptools

log "Installing API requirements…"
pip install -q -r "$ROOT/services/api/requirements.txt"

log "Installing UI requirements…"
pip install -q -r "$ROOT/services/ui/requirements.txt"

# ---------------------------------------------
# 6. START API
# ---------------------------------------------
log "Starting API on port $API_PORT…"
nohup python -m uvicorn services.api.main:app \
    --host 0.0.0.0 --port "$API_PORT" \
    > "$ROOT/api.log" 2>&1 &

# ---------------------------------------------
# 7. START UI
# ---------------------------------------------
log "Starting UI on port $UI_PORT…"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
nohup python -m streamlit run services/ui/app.py \
    --server.port "$UI_PORT" \
    --server.address 0.0.0.0 \
    > "$ROOT/ui.log" 2>&1 &

# ---------------------------------------------
# 8. DISPLAY LINKS
# ---------------------------------------------
echo ""
echo "🎉 Services running!"
echo "🌐 UI →  http://localhost:$UI_PORT"
echo "📘 API → http://localhost:$API_PORT/docs"
echo ""
echo "Logs:"
echo "  API → $ROOT/api.log"
echo "  UI  → $ROOT/ui.log"
echo ""
echo "Done."
