from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Media, User
from app.services.media import build_cdn_url, make_media_object_key

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/prepare-upload")
def prepare_upload(media_type: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if media_type not in {"image", "video"}:
        raise HTTPException(status_code=400, detail="Unsupported media type")
    object_key = make_media_object_key(current_user.id, media_type)
    media = Media(owner_id=current_user.id, media_type=media_type, object_key=object_key, cdn_url=build_cdn_url(object_key))
    db.add(media)
    db.commit()
    db.refresh(media)
    return {
        "media_id": media.id,
        "object_key": media.object_key,
        "upload_url": f"https://object-storage.example/upload/{media.object_key}",
        "cdn_url": media.cdn_url,
    }
