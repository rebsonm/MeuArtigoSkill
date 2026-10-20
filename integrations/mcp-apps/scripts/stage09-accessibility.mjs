/* Synthetic browser contract for ten screens, four UI locales, and fail-closed host data.
   No production browser, scientific approval, filesystem write or network call. */
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { JSDOM, VirtualConsole } from "jsdom";
import path from "node:path";

const html=await readFile(path.resolve("../../assets/research_site.html"),"utf8");
const templateMarker="__MEU_ARTIGO_SITE_MODEL_JSON__";
assert.equal(html.split(templateMarker).length,2);
const initial={schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"auto"};
const all=["overview","steps","tasks","sources","evidence","validations",
           "methods","trace","submission","sync"];
const strings={pt:/Painel indisponível/,en:/No authorized project data/,
  es:/Panel no disponible/,fr:/Tableau indisponible/};
const vc=new VirtualConsole(),errors=[];
vc.on("jsdomError",e=>errors.push(e.message));
const dom=new JSDOM(html.replace(templateMarker,JSON.stringify(initial)),{
 url:"https://isolated-host.invalid/",runScripts:"dangerously",
 pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  Object.defineProperty(w.navigator,"languages",{get:()=>["en-US"]});
  Object.defineProperty(w.navigator,"language",{get:()=>"en-US"});
 }});
const d=dom.window.document;
assert.equal(d.querySelectorAll("nav button[data-page]").length,10);
assert.equal(d.querySelector(".skip-link").getAttribute("href"),"#content");
assert.equal(d.getElementById("content").getAttribute("tabindex"),"-1");
assert.ok(d.getElementById("screen-status").getAttribute("aria-live"));
assert.match(html,/@media\(max-width:650px\)/);
assert.match(html,/@media\(prefers-reduced-motion:reduce\)/);
assert.match(html,/connect-src 'none'/);
for(const [locale,heading] of Object.entries(strings)){
 dom.window.MeuArtigoHost.locale(locale);
 assert.match(d.getElementById("content").textContent,heading);
 for(const page of all){
  d.querySelector('nav button[data-page="'+page+'"]').click();
  assert.equal(d.querySelector('nav button[aria-current="page"]').dataset.page,page);
  assert.match(d.getElementById("content").textContent,heading);
  assert.equal(d.activeElement,d.getElementById("content"));
 }
}
const forged="<img src=x onerror=alert(101)>";
const site={schema:"MEU_ARTIGO_SITE_V1",kind:"CANONICAL_LOCAL_SNAPSHOT",
 locale:"fr",active_route:"QUALITATIVE",documented_gate_count:7,
 canonical_drive_sync_verified:false,canonical_writes_allowed:false,
 automatic_scientific_approval:false,
 tasks:[{id:"CADA-0001",task:forged,execution_owner:"Pesquisador",deadline:null}],
 gates:[{id:"GATE-0001",approval_documented:true},
        {id:"GATE-0002",approval_documented:false}],
 next_action:{code:"HUMAN_REVIEW_REQUIRED",
 explanation:"Revisar a estratégia de busca e seus critérios",
 responsible:"HUMAN_RESEARCHER"}};
assert.equal(dom.window.MeuArtigoHost.receive(site),true);
assert.equal(d.documentElement.lang,"fr");
assert.doesNotMatch(d.getElementById("content").textContent,/12\/20|2\/7/);
assert.match(d.getElementById("content").textContent,/2 gate\(s\) exibidos/);
assert.equal(d.getElementById("content").querySelectorAll(".gate-dot.done").length,1);
d.querySelector('button[data-page="tasks"]').click();
assert.match(d.getElementById("content").textContent,/CADA-0001/);
assert.match(d.getElementById("content").textContent,/<img src=x onerror=alert\(101\)>/);
assert.equal(d.getElementById("content").querySelectorAll("img").length,0);
assert.doesNotMatch(d.getElementById("content").textContent,/Fonte: demonstração fictícia/);
d.querySelector('button[data-page="overview"]').click();
assert.match(d.getElementById("content").textContent,/Revisar a estratégia de busca e seus critérios/);
d.querySelector('button[data-page="methods"]').click();
assert.equal(d.getElementById("content").querySelectorAll('[data-method]').length,4);
const stageMethod=d.querySelector('button[data-method="dsr"]');
stageMethod.click();
assert.equal(d.querySelector('button[data-method="dsr"]').getAttribute("aria-pressed"),"true");
assert.doesNotMatch(d.getElementById("content").textContent,/GATE-0001 · Pergunta/);
assert.match(d.getElementById("content").textContent,/méthode enregistrée/);
d.querySelector('button[data-page="overview"]').click();
assert.equal(dom.window.MeuArtigoHost.receive({...site,canonical_drive_sync_verified:true}),false);
assert.match(d.getElementById("content").textContent,/Tableau indisponible/);
assert.doesNotMatch(d.getElementById("content").textContent,/HUMAN_REVIEW_REQUIRED|CADA-0001/);
assert.match(d.querySelector(".mock-badge").textContent,/EN ATTENTE DE DONNÉES|AGUARDANDO DADOS/);
const poisoned={...site,canonical_drive_sync_verified:false,
 tasks:[{id:"CADA-002",task:{html:"<svg>"},execution_owner:"Researcher"}]};
assert.equal(dom.window.MeuArtigoHost.receive(poisoned),false);
assert.equal(dom.window.MeuArtigoHost.receive(site),true);
dom.window.MeuArtigoHost.disconnect();
assert.match(d.getElementById("content").textContent,/Tableau indisponible/);
assert.equal(errors.length,0,errors.join("; "));
dom.window.close();
console.log("Stage09 synthetic UI verified: 10 sections x 4 locales, accessibility structure, XSS encoding, host revocation.");
