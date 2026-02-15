from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.entities import Follower, Post, Profile, Visibility


def build_feed_query(db: Session, user_id: int, city: str | None, cursor_post_id: int | None, limit: int = 20) -> Select:
    following_subq = select(Follower.followee_id).where(Follower.follower_id == user_id)
    query = select(Post).where(Post.is_deleted.is_(False))
    query = query.where(
        (Post.visibility == Visibility.PUBLIC)
        | ((Post.visibility == Visibility.FOLLOWERS) & (Post.author_id.in_(following_subq)))
        | (Post.author_id == user_id)
    )
    if city:
        query = query.where(Post.city == city)
    if cursor_post_id:
        query = query.where(Post.id < cursor_post_id)
    return query.order_by(Post.id.desc()).limit(limit)


def get_user_city(db: Session, user_id: int) -> str | None:
    profile = db.get(Profile, user_id)
    return profile.city if profile else None
