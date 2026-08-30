"use client";

import { useEffect, useMemo, useState } from "react";
import { listPlayers } from "@/lib/api";

export function PlayerSelector({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string | null;
  onChange: (playerDisplayName: string) => void;
}) {
  const [players, setPlayers] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState(value ?? "");
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Keep the text box in sync if `value` changes from outside this input.
  // Adjusted during render (React's recommended pattern for this) rather
  // than in an effect, so there's no extra render and no setState-in-effect.
  const [prevValue, setPrevValue] = useState(value);
  if (value !== prevValue) {
    setPrevValue(value);
    setInputValue(value ?? "");
  }

  useEffect(() => {
    listPlayers()
      .then(setPlayers)
      .catch((err: Error) => setError(err.message));
  }, []);

  const suggestions = useMemo(() => {
    const query = inputValue.trim().toLowerCase();
    if (!players || query.length === 0) return [];

    // Rank names that start with the query above names that merely contain
    // it, so typing "g" surfaces "Garrett Wilson" before "Casey Washington".
    const startsWith: string[] = [];
    const contains: string[] = [];
    for (const name of players) {
      const lower = name.toLowerCase();
      if (lower.startsWith(query)) startsWith.push(name);
      else if (lower.includes(query)) contains.push(name);
    }
    return [...startsWith, ...contains].slice(0, 8);
  }, [players, inputValue]);

  if (error) {
    return <p className="text-sm text-red-600">Could not load players: {error}</p>;
  }

  function submit(name: string) {
    const trimmed = name.trim();
    if (trimmed.length > 0) onChange(trimmed);
    setShowSuggestions(false);
  }

  const inputId = `player-input-${label.replace(/\s+/g, "-")}`;

  return (
    <div className="relative flex flex-col gap-1 text-sm">
      <label className="font-medium text-zinc-700 dark:text-zinc-300" htmlFor={inputId}>
        {label}
      </label>
      <input
        id={inputId}
        type="text"
        autoComplete="off"
        className="rounded border border-zinc-300 bg-white px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
        placeholder={players === null ? "Loading players..." : "Type a player name..."}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value);
          setShowSuggestions(true);
        }}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => submit(inputValue)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            submit(inputValue);
          }
          if (event.key === "Escape") setShowSuggestions(false);
        }}
        disabled={players === null}
      />

      {showSuggestions && suggestions.length > 0 && (
        <ul className="absolute top-full z-10 mt-1 max-h-56 w-full overflow-y-auto rounded border border-zinc-300 bg-white shadow-lg dark:border-zinc-700 dark:bg-zinc-900">
          {suggestions.map((name) => (
            <li
              key={name}
              className="cursor-pointer px-3 py-2 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              // onMouseDown (not onClick) fires before the input's onBlur, and
              // preventDefault stops the blur from happening at all, so we can
              // select a suggestion without it getting submitted as a typo first.
              onMouseDown={(event) => {
                event.preventDefault();
                setInputValue(name);
                submit(name);
              }}
            >
              {name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
