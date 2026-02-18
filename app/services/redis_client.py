import logging
from typing import Optional, Dict, Any
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis client with a "Fail Open" mechanism.
    If Redis is unreachable, it falls back to a local in-memory dictionary.
    """

    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis_url = redis_url
        self._redis: Optional[redis.Redis] = None
        self._local_storage: Dict[str, str] = {}
        self._is_connected = False

    async def connect(self):
        """Initialize Redis connection."""
        try:
            self._redis = redis.from_url(
                self.redis_url, 
                encoding="utf-8", 
                decode_responses=True,
                socket_timeout=2.0,
                socket_connect_timeout=2.0
            )
            # Test connection
            await self._redis.ping()
            self._is_connected = True
            logger.info("Successfully connected to Redis.")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            self._is_connected = False
            logger.error(f"Failed to connect to Redis: {e}. Using local in-memory storage fallback.")

    async def _ensure_connection(self):
        if self._redis is None:
            await self.connect()

    async def set_state(self, user_id: int, state: str, ex: Optional[int] = None) -> bool:
        """Set user state in Redis or local storage."""
        await self._ensure_connection()
        key = f"user_state:{user_id}"
        
        if self._is_connected and self._redis:
            try:
                await self._redis.set(key, state, ex=ex)
                return True
            except (redis.ConnectionError, redis.TimeoutError) as e:
                logger.error(f"Redis set_state error: {e}. Falling back to local storage.")
                self._is_connected = False

        # Fallback to local storage
        self._local_storage[key] = state
        return True

    async def get_state(self, user_id: int) -> Optional[str]:
        """Get user state from Redis or local storage."""
        await self._ensure_connection()
        key = f"user_state:{user_id}"

        if self._is_connected and self._redis:
            try:
                return await self._redis.get(key)
            except (redis.ConnectionError, redis.TimeoutError) as e:
                logger.error(f"Redis get_state error: {e}. Falling back to local storage.")
                self._is_connected = False

        # Fallback to local storage
        return self._local_storage.get(key)

    async def delete_state(self, user_id: int) -> bool:
        """Delete user state from Redis and local storage."""
        await self._ensure_connection()
        key = f"user_state:{user_id}"
        
        success = True
        if self._is_connected and self._redis:
            try:
                await self._redis.delete(key)
            except (redis.ConnectionError, redis.TimeoutError) as e:
                logger.error(f"Redis delete_state error: {e}. Falling back to local storage.")
                self._is_connected = False
                success = False

        # Always try to remove from local storage too
        if key in self._local_storage:
            del self._local_storage[key]
            
        return success

    async def close(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._is_connected = False


# Global instance
redis_client = RedisClient()
