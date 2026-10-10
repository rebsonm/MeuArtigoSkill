/**
 * Meu Artigo Visual — read-only MCP Apps server.
 *
 * A tool call reads a CONFIGURED local mirror. It never accepts arbitrary
 * paths from the model or from the iframe and never claims a live Drive sync.
 */
import { registerAppResource, registerAppTool, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/server";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs/promises";
import path from "node:path";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { z } from "zod";

const execute = promisify(execFile);
const currentDir = path.dirname(fileURLToPath(import.meta.url));
const resourceUri = "ui://meu-artigo-visual/dashboard.html";

function scriptPath(): string {
  const root = path.resolve(currentDir, existsSync(path.resolve(currentDir, "../scripts/visual_dashboard.py")) ? ".." : "../..");
  return path.join(root, "scripts", "visual_dashboard.py");
}

function appHtmlPath(): string {
  return path.join(currentDir, "mcp-app.html").replace("/dist/mcp-app.html", "/dist/mcp-app.html");
}

function summarize(data: any): string {
  const op = data.operational;
  const scientific = data.scientific;
  const action = op.next_action?.action ?? "Não identificada nos registros";
  return [
    "Meu Artigo Visual — " + data.project.title,
    "Tarefas concluídas (registradas): " + (op.tasks_done_reported ?? "indisponível") + "/" + (op.tasks_total ?? "indisponível"),
    "Validações científicas documentadas: " + (scientific.gates_approved_documented ?? "indisponível") + "/" + (scientific.gates_total ?? "indisponível"),
    "Próxima ação: " + action,
    "Armazenamento declarado: " + data.project.storage_state + " (não verificado nesta sessão).",
    "Progresso operacional não comprova validade científica.",
  ].join("\n");
}

async function loadDashboard(mode?: "MINIMAL" | "FULL"): Promise<any> {
  const project = process.env.MEU_ARTIGO_PROJECT_ROOT;
  if (!project || !path.isAbsolute(project)) {
    throw new Error("Configure MEU_ARTIGO_PROJECT_ROOT com um caminho absoluto autorizado.");
  }
  // The tool never takes a path argument; only the operator controls the workspace.
  const python = process.env.MEU_ARTIGO_PYTHON || "python3";
  const args = [scriptPath(), project, "--format", "json"];
  if (mode) args.push("--mode", mode);
  const { stdout } = await execute(python, args, { timeout: 10000, maxBuffer: 2 * 1024 * 1024 });
  return JSON.parse(stdout);
}

export function createServer(): McpServer {
  const server = new McpServer({ name: "Meu Artigo Visual", version: "0.1.0" });
  registerAppTool(
    server,
    "meu_artigo_dashboard",
    {
      title: "Acompanhar Meu Artigo",
      description: "Mostra o progresso C.A.D.A., a próxima ação e validações científicas registradas no projeto autorizado. Somente leitura; não autentica revisões ou sincronização.",
      inputSchema: z.object({ mode: z.enum(["MINIMAL", "FULL"]).optional() }),
      _meta: { ui: { resourceUri } },
    },
    async ({ mode }) => {
      try {
        const dashboard = await loadDashboard(mode);
        return {
          content: [{ type: "text" as const, text: summarize(dashboard) }],
          structuredContent: { dashboard },
        };
      } catch {
        // Avoid leaking environment paths or research content in diagnostics.
        return {
          isError: true,
          content: [{ type: "text" as const, text: "O painel não pôde ler o projeto autorizado. Verifique caminho, permissões e registros canônicos; nenhum dado de demonstração foi substituído." }],
        };
      }
    },
  );
  registerAppResource(
    server, resourceUri, resourceUri,
    { mimeType: RESOURCE_MIME_TYPE },
    async () => ({
      contents: [{
        uri: resourceUri,
        mimeType: RESOURCE_MIME_TYPE,
        text: await fs.readFile(appHtmlPath(), "utf-8"),
      }],
    }),
  );
  return server;
}
