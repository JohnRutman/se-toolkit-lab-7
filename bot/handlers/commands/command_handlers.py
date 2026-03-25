"""Command handlers for slash commands.

These handlers use the async API service (services/api.py) to communicate
with the LMS backend. They are plain async functions — same logic works
from --test mode, unit tests, or the Telegram bot.
"""

from services.api import APIError, check_health, fetch_items, fetch_pass_rates


async def handle_start(command: str, args: str = "") -> str:
    """Handle /start command — welcome message."""
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you check system health, browse labs, and view scores.\n\n"
        "Use /help to see all available commands."
    )


async def handle_help(command: str, args: str = "") -> str:
    """Handle /help command — list available commands."""
    return (
        "📚 Available Commands:\n\n"
        "/start — Welcome message\n"
        "/help — Show this help message\n"
        "/health — Check backend system status\n"
        "/labs — List available labs\n"
        "/scores <lab> — View scores for a specific lab\n\n"
        "You can also ask questions in plain language!"
    )


async def handle_health(command: str, args: str = "") -> str:
    """Handle /health command — backend status."""
    is_healthy, message, _ = await check_health()
    return message


async def handle_labs(command: str, args: str = "") -> str:
    """Handle /labs command — list available labs."""
    try:
        items = await fetch_items()
        labs = [item for item in items if item.type == "lab"]
        if not labs:
            return "No labs available."
        lines = ["Available labs:"]
        for lab in labs:
            lines.append(f"- {lab.title}")
        return "\n".join(lines)
    except APIError as e:
        return f"Failed to fetch labs: {e.message}"


async def handle_scores(command: str, args: str = "") -> str:
    """Handle /scores command — view scores for a lab."""
    lab_name = args.strip()
    if not lab_name:
        return "Please specify a lab, e.g., /scores lab-01"
    try:
        pass_rates = await fetch_pass_rates(lab_name)
        if not pass_rates:
            return f"No data available for {lab_name}."
        lines = [f"Pass rates for {lab_name}:"]
        for pr in pass_rates:
            task_name = pr.task or pr.title or "Unknown"
            rate = pr.pass_rate if pr.pass_rate is not None else 0
            attempts = pr.attempts or 0
            lines.append(f"- {task_name}: {rate:.1f}% ({attempts} attempts)")
        return "\n".join(lines)
    except APIError as e:
        return f"Failed to fetch scores: {e.message}"
