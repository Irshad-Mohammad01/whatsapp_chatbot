import httpx
from app.config import settings
from app.exceptions import WhatsAppAPIError


class WhatsAppClient:
    """
    Client for interacting with the Meta WhatsApp Cloud API.
    Handles authentication headers and sending messages asynchronously.
    """
    def __init__(self) -> None:
        self.base_url = f"https://graph.facebook.com/v20.0/{settings.PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    async def send_whatsapp_message(self, recipient_phone: str, message_text: str) -> dict:
        """
        Sends a text message to a WhatsApp user.
        Raises WhatsAppAPIError if the API request fails or returns an error.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=self.headers
                )
                response_data = response.json()
            except httpx.HTTPStatusError as exc:
                raise WhatsAppAPIError(f"HTTP error status: {exc.response.status_code}")
            except httpx.RequestError as exc:
                raise WhatsAppAPIError(f"Request connection failed: {str(exc)}")
            except Exception as exc:
                raise WhatsAppAPIError(f"Unexpected error: {str(exc)}")

            if response.status_code != 200:
                error_msg = response_data.get("error", {}).get("message", "Unknown Meta API error")
                raise WhatsAppAPIError(error_msg, status_code=response.status_code)

            return response_data
