"use client";

import { getPlayerProjection, type PlayerProjection } from "@/lib/api";
import { useAsyncData, type AsyncState } from "@/lib/useAsyncData";

function ProjectionStatus({
  label,
  state,
}: {
  label: string;
  state: AsyncState<PlayerProjection>;
}) {
  return (
    <div>
      <h3 className="text-xs font-medium uppercase tracking-wide text-zinc-500">{label}</h3>
      {state.status === "idle" && <p className="text-zinc-400">Select a player.</p>}
      {state.status === "loading" && <p className="text-zinc-400">Loading...</p>}
      {state.status === "error" && <p className="text-red-600">{state.error.message}</p>}
      {state.status === "success" && (
        <p className="text-2xl font-semibold">
          {state.data.projected_ppr} <span className="text-sm font-normal text-zinc-500">PPR</span>
        </p>
      )}
    </div>
  );
}

export function ComparisonCard({
  playerA,
  playerB,
}: {
  playerA: string | null;
  playerB: string | null;
}) {
  const stateA = useAsyncData(() => getPlayerProjection(playerA as string), playerA);
  const stateB = useAsyncData(() => getPlayerProjection(playerB as string), playerB);

  // The comparison itself (which projection is bigger) is deterministic, so
  // it's computed here in plain JS once both projections are in, the same
  // way the agent's compare_players tool does it in Python rather than
  // leaving an LLM to eyeball two numbers.
  let recommendation: string | null = null;
  if (stateA.status === "success" && stateB.status === "success") {
    const a = stateA.data;
    const b = stateB.data;
    if (a.projected_ppr === b.projected_ppr) {
      recommendation = `${a.player_display_name} and ${b.player_display_name} have the same projection: ${a.projected_ppr} PPR points each.`;
    } else {
      const [higher, lower] = a.projected_ppr > b.projected_ppr ? [a, b] : [b, a];
      recommendation = `Start ${higher.player_display_name} (${higher.projected_ppr} PPR) over ${lower.player_display_name} (${lower.projected_ppr} PPR).`;
    }
  }

  return (
    <div className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h2 className="text-sm font-medium text-zinc-500">Start/Sit Comparison</h2>
      <div className="mt-2 grid grid-cols-2 gap-4">
        <ProjectionStatus label="Player A" state={stateA} />
        <ProjectionStatus label="Player B" state={stateB} />
      </div>
      {recommendation && (
        <p className="mt-4 rounded bg-zinc-50 p-3 text-sm font-medium dark:bg-zinc-900">
          {recommendation}
        </p>
      )}
    </div>
  );
}
