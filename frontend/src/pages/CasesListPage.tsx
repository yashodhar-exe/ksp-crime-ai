import { useState } from "react";
import { Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { listCases } from "@/api/cases";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";

const CRIME_TYPES = [
  "Cyber Fraud", "UPI Fraud", "ATM Fraud", "Online Scam", "Identity Theft",
  "Chain Snatching", "Mobile Theft", "Vehicle Theft", "Burglary", "Assault",
  "Domestic Violence", "Drug Trafficking", "Kidnapping", "Missing Person", "Murder",
];
const STATUSES = ["Open", "Under Investigation", "Pending", "Closed", "Resolved"];

export default function CasesListPage() {
  const [crimeType, setCrimeType] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const limit = 25;

  const { data, loading, error, reload } = useAsync(
    () => listCases({ crime_type: crimeType || undefined, status: status || undefined, limit, offset }),
    [crimeType, status, offset]
  );

  return (
    <AppLayout title="Case Management">
      <div className="card p-4 mb-4 flex flex-wrap gap-3 items-center">
        <select
          value={crimeType}
          onChange={(e) => { setCrimeType(e.target.value); setOffset(0); }}
          className="border border-outline-variant rounded-md text-sm px-3 py-2"
        >
          <option value="">All Crime Types</option>
          {CRIME_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select
          value={status}
          onChange={(e) => { setStatus(e.target.value); setOffset(0); }}
          className="border border-outline-variant rounded-md text-sm px-3 py-2"
        >
          <option value="">All Statuses</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        {data && <span className="text-xs text-on-surface-variant ml-auto">{data.page.total} cases found</span>}
      </div>

      <div className="card overflow-hidden">
        {loading ? (
          <LoadingState label="Loading cases..." />
        ) : error ? (
          <ErrorState message={error} onRetry={reload} />
        ) : data && data.items.length === 0 ? (
          <EmptyState label="No cases match these filters." />
        ) : (
          <>
            <table className="data-table w-full text-sm">
              <thead>
                <tr>
                  <th className="px-4 py-2">FIR Number</th>
                  <th className="px-4 py-2">Crime Type</th>
                  <th className="px-4 py-2">District</th>
                  <th className="px-4 py-2">Incident Date</th>
                  <th className="px-4 py-2">Priority</th>
                  <th className="px-4 py-2">Status</th>
                  <th className="px-4 py-2"></th>
                </tr>
              </thead>
              <tbody>
                {data?.items.map((c) => (
                  <tr key={c.case_id} className="border-t border-outline-variant/50">
                    <td className="px-4 py-2 font-mono text-xs">{c.fir_number}</td>
                    <td className="px-4 py-2">{c.crime_type}</td>
                    <td className="px-4 py-2">{c.district}</td>
                    <td className="px-4 py-2">{c.incident_date}</td>
                    <td className="px-4 py-2"><PriorityBadge value={c.priority} /></td>
                    <td className="px-4 py-2"><StatusBadge value={c.status} /></td>
                    <td className="px-4 py-2 text-right">
                      <Link to={`/cases/${c.case_id}`} className="text-secondary font-semibold hover:underline">
                        View <Icon name="chevron_right" className="text-sm align-middle" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="flex items-center justify-between px-4 py-3 border-t border-outline-variant text-sm">
              <button
                disabled={offset === 0}
                onClick={() => setOffset(Math.max(0, offset - limit))}
                className="px-3 py-1.5 rounded-md border border-outline-variant disabled:opacity-40"
              >
                Previous
              </button>
              <span className="text-on-surface-variant text-xs">
                Showing {offset + 1}–{Math.min(offset + limit, data?.page.total ?? 0)} of {data?.page.total ?? 0}
              </span>
              <button
                disabled={!data || offset + limit >= data.page.total}
                onClick={() => setOffset(offset + limit)}
                className="px-3 py-1.5 rounded-md border border-outline-variant disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </AppLayout>
  );
}
