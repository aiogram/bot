from typing import Optional

import aioredis


class BaseRedis:
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db

        self._redis: Optional[aioredis.Redis] = None

    @property
    def closed(self):
        return not self._redis

    async def connect(self):
        if self.closed:
            self._redis = await aioredis.from_url(f"redis://{self.host}:{self.port}/{self.db}")

    async def disconnect(self):
        if not self.closed:
            await self._redis.close()

    @property
    def redis(self) -> aioredis.Redis:
        if self.closed:
            raise RuntimeError("Redis connection is not opened")
        return self._redis
