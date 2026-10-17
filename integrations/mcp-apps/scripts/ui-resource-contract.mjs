/** E03/E05: Test the ACTUAL resources/read HTML using synthetic data only.
 * JSDOM is not a replacement for a real browser or ChatGPT host.
 */
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {Script} from "node:vm";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {JSDOM,VirtualConsole} from "jsdom";
import {createServer} from "../server.mjs";
import {normalizeHostSnapshot} from "../host_projection.mjs";
import {uiOutputSchema} from "../ui_output_schema.mjs";
const uri="ui://meu-artigo/site-v1.html";
const client=new Client({name:"meu-artigo-ui-resource-contract",version:"0.1.0"});
const server=createServer();
const [serverTransport,clientTransport]=InMemoryTransport.createLinkedPair();
const fake=prefix=>({
 schema:"MEU_ARTIGO_SITE_V1",registered_gate_total:7,gate_view_partial:false,
 tasks:[{id:"SYNTH-01",task:"Synthetic task "+prefix,execution_owner:"Synthetic role",deadline:null}],
 gates:Array.from({length:7},(_,i)=>({id:"GATE-000"+(i+1),approval_documented:false})),
 next_action:{code:"REVIEW",explanation:"Synthetic review "+prefix,responsible:"Synthetic role"}
});
try{
 await server.connect(serverTransport);await client.connect(clientTransport);
 const tool=(await client.listTools()).tools.find(x=>x.name==="meu_artigo_painel");
 assert.equal(tool?._meta?.ui?.resourceUri,uri);
 assert.ok(tool?.outputSchema?.properties?.site,"Tool must advertise outputSchema.site");
 const result=await client.callTool({name:"meu_artigo_painel",arguments:{snapshot:fake("ALPHA")}});
 assert.notEqual(result.isError,true);
 assert.ok(uiOutputSchema.site.safeParse(result.structuredContent.site).success);
 assert.equal(uiOutputSchema.site.safeParse({...result.structuredContent.site,
  canonical_writes_allowed:true}).success,false);
 const resource=(await client.readResource({uri})).contents[0];
 const html=resource.text;
 assert.equal(resource.uri,uri);
 assert.equal(resource.mimeType,"text/html;profile=mcp-app");
 assert.ok(Buffer.byteLength(html,"utf8")<2*1024*1024);
 assert.ok(!html.includes("__MEU_ARTIGO_SITE_MODEL_JSON__"));
 assert.ok(html.includes("HOST_NOT_CONNECTED"));
 assert.deepEqual(resource._meta?.ui?.csp?.connectDomains,[]);
 assert.deepEqual(resource._meta?.ui?.csp?.resourceDomains,[]);
 const parsed=new JSDOM(html,{runScripts:"outside-only",url:"https://synthetic.invalid/"});
 const scripts=[...parsed.window.document.querySelectorAll("script")];
 if(scripts.length!==3){
  console.log("RESOURCE_SCRIPT_FORENSICS",JSON.stringify({
   dom_scripts:scripts.length,
   raw_script_open:(html.match(/<script\\b/gi)||[]).length,
   raw_script_close:(html.match(/<\\/script\\s*>/gi)||[]).length,
   sampled_elements:scripts.slice(0,12).map((s,i)=>({
    index:i,type:s.type,src:Boolean(s.src),length:s.textContent.length,
    prefix:s.textContent.slice(0,50)
   }))
  }));
 }
 assert.equal(scripts.length,3,"Expect JSON, dashboard code and bundled MCP bridge");
 assert.equal(scripts[0].type,"application/json");
 for(let i=1;i<scripts.length;i++)new Script(scripts[i].textContent,{filename:"resource-script-"+i});
 assert.ok(scripts[2].textContent.length>1000);
 parsed.window.close();
 const errors=[],vc=new VirtualConsole();
 vc.on("jsdomError",e=>errors.push(e.message));
 const dom=new JSDOM(html,{runScripts:"dangerously",
   url:"https://synthetic.invalid/",virtualConsole:vc});
 try{
  assert.ok(dom.window.MeuArtigoHost?.receive);
  assert.equal(dom.window.document.querySelectorAll('nav button[data-page]').length,10);
  for(const key of ["ALPHA","BRAVO"]){
   assert.equal(dom.window.MeuArtigoHost.receive({
    ...normalizeHostSnapshot(fake(key)),kind:"CANONICAL_LOCAL_SNAPSHOT"}),true);
   dom.window.document.querySelector('nav button[data-page="tasks"]').click();
   assert.match(dom.window.document.getElementById("content").textContent,
    new RegExp("Synthetic task "+key));
   if(key==="BRAVO")assert.doesNotMatch(
    dom.window.document.getElementById("content").textContent,/Synthetic task ALPHA/);
  }
  dom.window.MeuArtigoHost.disconnect();
  assert.doesNotMatch(dom.window.document.getElementById("content").textContent,
   /Synthetic task BRAVO/);
  assert.deepEqual(errors,[]);
 }finally{dom.window.close();}
 console.log(JSON.stringify({status:"UI_RESOURCE_ASSEMBLY_PASS",uri,
  mime:resource.mimeType,bytes:Buffer.byteLength(html,"utf8"),
  sha256:createHash("sha256").update(html).digest("hex"),scripts:scripts.length,
  screens:10,chatgpt_iframe:"NOT_TESTED"},null,2));
}finally{await client.close();await server.close();}
