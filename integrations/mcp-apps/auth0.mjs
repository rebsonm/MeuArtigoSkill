/** Auth0 resource-server checks for the optional Meu Artigo MCP transport.
 * Identity is NOT research telemetry. One explicitly allowlisted Google identity
 * is the only supported pilot; do not treat this as multi-tenant authorization.
 */
import { createRemoteJWKSet, jwtVerify } from "jose";

const oauthScopes = Object.freeze(["mcp:read"]);

function exactHttpsUrl(value, name) {
  const parsed = new URL(value);
  if (parsed.protocol !== "https:" || parsed.username || parsed.password ||
      parsed.search || parsed.hash) throw Error("Invalid " + name);
  return parsed;
}

export function auth0Configuration(env = process.env) {
  const issuer = exactHttpsUrl(env.MEU_ARTIGO_AUTH_ISSUER || "", "issuer");
  if (!issuer.hostname.endsWith(".auth0.com") || issuer.pathname !== "/")
    throw Error("Auth0 issuer must be the exact HTTPS Auth0 tenant issuer including trailing slash");
  const resource = exactHttpsUrl(env.MEU_ARTIGO_AUTH_RESOURCE || "", "resource");
  if (resource.pathname !== "/mcp")
    throw Error("Protected resource URL must be the HTTPS /mcp endpoint");
  const permittedSub = String(env.MEU_ARTIGO_PILOT_SUB || "");
  if (!/^google-oauth2\|[A-Za-z0-9_-]{5,128}$/.test(permittedSub))
    throw Error("Exactly one Google Auth0 subject must be allowlisted for pilot isolation");
  return Object.freeze({
    issuer: issuer.href,
    resource: resource.href,
    metadataUrl: new URL("/.well-known/oauth-protected-resource", resource).href,
    jwksUrl: new URL(".well-known/jwks.json", issuer).href,
    permittedSub,
    scopes: oauthScopes
  });
}

export function protectedResourceMetadata(config) {
  return {
    resource: config.resource,
    authorization_servers: [config.issuer],
    scopes_supported: [...config.scopes]
  };
}

export function bearerChallenge(config, error = null) {
  let result = 'Bearer resource_metadata="' + config.metadataUrl +
    '", scope="' + config.scopes.join(" ") + '"';
  if (error === "invalid_token") result += ', error="invalid_token"';
  if (error === "insufficient_scope") result += ', error="insufficient_scope"';
  return result;
}

export function createAuth0Verifier(config, { jwksUrl } = {}) {
  // Production always uses Auth0's JWKS URL. Alternate JWKS only for injected
  // unit-test verifiers; the HTTP server never passes a JWKS override.
  const jwks = createRemoteJWKSet(new URL(jwksUrl || config.jwksUrl), {
    timeoutDuration: 5000, cooldownDuration: 1000
  });
  return async function verifyAuthorization(header) {
    const match = /^Bearer ([A-Za-z0-9_.-]{20,12000})$/i.exec(header || "");
    if (!match) return { ok: false, status: 401, error: "invalid_token" };
    try {
      const { payload } = await jwtVerify(match[1], jwks, {
        issuer: config.issuer,
        audience: config.resource,
        algorithms: ["RS256"],
        clockTolerance: 5
      });
      // Reject perpetual or extremely long-lived user bearer grants.
      const now=Math.floor(Date.now()/1000);
      if(!Number.isSafeInteger(payload.exp)||!Number.isSafeInteger(payload.iat)||
         payload.iat>now+5||payload.exp<=payload.iat||
         payload.exp-payload.iat>3600)
        return {ok:false,status:401,error:"invalid_token"};
      // An Auth0 client-credentials token must never acquire user rights.
      if (payload.sub !== config.permittedSub)
        return { ok: false, status: 403, error: "access_denied" };
      const granted = typeof payload.scope === "string"
        ? payload.scope.split(/\s+/).filter(Boolean) : [];
      if (!config.scopes.every(scope => granted.includes(scope)))
        return { ok: false, status: 403, error: "insufficient_scope" };
      return { ok: true, principal: { sub: config.permittedSub } };
    } catch {
      return { ok: false, status: 401, error: "invalid_token" };
    }
  };
}
