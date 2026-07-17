import { useParams, Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { getCitizen, getCitizenCases, getCitizenRelationships, getCitizenAssets } from "@/api/citizens";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { StatusBadge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";

export default function CitizenProfilePage() {
  const { citizenId = "" } = useParams();
  const citizen = useAsync(() => getCitizen(citizenId), [citizenId]);
  const cases = useAsync(() => getCitizenCases(citizenId), [citizenId]);
  const relationships = useAsync(() => getCitizenRelationships(citizenId), [citizenId]);
  const assets = useAsync(() => getCitizenAssets(citizenId), [citizenId]);

  if (citizen.loading) return <AppLayout title="Citizen Profile"><LoadingState /></AppLayout>;
  if (citizen.error) return <AppLayout title="Citizen Profile"><ErrorState message={citizen.error} onRetry={citizen.reload} /></AppLayout>;
  const p = citizen.data!;

  return (
    <AppLayout title="Citizen 360 Profile">
      <div className="card p-5 mb-6 flex items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center text-xl font-bold">
          {p.first_name[0]}{p.last_name[0]}
        </div>
        <div className="flex-1">
          <h2 className="text-lg font-bold text-on-surface">{p.first_name} {p.last_name}</h2>
          <p className="text-sm text-on-surface-variant">
            {p.gender} · {p.age} yrs · {p.city}, {p.district}
          </p>
          <p className="text-xs text-on-surface-variant font-mono mt-1">{p.citizen_id}</p>
        </div>
        <Link
          to={`/network/${p.citizen_id}`}
          className="flex items-center gap-1.5 px-4 py-2 rounded-md border border-outline-variant text-sm font-semibold text-primary hover:bg-surface-container"
        >
          <Icon name="hub" className="text-base" /> View Network
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Associated Cases</h3>
            {cases.loading ? <LoadingState /> : cases.error ? <ErrorState message={cases.error} /> : cases.data!.length === 0 ? (
              <p className="text-sm text-on-surface-variant">No case involvement on file.</p>
            ) : (
              <ul className="divide-y divide-outline-variant">
                {cases.data!.map((c) => (
                  <li key={c.case_id} className="py-2.5 flex items-center justify-between">
                    <div>
                      <Link to={`/cases/${c.case_id}`} className="text-sm font-mono text-secondary hover:underline">{c.fir_number}</Link>
                      <p className="text-xs text-on-surface-variant">{c.crime_type}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="badge-pill bg-surface-container text-on-surface-variant">{c.role}</span>
                      <StatusBadge value={c.status} />
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Known Relationships</h3>
            {relationships.loading ? <LoadingState /> : relationships.error ? <ErrorState message={relationships.error} /> : relationships.data!.length === 0 ? (
              <p className="text-sm text-on-surface-variant">No recorded criminal relationships.</p>
            ) : (
              <ul className="space-y-2 text-sm">
                {relationships.data!.map((r) => {
                  const other = r.citizen_1 === citizenId ? r.citizen_2 : r.citizen_1;
                  return (
                    <li key={r.relationship_id} className="flex justify-between">
                      <Link to={`/citizens/${other}`} className="text-secondary hover:underline font-mono text-xs">{other}</Link>
                      <span className="text-xs text-on-surface-variant">{r.relationship_type}</span>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="card p-4 text-sm space-y-2">
            <h3 className="text-sm font-semibold text-on-surface mb-2">Contact</h3>
            <div className="flex justify-between"><span className="text-on-surface-variant">Phone</span><span className="font-mono">{p.phone}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Email</span><span>{p.email ?? "—"}</span></div>
            <div className="flex justify-between"><span className="text-on-surface-variant">Address</span><span className="text-right">{p.address ?? "—"}</span></div>
          </div>

          <div className="card p-4">
            <h3 className="text-sm font-semibold text-on-surface mb-3">Assets</h3>
            {assets.loading ? <LoadingState /> : assets.error ? <ErrorState message={assets.error} /> : (
              <div className="space-y-4 text-sm">
                <div>
                  <p className="text-xs font-semibold text-on-surface-variant uppercase mb-1">Phones</p>
                  {assets.data!.phones.map((ph) => <p key={ph.phone_id} className="font-mono text-xs">{ph.phone_number}</p>)}
                </div>
                <div>
                  <p className="text-xs font-semibold text-on-surface-variant uppercase mb-1">Vehicles</p>
                  {assets.data!.vehicles.map((v) => <p key={v.vehicle_id} className="font-mono text-xs">{v.vehicle_number} ({v.vehicle_type})</p>)}
                </div>
                <div>
                  <p className="text-xs font-semibold text-on-surface-variant uppercase mb-1">Bank Accounts</p>
                  {assets.data!.bank_accounts.map((b) => <p key={b.account_id} className="font-mono text-xs">{b.bank_name} · {b.account_number}</p>)}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
