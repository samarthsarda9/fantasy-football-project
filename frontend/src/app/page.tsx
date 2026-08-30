"use client";

import { useState } from "react";
import { PlayerSelector } from "@/components/PlayerSelector";
import { ProjectionCard } from "@/components/ProjectionCard";
import { RecentStatsCard } from "@/components/RecentStatsCard";
import { ComparisonCard } from "@/components/ComparisonCard";

export default function Home() {
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
  const [playerA, setPlayerA] = useState<string | null>(null);
  const [playerB, setPlayerB] = useState<string | null>(null);

  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col gap-10 px-6 py-12">
      <div className="flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-semibold">Fantasy Football AI Predictor</h1>
          <p className="text-sm text-zinc-500">
            Full-PPR wide receiver projections from this project&apos;s own model.
          </p>
        </div>

        <PlayerSelector label="Wide Receiver" value={selectedPlayer} onChange={setSelectedPlayer} />

        <div className="grid gap-4 sm:grid-cols-2">
          <ProjectionCard playerDisplayName={selectedPlayer} />
          <RecentStatsCard playerDisplayName={selectedPlayer} />
        </div>
      </div>

      <div className="flex flex-col gap-4 border-t border-zinc-200 pt-8 dark:border-zinc-800">
        <h2 className="text-xl font-semibold">Compare Two Players</h2>

        <div className="grid gap-4 sm:grid-cols-2">
          <PlayerSelector label="Player A" value={playerA} onChange={setPlayerA} />
          <PlayerSelector label="Player B" value={playerB} onChange={setPlayerB} />
        </div>

        <ComparisonCard playerA={playerA} playerB={playerB} />
      </div>
    </div>
  );
}
