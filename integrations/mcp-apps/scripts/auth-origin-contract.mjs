/** Offline regression: exact HTTPS browser Origin config, and fail-closed HTTP startup.
 * The test opens only a temporary loopback socket with fictitious bearer.
 * This does NOT verify live ChatGPT OAuth/PKCE or external user isolation.
 */
import assert from "node:assert/strict";
import {spawn} from "node:child_process";
import {configuredAllowedOrigin} from "../server.mjs";

const valid=["","https://chatgpt.com","https://trusted.example:8443"];
for(const value of valid){
 assert.equal(configuredAllowedOrigin({MEU_ARTIGO_ALLOWED_ORIGIN:value}),value);
}
assert.equal(configuredAllowedOrigin({}),"");
const invalid=[
 "null","*","http://trusted.example","http://127.0.0.1:8085",
 "https://trusted.example/","https://trusted.example/path",
 "https://trusted.example?foo=1","https://trusted.example#fragment",
 "https://user:pass@trusted.example","https://trusted.example:443",
 "https://trusted.example ","https://trusted.example/../",
 "file:///etc/hosts","data:text/plain,unsafe","ws://trusted.example"
];
for(const value of invalid){
 assert.throws(()=>configuredAllowedOrigin({MEU_ARTIGO_ALLOWED_ORIGIN:value}),
  /INVALID_ALLOWED_ORIGIN/, "Should refuse "+value);
}
for(const value of [null,17,{},["https://trusted.example"]]){
 assert.throws(()=>configuredAllowedOrigin({MEU_ARTIGO_ALLOWED_ORIGIN:value}),
  /INVALID_ALLOWED_ORIGIN/);
}

const PORT=18974;
const TOKEN="SYNTHETIC_HTTP_TEST_SECRET_NEVER_PRODUCTION_02468";
const BASE="http://127.0.0.1:"+PORT+"/mcp";
const env={...process.env,
 MEU_ARTIGO_AUTH_MODE:"bearer",MEU_ARTIGO_MCP_BEARER:TOKEN,
 MEU_ARTIGO_MCP_PORT:String(PORT),MEU_ARTIGO_BIND_HOST:"127.0.0.1",
 MEU_ARTIGO_ALLOWED_ORIGIN:"https://chatgpt.com",MEU_ARTIGO_PROJECT_ROOT:"",
 MEU_ARTIGO_E05_SYNTHETIC_ONLY:""
};
function launch(overrides={},port=PORT){
 return spawn(process.execPath,["server.mjs","--http"],{
  env:{...env,MEU_ARTIGO_MCP_PORT:String(port),...overrides},
  stdio:["ignore","ignore","pipe"]
 });
}
const proc=launch();
try{
 let ready=false;
 for(let i=0;i<70;i++){
  if(proc.exitCode!==null)throw Error("Origin test HTTP server failed to start");
  try{
   const response=await fetch(BASE,{method:"POST",body:"{}",
    headers:{"content-type":"application/json"}});
   if(response.status===401){ready=true;break;}
  }catch{}
  await new Promise(resolve=>setTimeout(resolve,100));
 }
 assert.ok(ready,"Origin test HTTP loopback was not ready");
 const request=origin=>fetch(BASE,{
  method:"POST",body:"{}",
  headers:{"authorization":"Bearer "+TOKEN,"content-type":"application/json",
   ...(origin===undefined?{}:{"origin":origin})}
 });
 for(const origin of ["null","http://chatgpt.com","https://other.example",
  "https://chatgpt.com:443","https://chatgpt.com.evil.example"]){
  const response=await request(origin);
  assert.equal(response.status,403,"Bad Origin must reject: "+origin);
 }
 for(const origin of ["https://chatgpt.com",undefined]){
  const response=await request(origin);
  assert.notEqual(response.status,403,"Trusted auth/no-Origin must pass Origin check");
  assert.notEqual(response.status,401,"Authenticated bearer must pass auth check");
 }
}finally{proc.kill("SIGTERM");}

async function expectStartupDenied(raw,mode,port){
 const child=launch({MEU_ARTIGO_ALLOWED_ORIGIN:raw,
   MEU_ARTIGO_AUTH_MODE:mode,
   MEU_ARTIGO_AUTH_ISSUER:"https://synthetic.us.auth0.com/",
   MEU_ARTIGO_AUTH_RESOURCE:"https://synthetic.example/mcp",
   MEU_ARTIGO_PILOT_SUB:"google-oauth2|synthetic-user-001"},port);
 let stderr="";
 child.stderr.on("data",part=>{stderr+=part.toString("utf8").slice(0,4096);});
 const result=await Promise.race([
  new Promise(resolve=>child.once("exit",resolve)),
  new Promise(resolve=>setTimeout(()=>resolve("TIMEOUT"),3500))
 ]);
 if(result==="TIMEOUT")child.kill("SIGTERM");
 assert.notEqual(result,"TIMEOUT","Unsafe origin must refuse startup without bind");
 assert.notEqual(result,0,"Unsafe Origin accepted");
 assert.match(stderr,/INVALID_ALLOWED_ORIGIN/);
}
for(const mode of ["bearer","auth0"]){
 await expectStartupDenied("null",mode,18975);
 await expectStartupDenied("https://chatgpt.com/path",mode,18975);
}
console.log("HTTP_ORIGIN_FAIL_CLOSED_PASS: canonical HTTPS only, invalid origins reject before bind; loopback bearer smoke and Auth0 startup denial tested.");
