import { useParams, useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAsync } from "@/hooks/useAsync";
import { getNetworkGraph } from "@/api/network";
import { LoadingState, ErrorState } from "@/components/ui/States";
import { Icon } from "@/components/ui/Icon";

const WIDTH = 640;
const HEIGHT = 480;
const CENTER = { x: WIDTH / 2, y: HEIGHT / 2 };
const RADIUS = 180;

export default function NetworkGraphPage() {
  const { citizenId = "" } = useParams();
  const [lookupValue, setLookupValue] = useState(citizenId);
  const navigate = useNavigate();
  const { data, loading, error, reload } = useAsync(() => getNetworkGraph(citizenId), [citizenId]);

  function handleLookup(e: React.FormEvent) {
    e.preventDefault();
    if (lookupValue.trim()) navigate(`/network/${lookupValue.trim()}`);
  }

  // Radial layout: center node in the middle, all others evenly spaced on a circle.
  const positions = new Map<string, { x: number; y: number }>();
  if (data) {
    positions.set(data.center, CENTER);
    const others = data.nodes.filter((n) => n.id !== data.center);
    others.forEach((n, i) => {
      const angle = (2 * Math.PI * i) / Math.max(others.length, 1);
      positions.set(n.id, {
        x: CENTER.x + RADIUS * Math.cos(angle),
        y: CENTER.y + RADIUS * Math.sin(angle),
      });
    });
  }

  return (
    <AppLayout title="Criminal Network Analysis">
      <form onSubmit={handleLookup} className="card p-4 mb-4 flex gap-2 items-center">
        <Icon name="hub" className="text-primary-container" />
        <input
          value={lookupValue}
          onChange={(e) => setLookupValue(e.target.value)}
          placeholder="Citizen ID, e.g. CID000245"
          className="flex-1 border border-outline-variant rounded-md px-3 py-2 text-sm font-mono"
        />
        <button type="submit" className="bg-primary-container text-on-primary px-5 py-2 rounded-md text-sm font-semibold">
          Load Network
        </button>
      </form>

      {!citizenId ? null : loading ? (
        <LoadingState label="Building network graph..." />
      ) : error ? (
        <ErrorState message={error} onRetry={reload} />
      ) : data && data.nodes.length <= 1 ? (
        <div className="card p-8 text-center text-sm text-on-surface-variant">
          No recorded relationships for this citizen.
        </div>
      ) : (
        <div className="card p-4">
          <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full h-auto">
            {data!.edges.map((e, i) => {
              const s = positions.get(e.source);
              const t = positions.get(e.target);
              if (!s || !t) return null;
              return (
                <g key={i}>
                  <line x1={s.x} y1={s.y} x2={t.x} y2={t.y} stroke="#c6c5d2" strokeWidth={1.5} />
                  <text
                    x={(s.x + t.x) / 2}
                    y={(s.y + t.y) / 2}
                    fontSize={9}
                    fill="#757681"
                    textAnchor="middle"
                  >
                    {e.relationship_type}
                  </text>
                </g>
              );
            })}
            {data!.nodes.map((n) => {
              const pos = positions.get(n.id);
              if (!pos) return null;
              const isCenter = n.id === data!.center;
              return (
                <g
                  key={n.id}
                  className="cursor-pointer"
                  onClick={() => navigate(`/citizens/${n.id}`)}
                >
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={isCenter ? 28 : 20}
                    fill={isCenter ? "#0b1f5e" : "#8b5cf6"}
                    fillOpacity={isCenter ? 1 : 0.85}
                  />
                  <text x={pos.x} y={pos.y + 4} textAnchor="middle" fontSize={10} fill="#ffffff" fontWeight={600}>
                    {n.label.slice(0, 3).toUpperCase()}
                  </text>
                  <text x={pos.x} y={pos.y + (isCenter ? 42 : 34)} textAnchor="middle" fontSize={10} fill="#454650">
                    {n.id}
                  </text>
                </g>
              );
            })}
          </svg>
          <p className="text-xs text-on-surface-variant mt-3 text-center">
            Click a node to open that citizen's profile. Center node ({data!.center}) shown in dark blue.
          </p>
          <div className="flex justify-center mt-2">
            <Link to={`/citizens/${data!.center}`} className="text-secondary text-sm font-semibold hover:underline">
              View center citizen's full profile
            </Link>
          </div>
        </div>
      )}
    </AppLayout>
  );
}
