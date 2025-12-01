from __future__ import annotations

import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from services.api import models, schemas
from services.api.database import get_db


router = APIRouter(prefix="/challenges", tags=["challenges"])
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _serialize_tags(tags: list[str] | None) -> str | None:
    if not tags:
        return None
    return ",".join(tag.strip() for tag in tags if tag.strip())


def _deserialize_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [value.strip() for value in raw.split(",") if value.strip()]


def _challenge_to_schema(challenge: models.Challenge) -> schemas.ChallengeRead:
    solutions = [
        schemas.SolutionRead.from_orm(solution)
        for solution in challenge.solutions
    ]
    data = {
        "id": challenge.id,
        "created_at": challenge.created_at,
        "submitter_name": challenge.submitter_name,
        "department": challenge.department,
        "region": challenge.region,
        "role": challenge.role,
        "title": challenge.title,
        "description": challenge.description,
        "task_type": challenge.task_type,
        "category": challenge.category,
        "difficulty": challenge.difficulty,
        "impact": challenge.impact,
        "urgency": challenge.urgency,
        "tags": _deserialize_tags(challenge.tags),
        "confidentiality": challenge.confidentiality,
        "team_size": challenge.team_size,
        "attachment_path": challenge.attachment_path,
        "solutions": solutions,
    }
    return schemas.ChallengeRead(**data)


@router.post("", response_model=schemas.ChallengeRead)
def create_challenge(payload: schemas.ChallengeCreate, db: Session = Depends(get_db)):
    challenge = models.Challenge(
        submitter_name=payload.submitter_name,
        department=payload.department,
        region=payload.region,
        role=payload.role,
        title=payload.title,
        description=payload.description,
        task_type=payload.task_type,
        category=payload.category,
        difficulty=payload.difficulty,
        impact=payload.impact,
        urgency=payload.urgency,
        tags=_serialize_tags(payload.tags),
        confidentiality=payload.confidentiality,
        team_size=payload.team_size,
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return _challenge_to_schema(challenge)


@router.get("", response_model=List[schemas.ChallengeRead])
def list_challenges(db: Session = Depends(get_db)):
    records = db.query(models.Challenge).order_by(models.Challenge.created_at.desc()).all()
    return [_challenge_to_schema(item) for item in records]


@router.post("/{challenge_id}/upload", response_model=schemas.ChallengeRead)
def upload_attachment(
    challenge_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    filename = f"challenge_{challenge_id}_{file.filename}"
    destination = UPLOAD_DIR / filename
    with destination.open("wb") as buffer:
        buffer.write(file.file.read())
    challenge.attachment_path = str(destination)
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return _challenge_to_schema(challenge)
