"use client";

import { useState } from "react";
import { PlayerSelector } from "@/components/PlayerSelector";
import { ProjectionCard } from "@/components/ProjectionCard";
import { RecentStatsCard } from "@/components/RecentStatsCard";
import { ComparisonCard } from "@/components/ComparisonCard";
import { AgentChat } from "@/components/AgentChat";

function SectionHeading({ children, dotColor }: { children: string; dotColor: string }) {
  return (
    <h2 className="flex items-center gap-2 text-xl font-semibold">
      <span className={`h-2.5 w-2.5 rounded-full ${dotColor}`} />
      {children}
    </h2>
  );
}

export default function Home() {
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
  const [playerA, setPlayerA] = useState<string | null>(null);
  const [playerB, setPlayerB] = useState<string | null>(null);

  return (
    <div className="relative overflow-hidden">
      {/* Decorative color glow - purely visual, sits behind the content */}
      <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-32 -left-24 h-80 w-80 rounded-full bg-accent/20 blur-3xl" />
        <div className="absolute top-40 -right-24 h-80 w-80 rounded-full bg-secondary/20 blur-3xl" />
      </div>

      <div className="mx-auto flex min-h-screen max-w-2xl flex-col gap-10 px-6 py-12">
        <div className="flex flex-col gap-6">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-accent/10 px-3 py-1 text-xs font-medium text-accent">
              AI-Powered Projections
            </span>
            <h1 className="mt-3 bg-linear-to-r from-accent to-secondary bg-clip-text text-3xl font-bold text-transparent">
              Fantasy Football AI Predictor
            </h1>
            <p className="mt-1 text-sm text-ink-secondary">
              Full-PPR wide receiver projections from this project&apos;s own model.
            </p>
          </div>

          <PlayerSelector label="Wide Receiver" value={selectedPlayer} onChange={setSelectedPlayer} />

          <div className="grid gap-4 sm:grid-cols-2">
            <ProjectionCard playerDisplayName={selectedPlayer} />
            <RecentStatsCard playerDisplayName={selectedPlayer} />
          </div>
        </div>

        <div className="flex flex-col gap-4 border-t border-line pt-8">
          <SectionHeading dotColor="bg-accent">Compare Two Players</SectionHeading>

          <div className="grid gap-4 sm:grid-cols-2">
            <PlayerSelector label="Player A" value={playerA} onChange={setPlayerA} />
            <PlayerSelector label="Player B" value={playerB} onChange={setPlayerB} />
          </div>

          <ComparisonCard playerA={playerA} playerB={playerB} />
        </div>

        <div className="flex flex-col gap-4 border-t border-line pt-8">
          <SectionHeading dotColor="bg-secondary">Ask the Agent</SectionHeading>
          <AgentChat />
        </div>
      </div>
    </div>
  );
}
