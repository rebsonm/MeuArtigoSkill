/** End-to-end OAuth HTTP discovery + protected endpoint, fake tenant only. */
import assert from "node:assert/strict";
import { spawn } from "node:child_process";

const port=18857;
const endpoint="http://127.0.0.1:"+port;
const resource="https://mcp.allflux.com.br/mcp";
const issuer="https://dev-meu-artigo-fixture.us.auth0.com/";
const env={...process.env,
  MEU_ARTIGO_AUTH_MODE:"auth0",
  MEU_ARTIGO_AUTH_ISSUER:issuer,
  MEU_ARTIGO_AUTH_RESOURCE:resource,
  MEU_ARTIGO_PILOT_SUB:"google-oauth2|synthetic-pilot-001",
  MEU_ARTIGO_MCP_PORT:String(port),
  MEU_ARTIGO_BIND_HOST:"127.0.0.1",
  MEU_ARTIGO_PROJECT_ROOT:""
};
const child=spawn(process.execPath,["server.mjs","--http"],
  {env,stdio:["ignore","ignore","pipe"]});
try{
 let ready=false;
 for(let i=0;i<70;i++){
  if(child.exitCode!==null)throw Error("OAuth server failed to start");
  try{
   const response=await fetch(endpoint+"/.well-known/oauth-protected-resource");
   if(response.status===200){ready=true;break;}
  }catch{}
  await new Promise(r=>setTimeout(r,100));
 }
 assert.ok(ready,"OAuth metadata server not ready");
 for(const path of ["/.well-known/oauth-protected-resource",
                    "/.well-known/oauth-protected-resource/mcp"]){
  const r=await fetch(endpoint+path);
  assert.equal(r.status,200);
  assert.deepEqual(await r.json(),{
   resource,
   authorization_servers:[issuer],
   scopes_supported:["mcp:read"]
  });
 }
 const unauthorized=await fetch(endpoint+"/mcp",{method:"POST",body:"{}",
  headers:{"content-type":"application/json"}});
 assert.equal(unauthorized.status,401);
 assert.match(unauthorized.headers.get("www-authenticate")||"",
  /resource_metadata="https:\/\/mcp\.allflux\.com\.br\/\.well-known\/oauth-protected-resource"/);
 const invalid=await fetch(endpoint+"/mcp",{method:"POST",body:"{}",
  headers:{"authorization":"Bearer this-is-not-a-valid-jwt"}});
 assert.equal(invalid.status,401);
 const disallowedOrigin=await fetch(endpoint+"/mcp",{method:"POST",body:"{}",
  headers:{"origin":"https://untrusted.example"}});
 assert.equal(disallowedOrigin.status,403);
 const unknown=await fetch(endpoint+"/other");
 assert.equal(unknown.status,404);
 const incorrectScheme=await fetch(endpoint+"/mcp",{method:"POST",
  headers:{"content-type":"application/json","authorization":"Basic "+("a".repeat(40))},
  body:"{}"});
 assert.equal(incorrectScheme.status,401);
 const missingTokenHeader=await fetch(endpoint+"/mcp",{method:"POST",
  headers:{"content-type":"application/json","authorization":"Bearer "+("b".repeat(90))},body:"{}"});
 assert.equal(missingTokenHeader.status,401);
 assert.equal(missingTokenHeader.headers.get("cache-control"),"no-store");
 const wrongMime=await fetch(endpoint+"/mcp",{method:"POST",
  headers:{"content-type":"text/plain","authorization":"Bearer "+("c".repeat(90))},body:"{}"});
 assert.equal(wrongMime.status,401);
 const noPrivateMetadata=await fetch(endpoint+"/.well-known/oauth-protected-resource",
   {method:"POST",headers:{"content-type":"application/json"},body:"{}"});
 assert.equal(noPrivateMetadata.status,404);

 console.log("OAuth HTTP: RFC 9728 discovery, 401 Bearer challenge, origin and invalid-token denials pass.");
}finally{
 child.kill("SIGTERM");
}
// The staged OAuth resource must not be externally bound, even if legacy
// reverse-proxy approval flags are set. These are fictional local processes.
async function expectStartupDenied(overrides,expected){
 const probe=spawn(process.execPath,["server.mjs","--http"],{
  env:{...env,MEU_ARTIGO_MCP_PORT:"18961",...overrides},
  stdio:["ignore","ignore","pipe"]
 });
 let stderr="";
 probe.stderr.on("data",part=>stderr+=part.toString("utf8"));
 const code=await Promise.race([
  new Promise(resolve=>probe.once("exit",resolve)),
  new Promise(resolve=>setTimeout(()=>resolve("TIMEOUT"),3000))
 ]);
 if(code==="TIMEOUT")probe.kill("SIGTERM");
 assert.notEqual(code,"TIMEOUT","Auth0 invalid configuration must reject before binding");
 assert.notEqual(code,0);
 assert.match(stderr,expected);
}
await expectStartupDenied(
 {MEU_ARTIGO_BIND_HOST:"0.0.0.0",
  MEU_ARTIGO_PROXY_TLS_CONFIRMED:"YES",
  MEU_ARTIGO_SINGLE_USER_ISOLATED:"YES"},
 /PUBLIC_HTTP_BIND_BLOCKED_UNTIL_AUTH0_OAUTH/);
await expectStartupDenied({MEU_ARTIGO_PILOT_SUB:""},/allowlisted/);
await expectStartupDenied({MEU_ARTIGO_AUTH_RESOURCE:"http:\/\/invalid.example\/mcp"},
 /Invalid resource/);
console.log("OAuth pilot startup: public binding, absent user allowlist and HTTP audience rejected.");

