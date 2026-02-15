from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.entities import MonetizationMetric, Post, Report, User, Verification, VerificationState

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/reports")
def list_reports(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.scalars(select(Report).order_by(Report.id.desc()).limit(100)).all()


@router.post("/posts/{post_id}/remove")
def remove_post(post_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_deleted = True
    db.commit()
    return {"status": "removed", "audit": {"action": "remove_post", "post_id": post_id}}


@router.post("/users/{user_id}/block")
def block_user(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"status": "blocked", "audit": {"action": "block_user", "user_id": user_id}}


@router.post("/verification/{user_id}")
def set_verification(user_id: int, new_state: VerificationState, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    record = db.get(Verification, user_id)
    if not record:
        raise HTTPException(status_code=404, detail="Verification record missing")
    record.state = new_state
    db.commit()
    return {"status": "updated", "audit": {"action": "set_verification", "user_id": user_id, "state": new_state.value}}


@router.get("/suspicious-growth")
def suspicious_growth(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.scalars(select(MonetizationMetric).where(MonetizationMetric.suspicious_growth_score > 70).limit(100)).all()
