from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_redis
from app.db.session import get_db
from app.models.entities import Follower, User
from app.services.notification import create_notification

router = APIRouter(prefix="/follow", tags=["follow"])


@router.post("/{target_user_id}")
def follow_user(target_user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    if target_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    existing = db.scalar(select(Follower).where(Follower.follower_id == current_user.id, Follower.followee_id == target_user_id))
    if existing:
        return {"status": "already_following"}
    db.add(Follower(follower_id=current_user.id, followee_id=target_user_id))
    db.commit()
    create_notification(db, redis_client, target_user_id, "follow", {"from_user_id": current_user.id})
    return {"status": "followed"}
