from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_redis
from app.db.session import get_db
from app.models.entities import Comment, Like, Post, User
from app.schemas.common import CommentCreate
from app.services.notification import create_notification

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/posts/{post_id}/like")
def like_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    post = db.get(Post, post_id)
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    existing = db.scalar(select(Like).where(Like.user_id == current_user.id, Like.post_id == post_id))
    if existing:
        return {"status": "already_liked"}
    db.add(Like(user_id=current_user.id, post_id=post_id))
    db.commit()
    if post.author_id != current_user.id:
        create_notification(db, redis_client, post.author_id, "like", {"from_user_id": current_user.id, "post_id": post.id})
    return {"status": "liked"}


@router.post("/posts/{post_id}/comments")
def add_comment(post_id: int, payload: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    post = db.get(Post, post_id)
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(user_id=current_user.id, post_id=post_id, text=payload.text)
    db.add(comment)
    db.commit()
    if post.author_id != current_user.id:
        create_notification(db, redis_client, post.author_id, "comment", {"from_user_id": current_user.id, "post_id": post.id})
    return {"comment_id": comment.id}
