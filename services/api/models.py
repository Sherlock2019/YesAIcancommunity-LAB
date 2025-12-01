from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.database import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    submitter_name: Mapped[str] = mapped_column(String(120))
    department: Mapped[str] = mapped_column(String(120))
    region: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(120))

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    tags: Mapped[str | None] = mapped_column(String(400), nullable=True)
    task_type: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(120))
    difficulty: Mapped[str] = mapped_column(String(50))
    impact: Mapped[float] = mapped_column(Float)
    urgency: Mapped[float] = mapped_column(Float)
    confidentiality: Mapped[str] = mapped_column(String(50))
    team_size: Mapped[int] = mapped_column(Integer, default=1)
    attachment_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    solutions: Mapped[list["Solution"]] = relationship(
        "Solution",
        back_populates="challenge",
        cascade="all, delete-orphan",
    )


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"), nullable=False)

    helper_name: Mapped[str] = mapped_column(String(120))
    approach: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))

    challenge: Mapped[Challenge] = relationship("Challenge", back_populates="solutions")
