from datetime import datetime

import redis

from app.core.config import settings


class LocalStorage:
    def __init__(self):
        self.storage = {}

    def set_key(self, key_name, time, data):
        self.storage[key_name] = {
            "expire_at": f"{datetime.now() + time}",
            "long_url": f"{data}",
        }

    def get_long_url(self, key_name):
        if key_name in self.storage:
            key_value = self.storage[key_name].get("long_url")
            self.update_keys(key_name)
        else:
            key_value = None

        return key_value

    def update_keys(self, key_name):
        if (
            datetime.strptime(
                self.storage[key_name].get("expire_at"), "%Y-%m-%d %H:%M:%S.%f"
            )
            < datetime.now()
        ):
            self.storage.pop(key_name, None)


class RedisStorage:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_URL,
            port=settings.REDIS_PORT,
            socket_connect_timeout=settings.REDIS_SOCKET_TIMEOUT,
            decode_responses=True,
        )

    def get_long_url(self, key_name):
        return self.r.get(key_name)

    def set_key(self, key_name, time, data):
        self.r.setex(key_name, time, value=f"{data}")


storage = RedisStorage() if settings.REDIS_CONNECTION else LocalStorage()
