/** Stage 10: real stdio/HTTP transports with synthetic-only credentials and roots.
 * No externally networked server, authenticated project or external writes. */
import assert from "node:assert/strict";
import {spawn} from "node:child_process";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {StdioClientTransport} from "@modelcontextprotocol/sdk/client/stdio.js";
import {StreamableHTTPClientTransport} from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import {mkdtemp,mkdir,symlink,rm} from "node:fs/promises";
import path from "node:path";
import os from "node:os";

const PORT=18857, TOKEN="STAGE10_SYNTHETIC_BEARER_TOKEN_NEVER_PRODUCTION_1234";
const BASE="http://127.0.0.1:"+PORT+"/mcp";
const URI="ui://meu-artigo/site-v3.html";
const env={...process.env,MEU_ARTIGO_MCP_PORT:String(PORT),
 MEU_ARTIGO_BIND_HOST:"127.0.0.1",MEU_ARTIGO_MCP_BEARER:TOKEN,
 MEU_ARTIGO_PROJECT_ROOT:""};
const expectPublicReject=async()=>{
 const exposed=spawn(process.execPath,["server.mjs","--http"],{
  env:{...env,MEU_ARTIGO_BIND_HOST:"0.0.0.0",
   MEU_ARTIGO_MCP_PORT:"18859",MEU_ARTIGO_PROXY_TLS_CONFIRMED:"YES",
   MEU_ARTIGO_SINGLE_USER_ISOLATED:"YES"},
  stdio:["ignore","ignore","pipe"]});
 let stderr="";
 exposed.stderr.on("data",chunk=>stderr+=chunk.toString("utf8"));
 const code=await Promise.race([
  new Promise(resolve=>exposed.once("exit",resolve)),
  new Promise(resolve=>setTimeout(()=>resolve("TIMEOUT"),2500))
 ]);
 if(code==="TIMEOUT")exposed.kill("SIGTERM");
 assert.notEqual(code,"TIMEOUT","Public HTTP must never bind before OAuth");
 assert.notEqual(code,0);
 assert.match(stderr,/PUBLIC_HTTP_BIND_BLOCKED_UNTIL_AUTH0_OAUTH/);
};
await expectPublicReject();
const child=spawn(process.execPath,["server.mjs","--http"],{
 env,stdio:["ignore","ignore","pipe"]});
let client;
const authorization={"Authorization":"Bearer "+TOKEN};
const post=(body,headers={})=>fetch(BASE,{method:"POST",
 headers:{"content-type":"application/json",...authorization,...headers},
 body});
const pick=(code,data)=>assert.equal(data.status,code);
try {
 let ready=false;
 for(let n=0;n<80;n++){
  if(child.exitCode!==null)throw Error("MCP stage10 exited before ready");
  try{
   const x=await fetch(BASE,{method:"POST",headers:{"content-type":"application/json"},body:"{}"});
   if(x.status===401){ready=true;break;}
  }catch{}
  await new Promise(r=>setTimeout(r,100));
 }
 assert.ok(ready,"MCP HTTP test endpoint did not start");
 pick(404,await fetch("http://127.0.0.1:"+PORT+"/health"));
 pick(405,await fetch(BASE,{method:"OPTIONS"}));
 pick(401,await post("{}",{"Authorization":TOKEN}));
 pick(401,await post("{}",{"Authorization":"Basic "+TOKEN}));
 pick(401,await post("{}",{"Authorization":"Bearer wrong"}));
 pick(403,await post("{}",{"Origin":"https://outside.example"}));
 pick(415,await post("{}",{"content-type":"text/plain"}));
 pick(400,await post("{invalid"));
 pick(400,await post("[]"));
 const big=JSON.stringify({jsonrpc:"2.0",method:"ping",
   params:{huge:"X".repeat(260*1024)}});
 pick(413,await post(big));
 // A rejected oversized payload must not poison a later valid session.
 client=new Client({name:"meu-artigo-stage10-http",version:"0.1.0"});
 await client.connect(new StreamableHTTPClientTransport(new URL(BASE),{
  requestInit:{headers:authorization}
 }));
 const tools=await client.listTools();
 assert.deepEqual(tools.tools.map(t=>t.name),["meu_artigo_painel"]);
 const panel=tools.tools[0];
 assert.equal(panel.annotations.readOnlyHint,true);
 assert.equal(panel.annotations.idempotentHint,true);
 assert.equal(panel._meta.ui.resourceUri,URI);
 assert.equal(panel._meta["openai/outputTemplate"],URI);
 const resources=await client.listResources();
 assert.deepEqual(resources.resources.map(x=>x.uri),[URI]);
 const noProject=await client.callTool({name:"meu_artigo_painel",
   arguments:{locale:"fr"}});
 assert.equal(noProject.isError,true);
 assert.match(noProject.content[0].text,/ce MCP fournit uniquement/);
 assert.equal(noProject.structuredContent,undefined);
 const wrongArgs=await client.callTool({name:"meu_artigo_painel",
   arguments:{mode:"NOT_AN_ALLOWED_MODE"}});
 assert.equal(wrongArgs.isError,true);
 const view=await client.readResource({uri:URI});
 assert.equal(view.contents.length,1);
 assert.equal(view.contents[0].mimeType,"text/html;profile=mcp-app");
 assert.ok(Buffer.byteLength(view.contents[0].text,"utf8")<2*1024*1024);
 assert.match(view.contents[0].text,/HOST_NOT_CONNECTED/);
 assert.match(view.contents[0].text,/connect-src 'none'/);
 assert.doesNotMatch(view.contents[0].text,/__MEU_ARTIGO_SITE_MODEL_JSON__/);
 console.log("Stage10 HTTP passed: auth scheme, origin, JSON/media/body limits, one tool and resource, fallback.");
} finally {
 await client?.close();
 child.kill("SIGTERM");
}
// Any attempt to enable project access via an environment variable must
// cause startup refusal, not a silent fallback to someone else's Drive.
const root=await mkdtemp(path.join(os.tmpdir(),"meu-artigo-host-only-private-"));
try{
 const proc=spawn(process.execPath,["server.mjs","--stdio"],{
  env:{...process.env,MEU_ARTIGO_PROJECT_ROOT:root},
  stdio:["ignore","ignore","pipe"]
 });
 let stderr="";
 proc.stderr.on("data",part=>stderr+=part.toString("utf8"));
 const code=await Promise.race([
  new Promise(resolve=>proc.once("exit",resolve)),
  new Promise(resolve=>setTimeout(()=>resolve("TIMEOUT"),2500))
 ]);
 if(code==="TIMEOUT")proc.kill("SIGTERM");
 assert.notEqual(code,"TIMEOUT");
 assert.notEqual(code,0);
 assert.match(stderr,/MCP_RESEARCH_ACCESS_FORBIDDEN/);
 console.log("Stage10 stdio passed: project root forbidden, no storage or Drive access.");
}finally{
 await rm(root,{recursive:true,force:true});
}
