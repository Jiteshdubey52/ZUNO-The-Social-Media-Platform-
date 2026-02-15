from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Profile, User

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.get(Profile, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "city": profile.city,
        "bio": profile.bio,
    }
