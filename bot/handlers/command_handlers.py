"""Command handlers for slash commands."""


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
    """Handle /health command — backend status (placeholder)."""
    # Task 2: Replace with real API call
    return "🟢 Backend is online (placeholder — will fetch real status in Task 2)"


def handle_labs(command: str, args: str = "") -> str:
    """Handle /labs command — list available labs (placeholder)."""
    # Task 2: Replace with real API call
    return (
        "📋 Available Labs:\n\n"
        "Lab 1 — Introduction\n"
        "Lab 2 — Basic Concepts\n"
        "Lab 3 — Advanced Topics\n\n"
        "(placeholder — will fetch real data in Task 2)"
    )


def handle_scores(command: str, args: str = "") -> str:
    """Handle /scores command — view scores for a lab (placeholder)."""
    # Task 2: Replace with real API call
    if args:
        return f"📊 Scores for {args}:\n\nTask 1: 80%\nTask 2: 75%\n\n(placeholder — will fetch real data in Task 2)"
    return "Please specify a lab, e.g., /scores lab-01"
