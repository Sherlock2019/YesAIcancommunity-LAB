from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChallengeBase(BaseModel):
    submitter_name: str = Field(..., min_length=1)
    department: str
    region: str
    role: str
    title: str
    description: str
    task_type: str
    category: str
    difficulty: str
    impact: float = Field(..., ge=0, le=10)
    urgency: float = Field(..., ge=0, le=10)
    tags: List[str] = Field(default_factory=list)
    confidentiality: str
    team_size: int = Field(..., ge=1)


class ChallengeCreate(ChallengeBase):
    pass


class SolutionBase(BaseModel):
    helper_name: str
    approach: str
    difficulty: str
    status: str


class SolutionCreate(SolutionBase):
    pass


class SolutionRead(SolutionBase):
    id: int
    challenge_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ChallengeRead(ChallengeBase):
    id: int
    created_at: datetime
    attachment_path: Optional[str] = None
    solutions: List[SolutionRead] = Field(default_factory=list)

    class Config:
        orm_mode = True
