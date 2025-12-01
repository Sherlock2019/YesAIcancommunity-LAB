from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from services.api import models
from services.api.database import SessionLocal, init_db
from services.api.routers import challenges, solutions


def seed_data() -> None:
    with SessionLocal() as session:
        if session.query(models.Challenge).count() > 0:
            return
        sample_challenge = models.Challenge(
            submitter_name="Jordan Lee",
            department="Finance Ops",
            region="AMER",
            role="Billing Analyst",
            title="Automate Monthly Billing Reconciliation",
            description="Manual spreadsheet matching for 12 regions. Need automation to reconcile invoices vs ERP.",
            task_type="Document-heavy",
            category="Finance",
            difficulty="Medium",
            impact=9.2,
            urgency=8.7,
            tags="finance,automation,billing",
            confidentiality="Internal",
            team_size=3,
        )
        session.add(sample_challenge)
        session.commit()
        session.refresh(sample_challenge)
        sample_solution = models.Solution(
            challenge_id=sample_challenge.id,
            helper_name="John Lennon",
            approach="“Imagine Ledger” — rule-based matcher + explainability layer.",
            difficulty="Medium",
            status="Prototype",
        )
        session.add(sample_solution)
        session.commit()


def create_app() -> FastAPI:
    init_db()
    seed_data()
    app = FastAPI(title="YES AI CAN — Challenge Hub API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(challenges.router)
    app.include_router(solutions.router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", "8090")))
