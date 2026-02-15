import json
import time

from redis import Redis

from app.core.config import settings
from app.services.notification import NOTIFICATION_QUEUE


def run_worker() -> None:
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    while True:
        item = redis_client.lpop(NOTIFICATION_QUEUE)
        if not item:
            time.sleep(0.25)
            continue
        payload = json.loads(item)
        print(f"dispatch notification {payload}")


if __name__ == "__main__":
    run_worker()
