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
const clear=()=>{
 window.MeuArtigoHost?.disconnect();
 const n=document.querySelector(".mock-badge");
 if(n)n.textContent="AGUARDANDO DADOS DO CHATGPT";
};
function provenance(){
 const badge=document.querySelector(".mock-badge");
 if(badge)badge.textContent="DADOS DO CHATGPT · SEM GRAVAÇÃO";
 const footer=document.querySelector(".source-line");
 if(footer){
  const spans=footer.querySelectorAll("span");
  if(spans[0])spans[0].textContent="Fonte: visualização recebida do ChatGPT nesta sessão";
  if(spans[1])spans[1].textContent="MCP não consultou o Drive · Sem aprovação científica";
 }
 const header=document.querySelector(".page-top .stage");
 if(header)header.textContent="Snapshot do ChatGPT · não persistido";
}
app.ontoolresult=(event:any)=>{
 const site=event?.structuredContent?.site;
 if(!site||site.schema!=="MEU_ARTIGO_SITE_V1"||
    site.kind!=="HOST_AUTHORIZED_SNAPSHOT"||
    !window.MeuArtigoHost?.receive({...site,kind:"CANONICAL_LOCAL_SNAPSHOT"})){
  clear();return;
 }
 provenance();
};
app.onhostcontextchanged=(ctx:any)=>{
 if(ctx?.locale)window.MeuArtigoHost?.locale(ctx.locale);
};
app.connect().then(()=>{
 const ctx:any=app.getHostContext?.();
 if(ctx?.locale)window.MeuArtigoHost?.locale(ctx.locale);
}).catch(()=>clear());
