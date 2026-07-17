import { client } from "./client";
import type { Station, Case } from "@/types/api";

export async function listStations() {
  const res = await client.get<Station[]>("/stations");
  return res.data;
}
export async function getStationCases(stationId: string) {
  const res = await client.get<Case[]>(`/stations/${stationId}/cases`);
  return res.data;
}
