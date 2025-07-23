import redis
from .settings import settings

redis_pool = redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True
)

def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)