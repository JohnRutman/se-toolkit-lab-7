"""LMS API client for fetching data from the backend."""

import httpx
from typing import Any


class LMSClient:
    """HTTP client for the LMS backend API.
    
    Uses Bearer token authentication and handles errors gracefully.
    """
    
    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize the LMS client.
        
        Args:
            base_url: Base URL of the LMS backend (e.g., http://localhost:42002)
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10.0,
        )
    
    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make an authenticated request to the backend.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., "/items/", "/analytics/pass-rates")
            params: Optional query parameters
            
        Returns:
            JSON response as dict or list
            
        Raises:
            ConnectionError: If backend is unreachable
            httpx.HTTPStatusError: If backend returns an error status
        """
        try:
            response = self._client.request(method, path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url}). Check that the services are running.") from e
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.",
                request=e.request,
                response=e.response,
            ) from e
        except httpx.TimeoutException:
            raise ConnectionError(f"timeout connecting to backend ({self.base_url}). The service is taking too long to respond.")
    
    def get_items(self) -> list[dict[str, Any]]:
        """Fetch all items (labs and tasks) from the backend.
        
        Returns:
            List of items with their metadata
        """
        return self._request("GET", "/items/")
    
    def get_pass_rates(self, lab: str) -> list[dict[str, Any]]:
        """Fetch pass rates for a specific lab.
        
        Args:
            lab: Lab identifier (e.g., "lab-01", "lab-04")
            
        Returns:
            List of pass rate data per task
        """
        return self._request("GET", "/analytics/pass-rates", params={"lab": lab})
    
    def get_scores(self, lab: str) -> list[dict[str, Any]]:
        """Fetch score distribution for a specific lab.
        
        Args:
            lab: Lab identifier
            
        Returns:
            List of score bucket data
        """
        return self._request("GET", "/analytics/scores", params={"lab": lab})
    
    def health_check(self) -> dict[str, Any]:
        """Check if the backend is healthy.

        Returns:
            Health status with item count
        """
        items = self.get_items()
        return {"healthy": True, "item_count": len(items)}

    def get_learners(self) -> list[dict[str, Any]]:
        """Fetch all enrolled learners and their groups.

        Returns:
            List of learners with their metadata
        """
        return self._request("GET", "/learners/")

    def get_timeline(self, lab: str) -> list[dict[str, Any]]:
        """Fetch submission timeline for a specific lab.

        Args:
            lab: Lab identifier

        Returns:
            List of timeline data (submissions per day)
        """
        return self._request("GET", "/analytics/timeline", params={"lab": lab})

    def get_groups(self, lab: str) -> list[dict[str, Any]]:
        """Fetch per-group scores and student counts for a lab.

        Args:
            lab: Lab identifier

        Returns:
            List of group data
        """
        return self._request("GET", "/analytics/groups", params={"lab": lab})

    def get_top_learners(self, lab: str, limit: int = 5) -> list[dict[str, Any]]:
        """Fetch top N learners by score for a lab.

        Args:
            lab: Lab identifier
            limit: Number of top learners to return

        Returns:
            List of top learners with their scores
        """
        return self._request("GET", "/analytics/top-learners", params={"lab": lab, "limit": limit})

    def get_completion_rate(self, lab: str) -> dict[str, Any]:
        """Fetch completion rate percentage for a lab.

        Args:
            lab: Lab identifier

        Returns:
            Completion rate data
        """
        return self._request("GET", "/analytics/completion-rate", params={"lab": lab})

    def trigger_sync(self) -> dict[str, Any]:
        """Trigger a data sync from the autochecker.

        Returns:
            Sync status
        """
        return self._request("POST", "/pipeline/sync")
