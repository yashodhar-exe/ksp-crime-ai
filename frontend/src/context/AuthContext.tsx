import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { login as apiLogin, logout as apiLogout } from "@/api/auth";
import { getAccessToken, clearTokens } from "@/api/client";
import { decodeJwt } from "@/api/jwt";

interface AuthUser {
  user_id: string;
  role_id: string;
  station_id: string | null;
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function userFromToken(): AuthUser | null {
  const token = getAccessToken();
  if (!token) return null;
  const claims = decodeJwt(token);
  if (!claims) return null;
  if (claims.exp * 1000 < Date.now()) return null;
  return { user_id: claims.sub, role_id: claims.role_id, station_id: claims.station_id };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setUser(userFromToken());
    setLoading(false);
  }, []);

  async function login(username: string, password: string) {
    await apiLogin(username, password);
    setUser(userFromToken());
  }

  async function logout() {
    await apiLogout().catch(() => {
      // even if the network call fails, clear local state
      clearTokens();
    });
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
