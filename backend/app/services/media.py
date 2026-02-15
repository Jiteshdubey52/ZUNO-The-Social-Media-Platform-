from uuid import uuid4

from app.core.config import settings


def make_media_object_key(user_id: int, media_type: str) -> str:
    return f"{user_id}/{media_type}/{uuid4()}"


def build_cdn_url(object_key: str) -> str:
    return f"{settings.media_cdn_base}/{object_key}"
