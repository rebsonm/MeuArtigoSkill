/** Synthetic cryptographic auth acceptance, no external Google/Auth0 calls. */
import assert from "node:assert/strict";
import { createHash, randomBytes } from "node:crypto";
import { createServer } from "node:http";
import { generateKeyPair, exportJWK, SignJWT } from "jose";
import {
  auth0Configuration, protectedResourceMetadata, bearerChallenge,
  createAuth0Verifier
} from "../auth0.mjs";

const issuer="https://dev-meu-artigo-fixture.us.auth0.com/";
const resource="https://mcp.allflux.com.br/mcp";
const sub="google-oauth2|synthetic-pilot-001";
const config=auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:issuer,
  MEU_ARTIGO_AUTH_RESOURCE:resource,
  MEU_ARTIGO_PILOT_SUB:sub
});
assert.equal(config.jwksUrl,issuer+".well-known/jwks.json");
assert.deepEqual(protectedResourceMetadata(config),{
  resource,
  authorization_servers:[issuer],
  scopes_supported:["mcp:read"]
});
assert.match(bearerChallenge(config),/resource_metadata=/);
assert.throws(()=>auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:issuer,
  MEU_ARTIGO_AUTH_RESOURCE:resource,
  MEU_ARTIGO_PILOT_SUB:""
}),/allowlisted/);
assert.throws(()=>auth0Configuration({
  MEU_ARTIGO_AUTH_ISSUER:"http://dev-meu-artigo-fixture.us.auth0.com/",
  MEU_ARTIGO_AUTH_RESOURCE:resource,
  MEU_ARTIGO_PILOT_SUB:sub
}),/Invalid issuer/);

const {privateKey,publicKey}=await generateKeyPair("RS256");
const jwk={...await exportJWK(publicKey),kid:"fixture-only",alg:"RS256",use:"sig"};
const jwksServer=createServer((req,res)=>{
 if(req.url!=="/.well-known/jwks.json"){res.writeHead(404).end();return;}
 res.writeHead(200,{"content-type":"application/json"});
 res.end(JSON.stringify({keys:[jwk]}));
});
await new Promise(resolve=>jwksServer.listen(0,"127.0.0.1",resolve));
try{
 const url="http://127.0.0.1:"+jwksServer.address().port+"/.well-known/jwks.json";
 const verify=createAuth0Verifier(config,{jwksUrl:url});
 const makeToken=({subject=sub,aud=resource,iss=issuer,scope="mcp:read",
     exp=120,withExp=true,withIssuedAt=true,nbf=undefined}={})=>{
   let token=new SignJWT({scope}).setProtectedHeader({alg:"RS256",kid:jwk.kid})
    .setIssuer(iss).setAudience(aud).setSubject(subject);
   if(withIssuedAt)token=token.setIssuedAt();
   if(withExp)token=token.setExpirationTime(Math.floor(Date.now()/1000)+exp);
   if(nbf!==undefined)token=token.setNotBefore(nbf);
   return token.sign(privateKey);
 };
 const valid=await makeToken();
 assert.equal((await verify("Bearer "+valid)).ok,true);
 assert.equal((await verify(undefined)).status,401);
 assert.equal((await verify("Bearer bogus")).status,401);
 assert.equal((await verify("Bearer "+await makeToken({aud:"https://other.example/mcp"}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({iss:"https://wrong.example/"}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({exp:-120}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({scope:"openid profile email"}))).error,
  "insufficient_scope");
 assert.equal((await verify("Bearer "+await makeToken({
  subject:"google-oauth2|different-account"
 }))).error,"access_denied");
 assert.equal((await verify("Bearer "+await makeToken({
  subject:"client@clients"
 }))).status,403);
 // Fail-closed temporal and identity cases, not just expired timestamps.
 assert.equal((await verify("Bearer "+await makeToken({withExp:false}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({withIssuedAt:false}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({exp:7200}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({nbf:Math.floor(Date.now()/1000)+3600}))).status,401);
 assert.equal((await verify("Bearer "+await makeToken({scope:"mcp:write"}))).status,403);
 assert.equal((await verify("Bearer "+await makeToken({scope:"mcp:reader"}))).status,403);
 assert.equal((await verify("Bearer "+await makeToken({scope:"mcp:read mcp:write"}))).ok,true);
 assert.equal((await verify("Basic "+valid)).status,401);
 assert.equal((await verify(valid)).status,401);
 assert.equal((await verify("Bearer  "+valid)).status,401);
 assert.equal((await verify("Bearer "+valid+"\n")).status,401);
 assert.equal((await verify("Bearer "+valid.slice(0,-9)+"corrupted")).status,401);
 const attackerJwt=await new SignJWT({scope:"mcp:read"})
   .setProtectedHeader({alg:"HS256",kid:jwk.kid})
   .setIssuer(issuer).setAudience(resource).setSubject(sub)
   .setIssuedAt().setExpirationTime("2m")
   .sign(new TextEncoder().encode("synthetic-weak-secret-is-not-Auth0"));
 assert.equal((await verify("Bearer "+attackerJwt)).status,401);
 for(const invalid of ["","http://dev-meu-artigo-fixture.us.auth0.com/",
   "https://dev-meu-artigo-fixture.us.auth0.com/path/",
   "https://attacker.example/"]){
   assert.throws(()=>auth0Configuration({
      MEU_ARTIGO_AUTH_ISSUER:invalid,MEU_ARTIGO_AUTH_RESOURCE:resource,
      MEU_ARTIGO_PILOT_SUB:sub
   }));
 }
 assert.throws(()=>auth0Configuration({
   MEU_ARTIGO_AUTH_ISSUER:issuer,MEU_ARTIGO_AUTH_RESOURCE:"http://wrong.example/mcp",
   MEU_ARTIGO_PILOT_SUB:sub
 }));
 // PKCE S256 client-side simulator: a resource server does not perform
 // authorization code exchanges and cannot certify Auth0 PKCE enforcement.
 const pkceVerifier=randomBytes(48).toString("base64url");
 const challenge=createHash("sha256").update(pkceVerifier,"ascii").digest("base64url");
 assert.match(pkceVerifier,/^[A-Za-z0-9_-]{43,128}$/);
 assert.equal(challenge,createHash("sha256").update(pkceVerifier).digest("base64url"));
 assert.notEqual(challenge,createHash("sha256").update(pkceVerifier+"wrong").digest("base64url"));
 console.log("PKCE S256 simulator: challenge binding and wrong verifier divergence pass; no Auth0 token exchange performed.");
 console.log("OAuth JWT acceptance: exact issuer/audience, RS256, expiry, scope and pilot account restrictions pass.");
}finally{
 await new Promise(resolve=>jwksServer.close(resolve));
}
