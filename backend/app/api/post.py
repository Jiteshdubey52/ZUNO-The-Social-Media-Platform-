from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Media, Post, User, Visibility
from app.schemas.common import PostCreate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("")
def create_post(payload: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    media = db.get(Media, payload.media_id)
    if not media or media.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Invalid media ownership")
    if payload.visibility not in {Visibility.PUBLIC.value, Visibility.FOLLOWERS.value}:
        raise HTTPException(status_code=400, detail="Invalid visibility")
    post = Post(
        author_id=current_user.id,
        caption=payload.caption,
        media_id=payload.media_id,
        visibility=Visibility(payload.visibility),
        city=payload.city,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"post_id": post.id}


@router.delete("/{post_id}")
def soft_delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_deleted = True
    db.commit()
    return {"status": "deleted"}
