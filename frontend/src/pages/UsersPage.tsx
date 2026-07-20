import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { listUsers, createUser, updateUser, approveUser, rejectUser } from "@/api/audit";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { Icon } from "@/components/ui/Icon";
import { getRole, ROLES } from "@/types/roles";

export default function UsersPage() {
  const { data, loading, error, reload } = useAsync(listUsers, []);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ username: "", password: "", role_id: "ROLE06" });
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setFormError(null);
    try {
      await createUser(form);
      setForm({ username: "", password: "", role_id: "ROLE06" });
      setShowForm(false);
      reload();
    } catch (err: any) {
      setFormError(err?.response?.data?.detail ?? "Could not create user.");
    } finally {
      setSubmitting(false);
    }
  }

  const [actioningId, setActioningId] = useState<string | null>(null);

  async function toggleStatus(userId: string, current: string) {
    await updateUser(userId, { status: current === "Active" ? "Inactive" : "Active" });
    reload();
  }

  async function handleApprove(userId: string) {
    setActioningId(userId);
    try {
      await approveUser(userId);
      reload();
    } finally {
      setActioningId(null);
    }
  }

  async function handleReject(userId: string) {
    if (!window.confirm("Reject this registration? The account will not be able to log in.")) return;
    setActioningId(userId);
    try {
      await rejectUser(userId);
      reload();
    } finally {
      setActioningId(null);
    }
  }

  const pendingUsers = data?.filter((u) => u.status === "Pending") ?? [];
  const otherUsers = data?.filter((u) => u.status !== "Pending") ?? [];

  return (
    <AppLayout title="User Management">
      <div className="flex justify-end mb-4">
        <button
          onClick={() => setShowForm((s) => !s)}
          className="flex items-center gap-1.5 bg-primary-container text-on-primary px-4 py-2 rounded-md text-sm font-semibold"
        >
          <Icon name="add" className="text-sm" /> New User
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card p-4 mb-4 flex flex-wrap gap-3 items-end">
          <div>
            <label className="text-xs text-on-surface-variant block mb-1">Username</label>
            <input
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
              className="border border-outline-variant rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="text-xs text-on-surface-variant block mb-1">Password</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
              className="border border-outline-variant rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="text-xs text-on-surface-variant block mb-1">Role</label>
            <select
              value={form.role_id}
              onChange={(e) => setForm({ ...form, role_id: e.target.value })}
              className="border border-outline-variant rounded-md px-3 py-2 text-sm"
            >
              {Object.values(ROLES).map((r) => (
                <option key={r.role_id} value={r.role_id}>{r.role_name}</option>
              ))}
            </select>
          </div>
          <button type="submit" disabled={submitting} className="bg-primary-container text-on-primary px-4 py-2 rounded-md text-sm font-semibold disabled:opacity-60">
            {submitting ? "Creating..." : "Create"}
          </button>
          {formError && <p className="text-error text-xs w-full">{formError}</p>}
        </form>
      )}

      {!loading && !error && pendingUsers.length > 0 && (
        <div className="card overflow-hidden mb-4 border-amber-300/60">
          <div className="px-4 py-3 border-b border-outline-variant/50 flex items-center gap-2 bg-amber-50">
            <Icon name="pending_actions" className="text-amber-700 text-lg" />
            <h2 className="text-sm font-semibold text-amber-900">
              Pending Approvals ({pendingUsers.length})
            </h2>
          </div>
          <table className="data-table w-full text-sm">
            <thead>
              <tr>
                <th className="px-4 py-2">Username</th>
                <th className="px-4 py-2">Requested Role</th>
                <th className="px-4 py-2"></th>
              </tr>
            </thead>
            <tbody>
              {pendingUsers.map((u) => (
                <tr key={u.user_id} className="border-t border-outline-variant/50">
                  <td className="px-4 py-2">{u.username}</td>
                  <td className="px-4 py-2">{getRole(u.role_id)?.role_name ?? u.role_id}</td>
                  <td className="px-4 py-2 text-right space-x-3">
                    <button
                      disabled={actioningId === u.user_id}
                      onClick={() => handleApprove(u.user_id)}
                      className="text-green-700 text-xs font-semibold hover:underline disabled:opacity-50"
                    >
                      Approve
                    </button>
                    <button
                      disabled={actioningId === u.user_id}
                      onClick={() => handleReject(u.user_id)}
                      className="text-error text-xs font-semibold hover:underline disabled:opacity-50"
                    >
                      Reject
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card overflow-hidden">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState message={error} onRetry={reload} />
        ) : (
          <table className="data-table w-full text-sm">
            <thead>
              <tr>
                <th className="px-4 py-2">Username</th>
                <th className="px-4 py-2">Role</th>
                <th className="px-4 py-2">Station</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2">Last Login</th>
                <th className="px-4 py-2"></th>
              </tr>
            </thead>
            <tbody>
              {otherUsers.map((u) => (
                <tr key={u.user_id} className="border-t border-outline-variant/50">
                  <td className="px-4 py-2">{u.username}</td>
                  <td className="px-4 py-2">{getRole(u.role_id)?.role_name ?? u.role_id}</td>
                  <td className="px-4 py-2 font-mono text-xs">{u.station_id ?? "—"}</td>
                  <td className="px-4 py-2">
                    <span
                      className={`badge-pill ${
                        u.status === "Active"
                          ? "bg-green-50 text-green-700"
                          : u.status === "Rejected"
                          ? "bg-red-50 text-red-700"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {u.status}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-xs">{u.last_login ?? "—"}</td>
                  <td className="px-4 py-2 text-right">
                    <button
                      onClick={() => toggleStatus(u.user_id, u.status)}
                      className="text-secondary text-xs font-semibold hover:underline"
                    >
                      {u.status === "Active" ? "Deactivate" : "Activate"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  );
}
