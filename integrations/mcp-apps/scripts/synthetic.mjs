/** End-to-end local only: one authorized synthetic project, no Drive writes. */
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { mkdtemp,mkdir,writeFile,readFile,rm } from "node:fs/promises";
import path from "node:path";
import os from "node:os";
const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-mcp-synthetic-"));
const folder=path.join(root,"00_Gestao_e_Continuidade");
let client;
try{
 await mkdir(folder,{recursive:true});
 const config={
  project_name:"SYNTHETIC_MCP_UI_TEST_ONLY",
  presentation_mode:"MINIMAL",method_route:"UNDECIDED",storage_mode:"WORK_FALLBACK",
  storage_state:"WORK_FALLBACK_AUTHORIZED",
 };
 const configPath=path.join(folder,"PROJECT_CONFIG.json");
 const rawConfig=JSON.stringify(config);
 await writeFile(configPath,rawConfig,"utf8");
 await writeFile(path.join(folder,"CONTINUIDADE.md"),
  "Only synthetic test events; no research conclusions.\n","utf8");
 await writeFile(path.join(folder,"11_CADA_Control.csv"),
  "CADA_ID,Title,Assigned_to,Status,Deadline,Completion_evidence\n"+
  "CADA-0010,Review fictional search criteria,Researcher,READY,,\n"+
  "CADA-0009,Prepare fictional paper outline,Researcher,DONE,,synthetic proof\n","utf8");
 let gates="GATE_ID,Name,Status,Decision,Validated_by,Validation_evidence\n";
 for(let i=1;i<=7;i++)gates+="GATE-"+String(i).padStart(4,"0")+
 ",Synthetic checkpoint "+i+",READY,PENDING,,\n";
 await writeFile(path.join(folder,"18_Human_Validation_Gates.csv"),gates,"utf8");
 const env=Object.fromEntries(Object.entries(process.env).filter(([,v])=>typeof v==="string"));
 client=new Client({name:"meu-artigo-synthetic-test",version:"0.1.0"});
 await client.connect(new StdioClientTransport({
  command:process.execPath,args:[path.resolve("server.mjs"),"--stdio"],
  env:{...env,MEU_ARTIGO_PROJECT_ROOT:root}
 }));
 const outcome=await client.callTool({name:"meu_artigo_painel",arguments:{locale:"en",mode:"FULL"}});
 assert.notEqual(outcome.isError,true,"Synthetic canonical project must be readable");
 assert.ok(outcome.content?.[0]?.text);
 assert.match(outcome.content[0].text,/Drive not verified/);
 const site=outcome.structuredContent?.site;
 assert.equal(site?.kind,"CANONICAL_LOCAL_SNAPSHOT");
 assert.equal(site?.canonical_drive_sync_verified,false);
 assert.equal(site?.automatic_scientific_approval,false);
 assert.equal(site?.canonical_writes_allowed,false);
 assert.equal(site?.tasks?.[0]?.id,"CADA-0010");
 assert.equal(site?.locale,"en");
 assert.equal((site?.gates||[]).filter(g=>g.approval_documented).length,0);
 assert.equal(await readFile(configPath,"utf8"),rawConfig);
 console.log("Synthetic real MCP tool: localized fallback, source-grounded JSON, 7 gates unapproved, no source modifications.");
}finally{
 await client?.close();
 await rm(root,{recursive:true,force:true});
}
