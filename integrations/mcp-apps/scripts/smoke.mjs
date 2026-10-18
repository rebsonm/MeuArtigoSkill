/** MCP stdio acceptance: discovery, fallback text, real UI resource.
 * Unconfigured data MUST fail closed without returning fictional content. */
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { resolve } from "node:path";
const client=new Client({name:"meu-artigo-test",version:"0.1.0"});
const env=Object.fromEntries(Object.entries(process.env).filter(([k,v])=>typeof v==="string"&&k!=="MEU_ARTIGO_PROJECT_ROOT"));
try{
 await client.connect(new StdioClientTransport({
  command:process.execPath,args:[resolve("server.mjs"),"--stdio"],env
 }));
 const listed=await client.listTools();
 const tool=listed.tools.find(t=>t.name==="meu_artigo_painel");
 assert.ok(tool);
 assert.equal(tool._meta.ui.resourceUri,"ui://meu-artigo/site-v3.html");
 assert.equal(tool._meta["openai/outputTemplate"],"ui://meu-artigo/site-v3.html");
 const result=await client.callTool({name:"meu_artigo_painel",arguments:{locale:"es"}});
 assert.equal(result.isError,true);
 assert.match(result.content[0].text,/interfaz y orientación metodológica genérica/);
 assert.equal(result.structuredContent,undefined);
 const resource=await client.readResource({uri:"ui://meu-artigo/site-v3.html"});
 const content=resource.contents[0];
 assert.equal(content.mimeType,"text/html;profile=mcp-app");
 assert.match(content.text,/Meu Artigo/);
 assert.match(content.text,/HOST_NOT_CONNECTED/);
 assert.doesNotMatch(content.text,/__MEU_ARTIGO_SITE_MODEL_JSON__/);
 assert.match(content.text,/ui\/notifications\/tool-result|ontoolresult/);
 assert.match(content.text,/connect-src 'none'/);
 assert.match(content.text,/option.selected h3/);
 console.log("MCP Apps protocol smoke: tool, UI resource, safe fallback, no fictional project data.");
}finally{
 await client.close();
}
