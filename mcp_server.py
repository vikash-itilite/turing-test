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

from mcp.server.fastmcp import FastMCP

from tools import (
    get_author_name,
    get_option_approval_details,
    get_temp,
    get_trip_farequote,
    get_weather,
    approve_trip,
    reject_trip,
)

# For SSE (internet): bind to all interfaces; port from env or 8000
_HOST = os.environ.get("FASTMCP_HOST", "0.0.0.0")
_PORT = int(os.environ.get("FASTMCP_PORT", "8000"))

mcp = FastMCP(
    "turing-test",
    instructions="Tools for weather, temperature, and author lookup.",
    host=_HOST,
    port=_PORT,
)

# Register tools from tools.py
mcp.tool()(get_weather)
mcp.tool()(get_temp)
mcp.tool()(get_author_name)
mcp.tool()(get_option_approval_details)
mcp.tool()(get_trip_farequote)
mcp.tool()(approve_trip)
mcp.tool()(reject_trip)


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
