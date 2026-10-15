/** Local engineering smoke for the MCP Apps preview. Fictional data only. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const here = dirname(fileURLToPath(import.meta.url));
const client = new Client({ name: "meu-artigo-mcp-test", version: "0.1.0" });
const transport = new StdioClientTransport({
  command: process.execPath,
  args: [resolve(here, "server.mjs"), "--stdio"],
  env: { ...process.env },
});
try {
  await client.connect(transport);
  const listing = await client.listTools();
  const tool = listing.tools.find(x => x.name === "meu_artigo_preview");
  assert.ok(tool, "Read-only preview tool missing");
  assert.equal(tool._meta?.ui?.resourceUri, "ui://meu-artigo/research-map.html");
  assert.ok(!listing.tools.some(x => /(approve|commit|write|delete|gate)/i.test(x.name)),
    "Unexpected mutation tool exposed");

  const ui = await client.readResource({ uri: "ui://meu-artigo/research-map.html" });
  const html = ui.contents?.[0]?.text;
  assert.match(html, /ui\/initialize/);
  assert.match(html, /ui\/notifications\/tool-result/);
  assert.match(html, /tools\/call/);
  assert.match(html, /Comparar duas alternativas/);
  assert.ok(!html.includes("commit_method_field.py"), "Browser must not suggest implicit writes");

  for (const route of ["QUALITATIVE", "QUANTITATIVE", "MIXED_METHODS", "DESIGN_SCIENCE", "CONCEPTUAL_THEORY", "OTHER_NOT_LISTED"]) {
    const answer = await client.callTool({ name: "meu_artigo_preview", arguments: { route, mode: "FULL" } });
    assert.equal(answer.isError, undefined, "Preview failed: " + route);
    const map = answer.structuredContent?.researchMap;
    assert.equal(map?.active_route, route);
    assert.equal(map?.is_project_bound, false);
    assert.equal(map?.mcp_app?.fictional_only, true);
    assert.equal(map?.mcp_app?.real_project_access, false);
    assert.equal(map?.mcp_app?.write_tools_available, false);
    assert.equal(map?.mcp_app?.scientific_gate_approval_available, false);
    assert.equal(map?.overview?.independent_scientific_validation, false);
    assert.equal(map?.overview?.canonical_drive_sync_verified, false);
    assert.ok(map?.method_guides?.overview?.options?.some(x=>x.id==="OTHER_NOT_LISTED"),
      "Other traditions must remain available: " + route);
  }

  const invalid = await client.callTool({
    name: "meu_artigo_preview",
    arguments: { route: "../../private-project", mode: "FULL" },
  });
  assert.equal(invalid.isError, true, "Tool must reject project-like input");
  const local = readFileSync(resolve(here,"../scripts/mcp_preview_projection.py"),"utf8");
  assert.ok(!local.includes("add_argument(\"project\""), "Preview CLI must not accept a project path");
  console.log("MCP Apps smoke: protocol, UI resource, six fictional routes, no user data or write tools.");
} finally {
  await client.close();
}
