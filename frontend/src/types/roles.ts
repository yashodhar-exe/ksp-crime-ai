// Mirrors dataset/processed/roles.csv exactly. This is small and static
// enough to hardcode client-side rather than add a round trip for it —
// if roles.csv changes, update this table to match.
export interface RoleDef {
  role_id: string;
  role_name: string;
  level: number;
  can_view_all_districts: boolean;
  can_export: boolean;
  can_edit_case: boolean;
  can_manage_users: boolean;
}

export const ROLES: Record<string, RoleDef> = {
  ROLE01: { role_id: "ROLE01", role_name: "Admin", level: 1, can_view_all_districts: true, can_export: true, can_edit_case: true, can_manage_users: true },
  ROLE02: { role_id: "ROLE02", role_name: "SP", level: 2, can_view_all_districts: true, can_export: true, can_edit_case: true, can_manage_users: false },
  ROLE03: { role_id: "ROLE03", role_name: "DSP", level: 3, can_view_all_districts: false, can_export: true, can_edit_case: true, can_manage_users: false },
  ROLE04: { role_id: "ROLE04", role_name: "Inspector", level: 4, can_view_all_districts: false, can_export: true, can_edit_case: true, can_manage_users: false },
  ROLE05: { role_id: "ROLE05", role_name: "Sub Inspector", level: 5, can_view_all_districts: false, can_export: false, can_edit_case: true, can_manage_users: false },
  ROLE06: { role_id: "ROLE06", role_name: "Constable", level: 6, can_view_all_districts: false, can_export: false, can_edit_case: false, can_manage_users: false },
};

export function getRole(roleId: string | undefined | null): RoleDef | null {
  if (!roleId) return null;
  return ROLES[roleId] ?? null;
}
