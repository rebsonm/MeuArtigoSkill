/** User-delegated Google Drive, metadata-only. No shared/owner Google credentials.
 * Confidential refresh grants are encrypted per Auth0 Google subject.
 * Network endpoints are pinned; only tests can inject a fake fetch.
 */
import {randomBytes,createHash,createCipheriv,createDecipheriv} from "node:crypto";
import {lstat,realpath,mkdir,open,rename,unlink} from "node:fs/promises";
import {constants} from "node:fs";
import path from "node:path";

export const DRIVE_SCOPE="https://www.googleapis.com/auth/drive.metadata.readonly";
const SCOPES=["openid",DRIVE_SCOPE];
const GOOGLE_AUTH="https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_TOKEN="https://oauth2.googleapis.com/token";
const GOOGLE_USERINFO="https://openidconnect.googleapis.com/v1/userinfo";
const DRIVE_API="https://www.googleapis.com/drive/v3/files";
const FOLDER="application/vnd.google-apps.folder";
const pendingLifetime=10*60*1000;
const privatePath=async (p,type="directory")=>{
 const abs=path.resolve(p);
 if(!path.isAbsolute(p)||p!==abs||(await realpath(abs))!==abs)throw Error("PRIVATE_PATH_INVALID");
 const stat=await lstat(abs);
 if(stat.isSymbolicLink()||(type==="directory"?!stat.isDirectory():!stat.isFile()))
  throw Error("PRIVATE_PATH_INVALID");
 if(process.platform!=="win32"&&((stat.mode&0o077)!==0||
    (typeof process.getuid==="function"&&stat.uid!==process.getuid())))
  throw Error("PRIVATE_PATH_PERMISSIONS");
 return abs;
};
const googleSubject=sub=>{
 if(typeof sub!=="string")throw Error("GOOGLE_IDENTITY_REQUIRED");
 const match=/^google-oauth2\|([A-Za-z0-9_-]{5,128})$/.exec(sub);
 if(!match)throw Error("GOOGLE_IDENTITY_REQUIRED");
 return match[1];
};
const httpJson=async(fetchImpl,url,options={})=>{
 const response=await fetchImpl(url,{...options,redirect:"error",signal:AbortSignal.timeout(8000)});
 if(!response.ok)throw Error("GOOGLE_REMOTE_REJECTED");
 const body=await response.json();
 if(!body||typeof body!=="object"||Array.isArray(body))throw Error("GOOGLE_REMOTE_INVALID");
 return body;
};
const tenantKey=sub=>createHash("sha256").update(sub,"utf8").digest("hex")+".enc.json";
const exactEnv=(env,key)=>String(env[key]||"").trim();
export async function openUserGoogleDrive(env=process.env,{fetchImpl=fetch,now=()=>Date.now()}={}){
 if(env.MEU_ARTIGO_GOOGLE_DRIVE_MODE!=="per_user")
  throw Error("GOOGLE_MODE_NOT_ENABLED");
 const clientId=exactEnv(env,"MEU_ARTIGO_GOOGLE_CLIENT_ID");
 const clientSecret=exactEnv(env,"MEU_ARTIGO_GOOGLE_CLIENT_SECRET");
 const redirect=exactEnv(env,"MEU_ARTIGO_GOOGLE_REDIRECT_URI");
 const keyValue=exactEnv(env,"MEU_ARTIGO_GOOGLE_TOKEN_KEY");
 const storage=exactEnv(env,"MEU_ARTIGO_GOOGLE_TOKEN_DIR");
 if(!clientId||!clientSecret||!storage||!keyValue)throw Error("GOOGLE_CONFIG_REQUIRED");
 const parsed=new URL(redirect);
 if(parsed.href!==redirect||parsed.protocol!=="https:"||parsed.hostname!=="mcp.allflux.com.br"||
    parsed.pathname!=="/google/oauth/callback"||parsed.search||parsed.hash||parsed.username||
    parsed.password)throw Error("GOOGLE_REDIRECT_URI_UNREVIEWED");
 // Deployment needs a dedicated unprivileged account and a pre-created 0700 directory.
 await privatePath(storage);
 const key=Buffer.from(keyValue,"base64url");
 if(key.length!==32)throw Error("GOOGLE_ENCRYPTION_KEY_INVALID");
 const inFlight=new Map();
 const usedStates=new Set(); // bound memory; replay detection is implicit via removal
 const fileFor=sub=>path.join(storage,tenantKey(sub));
 async function tokenFile(sub){
  const p=fileFor(sub);
  let fd;
  try{
   fd=await open(p,constants.O_RDONLY|(constants.O_NOFOLLOW||0));
   const stat=await fd.stat();
   if(!stat.isFile()||stat.size>4096||stat.size<50||
      (process.platform!=="win32"&&((stat.mode&0o077)!==0||
        (typeof process.getuid==="function"&&stat.uid!==process.getuid()))))
    throw Error("GOOGLE_TOKEN_FILE_INVALID");
   const ciphertext=JSON.parse(await fd.readFile({encoding:"utf8"}));
   if(ciphertext.version!==1||typeof ciphertext.iv!=="string"||
      typeof ciphertext.tag!=="string"||typeof ciphertext.data!=="string")
    throw Error("GOOGLE_TOKEN_FILE_INVALID");
   const decipher=createDecipheriv("aes-256-gcm",key,Buffer.from(ciphertext.iv,"base64url"));
   decipher.setAAD(Buffer.from(sub));
   decipher.setAuthTag(Buffer.from(ciphertext.tag,"base64url"));
   const grant=JSON.parse(Buffer.concat([
     decipher.update(Buffer.from(ciphertext.data,"base64url")),decipher.final()
   ]).toString("utf8"));
   if(grant.googleSub!==googleSubject(sub)||!grant.refreshToken||
      typeof grant.refreshToken!=="string")throw Error("GOOGLE_TOKEN_SUBJECT_MISMATCH");
   return grant;
  }catch(error){
   if(error.code==="ENOENT")return null;
   throw Error("GOOGLE_PRIVATE_TOKEN_UNAVAILABLE");
  }finally{await fd?.close();}
 }
 async function persist(sub,refreshToken){
  if(typeof refreshToken!=="string"||refreshToken.length<20||refreshToken.length>4096)
   throw Error("GOOGLE_REFRESH_GRANT_INVALID");
  const payload=Buffer.from(JSON.stringify({
   googleSub:googleSubject(sub),refreshToken
  }));
  const iv=randomBytes(12);
  const cipher=createCipheriv("aes-256-gcm",key,iv);
  cipher.setAAD(Buffer.from(sub));
  const data=Buffer.concat([cipher.update(payload),cipher.final()]);
  const record=JSON.stringify({
   version:1,iv:iv.toString("base64url"),
   tag:cipher.getAuthTag().toString("base64url"),data:data.toString("base64url")
  });
  const temp=path.join(storage,".tmp-"+randomBytes(16).toString("hex"));
  let fd;
  try{
   fd=await open(temp,constants.O_WRONLY|constants.O_CREAT|constants.O_EXCL|
     (constants.O_NOFOLLOW||0),0o600);
   await fd.writeFile(record,"utf8");
   await fd.sync();
   await fd.close();fd=null;
   await rename(temp,fileFor(sub));
  }finally{await fd?.close();await unlink(temp).catch(()=>{});}
 }
 async function tokenFor(sub){
  const grant=await tokenFile(sub);
  if(!grant)throw Error("GOOGLE_USER_NOT_CONNECTED");
  const form=new URLSearchParams({client_id:clientId,client_secret:clientSecret,
    refresh_token:grant.refreshToken,grant_type:"refresh_token"});
  const response=await httpJson(fetchImpl,GOOGLE_TOKEN,{
    method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},
    body:form.toString()
  });
  if(typeof response.access_token!=="string"||response.access_token.length<20)
   throw Error("GOOGLE_ACCESS_TOKEN_INVALID");
  await checkUser(sub,response.access_token);
  return response.access_token;
 }
 async function checkUser(sub,accessToken){
  const id=await httpJson(fetchImpl,GOOGLE_USERINFO,{
    headers:{authorization:"Bearer "+accessToken}
  });
  if(id.sub!==googleSubject(sub))throw Error("GOOGLE_ACCOUNT_MISMATCH");
  return id.sub;
 }
 function begin(sub){
  googleSubject(sub);
  for(const [state,attempt] of inFlight)
   if(attempt.expires<now())inFlight.delete(state);
  if(inFlight.size>=128)throw Error("GOOGLE_PENDING_LIMIT");
  const state=randomBytes(32).toString("base64url");
  const verifier=randomBytes(32).toString("base64url");
  const challenge=createHash("sha256").update(verifier).digest("base64url");
  inFlight.set(state,{sub,verifier,expires:now()+pendingLifetime});
  const uri=new URL(GOOGLE_AUTH);
  for(const [k,v] of Object.entries({
    client_id:clientId,redirect_uri:redirect,response_type:"code",
    scope:SCOPES.join(" "),access_type:"offline",prompt:"consent",
    include_granted_scopes:"false",state,code_challenge:challenge,
    code_challenge_method:"S256"
  }))uri.searchParams.set(k,v);
  return {authorization_url:uri.href,expires_in_seconds:600};
 }
 async function complete(uri){
  const u=new URL(uri,"https://mcp.allflux.com.br");
  if(u.pathname!=="/google/oauth/callback"||
    u.searchParams.getAll("state").length!==1||
    u.searchParams.getAll("code").length>1)
   throw Error("GOOGLE_CALLBACK_INVALID");
  const state=u.searchParams.get("state")||"";
  const flow=inFlight.get(state);
  inFlight.delete(state); // Consume before any asynchronous operation.
  if(!flow||flow.expires<now()||u.searchParams.has("error"))
   throw Error("GOOGLE_CALLBACK_EXPIRED");
  const code=u.searchParams.get("code");
  if(!code||code.length>4096)throw Error("GOOGLE_CALLBACK_CODE_INVALID");
  const response=await httpJson(fetchImpl,GOOGLE_TOKEN,{
   method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},
   body:new URLSearchParams({
    client_id:clientId,client_secret:clientSecret,code,
    redirect_uri:redirect,grant_type:"authorization_code",
    code_verifier:flow.verifier
   }).toString()
  });
  if(response.token_type!=="Bearer"||typeof response.access_token!=="string"||
     response.access_token.length<20||typeof response.refresh_token!=="string"||
     response.refresh_token.length<20||typeof response.scope!=="string"||
     !SCOPES.every(x=>response.scope.split(" ").includes(x)))
   throw Error("GOOGLE_TOKEN_SCOPE_INVALID");
  await checkUser(flow.sub,response.access_token);
  await persist(flow.sub,response.refresh_token);
  return {connected:true}; // Do not echo subject, tokens or Google account metadata.
 }
 async function getPage(sub,accessToken,q,pageToken=""){
  const u=new URL(DRIVE_API);
  for(const [k,v] of Object.entries({
   corpora:"user",spaces:"drive",pageSize:"100",
   fields:"nextPageToken,incompleteSearch,files(id,name,mimeType,parents,webViewLink)",
   q
  }))u.searchParams.set(k,v);
  if(pageToken)u.searchParams.set("pageToken",pageToken);
  return httpJson(fetchImpl,u.href,{headers:{authorization:"Bearer "+accessToken}});
 }
 async function scan(sub,accessToken,q){
  let cursor="",items=[],seen=new Set();
  for(let page=0;page<10;page++){
   const json=await getPage(sub,accessToken,q,cursor);
   if(json.incompleteSearch||!Array.isArray(json.files))
    throw Error("GOOGLE_DRIVE_SCAN_INCOMPLETE");
   for(const f of json.files){
    if(!f||typeof f.id!=="string"||typeof f.name!=="string"||
      f.mimeType!==FOLDER||!Array.isArray(f.parents)||f.parents.length!==1||
      seen.has(f.id))throw Error("GOOGLE_DRIVE_METADATA_INVALID");
    seen.add(f.id);items.push(f);
    if(items.length>200)throw Error("GOOGLE_DRIVE_SCAN_LIMIT");
   }
   if(!json.nextPageToken)return items;
   if(typeof json.nextPageToken!=="string"||json.nextPageToken===cursor)
    throw Error("GOOGLE_DRIVE_CURSOR_INVALID");
   cursor=json.nextPageToken;
  }
  throw Error("GOOGLE_DRIVE_SCAN_INCOMPLETE");
 }
 async function projects(sub){
  const accessToken=await tokenFor(sub);
  const root=await httpJson(fetchImpl,DRIVE_API+"/root?fields=id,name,mimeType",{
   headers:{authorization:"Bearer "+accessToken}
  });
  if(typeof root.id!=="string"||root.mimeType!==FOLDER)
   throw Error("GOOGLE_DRIVE_ROOT_INVALID");
  const containers=await scan(sub,accessToken,
    "'"+root.id+"' in parents and name = 'Meu Artigo' and mimeType = '"+FOLDER+"' and trashed = false");
  if(containers.some(x=>x.parents[0]!==root.id)||containers.length>1)
   throw Error("GOOGLE_DRIVE_CANONICAL_AMBIGUOUS");
  if(containers.length===0)return {connected:true,container_found:false,projects:[]};
  const container=containers[0];
  const children=await scan(sub,accessToken,
    "'"+container.id+"' in parents and mimeType = '"+FOLDER+"' and trashed = false");
  if(children.some(x=>x.parents[0]!==container.id))
   throw Error("GOOGLE_DRIVE_CHILD_PARENT_INVALID");
  return {connected:true,container_found:true,
   projects:children.map(x=>({id:x.id,name:x.name}))};
 }
 async function disconnect(sub){
  googleSubject(sub);
  const p=fileFor(sub);
  try{
   const fd=await open(p,constants.O_RDONLY|(constants.O_NOFOLLOW||0));
   try{const st=await fd.stat();if(!st.isFile())throw Error("GOOGLE_TOKEN_FILE_INVALID");}
   finally{await fd.close();}
   await unlink(p);return {connected:false};
  }catch(e){if(e.code==="ENOENT")return {connected:false};
   throw Error("GOOGLE_PRIVATE_TOKEN_UNAVAILABLE");}
 }
 return Object.freeze({
  begin,complete,projects,disconnect,
  async status(sub){googleSubject(sub);return {connected:Boolean(await tokenFile(sub))};}
 });
}
