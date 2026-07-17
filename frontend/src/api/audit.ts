import { client } from "./client";
import type { AuditLog, User } from "@/types/api";

export async function listAuditLogs(params: { user_id?: string; case_id?: string; limit?: number } = {}) {
  const res = await client.get<AuditLog[]>("/audit-logs", { params });
  return res.data;
}

export async function listUsers() {
  const res = await client.get<User[]>("/users");
  return res.data;
}
export async function createUser(payload: {
  username: string;
  password: string;
  role_id: string;
  officer_id?: string | null;
  station_id?: string | null;
}) {
  const res = await client.post<User>("/users", payload);
  return res.data;
}
export async function updateUser(
  userId: string,
  payload: Partial<{ role_id: string; station_id: string | null; status: string; password: string }>
) {
  const res = await client.patch<User>(`/users/${userId}`, payload);
  return res.data;
}
