/* Stage 15 horizontal end-to-end: Skill/native/blue site/one MCP Apps server.
 * Only synthetic disposable project files and loopback stdio. No remote auth or Drive.
 */
import assert from "node:assert/strict";
import {execFileSync} from "node:child_process";
import {mkdtemp,mkdir,writeFile,readFile,rm,readdir} from "node:fs/promises";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {StdioClientTransport} from "@modelcontextprotocol/sdk/client/stdio.js";
import {JSDOM,VirtualConsole} from "jsdom";
import path from "node:path";
import os from "node:os";
const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-horizontal15-"));
const mgmt=path.join(root,"00_Gestao_e_Continuidade");
const scripts=path.resolve("../../scripts");
const localeCodes=["pt","en","es","fr"];
const banned=["PRIVATE_EVIDENCE_PASSAGE_15","PRIVATE_RESEARCHER_ID_15","PRIVATE_SOURCE_PATH_15"];
const file=(p)=>path.join(mgmt,p);
const py=(script,args)=>JSON.parse(execFileSync("python3",
 [path.join(scripts,script),...args],{
  encoding:"utf8",timeout:20000,env:{...process.env,PYTHONDONTWRITEBYTECODE:"1"}
 }));
const site=(mode,locale)=>py("build_research_site.py",[
 "--project",root,"--json-only","--mode",mode,"--language",locale]);
// Horizontal integration validates the authorized in-process panel projection;
// the operator CLI is intentionally reduced to a private-data-free summary.
const native=(mode)=>JSON.parse(execFileSync("python3",["-c",
 "import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from native_chat_dashboard import panel;print(json.dumps(panel(Path(sys.argv[2]),mode=sys.argv[3]),sort_keys=True))",
 scripts,root,mode],{
 encoding:"utf8",timeout:20000,env:{...process.env,PYTHONDONTWRITEBYTECODE:"1"}
 }));
const skill=(mode)=>JSON.parse(execFileSync("python3",["-c",
 "import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from build_research_workspace import model;print(json.dumps(model(project=Path(sys.argv[2]),mode=sys.argv[3]),sort_keys=True))",
 scripts,root,mode],{
 encoding:"utf8",timeout:20000,env:{...process.env,PYTHONDONTWRITEBYTECODE:"1"}
 }));
const observe=async()=>Object.fromEntries(await Promise.all(
 (await readdir(mgmt)).sort().map(async name=>[name,await readFile(file(name),"utf8")])));
let client;
try{
 await mkdir(mgmt,{recursive:true});
 await writeFile(file("PROJECT_CONFIG.json"),JSON.stringify({
  project_name:"SYNTHETIC_HORIZONTAL_FIFTEEN",presentation_mode:"MINIMAL",
  method_route:"UNDECIDED",storage_mode:"WORK_FALLBACK",
  storage_state:"WORK_FALLBACK_AUTHORIZED"
 }),"utf8");
 await writeFile(file("CONTINUIDADE.md"),"Synthetic-only research, never approved automatically.\n","utf8");
 await writeFile(file("11_CADA_Control.csv"),
  "CADA_ID,Title,Assigned_to,Status,Deadline,Completion_evidence,Notes\n"+
  "CADA-0015,Review synthetic sources,Researcher,READY,,,"+banned[0]+"\n"+
  "CADA-0016,Record synthetic method,Researcher,BLOCKED,,,\n","utf8");
 let gates="GATE_ID,Name,Status,Decision,Validated_by,Validation_evidence\n";
 for(let i=1;i<=7;i++){
  const chosen=i===4;
  gates+="GATE-"+String(i).padStart(4,"0")+
   ",Synthetic gate "+i+","+(chosen?"COMPLETED":"READY")+","+
   (chosen?"APPROVED":"PENDING")+","+(chosen?"RESEARCHER":"")+","+
   (chosen?"synthetic evidence record":"")+"\n";
 }
 await writeFile(file("18_Human_Validation_Gates.csv"),gates,"utf8");
 await writeFile(file("05_Evidence_Matrix.csv"),
  "Evidence_ID,FullText_path\nEVID-001,"+banned[2]+"\n","utf8");
 await writeFile(file("09_Claims_Ledger.csv"),
  "Claim_ID,Claim_text\nCLAIM-001,"+banned[0]+"\n","utf8");
 await writeFile(file("13_Traceability_Log.csv"),
  "Trace_ID,Notes\nTRACE-001,"+banned[1]+"\n","utf8");
 const before=await observe();
 const lmn=native("MINIMAL"), full=native("FULL");
 const skmin=skill("MINIMAL"), skfull=skill("FULL");
 assert.equal(full.overview.documented_gate_approvals,1);
 assert.equal(lmn.overview.documented_gate_approvals,1);
 assert.equal(lmn.gates.items_partial,true);
 assert.equal(skmin.human_gates.items_partial,true);
 assert.equal(skfull.human_gates.items_partial,false);
 assert.deepEqual(skfull.decision_continuity,full.decision_continuity);
 assert.deepEqual(skfull.scientific_diagnostic,full.scientific_diagnostic);
 const minSite=site("MINIMAL","pt"),fullSite=site("FULL","pt");
 assert.equal(minSite.registered_gate_total,7);
 assert.equal(minSite.gate_view_partial,true);
 assert.equal(minSite.documented_gate_count,0);
 assert.equal(minSite.gates.length,3);
 assert.equal(fullSite.registered_gate_total,7);
 assert.equal(fullSite.gate_view_partial,false);
 assert.equal(fullSite.documented_gate_count,1);
 assert.equal(fullSite.gates.length,7);
 assert.deepEqual(fullSite.tasks,full.tasks.items);
 assert.deepEqual(fullSite.tasks,skfull.tasks.items);
 assert.equal(fullSite.next_action.code,full.decision_continuity.next_action.code);
 assert.equal(fullSite.canonical_drive_sync_verified,false);
 assert.equal(fullSite.automatic_scientific_approval,false);
 assert.equal(fullSite.canonical_writes_allowed,false);
 for(const data of [lmn,full,skmin,skfull,minSite,fullSite]){
  const json=JSON.stringify(data);
  for(const marker of banned)assert.ok(!json.includes(marker),
   "Private source or researcher passage leaked into projection");
 }
 client=new Client({name:"stage15-horizontal-acceptance",version:"0.1.0"});
 const env=Object.fromEntries(Object.entries(process.env).filter(([,v])=>typeof v==="string"));
 await client.connect(new StdioClientTransport({
  command:process.execPath,args:[path.resolve("server.mjs"),"--stdio"],
  env:{...env,MEU_ARTIGO_PROJECT_ROOT:"",MEU_ARTIGO_AUTH_MODE:"bearer"}
 }));
 const tools=(await client.listTools()).tools;
 assert.deepEqual(tools.map(x=>x.name),["meu_artigo_painel"]);
 assert.equal(tools[0].annotations.readOnlyHint,true);
 const resources=(await client.listResources()).resources;
 assert.deepEqual(resources.map(x=>x.uri),["ui://meu-artigo/site-v3.html"]);
 for(const mode of ["MINIMAL","FULL"]){
  for(const locale of localeCodes){
   const response=await client.callTool({name:"meu_artigo_painel",
    arguments:{mode,locale}});
   assert.notEqual(response.isError,true);
   assert.ok(response.content?.[0]?.text);
   assert.equal(response.structuredContent?.site?.kind,"HOST_NOT_CONNECTED");
   assert.equal(response.structuredContent?.site?.status,"NO_SNAPSHOT_PROVIDED");
   assert.equal(response.structuredContent?.site?.project_loaded,false);
   assert.equal(response.structuredContent?.site?.drive_sync_verified,false);
   assert.equal(response.structuredContent?.site?.scientific_approval_verified,false);
   assert.match(response.content[0].text,/Meu Artigo/);
   assert.ok(!JSON.stringify(response).includes("SYNTHETIC_HORIZONTAL_FIFTEEN"));
   assert.ok(!JSON.stringify(response).includes("CADA-0015"));
   for(const marker of banned){
    assert.ok(!JSON.stringify(response).includes(marker));
   }
  }
 }
 const resource=await client.readResource({uri:"ui://meu-artigo/site-v3.html"});
 assert.equal(resource.contents.length,1);
 assert.ok(resource.contents[0].text.includes("HOST_NOT_CONNECTED"));
 const html=await readFile(path.resolve("../../assets/research_site.html"),"utf8");
 const vc=new VirtualConsole(),errs=[];
 vc.on("jsdomError",e=>errs.push(String(e)));
 for(const [label,data,expected] of [["partial",minSite,true],["full",fullSite,false]]){
  const dom=new JSDOM(html.replace("__MEU_ARTIGO_SITE_MODEL_JSON__",
   JSON.stringify({schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"pt"})),{
    url:"https://synthetic-horizontal.invalid",runScripts:"dangerously",virtualConsole:vc
  });
  const d=dom.window.document;
  assert.equal(dom.window.MeuArtigoHost.receive(data),true);
  assert.equal(d.querySelectorAll("nav button[data-page]").length,10);
  d.querySelector('nav button[data-page="overview"]').click();
  const prose=d.getElementById("content").textContent;
  if(expected){
    assert.match(prose,/Visão parcial: 3 de 7 gates registrados/);
    for(const [code,phrase] of [["en","Partial view: 3 of 7 registered gates"],
                                ["es","Vista parcial: 3 de 7 etapas registradas"],
                                ["fr","Vue partielle : 3 sur 7 étapes enregistrées"],
                                ["pt-BR","Visão parcial: 3 de 7 gates registrados"]]){
      const picker=d.getElementById("site-language");
      picker.value=code;
      picker.dispatchEvent(new dom.window.Event("change",{bubbles:true}));
      assert.ok(d.getElementById("content").textContent.includes(phrase),phrase);
    }
  }else assert.doesNotMatch(prose,/Visão parcial/);
  d.querySelector('nav button[data-page="steps"]').click();
  if(expected)assert.match(d.getElementById("content").textContent,/Visão parcial/);
  d.querySelector('nav button[data-page="validations"]').click();
  assert.equal(d.querySelectorAll("script[src]").length,0);
  assert.equal(d.querySelectorAll("img[onerror]").length,0);
  dom.window.MeuArtigoHost.disconnect();
  assert.doesNotMatch(d.getElementById("content").textContent,/PRIVATE_/);
  dom.window.close();
 }
 assert.equal(errs.length,0,errs.join("; "));
 assert.deepEqual(await observe(),before,
  "Cross-projection tool, UI, methods and case reading must not mutate files");
 console.log("Stage15 horizontal pass: Skill/native projections agree, MCP receives no research data in 8 modes x locales, neutral UI only.");
}finally{
 await client?.close();
 await rm(root,{recursive:true,force:true});
}
