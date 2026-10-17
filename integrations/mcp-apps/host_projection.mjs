/** One-request, display-only projection from the current researcher's ChatGPT session.
 * The MCP never fetches Drive files. Reject extras, private document bodies,
 * provenance claims, auto-approval and oversized projections.
 */
export const HOST_SCHEMA="MEU_ARTIGO_SITE_V1";
const keys=(x,allow,required=allow)=>{
 if(!x||typeof x!=="object"||Array.isArray(x))return false;
 const present=Object.keys(x);
 return present.every(k=>allow.includes(k))&&required.every(k=>Object.hasOwn(x,k));
};
const str=(v,max=120)=>v===null||(typeof v==="string"&&v.length<=max&&
 !/[\u0000-\u0008\u000b\u000e-\u001f]/.test(v));
const flag=(v)=>typeof v==="boolean";
const natural=(n,max)=>n===null||(Number.isSafeInteger(n)&&n>=0&&n<=max);
const diagKeys=["schema","status","verdict","objective_blockers",
 "review_occurrences","advisory_occurrences","strict_required_occurrences",
 "priority_codes","human_review_required","semantic_support_proven",
 "scientific_quality_validated","scientific_gate_approved",
 "reports_written","drive_sync_verified"];
const report=error=>{throw Error("HOST_PROJECTION_REJECTED_"+error)};
export function normalizeHostSnapshot(input){
 const allowed=["schema","tasks","gates","next_action","active_route",
  "gate_view_partial","registered_gate_total","scientific_diagnostic"];
 if(!keys(input,allowed,["schema","tasks","gates","next_action"]))
  report("SHAPE");
 if(input.schema!==HOST_SCHEMA)report("SCHEMA");
 if(!Array.isArray(input.tasks)||input.tasks.length>200||
    !Array.isArray(input.gates)||input.gates.length>7)report("LIMIT");
 if(!str(input.active_route??null,120))report("ROUTE");
 if(input.gate_view_partial!==undefined&&!flag(input.gate_view_partial))report("GATE_PARTIAL");
 if(input.registered_gate_total!==undefined&&!natural(input.registered_gate_total,7))
  report("TOTAL");
 const taskKeys=["id","task","execution_owner","deadline"];
 const tasks=input.tasks.map(t=>{
  if(!keys(t,taskKeys))report("TASK_SHAPE");
  if(!str(t.id,120)||!str(t.task,600)||!str(t.execution_owner,120)||!str(t.deadline,120))
   report("TASK_VALUE");
  return {id:t.id,task:t.task,execution_owner:t.execution_owner,deadline:t.deadline};
 });
 const gateKeys=["id","approval_documented"];
 const gates=input.gates.map(g=>{
  if(!keys(g,gateKeys)||!str(g.id,120)||!flag(g.approval_documented))
   report("GATE_VALUE");
  return {id:g.id,approval_documented:g.approval_documented};
 });
 const actionKeys=["code","explanation","responsible"];
 if(!keys(input.next_action,actionKeys)||
    !str(input.next_action.code,120)||
    !str(input.next_action.explanation,600)||
    !str(input.next_action.responsible,120))report("ACTION");
 const total=input.registered_gate_total??null;
 if(total!==null&&total<gates.length)report("GATE_TOTAL");
 if(input.gate_view_partial===false&&total!==null&&total>gates.length)
  report("GATE_INCOMPLETE_UNMARKED");
 let diagnostic=null;
 if(input.scientific_diagnostic!==undefined&&input.scientific_diagnostic!==null){
  const d=input.scientific_diagnostic;
  if(!keys(d,diagKeys)||d.schema!=="MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1"||
     !["RECORDED_UNASSESSED","INPUTS_UNAVAILABLE"].includes(d.status)||
     ![null,"CORRECAO_REQUERIDA","REVISAO_CIENTIFICA_PENDENTE"].includes(d.verdict)||
     d.human_review_required!==true||
     ["semantic_support_proven","scientific_quality_validated",
      "scientific_gate_approved","reports_written","drive_sync_verified"]
      .some(k=>d[k]!==false))report("DIAGNOSTIC");
  const counters=["objective_blockers","review_occurrences","advisory_occurrences",
    "strict_required_occurrences"];
  if(counters.some(k=>!natural(d[k],1_000_000)||
      (d.status==="INPUTS_UNAVAILABLE"&&d[k]!==null)))report("DIAGNOSTIC_COUNTS");
  if(!Array.isArray(d.priority_codes)||d.priority_codes.length>6||
     !d.priority_codes.every(c=>typeof c==="string"&&/^[A-Z][A-Z0-9_]{0,63}$/.test(c)))
    report("DIAGNOSTIC_CODES");
  diagnostic=Object.fromEntries(diagKeys.map(k=>[k,k==="priority_codes"?[...d[k]]:d[k]]));
 }
 const out={
  schema:HOST_SCHEMA,kind:"HOST_AUTHORIZED_SNAPSHOT",
  active_route:input.active_route??null,
  documented_gate_count:gates.filter(x=>x.approval_documented).length,
  gate_view_partial:input.gate_view_partial===true||
    (total!==null&&total>gates.length),
  registered_gate_total:total,
  tasks,gates,next_action:{...input.next_action},
  scientific_diagnostic:diagnostic,
  canonical_drive_sync_verified:false,
  automatic_scientific_approval:false,
  canonical_writes_allowed:false
 };
 if(Buffer.byteLength(JSON.stringify(out),"utf8")>96*1024)report("BYTES");
 return out;
}
