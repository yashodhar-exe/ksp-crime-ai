import { useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { searchEntity } from "@/api/search";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/States";
import { Icon } from "@/components/ui/Icon";

const ENTITY_TYPES = ["Citizen", "Phone", "Vehicle", "Bank", "Officer", "Case"];

export default function SearchPage() {
  const [params, setParams] = useSearchParams();
  const [value, setValue] = useState(params.get("q") ?? "");
  const [entityType, setEntityType] = useState("");
  const [submitted, setSubmitted] = useState(params.get("q") ?? "");

  const { data, loading, error, reload } = useAsync(
    () => searchEntity(submitted, entityType || undefined),
    [submitted, entityType]
  );

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitted(value);
    setParams(value ? { q: value } : {});
  }

  return (
    <AppLayout title="Unified Intelligence Search">
      <form onSubmit={handleSubmit} className="card p-4 mb-4 flex flex-wrap gap-3 items-center">
        <div className="relative flex-1 min-w-[280px]">
          <Icon name="search" className="absolute left-3 top-1/2 -translate-y-1/2 text-outline" />
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Phone number, vehicle number, account number, FIR, citizen ID"
            className="w-full pl-10 pr-3 py-2.5 border border-outline-variant rounded-md text-sm"
          />
        </div>
        <select
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
          className="border border-outline-variant rounded-md text-sm px-3 py-2.5"
        >
          <option value="">Any Entity Type</option>
          {ENTITY_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <button type="submit" className="bg-primary-container text-on-primary px-5 py-2.5 rounded-md text-sm font-semibold">
          Search
        </button>
      </form>

      {!submitted ? (
        <EmptyState label="Enter a value to search across citizens, phones, vehicles, bank accounts, officers, and cases." />
      ) : loading ? (
        <LoadingState label="Searching..." />
      ) : error ? (
        <ErrorState message={error} onRetry={reload} />
      ) : data && data.results.length === 0 ? (
        <EmptyState label={`No results for "${submitted}".`} />
      ) : (
        <div className="card overflow-hidden">
          <table className="data-table w-full text-sm">
            <thead>
              <tr>
                <th className="px-4 py-2">Entity Type</th>
                <th className="px-4 py-2">Value</th>
                <th className="px-4 py-2">Linked Case</th>
                <th className="px-4 py-2">Crime Type</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2"></th>
              </tr>
            </thead>
            <tbody>
              {data?.results.map((r, i) => (
                <tr key={i} className="border-t border-outline-variant/50">
                  <td className="px-4 py-2">{r.entity_type}</td>
                  <td className="px-4 py-2 font-mono text-xs">{r.entity_value}</td>
                  <td className="px-4 py-2 font-mono text-xs">{r.fir_number ?? r.case_id}</td>
                  <td className="px-4 py-2">{r.crime_type ?? "—"}</td>
                  <td className="px-4 py-2">{r.status ?? "—"}</td>
                  <td className="px-4 py-2 text-right">
                    <Link to={`/cases/${r.case_id}`} className="text-secondary font-semibold hover:underline">
                      Open Case
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </AppLayout>
  );
}
