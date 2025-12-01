#!/usr/bin/env python3
"""Error Logger for Troubleshooting"""
from __future__ import annotations

import traceback
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import streamlit as st

# Log file path
LOG_DIR = Path(__file__).parent.parent / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
ERROR_LOG_FILE = LOG_DIR / "error_log.json"

def log_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    user_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log an error with context information.
    
    Args:
        error: The exception that occurred
        context: Additional context (form data, agent info, etc.)
        user_message: User-friendly error message
    
    Returns:
        Dict with error log entry
    """
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc(),
        "context": context or {},
        "user_message": user_message
    }
    
    # Load existing logs
    logs = []
    if ERROR_LOG_FILE.exists():
        try:
            with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    # Add new log entry
    logs.append(error_entry)
    
    # Keep only last 100 entries
    if len(logs) > 100:
        logs = logs[-100:]
    
    # Save logs
    try:
        with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to write error log: {e}")
    
    return error_entry

def get_recent_errors(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent error logs."""
    if not ERROR_LOG_FILE.exists():
        return []
    
    try:
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return logs[-limit:] if len(logs) > limit else logs
    except Exception:
        return []

def clear_error_log():
    """Clear all error logs."""
    if ERROR_LOG_FILE.exists():
        ERROR_LOG_FILE.unlink()
    return True

def log_form_data(form_name: str, data: Dict[str, Any]) -> None:
    """Log form data for debugging."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "form_data",
        "form_name": form_name,
        "data": data
    }
    
    logs = []
    if ERROR_LOG_FILE.exists():
        try:
            with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    logs.append(log_entry)
    if len(logs) > 100:
        logs = logs[-100:]
    
    try:
        with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
