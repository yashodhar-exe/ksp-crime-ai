import { client } from "./client";
import type { Officer, Case } from "@/types/api";

export async function getOfficer(officerId: string) {
  const res = await client.get<Officer>(`/officers/${officerId}`);
  return res.data;
}
export async function getOfficerCases(officerId: string) {
  const res = await client.get<Case[]>(`/officers/${officerId}/cases`);
  return res.data;
}
