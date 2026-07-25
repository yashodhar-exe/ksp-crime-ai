import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { getOfficer, getOfficerCases } from "@/api/officers";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";

export default function OfficersPage() {
  const { officerId } = useParams();
  const [lookupValue, setLookupValue] = useState(officerId ?? "");
  const navigate = useNavigate();

  const officer = useAsync(() => getOfficer(officerId!), [officerId]);
  const cases = useAsync(() => getOfficerCases(officerId!), [officerId]);

  function handleLookup(e: React.FormEvent) {
    e.preventDefault();
    if (lookupValue.trim()) navigate(`/officers/${lookupValue.trim()}`);
  }

  return (
    <AppLayout title="Officer Management & Performance">
      <form onSubmit={handleLookup} className="card p-4 mb-4 flex gap-2 items-center">
        <Icon name="local_police" className="text-primary-container" />
        <input
          value={lookupValue}
          onChange={(e) => setLookupValue(e.target.value)}
          placeholder="Officer ID, e.g. OFF00074"
          className="flex-1 border border-outline-variant rounded-md px-3 py-2 text-sm font-mono"
        />
        <button type="submit" className="bg-primary-container text-on-primary px-5 py-2 rounded-md text-sm font-semibold">
          Look Up
        </button>
      </form>

      {!officerId ? (
        <div className="card p-8 text-center text-sm text-on-surface-variant">
          Enter an Officer ID above (visible on any case detail page) to view their assignment history.
        </div>
      ) : officer.loading ? (
        <LoadingState />
      ) : officer.error ? (
        <ErrorState message={officer.error} onRetry={officer.reload} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="card p-5 lg:col-span-1">
            <h2 className="text-lg font-bold text-on-surface">{officer.data!.name}</h2>
            <p className="text-sm text-on-surface-variant mb-4">{officer.data!.rank}</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-on-surface-variant">Officer ID</span><span className="font-mono">{officer.data!.officer_id}</span></div>
              <div className="flex justify-between"><span className="text-on-surface-variant">Station</span>
                <Link to={`/stations/${officer.data!.station_id}`} className="text-secondary hover:underline">{officer.data!.station_id}</Link>
              </div>
              <div className="flex justify-between"><span className="text-on-surface-variant">Phone</span><span className="font-mono">{officer.data!.phone}</span></div>
              <div className="flex justify-between"><span className="text-on-surface-variant">Email</span><span>{officer.data!.email ?? "—"}</span></div>
            </div>
          </div>

          <div className="card p-4 lg:col-span-2">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Assigned Cases ({cases.data?.length ?? "…"})</h3>
            {cases.loading ? <LoadingState /> : cases.error ? <ErrorState message={cases.error} /> : (
              <ul className="divide-y divide-outline-variant">
                {cases.data!.map((c) => (
                  <li key={c.case_master_id} className="py-2.5 flex items-center justify-between">
                    <div>
                      <Link to={`/cases/${c.case_master_id}`} className="text-sm font-mono text-secondary hover:underline">{c.crime_no}</Link>
                      <p className="text-xs text-on-surface-variant">{c.crime_head_name} · {c.district_name}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <PriorityBadge value={c.gravity_name ?? "Unknown"} />
                      <StatusBadge value={c.case_status_name ?? "Unknown"} />
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </AppLayout>
  );
}
