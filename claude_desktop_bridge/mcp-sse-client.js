#!/usr/bin/env node
/**
 * Bridge: Claude Desktop (stdio) <-> your MCP server (SSE).
 * Claude Desktop spawns this and talks MCP over stdio; this script
 * connects to your SSE MCP server and forwards requests/responses.
 *
 * Env:
 *   BASE_URL  - e.g. http://localhost:8000 (default)
 *   SSE_PATH  - e.g. /sse (default)
 *   API_KEY   - optional auth header: Bearer <API_KEY>
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// Use 127.0.0.1 to avoid Node resolving localhost to IPv6 (::1) which can cause ECONNREFUSED
let BASE_URL = process.env.BASE_URL || "http://127.0.0.1:8000";
if (BASE_URL.includes("localhost")) {
  BASE_URL = BASE_URL.replace("localhost", "127.0.0.1");
}
const SSE_PATH = process.env.SSE_PATH || "/sse";
const API_KEY = process.env.API_KEY;
const FULL_URL = `${BASE_URL.replace(/\/$/, "")}${SSE_PATH.startsWith("/") ? SSE_PATH : "/" + SSE_PATH}`;

function log(msg) {
  console.error(`[mcp-sse-bridge] ${msg}`);
}

async function run() {
  log(`Connecting to ${FULL_URL}`);
  const headers = {};
  if (API_KEY) headers["Authorization"] = `Bearer ${API_KEY}`;

  const sseTransport = new SSEClientTransport(new URL(FULL_URL), {
    requestInit: { headers },
  });

  const client = new Client(
    { name: "mcp-sse-bridge", version: "1.0.0" },
    { capabilities: {} },
  );

  await client.connect(sseTransport);
  log("Connected to MCP server (SSE). Starting stdio server for Claude Desktop.");

  const server = new Server(
    { name: "mcp-sse-bridge", version: "1.0.0" },
    { capabilities: { tools: {} } },
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    const result = await client.listTools();
    return result;
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const result = await client.callTool({
      name: request.params.name,
      arguments: request.params.arguments ?? {},
    });
    return result;
  });

  const stdioTransport = new StdioServerTransport();
  await server.connect(stdioTransport);
  log("Bridge running (stdio <-> SSE). Claude Desktop can use tools.");
}

run().catch((err) => {
  log(`Fatal: ${err.message}`);
  process.exit(1);
});
