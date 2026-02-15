from datetime import datetime, timezone

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_redis
from app.db.session import get_db
from app.models.entities import Message, User
from app.schemas.common import MessageCreate
from app.services.chat import set_presence

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/messages")
def send_message(payload: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = Message(
        conversation_id=payload.conversation_id,
        sender_id=current_user.id,
        body=payload.body,
        media_id=payload.media_id,
        delivered_at=datetime.now(tz=timezone.utc),
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message_id": message.id}


@router.get("/conversations/{conversation_id}/messages")
def list_messages(conversation_id: int, cursor_id: int | None = None, limit: int = 30, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(Message).where(Message.conversation_id == conversation_id)
    if cursor_id:
        query = query.where(Message.id < cursor_id)
    messages = db.scalars(query.order_by(Message.id.desc()).limit(limit)).all()
    return [{"id": m.id, "sender_id": m.sender_id, "body": m.body, "created_at": m.created_at.isoformat()} for m in messages]


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    redis_client = Redis.from_url("redis://redis:6379/0", decode_responses=True)
    set_presence(redis_client, user_id, True)
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"ack:{message}")
    except WebSocketDisconnect:
        set_presence(redis_client, user_id, False)
