"""LMS API client - fetches data from the backend."""

import httpx
from pydantic import BaseModel

from config import config


class APIError(Exception):
    """Raised when the API returns an error."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class Item(BaseModel):
    """Represents a lab or task from the backend."""

    id: int
    type: str
    title: str
    lab: str | None = None
    task: str | None = None


class PassRate(BaseModel):
    """Pass rate for a task."""

    task: str | None = None
    title: str | None = None
    pass_rate: float | None = None
    attempts: int | None = None


async def fetch_items() -> list[Item]:
    """Fetch all items (labs and tasks) from the backend."""
    url = f"{config.lms_api_base_url}/items/"
    headers = {"Authorization": f"Bearer {config.lms_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return [Item.model_validate(item) for item in resp.json()]
    except httpx.ConnectError as e:
        raise APIError(f"connection refused ({config.lms_api_base_url})", status_code=None) from e
    except httpx.HTTPStatusError as e:
        reason = e.response.reason_phrase or "Error"
        raise APIError(f"HTTP {e.response.status_code} {reason}. The backend service may be down.", status_code=e.response.status_code) from e
    except httpx.HTTPError as e:
        raise APIError(f"HTTP error: {str(e)}", status_code=None) from e


async def fetch_pass_rates(lab: str) -> list[PassRate]:
    """Fetch pass rates for a specific lab."""
    url = f"{config.lms_api_base_url}/analytics/pass-rates"
    params = {"lab": lab}
    headers = {"Authorization": f"Bearer {config.lms_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return [PassRate.model_validate(item) for item in data]
    except httpx.ConnectError as e:
        raise APIError(f"connection refused ({config.lms_api_base_url})", status_code=None) from e
    except httpx.HTTPStatusError as e:
        reason = e.response.reason_phrase or "Error"
        raise APIError(f"HTTP {e.response.status_code} {reason}. The backend service may be down.", status_code=e.response.status_code) from e
    except httpx.HTTPError as e:
        raise APIError(f"HTTP error: {str(e)}", status_code=None) from e


async def check_health() -> tuple[bool, str, int | None]:
    """
    Check backend health.
    
    Returns:
        Tuple of (is_healthy, message, item_count)
    """
    try:
        items = await fetch_items()
        return True, f"Backend is healthy. {len(items)} items available.", len(items)
    except APIError as e:
        return False, f"Backend error: {e.message}. Check that the services are running.", None
