/** Security regression: MCP is a generic UI, not a research/Drive reader.
 * User-specific documents remain in each researcher's ChatGPT Google Drive connector.
 */
import assert from "node:assert/strict";
import {mkdtemp,mkdir,writeFile,readFile,rm} from "node:fs/promises";
import {createServer as createHttpServer} from "node:http";
import {generateKeyPair,exportJWK,SignJWT} from "jose";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {StdioClientTransport} from "@modelcontextprotocol/sdk/client/stdio.js";
import {spawn} from "node:child_process";
import path from "node:path";
import os from "node:os";
import {createServer} from "../server.mjs";
import {auth0Configuration,createAuth0Verifier} from "../auth0.mjs";

const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-host-only-"));
const secret="RESEARCHER_A_UNDISCLOSED_CONTENT_9F7B";
const filename=path.join(root,"private-paper.txt");
const dispose=[];
try{
 await writeFile(filename,secret);
 const mcp=createServer();
 const client=new Client({name:"host-boundary",version:"0.1.0"});
 const [a,b]=InMemoryTransport.createLinkedPair();
 await mcp.connect(a);
 await client.connect(b);
 dispose.push(async()=>{await client.close();await mcp.close();});
 const tools=await client.listTools();
 assert.deepEqual(tools.tools.map(t=>t.name),["meu_artigo_painel"]);
 assert.deepEqual(Object.keys(tools.tools[0].inputSchema.properties).sort(),["locale","mode"]);
 const output=await client.callTool({name:"meu_artigo_painel",
  arguments:{locale:"pt",mode:"FULL",project_id:root,document:secret}});
 assert.equal(output.isError,true);
 assert.equal(output.structuredContent,undefined);
 assert.match(output.content[0].text,/Google Drive individual do ChatGPT/);
 const resource=await client.readResource({uri:"ui://meu-artigo/site-v1.html"});
 assert.equal(resource.contents.length,1);
 const all=JSON.stringify(output)+JSON.stringify(resource);
 assert.ok(all.includes("HOST_NOT_CONNECTED"));
 assert.ok(!all.includes(secret)&&!all.includes(root)&&!all.includes("CANONICAL_LOCAL_SNAPSHOT"));
 assert.equal(await readFile(filename,"utf8"),secret);
 // Production and stdio cannot silently enable a research folder, Google
 // credential, tenant registry or user data adapter through env variables.
 for(const name of [
  "MEU_ARTIGO_PROJECT_ROOT","MEU_ARTIGO_TENANT_DATA_ROOT",
  "MEU_ARTIGO_MULTIUSER_REGISTRY","MEU_ARTIGO_GOOGLE_DRIVE_MODE",
  "MEU_ARTIGO_GOOGLE_CLIENT_SECRET","MEU_ARTIGO_GOOGLE_TOKEN_DIR"
 ]){
  const prior=process.env[name];process.env[name]="synthetic-forbidden";
  assert.throws(()=>createServer(),/MCP_RESEARCH_ACCESS_FORBIDDEN/);
  if(prior===undefined)delete process.env[name];else process.env[name]=prior;
 }
 const proc=spawn(process.execPath,["server.mjs","--stdio"],{
  env:{...process.env,MEU_ARTIGO_PROJECT_ROOT:root},
  stdio:["ignore","ignore","pipe"]
 });
 let error="";
 proc.stderr.on("data",chunk=>error+=chunk.toString());
 const exit=await Promise.race([
  new Promise(resolve=>proc.on("exit",resolve)),
  new Promise(resolve=>setTimeout(()=>resolve("TIMEOUT"),2500))
 ]);
 if(exit==="TIMEOUT")proc.kill("SIGTERM");
 assert.notEqual(exit,"TIMEOUT");
 assert.notEqual(exit,0);
 assert.match(error,/MCP_RESEARCH_ACCESS_FORBIDDEN/);
 // Auth0 user identity is separate from Google Drive authorization:
 // two valid research users can call the SAME generic MCP safely.
 const auth0=auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:"https://example-fixture.us.auth0.com/",
  MEU_ARTIGO_AUTH_RESOURCE:"https://mcp.allflux.com.br/mcp",
  MEU_ARTIGO_MCP_MULTIUSER:"YES"
 });
 const pair=await generateKeyPair("RS256");
 const jwk={...await exportJWK(pair.publicKey),kid:"fixture-1",use:"sig",alg:"RS256"};
 const server=createHttpServer((req,res)=>{
  res.setHeader("content-type","application/json");
  res.end(JSON.stringify({keys:[jwk]}));
 });
 await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
 dispose.push(async()=>new Promise(resolve=>server.close(resolve)));
 const verify=createAuth0Verifier(auth0,{
  jwksUrl:"http://127.0.0.1:"+server.address().port+"/jwks"
 });
 async function jwt(subject,scope="mcp:read"){
  return "Bearer "+await new SignJWT({scope})
   .setProtectedHeader({alg:"RS256",kid:"fixture-1"})
   .setIssuer(auth0.issuer).setAudience(auth0.resource)
   .setSubject(subject).setIssuedAt().setExpirationTime("5m").sign(pair.privateKey);
 }
 for(const sub of ["google-oauth2|synthetic-user-A","google-oauth2|synthetic-user-B"]){
  const result=await verify(await jwt(sub));
  assert.equal(result.ok,true);
  assert.equal(result.principal.sub,sub);
 }
 assert.equal((await verify(await jwt("client@clients"))).status,403);
 assert.equal((await verify(await jwt("google-oauth2|synthetic-user-A","wrong"))).status,403);
 assert.throws(()=>auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:auth0.issuer,
  MEU_ARTIGO_AUTH_RESOURCE:auth0.resource,
  MEU_ARTIGO_MCP_MULTIUSER:"YES",
  MEU_ARTIGO_PILOT_SUB:"google-oauth2|synthetic-user-A"
 }),/must not be used/);
 const source=await readFile(path.resolve("server.mjs"),"utf8");
 for(const forbidden of [
  "google_user_drive.mjs","tenant_registry.mjs","build_research_site.py",
  "execFile(","googleapis.com/drive","google_oauth",
  "CANONICAL_LOCAL_SNAPSHOT"
 ])assert.ok(!source.includes(forbidden),"MCP must not include "+forbidden);
 console.log("HOST_SIDE_DRIVE_BOUNDARY_PASS: no research files, no Google tokens, no stored projects, two independent Auth0 users, generic UI only.");
}finally{
 for(const close of dispose.reverse())await close().catch(()=>{});
 await rm(root,{recursive:true,force:true});
}
