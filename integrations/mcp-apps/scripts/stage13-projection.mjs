/* Stage 13: synthetic contract: technical triage is distinct from gate approval.
 * No live MCP, project text, source passage or actual permissions.
 */
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {JSDOM,VirtualConsole} from "jsdom";
import path from "node:path";
const html=await readFile(path.resolve("../../assets/research_site.html"),"utf8");
const slot="__MEU_ARTIGO_SITE_MODEL_JSON__";
assert.equal(html.split(slot).length,2);
const vc=new VirtualConsole(),errors=[];
vc.on("jsdomError",e=>errors.push(e.message));
const dom=new JSDOM(html.replace(slot,JSON.stringify({
 schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"pt"
})),{url:"https://synthetic.invalid",runScripts:"dangerously",
 pretendToBeVisual:true,virtualConsole:vc});
const d=dom.window.document;
const base={schema:"MEU_ARTIGO_SITE_V1",kind:"CANONICAL_LOCAL_SNAPSHOT",
 active_route:"QUALITATIVE",locale:"pt",documented_gate_count:0,
 tasks:[],gates:[],next_action:{code:"HUMAN_REVIEW_REQUIRED",
 explanation:"Consult canonical records",responsible:"HUMAN_RESEARCHER"},
 canonical_drive_sync_verified:false,automatic_scientific_approval:false,
 canonical_writes_allowed:false};
const unavailable={schema:"MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1",
 status:"INPUTS_UNAVAILABLE",verdict:null,objective_blockers:null,
 review_occurrences:null,advisory_occurrences:null,
 strict_required_occurrences:null,priority_codes:[],
 human_review_required:true,semantic_support_proven:false,
 scientific_quality_validated:false,scientific_gate_approved:false,
 reports_written:false,drive_sync_verified:false};
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:unavailable
}),true);
d.querySelector('nav button[data-page="evidence"]').click();
assert.match(d.getElementById("content").textContent,/Diagnóstico técnico indisponível/);
assert.doesNotMatch(d.getElementById("content").textContent,/Conflitos objetivos: 0/);
const known={...unavailable,status:"RECORDED_UNASSESSED",
 verdict:"CORRECAO_REQUERIDA",objective_blockers:2,
 review_occurrences:3,advisory_occurrences:5,
 strict_required_occurrences:4,priority_codes:["UNKNOWN_REFERENCE",
 "CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH"]};
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:known
}),true);
for(const view of ["evidence","validations"]){
 d.querySelector('nav button[data-page="'+view+'"]').click();
 const text=d.getElementById("content").textContent;
 assert.match(text,/Conflitos objetivos: 2/);
 assert.match(text,/Indícios semânticos ADVISORY: 5/);
 assert.match(text,/UNKNOWN_REFERENCE/);
 assert.match(text,/Não autentica pareceristas/);
 assert.doesNotMatch(text,/Pesquisa aprovada|Validação científica independente/);
}
const malicious={...known,priority_codes:["<img src=x onerror=alert(99)>"]};
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:malicious
}),false);
assert.match(d.getElementById("content").textContent,/Painel indisponível/);
assert.equal(d.querySelectorAll("img").length,0);
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:{...known,scientific_quality_validated:true}
}),false);
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:{...unavailable,objective_blockers:0}
}),false);
assert.equal(dom.window.MeuArtigoHost.receive({
 ...base,scientific_diagnostic:known
}),true);
d.querySelector('nav button[data-page="steps"]').click();
assert.match(d.getElementById("content").textContent,/Nenhum registro de gate disponível/);
assert.equal(d.querySelectorAll(".gate-dot.done").length,0);
assert.equal(errors.length,0,errors.join("; "));
dom.window.close();
console.log("Stage13 browser contract passed: null≠zero, advisory segregation, malicious code rejected, no auto-gate.");
