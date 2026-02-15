from redis import Redis


def set_presence(redis_client: Redis, user_id: int, is_online: bool) -> None:
    key = f"presence:{user_id}"
    if is_online:
        redis_client.setex(key, 120, "1")
    else:
        redis_client.delete(key)


def is_online(redis_client: Redis, user_id: int) -> bool:
    return redis_client.exists(f"presence:{user_id}") == 1
