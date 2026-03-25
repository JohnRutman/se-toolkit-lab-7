"""Command handlers for slash commands."""

import httpx
from config import config
from services.lms_client import LMSClient


def _get_lms_client() -> LMSClient:
    """Create an LMS client from config."""
    return LMSClient(config.lms_api_base_url, config.lms_api_key)


def handle_start(command: str, args: str = "") -> str:
    """Handle /start command — welcome message."""
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you check system health, browse labs, and view scores.\n\n"
        "Use /help to see all available commands."
    )


def handle_help(command: str, args: str = "") -> str:
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


def handle_health(command: str, args: str = "") -> str:
    """Handle /health command — backend status."""
    client = _get_lms_client()
    try:
        result = client.health_check()
        return f"🟢 Backend is healthy. {result['item_count']} items available."
    except ConnectionError as e:
        return f"🔴 Backend error: {e}"
    except httpx.HTTPStatusError as e:
        return f"🔴 Backend error: {e}"


def handle_labs(command: str, args: str = "") -> str:
    """Handle /labs command — list available labs."""
    client = _get_lms_client()
    try:
        items = client.get_items()
        if not items:
            return "📋 No labs available."
        
        # Filter only labs (not tasks) and extract titles
        labs = []
        for item in items:
            if item.get("type") == "lab":
                labs.append(item.get("title", "Unknown Lab"))
        
        if not labs:
            return "📋 No labs found."
        
        lines = ["📋 Available Labs:\n"]
        for lab_name in labs:
            lines.append(f"- {lab_name}")
        
        return "\n".join(lines)
    except ConnectionError as e:
        return f"🔴 Backend error: {e}"
    except httpx.HTTPStatusError as e:
        return f"🔴 Backend error: {e}"


def handle_scores(command: str, args: str = "") -> str:
    """Handle /scores command — view scores for a lab."""
    if not args:
        return "Please specify a lab, e.g., /scores lab-01"
    
    client = _get_lms_client()
    try:
        pass_rates = client.get_pass_rates(args)
        if not pass_rates:
            return f"📊 No pass rate data found for {args}."
        
        lines = [f"📊 Pass rates for {args}:"]
        for rate in pass_rates:
            task_name = rate.get("task", "Unknown Task")
            pass_rate = rate.get("avg_score", 0)
            attempts = rate.get("attempts", 0)
            lines.append(f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)")
        
        return "\n".join(lines)
    except ConnectionError as e:
        return f"🔴 Backend error: {e}"
    except httpx.HTTPStatusError as e:
        return f"🔴 Backend error: {e}"
