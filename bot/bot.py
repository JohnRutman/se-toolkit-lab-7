#!/usr/bin/env python3
"""LMS Telegram Bot entry point.

Usage:
    uv run bot.py              # Start Telegram bot
    uv run bot.py --test "message"  # Test mode (no Telegram connection)
"""

import argparse
import sys
from typing import Callable

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import config
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)
from services.llm_client import LLMClient


def parse_command(text: str) -> tuple[str, str]:
    """Parse a command string into command and args.

    Example: "/scores lab-01" -> ("/scores", "lab-01")
    """
    parts = text.strip().split(maxsplit=1)
    command = parts[0] if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    return command, args


def get_handler(command: str) -> Callable[[str, str], str]:
    """Get the handler function for a command."""
    handlers = {
        "/start": handle_start,
        "/help": handle_help,
        "/health": handle_health,
        "/labs": handle_labs,
        "/scores": handle_scores,
    }
    return handlers.get(command)


async def run_test_mode(message_text: str) -> None:
    """Run in test mode — use LLM intent routing for plain text."""
    # Check if it's a slash command
    if message_text.startswith("/"):
        command, args = parse_command(message_text)
        handler = get_handler(command)

        if handler is None:
            print(f"Unknown command: {command}")
            print("Available commands: /start, /help, /health, /labs, /scores")
            sys.exit(0)

        response = await handler(command, args)
        print(response)
    else:
        # Plain text — use LLM intent routing
        if not config.llm_api_key or not config.llm_api_base_url:
            print("Error: LLM_API_KEY or LLM_API_BASE_URL not set in .env.bot.secret")
            sys.exit(1)

        llm = LLMClient(config.llm_api_base_url, config.llm_api_key, config.llm_api_model)
        response = llm.chat(message_text, debug=True)
        print(response)

    sys.exit(0)


async def handle_telegram_start(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /start."""
    response = await handle_start("/start", "")

    # Add inline keyboard buttons for common actions
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏥 Health", callback_data="health"),
                InlineKeyboardButton(text="📚 Labs", callback_data="labs"),
            ],
            [
                InlineKeyboardButton(text="📊 Scores", callback_data="scores"),
                InlineKeyboardButton(text="❓ Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton(text="🏆 Top Learners", callback_data="top_learners"),
                InlineKeyboardButton(text="📈 Pass Rates", callback_data="pass_rates"),
            ],
        ]
    )

    await message.answer(response, reply_markup=keyboard)


async def handle_telegram_help(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /help."""
    response = await handle_help("/help", "")
    await message.answer(response)


async def handle_telegram_health(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /health."""
    response = await handle_health("/health", "")
    await message.answer(response)


async def handle_telegram_labs(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /labs."""
    response = await handle_labs("/labs", "")
    await message.answer(response)


async def handle_telegram_scores(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /scores."""
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    response = await handle_scores("/scores", args)
    await message.answer(response)


async def handle_telegram_callback(message: types.CallbackQuery, bot: Bot) -> None:
    """Handle inline keyboard button callbacks."""
    action = message.data

    if action == "health":
        response = await handle_health("/health", "")
    elif action == "labs":
        response = await handle_labs("/labs", "")
    elif action == "help":
        response = await handle_help("/help", "")
    elif action == "scores":
        response = "Please use /scores <lab-name> to view scores, e.g., /scores lab-01"
    elif action == "top_learners":
        response = "Please ask: 'who are the top 5 students in lab-01?'"
    elif action == "pass_rates":
        response = "Please ask: 'what are the pass rates for lab-01?'"
    else:
        response = "Unknown action."

    await message.answer(response)


async def handle_telegram_message(message: types.Message, bot: Bot) -> None:
    """Handle plain text messages with LLM-based intent routing."""
    if not config.llm_api_key or not config.llm_api_base_url:
        await message.answer("LLM configuration is missing. Please contact the administrator.")
        return

    llm = LLMClient(config.llm_api_base_url, config.llm_api_key, config.llm_api_model)
    response = llm.chat(message.text, debug=False)
    await message.answer(response)


async def run_telegram_bot() -> None:
    """Start the Telegram bot."""
    if not config.bot_token:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        print("Copy .env.bot.example to .env.bot.secret and fill in your bot token")
        sys.exit(1)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    # Register handlers
    dp.message.register(handle_telegram_start, CommandStart())
    dp.message.register(handle_telegram_help, Command("help"))
    dp.message.register(handle_telegram_health, Command("health"))
    dp.message.register(handle_telegram_labs, Command("labs"))
    dp.message.register(handle_telegram_scores, Command("scores"))
    dp.message.register(handle_telegram_message)  # Plain text messages
    dp.callback_query.register(handle_telegram_callback)  # Inline keyboard callbacks

    print("Bot is starting...")
    await dp.start_polling(bot)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        metavar="MESSAGE",
        help="Test mode: send a message and print result (e.g., --test 'what labs are available')",
    )

    args = parser.parse_args()

    if args.test:
        import asyncio
        asyncio.run(run_test_mode(args.test))
    else:
        import asyncio
        asyncio.run(run_telegram_bot())


if __name__ == "__main__":
    main()
