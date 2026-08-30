"use client";

import { getPlayerProjection } from "@/lib/api";
import { useAsyncData } from "@/lib/useAsyncData";

export function ProjectionCard({ playerDisplayName }: { playerDisplayName: string | null }) {
  const state = useAsyncData(
    () => getPlayerProjection(playerDisplayName as string),
    playerDisplayName,
  );

  return (
    <div className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h2 className="text-sm font-medium text-zinc-500">Next-Week Projection</h2>

      {state.status === "idle" && (
        <p className="mt-2 text-zinc-400">Select a player to see a projection.</p>
      )}
      {state.status === "loading" && <p className="mt-2 text-zinc-400">Loading...</p>}
      {state.status === "error" && <p className="mt-2 text-red-600">{state.error.message}</p>}
      {state.status === "success" && (
        <p className="mt-2 text-3xl font-semibold">
          {state.data.projected_ppr}{" "}
          <span className="text-base font-normal text-zinc-500">PPR points</span>
        </p>
      )}
    </div>
  );
}
