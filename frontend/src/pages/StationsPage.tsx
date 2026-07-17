import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { listStations, getStationCases } from "@/api/stations";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";

export default function StationsPage() {
  const { stationId } = useParams();
  const [query, setQuery] = useState("");
  const stations = useAsync(listStations, []);
  const stationCases = useAsync(
    () => (stationId ? getStationCases(stationId) : Promise.resolve([])),
    [stationId]
  );

  if (stationId) {
    const station = stations.data?.find((s) => s.station_id === stationId);
    return (
      <AppLayout title="Station Detail">
        <Link to="/stations" className="text-sm text-secondary font-semibold flex items-center gap-1 mb-4">
          <Icon name="arrow_back" className="text-sm" /> Back to Directory
        </Link>
        {stations.loading ? <LoadingState /> : station && (
          <div className="card p-5 mb-6">
            <h2 className="text-lg font-bold text-on-surface">{station.station_name}</h2>
            <p className="text-sm text-on-surface-variant">{station.city}, {station.district} · {station.phone}</p>
          </div>
        )}
        <div className="card p-4">
          <h3 className="text-sm font-semibold text-on-surface mb-3">Cases Filed at this Station</h3>
          {stationCases.loading ? <LoadingState /> : stationCases.error ? <ErrorState message={stationCases.error} /> : (
            <ul className="divide-y divide-outline-variant">
              {stationCases.data!.map((c) => (
                <li key={c.case_id} className="py-2.5 flex items-center justify-between">
                  <div>
                    <Link to={`/cases/${c.case_id}`} className="text-sm font-mono text-secondary hover:underline">{c.fir_number}</Link>
                    <p className="text-xs text-on-surface-variant">{c.crime_type}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <PriorityBadge value={c.priority} />
                    <StatusBadge value={c.status} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </AppLayout>
    );
  }

  const filtered = stations.data?.filter(
    (s) =>
      s.station_name.toLowerCase().includes(query.toLowerCase()) ||
      s.district.toLowerCase().includes(query.toLowerCase()) ||
      s.city.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <AppLayout title="Police Station Directory">
      <div className="card p-4 mb-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Filter by station name, city, or district..."
          className="w-full border border-outline-variant rounded-md px-3 py-2 text-sm"
        />
      </div>
      {stations.loading ? (
        <LoadingState />
      ) : stations.error ? (
        <ErrorState message={stations.error} onRetry={stations.reload} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered!.map((s) => (
            <Link key={s.station_id} to={`/stations/${s.station_id}`} className="card p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-center gap-2 mb-1">
                <Icon name="location_city" className="text-primary-container text-lg" />
                <h3 className="text-sm font-semibold text-on-surface">{s.station_name}</h3>
              </div>
              <p className="text-xs text-on-surface-variant">{s.city}, {s.district}</p>
              <p className="text-xs text-on-surface-variant font-mono mt-1">{s.phone}</p>
            </Link>
          ))}
        </div>
      )}
    </AppLayout>
  );
}
