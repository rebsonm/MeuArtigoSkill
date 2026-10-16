/** Optional, isolated, read-only MCP Apps server for the user-approved
 * Meu Artigo blue website. Requires a separately deployed authorized MCP
 * service to appear in ChatGPT. This is not an automatically installed Skill.
 */
import { registerAppResource, registerAppTool, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { createServer as createHttpServer } from "node:http";
import { timingSafeEqual } from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { readFile, stat, realpath } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";

const execute=promisify(execFile);
const dirname=path.dirname(fileURLToPath(import.meta.url));
const ROOT=path.resolve(dirname,"../..");
const URI="ui://meu-artigo/site-v1.html";
const LOCALES=new Set(["pt","en","es","fr"]);
const MAX_REQUEST_BYTES=256*1024;
const MAX_SITE_BYTES=256*1024;
const MAX_RESOURCE_BYTES=2*1024*1024;
const SAFE_CODE=/^[A-Z][A-Z0-9_:-]{0,127}$/;
const projectRoot=process.env.MEU_ARTIGO_PROJECT_ROOT||"";

const language=(tag="auto")=>{
 const base=String(tag).split("-")[0].toLowerCase();
 return tag==="auto"?"auto":LOCALES.has(base)?base:"en";
};
const fallback=(locale,msg)=>{
 const base=language(locale);
 const text={
  noProject:{pt:"Painel não carregado: não há projeto local autorizado configurado. Continue a pesquisa no chat.",en:"Dashboard unavailable: no authorized local project is configured. Continue in chat.",es:"Panel no disponible: falta un proyecto local autorizado. Continúe en el chat.",fr:"Tableau indisponible : aucun projet local autorisé. Continuez dans la conversation."},
  failed:{pt:"Não foi possível consultar os registros autorizados. Nenhuma alteração foi realizada; continue no chat.",en:"Authorized records could not be loaded. Nothing was changed; continue in chat.",es:"No se pudieron cargar los registros autorizados. No se modificó nada; continúe en el chat.",fr:"Impossible de charger les dossiers autorisés. Rien n'a changé ; continuez dans la conversation."}
 };
 return text[msg][base==="auto"?"en":base]??text[msg].en;
};
async function readSite({locale="auto",mode="MINIMAL"}={}){
 const selected=projectRoot;
 if(!selected||!path.isAbsolute(selected))return {error:"noProject",locale};
 // Model-provided args cannot select filesystem paths. The trusted operator
 // chooses a SINGLE authorized root outside model/tool input.
 try{
  // A symlink anywhere in the configured path can switch the project
  // between operators. Deny such roots instead of following them.
  const resolved=await realpath(selected);
  if(resolved!==path.resolve(selected))return {error:"failed",locale};
  const info=await stat(resolved);
  if(!info.isDirectory())return {error:"noProject",locale};
  const {stdout}=await execute(process.env.MEU_ARTIGO_PYTHON||"python3",
   [path.join(ROOT,"scripts/build_research_site.py"),
    "--project",selected,"--json-only","--mode",mode,"--language",language(locale)],{
      timeout:15000,maxBuffer:MAX_SITE_BYTES,env:{
        PATH:process.env.PATH||"/usr/bin:/bin",
        LANG:"C.UTF-8",LC_ALL:"C.UTF-8",
        PYTHONIOENCODING:"utf-8",PYTHONDONTWRITEBYTECODE:"1",
      },
    });
  if(Buffer.byteLength(stdout,"utf8")>MAX_SITE_BYTES)
    throw Error("Oversized projection");
  const site=JSON.parse(stdout);
  if(site.schema!=="MEU_ARTIGO_SITE_V1"||
     site.kind!=="CANONICAL_LOCAL_SNAPSHOT"||
     site.canonical_writes_allowed!==false||
     site.automatic_scientific_approval!==false||
     site.canonical_drive_sync_verified!==false||
     !Array.isArray(site.tasks)||!Array.isArray(site.gates)||
     site.tasks.length>10000||site.gates.length>7||
     !site.next_action||typeof site.next_action!=="object"||
     !SAFE_CODE.test(String(site.next_action.code||""))||
     !site.tasks.every(t=>t&&typeof t==="object"&&
       ["id","task","execution_owner","deadline"].every(k=>
         t[k]==null||(typeof t[k]==="string"&&t[k].length<=2000)))||
     !site.gates.every(g=>g&&typeof g==="object"&&
       typeof g.approval_documented==="boolean"))
    throw Error("Untrusted snapshot");
  return {site,locale};
 }catch{return {error:"failed",locale};}
}
function summary(site,locale){
 const count=site.tasks.length;
 const approvals=site.gates.filter(g=>g.approval_documented===true).length;
 const code=SAFE_CODE.test(String(site.next_action?.code||""))?site.next_action.code:"UNVERIFIED";
 const base=language(locale);
 if(base==="pt")return "Meu Artigo — leitura local: "+count+" tarefas registradas; "+approvals+" gates com aprovação documentada. Próxima ação registrada: "+code+". Drive não verificado; nenhum gate aprovado pelo painel.";
 if(base==="es")return "Meu Artigo — lectura local: "+count+" tareas registradas; "+approvals+" validaciones documentadas. Próxima acción: "+code+". Drive no verificado; sin aprobaciones automáticas.";
 if(base==="fr")return "Meu Artigo — vue locale : "+count+" tâches enregistrées ; "+approvals+" validations documentées. Prochaine action : "+code+". Drive non vérifié ; aucune approbation automatique.";
 return "Meu Artigo — authorized local read: "+count+" recorded tasks; "+approvals+" documented gate approvals. Recorded next action: "+code+". Drive not verified; no automatic scientific approvals.";
}
async function htmlResource(){
 const template=await readFile(path.join(ROOT,"assets/research_site.html"),"utf8");
 const marker="__MEU_ARTIGO_SITE_MODEL_JSON__";
 if(template.split(marker).length!==2)throw Error("Unreviewed UI template");
 const neutral=JSON.stringify({schema:"MEU_ARTIGO_SITE_V1",kind:"HOST_NOT_CONNECTED",locale:"auto"});
 const compiled=await readFile(path.join(dirname,"dist/bridge.js"),"utf8");
 if(compiled.includes("</script>"))throw Error("Unsafe bundle");
 if(!template.endsWith("</body></html>"))throw Error("Unreviewed HTML footer");
 const result=template.replace(marker,neutral).replace(
  "</body></html>","<script>"+compiled+"</script></body></html>");
 if(Buffer.byteLength(result,"utf8")>MAX_RESOURCE_BYTES)
   throw Error("MCP Apps resource exceeds bounded size");
 return result;
}
export function createServer(){
 const server=new McpServer({name:"Meu Artigo Research Panel",version:"0.1.0"});
 registerAppTool(server,"meu_artigo_painel",{
  title:"Meu Artigo — research dashboard (read only)",
  description:"Read-only authorized local C.A.D.A. and scientific-gate overview. It always supplies text if the host cannot render MCP Apps. Never creates projects, approves gates or claims Drive sync.",
  inputSchema:{locale:z.string().max(35).optional(),mode:z.enum(["MINIMAL","FULL"]).optional()},
  annotations:{readOnlyHint:true,idempotentHint:true,openWorldHint:false},
  _meta:{ui:{resourceUri:URI},"openai/outputTemplate":URI}
 },async(args)=>{
  const response=await readSite(args);
  if(response.error)return {isError:true,content:[{type:"text",text:fallback(response.locale,response.error)}]};
  return {content:[{type:"text",text:summary(response.site,response.locale)}],
   structuredContent:{site:response.site}};
 });
 registerAppResource(server,"Meu Artigo approved blue dashboard",URI,{},async()=>({
  contents:[{uri:URI,mimeType:RESOURCE_MIME_TYPE,text:await htmlResource(),
   _meta:{ui:{prefersBorder:true,csp:{connectDomains:[],resourceDomains:[]}},
      "openai/ui":{availableDisplayModes:["inline","fullscreen"]}}}]
 }));
 return server;
}
function fixedTokenEqual(expected, actual){
 const a=Buffer.from(expected),b=Buffer.from(actual);
 return a.length===b.length&&timingSafeEqual(a,b);
}
async function startHttp(){
 const bind=process.env.MEU_ARTIGO_BIND_HOST||"127.0.0.1";
 const port=Number(process.env.MEU_ARTIGO_MCP_PORT||"8085");
 const token=process.env.MEU_ARTIGO_MCP_BEARER||"";
 if(!Number.isInteger(port)||port<1024||port>65535)throw Error("Invalid explicit MCP port");
 if(token.length<32)throw Error("A secret bearer of at least 32 characters is required");
 // Stage 10 must never expose a bearer-only endpoint to a public
 // interface; OAuth with resource-specific authorization belongs to Stage 11.
 if(!["127.0.0.1","::1"].includes(bind))
   throw Error("PUBLIC_HTTP_BIND_BLOCKED_UNTIL_AUTH0_OAUTH");
 const allowedOrigin=process.env.MEU_ARTIGO_ALLOWED_ORIGIN||"";
 const app=createHttpServer(async(req,res)=>{
  const path=req.url?.split("?")[0];
  if(path!=="/mcp"){res.writeHead(404).end();return;}
  const methods=new Set(["POST","GET","DELETE"]);
  if(!methods.has(req.method)){res.writeHead(405).end();return;}
  if(req.headers.origin&&(!allowedOrigin||req.headers.origin!==allowedOrigin)){
   res.writeHead(403).end();return;
  }
  const header=req.headers.authorization;
  const auth=typeof header==="string"&&header.length<=512&&
    /^Bearer [^\s]+$/i.test(header);
  const sent=auth?header.slice(7):"";
  if(!auth||!fixedTokenEqual(token,sent)){
   res.writeHead(401,{"content-type":"application/json"}).end('{"error":"Unauthorized"}');return;
  }
  // Prevent unbounded JSON-RPC POST buffering inside transport handlers.
  // The SDK accepts an already parsed body as handleRequest's third arg.
  let parsed;
  if(req.method==="POST"){
    if(!/^application\/json(?:\s*;[^\r\n]*)?$/i.test(
       String(req.headers["content-type"]||""))){
      res.writeHead(415,{"content-type":"application/json"}).end('{"error":"Unsupported media type"}');return;
    }
    const length=Number(req.headers["content-length"]||"0");
    if(!Number.isSafeInteger(length)||length<0||length>MAX_REQUEST_BYTES){
      res.writeHead(413,{"content-type":"application/json"}).end('{"error":"Payload too large"}');return;
    }
    try{
      const chunks=[];let used=0;
      for await(const chunk of req){
        used+=chunk.length;
        if(used>MAX_REQUEST_BYTES){
          res.writeHead(413,{"content-type":"application/json"}).end('{"error":"Payload too large"}');return;
        }
        chunks.push(chunk);
      }
      parsed=JSON.parse(Buffer.concat(chunks).toString("utf8"));
      if(!parsed||typeof parsed!=="object"||Array.isArray(parsed)){
        res.writeHead(400,{"content-type":"application/json"}).end('{"error":"Invalid JSON-RPC payload"}');return;
      }
    }catch{
      if(!res.headersSent)res.writeHead(400,{"content-type":"application/json"}).end('{"error":"Invalid JSON payload"}');
      return;
    }
  }
  const mcp=createServer();
  const transport=new StreamableHTTPServerTransport({
    sessionIdGenerator:undefined,enableJsonResponse:true,
  });
  res.on("close",()=>{
   transport.close().catch(()=>{});
   mcp.close().catch(()=>{});
  });
  try{
   await mcp.connect(transport);
   await transport.handleRequest(req,res,parsed);
  }catch{
   if(!res.headersSent)res.writeHead(500).end('{"error":"MCP transport unavailable"}');
  }
 });
 app.listen(port,bind,()=>console.error("Meu Artigo MCP Apps listening on loopback or operator-authorized proxy boundary"));
}
if(process.argv.includes("--stdio")){
 await createServer().connect(new StdioServerTransport());
}else if(process.argv.includes("--http")){
 await startHttp();
}else{
 console.error("Choose --stdio or --http (authenticated, isolated, explicitly configured).");
 process.exitCode=2;
}
