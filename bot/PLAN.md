# LMS Telegram Bot — Development Plan

## Overview

This document outlines the development plan for building a Telegram bot that integrates with the LMS backend. The bot allows users to check system health, browse labs and scores, and ask questions in plain language using an LLM for intent routing.

## Architecture

The bot follows a **layered architecture** with clear separation of concerns:

1. **Entry point** (`bot.py`) — Handles Telegram bot startup and `--test` mode for offline testing
2. **Handlers** (`handlers/`) — Command logic as pure functions that take input and return text
3. **Services** (`services/`) — API client for LMS backend and LLM client for natural language understanding
4. **Configuration** (`config.py`) — Environment variable loading using pydantic-settings

The key design principle is **testable handlers**: handler functions don't depend on Telegram. They can be called from `--test` mode, unit tests, or the Telegram bot — same logic, different entry points.

## Task 1: Scaffold and Test Mode

Create the project skeleton with `--test` mode support. Handlers return placeholder text. The goal is to verify the architecture works before adding real functionality.

**Deliverables:**
- `bot/bot.py` — Entry point with `--test` flag
- `bot/handlers/` — Handler modules for `/start`, `/help`, `/health`, `/labs`, `/scores`
- `bot/config.py` — Configuration loading from `.env.bot.secret`
- `bot/PLAN.md` — This development plan

## Task 2: Backend Integration

Replace placeholder handlers with real API calls. Each handler fetches data from the LMS backend using Bearer token authentication.

**Deliverables:**
- `bot/services/lms_client.py` — HTTP client for LMS API
- Update handlers to call real endpoints (`/items`, `/analytics`, `/sync`)
- Error handling for backend failures (friendly messages, not crashes)

## Task 3: Intent-Based Natural Language Routing

Add LLM-powered intent routing so users can ask questions in plain language. The LLM receives tool descriptions and decides which handler to call.

**Deliverables:**
- `bot/services/llm_client.py` — LLM client for tool calling
- `bot/handlers/intent_router.py` — Routes plain text to appropriate handlers via LLM
- Tool definitions for all 9 backend endpoints
- System prompt for intent classification

## Task 4: Containerize and Deploy

Package the bot in Docker and deploy alongside the existing backend on the VM.

**Deliverables:**
- `bot/Dockerfile` — Container image definition
- Update `docker-compose.yml` to add bot service
- Documentation in README
- Verification that bot responds in Telegram

## Testing Strategy

- **Test mode**: `uv run bot.py --test "/command"` for offline verification
- **Telegram testing**: Manual testing after deployment
- **Error scenarios**: Backend down, invalid input, LLM failures

## Environment Variables

- `BOT_TOKEN` — Telegram bot authentication
- `LMS_API_BASE_URL` — LMS backend URL
- `LMS_API_KEY` — LMS API authentication
- `LLM_API_KEY` — LLM service authentication
- `LLM_API_BASE_URL` — LLM service URL
