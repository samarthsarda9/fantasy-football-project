"use client";

import { getPlayerStats } from "@/lib/api";
import { useAsyncData } from "@/lib/useAsyncData";

export function RecentStatsCard({ playerDisplayName }: { playerDisplayName: string | null }) {
  const state = useAsyncData(
    () => getPlayerStats(playerDisplayName as string),
    playerDisplayName,
  );

  return (
    <div className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h2 className="text-sm font-medium text-zinc-500">Most Recent Game</h2>

      {state.status === "idle" && (
        <p className="mt-2 text-zinc-400">Select a player to see recent stats.</p>
      )}
      {state.status === "loading" && <p className="mt-2 text-zinc-400">Loading...</p>}
      {state.status === "error" && <p className="mt-2 text-red-600">{state.error.message}</p>}
      {state.status === "success" && (
        <dl className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
          <dt className="text-zinc-500">Week</dt>
          <dd>
            {state.data.season} · Week {state.data.week} vs {state.data.opponent_team}
          </dd>

          <dt className="text-zinc-500">Receptions / Targets</dt>
          <dd>
            {state.data.receptions} / {state.data.targets}
          </dd>

          <dt className="text-zinc-500">Receiving Yards</dt>
          <dd>{state.data.receiving_yards}</dd>

          <dt className="text-zinc-500">Receiving TDs</dt>
          <dd>{state.data.receiving_tds}</dd>

          <dt className="text-zinc-500">Full-PPR Points</dt>
          <dd>{state.data.calculated_ppr}</dd>

          <dt className="text-zinc-500">Prior 3-Game Avg</dt>
          <dd>{state.data.prev_rolling_3_ppr ?? "N/A"}</dd>

          <dt className="text-zinc-500">Season Avg (before this game)</dt>
          <dd>{state.data.prev_season_avg_ppr ?? "N/A"}</dd>
        </dl>
      )}
    </div>
  );
}
