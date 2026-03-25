#!/usr/bin/env python3
"""LMS Telegram Bot entry point.

Usage:
    uv run bot.py              # Start Telegram bot
    uv run bot.py --test "/command"  # Test mode (no Telegram connection)
"""

import argparse
import sys
from typing import Callable

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from config import config
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)


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


async def run_test_mode(command_text: str) -> None:
    """Run in test mode — call handler directly and print result."""
    command, args = parse_command(command_text)
    handler = get_handler(command)

    if handler is None:
        print(f"Unknown command: {command}")
        print("Available commands: /start, /help, /health, /labs, /scores")
        sys.exit(0)

    response = await handler(command, args)
    print(response)
    sys.exit(0)


async def handle_telegram_start(message: types.Message, bot: Bot) -> None:
    """Telegram handler for /start."""
    response = await handle_start("/start", "")
    await message.answer(response)


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


async def handle_telegram_message(message: types.Message, bot: Bot) -> None:
    """Handle plain text messages (Task 3: intent routing)."""
    # Task 3: Add LLM-based intent routing here
    response = "I understand you're asking about: " + message.text
    response += "\n\n(Task 3: I'll learn to route this to the right handler)"
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
    
    print("Bot is starting...")
    await dp.start_polling(bot)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        metavar="COMMAND",
        help="Test mode: run a command and print result (e.g., --test '/start')",
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
