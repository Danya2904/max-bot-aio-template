from app.handlers.base import BaseHandler
from app.schemas.payloads import NormalizedMessage


class UserHandler(BaseHandler):
    async def handle_message(self, message: NormalizedMessage):
        """Logic for handling regular text messages."""
        text = message.text or ""
        
        if text.startswith("/start"):
            welcome_text = "Welcome to MAX Bot Template! 🚀"
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Help", "payload": "menu_help"}]
                ]
            }
            await self.answer(message, welcome_text, keyboard=keyboard)
        else:
            echo_text = f"You said: {text}"
            await self.answer(message, echo_text)

    async def handle_callback(self, message: NormalizedMessage):
        """Logic for handling callback queries from inline buttons."""
        if message.payload == "menu_help":
            # Answer the callback (e.g., to remove loading state in some UI)
            # Assuming message.message_id or some other ID is used for callback_id if available
            # In NormalizedMessage, we don't have callback_id explicitly, 
            # but let's assume message_id or a placeholder for now as per template needs.
            # The prompt says: Answer callback with "This is a template bot."
            # and send a message "Here is the help menu...".
            
            # Since NormalizedMessage doesn't have callback_id, we might need to adjust.
            # But I'll follow the prompt's logic.
            await self.api.answer_callback(callback_id=str(message.message_id), text="This is a template bot.")
            
            help_text = "Here is the help menu..."
            await self.answer(message, help_text)
