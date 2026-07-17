import { NavLink } from "react-router-dom";
import { Icon } from "@/components/ui/Icon";
import { useAuth } from "@/context/AuthContext";
import { getRole } from "@/types/roles";

const NAV_ITEMS: { to: string; label: string; icon: string }[] = [
  { to: "/dashboard", label: "Dashboard", icon: "dashboard" },
  { to: "/cases", label: "Cases", icon: "folder_shared" },
  { to: "/search", label: "Search Intelligence", icon: "search" },
  { to: "/citizens", label: "Citizens", icon: "person_search" },
  { to: "/network", label: "Criminal Network", icon: "hub" },
  { to: "/officers", label: "Officers", icon: "local_police" },
  { to: "/stations", label: "Stations", icon: "location_city" },
  { to: "/analytics", label: "Analytics", icon: "analytics" },
  { to: "/assistant", label: "AI Assistant", icon: "psychology" },
  { to: "/audit", label: "Audit Logs", icon: "history" },
];

const ADMIN_ITEMS = [{ to: "/users", label: "User Management", icon: "manage_accounts" }];

export function Sidebar() {
  const { user } = useAuth();
  const role = getRole(user?.role_id);

  return (
    <aside className="w-[260px] h-full fixed left-0 top-0 bg-primary-container border-r border-outline-variant flex flex-col py-4 z-50">
      <div className="px-6 pb-6 flex items-center gap-2">
        <Icon name="shield" className="text-on-primary-container text-2xl" filled />
        <div className="leading-tight">
          <p className="text-on-primary-container font-bold text-sm">KSP Crime AI</p>
          <p className="text-on-primary-container/60 text-[11px] uppercase tracking-wide">SCRB Platform</p>
        </div>
      </div>

      <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-semibold text-sm transition-opacity ${
                isActive
                  ? "text-on-secondary-container bg-on-primary-fixed-variant opacity-100"
                  : "text-on-primary-container opacity-60 hover:opacity-100 hover:bg-on-primary-fixed-variant"
              }`
            }
          >
            <Icon name={item.icon} />
            {item.label}
          </NavLink>
        ))}

        {role?.can_manage_users &&
          ADMIN_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg font-semibold text-sm transition-opacity ${
                  isActive
                    ? "text-on-secondary-container bg-on-primary-fixed-variant opacity-100"
                    : "text-on-primary-container opacity-60 hover:opacity-100 hover:bg-on-primary-fixed-variant"
                }`
              }
            >
              <Icon name={item.icon} />
              {item.label}
            </NavLink>
          ))}
      </nav>

      <div className="px-3 pt-2 border-t border-on-primary-container/10 space-y-1">
        <NavLink
          to="/settings"
          className="flex items-center gap-3 px-4 py-2 rounded-lg text-on-primary-container opacity-60 hover:opacity-100 hover:bg-on-primary-fixed-variant text-sm font-semibold"
        >
          <Icon name="settings" />
          Settings
        </NavLink>
      </div>
    </aside>
  );
}
