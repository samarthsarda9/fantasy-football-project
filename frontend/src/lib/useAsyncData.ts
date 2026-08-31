"use client";

import { useEffect, useState } from "react";

export type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "success"; data: T };

type Result<T> =
  | { key: string; status: "error"; error: Error }
  | { key: string; status: "success"; data: T };

/**
 * Runs `fetcher` whenever `key` changes, tracking idle/loading/error/success
 * state. `key` doubles as the effect dependency, e.g. a selected player's
 * name, so the fetch reruns when the thing being fetched changes.
 *
 * "loading" is derived (result's key doesn't match the current key yet)
 * rather than set directly in the effect, so a result for an old key that
 * resolves after the user has already moved on is automatically ignored.
 */
export function useAsyncData<T>(fetcher: () => Promise<T>, key: string | null): AsyncState<T> {
  const [result, setResult] = useState<Result<T> | null>(null);

  useEffect(() => {
    if (key === null) return;

    fetcher()
      .then((data) => setResult({ key, status: "success", data }))
      .catch((error: Error) => setResult({ key, status: "error", error }));
    // fetcher is intentionally omitted: callers pass a fresh closure each
    // render, and re-running only when `key` changes is what we want here.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  if (key === null) return { status: "idle" };
  if (result === null || result.key !== key) return { status: "loading" };
  return result;
}
