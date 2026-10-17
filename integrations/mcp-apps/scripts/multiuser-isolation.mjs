/** Synthetic-only multiuser isolation and signed Auth0 subject tests.
 * Every fixture is disposable. No Drive, live OAuth or public listener.
 */
import assert from "node:assert/strict";
import {createServer as createHttpServer} from "node:http";
import {generateKeyPair,exportJWK,SignJWT} from "jose";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {mkdtemp,mkdir,writeFile,readFile,chmod,symlink,rm} from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import {createServer} from "../server.mjs";
import {loadTenantRegistry} from "../tenant_registry.mjs";
import {auth0Configuration,createAuth0Verifier} from "../auth0.mjs";

const SUBJECT_A="google-oauth2|fixture-A-12345";
const SUBJECT_B="google-oauth2|fixture-B-12345";
const SUBJECT_X="google-oauth2|intruder-12345";
const DATA_SCHEMA="MEU_ARTIGO_TENANT_REGISTRY_V1";
const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-tenants-test-"));
const dataRoot=path.join(root,"data");
const registryPath=path.join(root,"private-registry.json");
const fixture={
 schema:DATA_SCHEMA,
 tenants:[
  {subject:SUBJECT_A,tenant_id:"tenant-alpha",projects:["article-alpha","article-two"]},
  {subject:SUBJECT_B,tenant_id:"tenant-bravo",projects:["article-bravo"]}
 ]
};
const clean=[];
async function project(t,p,tag){
 const base=path.join(dataRoot,t,p,"00_Gestao_e_Continuidade");
 await mkdir(base,{recursive:true});
 await writeFile(path.join(base,"PROJECT_CONFIG.json"),JSON.stringify({
  project_name:tag,presentation_mode:"MINIMAL",method_route:"UNDECIDED",
  storage_mode:"WORK_FALLBACK",storage_state:"WORK_FALLBACK_AUTHORIZED"
 }));
 await writeFile(path.join(base,"CONTINUIDADE.md"),"Fictional trace only");
 await writeFile(path.join(base,"11_CADA_Control.csv"),
  "CADA_ID,Title,Assigned_to,Status,Deadline,Completion_evidence\n"+
  "CADA-0001,Synthetic "+tag+",Researcher,READY,,\n");
 await writeFile(path.join(base,"18_Human_Validation_Gates.csv"),
  "GATE_ID,Name,Status,Decision,Validated_by,Validation_evidence\n"+
  Array.from({length:7},(_,i)=>"GATE-"+String(i+1).padStart(4,"0")+
  ",Synthetic gate,READY,PENDING,,").join("\n")+"\n");
}
async function connected(registry,subject){
 const server=createServer({
  resolveProject:id=>registry.projectFor(subject,id),
  listProjects:()=>registry.listProjects(subject)
 });
 const client=new Client({name:"isolation-test",version:"0.1.0"});
 const [a,b]=InMemoryTransport.createLinkedPair();
 await server.connect(a);
 await client.connect(b);
 clean.push(async()=>{await client.close();await server.close();});
 return client;
}
async function expectDenied(fn){await assert.rejects(fn,/TENANT_REGISTRY_BLOCKED|ENOENT/);}
async function signedIdentityTests(config,registry){
 const keys=await generateKeyPair("RS256");
 const key=await exportJWK(keys.publicKey);key.kid="test-key";key.use="sig";key.alg="RS256";
 const web=createHttpServer((req,res)=>{
  if(req.url!=="/jwks"){res.writeHead(404).end();return;}
  res.writeHead(200,{"content-type":"application/json"});
  res.end(JSON.stringify({keys:[key]}));
 });
 await new Promise(resolve=>web.listen(0,"127.0.0.1",resolve));
 clean.push(async()=>new Promise(resolve=>web.close(resolve)));
 const jwksUrl="http://127.0.0.1:"+web.address().port+"/jwks";
 const verify=createAuth0Verifier(config,{jwksUrl});
 const signed=async(sub,scope="mcp:read",audience=config.resource)=>new SignJWT({scope})
  .setProtectedHeader({alg:"RS256",kid:"test-key"})
  .setIssuer(config.issuer).setAudience(audience).setSubject(sub)
  .setIssuedAt().setExpirationTime("5m").sign(keys.privateKey);
 const a=await verify("Bearer "+await signed(SUBJECT_A));
 const b=await verify("Bearer "+await signed(SUBJECT_B));
 assert.equal(a.ok,true);assert.equal(b.ok,true);
 assert.equal(a.principal.sub,SUBJECT_A);assert.equal(b.principal.sub,SUBJECT_B);
 assert.ok(registry.hasSubject(a.principal.sub));
 assert.ok(!registry.hasSubject(SUBJECT_X));
 assert.equal((await verify("Bearer "+await signed(SUBJECT_A,"wrong"))).status,403);
 assert.equal((await verify("Bearer "+await signed(SUBJECT_A,"mcp:read","https://wrong.example/mcp"))).status,401);
 assert.equal((await verify("Bearer invalid")).status,401);
}
try{
 await project("tenant-alpha","article-alpha","ALPHA-SECRET-FIXTURE");
 await project("tenant-alpha","article-two","SECOND-SECRET-FIXTURE");
 await project("tenant-bravo","article-bravo","BRAVO-SECRET-FIXTURE");
 await writeFile(registryPath,JSON.stringify(fixture));
 await chmod(registryPath,0o600);
 const env={MEU_ARTIGO_MULTIUSER_REGISTRY:registryPath,MEU_ARTIGO_TENANT_DATA_ROOT:dataRoot};
 const registry=await loadTenantRegistry(env);
 assert.deepEqual(registry.listProjects(SUBJECT_A),["article-alpha","article-two"]);
 assert.deepEqual(registry.listProjects(SUBJECT_B),["article-bravo"]);
 assert.deepEqual(registry.listProjects(SUBJECT_X),[]);
 assert.equal(registry.projectFor(SUBJECT_A),null,"Ambiguous projects require explicit selection");
 assert.equal(registry.projectFor(SUBJECT_A,"article-bravo"),null);
 assert.equal(registry.projectFor(SUBJECT_B,"article-alpha"),null);
 assert.equal(registry.projectFor(SUBJECT_B,"../tenant-alpha/article-alpha"),null);
 assert.equal(registry.projectFor(SUBJECT_X,"article-alpha"),null);
 const clientA=await connected(registry,SUBJECT_A);
 const clientB=await connected(registry,SUBJECT_B);
 const toolsA=await clientA.listTools();
 assert.deepEqual(toolsA.tools.map(t=>t.name).sort(),["meu_artigo_painel","meu_artigo_projetos"]);
 const ownList=await clientA.callTool({name:"meu_artigo_projetos",arguments:{}});
 assert.deepEqual(ownList.structuredContent.projects,["article-alpha","article-two"]);
 const deniedA=await clientA.callTool({name:"meu_artigo_painel",arguments:{locale:"en"}});
 assert.equal(deniedA.isError,true,"Multiple project IDs need explicit choice");
 const own=await clientA.callTool({name:"meu_artigo_painel",
  arguments:{project_id:"article-alpha",locale:"en",mode:"MINIMAL"}});
 assert.notEqual(own.isError,true);
 assert.equal(own.structuredContent.site.kind,"CANONICAL_LOCAL_SNAPSHOT");
 assert.equal(own.structuredContent.site.canonical_drive_sync_verified,false);
 assert.equal(own.structuredContent.site.automatic_scientific_approval,false);
 assert.equal(own.structuredContent.site.canonical_writes_allowed,false);
 assert.equal(own.structuredContent.site.gates.filter(g=>g.approval_documented).length,0);
 const deniedCross=await clientA.callTool({name:"meu_artigo_painel",
  arguments:{project_id:"article-bravo",locale:"en"}});
 assert.equal(deniedCross.isError,true);
 assert.ok(!JSON.stringify(deniedCross).includes("BRAVO-SECRET-FIXTURE"));
 const deniedPath=await clientA.callTool({name:"meu_artigo_painel",
  arguments:{project_id:"../../tenant-bravo/article-bravo",locale:"en"}});
 assert.equal(deniedPath.isError,true);
 const ownB=await clientB.callTool({name:"meu_artigo_painel",arguments:{locale:"en"}});
 assert.notEqual(ownB.isError,true,"Single mapped project auto-selects for its owner");
 const listB=await clientB.callTool({name:"meu_artigo_projetos",arguments:{}});
 assert.deepEqual(listB.structuredContent.projects,["article-bravo"]);
 const deniedB=await clientB.callTool({name:"meu_artigo_painel",
  arguments:{project_id:"article-alpha",locale:"en"}});
 assert.equal(deniedB.isError,true);
 const [repeatA,repeatB]=await Promise.all([
  clientA.callTool({name:"meu_artigo_painel",arguments:{project_id:"article-two",locale:"pt"}}),
  clientB.callTool({name:"meu_artigo_painel",arguments:{project_id:"article-bravo",locale:"fr"}})
 ]);
 assert.notEqual(repeatA.isError,true);assert.notEqual(repeatB.isError,true);
 assert.equal(repeatA.structuredContent.site.locale,"pt");
 assert.equal(repeatB.structuredContent.site.locale,"fr");
 await signedIdentityTests(auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:"https://fixture.us.auth0.com/",
  MEU_ARTIGO_AUTH_RESOURCE:"https://mcp.allflux.com.br/mcp",
  MEU_ARTIGO_MULTIUSER_REGISTRY:registryPath
 }),registry);
 await chmod(registryPath,0o644);
 await expectDenied(()=>loadTenantRegistry(env));
 await chmod(registryPath,0o600);
 await writeFile(registryPath,JSON.stringify({...fixture,tenants:[fixture.tenants[0],fixture.tenants[0]]}));
 await expectDenied(()=>loadTenantRegistry(env));
 await writeFile(registryPath,JSON.stringify(fixture));
 const alias=path.join(root,"symlink-registry.json");
 await symlink(registryPath,alias);
 await expectDenied(()=>loadTenantRegistry({...env,MEU_ARTIGO_MULTIUSER_REGISTRY:alias}));
 assert.throws(()=>auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:"https://fixture.us.auth0.com/",
  MEU_ARTIGO_AUTH_RESOURCE:"https://mcp.allflux.com.br/mcp",
  MEU_ARTIGO_MULTIUSER_REGISTRY:registryPath,
  MEU_ARTIGO_PILOT_SUB:SUBJECT_A
 }),/must not coexist/);
 console.log("Multiuser isolation: signed JWT subjects, separate authorized projects, cross-tenant denies, parallel calls, private registry and fail-closed configuration PASS.");
}finally{
 for(const f of clean.reverse()){try{await f();}catch{}}
 await rm(root,{recursive:true,force:true});
}
