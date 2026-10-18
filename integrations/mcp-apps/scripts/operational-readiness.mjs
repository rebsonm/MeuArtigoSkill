/** Local-only operation preflight: no real accounts, keys, Drive or deployment.
 * Checks the two authenticated transport modes and the public *minimal*
 * loopback liveness/readiness response. Does not certify HTTPS, OAuth/PKCE,
 * effective host CSP, A/B isolation or scientific validity.
 */
import assert from "node:assert/strict";
import {spawn} from "node:child_process";
import {createServer as createHttpServer} from "node:http";
import {configureHttpLimits} from "../server.mjs";

// Assert concrete operational limits without waiting real timeout periods.
const configured=configureHttpLimits(createHttpServer());
assert.equal(configured.headersTimeout,10000);
assert.equal(configured.requestTimeout,15000);
assert.equal(configured.timeout,15000);
assert.equal(configured.keepAliveTimeout,5000);
assert.equal(configured.maxConnections,64);
assert.equal(configured.maxRequestsPerSocket,64);
assert.equal(configured.maxHeadersCount,64);
configured.closeAllConnections();

const TOKEN="SYNTHETIC_READINESS_TEST_BEARER_NEVER_PRODUCTION_123456";
const baseEnv={...process.env,MEU_ARTIGO_PROJECT_ROOT:"",
 MEU_ARTIGO_GOOGLE_TOKEN_DIR:"",MEU_ARTIGO_GOOGLE_CLIENT_SECRET:"",
 MEU_ARTIGO_MCP_BEARER:TOKEN,MEU_ARTIGO_ALLOWED_ORIGIN:"",
 MEU_ARTIGO_BIND_HOST:"127.0.0.1",MEU_ARTIGO_E05_SYNTHETIC_ONLY:""};
async function check(mode,port){
 const endpoint="http://127.0.0.1:"+port;
 const child=spawn(process.execPath,["server.mjs","--http"],{
  env:{...baseEnv,MEU_ARTIGO_AUTH_MODE:mode,MEU_ARTIGO_MCP_PORT:String(port),
    MEU_ARTIGO_AUTH_ISSUER:"https://synthetic-demo.us.auth0.com/",
    MEU_ARTIGO_AUTH_RESOURCE:"https://synthetic.example/mcp",
    MEU_ARTIGO_PILOT_SUB:"google-oauth2|synthetic-test-12345"},
  stdio:["ignore","ignore","pipe"]});
 try{
  let ready=false;
  for(let i=0;i<70;i++){
   if(child.exitCode!==null)throw Error("Readiness process unexpectedly exited");
   try{
    const r=await fetch(endpoint+"/readyz");
    if(r.status===200){ready=true;break;}
   }catch{}
   await new Promise(done=>setTimeout(done,100));
  }
  assert.ok(ready,"Reviewed UI must assemble before HTTP bind");
  for(const pathname of ["/healthz","/readyz"]){
   const r=await fetch(endpoint+pathname);
   assert.equal(r.status,200);
   assert.deepEqual(await r.json(),{status:"ok"});
   assert.equal(r.headers.get("cache-control"),"no-store");
   assert.equal(r.headers.get("x-content-type-options"),"nosniff");
   assert.equal(r.headers.get("access-control-allow-origin"),null);
   const bad=await fetch(endpoint+pathname,{method:"POST",body:"{}"});
   assert.equal(bad.status,405);
  }
  for(const pathname of ["/metrics","/debug","/admin","/google/oauth/callback"]){
   const r=await fetch(endpoint+pathname);
   assert.equal(r.status,404,"No extra operational surface: "+pathname);
  }
  // Node's fixed per-request header limit must reject oversized headers
  // before JWT verification, JSON parsing, or MCP tool dispatch.
  const enormous=await fetch(endpoint+"/mcp",{
   method:"POST",headers:{"content-type":"application/json",
     "x-synthetic-large-header":"X".repeat(20*1024)},
   body:"{}"});
  assert.equal(enormous.status,431);
  const denied=await fetch(endpoint+"/mcp",{method:"POST",
   headers:{"content-type":"application/json"},body:"{}"});
  assert.equal(denied.status,401,"Operational probe must not remove auth");
  assert.equal(denied.headers.get("access-control-allow-origin"),null);
  // Invalid browser Origin is denied even with a valid bearer; readiness is
  // never counted as permission to call the protected MCP method.
  if(mode==="bearer"){
   const bad=await fetch(endpoint+"/mcp",{method:"POST",body:"{}",
    headers:{"authorization":"Bearer "+TOKEN,"origin":"https://bad.example",
     "content-type":"application/json"}});
   assert.equal(bad.status,403);
  }
 }finally{
  if(child.exitCode===null && child.signalCode===null){
   const stopped=new Promise(done=>child.once("exit",done));
   child.kill("SIGTERM");
   await stopped;
  }
 }
}
await check("bearer",18862);
await check("auth0",18863);
console.log("OPERATIONAL_LOOPBACK_PROBE_PASS: preflight, minimal health/ready, no auth bypass (synthetic).");
