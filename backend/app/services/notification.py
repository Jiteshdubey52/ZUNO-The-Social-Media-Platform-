import json

from redis import Redis
from sqlalchemy.orm import Session

from app.models.entities import Notification


NOTIFICATION_QUEUE = "zuno:notifications:queue"


def create_notification(db: Session, redis_client: Redis, user_id: int, event_type: str, payload: dict) -> Notification:
    notif = Notification(user_id=user_id, event_type=event_type, payload_json=payload)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    redis_client.rpush(NOTIFICATION_QUEUE, json.dumps({"notification_id": notif.id, "user_id": user_id}))
    return notif
