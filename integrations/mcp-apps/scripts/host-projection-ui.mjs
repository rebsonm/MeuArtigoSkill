/** Browser-level acceptance of the original ten-screen dashboard using
 * canonical display fields already read by ChatGPT (synthetic fixture only).
 */
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {JSDOM,VirtualConsole} from "jsdom";
import {normalizeHostSnapshot} from "../host_projection.mjs";
import path from "node:path";
const html=await readFile(path.resolve("../../assets/research_site.html"),"utf8");
const make=(prefix)=>normalizeHostSnapshot({
 schema:"MEU_ARTIGO_SITE_V1",active_route:"documentary",
 registered_gate_total:7,gate_view_partial:false,
 tasks:[{id:prefix+"-01",task:"Synthetic task "+prefix,
  execution_owner:"Researcher",deadline:null}],
 gates:Array.from({length:7},(_,i)=>({id:"GATE-000"+(i+1),
  approval_documented:false})),
 next_action:{code:"REVIEW",explanation:"Review method "+prefix,
  responsible:"Researcher"}
});
const errors=[],vc=new VirtualConsole();
vc.on("jsdomError",e=>errors.push(String(e)));
const dom=new JSDOM(html.replace("__MEU_ARTIGO_SITE_MODEL_JSON__",
 JSON.stringify({schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"pt"})),{
 url:"https://synthetic.invalid",runScripts:"dangerously",virtualConsole:vc
});
try{
 const d=dom.window.document, host=dom.window.MeuArtigoHost;
 assert.ok(host?.receive);
 const empty=normalizeHostSnapshot({
  schema:"MEU_ARTIGO_SITE_V1",
  tasks:[],gates:[],
  next_action:{code:null,explanation:null,responsible:null}
 });
 assert.equal(host.receive({...empty,kind:"CANONICAL_LOCAL_SNAPSHOT"}),true);
 const overview=d.getElementById("content");
 const rendered=overview.textContent;
 assert.match(rendered,/Nenhuma próxima ação registrada/);
 assert.match(rendered,/Nenhum gate exibido/);
 assert.match(rendered,/Nenhum gate ou aprovação foi apresentado/);
 assert.doesNotMatch(rendered,/UNKNOWN|CONTINUIDADE\.md|0 de não informado/);
 assert.equal(overview.querySelectorAll(".gate-dot").length,0,
  "No imaginary 7-gate sequence may appear when registry total is unknown");
 assert.equal(overview.querySelectorAll('button[data-go="tasks"]').length,0,
  "No task CTA when neither action nor task was supplied");
 d.querySelector('nav button[data-page="validations"]').click();
 assert.match(d.getElementById("content").textContent,/Sem estados de validação disponíveis/);
 const a=make("ALPHA"),b=make("BRAVO");
 assert.equal(host.receive({...a,kind:"CANONICAL_LOCAL_SNAPSHOT"}),true);
 assert.equal(d.querySelectorAll("nav button[data-page]").length,10);
 const tasks=d.querySelector('nav button[data-page="tasks"]');
 tasks.click();
 assert.match(d.getElementById("content").textContent,/Synthetic task ALPHA/);
 assert.ok(!d.getElementById("content").textContent.includes("BRAVO"));
 assert.equal(host.receive({...b,kind:"CANONICAL_LOCAL_SNAPSHOT"}),true);
 d.querySelector('nav button[data-page="tasks"]').click();
 assert.match(d.getElementById("content").textContent,/Synthetic task BRAVO/);
 assert.ok(!d.getElementById("content").textContent.includes("Synthetic task ALPHA"));
 d.querySelector('nav button[data-page="validations"]').click();
 assert.match(d.getElementById("content").textContent,/GATE-0001/);
 assert.match(d.getElementById("content").textContent,/Sem aprovação verificada/);
 assert.equal(d.querySelectorAll('script[src]').length,0);
 assert.equal(d.querySelectorAll('img[onerror]').length,0);
 host.disconnect();
 assert.ok(!d.getElementById("content").textContent.includes("BRAVO"));
 assert.equal(errors.length,0,errors.join("; "));
 console.log("HOST_PROJECTION_UI_PASS: 10 screens, A/B replace, seven gates, no stale researcher data after disconnect.");
}finally{dom.window.close();}
