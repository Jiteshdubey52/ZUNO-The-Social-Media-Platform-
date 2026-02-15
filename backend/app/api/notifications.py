from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Notification, User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(limit: int = 50, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.scalars(
        select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.id.desc()).limit(limit)
    ).all()
    return notifications
