from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

__all__ = [
    "load_human_stack",
    "save_human_stack",
    "update_my_profile",
    "delete_profile_by_id",
    "search_by_skills",
    "search_by_project",
]


def _ensure_list(value: Any) -> List:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


class HumanStack:
    def __init__(self, path: str | Path | None = None):
        base_path = (
            Path(path)
            if path is not None
            else Path(__file__).resolve().parent / ".sandbox_meta" / "humans.json"
        )
        self.path = base_path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Dict]:
        if not self.path.exists():
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def save(self, records: List[Dict]) -> None:
        tmp = self.path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        tmp.replace(self.path)

    def update(self, profile: Dict) -> None:
        records = self.load()
        key = profile.get("id")

        # update or append
        for i, r in enumerate(records):
            if r.get("id") == key:
                records[i] = {**r, **profile}
                self.save(records)
                return

        # else create
        records.append(profile)
        self.save(records)

    def delete(self, profile_id: str) -> None:
        records = self.load()
        records = [r for r in records if r.get("id") != profile_id]
        self.save(records)

    def search_people(self, query: str | Iterable[str]) -> List[Dict]:
        if not query:
            return []

        tokens = [q.lower() for q in (query.split() if isinstance(query, str) else query)]

        out = []
        for h in self.load():
            text = " ".join(_ensure_list(h.get("skills"))).lower()
            if all(t in text for t in tokens):
                out.append(h)
        return out

    def search_projects(self, query: str | Iterable[str]) -> List[Dict]:
        if not query:
            return []

        tokens = [q.lower() for q in (query.split() if isinstance(query, str) else query)]

        out = []
        for profile in self.load():
            for p in _ensure_list(profile.get("projects_built")):
                combined = (
                    f"{p.get('title','')} "
                    f"{p.get('description','')} "
                    f"{' '.join(_ensure_list(p.get('skills_used')))}"
                ).lower()

                if all(t in combined for t in tokens):
                    entry = dict(p)
                    entry["owner_name"] = profile.get("name")
                    out.append(entry)
        return out


# Global instance
STACK = HumanStack()


def load_human_stack():
    return STACK.load()


def save_human_stack(records: List[Dict]):
    STACK.save(records)


def update_my_profile(profile: Dict):
    STACK.update(profile)


def delete_profile_by_id(profile_id: str):
    STACK.delete(profile_id)


def search_by_skills(query):
    return STACK.search_people(query)


def search_by_project(query):
    return STACK.search_projects(query)
