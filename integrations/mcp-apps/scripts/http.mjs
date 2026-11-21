/** Local-only HTTP protocol acceptance and authentication, no real researcher data. */
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
const port=18853;
const token="SYNTHETIC_TEST_TOKEN_NOT_FOR_PRODUCTION_123456";
const base="http://127.0.0.1:"+port+"/mcp";
const env={...process.env,MEU_ARTIGO_MCP_PORT:String(port),MEU_ARTIGO_BIND_HOST:"127.0.0.1",
 MEU_ARTIGO_MCP_BEARER:token,MEU_ARTIGO_PROJECT_ROOT:""};
const child=spawn(process.execPath,["server.mjs","--http"],{env,stdio:["ignore","ignore","pipe"]});
let client;
try{
 let ready=false;
 for(let i=0;i<60;i++){
   if(child.exitCode!==null)throw Error("Local server exited before ready");
   try{
     const r=await fetch(base,{method:"POST",headers:{"content-type":"application/json"},body:"{}"});
     if(r.status===401){ready=true;break;}
   }catch{}
   await new Promise(r=>setTimeout(r,100));
 }
 assert.ok(ready,"Unconfigured MCP HTTP must not be publicly readable");
 const unauthorized=await fetch(base,{method:"POST",headers:{"content-type":"application/json"},body:"{}"});
 assert.equal(unauthorized.status,401);
 const badOrigin=await fetch(base,{method:"POST",
  headers:{"content-type":"application/json","authorization":"Bearer "+token,"origin":"https://untrusted.example"},
  body:"{}"});
 assert.equal(badOrigin.status,403);
 client=new Client({name:"mcp-local-http-test",version:"0.1.0"});
 await client.connect(new StreamableHTTPClientTransport(new URL(base),{
  requestInit:{headers:{"Authorization":"Bearer "+token}}
 }));
 const tools=await client.listTools();
 assert.ok(tools.tools.find(x=>x.name==="meu_artigo_painel"));
 const result=await client.callTool({name:"meu_artigo_painel",arguments:{locale:"en"}});
 assert.equal(result.isError,true);
 assert.match(result.content[0].text,/Continue in chat/);
 const resource=await client.readResource({uri:"ui://meu-artigo/site-v1.html"});
 assert.equal(resource.contents[0].mimeType,"text/html;profile=mcp-app");
 console.log("MCP HTTP local authentication, origin guard, tool/text fallback and UI resource passed.");
}finally{
 await client?.close();
 child.kill("SIGTERM");
}
