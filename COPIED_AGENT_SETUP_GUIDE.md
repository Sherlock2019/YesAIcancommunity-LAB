# 📋 Files That Must Be Updated When Using a Copied Agent

This guide explains all the files that need to be updated when you want a copied agent to have its **own independent backend** (not sharing with the original).

## 🎯 Two Scenarios

### Scenario 1: Shared Backend (Current Implementation) ✅
- **Copied agent routes to the same backend page as original**
- **Only 1 file needs updating:**
  - `services/ui/data/agents.json` - Agent definition with `route_name` field

### Scenario 2: Independent Backend (Full Copy) 🔧
- **Copied agent has its own separate backend page**
- **Multiple files need updating:**
  - See list below

---

## 📁 Files That Must Be Updated for Independent Backend

### 1. **Agent Definition File** (Required)
**File:** `services/ui/data/agents.json`
- Add the copied agent entry
- Set unique `route_name` (e.g., `"ceo_driver_dashboard_copy"`)
- Update agent name, description, etc.

**Example:**
```json
{
  "agent": "🚗 CEO driver DASHBOARD (Copy)",
  "route_name": "ceo_driver_dashboard_copy",
  "sector": "🏢 Executive Leadership",
  "industry": "🚗 Boardroom Intelligence",
  ...
}
```

---

### 2. **Backend Page File** (Required)
**File:** `services/ui/pages/{route_name}.py`
- Create a new page file for the copied agent
- Copy the original backend page (e.g., `ceo_driver_dashboard.py`)
- Rename to match the new `route_name` (e.g., `ceo_driver_dashboard_copy.py`)
- Update any agent-specific logic if needed

**Example:**
```bash
cp services/ui/pages/ceo_driver_dashboard.py services/ui/pages/ceo_driver_dashboard_copy.py
```

---

### 3. **Main App Routing** (Required)
**File:** `services/ui/app.py`

#### 3a. Add to `launch_path_overrides` dictionary (Line ~1273)
```python
launch_path_overrides = {
    ...
    "ceo_driver_dashboard": "/ceo_driver_dashboard",
    "ceo_driver_dashboard_copy": "/ceo_driver_dashboard_copy",  # Add this
    ...
}
```

#### 3b. Add to special cases list (Line ~1361)
```python
if route_name in {"lottery_wizard", "ceo_driver_dashboard", "ceo_driver_seat", 
                  "ceo_driver_dashboard_copy",  # Add this
                  "real_estate_evaluator", "agent_builder", "hf_inspector"}:
```

#### 3c. Add to query parameter routing (Line ~846)
```python
elif agent in {"ceo", "ceo_driver", "driver_dashboard", "ceo_dashboard", 
               "ceo_driver_copy", "ceo_copy"}:  # Add aliases
    try:
        st.switch_page("pages/ceo_driver_dashboard_copy.py")  # Update path
```

#### 3d. Add to stage-based routing (Line ~2104)
```python
if st.session_state.stage == "ceo_driver_dashboard_copy":  # Add this
    try:
        st.switch_page("pages/ceo_driver_dashboard_copy.py")
```

---

### 4. **API Router Registration** (If agent has API endpoints)
**File:** `services/api/routers/agents.py`

#### 4a. Add to imports (if needed)
```python
from agents.{agent_name}_copy.runner import run as run_{agent_name}_copy
```

#### 4b. Add to `AGENT_REGISTRY` (Line ~50)
```python
AGENT_REGISTRY["ceo_driver_dashboard_copy"] = {
    "runner": run_ceo_driver_dashboard_copy,
    "display_name": "CEO driver DASHBOARD (Copy)",
    "description": "...",
    ...
}
```

---

### 5. **Agent Backend Logic** (If agent has separate backend)
**Directory:** `agents/{agent_name}_copy/`

If the agent has its own backend logic (not just a UI page), you may need:
- `agents/{agent_name}_copy/runner.py` - Main runner logic
- `agents/{agent_name}_copy/agent.py` - Agent implementation
- `agents/{agent_name}_copy/config.yaml` - Configuration
- Other agent-specific files

**Example:**
```bash
cp -r agents/credit_appraisal agents/credit_appraisal_copy
# Then update imports and references inside the copied files
```

---

### 6. **Configuration Files** (If applicable)
**Files:**
- `config/*.yaml` - Agent-specific configurations
- `.env` or environment files - API keys, endpoints
- `docker-compose.yml` - Service definitions (if agent runs as separate service)

---

### 7. **Admin Interface** (Optional)
**File:** `services/ui/pages/admin_agents.py`
- The admin interface should automatically pick up the new agent from `agents.json`
- No changes needed unless you want custom admin features for the copied agent

---

## 🔄 Quick Reference: Minimal Setup (Shared Backend)

If you just want the copied agent to **share the backend** with the original:

**Only update:**
1. ✅ `services/ui/data/agents.json` - Add agent with `route_name` pointing to original

**That's it!** The current implementation handles this automatically.

---

## 🔧 Full Setup (Independent Backend)

If you want the copied agent to have its **own independent backend**:

**Update these files:**
1. ✅ `services/ui/data/agents.json` - Add agent with unique `route_name`
2. ✅ `services/ui/pages/{route_name}.py` - Create new backend page
3. ✅ `services/ui/app.py` - Add routing in 4 places (see above)
4. ✅ `services/api/routers/agents.py` - Add API registration (if needed)
5. ✅ `agents/{agent_name}_copy/` - Copy agent backend logic (if exists)
6. ✅ Configuration files - Update as needed

---

## 📝 Example: Copying CEO Driver Dashboard

### Step 1: Update agents.json
```json
{
  "agent": "🚗 CEO driver DASHBOARD (Copy)",
  "route_name": "ceo_driver_dashboard_copy",
  "sector": "🏢 Executive Leadership",
  "industry": "🚗 Boardroom Intelligence",
  "description": "Copy of CEO dashboard with independent backend",
  "status": "WIP",
  "emoji": "🚗",
  "requires_login": false
}
```

### Step 2: Create backend page
```bash
cp services/ui/pages/ceo_driver_dashboard.py services/ui/pages/ceo_driver_dashboard_copy.py
```

### Step 3: Update app.py routing
Add to `launch_path_overrides`, special cases, query routing, and stage routing (see sections 3a-3d above)

### Step 4: Test
- Launch the copied agent from landing page
- Verify it routes to the new backend page
- Verify backend functionality works independently

---

## ⚠️ Important Notes

1. **Route Name Convention**: Use `{original_route}_copy` for clarity
2. **Page File Naming**: Must match `route_name` (e.g., `route_name: "x"` → `pages/x.py`)
3. **Caching**: Streamlit caches agent data for 1 second - changes appear quickly
4. **Testing**: Always test both original and copied agents after changes
5. **Backend Logic**: If agent has complex backend, ensure copied version doesn't conflict with original

---

## 🎯 Current Implementation Status

**✅ Already Implemented:**
- Copy agent functionality in admin interface
- `route_name` field preservation
- Route name mapping system
- Shared backend routing

**🔧 Needs Manual Setup:**
- Independent backend pages (if desired)
- API endpoint registration (if agent has API)
- Backend logic copying (if agent has separate backend)

---

## 💡 Recommendation

**For most use cases:** Use **Scenario 1 (Shared Backend)** - it's simpler and requires only updating `agents.json`.

**For independent testing/customization:** Use **Scenario 2 (Independent Backend)** - requires updating multiple files as listed above.
