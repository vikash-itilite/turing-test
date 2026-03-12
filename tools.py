"""MCP tools: weather, temperature, author lookup, and option approval details."""

import json
import os
import urllib.request
from urllib.parse import urlencode
from typing import Literal, Optional

# Environment: set ILTECH_ENV=qa or ILTECH_ENV=dev (default: qa).
# All trip/service tools use these base URLs; override per-call with base_url if needed.
_ENV = (os.environ.get("ILTECH_ENV") or "dev").lower().strip()
if _ENV not in ("qa", "dev"):
    _ENV = "qa"

_ENDPOINTS = {
    "qa": {
        "service": "https://service-qa.iltech.in",
        "app": "https://app-qa.iltech.in",
        "origin": "https://booking-qa.iltech.in",
    },
    "dev": {
        "service": "https://service-dev.iltech.in",
        "app": "https://app-dev.iltech.in",
        "origin": "https://booking-dev.iltech.in",
    },
}
# Edit _ENDPOINTS above if your dev hostnames differ.
_SERVICE_URL = _ENDPOINTS[_ENV]["service"]
_APP_URL = _ENDPOINTS[_ENV]["app"]
_ORIGIN = _ENDPOINTS[_ENV]["origin"]


def get_weather(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
    include_forecast: bool = False,
) -> str:
    """Get current weather and optional 5-day forecast for a location."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result


def get_temp(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
) -> str:
    """Get the current temperature for a location."""
    temp = 22 if units == "celsius" else 72
    return f"Temperature in {location}: {temp}°{units[0].upper()}"


def get_author_name(book_or_work: str) -> str:
    """Get the author name for a book, article, or other work."""
    return f"Author of \"{book_or_work}\": Vikash"


def get_option_approval_details(
    trip_id: str,
    token_id: str,
    base_url: Optional[str] = None,
) -> str:
    """Get option approval details for a trip from the service API.
    Requires trip_id, token_id. Uses ILTECH_ENV (qa/dev) for host unless base_url is set."""
    base = (base_url or _SERVICE_URL).rstrip("/")
    path = f"/api/v1/trip/details/{trip_id.strip('/')}/"
    params = f"token_id={token_id}&type=options"
    url = f"{base}{path}?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "*/*",
            "User-Agent": "MCP-Tools/1.0",
            "Origin": _ORIGIN,
            "Referer": f"{_ORIGIN}/",
        },
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return json.dumps(data, indent=2)


def get_trip_farequote(
    trip_id: str,
    token_id: str,
    base_url: Optional[str] = None,
) -> str:
    """Fetch trip fare quote for a trip from the service API.
    Requires trip_id, token_id. Uses ILTECH_ENV (qa/dev) for host unless base_url is set."""
    base = (base_url or _SERVICE_URL).rstrip("/")
    path = f"/api/v1/trip/farequote/{trip_id.strip('/')}/"
    params = f"token_id={token_id}&type=options"
    url = f"{base}{path}?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "*/*",
            "User-Agent": "MCP-Tools/1.0",
            "Origin": _ORIGIN,
            "Referer": f"{_ORIGIN}/",
        },
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return json.dumps(data, indent=2)


def approve_trip(
    trip_id: str,
    token: str,
    approval_type: str = "cost",
    approver_reason: str = "",
    v2_approval_type: str = "V2",
    base_url: Optional[str] = None,
) -> str:
    """Approve a trip via the ARE (Approval) API. POST to approveTripARE.
    Requires trip_id, token. Uses ILTECH_ENV (qa/dev) for host unless base_url is set."""
    base = (base_url or _APP_URL).rstrip("/")
    url = f"{base}/approveTripARE"
    body = urlencode({
        "trip_id": trip_id.strip(),
        "type": approval_type,
        "token": token,
        "approver_reason": approver_reason,
        "v2_approval_type": v2_approval_type
    })
    req = urllib.request.Request(
        url,
        data=body.encode("utf-8"),
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MCP-Tools/1.0",
            "Origin": _ORIGIN,
            "Referer": f"{_ORIGIN}/",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return json.dumps(data, indent=2)


def reject_trip(
    trip_id: str,
    token: str,
    approver_reason: str = "",
    approval_type: str = "cost",
    v2_approval_type: str = "V2",
    base_url: Optional[str] = None,
) -> str:
    """Reject a trip via the ARE (Approval) API. POST to rejectTripARE.
    Requires trip_id, token. Uses ILTECH_ENV (qa/dev) for host unless base_url is set."""
    base = (base_url or _APP_URL).rstrip("/")
    url = f"{base}/rejectTripARE"
    body = urlencode({
        "trip_id": trip_id.strip(),
        "type": approval_type,
        "token": token,
        "approver_reason": approver_reason,
        "v2_approval_type": v2_approval_type
    })
    req = urllib.request.Request(
        url,
        data=body.encode("utf-8"),
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MCP-Tools/1.0",
            "Origin": _ORIGIN,
            "Referer": f"{_ORIGIN}/",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return json.dumps(data, indent=2)
