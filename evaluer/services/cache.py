import json
from typing import Any, Optional

import redis


class CacheService:
    def __init__(self, redis_client: redis.Redis, ttl: int):
        self.redis_client = redis_client
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        cached_data = self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expire_time = ttl if ttl is not None else self.ttl
        self.redis_client.setex(key, expire_time, json.dumps(value, default=str))

    def delete(self, key: str) -> bool:
        return bool(self.redis_client.delete(key))

    def exists(self, key: str) -> bool:
        return bool(self.redis_client.exists(key))

    def get_or_set(
        self, key: str, factory_func: callable, ttl: Optional[int] = None
    ) -> Any:
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value

        new_value = factory_func()
        self.set(key, new_value, ttl)
        return new_value

    def invalidate_pattern(self, pattern: str) -> int:
        keys = self.redis_client.keys(pattern)
        if keys:
            return self.redis_client.delete(*keys)
        return 0

    def clear_all(self) -> None:
        self.redis_client.flushdb()
