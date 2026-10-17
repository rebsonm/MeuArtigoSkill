/** Synthetic delegated Google Drive: no Google network or real credentials. */
import assert from "node:assert/strict";
import {mkdtemp,mkdir,readFile,readdir,chmod,symlink,rm} from "node:fs/promises";
import {randomBytes} from "node:crypto";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import path from "node:path";
import os from "node:os";
import {openUserGoogleDrive,DRIVE_SCOPE} from "../google_user_drive.mjs";
import {createServer} from "../server.mjs";

const subA="google-oauth2|11111-AAAA";
const subB="google-oauth2|22222-BBBB";
const subC="google-oauth2|33333-CCCC";
const fakeRoot=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-per-user-drive-"));
const vault=path.join(fakeRoot,"private-tokens");
const fake=async(url,options={})=>{
 const u=new URL(url),headers=options.headers||{};
 const json=(obj,status=200)=>({ok:status===200,status,async json(){return obj;}});
 if(u.hostname==="oauth2.googleapis.com"){
  const form=new URLSearchParams(options.body||"");
  if(form.get("grant_type")==="authorization_code"){
   assert.ok(form.get("code_verifier"),"PKCE is required for each grant");
   if(form.get("code")==="code-A")return json({token_type:"Bearer",
    access_token:"access-token-A-abcdefghijklmnopqrstuvwxyz",
    refresh_token:"refresh-token-A-abcdefghijklmnopqrstuv",
    scope:"openid "+DRIVE_SCOPE});
   if(form.get("code")==="code-B")return json({token_type:"Bearer",
    access_token:"access-token-B-abcdefghijklmnopqrstuvwxyz",
    refresh_token:"refresh-token-B-abcdefghijklmnopqrstuv",
    scope:"openid "+DRIVE_SCOPE});
   if(form.get("code")==="code-bad")return json({token_type:"Bearer",
    access_token:"access-token-B-abcdefghijklmnopqrstuvwxyz",
    refresh_token:"refresh-token-B-abcdefghijklmnopqrstuv",
    scope:"openid "+DRIVE_SCOPE});
  }
  if(form.get("grant_type")==="refresh_token"){
   if(form.get("refresh_token")?.includes("-A-"))
    return json({access_token:"access-token-A-abcdefghijklmnopqrstuvwxyz"});
   if(form.get("refresh_token")?.includes("-B-"))
    return json({access_token:"access-token-B-abcdefghijklmnopqrstuvwxyz"});
  }
 }
 if(u.hostname==="openidconnect.googleapis.com"){
  if(headers.authorization?.includes("access-token-A-"))return json({sub:"11111-AAAA"});
  if(headers.authorization?.includes("access-token-B-"))return json({sub:"22222-BBBB"});
 }
 if(u.hostname==="www.googleapis.com"){
  const who=headers.authorization?.includes("access-token-A-")?"A":
    headers.authorization?.includes("access-token-B-")?"B":null;
  assert.ok(who,"No default or global Drive bearer is allowed");
  const root="root-"+who,container="folder-"+who;
  if(u.pathname.endsWith("/root"))return json({id:root,mimeType:"application/vnd.google-apps.folder"});
  if(u.pathname.endsWith("/files")){
   const q=u.searchParams.get("q")||"";
   if(q.includes("'"+root+"' in parents"))return json({files:[{id:container,
     name:"Meu Artigo",mimeType:"application/vnd.google-apps.folder",parents:[root]}]});
   if(q.includes("'"+container+"' in parents"))return json({files:[{id:"paper-"+who,
     name:"ARTIGO_"+who+"_2026",mimeType:"application/vnd.google-apps.folder",parents:[container]}]});
  }
 }
 return json({error:"fake endpoint rejected"},401);
};
const env={
 MEU_ARTIGO_GOOGLE_DRIVE_MODE:"per_user",
 MEU_ARTIGO_GOOGLE_CLIENT_ID:"synthetic-client-id",
 MEU_ARTIGO_GOOGLE_CLIENT_SECRET:"synthetic-client-secret",
 MEU_ARTIGO_GOOGLE_REDIRECT_URI:"https://mcp.allflux.com.br/google/oauth/callback",
 MEU_ARTIGO_GOOGLE_TOKEN_DIR:vault,
 MEU_ARTIGO_GOOGLE_TOKEN_KEY:randomBytes(32).toString("base64url")
};
const closer=[];
try{
 await mkdir(vault,{recursive:true,mode:0o700});
 await chmod(vault,0o700);
 const store=await openUserGoogleDrive(env,{fetchImpl:fake});
 assert.deepEqual(await store.status(subA),{connected:false});
 assert.deepEqual(await store.status(subB),{connected:false});
 assert.throws(()=>store.begin("github|unrelated-user"),/GOOGLE_IDENTITY_REQUIRED/);
 const startA=store.begin(subA);
 const startB=store.begin(subB);
 let urlA=new URL(startA.authorization_url),urlB=new URL(startB.authorization_url);
 assert.equal(urlA.hostname,"accounts.google.com");
 assert.equal(urlA.searchParams.get("access_type"),"offline");
 assert.equal(urlA.searchParams.get("code_challenge_method"),"S256");
 assert.equal(urlA.searchParams.get("redirect_uri"),env.MEU_ARTIGO_GOOGLE_REDIRECT_URI);
 assert.notEqual(urlA.searchParams.get("state"),urlB.searchParams.get("state"));
 assert.ok(urlA.searchParams.get("scope").includes(DRIVE_SCOPE));
 const complete=async(u,code)=>store.complete("/google/oauth/callback?state="+
  encodeURIComponent(u.searchParams.get("state"))+"&code="+encodeURIComponent(code));
 assert.deepEqual(await complete(urlA,"code-A"),{connected:true});
 await assert.rejects(()=>complete(urlA,"code-A"),/CALLBACK_EXPIRED/);
 assert.deepEqual(await complete(urlB,"code-B"),{connected:true});
 assert.equal((await store.status(subA)).connected,true);
 assert.equal((await store.status(subB)).connected,true);
 assert.equal((await store.status(subC)).connected,false);
 const files=await readdir(vault);
 assert.equal(files.length,2);
 for(const file of files){
  const raw=await readFile(path.join(vault,file),"utf8");
  assert.ok(!raw.includes("refresh-token-"),"Stored grant must be encrypted");
  assert.ok(!raw.includes("11111-AAAA")&&!raw.includes("22222-BBBB"));
 }
 const [a,b]=await Promise.all([store.projects(subA),store.projects(subB)]);
 assert.equal(a.projects.length,1);assert.equal(b.projects.length,1);
 assert.equal(a.projects[0].name,"ARTIGO_A_2026");
 assert.equal(b.projects[0].name,"ARTIGO_B_2026");
 assert.notEqual(a.projects[0].id,b.projects[0].id);
 await assert.rejects(()=>store.projects(subC),/GOOGLE_USER_NOT_CONNECTED/);
 // Real MCP tool registration must be bound to one authenticated sub per request.
 async function mcp(sub){
  const server=createServer({googleDrive:{
   begin:()=>store.begin(sub),status:()=>store.status(sub),
   projects:()=>store.projects(sub),disconnect:()=>store.disconnect(sub)
  }});
  const client=new Client({name:"fake-google-mcp-"+sub,version:"0.1.0"});
  const [x,y]=InMemoryTransport.createLinkedPair();
  await server.connect(x);await client.connect(y);
  closer.push(async()=>{await client.close();await server.close();});
  return client;
 }
 const [clientA,clientB]=await Promise.all([mcp(subA),mcp(subB)]);
 const ownA=await clientA.callTool({name:"meu_artigo_google_projetos",arguments:{}});
 const ownB=await clientB.callTool({name:"meu_artigo_google_projetos",arguments:{}});
 assert.equal(ownA.structuredContent.projects[0].name,"ARTIGO_A_2026");
 assert.equal(ownB.structuredContent.projects[0].name,"ARTIGO_B_2026");
 assert.equal(JSON.stringify(ownA).includes("ARTIGO_B_2026"),false);
 assert.equal(JSON.stringify(ownB).includes("ARTIGO_A_2026"),false);
 const panel=await clientA.callTool({name:"meu_artigo_painel",arguments:{}});
 assert.equal(panel.isError,true,"Google-only mode must not fall back to local files");
 assert.equal(panel.structuredContent,undefined);
 const bad=store.begin(subA);
 await assert.rejects(()=>complete(new URL(bad.authorization_url),"code-bad"),/GOOGLE_ACCOUNT_MISMATCH/);
 assert.equal((await store.projects(subA)).projects[0].name,"ARTIGO_A_2026");
 await assert.rejects(()=>store.complete("/google/oauth/callback?state=invalid&code=code-A"),/CALLBACK_EXPIRED/);
 assert.deepEqual(await store.disconnect(subA),{connected:false});
 assert.equal((await store.status(subB)).connected,true,"Disconnect A cannot remove B's link");
 assert.equal((await store.status(subA)).connected,false);
 await assert.rejects(()=>store.projects(subA),/GOOGLE_USER_NOT_CONNECTED/);
 const link=path.join(fakeRoot,"linked-tokens");
 await symlink(vault,link);
 await assert.rejects(()=>openUserGoogleDrive({...env,MEU_ARTIGO_GOOGLE_TOKEN_DIR:link},{fetchImpl:fake}),
  /PRIVATE_PATH_INVALID/);
 await chmod(vault,0o755);
 await assert.rejects(()=>openUserGoogleDrive(env,{fetchImpl:fake}),/PRIVATE_PATH_PERMISSIONS/);
 await chmod(vault,0o700);
 console.log("GOOGLE_DELEGATED_ISOLATION_PASS: 2 OAuth users; 2 separate encrypted grants; identity checked on consent and refresh; no cross-drive reads; disconnection scoped; no local fallback; unsafe vault rejected.");
}finally{
 for(const fn of closer.reverse())await fn().catch(()=>{});
 await rm(fakeRoot,{recursive:true,force:true});
}
