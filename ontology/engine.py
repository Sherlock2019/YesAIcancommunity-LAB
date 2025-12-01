from __future__ import annotations
from typing import Dict, List, Any

class OntologyObject:
    type_name = "BaseObject"

    def __init__(self, **attrs: Any) -> None:
        self.attributes = attrs
        self.links: Dict[str, List["OntologyObject"]] = {}

    def set(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.attributes.get(key, default)

    def link(self, relation: str, obj: "OntologyObject") -> None:
        self.links.setdefault(relation, []).append(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name,
            "attributes": self.attributes,
            "links": {
                rel: [o.attributes for o in items]
                for rel, items in self.links.items()
            },
        }
