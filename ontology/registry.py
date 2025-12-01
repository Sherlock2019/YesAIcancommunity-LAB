from __future__ import annotations
from typing import Dict, Type, List, Any

from .engine import OntologyObject
from .objects import (
    Human,
    Department,
    Team,
    Skill,
    Challenge,
    Solution,
    Project,
    Agent,
    Dataset,
    Workflow,
    System,
    Ticket,
    Asset,
    Customer,
    Policy,
    RiskFactor,
    Decision,
    Event,
)

class OntologyRegistry:
    def __init__(self) -> None:
        self.types: Dict[str, Type[OntologyObject]] = {
            cls.__name__: cls for cls in [
                Human,
                Department,
                Team,
                Skill,
                Challenge,
                Solution,
                Project,
                Agent,
                Dataset,
                Workflow,
                System,
                Ticket,
                Asset,
                Customer,
                Policy,
                RiskFactor,
                Decision,
                Event,
            ]
        }
        self.objects: List[OntologyObject] = []

    def create(self, type_name: str, **attrs: Any) -> OntologyObject:
        if type_name not in self.types:
            raise ValueError(f"Unknown ontology type: {type_name}")
        obj = self.types[type_name](**attrs)
        self.objects.append(obj)
        return obj

    def find(self, type_name: str, **query: Any) -> List[OntologyObject]:
        return [
            o for o in self.objects
            if o.type_name == type_name
            and all(o.get(k) == v for k, v in query.items())
        ]

    def all(self) -> List[Dict[str, Any]]:
        return [o.to_dict() for o in self.objects]
