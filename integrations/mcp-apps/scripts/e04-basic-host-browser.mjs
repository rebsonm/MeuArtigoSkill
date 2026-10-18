/** E04 browser acceptance, run from pinned official ext-apps checkout.
 * Uses local/CI-only MCP, no Drive or authentication credentials.
 */
import {chromium} from "@playwright/test";
import {writeFile} from "node:fs/promises";

const evidencePath="stage17-e04-browser-evidence.json";
const screenshotPath="stage17-e04-browser.png";
const fixture={
 schema:"MEU_ARTIGO_SITE_V1",active_route:"documentary",
 registered_gate_total:7,gate_view_partial:false,
 tasks:[{id:"SYN-E04-01",task:"SYNTHETIC E04 ALPHA",execution_owner:"Synthetic researcher",deadline:null}],
 gates:Array.from({length:7},(_,i)=>({id:"GATE-000"+(i+1),approval_documented:false})),
 next_action:{code:"REVIEW",explanation:"Review synthetic E04 display",responsible:"Synthetic researcher"}
};
const evidence={
 schema:"MEU_ARTIGO_E04_BROWSER_V1",
 fixture:"SYNTHETIC_ONLY",
 host:"official-ext-apps-basic-host-pinned",
 mcp_read:"UNKNOWN",iframe_created:false,app_connect:"UNKNOWN",
 visual_dashboard:false,ten_screens:false,synthetic_task:false,
 script_console_errors:[],host_events:[],app_events:[],success:false
};
const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
const page=await browser.newPage({viewport:{width:1440,height:900}});
page.on("console",msg=>{
 const msgText=msg.text();
 if(msgText.startsWith("[MEU_ARTIGO_UI]")&&evidence.app_events.length<25)
  evidence.app_events.push(msgText.slice(16,90));
 if(msgText.startsWith("[HOST]")){
  for(const keyword of ["Connected via","Reading UI resource","Sandbox proxy loaded","MCP App initialized","Sending tool call result"]){
   if(msgText.includes(keyword)&&!evidence.host_events.includes(keyword)){
    evidence.host_events.push(keyword);
   }
  }
 }
 if(msg.type()==="error"&&evidence.script_console_errors.length<8){
  // Limit to error categories: URLs, payload and stack omitted.
  evidence.script_console_errors.push(msgText.slice(0,150).replace(/https?:\/\/[^\s]+/g,"[URL]"));
 }
});
page.on("pageerror",error=>{
 if(evidence.script_console_errors.length<8)
  evidence.script_console_errors.push((error.name+": "+error.message).slice(0,150));
});
try{
 await page.goto("http://localhost:8080",{waitUntil:"domcontentloaded",timeout:30000});
 const input=page.locator("textarea").first();
 await input.waitFor({state:"visible",timeout:30000});
 // Wait for React's async ServerSelect effect; otherwise it may reset input to "{}".
 await page.waitForFunction(()=>{
  const selects=document.querySelectorAll("select");
  return selects.length>=2 && selects[1].value==="meu_artigo_painel";
 },{timeout:30000});
 await page.waitForTimeout(400);
 const json=JSON.stringify({locale:"pt",mode:"FULL",snapshot:fixture});
 await input.fill(json);
 await page.waitForTimeout(300);
 if(await input.inputValue()!==json)throw Error("E04_INPUT_RESET_BEFORE_CALL");
 evidence.input_bytes=json.length;
 const submit=page.getByRole("button",{name:"Call Tool",exact:true});
 await submit.waitFor({state:"visible",timeout:15000});
 await submit.click();
 const deadline=Date.now()+45000;
 let target=null;
 while(Date.now()<deadline){
  for(const f of page.frames()){
   try{
    if(await f.locator('nav button[data-page]').count()===10){
     target=f;break;
    }
   }catch{}
  }
  if(target)break;
  await page.waitForTimeout(500);
 }
 evidence.iframe_created=page.frames().length>=3;
 evidence.mcp_read=evidence.host_events.includes("Reading UI resource")?"OBSERVED":"UNOBSERVED";
 evidence.app_connect=evidence.host_events.includes("MCP App initialized")?"OBSERVED":"UNOBSERVED";
 evidence.visual_dashboard=Boolean(target);
 if(!target)throw Error("E04_DASHBOARD_NOT_RENDERED");
 evidence.ten_screens=(await target.locator('nav button[data-page]').count())===10;
 // Wait for tool result to reach the iframe; plain nav rendering occurs first.
 const toolDeadline=Date.now()+25000;
 while(Date.now()<toolDeadline){
  if((await target.locator(".mock-badge").innerText()).includes("DADOS DO CHATGPT"))break;
  await page.waitForTimeout(300);
 }
 evidence.badge=(await target.locator(".mock-badge").innerText()).slice(0,80);
 await target.locator('nav button[data-page="tasks"]').click();
 evidence.synthetic_task=(await target.locator("#content").innerText()).includes("SYNTHETIC E04 ALPHA");
 if(!evidence.ten_screens||!evidence.synthetic_task)
  throw Error("E04_SYNTHETIC_UI_ASSERTION_FAILED");
 // Regress the actual mouse-on-menu case: leave the pointer over the clicked
 // menu item during host iframe resizing, and require stable button geometry.
 const ids=["steps","tasks","sources","evidence","validations","methods","trace","submission","sync","overview"];
 for(const id of ids){
  const button=target.locator('nav button[data-page="'+id+'"]');
  await button.hover();
  const start=await button.boundingBox();
  const scrollStart=await page.evaluate(()=>window.scrollY);
  await button.click();
  await page.waitForTimeout(220);
  const end=await button.boundingBox();
  const scrollEnd=await page.evaluate(()=>window.scrollY);
  if(!start||!end||(await button.getAttribute("aria-current"))!=="page"||
     Math.abs(start.x-end.x)>2||Math.abs(start.y-end.y)>2||
     Math.abs(start.width-end.width)>2||Math.abs(start.height-end.height)>2){
   // Only synthetic layout metrics; no project content or private addresses.
   console.error("E04_NAV_LAYOUT_METRICS",JSON.stringify({id,start,end,scrollStart,scrollEnd}));
   throw Error("E04_NAV_HOVER_JITTER_"+id.toUpperCase());
  }
 }
 evidence.menu_hover_stable=true;
 evidence.success=true;
 console.log("E04_BASIC_HOST_BROWSER_PASS");
}catch(e){
 evidence.error_code=String(e?.message||e).slice(0,160);
 console.error("E04_BASIC_HOST_BROWSER_FAIL:",evidence.error_code);
 process.exitCode=1;
}finally{
 await page.screenshot({path:screenshotPath,fullPage:true}).catch(()=>{});
 await writeFile(evidencePath,JSON.stringify(evidence,null,2));
 await browser.close();
 console.log(JSON.stringify({
  result:evidence.success?"PASS":"FAIL",
  iframe_created:evidence.iframe_created,mcp_read:evidence.mcp_read,
  app_connect:evidence.app_connect,visual_dashboard:evidence.visual_dashboard,
  ten_screens:evidence.ten_screens,synthetic_task:evidence.synthetic_task,
  host_events:evidence.host_events,app_events:evidence.app_events,error_code:evidence.error_code||null
 }));
}
