/** Experimental MCP Apps transport for the fictional Meu Artigo research map.
 * Reuses the canonical Python projection; does not expose user projects or writes.
 * Do not enable real-user access by adding a path or token parameter here.
 */
import { createServer as createHttpServer } from "node:http";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve, dirname } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  registerAppResource, registerAppTool, RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const exec = promisify(execFile);
const appDir = dirname(fileURLToPath(import.meta.url));
const root = resolve(appDir, "..");
const script = resolve(root, "scripts/mcp_preview_projection.py");
const widget = readFileSync(resolve(appDir, "widget.html"), "utf8");
const resourceUri = "ui://meu-artigo/research-map.html";
const routes = [
  "UNDECIDED", "INTEGRATIVE_REVIEW", "SYSTEMATIC_REVIEW",
  "PROBLEMATIZING_REVIEW", "CONCEPTUAL_THEORY", "QUALITATIVE",
  "QUANTITATIVE", "MIXED_METHODS", "DESIGN_SCIENCE", "OTHER_NOT_LISTED",
];
const modes = ["MINIMAL", "FULL"];
const routeSchema = z.enum(routes);
const modeSchema = z.enum(modes);

export async function loadFictionalPreview(route = "QUALITATIVE", mode = "MINIMAL") {
  if (!routes.includes(route) || !modes.includes(mode)) throw new Error("Invalid preview");
  const { stdout } = await exec(process.env.MEU_ARTIGO_PYTHON || "python3",
    ["-I", script, "--route", route, "--mode", mode],
    { cwd: root, timeout: 12000, maxBuffer: 2 * 1024 * 1024 });
  const result = JSON.parse(stdout);
  if (result.mcp_app?.fictional_only !== true ||
      result.mcp_app?.real_project_access !== false ||
      result.is_project_bound !== false ||
      result.snapshot_kind !== "FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT") {
    throw new Error("Unsafe research snapshot refused");
  }
  return result;
}

export function makeServer() {
  const server = new McpServer({ name: "meu-artigo-research-preview", version: "0.1.0" });
  registerAppResource(server, "research-map", resourceUri, {},
    async () => ({ contents: [{ uri: resourceUri, mimeType: RESOURCE_MIME_TYPE, text: widget }] }));
  registerAppTool(server, "meu_artigo_preview", {
    title: "Explorar mapa de pesquisa fictício",
    description: "Abre o mapa metodológico interativo do Meu Artigo usando apenas catálogo e cenários fictícios. Nenhum projeto pessoal, decisão ou gate é acessado ou gravado.",
    inputSchema: { route: routeSchema.optional(), mode: modeSchema.optional() },
    _meta: { ui: { resourceUri } },
  }, async ({ route = "QUALITATIVE", mode = "MINIMAL" }) => {
    try {
      const researchMap = await loadFictionalPreview(route, mode);
      return {
        content: [{ type: "text", text: "Mapa metodológico fictício para explorar e comparar abordagens. Sem autenticação de pesquisador, registros ou aprovação científica." }],
        structuredContent: { researchMap },
      };
    } catch {
      return {
        isError: true,
        content: [{ type: "text", text: "Prévia indisponível. Nenhum dado de projeto foi consultado ou modificado." }],
      };
    }
  });
  return server;
}

async function startHttp() {
  // This transport is an anonymous, fictional preview, NOT a multiuser API.
  // Bind only to loopback. An externally exposed tunnel must remain demo-only.
  const host = "127.0.0.1";
  const port = Number(process.env.PORT || "8787");
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error("Invalid port");
  }
  const allowedOrigin = process.env.MEU_ARTIGO_MCP_ALLOWED_ORIGIN || "";
  createHttpServer(async (req, res) => {
    if (!req.url) { res.writeHead(400).end(); return; }
    const url = new URL(req.url, "http://localhost");
    if (url.pathname === "/" && req.method === "GET") {
      res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" });
      res.end("Meu Artigo MCP Apps: fictional preview only; no project access.");
      return;
    }
    if (url.pathname !== "/mcp" || !["POST", "GET", "DELETE"].includes(req.method || "")) {
      res.writeHead(404).end(); return;
    }
    if (req.headers.origin && (!allowedOrigin || req.headers.origin !== allowedOrigin)) {
      res.writeHead(403).end(); return;
    }
    const server = makeServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, enableJsonResponse: true,
    });
    res.on("close", () => {
      void transport.close();
      void server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch {
      if (!res.headersSent) res.writeHead(500).end("Internal MCP failure");
    }
  }).listen(port, host, () => {
    console.error("Meu Artigo fictional MCP preview on http://" + host + ":" + port + "/mcp");
  });
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.includes("--stdio")) {
    await makeServer().connect(new StdioServerTransport());
  } else {
    await startHttp();
  }
}
