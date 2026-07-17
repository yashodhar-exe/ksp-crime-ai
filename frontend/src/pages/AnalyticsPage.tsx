import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { getCrimeTrends, getHotspots, getPatterns } from "@/api/analytics";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { Icon } from "@/components/ui/Icon";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";

export default function AnalyticsPage() {
  const [district, setDistrict] = useState("");
  const trends = useAsync(() => getCrimeTrends({ district: district || undefined }), [district]);
  const hotspots = useAsync(getHotspots, []);
  const patterns = useAsync(getPatterns, []);

  // Reshape trend points (period, crime_type, count) into recharts-friendly rows per period.
  const chartData = (() => {
    if (!trends.data) return [];
    const byPeriod = new Map<string, Record<string, number | string>>();
    for (const p of trends.data.points) {
      const row = byPeriod.get(p.period) ?? { period: p.period };
      row[p.crime_type] = p.count;
      byPeriod.set(p.period, row);
    }
    return Array.from(byPeriod.values());
  })();
  const crimeTypesInChart = Array.from(new Set(trends.data?.points.map((p) => p.crime_type) ?? [])).slice(0, 5);
  const COLORS = ["#0b1f5e", "#1d4ed8", "#8b5cf6", "#dc2626", "#059669"];

  return (
    <AppLayout title="Crime Analytics & Predictive Intelligence">
      <div className="card p-4 mb-6 flex items-center gap-3">
        <input
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
          placeholder="Filter by district (leave blank for all)"
          className="border border-outline-variant rounded-md px-3 py-2 text-sm w-72"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2 card p-4">
          <h2 className="text-sm font-semibold text-on-surface mb-4">Crime Trends</h2>
          {trends.loading ? <LoadingState /> : trends.error ? <ErrorState message={trends.error} onRetry={trends.reload} /> : (
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData}>
                <XAxis dataKey="period" fontSize={11} />
                <YAxis fontSize={11} allowDecimals={false} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                {crimeTypesInChart.map((ct, i) => (
                  <Line key={ct} type="monotone" dataKey={ct} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={false} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card p-4">
          <div className="flex items-center gap-2 mb-4">
            <Icon name="location_on" className="text-error text-lg" />
            <h2 className="text-sm font-semibold text-on-surface">District Hotspots</h2>
          </div>
          {hotspots.loading ? <LoadingState /> : hotspots.error ? <ErrorState message={hotspots.error} /> : (
            <ul className="space-y-2 text-sm max-h-64 overflow-y-auto">
              {hotspots.data!.slice(0, 12).map((h) => (
                <li key={h.district} className="flex justify-between">
                  <span>{h.district}</span>
                  <span className="text-xs text-on-surface-variant">{h.case_count} cases {h.top_crime_type ? `· ${h.top_crime_type}` : ""}</span>
                </li>
              ))}
            </ul>
          )}
          <p className="text-[11px] text-on-surface-variant mt-3 pt-3 border-t border-outline-variant">
            District-level only — no GPS coordinates in this dataset. See README "Known limitations."
          </p>
        </div>
      </div>

      <div className="card p-4">
        <h2 className="text-sm font-semibold text-on-surface mb-4">Crime Patterns & Risk Levels</h2>
        {patterns.loading ? <LoadingState /> : patterns.error ? <ErrorState message={patterns.error} /> : (
          <table className="data-table w-full text-sm">
            <thead>
              <tr>
                <th className="px-4 py-2">Crime Type</th>
                <th className="px-4 py-2">Modus Operandi</th>
                <th className="px-4 py-2">Risk Level</th>
                <th className="px-4 py-2">Case Count</th>
              </tr>
            </thead>
            <tbody>
              {patterns.data!.map((p) => (
                <tr key={p.pattern_id} className="border-t border-outline-variant/50">
                  <td className="px-4 py-2">{p.crime_type}</td>
                  <td className="px-4 py-2">{p.modus_operandi ?? "—"}</td>
                  <td className="px-4 py-2">{p.risk_level}</td>
                  <td className="px-4 py-2">{p.case_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  );
}
