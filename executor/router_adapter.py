"""Provider-neutral boundary to the server's existing intelligent model router."""
from typing import Protocol, Any

class UpstreamRouter(Protocol):
    def execute(self, request: dict) -> dict: ...

def assert_router_response(response: dict) -> dict:
    if not isinstance(response, dict):
        raise TypeError("router response must be a dict")
    if response.get("status") not in {"SUCCEEDED", "FAILED", "PENDING"}:
        raise ValueError("router response has invalid status")
    if not response.get("request_id"):
        raise ValueError("router response missing request_id")
    return response
