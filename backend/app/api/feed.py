import json

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_redis
from app.db.session import get_db
from app.models.entities import User
from app.services.feed import build_feed_query, get_user_city

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("")
def get_feed(cursor_post_id: int | None = None, limit: int = 20, city: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    selected_city = city or get_user_city(db, current_user.id)
    cache_key = f"feed:{current_user.id}:{selected_city}:{cursor_post_id}:{limit}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"source": "cache", "items": json.loads(cached)}
    posts = db.scalars(build_feed_query(db, current_user.id, selected_city, cursor_post_id, limit)).all()
    items = [{"id": p.id, "author_id": p.author_id, "caption": p.caption, "city": p.city, "created_at": p.created_at.isoformat()} for p in posts]
    redis_client.setex(cache_key, 30, json.dumps(items))
    return {"source": "db", "items": items}
