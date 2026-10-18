/** End-to-end per-call UI snapshot derived from hypothetical ChatGPT Drive reads.
 * Does not connect to Google or load research files in the MCP process.
 */
import assert from "node:assert/strict";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {createServer} from "../server.mjs";
import {normalizeHostSnapshot} from "../host_projection.mjs";

const create=(id)=>({
 schema:"MEU_ARTIGO_SITE_V1",active_route:"Qualitative documentary",
 registered_gate_total:7,gate_view_partial:false,
 tasks:[{id:"TASK-01",task:"Prepare "+id+" literature map",
   execution_owner:"Researcher",deadline:null}],
 gates:Array.from({length:7},(_,i)=>({
   id:"GATE-000"+(i+1),approval_documented:false
 })),
 next_action:{code:"REVIEW_METHODOLOGY",explanation:"Review "+id+" method",
  responsible:"Researcher"}
});
const a=create("alpha"),b=create("bravo");
const client=new Client({name:"host-projection-fixture",version:"0.1.0"});
const server=createServer();
const [t1,t2]=InMemoryTransport.createLinkedPair();
try{
 await server.connect(t1);await client.connect(t2);
 const listed=await client.listTools();
 assert.deepEqual(listed.tools.map(x=>x.name),["meu_artigo_painel"]);
 const schema=listed.tools[0].inputSchema.properties;
 assert.deepEqual(Object.keys(schema).sort(),["locale","mode","snapshot"]);
 const resultA=await client.callTool({name:"meu_artigo_painel",
  arguments:{locale:"pt",snapshot:a}});
 assert.notEqual(resultA.isError,true);
 assert.equal(resultA.structuredContent.site.kind,"HOST_AUTHORIZED_SNAPSHOT");
 assert.equal(resultA.structuredContent.site.tasks[0].task,
  "Prepare alpha literature map");
 assert.equal(resultA.structuredContent.site.canonical_writes_allowed,false);
 assert.equal(resultA.structuredContent.site.automatic_scientific_approval,false);
 assert.equal(resultA.structuredContent.site.canonical_drive_sync_verified,false);
 assert.equal(resultA.structuredContent.site.documented_gate_count,0);
 const resultB=await client.callTool({name:"meu_artigo_painel",
  arguments:{snapshot:b}});
 assert.notEqual(resultB.isError,true);
 assert.equal(resultB.structuredContent.site.tasks[0].task,
  "Prepare bravo literature map");
 assert.equal(JSON.stringify(resultB).includes("alpha"),false,
  "No previous request state may leak");
 const blank=await client.callTool({name:"meu_artigo_painel",
  arguments:{locale:"pt"}});
 assert.equal(blank.isError,true);
 assert.equal(blank.structuredContent,undefined);
 assert.equal(JSON.stringify(blank).includes("bravo"),false,
  "No cached research data when next caller has no data");
 const badCases=[
  {...a,documents:[{content:"PRIVATE_FULL_TEXT"}]},
  {...a,tasks:[{...a.tasks[0],body:"PRIVATE_SOURCE_PASSAGE"}]},
  {...a,tasks:[{...a.tasks[0],task:"A".repeat(601)}]},
  {...a,tasks:Array.from({length:201},(_,i)=>({
    id:String(i),task:"synthetic",execution_owner:"",deadline:null}))},
  {...a,gates:[...a.gates,{id:"GATE-0008",approval_documented:false}]},
  {...a,gates:a.gates.map(g=>({...g,approval_documented:true})),
   automatic_scientific_approval:true},
  {...a,registered_gate_total:3},
  {...a,scientific_diagnostic:{schema:"MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1",
    status:"INPUTS_UNAVAILABLE",verdict:null,objective_blockers:0}},
  {...a,next_action:{...a.next_action,source_quote:"Sensitive research quote"}},
  {...a,google_token:"secret"},
  {...a,tasks:[{...a.tasks[0],task:"Inspect https://drive.google.com/drive/folders/private"}]},
  {...a,tasks:[{...a.tasks[0],execution_owner:"researcher@example.org"}]},
  {...a,tasks:[{...a.tasks[0],task:"Authorization: Bearer abcdef0123456789"}]},
  {...a,tasks:[{...a.tasks[0],task:"Google token ya29.example_secret_token"}]},
  {...a,tasks:[{...a.tasks[0],task:"password: confidential"}]},
  {...a,tasks:[{...a.tasks[0],task:"Read /home/researcher/private/files"}]},
  {...a,tasks:[{...a.tasks[0],task:String.raw`Review C:\\Users\\Alice\\Private\\article.docx`}]},
  {...a,tasks:[{...a.tasks[0],task:String.raw`Review D:\\Research\\private-paper.docx`}]},
  {...a,tasks:[{...a.tasks[0],task:String.raw`Open \\\\research-server\\share\\notes.docx`}]},
  {...a,next_action:{...a.next_action,
   explanation:String.raw`Look up E:\\Archive\\records\\source.pdf`}},
  {...a,tasks:[a.tasks[0],a.tasks[0]]},
  {...a,gates:[a.gates[0],a.gates[0]]},
  {...a,gates:[{...a.gates[0],id:"GATE-0008"}]}
 ];
 for(const input of badCases){
  const result=await client.callTool({name:"meu_artigo_painel",
   arguments:{snapshot:input}});
  assert.equal(result.isError,true);
  assert.equal(result.structuredContent,undefined);
  assert.ok(!JSON.stringify(result).includes("PRIVATE_"));
  assert.ok(!JSON.stringify(result).includes("secret"));
 }
 const empty=normalizeHostSnapshot({
  schema:"MEU_ARTIGO_SITE_V1",tasks:[],gates:[],
  next_action:{code:null,explanation:null,responsible:null}
 });
 assert.equal(empty.documented_gate_count,0);
 assert.equal(empty.registered_gate_total,null);
 assert.equal(empty.gate_view_partial,true,
  "Missing canonical gate totals must remain partial/unknown");
 const html=await client.readResource({uri:"ui://meu-artigo/site-v3.html"});
 assert.match(html.contents[0].text,/HOST_NOT_CONNECTED/);
 assert.equal(JSON.stringify(html).includes("alpha"),false);
 console.log("HOST_PROJECTION_PASS: host-supplied A/B snapshots rendered per call; no cross-user cache, Drive calls, full files, automatic gates or writes.");
}finally{await client.close();await server.close();}
