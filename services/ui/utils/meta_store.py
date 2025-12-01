from __future__ import annotations

import json
from pathlib import Path
from typing import Any


META_DIR = Path(__file__).resolve().parents[2] / ".sandbox_meta"
META_DIR.mkdir(exist_ok=True)


def _path(name: str) -> Path:
    return META_DIR / name


def load_json(name: str, default: Any) -> Any:
    path = _path(name)
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(name: str, data: Any) -> None:
    path = _path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
