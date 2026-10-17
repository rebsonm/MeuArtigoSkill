/* Meu Artigo MCP Apps shell: never ingest researcher content or a
 * ChatGPT Google Drive connector result. Document reads stay in ChatGPT.
 * The UI resource is neutral and any unexpected data is discarded.
 */
import { App } from "@modelcontextprotocol/ext-apps";

declare global {
 interface Window {
  MeuArtigoHost?: {
   disconnect: () => void;
   locale: (value: string) => void;
  };
 }
}
const app=new App({name:"Meu Artigo",version:"0.2.0"});
const neutral=()=>{
 window.MeuArtigoHost?.disconnect();
 const notice=document.querySelector(".mock-badge");
 if(notice)notice.textContent="DRIVE ACCESS BELONGS TO CHATGPT";
};
// Deliberately discard ALL tool results, even if a host inadvertently
// passes structuredContent from a user's personal Drive connection.
app.ontoolresult=()=>neutral();
app.onhostcontextchanged=(context:any)=>{
 if(context?.locale)window.MeuArtigoHost?.locale(context.locale);
};
app.connect().then(()=>{
 const context:any=app.getHostContext?.();
 if(context?.locale)window.MeuArtigoHost?.locale(context.locale);
}).catch(()=>neutral());
