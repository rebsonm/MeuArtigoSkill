/* Contract tests for browser locale, navigation and host data on the real UI
 * template using ONLY synthetic snapshots. Not a production browser certificate. */
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { JSDOM, VirtualConsole } from "jsdom";
import path from "node:path";
const html=await readFile(path.resolve("../../assets/research_site.html"),"utf8");
const neutral={schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"auto"};
const preview={schema:"MEU_ARTIGO_SITE_V1",kind:"ILLUSTRATIVE_PREVIEW",locale:"en"};
const errors=[];
const vc=new VirtualConsole();
vc.on("jsdomError",e=>errors.push(e.message));
async function start(model,lang="en-US"){
 const filled=html.replace("__MEU_ARTIGO_SITE_MODEL_JSON__",JSON.stringify(model));
 return new JSDOM(filled,{url:"https://host.local/",runScripts:"dangerously",
  pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
    Object.defineProperty(w.navigator,"languages",{get:()=>[lang]});
    Object.defineProperty(w.navigator,"language",{get:()=>lang});
 }});
}
{
 const dom=await start(preview,"en-US");
 const d=dom.window.document;
 assert.equal(d.documentElement.lang,"en");
 assert.match(d.querySelector("nav").textContent,/Overview/);
 d.querySelector('button[data-page="methods"]').click();
 assert.match(d.getElementById("content").textContent,/Explore research methods/);
 const selected=d.querySelector('button[data-method="dsr"]');
 assert.ok(selected);
 selected.click();
 assert.equal(d.querySelector('button[data-method="dsr"]').getAttribute("aria-pressed"),"true");
 d.getElementById("site-language").value="es";
 d.getElementById("site-language").dispatchEvent(new dom.window.Event("change",{bubbles:true}));
 assert.equal(d.documentElement.lang,"es");
 assert.match(d.querySelector("nav").textContent,/Vista general/);
 assert.match(d.getElementById("content").textContent,/Explorar enfoques metodológicos/);
 dom.window.close();
}
{
 const dom=await start(neutral,"fr-FR");
 const d=dom.window.document;
 assert.doesNotMatch(d.getElementById("content").textContent,/12\/20|2\/7/);
 assert.match(d.getElementById("content").textContent,/Tableau indisponible/);
 const actual={schema:"MEU_ARTIGO_SITE_V1",kind:"CANONICAL_LOCAL_SNAPSHOT",
 locale:"fr",active_route:"QUALITATIVE",documented_gate_count:0,
 tasks:[{id:"CADA-0001",task:"Do not translate source content",
 execution_owner:"Researcher",deadline:null}],
 gates:[],canonical_drive_sync_verified:false,
 automatic_scientific_approval:false,canonical_writes_allowed:false,
 next_action:{code:"HUMAN_REVIEW_REQUIRED",
 explanation:"Revisar a estratégia de busca e seus critérios",responsible:"HUMAN_RESEARCHER"}};
 assert.equal(dom.window.MeuArtigoHost.receive(actual),true);
 assert.match(d.getElementById("content").textContent,/HUMAN_REVIEW_REQUIRED/);
 assert.doesNotMatch(d.getElementById("content").textContent,/12\/20|2\/7/);
 assert.equal(d.documentElement.lang,"fr");
 d.querySelector('button[data-page="tasks"]').click();
 assert.match(d.getElementById("content").textContent,/CADA-0001/);
 d.querySelector('button[data-page="methods"]').click();
 assert.equal(d.querySelectorAll('button[data-method]').length,4);
 d.querySelector('button[data-page="overview"]').click();
 dom.window.MeuArtigoHost.locale("en");
 assert.match(d.getElementById("content").textContent,/Revisar a estratégia de busca e seus critérios/);
 const falseData={schema:"MEU_ARTIGO_SITE_V1",kind:"ILLUSTRATIVE_PREVIEW",tasks:[],gates:[]};
 assert.equal(dom.window.MeuArtigoHost.receive(falseData),false);
 dom.window.close();
}
assert.equal(errors.length,0,errors.join("; "));
console.log("Read-only site i18n/browser smoke passed: EN/ES/FR, methods, connected data, no fake KPIs.");
