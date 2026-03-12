# Claude Desktop bridge (stdio → SSE)

This folder contains **mcp-sse-client.js**, a small bridge so **Claude Desktop** can use your MCP server that runs over **SSE** (e.g. `http://localhost:8000/sse`).

## Setup

```bash
cd claude_desktop_bridge
npm install
```

## Run (for Claude Desktop config)

Claude Desktop will run this script. You can test it manually:

```bash
BASE_URL=http://127.0.0.1:8000 SSE_PATH=/sse node mcp-sse-client.js
```

**Important:** Your MCP server must be running first, or you'll get `ECONNREFUSED`. In the project root run: `python mcp_server.py sse`

## Claude Desktop config

Edit Claude Desktop’s config:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add (use the **absolute path** to this folder):

```json
{
  "mcpServers": {
    "ai-agent-tools": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/ai-agent/claude_desktop_bridge/mcp-sse-client.js"],
      "env": {
        "BASE_URL": "http://127.0.0.1:8000",
        "SSE_PATH": "/sse"
      }
    }
  }
}
```

**Start your MCP server before opening Claude Desktop** (in the ai-agent project root: `python mcp_server.py sse`). Otherwise the bridge will log `ECONNREFUSED`.

Example path on macOS if the project is in `Documents/ai-agent`:

```json
"args": ["/Users/YOUR_USERNAME/Documents/ai-agent/claude_desktop_bridge/mcp-sse-client.js"]
```

Restart Claude Desktop after saving.
