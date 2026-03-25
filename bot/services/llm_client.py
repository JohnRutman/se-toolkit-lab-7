"""LLM client with tool calling support for intent routing."""

import json
import sys
from typing import Any

import httpx

from config import config


class LLMClient:
    """HTTP client for the LLM API with tool calling support."""

    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout=60.0,
        )

    def get_tools(self) -> list[dict[str, Any]]:
        return [
            {"type": "function", "function": {"name": "get_items", "description": "Get a list of all labs and tasks available in the system", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "get_learners", "description": "Get a list of enrolled learners and their groups", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution (4 buckets) for a specific lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}}, "required": ["lab"]}}},
            {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task average scores and attempt counts for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}}, "required": ["lab"]}}},
            {"type": "function", "function": {"name": "get_timeline", "description": "Get submission timeline (submissions per day) for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}}, "required": ["lab"]}}},
            {"type": "function", "function": {"name": "get_groups", "description": "Get per-group scores and student counts for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}}, "required": ["lab"]}}},
            {"type": "function", "function": {"name": "get_top_learners", "description": "Get top N learners by score for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}, "limit": {"type": "integer", "description": "Number of top learners to return, e.g., 5, 10"}}, "required": ["lab", "limit"]}}},
            {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion rate percentage for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01', 'lab-04'"}}, "required": ["lab"]}}},
            {"type": "function", "function": {"name": "trigger_sync", "description": "Trigger a data sync from the autochecker to refresh data", "parameters": {"type": "object", "properties": {}, "required": []}}},
        ]

    def _execute_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        from services.lms_client import LMSClient
        lms = LMSClient(config.lms_api_base_url, config.lms_api_key)
        if name == "get_items": return lms.get_items()
        elif name == "get_learners": return lms.get_learners()
        elif name == "get_scores": return lms.get_scores(arguments.get("lab", ""))
        elif name == "get_pass_rates": return lms.get_pass_rates(arguments.get("lab", ""))
        elif name == "get_timeline": return lms.get_timeline(arguments.get("lab", ""))
        elif name == "get_groups": return lms.get_groups(arguments.get("lab", ""))
        elif name == "get_top_learners": return lms.get_top_learners(arguments.get("lab", ""), arguments.get("limit", 5))
        elif name == "get_completion_rate": return lms.get_completion_rate(arguments.get("lab", ""))
        elif name == "trigger_sync": return lms.trigger_sync()
        else: return {"error": f"Unknown tool: {name}"}

    def chat(self, user_message: str, debug: bool = False) -> str:
        tools = self.get_tools()
        system_prompt = """You are a helpful assistant for a Learning Management System (LMS) Telegram bot.
You have access to tools that fetch data from the backend API.

When a user asks a question:
1. Think about what information you need to answer
2. Call the appropriate tool(s) to get that data
3. Use the tool results to formulate a helpful, accurate response
4. If the user's message is gibberish or unclear, provide a helpful response explaining what you can do
5. If the user greets you, respond warmly and mention you can help with labs, scores, and analytics

Always call tools when you need data. Don't make up numbers - use the tool results.
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}]
        max_iterations = 10
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            response = self._client.post("/chat/completions", json={"model": self.model, "messages": messages, "tools": tools, "tool_choice": "auto"})
            if response.status_code != 200:
                if debug: print(f"[LLM] HTTP {response.status_code}: {response.text}", file=sys.stderr)
                return f"LLM error: HTTP {response.status_code}"
            data = response.json()
            choice = data["choices"][0]["message"]
            tool_calls = choice.get("tool_calls")
            if not tool_calls:
                return choice.get("content", "I don't have a response for that.")
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                if debug: print(f"[tool] LLM called: {function_name}({function_args})", file=sys.stderr)
                result = self._execute_tool(function_name, function_args)
                if debug:
                    result_preview = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                    print(f"[tool] Result: {result_preview}", file=sys.stderr)
                messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(result, default=str)})
            if debug: print(f"[summary] Feeding {len(tool_calls)} tool result(s) back to LLM", file=sys.stderr)
        return "I'm having trouble processing your request. Please try rephrasing."
