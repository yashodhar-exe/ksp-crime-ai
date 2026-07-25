import { NavLink, Link } from "react-router-dom";
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
    <aside className="w-[260px] h-full fixed left-0 top-0 bg-surface-container-lowest border-r border-outline-variant flex flex-col py-4 z-50 shadow-sm">
      <Link to="/dashboard" className="px-6 pb-6 flex items-center gap-3 cursor-pointer">
        <img src="/src/assets/Karnataka Police.svg" alt="Karnataka Police" className="w-10 h-10 object-contain drop-shadow-sm" />
        <div className="leading-tight">
          <p className="text-on-surface font-bold text-sm">KSP Crime AI</p>
        </div>
      </Link>

      <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-semibold text-sm transition-colors ${
                isActive
                  ? "text-primary bg-surface-container-high"
                  : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container"
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
                `flex items-center gap-3 px-4 py-3 rounded-lg font-semibold text-sm transition-colors ${
                  isActive
                    ? "text-primary bg-surface-container-high"
                    : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container"
                }`
              }
            >
              <Icon name={item.icon} />
              {item.label}
            </NavLink>
          ))}
      </nav>

      <div className="px-3 pt-2 border-t border-outline-variant space-y-1">
        <NavLink
          to="/settings"
          className="flex items-center gap-3 px-4 py-2 rounded-lg text-on-surface-variant hover:text-on-surface hover:bg-surface-container text-sm font-semibold"
        >
          <Icon name="settings" />
          Settings
        </NavLink>
      </div>
    </aside>
  );
}
