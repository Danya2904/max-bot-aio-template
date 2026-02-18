from typing import Optional
from pydantic import BaseModel, Field


class Sender(BaseModel):
    user_id: int
    name: Optional[str] = None


class Recipient(BaseModel):
    chat_id: int


class NormalizedMessage(BaseModel):
    chat_id: int
    user_id: int
    message_id: int
    text: Optional[str] = None
    payload: Optional[str] = None  # For callback data

    @property
    def is_callback(self) -> bool:
        """Returns True if the message is a callback (has payload)."""
        return self.payload is not None
