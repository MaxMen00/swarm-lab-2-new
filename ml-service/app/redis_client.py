import redis.asyncio as redis

from app.config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_APP_PASSWORD


def create_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        username=REDIS_USERNAME,
        password=REDIS_APP_PASSWORD,
        decode_responses=True,
    )