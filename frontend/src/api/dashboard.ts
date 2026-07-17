import { client } from "./client";
import type { DashboardSummary, DashboardStats, DashboardRecent, DashboardActivity } from "@/types/api";

export async function getDashboardSummary() {
  const res = await client.get<DashboardSummary>("/dashboard/summary");
  return res.data;
}
export async function getDashboardStats() {
  const res = await client.get<DashboardStats>("/dashboard/stats");
  return res.data;
}
export async function getDashboardRecent() {
  const res = await client.get<DashboardRecent>("/dashboard/recent");
  return res.data;
}
export async function getDashboardActivity() {
  const res = await client.get<DashboardActivity>("/dashboard/activity");
  return res.data;
}
