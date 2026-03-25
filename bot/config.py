"""Configuration loading from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory containing this config file
BOT_DIR = Path(__file__).resolve().parent


class BotConfig(BaseSettings):
    """Bot configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=BOT_DIR / ".env.bot.secret",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram
    bot_token: str = ""

    # LMS API
    lms_api_base_url: str = "http://localhost:42002"
    lms_api_key: str = ""

    # LLM API
    llm_api_key: str = ""
    llm_api_base_url: str = ""
    llm_api_model: str = "coder-model"


config = BotConfig()
