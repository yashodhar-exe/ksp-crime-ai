import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { listAuditLogs } from "@/api/audit";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { Icon } from "@/components/ui/Icon";

export default function AuditPage() {
  const { data, loading, error, reload } = useAsync(() => listAuditLogs({ limit: 200 }), []);

  return (
    <AppLayout title="Audit Trail">
      <div className="card overflow-hidden">
        {loading ? (
          <LoadingState label="Loading audit logs..." />
        ) : error ? (
          <ErrorState message={error} onRetry={reload} />
        ) : (
          <table className="data-table w-full text-sm">
            <thead>
              <tr>
                <th className="px-4 py-2">Timestamp</th>
                <th className="px-4 py-2">User</th>
                <th className="px-4 py-2">Action</th>
                <th className="px-4 py-2">Case</th>
                <th className="px-4 py-2">IP Address</th>
              </tr>
            </thead>
            <tbody>
              {data!.map((log) => (
                <tr key={log.log_id} className="border-t border-outline-variant/50">
                  <td className="px-4 py-2 text-xs">{new Date(log.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-2 font-mono text-xs">{log.user_id}</td>
                  <td className="px-4 py-2 flex items-center gap-1.5">
                    <Icon name="history" className="text-sm text-on-surface-variant" />
                    {log.action}
                  </td>
                  <td className="px-4 py-2 font-mono text-xs">{log.case_id ?? "—"}</td>
                  <td className="px-4 py-2 font-mono text-xs">{log.ip_address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  );
}
