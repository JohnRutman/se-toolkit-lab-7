"""LMS API client with async support."""

import httpx
from pydantic import BaseModel
from config import config


class APIError(Exception):
    """Exception raised when API request fails."""
    
    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class Item(BaseModel):
    """Item model from LMS API."""
    
    id: int
    type: str
    title: str
    lab: str | None = None


class PassRate(BaseModel):
    """Pass rate model from LMS API."""
    
    task: str | None = None
    title: str | None = None
    pass_rate: float | None = None
    attempts: int | None = None


async def fetch_items() -> list[Item]:
    """Fetch all items from the LMS API.
    
    Returns:
        List of items (labs and tasks)
        
    Raises:
        APIError: If the API request fails
    """
    url = f"{config.lms_api_base_url}/items/"
    headers = {"Authorization": f"Bearer {config.lms_api_key}"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return [Item.model_validate(item) for item in resp.json()]
    except httpx.ConnectError as e:
        raise APIError(f"connection refused ({config.lms_api_base_url})") from e
    except httpx.HTTPStatusError as e:
        raise APIError(f"HTTP {e.response.status_code}", status_code=e.response.status_code) from e


async def fetch_pass_rates(lab: str) -> list[PassRate]:
    """Fetch pass rates for a specific lab.
    
    Args:
        lab: Lab identifier (e.g., "lab-01", "lab-04")
        
    Returns:
        List of pass rate data per task
        
    Raises:
        APIError: If the API request fails
    """
    url = f"{config.lms_api_base_url}/analytics/pass-rates"
    params = {"lab": lab}
    headers = {"Authorization": f"Bearer {config.lms_api_key}"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            return [PassRate.model_validate(item) for item in resp.json()]
    except httpx.ConnectError as e:
        raise APIError(f"connection refused") from e
    except httpx.HTTPStatusError as e:
        raise APIError(f"HTTP {e.response.status_code}", status_code=e.response.status_code) from e


async def check_health() -> tuple[bool, str, int | None]:
    """Check if the backend is healthy.
    
    Returns:
        Tuple of (is_healthy, message, item_count)
    """
    try:
        items = await fetch_items()
        return True, f"Backend is healthy. {len(items)} items available.", len(items)
    except APIError as e:
        return False, f"Backend error: {e.message}", None
