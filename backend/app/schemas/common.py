from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    city: str = Field(min_length=2, max_length=120)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    caption: str = Field(max_length=500)
    media_id: int
    visibility: str
    city: str


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=600)


class MessageCreate(BaseModel):
    conversation_id: int
    body: str = Field(max_length=1000)
    media_id: int | None = None


class NotificationOut(BaseModel):
    id: int
    event_type: str
    payload_json: dict
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
