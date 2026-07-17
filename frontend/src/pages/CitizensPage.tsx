import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { Icon } from "@/components/ui/Icon";

export default function CitizensPage() {
  const [citizenId, setCitizenId] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (citizenId.trim()) navigate(`/citizens/${citizenId.trim()}`);
  }

  return (
    <AppLayout title="Citizens Module">
      <div className="card p-8 max-w-lg mx-auto text-center mt-12">
        <Icon name="person_search" className="text-4xl text-primary-container mb-3" />
        <h2 className="text-lg font-bold text-on-surface mb-1">Look up a Citizen</h2>
        <p className="text-sm text-on-surface-variant mb-6">
          The backend exposes citizen lookup by ID (e.g. from search results or a case's suspect/victim
          list) rather than a full citizen directory — enter a citizen ID to open their 360° profile.
        </p>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            value={citizenId}
            onChange={(e) => setCitizenId(e.target.value)}
            placeholder="e.g. CID000245"
            className="flex-1 border border-outline-variant rounded-md px-3 py-2 text-sm font-mono"
          />
          <button type="submit" className="bg-primary-container text-on-primary px-5 py-2 rounded-md text-sm font-semibold">
            Open Profile
          </button>
        </form>
        <p className="text-xs text-on-surface-variant mt-4">
          Tip: use <span className="font-mono">Unified Intelligence Search</span> to find a citizen by phone,
          vehicle, or bank account first.
        </p>
      </div>
    </AppLayout>
  );
}
