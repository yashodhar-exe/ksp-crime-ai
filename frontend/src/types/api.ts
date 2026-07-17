// Mirrors backend/app/schemas/*.py — keep in sync manually since the two
// codebases aren't in the same language for a shared codegen step.

export interface Page {
  total: number;
  limit: number;
  offset: number;
}

export interface CurrentUser {
  user_id: string;
  username: string;
  role_id: string;
  officer_id: string | null;
  station_id: string | null;
  status: string;
}

export interface Case {
  case_id: string;
  fir_number: string;
  crime_type: string;
  station_id: string;
  officer_id: string;
  status: string;
  priority: "High" | "Medium" | "Low" | "Critical" | string;
  incident_date: string;
  registered_date: string;
  city: string;
  district: string;
  estimated_loss: number;
  pattern_id: string | null;
}

export interface CaseDetail extends Case {
  description: string | null;
  complaint_text: string;
  station_name?: string | null;
  officer_name?: string | null;
}

export interface CaseListResponse {
  items: Case[];
  page: Page;
}

export interface Suspect {
  suspect_id: string;
  case_id: string;
  citizen_id: string;
  role: string;
  arrest_status: string;
}

export interface Victim {
  victim_id: string;
  case_id: string;
  citizen_id: string;
  injury_level: string;
}

export interface Evidence {
  evidence_id: string;
  case_id: string;
  evidence_type: string;
  description: string | null;
  status: string;
  collected_by: string | null;
}

export interface DigitalEvidence {
  digital_evidence_id: string;
  case_id: string;
  file_type: string;
  file_name: string | null;
  phone_number: string | null;
  email: string | null;
  ip_address: string | null;
  uploaded_by: string | null;
  status: string;
  extracted_entities: string | null;
}

export interface InvestigationNote {
  note_id: string;
  case_id: string;
  officer_id: string;
  note: string;
}

export interface TimelineEvent {
  event_id: string;
  case_id: string;
  event: string;
}

export interface SimilarCase {
  case_id: string;
  fir_number: string;
  crime_type: string;
  status: string;
  district: string;
  pattern_id: string | null;
  similarity_reason: string;
}

export interface Citizen {
  citizen_id: string;
  first_name: string;
  last_name: string;
  gender: string;
  age: number;
  phone: string;
  email: string | null;
  address: string | null;
  city: string;
  district: string;
}

export interface CitizenCaseLink {
  case_id: string;
  fir_number: string;
  crime_type: string;
  status: string;
  role: "Suspect" | "Victim" | string;
}

export interface RelationshipEdge {
  relationship_id: string;
  citizen_1: string;
  citizen_2: string;
  relationship_type: string;
}

export interface CitizenAssets {
  phones: { phone_id: string; phone_number: string; provider: string | null }[];
  vehicles: { vehicle_id: string; vehicle_number: string; vehicle_type: string | null }[];
  bank_accounts: { account_id: string; bank_name: string; account_number: string; ifsc: string | null }[];
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
}
export interface GraphEdge {
  source: string;
  target: string;
  relationship_type: string;
}
export interface NetworkGraph {
  center: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface SearchResult {
  entity_type: string;
  entity_value: string;
  case_id: string;
  fir_number?: string | null;
  crime_type?: string | null;
  status?: string | null;
}
export interface SearchResponse {
  query: string;
  entity_type: string | null;
  results: SearchResult[];
}

export interface DashboardSummary {
  total_cases: number;
  open_cases: number;
  critical_cases: number;
  total_citizens: number;
  total_officers: number;
  district: string | null;
}
export interface BreakdownPoint {
  label: string;
  count: number;
}
export interface DashboardStats {
  by_status: BreakdownPoint[];
  by_crime_type: BreakdownPoint[];
}
export interface DashboardRecent {
  cases: Case[];
}
export interface AuditLog {
  log_id: string;
  user_id: string;
  action: string;
  case_id: string | null;
  timestamp: string;
  ip_address: string;
}
export interface DashboardActivity {
  entries: AuditLog[];
}

export interface ChatSource {
  case_id: string;
  fir_number: string;
  snippet: string;
}
export interface ChatQueryResponse {
  session_id: string;
  answer: string;
  sources: ChatSource[];
}
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}
export interface ChatHistory {
  session_id: string;
  messages: ChatMessage[];
}

export interface Officer {
  officer_id: string;
  name: string;
  rank: string;
  station_id: string;
  phone: string;
  email: string | null;
}

export interface Station {
  station_id: string;
  station_name: string;
  district: string;
  city: string;
  phone: string;
}

export interface User {
  user_id: string;
  officer_id: string | null;
  username: string;
  role_id: string;
  station_id: string | null;
  status: string;
  last_login: string | null;
}
