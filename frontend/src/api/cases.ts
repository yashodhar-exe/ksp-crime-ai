import { client } from "./client";
import type {
  Case,
  CaseDetail,
  CaseListResponse,
  SimilarCase,
} from "@/types/api";

export interface CaseFilters {
  crime_type?: string;
  status?: string;
  district?: string;
  limit?: number;
  offset?: number;
}

export async function listCases(filters: CaseFilters = {}) {
  const res = await client.get<CaseListResponse>("/cases", { params: filters });
  return res.data;
}

export async function getCase(caseId: string) {
  const res = await client.get<CaseDetail>(`/cases/${caseId}`);
  return res.data;
}

export async function updateCase(caseId: string, updates: Partial<Case> & { description?: string | null }) {
  const res = await client.patch<CaseDetail>(`/cases/${caseId}`, updates);
  return res.data;
}

export async function createCase(payload: Record<string, unknown>) {
  const res = await client.post<CaseDetail>("/cases", payload);
  return res.data;
}

export async function getSimilarCases(caseId: string) {
  const res = await client.get<SimilarCase[]>(`/cases/${caseId}/similar-cases`);
  return res.data;
}
