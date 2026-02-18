import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.api_client import MaxApiClient
from app.services.redis_client import RedisClient
from app.schemas.payloads import NormalizedMessage
from app.handlers.user import UserHandler

logger = logging.getLogger(__name__)


async def route_update(
    message: NormalizedMessage, 
    api: MaxApiClient, 
    db: AsyncSession, 
    redis: RedisClient
):
    """
    Routes the normalized message to the appropriate handler.
    """
    try:
        handler = UserHandler(api, db, redis)
        
        if message.is_callback:
            await handler.handle_callback(message)
        else:
            await handler.handle_message(message)
            
    except Exception as e:
        logger.exception(f"Error routing update: {e}")
