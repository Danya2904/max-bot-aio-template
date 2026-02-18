import logging
from typing import Optional, Dict, Any, List
import aiohttp
from app.core.config import settings

logger = logging.getLogger(__name__)


class MaxApiClient:
    """
    Client for interacting with the MAX Messenger API.
    Handles authentication, updates, and sending messages.
    """

    def __init__(self, token: str = settings.MAX_BOT_TOKEN, base_url: str = settings.MAX_API_URL):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Internal method to handle API requests with authorization headers.
        """
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            async with session.request(method, url, params=params, json=json, headers=headers) as response:
                response_data = await response.json()
                if not response.ok:
                    logger.error(f"API request failed: {method} {url} - {response.status} - {response_data}")
                    response.raise_for_status()
                return response_data
        except Exception as e:
            logger.exception(f"Exception during request to {url}: {e}")
            raise

    async def get_updates(self, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve new updates from the MAX platform.
        """
        params = {"offset": offset}
        data = await self._request("GET", "updates", params=params)
        return data.get("updates", [])

    async def send_message(self, chat_id: int, text: str, keyboard: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a text message to a specific chat.
        """
        payload = {
            "recipient": {"chat_id": chat_id},
            "message": {"text": text}
        }
        if keyboard:
            payload["message"]["keyboard"] = keyboard
            
        return await self._request("POST", "messages", json=payload)

    async def answer_callback(self, callback_id: str, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Answer a callback query from an inline button.
        """
        payload = {"callback_id": callback_id}
        if text:
            payload["text"] = text
            
        return await self._request("POST", "answers", json=payload)

    async def close(self):
        """Close the underlying aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()


# Global instance
max_api = MaxApiClient()
