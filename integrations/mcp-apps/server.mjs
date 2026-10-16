/** Optional, isolated, read-only MCP Apps server for the user-approved
 * Meu Artigo blue website. Requires a separately deployed authorized MCP
 * service to appear in ChatGPT. This is not an automatically installed Skill.
 */
import { registerAppResource, registerAppTool, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";

const execute=promisify(execFile);
const dirname=path.dirname(fileURLToPath(import.meta.url));
const ROOT=path.resolve(dirname,"../..");
const URI="ui://meu-artigo/site-v1.html";
const LOCALES=new Set(["pt","en","es","fr"]);
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
async function readSite({locale="auto"}={}){
 const selected=process.env.MEU_ARTIGO_PROJECT_ROOT;
 if(!selected||!path.isAbsolute(selected))return {error:"noProject",locale};
 // Model-provided args cannot select filesystem paths. The trusted operator
 // chooses a SINGLE authorized root outside model/tool input.
 try{
  const info=await stat(selected);
  if(!info.isDirectory())return {error:"noProject",locale};
  const {stdout}=await execute(process.env.MEU_ARTIGO_PYTHON||"python3",
   [path.join(ROOT,"scripts/build_research_site.py"),
    "--project",selected,"--json-only","--language",language(locale)],{
      timeout:15000,maxBuffer:2*1024*1024,env:process.env,
    });
  const site=JSON.parse(stdout);
  if(site.schema!=="MEU_ARTIGO_SITE_V1"||
     site.kind!=="CANONICAL_LOCAL_SNAPSHOT"||
     site.canonical_writes_allowed!==false||
     site.automatic_scientific_approval!==false||
     site.canonical_drive_sync_verified!==false)throw Error("Untrusted snapshot");
  return {site,locale};
 }catch{return {error:"failed",locale};}
}
function summary(site,locale){
 const count=site.tasks.length;
 const approvals=site.gates.filter(g=>g.approval_documented===true).length;
 const code=String(site.next_action?.code||"UNVERIFIED");
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
 return template.replace(marker,neutral).replace(
  "</body></html>","<script>"+compiled+"</script></body></html>");
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
if(process.argv.includes("--stdio")){
 const server=createServer();
 await server.connect(new StdioServerTransport());
}else{
 console.error("No authorized HTTP deployment configured. Start via --stdio in an MCP Apps-compatible client; hosted ChatGPT requires separately approved HTTPS deployment and authentication.");
 process.exitCode=2;
}
