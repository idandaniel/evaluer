from functools import lru_cache

from fastapi import Depends
import redis

from evaluer.core.settings import get_settings
from evaluer.services.cache import CacheService


@lru_cache
def get_redis_client() -> redis.Redis:
    settings = get_settings()
    return redis.from_url(settings.redis.url)


def get_cache_service(
    redis_client: redis.Redis = Depends(get_redis_client),
) -> CacheService:
    settings = get_settings()
    return CacheService(redis_client=redis_client, ttl=settings.redis.cache_ttl)
