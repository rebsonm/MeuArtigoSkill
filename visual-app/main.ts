/** MCP Apps streamable HTTP and stdio transports. */
import { createMcpExpressApp } from "@modelcontextprotocol/express";
import { NodeStreamableHTTPServerTransport } from "@modelcontextprotocol/node";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio";
import { timingSafeEqual } from "node:crypto";
import cors from "cors";
import type { Request, Response } from "express";
import { createServer } from "./server.js";

function constantTimeToken(a: string, b: string): boolean {
  const x = Buffer.from(a); const y = Buffer.from(b);
  return x.length === y.length && timingSafeEqual(x, y);
}

async function startHttp(): Promise<void> {
  const host = process.env.MEU_ARTIGO_HOST || "127.0.0.1";
  const port = Number.parseInt(process.env.PORT || "3001", 10);
  const token = process.env.MEU_ARTIGO_BEARER_TOKEN || "";
  const origin = process.env.MEU_ARTIGO_ALLOWED_ORIGIN || "";
  if (!["127.0.0.1", "localhost", "::1"].includes(host) && token.length < 32) {
    throw new Error("Public binding requires a 32+ character bearer token and a trusted HTTPS reverse proxy.");
  }
  const app = createMcpExpressApp({ host });
  if (origin) app.use(cors({ origin, methods: ["POST", "GET", "DELETE"], allowedHeaders: ["Authorization", "Content-Type", "Mcp-Session-Id", "Mcp-Protocol-Version"] }));
  app.all("/mcp", async (req: Request, res: Response) => {
    if (token && !constantTimeToken((req.headers.authorization || "").replace(/^Bearer\s+/i, ""), token)) {
      res.status(401).json({ error: "Unauthorized" }); return;
    }
    const server = createServer();
    const transport = new NodeStreamableHTTPServerTransport({ sessionIdGenerator: undefined });
    res.on("close", () => {
      transport.close().catch(() => {});
      server.close().catch(() => {});
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res, req.body);
    } catch {
      if (!res.headersSent) res.status(500).json({ jsonrpc: "2.0", id: null, error: { code: -32603, message: "Internal server error" } });
    }
  });
  app.listen(port, host, () => console.error("Meu Artigo Visual MCP on " + host + ":" + port + "/mcp"));
}

async function main(): Promise<void> {
  if (process.argv.includes("--stdio")) {
    await createServer().connect(new StdioServerTransport());
  } else {
    await startHttp();
  }
}
main().catch((err) => { console.error("MCP startup failed:", String(err?.message || err)); process.exitCode = 1; });
