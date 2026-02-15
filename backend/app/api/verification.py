from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import MonetizationMetric, User, Verification, VerificationState
from app.services.verification import compute_verification_state

router = APIRouter(prefix="/verification", tags=["verification"])


@router.get("/status")
def verification_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.get(Verification, current_user.id)
    metric = db.get(MonetizationMetric, current_user.id)
    eligible_state = compute_verification_state(metric)
    if record and record.state == VerificationState.NOT_ELIGIBLE and eligible_state == VerificationState.ELIGIBLE:
        record.state = eligible_state
        db.commit()
    return {
        "state": record.state.value if record else VerificationState.NOT_ELIGIBLE.value,
        "metrics": {
            "posts_count": metric.posts_count if metric else 0,
            "followers_count": metric.followers_count if metric else 0,
            "total_reach": metric.total_reach if metric else 0,
        },
    }


@router.post("/request")
def request_verification(note: str = "", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.get(Verification, current_user.id)
    record.request_note = note
    db.commit()
    return {"status": "submitted", "state": record.state.value}
