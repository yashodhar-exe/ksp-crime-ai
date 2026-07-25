import { Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { getDashboardSummary, getDashboardStats, getDashboardRecent, getDashboardActivity } from "@/api/dashboard";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell,
} from "recharts";

const PIE_COLORS = ["#0b1f5e", "#1d4ed8", "#8b5cf6", "#dc2626", "#d97706", "#059669"];

function StatCard({ label, value, icon }: { label: string; value: number | string; icon: string }) {
  return (
    <div className="card p-4 flex items-center gap-3">
      <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center">
        <Icon name={icon} className="text-primary-container" />
      </div>
      <div>
        <p className="text-2xl font-bold text-on-surface leading-none">{value}</p>
        <p className="text-xs text-on-surface-variant mt-1">{label}</p>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const summary = useAsync(getDashboardSummary, []);
  const stats = useAsync(getDashboardStats, []);
  const recent = useAsync(getDashboardRecent, []);
  const activity = useAsync(getDashboardActivity, []);

  return (
    <AppLayout title="Command Dashboard">
      {summary.loading ? (
        <LoadingState label="Loading dashboard..." />
      ) : summary.error ? (
        <ErrorState message={summary.error} onRetry={summary.reload} />
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <StatCard label="Total Cases" value={summary.data!.total_cases} icon="folder_shared" />
            <StatCard label="Open Cases" value={summary.data!.open_cases} icon="lock_open" />
            <StatCard label="Critical Cases" value={summary.data!.critical_cases} icon="priority_high" />
            <StatCard label="Citizens" value={summary.data!.total_citizens} icon="groups" />
            <StatCard label="Officers" value={summary.data!.total_officers} icon="local_police" />
          </div>
          {summary.data!.district && (
            <p className="text-xs text-on-surface-variant -mt-2">
              Scoped to <span className="font-semibold">{summary.data!.district}</span> district (your role's view)
            </p>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 card p-4">
              <h2 className="text-sm font-semibold text-on-surface mb-4">Cases by Status</h2>
              {stats.loading ? (
                <LoadingState />
              ) : stats.error ? (
                <ErrorState message={stats.error} onRetry={stats.reload} />
              ) : (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={stats.data!.by_status}>
                    <XAxis dataKey="label" fontSize={12} />
                    <YAxis fontSize={12} allowDecimals={false} />
                    <Tooltip cursor={false} />
                    <Bar dataKey="count" fill="#0b1f5e" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="card p-4">
              <h2 className="text-sm font-semibold text-on-surface mb-4">Cases by Crime Type</h2>
              {stats.loading ? (
                <LoadingState />
              ) : stats.error ? null : (
                <ResponsiveContainer width="100%" height={240}>
                  <PieChart>
                    <Pie
                      data={stats.data!.by_crime_type?.slice(0, 6) || []}
                      dataKey="count"
                      nameKey="label"
                      innerRadius={45}
                      outerRadius={80}
                    >
                      {(stats.data!.by_crime_type?.slice(0, 6) || []).map((_: any, i: number) => (
                        <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip cursor={false} />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 card p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-on-surface">Recent Cases</h2>
                <Link to="/cases" className="text-secondary text-sm font-bold flex items-center gap-1">
                  View All <Icon name="chevron_right" className="text-sm" />
                </Link>
              </div>
              {recent.loading ? (
                <LoadingState />
              ) : recent.error ? (
                <ErrorState message={recent.error} onRetry={recent.reload} />
              ) : (
                <div className="divide-y divide-outline-variant">
                  {(recent.data!.cases || []).map((c) => (
                    <Link
                      key={c.case_master_id}
                      to={`/cases/${c.case_master_id}`}
                      className="flex items-center justify-between py-3 hover:bg-surface-container-low -mx-2 px-2 rounded"
                    >
                      <div>
                        <p className="text-sm font-mono font-semibold text-on-surface">{c.crime_no}</p>
                        <p className="text-xs text-on-surface-variant">{c.crime_head_name} · {c.district_name}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <PriorityBadge value={c.gravity_name ?? "Unknown"} />
                        <StatusBadge value={c.case_status_name ?? "Unknown"} />
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            <div className="ai-panel p-4">
              <div className="flex items-center gap-2 mb-3">
                <h2 className="text-sm font-semibold text-on-surface">Recent Activity</h2>
              </div>
              {activity.loading ? (
                <LoadingState />
              ) : activity.error ? (
                <ErrorState message={activity.error} onRetry={activity.reload} />
              ) : (
                <ul className="space-y-3">
                  {(activity.data!.entries || []).slice(0, 8).map((entry) => (
                    <li key={entry.log_id} className="text-xs">
                      <p className="text-on-surface font-medium">{entry.action}</p>
                      <p className="text-on-surface-variant">
                        {entry.user_id} · {new Date(entry.timestamp).toLocaleString()}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </AppLayout>
  );
}
