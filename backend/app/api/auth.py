from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import enforce_rate_limit
from app.core.security import create_token, hash_password, verify_password
from app.db.session import get_db, get_redis
from app.models.entities import MonetizationMetric, Profile, User, Verification
from app.schemas.common import TokenPair, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> TokenPair:
    existing = db.scalar(select(User).where((User.email == payload.email) | (User.username == payload.username)))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already exists")
    user = User(email=payload.email, username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()
    db.add(Profile(user_id=user.id, city=payload.city))
    db.add(Verification(user_id=user.id))
    db.add(MonetizationMetric(user_id=user.id))
    db.commit()
    return TokenPair(
        access_token=create_token(str(user.id), settings.access_token_exp_minutes, "access"),
        refresh_token=create_token(str(user.id), settings.refresh_token_exp_minutes, "refresh"),
    )


@router.post("/login", response_model=TokenPair)
def login(email: str, password: str, request: Request, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)) -> TokenPair:
    enforce_rate_limit(redis_client, "login", request, limit=10)
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenPair(
        access_token=create_token(str(user.id), settings.access_token_exp_minutes, "access"),
        refresh_token=create_token(str(user.id), settings.refresh_token_exp_minutes, "refresh"),
    )
