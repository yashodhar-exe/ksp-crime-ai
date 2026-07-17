import { useParams, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import {
  getCase, getCaseSuspects, getCaseVictims, getCaseEvidence,
  getCaseDigitalEvidence, getCaseNotes, getCaseTimeline, getSimilarCases,
} from "@/api/cases";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge, PriorityBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";

export default function CaseDetailPage() {
  const { caseId = "" } = useParams();

  const caseQ = useAsync(() => getCase(caseId), [caseId]);
  const suspects = useAsync(() => getCaseSuspects(caseId), [caseId]);
  const victims = useAsync(() => getCaseVictims(caseId), [caseId]);
  const evidence = useAsync(() => getCaseEvidence(caseId), [caseId]);
  const digitalEvidence = useAsync(() => getCaseDigitalEvidence(caseId), [caseId]);
  const notes = useAsync(() => getCaseNotes(caseId), [caseId]);
  const timeline = useAsync(() => getCaseTimeline(caseId), [caseId]);
  const similar = useAsync(() => getSimilarCases(caseId), [caseId]);

  if (caseQ.loading) return <AppLayout title="Case Details"><LoadingState label="Loading case..." /></AppLayout>;
  if (caseQ.error) return <AppLayout title="Case Details"><ErrorState message={caseQ.error} onRetry={caseQ.reload} /></AppLayout>;
  const c = caseQ.data!;

  return (
    <AppLayout title={`Case ${c.fir_number}`}>
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h2 className="text-xl font-bold text-on-surface font-mono">{c.fir_number}</h2>
            <PriorityBadge value={c.priority} />
            <StatusBadge value={c.status} />
          </div>
          <p className="text-sm text-on-surface-variant">
            {c.crime_type} · {c.city}, {c.district} · Reported {c.registered_date}
          </p>
        </div>
        <Link to="/cases" className="text-sm text-secondary font-semibold flex items-center gap-1">
          <Icon name="arrow_back" className="text-sm" /> Back to Cases
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-2">Complaint Narrative</h3>
            <p className="text-sm text-on-surface-variant leading-relaxed">{c.complaint_text}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Suspects ({suspects.data?.length ?? "…"})</h3>
              {suspects.loading ? <LoadingState /> : suspects.error ? <ErrorState message={suspects.error} /> : (
                <ul className="space-y-2 text-sm">
                  {suspects.data!.map((s) => (
                    <li key={s.suspect_id} className="flex justify-between">
                      <Link to={`/citizens/${s.citizen_id}`} className="text-secondary hover:underline font-mono text-xs">{s.citizen_id}</Link>
                      <span className="text-xs text-on-surface-variant">{s.role} · {s.arrest_status}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Victims ({victims.data?.length ?? "…"})</h3>
              {victims.loading ? <LoadingState /> : victims.error ? <ErrorState message={victims.error} /> : (
                <ul className="space-y-2 text-sm">
                  {victims.data!.map((v) => (
                    <li key={v.victim_id} className="flex justify-between">
                      <Link to={`/citizens/${v.citizen_id}`} className="text-secondary hover:underline font-mono text-xs">{v.citizen_id}</Link>
                      <span className="text-xs text-on-surface-variant">{v.injury_level}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Timeline</h3>
            {timeline.loading ? <LoadingState /> : timeline.error ? <ErrorState message={timeline.error} /> : (
              <ol className="relative border-l border-outline-variant ml-2 space-y-4">
                {timeline.data!.map((t) => (
                  <li key={t.event_id} className="ml-4">
                    <div className="absolute w-2 h-2 bg-primary-container rounded-full -left-[4.5px] mt-1.5" />
                    <p className="text-sm text-on-surface">{t.event}</p>
                  </li>
                ))}
              </ol>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Evidence</h3>
              {evidence.loading ? <LoadingState /> : evidence.error ? <ErrorState message={evidence.error} /> : (
                <ul className="space-y-2 text-sm">
                  {evidence.data!.map((e) => (
                    <li key={e.evidence_id} className="flex justify-between">
                      <span>{e.evidence_type}</span>
                      <span className="text-xs text-on-surface-variant">{e.status}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-on-surface mb-3">Digital Evidence</h3>
              {digitalEvidence.loading ? <LoadingState /> : digitalEvidence.error ? <ErrorState message={digitalEvidence.error} /> : (
                <ul className="space-y-2 text-sm">
                  {digitalEvidence.data!.map((d) => (
                    <li key={d.digital_evidence_id}>
                      <p className="font-medium">{d.file_type} {d.file_name ? `· ${d.file_name}` : ""}</p>
                      {d.extracted_entities && (
                        <p className="text-xs text-on-surface-variant font-mono">{d.extracted_entities}</p>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Investigation Notes</h3>
            {notes.loading ? <LoadingState /> : notes.error ? <ErrorState message={notes.error} /> : (
              <ul className="space-y-3 text-sm">
                {notes.data!.map((n) => (
                  <li key={n.note_id} className="border-l-2 border-outline-variant pl-3">
                    <p className="text-on-surface">{n.note}</p>
                    <p className="text-xs text-on-surface-variant mt-1">Officer {n.officer_id}</p>
                  </li>
                ))}
              </ul>
            )}
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
                  <li key={s.case_id}>
                    <Link to={`/cases/${s.case_id}`} className="text-sm font-mono text-secondary hover:underline">
                      {s.fir_number}
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
            <div className="flex justify-between"><span className="text-on-surface-variant">Station</span><span>{c.station_id}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Officer</span><span>{c.officer_id}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Estimated Loss</span><span>₹{c.estimated_loss.toLocaleString()}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Pattern</span><span>{c.pattern_id ?? "—"}</span></div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
