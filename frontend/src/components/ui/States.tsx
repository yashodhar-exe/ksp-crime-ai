import { Icon } from "./Icon";

export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-2 py-16 text-on-surface-variant">
      <Icon name="progress_activity" className="animate-spin" />
      <span className="text-sm">{label}</span>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-center">
      <Icon name="error" className="text-error text-3xl" />
      <p className="text-sm text-on-surface-variant max-w-sm">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 rounded-md border border-outline-variant text-sm font-semibold text-primary hover:bg-surface-container"
        >
          Retry
        </button>
      )}
    </div>
  );
}

export function EmptyState({ label }: { label: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-16 text-center text-on-surface-variant">
      <Icon name="inbox" className="text-3xl opacity-50" />
      <p className="text-sm">{label}</p>
    </div>
  );
}
