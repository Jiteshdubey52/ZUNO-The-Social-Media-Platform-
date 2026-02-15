from fastapi import FastAPI

from app.api import admin, auth, chat, feed, follow, interactions, media, notifications, post, profile, reports, verification
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title="ZUNO API", version="1.0.0")

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(profile.router)
    app.include_router(follow.router)
    app.include_router(media.router)
    app.include_router(post.router)
    app.include_router(feed.router)
    app.include_router(interactions.router)
    app.include_router(chat.router)
    app.include_router(notifications.router)
    app.include_router(reports.router)
    app.include_router(verification.router)
    app.include_router(admin.router)
    return app


app = create_app()
