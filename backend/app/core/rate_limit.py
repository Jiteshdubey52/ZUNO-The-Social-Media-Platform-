from fastapi import HTTPException, Request, status
from redis import Redis

from app.core.config import settings


def get_rate_key(prefix: str, request: Request) -> str:
    client_ip = request.client.host if request.client else "unknown"
    return f"{prefix}:{client_ip}"


def enforce_rate_limit(redis_client: Redis, prefix: str, request: Request, limit: int | None = None) -> None:
    key = get_rate_key(prefix, request)
    cap = limit or settings.rate_limit_per_minute
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, 60)
    if current > cap:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
