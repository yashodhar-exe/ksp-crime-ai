import { useParams, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import {
  getCase, getSimilarCases,
} from "@/api/cases";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import type { Accused, Victim } from "@/types/api";

export default function CaseDetailPage() {
  const { caseId = "" } = useParams();

  const caseQ = useAsync(() => getCase(caseId), [caseId]);
  const similar = useAsync(() => getSimilarCases(caseId), [caseId]);

  if (caseQ.loading) return <AppLayout title="Case Details"><LoadingState label="Loading case..." /></AppLayout>;
  if (caseQ.error) return <AppLayout title="Case Details"><ErrorState message={caseQ.error} onRetry={caseQ.reload} /></AppLayout>;
  const c = caseQ.data!;

  return (
    <AppLayout title={`Case ${c.crime_no}`}>
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h2 className="text-xl font-bold text-on-surface font-mono">{c.crime_no}</h2>
            <PriorityBadge value={c.gravity_name ?? "Unknown"} />
            <StatusBadge value={c.case_status_name ?? "Unknown"} />
          </div>
          <p className="text-sm text-on-surface-variant">
            {c.crime_head_name} · {c.district_name} · Reported {c.crime_registered_date}
          </p>
        </div>
        <Link to="/cases" className="text-sm text-secondary font-semibold flex items-center gap-1">
          <Icon name="arrow_back" className="text-sm" /> Back to Cases
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-2">Brief Facts</h3>
            <p className="text-sm text-on-surface-variant leading-relaxed">{c.brief_facts}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Accused ({c.accused?.length ?? "0"})</h3>
                <ul className="space-y-2 text-sm">
                  {c.accused?.map((a: Accused) => (
                    <li key={a.accused_master_id} className="flex justify-between">
                      <span className="font-medium text-xs">{a.accused_name}</span>
                      <span className="text-xs text-on-surface-variant">Age: {a.age_year ?? "Unknown"}</span>
                    </li>
                  ))}
                </ul>
            </div>
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Victims ({c.victims?.length ?? "0"})</h3>
                <ul className="space-y-2 text-sm">
                  {c.victims?.map((v: Victim) => (
                    <li key={v.victim_master_id} className="flex justify-between">
                      <span className="font-medium text-xs">{v.victim_name}</span>
                      <span className="text-xs text-on-surface-variant">Age: {v.age_year ?? "Unknown"}</span>
                    </li>
                  ))}
                </ul>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="ai-panel p-4">
            <div className="flex items-center gap-2 mb-3">
              <Icon name="auto_awesome" className="text-ai-accent" />
              <h3 className="text-sm font-semibold text-on-surface">Similar Cases</h3>
            </div>
            {similar.loading ? <LoadingState /> : similar.error ? (
              <ErrorState message={similar.error} />
            ) : similar.data!.length === 0 ? (
              <p className="text-xs text-on-surface-variant">No similar cases found for this pattern.</p>
            ) : (
              <ul className="space-y-3">
                {similar.data!.map((s) => (
                  <li key={s.case_master_id}>
                    <Link to={`/cases/${s.case_master_id}`} className="text-sm font-mono text-secondary hover:underline">
                      {s.crime_no}
                    </Link>
                    <p className="text-xs text-on-surface-variant">{s.similarity_reason}</p>
                  </li>
                ))}
              </ul>
            )}
            <p className="text-[11px] text-on-surface-variant mt-3 pt-3 border-t border-outline-variant">
              Matched via crime_type + pattern_id, not a trained ML model — see AI Readiness notes in the project README.
            </p>
          </div>

          <div className="card p-4 text-sm space-y-2">
            <h3 className="text-sm font-semibold text-on-surface mb-2">Case Metadata</h3>
            <div className="flex justify-between"><span className="text-on-surface-variant">Station</span><span>{c.police_station_name ?? c.police_station_id}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Officer</span><span>{c.police_person_id}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Court</span><span>{c.court_name ?? c.court_id ?? "—"}</span></div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
