import { client } from "./client";
import type { Citizen, CitizenCaseLink, RelationshipEdge, CitizenAssets } from "@/types/api";

export async function getCitizen(citizenId: string) {
  const res = await client.get<Citizen>(`/citizens/${citizenId}`);
  return res.data;
}
export async function getCitizenCases(citizenId: string) {
  const res = await client.get<CitizenCaseLink[]>(`/citizens/${citizenId}/cases`);
  return res.data;
}
export async function getCitizenRelationships(citizenId: string) {
  const res = await client.get<RelationshipEdge[]>(`/citizens/${citizenId}/relationships`);
  return res.data;
}
export async function getCitizenAssets(citizenId: string) {
  const res = await client.get<CitizenAssets>(`/citizens/${citizenId}/assets`);
  return res.data;
}
