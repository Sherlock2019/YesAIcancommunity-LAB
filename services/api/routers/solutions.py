from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.api import models, schemas
from services.api.database import get_db


router = APIRouter(prefix="/solutions", tags=["solutions"])


def _solution_to_schema(record: models.Solution) -> schemas.SolutionRead:
    return schemas.SolutionRead.from_orm(record)


@router.post("/{challenge_id}", response_model=schemas.SolutionRead)
def create_solution(
    challenge_id: int,
    payload: schemas.SolutionCreate,
    db: Session = Depends(get_db),
):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    solution = models.Solution(
        challenge_id=challenge_id,
        helper_name=payload.helper_name,
        approach=payload.approach,
        difficulty=payload.difficulty,
        status=payload.status,
    )
    db.add(solution)
    db.commit()
    db.refresh(solution)
    return _solution_to_schema(solution)


@router.get("/{challenge_id}", response_model=List[schemas.SolutionRead])
def list_solutions(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    solutions = (
        db.query(models.Solution)
        .filter(models.Solution.challenge_id == challenge_id)
        .order_by(models.Solution.created_at.desc())
        .all()
    )
    return [_solution_to_schema(item) for item in solutions]
