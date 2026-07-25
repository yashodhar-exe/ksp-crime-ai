// Mirrors backend/app/schemas/*.py
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
  last_login: string | null;
}

export interface Case {
  case_master_id: number;
  crime_no: string;
  case_no: string;
  crime_registered_date: string;
  police_person_id: number;
  police_station_id: number;
  case_category_id: number;
  gravity_offence_id: number | null;
  crime_major_head_id: number | null;
  crime_minor_head_id: number | null;
  case_status_id: number;
  court_id: number | null;
  incident_from_date: string | null;
  incident_to_date: string | null;
  latitude: number | null;
  longitude: number | null;

  case_category_name: string | null;
  case_status_name: string | null;
  gravity_name: string | null;
  crime_head_name: string | null;
  crime_sub_head_name: string | null;
  police_station_name: string | null;
  district_name: string | null;
}

export interface Complainant {
  complainant_id: number;
  case_master_id: number;
  complainant_name: string;
  age_year: number | null;
  occupation_id: number | null;
  religion_id: number | null;
  caste_id: number | null;
  gender_id: number | null;
}

export interface ActSection {
  id: number;
  case_master_id: number;
  act_id: string;
  section_id: string;
  act_order_id: number | null;
  section_order_id: number | null;
}

export interface Victim {
  victim_master_id: number;
  case_master_id: number;
  victim_name: string;
  age_year: number | null;
  gender_id: string | null;
  victim_police: boolean;
}

export interface Accused {
  accused_master_id: number;
  case_master_id: number;
  accused_name: string;
  age_year: number | null;
  gender_id: string | null;
  person_id: string | null;
}

export interface ArrestSurrender {
  arrest_surrender_id: number;
  case_master_id: number;
  arrest_surrender_type_id: number | null;
  arrest_surrender_date: string | null;
  arrest_surrender_state_id: number | null;
  arrest_surrender_district_id: number | null;
  police_station_id: number | null;
  io_id: number | null;
  court_id: number | null;
  accused_master_id: number | null;
  is_accused: boolean;
  is_complainant_accused: boolean;
}

export interface Chargesheet {
  csid: number;
  case_master_id: number;
  csdate: string | null;
  cstype: string;
  police_person_id: number | null;
}

export interface CaseDetail extends Case {
  info_received_ps_date: string | null;
  brief_facts: string | null;
  registering_officer_name: string | null;
  court_name: string | null;

  complainants: Complainant[];
  act_sections: ActSection[];
  victims: Victim[];
  accused: Accused[];
  arrest_surrenders: ArrestSurrender[];
  chargesheets: Chargesheet[];
}

export interface CaseListResponse {
  items: Case[];
  page: Page;
}

export interface SimilarCase {
  case_master_id: number;
  crime_no: string;
  crime_sub_head_name: string | null;
  case_status_name: string | null;
  district_name: string | null;
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
  role: string;
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
  log_id: number;
  user_id: string;
  action: string;
  case_master_id: number | null;
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
  unit_id: number;
  unit_name: string;
  unit_type_name: string;
  district_name: string | null;
  active: boolean;
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
