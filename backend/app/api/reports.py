from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Report, User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
def create_report(reason: str, target_post_id: int | None = None, target_user_id: int | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = Report(
        reporter_id=current_user.id,
        target_post_id=target_post_id,
        target_user_id=target_user_id,
        reason=reason,
    )
    db.add(report)
    db.commit()
    return {"report_id": report.id}
