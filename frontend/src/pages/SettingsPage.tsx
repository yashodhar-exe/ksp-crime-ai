import { useNavigate } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAuth } from "@/context/AuthContext";
import { getRole } from "@/types/roles";
import { Icon } from "@/components/ui/Icon";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const role = getRole(user?.role_id);
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <AppLayout title="System Settings & Security">
      <div className="max-w-2xl space-y-6">
        <div className="card p-5">
          <h2 className="text-sm font-semibold text-on-surface mb-4">Account</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-on-surface-variant">User ID</span><span className="font-mono">{user?.user_id}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Role</span><span>{role?.role_name}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Station Scope</span><span className="font-mono">{user?.station_id ?? "All Districts"}</span></div>
          </div>
        </div>

        <div className="card p-5">
          <h2 className="text-sm font-semibold text-on-surface mb-4">Permissions</h2>
          <div className="grid grid-cols-2 gap-3 text-sm">
            {role && Object.entries(role)
              .filter(([k]) => k.startsWith("can_"))
              .map(([k, v]) => (
                <div key={k} className="flex items-center gap-2">
                  <Icon name={v ? "check_circle" : "cancel"} className={`text-base ${v ? "text-green-600" : "text-outline"}`} filled={!!v} />
                  <span className="capitalize">{k.replace(/_/g, " ").replace("can ", "")}</span>
                </div>
              ))}
          </div>
        </div>

        <div className="card p-5 border-error/30">
          <div className="flex items-center gap-2 mb-2">
            <Icon name="gpp_maybe" className="text-error" filled />
            <h2 className="text-sm font-semibold text-on-surface">Security Notice</h2>
          </div>
          <p className="text-xs text-on-surface-variant mb-4">
            All access to this platform is logged in the audit trail, including case views, exports,
            and searches. Session tokens expire automatically; use the logout button when stepping away.
          </p>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 bg-error/10 text-error rounded-md text-sm font-semibold hover:bg-error/20 transition-colors"
          >
            <Icon name="logout" /> Logout
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
