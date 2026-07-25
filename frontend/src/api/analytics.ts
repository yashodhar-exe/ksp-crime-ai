import { client } from "./client";

export interface CrimeTrendPoint {
  period: string;
  crime_sub_head_name: string;
  count: number;
}
export interface CrimeTrendsOut {
  district: string | null;
  period: string;
  points: CrimeTrendPoint[];
}
export interface HotspotOut {
  district_name: string;
  case_count: number;
  top_crime_sub_head_name: string | null;
}
export interface CrimeHeadOut {
  crime_head_id: number;
  crime_group_name: string;
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
export async function getCrimeHeads() {
  const res = await client.get<CrimeHeadOut[]>("/analytics/crime-heads");
  return res.data;
}
