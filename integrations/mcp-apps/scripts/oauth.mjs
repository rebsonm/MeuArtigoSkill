/** Synthetic cryptographic auth acceptance, no external Google/Auth0 calls. */
import assert from "node:assert/strict";
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
assert.match(bearerChallenge(config),"resource_metadata=");
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
 const makeToken=({subject=sub,aud=resource,iss=issuer,scope="mcp:read",exp=120}={})=>
  new SignJWT({scope})
   .setProtectedHeader({alg:"RS256",kid:jwk.kid})
   .setIssuer(iss).setAudience(aud).setSubject(subject)
   .setIssuedAt().setExpirationTime(Math.floor(Date.now()/1000)+exp)
   .sign(privateKey);
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
 console.log("OAuth JWT acceptance: exact issuer/audience, RS256, expiry, scope and pilot account restrictions pass.");
}finally{
 await new Promise(resolve=>jwksServer.close(resolve));
}
