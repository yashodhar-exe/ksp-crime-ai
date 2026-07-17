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
  const cls = PRIORITY_CLASS[value] ?? "badge-pill bg-surface-container text-on-surface-variant";
  return <span className={cls}>{value}</span>;
}

const STATUS_CLASS: Record<string, string> = {
  Open: "badge-pill bg-blue-50 text-blue-700",
  "Under Investigation": "badge-pill bg-amber-50 text-amber-700",
  Closed: "badge-pill bg-slate-100 text-slate-600",
  Resolved: "badge-pill bg-green-50 text-green-700",
  Pending: "badge-pill bg-amber-50 text-amber-700",
};

export function StatusBadge({ value }: BadgeProps) {
  const cls = STATUS_CLASS[value] ?? "badge-pill bg-surface-container text-on-surface-variant";
  return <span className={cls}>{value}</span>;
}
