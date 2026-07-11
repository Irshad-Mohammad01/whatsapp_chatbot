from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings validated using Pydantic Settings.
    Ensures fail-fast behavior if any required environment variable is missing.
    """
    VERIFY_TOKEN: str = Field(..., description="Meta Webhook Verification Token")
    WHATSAPP_ACCESS_TOKEN: str = Field(..., description="Access Token for WhatsApp Cloud API")
    PHONE_NUMBER_ID: str = Field(..., description="WhatsApp Business Phone Number ID")
    APP_SECRET: str = Field(..., description="Meta App Secret for HMAC Signature Verification")
    GEMINI_API_KEY: str = Field(..., description="API Key for Google Gemini API")

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model to use"
    )
    GEMINI_TEMPERATURE: float = Field(
        default=0.7,
        description="Gemini model temperature"
    )
    GEMINI_MAX_OUTPUT_TOKENS: int = Field(
        default=500,
        description="Gemini model max output tokens"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
