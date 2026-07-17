import { client, setTokens, clearTokens } from "./client";
import type { CurrentUser } from "@/types/api";

export async function login(username: string, password: string) {
  const res = await client.post("/auth/login", { username, password });
  setTokens(res.data.access_token, res.data.refresh_token);
  return res.data as { access_token: string; refresh_token: string; token_type: string };
}

export async function logout() {
  try {
    await client.post("/auth/logout");
  } finally {
    clearTokens();
  }
}

// The backend has no GET /auth/me — CurrentUser is decoded client-side
// from the JWT payload instead (see context/AuthContext.tsx).
export type { CurrentUser };
