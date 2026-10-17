/** Private Auth0 subject -> project resolver. No model-supplied paths or Drive writes. */
import { lstat, realpath, readFile } from "node:fs/promises";
import path from "node:path";

const SCHEMA="MEU_ARTIGO_TENANT_REGISTRY_V1";
const SEGMENT=/^[a-z][a-z0-9-]{2,63}$/;
const SUBJECT=/^[A-Za-z0-9_-]{2,48}\|[A-Za-z0-9_.-]{5,128}$/;
function block(reason){throw Error("TENANT_REGISTRY_BLOCKED: "+reason);}
function exact(obj,keys){return obj!==null&&typeof obj==="object"&&!Array.isArray(obj)&&
 Object.keys(obj).length===keys.length&&keys.every(k=>Object.hasOwn(obj,k));}
async function protectedPath(input,label,file=false){
 if(typeof input!=="string"||!path.isAbsolute(input)||path.normalize(input)!==input)
  block("Invalid "+label);
 const canonical=path.resolve(input);
 if(await realpath(canonical)!==canonical)block("Symlink "+label);
 const stat=await lstat(canonical);
 if(stat.isSymbolicLink()||(file?!stat.isFile():!stat.isDirectory()))
  block("Wrong type "+label);
 return {canonical,stat};
}
/** Immutable read-once configuration. Registry changes require a service restart. */
export async function loadTenantRegistry(env=process.env){
 const config=env.MEU_ARTIGO_MULTIUSER_REGISTRY||"";
 const baseDir=env.MEU_ARTIGO_TENANT_DATA_ROOT||"";
 if(!config&&!baseDir)return null;
 if(!config||!baseDir)block("Both registry and data root are required");
 const base=await protectedPath(baseDir,"tenant data root");
 const file=await protectedPath(config,"registry file",true);
 if(file.stat.size===0||file.stat.size>65536)block("Invalid registry size");
 if(process.platform!=="win32"&&(file.stat.mode&0o077)!==0)
  block("Registry must be private (0600)");
 let data;
 try{data=JSON.parse(await readFile(file.canonical,"utf8"));}catch{block("Invalid JSON");}
 if(!exact(data,["schema","tenants"])||data.schema!==SCHEMA||
    !Array.isArray(data.tenants)||data.tenants.length<1||data.tenants.length>1000)
  block("Invalid schema");
 const bySubject=new Map(),tenantIds=new Set();
 for(const entry of data.tenants){
  if(!exact(entry,["subject","tenant_id","projects"])||
     typeof entry.subject!=="string"||!SUBJECT.test(entry.subject)||
     typeof entry.tenant_id!=="string"||!SEGMENT.test(entry.tenant_id)||
     !Array.isArray(entry.projects)||entry.projects.length<1||entry.projects.length>100)
   block("Invalid tenant");
  if(bySubject.has(entry.subject)||tenantIds.has(entry.tenant_id))
   block("Duplicate identity or tenant");
  tenantIds.add(entry.tenant_id);
  const home=await protectedPath(path.join(base.canonical,entry.tenant_id),"tenant home");
  if(path.dirname(home.canonical)!==base.canonical)block("Tenant out of root");
  const projects=new Map();
  for(const projectId of entry.projects){
   if(typeof projectId!=="string"||!SEGMENT.test(projectId)||projects.has(projectId))
    block("Invalid or duplicate project ID");
   const p=await protectedPath(path.join(home.canonical,projectId),"project");
   if(path.dirname(p.canonical)!==home.canonical)block("Project out of tenant");
   projects.set(projectId,p.canonical);
  }
  bySubject.set(entry.subject,projects);
 }
 return Object.freeze({
  schema:SCHEMA,
  hasSubject:sub=>bySubject.has(sub),
  listProjects:sub=>Object.freeze([...(bySubject.get(sub)?.keys()||[])]),
  projectFor(sub,projectId){
   const projects=bySubject.get(sub);
   if(!projects)return null;
   if(projectId===undefined||projectId===null)
    return projects.size===1?projects.values().next().value:null;
   if(typeof projectId!=="string"||!SEGMENT.test(projectId))return null;
   return projects.get(projectId)||null;
  }
 });
}
