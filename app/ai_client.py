from google import genai
from google.genai import types
from google.genai import errors

from app.config import settings
from app.exceptions import GeminiAPIError


class GeminiClient:
    """
    Client wrapper for communicating with Google Gemini API asynchronously.
    """
    def __init__(self) -> None:
        # Initialize the Google Gen AI client with the Gemini API key
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_ai_response(self, user_message: str, sender_name: str) -> str:
        """
        Sends the user message along with sender context to Gemini and fetches the response.
        Raises GeminiAPIError if any API, network, or validation exception occurs.
        """
        try:
            # Using gemini-2.5-flash as the default model (fast, multi-modal, and large context)
            response = await self.client.aio.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        f"You are a helpful customer service assistant for SSJewellery. "
                        f"You are talking to {sender_name}. Keep responses polite, concise, and helpful."
                    ),
                    temperature=0.7,
                    max_output_tokens=500
                )
            )

            ai_text = response.text
            if not ai_text:
                raise GeminiAPIError("Received empty text response from Gemini API.")

            return ai_text.strip()

        except errors.APIError as exc:
            raise GeminiAPIError(f"Gemini API call failed: {str(exc)}")
        except Exception as exc:
            raise GeminiAPIError(f"Failed to communicate with Gemini: {str(exc)}")


# Alias to maintain architecture and webhook compatibility without modification
OpenAIClient = GeminiClient
