import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Icon } from "@/components/ui/Icon";
import { useAuth } from "@/context/AuthContext";
import { getRole } from "@/types/roles";

export function Topbar({ title }: { title: string }) {
  const { user } = useAuth();
  const role = getRole(user?.role_id);
  const navigate = useNavigate();
  const [query, setQuery] = useState("");

  function handleSearchSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  }

  return (
    <header className="h-16 border-b border-outline-variant bg-white flex items-center justify-between px-6 sticky top-0 z-40">
      <h1 className="text-lg font-bold text-on-surface">{title}</h1>

      <div className="flex items-center gap-4">
        <form onSubmit={handleSearchSubmit} className="relative hidden md:block">
          <Icon
            name="search"
            className="absolute left-3 top-1/2 -translate-y-1/2 text-outline text-lg"
          />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search phone, FIR, citizen..."
            className="pl-10 pr-3 py-2 w-72 rounded-md border border-outline-variant text-sm focus:outline-none focus:ring-2 focus:ring-secondary"
          />
        </form>

        <button className="text-on-surface-variant hover:text-primary transition-colors" title="Notifications">
          <Icon name="notifications" />
        </button>

        <div className="flex items-center gap-2 pl-4 border-l border-outline-variant">
          <div className="w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center text-xs font-bold uppercase">
            {user?.username?.slice(0, 2) ?? "??"}
          </div>
          <div className="leading-tight hidden sm:block">
            <p className="text-xs font-semibold text-on-surface">{user?.username}</p>
            <p className="text-[11px] text-on-surface-variant">{role?.role_name ?? "Unknown role"}</p>
          </div>
        </div>
      </div>
    </header>
  );
}
