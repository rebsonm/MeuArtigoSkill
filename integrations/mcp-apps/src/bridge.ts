/* The UI uses the official MCP Apps client bridge (standards-first).
 * No OpenAI-specific global is required; ChatGPT may add optional features.
 */
import { App } from "@modelcontextprotocol/ext-apps";

type SiteData = { schema?: string; kind?: string; locale?: string };
declare global {
  interface Window {
    MeuArtigoHost?: {
      receive: (data: SiteData) => boolean;
      locale: (locale: string) => void;
    };
  }
}
const app = new App({ name: "Meu Artigo", version: "0.1.0" });
const fail = () => {
  const notice = document.querySelector(".mock-badge");
  if (notice) notice.textContent = "NOT CONNECTED · CONTINUE IN CHAT";
};
app.ontoolresult = (event: any) => {
  const snapshot = event?.structuredContent?.site;
  if (!snapshot || snapshot.schema !== "MEU_ARTIGO_SITE_V1" ||
      snapshot.kind !== "CANONICAL_LOCAL_SNAPSHOT" ||
      !window.MeuArtigoHost?.receive(snapshot)) {
    fail();
  }
};
app.onhostcontextchanged = (context: any) => {
  if (context?.locale) window.MeuArtigoHost?.locale(context.locale);
};
app.connect().then(() => {
  const context: any = app.getHostContext?.();
  if (context?.locale) window.MeuArtigoHost?.locale(context.locale);
}).catch(() => fail());
