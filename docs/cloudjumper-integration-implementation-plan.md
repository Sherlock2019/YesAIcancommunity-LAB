# CloudJumper Integration — Implementation Plan

Status: Phase A implemented (Parts 1–3). Feature flag
`CLOUDJUMPER_PRODUCTION_FACTORY_ENABLED`.

## 1. Existing architecture (inspected)

| Concern | Finding |
|---|---|
| Backend | FastAPI, `services/api/main.py`, `create_app()` + `app.include_router(...)` |
| ORM | SQLAlchemy 2.0 style — `Mapped` / `mapped_column`, `Base` from `services/api/database.py` |
| Database | SQLite `services/api/challenge_hub.db` (`CHALLENGE_DB_URL` overrides) |
| Migrations | **None — no alembic.** `init_db()` calls `Base.metadata.create_all()` |
| Existing models | `Challenge`, `Solution` |
| Existing routers | `challenges.py`, `solutions.py` (+ many agent routers) |
| Frontend | Streamlit, `services/ui/` and `services/ui/pages/` |
| Tests | bare `test_*.py`, pytest |

Because there is no migration tool, new tables are created by `create_all()` on
startup. No existing column is renamed or dropped.

## 2. Relationship to AI 4 the People (SANDBOX)

Measured, not assumed:

- 12 of 12 shared top-level files are **byte-identical**
- **129 of 143** Python files present in both repos are byte-identical (90%)
- Separate git roots — the SANDBOX is a copy, not a branch
- Challenge Hub, Project Hub, Human Stack, Customer ZERO and ontology exist
  **only** in YES AI CAN

Therefore the integration is built **once, here**. The SANDBOX is a *producer*
of Agent Passports, not a second integration surface. Duplicating the engine
into a 90%-identical fork would guarantee drift.

## 3. CloudJumper: verified contract, not assumed

Checked against the running CloudJumper (`workflow_dashboard/ai_adoption`):

| Original spec assumed | Reality |
|---|---|
| `POST /api/v1/ai-adoption/import` + 8 more | `/ai-adoption/…`, 6 endpoints, no `/api/v1` prefix |
| separate `/gaps`, `/architecture`, `/artifacts` | embedded in one project document |
| `POST /scan`, `POST /deployment-plan` | `POST /assess`, `POST /plan` |
| 17 signed webhook events | **no webhook code exists** |
| service-to-service auth | **GitHub OAuth (browser) or loopback only** |
| statuses `READY_FOR_UAT`, `CANARY`, `PRODUCTION`, `ROLLED_BACK` | **do not exist** — 6 statuses ending at `PLANNED`/`HANDED_OFF` |

CloudJumper does not observe deployment, UAT or canary, so it cannot be the
source of truth for them. Any UI showing those stages would display data that
nothing sets.

**What does exist and is the integration point:** CloudJumper's Upload import
provider detects and validates `cloudjumper-handoff.yaml`, requiring
`schema_version`, `project`, `agent`, `model`, `data`, `deployment`, and warning
on missing model licence, data sensitivity, project owner or health endpoint.
This plan targets that contract exactly.

## 4. Scope: 31 spec sections → 5 parts

| Part | Content | Status |
|---|---|---|
| 1 Identity | `global_ai_project_id`, adoption mode, 2 tables | **Built** |
| 2 Evidence | Agent Passport, readiness gate | **Built** |
| 3 Transport | handoff package + checksums, bundle export | **Built** |
| 4 Link | REST client, S2S auth, status sync | Blocked — CloudJumper has no S2S auth |
| 5 Feedback | webhooks, deployment timeline, production metrics | Blocked — no emitter, no deploy states |

Parts 1–3 deliver the whole journey up to a signed, checksummed bundle that
CloudJumper already imports. Parts 4–5 need CloudJumper-side work first.

### Deliberate reductions

| Spec | Decision |
|---|---|
| 6 tables | **2** (`ProductionCandidate`, `ProductionEvidence`). The other 4 serve blocked Parts 4–5 |
| 22 candidate statuses | **6** — the other 16 mirror CloudJumper states that do not exist |
| 19 REST endpoints | **6** |
| 13 client methods | deferred with Part 4 |
| 13 doc files | **2** |
| 13 Human Stack roles | 4 that actually gate something |
| UAT / canary / production tiles | **removed** — nothing sets them |

## 5. Security model

- Bundle files are checksummed (SHA-256, `checksums.sha256`).
- Packages are scanned for secrets before writing; a hit is a **blocking** gap.
- Filenames sanitised; no absolute paths, no traversal, no symlinks.
- Size and file-count caps on the generated bundle.
- Nothing imported is executed.
- Readiness controls resolve `PASS / WARNING / FAIL / NOT_CHECKED`.
  **`NOT_CHECKED` is never converted to `PASS`.**
- No credentials in the bundle, the database, or logs — secret *references* only.
- Every generation and download is audit-logged with an actor and correlation id.

## 6. Testing

pytest, matching the repo. Unit tests for id generation, adoption-mode
validation, status transitions, readiness rules, passport generation, manifest
schema, checksums, secret detection, filename sanitisation. Round-trip test that
a generated bundle is accepted by CloudJumper's own validator.

## 7. Assumptions and unresolved

- CloudJumper is reached by **file handoff**, not API, in this phase.
- `global_ai_project_id` is minted here and is authoritative across systems.
- Parts 4–5 require, on the CloudJumper side: an API-key/service credential, a
  deployment state machine, and a webhook emitter. None exist today.
