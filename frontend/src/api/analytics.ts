import { client } from "./client";

export interface CrimeTrendPoint {
  period: string;
  crime_type: string;
  count: number;
}
export interface CrimeTrendsOut {
  district: string | null;
  period: string;
  points: CrimeTrendPoint[];
}
export interface HotspotOut {
  district: string;
  case_count: number;
  top_crime_type: string | null;
}
export interface PatternSummaryOut {
  pattern_id: string;
  crime_type: string;
  modus_operandi: string | null;
  risk_level: string;
  case_count: number;
}

export async function getCrimeTrends(params: { district?: string; period?: string } = {}) {
  const res = await client.get<CrimeTrendsOut>("/analytics/crime-trends", { params });
  return res.data;
}
export async function getHotspots() {
  const res = await client.get<HotspotOut[]>("/analytics/hotspots");
  return res.data;
}
export async function getPatterns() {
  const res = await client.get<PatternSummaryOut[]>("/analytics/patterns");
  return res.data;
}
