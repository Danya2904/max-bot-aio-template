import asyncio
import logging
import sys
from typing import Dict, Any, Optional

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal
from app.handlers.router import route_update
from app.services.api_client import max_api as api
from app.services.redis_client import redis_client
from app.schemas.payloads import NormalizedMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def normalize_update(update: Dict[str, Any]) -> Optional[NormalizedMessage]:
    """
    Normalizes raw MAX API updates into a unified NormalizedMessage model.
    """
    update_type = update.get("type")
    data = update.get("data", {})

    if update_type == "message_created":
        message = data.get("message", {})
        sender = message.get("sender", {})
        recipient = message.get("recipient", {})
        body = message.get("body", {})
        
        return NormalizedMessage(
            chat_id=recipient.get("chat_id"),
            user_id=sender.get("user_id"),
            message_id=message.get("message_id"),
            text=body.get("text")
        )

    elif update_type == "message_callback":
        callback = data.get("callback", {})
        user = callback.get("user", {})
        # Note: In callbacks, chat_id might be in a different field depending on API version, 
        # usually it's passed or available in the callback context. 
        # For this template, we assume it's provided or mapped from user/callback.
        return NormalizedMessage(
            chat_id=data.get("chat_id", user.get("user_id")), # Fallback to user_id as chat_id
            user_id=user.get("user_id"),
            message_id=callback.get("message_id", 0),
            payload=callback.get("payload")
        )

    elif update_type == "bot_started":
        # Handle Deep Linking
        user = data.get("user", {})
        return NormalizedMessage(
            chat_id=user.get("user_id"),
            user_id=user.get("user_id"),
            message_id=0,
            text=f"/start {data.get('payload', '')}".strip()
        )

    return None


async def start_polling():
    """
    Main polling loop to fetch and process updates.
    """
    offset = 0
    logger.info("Starting bot polling...")
    
    # Ignore these types for processing, just log them
    ignored_types = {"user_added", "user_removed", "chat_created"}

    try:
        while True:
            try:
                updates = await max_api.get_updates(offset=offset)
                
                for update in updates:
                    update_id = update.get("update_id")
                    if update_id:
                        offset = update_id + 1

                    update_type = update.get("type")
                    
                    if update_type in ignored_types:
                        logger.info(f"Received ignored update type: {update_type}")
                        continue

                    normalized = normalize_update(update)
                    if normalized:
                        # Create a new DB session for this update
                        async with AsyncSessionLocal() as session:
                            await route_update(normalized, api, session, redis_client)
                    else:
                        logger.warning(f"Could not normalize update: {update_type}")

            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

            await asyncio.sleep(0.5)  # Short delay between polls
    except asyncio.CancelledError:
        logger.info("Polling task cancelled.")


async def main():
    """
    Entry point for the application.
    Initializes services and starts the bot.
    """
    # 1. Initialize Redis
    await redis_client.connect()
    
    # 2. Database connection check (optional but recommended)
    try:
        async with engine.begin() as conn:
            logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")

    try:
        # 3. Start Polling
        await start_polling()
    finally:
        # 4. Cleanup
        await api.close()
        await redis_client.close()
        await engine.dispose()
        logger.info("Bot services shut down.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
