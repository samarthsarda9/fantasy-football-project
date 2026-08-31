const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type PlayerStats = {
  player_display_name: string;
  season: number;
  week: number;
  opponent_team: string;
  receptions: number;
  targets: number;
  receiving_yards: number;
  receiving_tds: number;
  calculated_ppr: number;
  prev_rolling_3_ppr: number | null;
  prev_season_avg_ppr: number | null;
};

export type PlayerProjection = {
  player_display_name: string;
  projected_ppr: number;
};

export class PlayerNotFoundError extends Error {
  constructor(playerDisplayName: string) {
    super(`Player not found: ${playerDisplayName}`);
    this.name = "PlayerNotFoundError";
  }
}

async function getJson<T>(path: string, playerDisplayName: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (response.status === 404) {
    throw new PlayerNotFoundError(playerDisplayName);
  }
  if (!response.ok) {
    throw new Error(`Request to ${path} failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function listPlayers(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/players`);
  if (!response.ok) {
    throw new Error(`Request to /players failed with status ${response.status}`);
  }
  return response.json() as Promise<string[]>;
}

export async function getPlayerStats(playerDisplayName: string): Promise<PlayerStats> {
  return getJson<PlayerStats>(
    `/players/${encodeURIComponent(playerDisplayName)}`,
    playerDisplayName,
  );
}

export async function getPlayerProjection(
  playerDisplayName: string,
): Promise<PlayerProjection> {
  return getJson<PlayerProjection>(
    `/predictions/${encodeURIComponent(playerDisplayName)}`,
    playerDisplayName,
  );
}

export type AgentAnswer = {
  answer: string;
  trace: string[];
};

export async function askAgent(question: string): Promise<AgentAnswer> {
  const response = await fetch(`${API_BASE_URL}/agent/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error(`Request to /agent/ask failed with status ${response.status}`);
  }

  return response.json() as Promise<AgentAnswer>;
}
