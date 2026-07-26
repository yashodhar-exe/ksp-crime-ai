import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";

let envBaseUrl = import.meta.env.VITE_API_BASE_URL || "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1";
envBaseUrl = envBaseUrl.replace(/\/+$/, "");
if (!envBaseUrl.endsWith("/api/v1")) {
  envBaseUrl += "/api/v1";
}
export const API_BASE_URL = envBaseUrl;

export const client = axios.create({
  baseURL: API_BASE_URL,
});

const ACCESS_TOKEN_KEY = "ksp_access_token";
const REFRESH_TOKEN_KEY = "ksp_refresh_token";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}
export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}
export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}
export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

client.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  // Do not attach token for auth endpoints to prevent preflight OPTIONS requests
  if (config.url?.startsWith('/auth/')) {
    return config;
  }
  
  const token = getAccessToken();
  if (token) {
    // ALWAYS send token in query params to avoid Authorization header triggering CORS OPTIONS
    config.params = config.params || {};
    config.params.token = token;
  }
  return config;
});

let refreshInFlight: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return null;
  try {
    const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });
    const { access_token, refresh_token } = res.data;
    setTokens(access_token, refresh_token);
    return access_token;
  } catch {
    clearTokens();
    return null;
  }
}

client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined;

    if (error.response?.status === 401 && original && !original._retry) {
      original._retry = true;
      if (!refreshInFlight) {
        refreshInFlight = refreshAccessToken().finally(() => {
          refreshInFlight = null;
        });
      }
      const newToken = await refreshInFlight;
      if (newToken) {
        original.headers = original.headers ?? {};
        original.headers.Authorization = `Bearer ${newToken}`;
        return client(original);
      }
      // refresh failed — force re-login
      clearTokens();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
