/** E05 go-live CSP resource regression. Runs ONLY against local, synthetic MCP.
 * A passing metadata test is NOT evidence of effective ChatGPT host CSP.
 * Never change these tests to ignore the ChatGPT 'CSP disabled' UI signal.
 */
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {JSDOM} from "jsdom";
import {Client} from "@modelcontextprotocol/sdk/client/index.js";
import {InMemoryTransport} from "@modelcontextprotocol/sdk/inMemory.js";
import {createServer} from "../server.mjs";

const URI="ui://meu-artigo/site-v3.html";
const EXPECTED_META_POLICY="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'";
const clone=value=>structuredClone(value);

// This is only our component's DECLARED resource policy, not browser enforcement.
function assertDeclaredCsp(resource){
 assert.equal(resource.uri,URI,"Unexpected resource version");
 assert.equal(resource.mimeType,"text/html;profile=mcp-app");
 assert.equal(typeof resource.text,"string");
 const meta=resource._meta?.ui;
 assert.ok(meta&&typeof meta==="object"&&!Array.isArray(meta),"Missing UI metadata");
 const csp=meta.csp;
 assert.ok(csp&&typeof csp==="object"&&!Array.isArray(csp),"Missing CSP declaration");
 assert.deepEqual(Object.keys(csp).sort(),["connectDomains","resourceDomains"],
  "Unreviewed CSP metadata keys or frame allowlist");
 assert.deepEqual(csp.connectDomains,[],"Unexpected fetch/XHR allowlist");
 assert.deepEqual(csp.resourceDomains,[],"Unexpected external resource allowlist");
 const dom=new JSDOM(resource.text,{url:"https://synthetic.invalid/"});
 try{
  const doc=dom.window.document;
  const tags=[...doc.querySelectorAll('meta[http-equiv]')].filter(x=>
   x.getAttribute("http-equiv")?.toLowerCase()==="content-security-policy");
  assert.equal(tags.length,1,"Require exactly one CSP meta directive");
  assert.equal(tags[0].getAttribute("content"),EXPECTED_META_POLICY,
   "Resource HTML policy widened or changed without review");
  const blocked=doc.querySelector(
   "script[src],link[href],iframe,frame,object,embed,base,form[action],meta[http-equiv=refresh]");
  assert.equal(blocked,null,"Unexpected active external/embedded content");
  const scripts=[...doc.querySelectorAll("script")];
  assert.equal(scripts.length,3,"Expected JSON, page script, and bridge");
  assert.equal(scripts[0].type,"application/json");
  assert.ok(scripts.slice(1).every(x=>!x.hasAttribute("src")));
  const images=[...doc.querySelectorAll("img[src]")];
  assert.ok(images.every(x=>/^data:image\/svg\+xml;base64,[A-Za-z0-9+/=]+$/.test(x.getAttribute("src"))),
   "Unexpected image source");
  for(const style of doc.querySelectorAll("style")){
   assert.ok(!/@import\b/i.test(style.textContent),"External CSS imports forbidden");
   assert.ok(!/url\(\s*['"]?https?:/i.test(style.textContent),"External CSS URLs forbidden");
  }
 }finally{dom.window.close();}
 return {declared_csp:"PASS",host_iframe_csp:"NOT_OBSERVED",
  public_ui_unique_origin:typeof meta.domain==="string"?"REQUIRES_REAL_DOMAIN_REVIEW":"NOT_CONFIGURED",
  public_release:"HOLD"};
}
const server=createServer();
const client=new Client({name:"e05-csp-contract",version:"0.1.0"});
const [a,b]=InMemoryTransport.createLinkedPair();
try{
 await server.connect(a);await client.connect(b);
 const tools=(await client.listTools()).tools;
 const dashboard=tools.find(x=>x.name==="meu_artigo_painel");
 assert.equal(dashboard?._meta?.ui?.resourceUri,URI);
 const resource=(await client.readResource({uri:URI})).contents[0];
 const audit=assertDeclaredCsp(resource);
 const mustFail=(mutate,label)=>{
  const changed=clone(resource);mutate(changed);
  assert.throws(()=>assertDeclaredCsp(changed),undefined,label);
 };
 mustFail(x=>{delete x._meta.ui.csp;},"Missing metadata CSP");
 mustFail(x=>{x._meta.ui.csp.connectDomains.push("https://example.invalid");},"External API allowlist");
 mustFail(x=>{x._meta.ui.csp.resourceDomains.push("https://example.invalid");},"External resource allowlist");
 mustFail(x=>{x._meta.ui.csp.frameDomains=["https://example.invalid"];},"Unreviewed iframe allowlist");
 mustFail(x=>{x.text=x.text.replace(EXPECTED_META_POLICY,"default-src *");},"Widened HTML CSP");
 mustFail(x=>{x.text=x.text.replace("</body>","<iframe src='https://example.invalid'></iframe></body>");},"Nested iframe");
 mustFail(x=>{x.text=x.text.replace("</body>","<script src='https://example.invalid/a.js'></script></body>");},"Remote script");
 console.log(JSON.stringify({status:"E05_CSP_DECLARATION_GATE_PASS",
  resource_sha256:createHash("sha256").update(resource.text).digest("hex"),
  negative_regressions:7,...audit},null,2));
}finally{await client.close();await server.close();}
