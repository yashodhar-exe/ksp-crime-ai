interface BadgeProps {
  value: string;
}

const PRIORITY_CLASS: Record<string, string> = {
  Critical: "badge-high",
  High: "badge-high",
  Medium: "badge-medium",
  Low: "badge-low",
};

export function PriorityBadge({ value }: BadgeProps) {
  const cls = PRIORITY_CLASS[value] ?? "text-on-surface-variant font-medium text-xs px-2";
  return <span className={cls}>{value}</span>;
}

const STATUS_CLASS: Record<string, string> = {
  Open: "badge-pill bg-blue-50 text-blue-700",
  "Under Investigation": "text-amber-700 font-medium text-xs px-2",
  Closed: "badge-pill bg-slate-100 text-slate-600",
  Resolved: "badge-pill bg-green-50 text-green-700",
  Pending: "badge-pill bg-amber-50 text-amber-700",
};

export function StatusBadge({ value }: BadgeProps) {
  const cls = STATUS_CLASS[value] ?? "text-on-surface-variant font-medium text-xs px-2";
  return <span className={cls}>{value}</span>;
}
