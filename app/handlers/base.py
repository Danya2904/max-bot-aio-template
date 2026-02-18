from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.api_client import MaxApiClient
from app.services.redis_client import RedisClient
from app.schemas.payloads import NormalizedMessage


class BaseHandler:
    def __init__(self, api: MaxApiClient, db: AsyncSession, redis: RedisClient):
        self.api = api
        self.db = db
        self.redis = redis

    async def answer(self, message: NormalizedMessage, text: str, keyboard: Optional[Dict[str, Any]] = None):
        """Wraps api.send_message to reply to the current message's chat."""
        return await self.api.send_message(
            chat_id=message.chat_id,
            text=text,
            keyboard=keyboard
        )
