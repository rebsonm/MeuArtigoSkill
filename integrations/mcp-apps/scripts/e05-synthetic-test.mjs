/** No live Drive content: staging must reject everything but two fixed fixtures. */
import assert from "node:assert/strict";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {createServer} from "../server.mjs";
const old=process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY;
process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY="YES";
const server=createServer();
const client=new Client({name:"e05-fixtures-only",version:"0.1.0"});
const [st,ct]=InMemoryTransport.createLinkedPair();
function fixture(label){
 const a=label==="ALPHA";
 return {
  schema:"MEU_ARTIGO_SITE_V1",active_route:"documentary",
  registered_gate_total:7,gate_view_partial:false,
  tasks:[{id:a?"SYN-E05-A-01":"SYN-E05-B-01",
   task:"SYNTHETIC E05 "+label,execution_owner:"Synthetic Researcher",deadline:null}],
  gates:Array.from({length:7},(_,i)=>({id:"GATE-000"+(i+1),approval_documented:false})),
  next_action:{code:"REVIEW",explanation:"SYNTHETIC E05 REVIEW",
   responsible:"Synthetic Researcher"}
 };
}
async function call(snapshot){
 return client.callTool({name:"meu_artigo_painel",arguments:{locale:"pt",mode:"FULL",snapshot}});
}
try{
 await server.connect(st);await client.connect(ct);
 const tool=(await client.listTools()).tools.find(x=>x.name==="meu_artigo_painel");
 assert.match(tool.title,/synthetic visual acceptance/);
 assert.equal(tool._meta.ui.resourceUri,"ui://meu-artigo/site-v3.html");
 const res=await client.readResource({uri:"ui://meu-artigo/site-v3.html"});
 assert.equal(res.contents[0].mimeType,"text/html;profile=mcp-app");
 assert.equal(res.contents[0]._meta?.["openai/ui"]?.preferredDisplayMode,"inline");
 assert.deepEqual(res.contents[0]._meta?.["openai/ui"]?.availableDisplayModes,["inline","fullscreen"]);
 for(const value of ["ALPHA","BRAVO"]){
  const result=await call(fixture(value));
  assert.notEqual(result.isError,true);
  assert.equal(result.structuredContent.site.tasks[0].task,"SYNTHETIC E05 "+value);
  assert.equal(result.structuredContent.site.documented_gate_count,0);
 }
 const noSnapshot=await client.callTool({name:"meu_artigo_painel",
   arguments:{locale:"pt",mode:"MINIMAL"}});
 assert.equal(noSnapshot.isError,true,"E05 blank mode must remain closed");
 assert.equal(noSnapshot.structuredContent,undefined);
 const real=fixture("ALPHA");real.tasks[0].task="PRIVATE RESEARCH DOCUMENT";
 assert.equal((await call(real)).isError,true);
 const gate=fixture("ALPHA");gate.gates[0].approval_documented=true;
 assert.equal((await call(gate)).isError,true);
 const extra=fixture("ALPHA");extra.drive_url="https://example.invalid/private";
 assert.equal((await call(extra)).isError,true);
 console.log("E05_SYNTHETIC_ONLY_PASS: fixed fixtures allowed; real, extra and approved-gate data rejected.");
}finally{
 await client.close();await server.close();
 if(old===undefined)delete process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY;
 else process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY=old;
}
