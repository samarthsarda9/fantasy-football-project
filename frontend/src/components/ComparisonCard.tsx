"use client";

import { getPlayerProjection, type PlayerProjection } from "@/lib/api";
import { useAsyncData, type AsyncState } from "@/lib/useAsyncData";

function ProjectionStatus({
  label,
  state,
  isWinner,
}: {
  label: string;
  state: AsyncState<PlayerProjection>;
  isWinner: boolean;
}) {
  return (
    <div className={`rounded-lg p-2 transition-colors ${isWinner ? "bg-good/10" : ""}`}>
      <h3 className="text-xs font-medium tracking-wide text-muted uppercase">{label}</h3>
      {state.status === "idle" && <p className="text-muted">Select a player.</p>}
      {state.status === "loading" && <p className="text-muted">Loading...</p>}
      {state.status === "error" && <p className="text-red-600">{state.error.message}</p>}
      {state.status === "success" && (
        <>
          <p className={`text-2xl font-semibold ${isWinner ? "text-good" : ""}`}>
            {state.data.projected_ppr}{" "}
            <span className="text-sm font-normal text-muted">PPR</span>
          </p>
          {isWinner && (
            <p className="mt-1 flex items-center gap-1 text-xs font-medium text-good">
              <span aria-hidden="true">▲</span> Better start
            </p>
          )}
        </>
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
  let winner: "A" | "B" | null = null;
  if (stateA.status === "success" && stateB.status === "success") {
    const a = stateA.data;
    const b = stateB.data;
    if (a.projected_ppr === b.projected_ppr) {
      recommendation = `${a.player_display_name} and ${b.player_display_name} have the same projection: ${a.projected_ppr} PPR points each.`;
    } else {
      winner = a.projected_ppr > b.projected_ppr ? "A" : "B";
      const [higher, lower] = a.projected_ppr > b.projected_ppr ? [a, b] : [b, a];
      recommendation = `Start ${higher.player_display_name} (${higher.projected_ppr} PPR) over ${lower.player_display_name} (${lower.projected_ppr} PPR).`;
    }
  }

  return (
    <div className="rounded-xl border border-line bg-surface p-4 shadow-sm">
      <h2 className="text-sm font-medium text-ink-secondary">Start/Sit Comparison</h2>
      <div className="mt-2 grid grid-cols-2 gap-4">
        <ProjectionStatus label="Player A" state={stateA} isWinner={winner === "A"} />
        <ProjectionStatus label="Player B" state={stateB} isWinner={winner === "B"} />
      </div>
      {recommendation && (
        <p className="mt-4 rounded-lg bg-accent/10 p-3 text-sm font-medium text-accent">
          {recommendation}
        </p>
      )}
    </div>
  );
}
