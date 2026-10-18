/** Meu Artigo MCP Apps: host-owned Drive boundary.
 * No direct Google API, tokens, file reads or cross-user mutable state.
 * Only the display fields explicitly supplied for THIS call by the host are
 * validated, returned to its UI and discarded. Original files stay in Drive.
 */
import {registerAppResource,registerAppTool,RESOURCE_MIME_TYPE} from "@modelcontextprotocol/ext-apps/server";
import {McpServer} from "@modelcontextprotocol/sdk/server/mcp.js";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
import {StreamableHTTPServerTransport} from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import {createServer as createHttpServer} from "node:http";
import {timingSafeEqual} from "node:crypto";
import {readFile} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {z} from "zod";
import {auth0Configuration,protectedResourceMetadata,bearerChallenge,createAuth0Verifier} from "./auth0.mjs";
import {normalizeHostSnapshot} from "./host_projection.mjs";
import {uiOutputSchema} from "./ui_output_schema.mjs";

const HERE=path.dirname(fileURLToPath(import.meta.url));
const REPO=path.resolve(HERE,"../..");
const URI="ui://meu-artigo/site-v3.html";
const MAX_REQUEST_BYTES=256*1024;
const MAX_RESOURCE_BYTES=2*1024*1024;
const LOCALES=new Set(["pt","en","es","fr"]);
const forbiddenConfig=[
 "MEU_ARTIGO_PROJECT_ROOT","MEU_ARTIGO_MULTIUSER_REGISTRY",
 "MEU_ARTIGO_TENANT_DATA_ROOT","MEU_ARTIGO_GOOGLE_DRIVE_MODE",
 "MEU_ARTIGO_GOOGLE_TOKEN_DIR","MEU_ARTIGO_GOOGLE_TOKEN_KEY",
 "MEU_ARTIGO_GOOGLE_CLIENT_ID","MEU_ARTIGO_GOOGLE_CLIENT_SECRET",
 "MEU_ARTIGO_GOOGLE_REDIRECT_URI"
];
function noResearchAccess(env=process.env){
 if(forbiddenConfig.some(key=>String(env[key]??"").trim()))
  throw Error("MCP_RESEARCH_ACCESS_FORBIDDEN_USE_CHATGPT_DRIVE_CONNECTOR");
}
function locale(raw="auto"){
 const code=String(raw).split("-")[0].toLowerCase();
 return LOCALES.has(code)?code:"pt";
}
// E05's tunnel must accept ONLY two fixed, non-personal test fixtures.
// This is defensive staging-only enforcement, never enabled in the live pilot.
function e05SyntheticFixture(raw){
 if(!raw||typeof raw!=="object"||Array.isArray(raw))return false;
 if(Object.keys(raw).some(k=>!["schema","active_route","registered_gate_total",
    "gate_view_partial","tasks","gates","next_action"].includes(k)))return false;
 if(raw.schema!=="MEU_ARTIGO_SITE_V1"||raw.active_route!=="documentary"||
    raw.registered_gate_total!==7||raw.gate_view_partial!==false)return false;
 if(!Array.isArray(raw.tasks)||raw.tasks.length!==1)return false;
 const task=raw.tasks[0];
 if(!task||typeof task!=="object"||Array.isArray(task)||
    Object.keys(task).some(k=>!["id","task","execution_owner","deadline"].includes(k)))return false;
 const permitted=new Map([
  ["SYN-E05-A-01","SYNTHETIC E05 ALPHA"],
  ["SYN-E05-B-01","SYNTHETIC E05 BRAVO"]
 ]);
 if(permitted.get(task.id)!==task.task||
    task.execution_owner!=="Synthetic Researcher"||task.deadline!==null)return false;
 if(!Array.isArray(raw.gates)||raw.gates.length!==7)return false;
 for(let i=0;i<7;i++){
  const g=raw.gates[i];
  if(!g||typeof g!=="object"||Array.isArray(g)||Object.keys(g).length!==2||
     g.id!=="GATE-000"+(i+1)||g.approval_documented!==false)return false;
 }
 const action=raw.next_action;
 return action&&typeof action==="object"&&!Array.isArray(action)&&
  Object.keys(action).length===3&&action.code==="REVIEW"&&
  action.explanation==="SYNTHETIC E05 REVIEW"&&
  action.responsible==="Synthetic Researcher";
}
function guidance(raw){
 const message={
  pt:"Meu Artigo: o MCP fornece somente interface e orientações metodológicas genéricas. Use a conexão Google Drive individual do ChatGPT para consultar seus próprios arquivos. Nenhum projeto ou decisão científica foi carregado ou aprovado pelo MCP.",
  en:"Meu Artigo: this MCP serves only a generic interface and methodological guidance. Read your own files through your personal ChatGPT Google Drive connection. The MCP has not loaded any project or approved scientific decisions.",
  es:"Meu Artigo: este MCP solo ofrece interfaz y orientación metodológica genérica. Consulte sus archivos mediante su propia conexión Google Drive de ChatGPT. El MCP no ha cargado proyectos ni aprobado decisiones científicas.",
  fr:"Meu Artigo : ce MCP fournit uniquement une interface et des conseils méthodologiques génériques. Consultez vos propres fichiers via votre connexion Google Drive dans ChatGPT. Le MCP n'a chargé aucun projet ni validé de décision scientifique."
 };
 return message[locale(raw)];
}
async function uiResource(){
 const html=await readFile(path.join(REPO,"assets/research_site.html"),"utf8");
 const script=await readFile(path.join(HERE,"dist/bridge.js"),"utf8");
 const marker="__MEU_ARTIGO_SITE_MODEL_JSON__";
 if(html.split(marker).length!==2||!html.endsWith("</body></html>")||
    script.includes("</script>"))throw Error("UNREVIEWED_STATIC_MCP_UI");
 const state={schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"auto"};
 const result=html.replace(marker,JSON.stringify(state)).replace(
  "</body></html>",()=>"<script>"+script+"</script></body></html>");
 if(Buffer.byteLength(result,"utf8")>MAX_RESOURCE_BYTES)throw Error("UI_RESOURCE_TOO_LARGE");
 return result;
}
export function createServer(){
 noResearchAccess();
 const server=new McpServer({name:"Meu Artigo — Host-Side Research",version:"0.3.0"});
 registerAppTool(server,"meu_artigo_painel",{
  title:process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY==="YES"?"Meu Artigo E05 — synthetic visual acceptance":"Meu Artigo — current research dashboard (transient)",
  description:process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY==="YES"?
   "E05 synthetic-only visual acceptance. Use only the fixed ALPHA/BRAVO fixtures. No Drive, names, documents or real research records. No scientific approvals.":
   "Display ONLY a strictly bounded projection prepared by ChatGPT from the currently connected researcher's own Drive. Do not send PDFs, complete documents, original claims, full research manuscripts, file IDs, URLs or tokens. This MCP never accesses Drive and never persists the supplied projection.",
  inputSchema:{locale:z.string().max(35).optional(),mode:z.enum(["MINIMAL","FULL"]).optional(),
   snapshot:z.unknown().optional()},
  outputSchema:uiOutputSchema,
  annotations:{readOnlyHint:true,idempotentHint:true,openWorldHint:false},
  ...(process.env.MEU_ARTIGO_AUTH_MODE==="auth0"?{securitySchemes:[{type:"oauth2",scopes:["mcp:read"]}]}:{}),
  _meta:{ui:{resourceUri:URI},"openai/outputTemplate":URI}
 },async args=>{
  if(args.snapshot===undefined)return {
   isError:true,content:[{type:"text",text:guidance(args.locale)}]
  };
  if(process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY==="YES"&&!e05SyntheticFixture(args.snapshot))
   return {isError:true,content:[{type:"text",text:"E05_SYNTHETIC_ONLY: projection rejected. Use only approved fake ALPHA/BRAVO fixtures."}]};
  try{
   // Response exists only in the scope of this request; no cache, DB,
   // per-user registry, telemetry or persistence is permitted.
   const site=normalizeHostSnapshot(args.snapshot);
   return {content:[{type:"text",text:"Display-only snapshot received for this call. Original records remain in the user's ChatGPT-connected Drive. Scientific validation and Drive synchronization have NOT been verified by this MCP."}],
    structuredContent:{site}};
  }catch{
   // Never echo rejected private payload, source text or path into errors.
   return {isError:true,content:[{type:"text",text:"Dashboard projection rejected: invalid fields, unverified state or size. Return to ChatGPT and regenerate a minimal approved projection."}]};
  }
 });
 registerAppResource(server,"Meu Artigo neutral interface",URI,{},async()=>({
  contents:[{uri:URI,mimeType:RESOURCE_MIME_TYPE,text:await uiResource(),
   _meta:{ui:{prefersBorder:true,csp:{connectDomains:[],resourceDomains:[]}},
    // Inline first for model-initiated dashboard views. Host retains the final choice.
    "openai/ui":{preferredDisplayMode:"inline",availableDisplayModes:["inline","fullscreen"]}}}]
 }));
 return server;
}
function equalToken(expected,actual){
 const a=Buffer.from(expected),b=Buffer.from(actual);
 return a.length===b.length&&timingSafeEqual(a,b);
}
// Browser Origin is a scheme/host/port tuple, not a URL path or wildcard.
// Never allow opaque "null", insecure origins, credentials or a synthetic
// host policy to weaken the authenticated MCP interface.
export function configuredAllowedOrigin(env=process.env){
 const value=env.MEU_ARTIGO_ALLOWED_ORIGIN;
 if(value===undefined||value==="")return "";
 if(typeof value!=="string")throw Error("INVALID_ALLOWED_ORIGIN");
 let origin;
 try{origin=new URL(value);}catch{throw Error("INVALID_ALLOWED_ORIGIN");}
 if(origin.protocol!=="https:"||origin.username||origin.password||
    origin.pathname!=="/"||origin.search||origin.hash||
    origin.origin==="null"||origin.origin!==value)
  throw Error("INVALID_ALLOWED_ORIGIN");
 return value;
}
async function serveHttp(){
 noResearchAccess();
 const bind=process.env.MEU_ARTIGO_BIND_HOST||"127.0.0.1";
 const port=Number(process.env.MEU_ARTIGO_MCP_PORT||"8085");
 const mode=process.env.MEU_ARTIGO_AUTH_MODE||"bearer";
 if(!["bearer","auth0"].includes(mode))throw Error("UNSUPPORTED_AUTH_MODE");
 if(!Number.isInteger(port)||port<1024||port>65535)throw Error("INVALID_MCP_PORT");
 const token=process.env.MEU_ARTIGO_MCP_BEARER||"";
 if(mode==="bearer"&&token.length<32)throw Error("BEARER_TOO_SHORT");
 const config=mode==="auth0"?auth0Configuration():null;
 const verify=config?createAuth0Verifier(config):null;
 if(!["127.0.0.1","::1"].includes(bind))
  throw Error("PUBLIC_HTTP_BIND_BLOCKED_UNTIL_AUTH0_OAUTH");
 const allowedOrigin=configuredAllowedOrigin();
 const app=createHttpServer(async(req,res)=>{
  const pathname=req.url?.split("?")[0];
  if(config&&req.method==="GET"&&[
   "/.well-known/oauth-protected-resource",
   "/.well-known/oauth-protected-resource/mcp"
  ].includes(pathname)){
   res.writeHead(200,{"content-type":"application/json; charset=utf-8",
    "cache-control":"public, max-age=300","x-content-type-options":"nosniff"});
   res.end(JSON.stringify(protectedResourceMetadata(config)));return;
  }
  if(pathname!=="/mcp"){res.writeHead(404).end();return;}
  if(!["GET","POST","DELETE"].includes(req.method)){res.writeHead(405).end();return;}
  if(req.headers.origin&&(!allowedOrigin||req.headers.origin!==allowedOrigin)){
   res.writeHead(403).end();return;
  }
  if(config){
   const verdict=await verify(req.headers.authorization);
   if(!verdict.ok){
    const headers={"content-type":"application/json; charset=utf-8",
     "cache-control":"no-store","x-content-type-options":"nosniff"};
    if(verdict.status===401||verdict.error==="insufficient_scope")
     headers["www-authenticate"]=bearerChallenge(config,
      verdict.error==="invalid_token"?"invalid_token":
      verdict.error==="insufficient_scope"?"insufficient_scope":null);
    res.writeHead(verdict.status,headers).end(JSON.stringify({
     error:verdict.status===401?"Unauthorized":"Forbidden"
    }));return;
   }
  }else{
   const header=req.headers.authorization;
   const valid=typeof header==="string"&&header.length<=512&&
    /^Bearer [^\s]+$/i.test(header);
   if(!valid||!equalToken(token,header.slice(7))){
    res.writeHead(401,{"content-type":"application/json",
     "cache-control":"no-store"}).end('{"error":"Unauthorized"}');return;
   }
  }
  let parsed;
  if(req.method==="POST"){
   if(!/^application\/json(?:\s*;[^\r\n]*)?$/i.test(String(req.headers["content-type"]||""))){
    res.writeHead(415).end();return;
   }
   const size=Number(req.headers["content-length"]||"0");
   if(!Number.isSafeInteger(size)||size<0||size>MAX_REQUEST_BYTES){
    res.writeHead(413).end();return;
   }
   try{
    const chunks=[];let total=0;
    for await(const chunk of req){
     total+=chunk.length;
     if(total>MAX_REQUEST_BYTES){res.writeHead(413).end();return;}
     chunks.push(chunk);
    }
    parsed=JSON.parse(Buffer.concat(chunks).toString("utf8"));
    if(!parsed||typeof parsed!=="object"||Array.isArray(parsed)){
     res.writeHead(400).end();return;
    }
   }catch{
    if(!res.headersSent)res.writeHead(400).end();return;
   }
  }
  const server=createServer();
  const transport=new StreamableHTTPServerTransport({
   sessionIdGenerator:undefined,enableJsonResponse:true
  });
  res.on("close",()=>{
   transport.close().catch(()=>{});
   server.close().catch(()=>{});
  });
  try{
   await server.connect(transport);
   await transport.handleRequest(req,res,parsed);
  }catch{
   if(!res.headersSent)res.writeHead(500).end('{"error":"MCP unavailable"}');
  }
 });
 app.listen(port,bind,()=>console.error("Meu Artigo generic MCP ready on loopback"));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 if(process.argv.includes("--stdio")){
  noResearchAccess();
  await createServer().connect(new StdioServerTransport());
 }else if(process.argv.includes("--http")){
  await serveHttp();
 }else{
  console.error("Specify --stdio or --http");
  process.exitCode=2;
 }
}
