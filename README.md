# ZUNO - Scalable Social Media Platform

ZUNO is implemented as a modular monolith (microservice-ready boundaries) with FastAPI + PostgreSQL + Redis + Flutter.

## Architecture

- API Layer (FastAPI): `backend/app/main.py`
- Auth Service: `backend/app/api/auth.py`
- Social Graph Service: `backend/app/api/follow.py`
- Feed Service: `backend/app/api/feed.py` + `backend/app/services/feed.py`
- Chat Service: `backend/app/api/chat.py` + WebSocket endpoint
- Media Service: `backend/app/api/media.py`
- Notification Service: `backend/app/api/notifications.py` + `backend/app/services/notification.py`
- Monetization/Verification Service: `backend/app/api/verification.py` + `backend/app/services/verification.py`
- Admin/Moderation Service: `backend/app/api/admin.py` + `backend/app/api/reports.py`

## Core Platform Capabilities

- JWT access/refresh auth, password hashing, login rate limiting.
- Profiles, follow graph, posts, likes, comments.
- Visibility enforcement (`public` or `followers`).
- City-based discovery feed with Redis caching and cursor pagination.
- Realtime chat (1-1 ready) with WebSocket ack path and Redis presence.
- Notification persistence + Redis queue worker.
- Media upload preparation flow with object storage key strategy.
- Verification state machine: `not_eligible`, `eligible`, `verified_earned`, `verified_paid`, `revoked`.
- Admin moderation endpoints with auditable action payloads.

## Data Layer

Primary: PostgreSQL (SQLAlchemy models)
Cache/Queue/Presence/Rate limits: Redis
Future-ready search boundary for Elasticsearch integration.

## Run locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker & Infra

Use `infra/docker-compose.yml` for local stack with API + Postgres + Redis + worker.

## Incremental Implementation Order

1. Core DB + Auth
2. Profile + Follow
3. Post + Media
4. Feed
5. Interactions
6. Chat
7. Notifications
8. Verification
9. Admin
10. Performance and scaling hardening
