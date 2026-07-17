// Client-side only — decodes the payload for UI purposes (which role,
// which station). The server is the one that actually verifies the
// signature on every request; this is never used for access control.
export interface AccessTokenClaims {
  sub: string; // user_id
  role_id: string;
  station_id: string | null;
  type: "access" | "refresh";
  iat: number;
  exp: number;
}

export function decodeJwt<T = AccessTokenClaims>(token: string): T | null {
  try {
    const payload = token.split(".")[1];
    const json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}
