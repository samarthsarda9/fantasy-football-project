"use client";

import { getPlayerProjection } from "@/lib/api";
import { useAsyncData } from "@/lib/useAsyncData";

export function ProjectionCard({ playerDisplayName }: { playerDisplayName: string | null }) {
  const state = useAsyncData(
    () => getPlayerProjection(playerDisplayName as string),
    playerDisplayName,
  );

  return (
    <div className="rounded-xl border border-line border-t-4 border-t-accent bg-surface p-4 shadow-sm transition-shadow hover:shadow-md">
      <h2 className="text-sm font-medium text-ink-secondary">Next-Week Projection</h2>

      {state.status === "idle" && (
        <p className="mt-2 text-muted">Select a player to see a projection.</p>
      )}
      {state.status === "loading" && <p className="mt-2 text-muted">Loading...</p>}
      {state.status === "error" && <p className="mt-2 text-red-600">{state.error.message}</p>}
      {state.status === "success" && (
        <p className="mt-2 text-3xl font-semibold text-accent">
          {state.data.projected_ppr}{" "}
          <span className="text-base font-normal text-ink-secondary">PPR points</span>
        </p>
      )}
    </div>
  );
}
