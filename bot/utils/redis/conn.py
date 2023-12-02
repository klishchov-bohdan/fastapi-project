import redis
from data.config import REDIS_SERVER_BOT, REDIS_PORT_BOT


def new_redis_conn():
    return redis.Redis(
        host=REDIS_SERVER_BOT,
        port=REDIS_PORT_BOT,
    )
