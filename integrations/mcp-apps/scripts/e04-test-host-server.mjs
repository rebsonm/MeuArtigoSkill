/** E04 ONLY: loopback MCP server for an isolated, fixture-only browser run.
 * NEVER deploy this file. No Auth0 bypass is enabled in server.mjs.
 * The official basic-host requires an unauthenticated local MCP endpoint;
 * this ephemeral process uses the exact createServer() tool/resource handlers.
 */
import {createServer} from "../server.mjs";
import {createServer as createHttpServer} from "node:http";
import {StreamableHTTPServerTransport} from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const HOST="127.0.0.1";
const PORT=18871;
const ORIGIN="http://localhost:8080";
const MAX_BYTES=256*1024;
if(process.env.CI!=="true"||process.env.MEU_ARTIGO_E04_SYNTHETIC_ONLY!=="YES"){
 console.error("E04_CI_ONLY_REFUSAL");
 process.exit(2);
}
const app=createHttpServer(async(req,res)=>{
 const path=req.url?.split("?")[0];
 if(path==="/e04-ready"&&req.method==="GET"){
  res.writeHead(200,{"content-type":"text/plain","cache-control":"no-store"}).end("READY");
  return;
 }
 if(path!=="/mcp"){res.writeHead(404).end();return;}
 if(req.headers.origin&&req.headers.origin!==ORIGIN){res.writeHead(403).end();return;}
 // CORS for this single local reference-host origin, no wildcard or credentials.
 res.setHeader("access-control-allow-origin",ORIGIN);
 res.setHeader("access-control-allow-methods","GET, POST, DELETE, OPTIONS");
 res.setHeader("access-control-allow-headers","content-type, accept, mcp-protocol-version, mcp-session-id, last-event-id");
 res.setHeader("access-control-expose-headers","mcp-session-id");
 res.setHeader("vary","Origin");
 res.setHeader("cache-control","no-store");
 if(req.method==="OPTIONS"){res.writeHead(204).end();return;}
 if(!["GET","POST","DELETE"].includes(req.method)){res.writeHead(405).end();return;}
 let body;
 if(req.method==="POST"){
  if(!/^application\/json(?:\s*;[^\r\n]*)?$/i.test(String(req.headers["content-type"]||""))){
   res.writeHead(415).end();return;
  }
  try{
   let size=0;const chunks=[];
   for await(const chunk of req){
    size+=chunk.length;
    if(size>MAX_BYTES){res.writeHead(413).end();return;}
    chunks.push(chunk);
   }
   body=JSON.parse(Buffer.concat(chunks).toString("utf8"));
  }catch{if(!res.headersSent)res.writeHead(400).end();return;}
 }
 const server=createServer();
 const transport=new StreamableHTTPServerTransport({sessionIdGenerator:undefined,enableJsonResponse:true});
 res.on("close",()=>{
  transport.close().catch(()=>{});
  server.close().catch(()=>{});
 });
 try{
  await server.connect(transport);
  await transport.handleRequest(req,res,body);
 }catch{
  if(!res.headersSent)res.writeHead(500).end("E04_MCP_FAILURE");
 }
});
app.listen(PORT,HOST,()=>console.error("E04_LOOPBACK_MCP_READY"));
