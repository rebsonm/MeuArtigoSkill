/** Private launch guard: real signature verification, synthetic accounts only. */
import assert from "node:assert/strict";
import {createServer} from "node:http";
import {generateKeyPair,exportJWK,SignJWT} from "jose";
import {auth0Configuration,createAuth0Verifier} from "../auth0.mjs";

const issuer="https://private-pilot-fixture.us.auth0.com/";
const resource="https://mcp.allflux.com.br/mcp";
const alice="google-oauth2|synthetic-alpha-0001";
const bob="google-oauth2|synthetic-bravo-0002";
const stranger="google-oauth2|synthetic-other-0003";
const base={MEU_ARTIGO_AUTH_ISSUER:issuer,MEU_ARTIGO_AUTH_RESOURCE:resource,
 MEU_ARTIGO_MCP_MULTIUSER:"YES",MEU_ARTIGO_MCP_PRIVATE_PILOT:"YES"};
const makeConfig=(subs)=>auth0Configuration({...base,MEU_ARTIGO_MCP_PILOT_SUBS:subs});
const deny=makeConfig("DENY_ALL");
assert.equal(deny.privatePilot,true);
assert.deepEqual(deny.pilotSubjects,[]);
const allowed=makeConfig(alice+","+bob);
assert.deepEqual(allowed.pilotSubjects,[alice,bob]);
for(const subjects of ["",alice+","+alice,alice+",",alice+","+bob+","+stranger,
    "not-an-auth0-sub","*","google-oauth2|foo bar"]){
  assert.throws(()=>makeConfig(subjects),/Private pilot needs/);
}
assert.throws(()=>auth0Configuration({
  ...base,MEU_ARTIGO_MCP_PRIVATE_PILOT:"OFF",MEU_ARTIGO_MCP_PILOT_SUBS:"DENY_ALL"
}),/Private pilot mode/);
assert.throws(()=>auth0Configuration({
  ...base,MEU_ARTIGO_MCP_MULTIUSER:"",MEU_ARTIGO_MCP_PILOT_SUBS:"DENY_ALL"
}),/Private pilot requires/);
assert.throws(()=>auth0Configuration({
  ...base,MEU_ARTIGO_MCP_PRIVATE_PILOT:"",
  MEU_ARTIGO_MCP_PILOT_SUBS:"DENY_ALL"
}),/Pilot subject list requires/);

const {privateKey,publicKey}=await generateKeyPair("RS256");
const jwk={...await exportJWK(publicKey),kid:"private-pilot-test",alg:"RS256",use:"sig"};
const jwks=createServer((req,res)=>{
 if(req.url!=="/jwks"){res.writeHead(404).end();return;}
 res.writeHead(200,{"content-type":"application/json"});
 res.end(JSON.stringify({keys:[jwk]}));
});
await new Promise(resolve=>jwks.listen(0,"127.0.0.1",resolve));
try {
 const jwksUrl="http://127.0.0.1:"+jwks.address().port+"/jwks";
 const token=subject=>new SignJWT({scope:"mcp:read"})
   .setProtectedHeader({alg:"RS256",kid:jwk.kid})
   .setIssuer(issuer).setAudience(resource).setSubject(subject)
   .setIssuedAt().setExpirationTime("2m").sign(privateKey);
 const verifyDenied=createAuth0Verifier(deny,{jwksUrl});
 const verifyAllowed=createAuth0Verifier(allowed,{jwksUrl});
 for(const person of [alice,bob,stranger]){
   assert.equal((await verifyDenied("Bearer "+await token(person))).status,403);
 }
 assert.equal((await verifyAllowed("Bearer "+await token(alice))).ok,true);
 assert.equal((await verifyAllowed("Bearer "+await token(bob))).ok,true);
 assert.equal((await verifyAllowed("Bearer "+await token(stranger))).status,403);
 assert.equal((await verifyAllowed(undefined)).status,401);
 console.log("PRIVATE_PILOT_FAIL_CLOSED_PASS: DENY_ALL and explicit two-subject list, RS256 fixture.");
} finally {
 await new Promise(resolve=>jwks.close(resolve));
}
