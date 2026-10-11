/**
 * Test real MCP client/server handshake, tool and UI resource with a disposable,
 * explicitly synthetic local project. No external research or Drive involved.
 */
import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const root = await mkdtemp(path.join(os.tmpdir(), "meu-artigo-visual-test-"));
const base = path.join(root, "00_Gestao_e_Continuidade");
let client;
try {
  await mkdir(base, { recursive: true });
  const config = JSON.stringify({
    project_name: "SYNTHETIC SMOKE TEST — NOT RESEARCH",
    presentation_mode: "MINIMAL",
    storage_mode: "WORK_FALLBACK",
    storage_state: "WORK_FALLBACK_AUTHORIZED",
  });
  const configPath = path.join(base, "PROJECT_CONFIG.json");
  await writeFile(configPath, config, "utf8");
  await writeFile(path.join(base, "11_CADA_Control.csv"),
    "CADA_ID,Title,Status,Next_action,Completion_evidence\nCADA-0001,Prepare outline,DONE,,local fixture\nCADA-0002,Review method,READY,Review method,\n", "utf8");
  await writeFile(path.join(base, "18_Human_Validation_Gates.csv"),
    "GATE_ID,Name,Status,Decision,Validated_by,Validation_evidence\nGATE-0001,Research question,READY,PENDING,,\n", "utf8");
  const env = Object.fromEntries(Object.entries(process.env).filter(([, value]) => typeof value === "string"));
  client = new Client({ name: "meu-artigo-visual-smoke", version: "0.1.0" });
  await client.connect(new StdioClientTransport({
    command: process.execPath, args: [path.resolve("dist/main.js"), "--stdio"],
    env: { ...env, MEU_ARTIGO_PROJECT_ROOT: root },
  }));
  const tools = await client.listTools();
  const dashboardTool = tools.tools.find(t => t.name === "meu_artigo_dashboard");
  assert.ok(dashboardTool, "dashboard tool not registered");
  assert.equal(dashboardTool._meta?.ui?.resourceUri, "ui://meu-artigo-visual/dashboard.html");

  const tool = await client.callTool({ name: "meu_artigo_dashboard", arguments: { mode: "FULL" } });
  assert.equal(tool.isError, undefined);
  const view = tool.structuredContent?.dashboard;
  assert.equal(view?.project?.title, "SYNTHETIC SMOKE TEST — NOT RESEARCH");
  assert.equal(view?.operational?.tasks_done_reported, 1);
  assert.equal(view?.operational?.next_action?.id, "CADA-0002");
  assert.equal(view?.scientific?.gates_approved_documented, 0);
  assert.equal(view?.project?.storage_verified_in_this_session, false);

  const resource = await client.readResource({ uri: "ui://meu-artigo-visual/dashboard.html" });
  assert.match(resource.contents[0]?.text || "", /Meu Artigo Visual/);
  assert.match(resource.contents[0]?.text || "", /src/); // Bundled HTML contains client code.
  assert.equal(await readFile(configPath, "utf8"), config);
  console.log("MCP smoke passed: stdio handshake, canonical read, UI resource, no mutation.");
} finally {
  await client?.close();
  await rm(root, { recursive: true, force: true });
}
