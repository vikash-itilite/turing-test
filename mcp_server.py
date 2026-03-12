"""
MCP server that exposes get_weather, get_temp, and get_author_name as MCP tools.

Run locally (stdio, for Cursor):
  python mcp_server.py
  python mcp_server.py stdio

Run on the network / internet (SSE over HTTP):
  python mcp_server.py sse
  # Listens on http://0.0.0.0:8000 by default. Set FASTMCP_HOST, FASTMCP_PORT if needed.

Connect from Cursor (stdio): use command + args to this script.
Connect remotely: use the SSE URL, e.g. https://your-domain.com/sse
"""

import os
import sys
from typing import Literal

from mcp.server.fastmcp import FastMCP

# For SSE (internet): bind to all interfaces; port from env or 8000
_HOST = os.environ.get("FASTMCP_HOST", "0.0.0.0")
_PORT = int(os.environ.get("FASTMCP_PORT", "8000"))

mcp = FastMCP(
    "ai-agent-tools",
    instructions="Tools for weather, temperature, and author lookup.",
    host=_HOST,
    port=_PORT,
)


@mcp.tool()
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


@mcp.tool()
def get_temp(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
) -> str:
    """Get the current temperature for a location."""
    temp = 22 if units == "celsius" else 72
    return f"Temperature in {location}: {temp}°{units[0].upper()}"


@mcp.tool()
def get_author_name(book_or_work: str) -> str:
    """Get the author name for a book, article, or other work."""
    # Mock lookup: return a placeholder author based on the title
    return f"Author of \"{book_or_work}\": Vikash"


if __name__ == "__main__":
    transport = (sys.argv[1] if len(sys.argv) > 1 else "stdio").lower()
    if transport not in ("stdio", "sse"):
        print("Usage: python mcp_server.py [stdio|sse]", file=sys.stderr)
        print("  stdio  - local (default), for Cursor", file=sys.stderr)
        print("  sse    - HTTP server for remote clients, e.g. https://your-host/sse", file=sys.stderr)
        sys.exit(1)
    if transport == "sse":
        print(f"MCP server (SSE) at http://{_HOST}:{_PORT}/sse", file=sys.stderr)
    mcp.run(transport=transport)
