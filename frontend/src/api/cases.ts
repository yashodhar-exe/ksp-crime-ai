import { client } from "./client";
import type {
  Case,
  CaseDetail,
  CaseListResponse,
  Suspect,
  Victim,
  Evidence,
  DigitalEvidence,
  InvestigationNote,
  TimelineEvent,
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

export async function getCaseSuspects(caseId: string) {
  const res = await client.get<Suspect[]>(`/cases/${caseId}/suspects`);
  return res.data;
}
export async function getCaseVictims(caseId: string) {
  const res = await client.get<Victim[]>(`/cases/${caseId}/victims`);
  return res.data;
}
export async function getCaseEvidence(caseId: string) {
  const res = await client.get<Evidence[]>(`/cases/${caseId}/evidence`);
  return res.data;
}
export async function getCaseDigitalEvidence(caseId: string) {
  const res = await client.get<DigitalEvidence[]>(`/cases/${caseId}/digital-evidence`);
  return res.data;
}
export async function getCaseNotes(caseId: string) {
  const res = await client.get<InvestigationNote[]>(`/cases/${caseId}/notes`);
  return res.data;
}
export async function getCaseTimeline(caseId: string) {
  const res = await client.get<TimelineEvent[]>(`/cases/${caseId}/timeline`);
  return res.data;
}
export async function getSimilarCases(caseId: string) {
  const res = await client.get<SimilarCase[]>(`/cases/${caseId}/similar-cases`);
  return res.data;
}
