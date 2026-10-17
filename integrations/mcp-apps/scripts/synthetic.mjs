/** Synthetic project data must remain inaccessible to the MCP itself. */
import assert from "node:assert/strict";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {StdioClientTransport} from "@modelcontextprotocol/sdk/client/stdio.js";
import {mkdtemp,mkdir,writeFile,readFile,rm} from "node:fs/promises";
import path from "node:path";
import os from "node:os";
const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-mcp-data-deny-"));
const source=path.join(root,"00_Gestao_e_Continuidade");
const privateMark="PRIVATE_RESEARCH_TEXT_MUST_NEVER_REACH_MCP";
let client;
try{
 await mkdir(source,{recursive:true});
 const paper=path.join(source,"CONTINUIDADE.md");
 await writeFile(paper,privateMark,"utf8");
 client=new Client({name:"host-drive-synthetic",version:"0.1.0"});
 const env=Object.fromEntries(Object.entries(process.env).filter(([k,v])=>
  typeof v==="string"&&!k.startsWith("MEU_ARTIGO_PROJECT_ROOT")&&
  !k.startsWith("MEU_ARTIGO_MULTIUSER_REGISTRY")&&
  !k.startsWith("MEU_ARTIGO_GOOGLE_")&&k!=="MEU_ARTIGO_TENANT_DATA_ROOT"));
 await client.connect(new StdioClientTransport({
  command:process.execPath,args:[path.resolve("server.mjs"),"--stdio"],env
 }));
 const result=await client.callTool({name:"meu_artigo_painel",
  arguments:{locale:"en",mode:"FULL"}});
 assert.equal(result.isError,true,"MCP must not read a project");
 assert.equal(result.structuredContent,undefined);
 assert.match(result.content[0].text,/personal ChatGPT Google Drive connection/);
 const view=await client.readResource({uri:"ui://meu-artigo/site-v1.html"});
 assert.match(view.contents[0].text,/HOST_NOT_CONNECTED/);
 assert.ok(!JSON.stringify(result).includes(privateMark));
 assert.ok(!JSON.stringify(view).includes(privateMark));
 assert.equal(await readFile(paper,"utf8"),privateMark);
 console.log("Synthetic MCP project isolation: no file access, no Drive metadata, generic UI only.");
}finally{
 await client?.close();
 await rm(root,{recursive:true,force:true});
}
