/* ChatGPT reads the researcher's own Drive and calls the MCP with a
 * bounded UI projection. This bridge only displays that per-call projection.
 * No persistent cache or cross-user memory.
 */
import {App} from "@modelcontextprotocol/ext-apps";
type SiteData={schema?:string;kind?:string;locale?:string};
declare global {interface Window {MeuArtigoHost?:{
 receive:(data:SiteData)=>boolean;disconnect:()=>void;locale:(code:string)=>void;
}}}
const app=new App({name:"Meu Artigo",version:"0.3.0"});
let showingSnapshot=false;
let lastHostLocaleKey:string|null=null;
function syncHostLocale(value:unknown){
 // ChatGPT emits host-context events for resize/theme/safe-area too.
 // Only a genuine locale change may repaint the dashboard.
 if(typeof value!=="string")return;
 const key=value.trim().toLowerCase().replace(/_/g,"-").split("-")[0];
 if(!["pt","en","es","fr"].includes(key)||key===lastHostLocaleKey)return;
 lastHostLocaleKey=key;
 const rendered=(document.documentElement.lang||"").toLowerCase().split("-")[0];
 if(rendered!==key)window.MeuArtigoHost?.locale(value);
}
// Codes only, never research content, tokens or personal identifiers.
const trace=(code:string)=>console.info("[MEU_ARTIGO_UI] "+code);
const clear=()=>{
 showingSnapshot=false;
 window.MeuArtigoHost?.disconnect();
 const n=document.querySelector(".mock-badge");
 if(n)n.textContent="AGUARDANDO DADOS DO CHATGPT";
};
function provenance(){
 const badge=document.querySelector(".mock-badge");
 if(badge&&badge.textContent!=="DADOS DO CHATGPT · SEM GRAVAÇÃO")badge.textContent="DADOS DO CHATGPT · SEM GRAVAÇÃO";
 const footer=document.querySelector(".source-line");
 if(footer){
  const spans=footer.querySelectorAll("span");
  if(spans[0]&&spans[0].textContent!=="Fonte: visualização recebida do ChatGPT nesta sessão")spans[0].textContent="Fonte: visualização recebida do ChatGPT nesta sessão";
  if(spans[1]&&spans[1].textContent!=="MCP não consultou o Drive · Sem aprovação científica")spans[1].textContent="MCP não consultou o Drive · Sem aprovação científica";
 }
 const header=document.querySelector(".page-top .stage");
 if(header&&header.textContent!=="Snapshot do ChatGPT · não persistido")header.textContent="Snapshot do ChatGPT · não persistido";
 const title=document.querySelector(".page-top .page-title");
 if(title&&title.textContent==="Projeto autorizado · visão local")
  title.textContent="Painel de pesquisa · dados enviados pelo ChatGPT";
 document.querySelectorAll(".footnote").forEach((element)=>{
  if(element.textContent?.startsWith("Snapshot local autorizado"))
   element.textContent="Visualização dos registros encaminhados pelo ChatGPT; confirme os documentos originais em seu Drive.";
 });
}
// The shared HTML redraws on navigation. Keep the host-provenance notice
// correct without changing or storing any research data.
const labelObserver=new MutationObserver(()=>{if(showingSnapshot)provenance();});
labelObserver.observe(document.documentElement,{childList:true,subtree:true});
// The next invocation must never display a previous tool result while loading.
app.ontoolinput=()=>{
 trace("TOOL_INPUT_RECEIVED");
 clear();
};
app.ontoolresult=(event:any)=>{
 trace("TOOL_RESULT_RECEIVED");
 const site=event?.structuredContent?.site;
 if(!site){trace("SITE_MISSING");clear();return;}
 if(site.schema!=="MEU_ARTIGO_SITE_V1"){trace("SCHEMA_MISMATCH");clear();return;}
 if(site.kind!=="HOST_AUTHORIZED_SNAPSHOT"){trace("KIND_MISMATCH");clear();return;}
 if(!window.MeuArtigoHost?.receive({...site,kind:"CANONICAL_LOCAL_SNAPSHOT"})){
  trace("SNAPSHOT_REJECTED");clear();return;
 }
 showingSnapshot=true;
 provenance();
 trace("SNAPSHOT_SHOWN");
};
app.onhostcontextchanged=(ctx:any)=>{
 // Host context changes include resizing, theme, safe-area and locale.
 // They do not authenticate a new researcher or define a new tool invocation.
 // Clearing here erased valid results repeatedly during iframe auto-resizing.
 trace("HOST_CONTEXT_CHANGED");
 syncHostLocale(ctx?.locale);
};
app.onteardown=async()=>{
 trace("TEARDOWN");
 clear();
 return {};
};
app.connect().then(()=>{
 trace("CONNECTED");
 const ctx:any=app.getHostContext?.();
 syncHostLocale(ctx?.locale);
}).catch(()=>{trace("CONNECT_FAILED");clear();});
