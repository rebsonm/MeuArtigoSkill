/* MCP Apps displays a request-local, bounded projection supplied by
 * the current ChatGPT session. Google Drive files remain in that user's
 * connected Drive; never persist or fetch them here.
 */
import {App} from "@modelcontextprotocol/ext-apps";
type SiteData={schema?:string;kind?:string;locale?:string};
declare global {interface Window {MeuArtigoHost?:{
 receive:(data:SiteData)=>boolean;
 disconnect:()=>void;
 locale:(value:string)=>void;
}}}
const app=new App({name:"Meu Artigo",version:"0.2.0"});
const fail=()=>{
 // Always revoke the previous request's rendering, including between users
 // or when the model fails to prepare the next snapshot.
 window.MeuArtigoHost?.disconnect();
 const notice=document.querySelector(".mock-badge");
 if(notice)notice.textContent="AGUARDANDO DADOS DO CHATGPT";
};
app.ontoolresult=(event:any)=>{
 const data=event?.structuredContent?.site;
 if(!data||data.schema!=="MEU_ARTIGO_SITE_V1"||
    data.kind!=="HOST_AUTHORIZED_SNAPSHOT"||
    !window.MeuArtigoHost?.receive(data))fail();
};
app.onhostcontextchanged=(context:any)=>{
 if(context?.locale)window.MeuArtigoHost?.locale(context.locale);
};
app.connect().then(()=>{
 const context:any=app.getHostContext?.();
 if(context?.locale)window.MeuArtigoHost?.locale(context.locale);
}).catch(()=>fail());
