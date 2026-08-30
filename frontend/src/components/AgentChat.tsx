"use client";

import { useState } from "react";
import { askAgent } from "@/lib/api";

type ChatMessage =
  | { role: "user"; text: string }
  | { role: "agent"; text: string; trace: string[] }
  | { role: "error"; text: string };

export function AgentChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function submit() {
    const trimmed = question.trim();
    if (trimmed.length === 0 || isLoading) return;

    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setQuestion("");
    setIsLoading(true);

    try {
      const result = await askAgent(trimmed);
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: result.answer, trace: result.trace },
      ]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "error", text: (err as Error).message }]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h2 className="text-sm font-medium text-zinc-500">Ask the Fantasy Analyst</h2>

      <div className="flex flex-col gap-3">
        {messages.length === 0 && (
          <p className="text-sm text-zinc-400">
            Try: &quot;Should I start CeeDee Lamb or Puka Nacua?&quot;
          </p>
        )}

        {messages.map((message, index) => (
          <div key={index}>
            {message.role === "user" && (
              <p className="text-sm">
                <span className="font-medium">You: </span>
                {message.text}
              </p>
            )}
            {message.role === "agent" && (
              <div className="rounded bg-zinc-50 p-3 text-sm dark:bg-zinc-900">
                <p className="whitespace-pre-wrap">{message.text}</p>
                {message.trace.length > 0 && (
                  <p className="mt-2 text-xs text-zinc-400">
                    Tools used:{" "}
                    {message.trace
                      .filter((line) => line.startsWith("called tool:"))
                      .map((line) => line.replace("called tool: ", ""))
                      .join(", ")}
                  </p>
                )}
              </div>
            )}
            {message.role === "error" && <p className="text-sm text-red-600">{message.text}</p>}
          </div>
        ))}

        {isLoading && <p className="text-sm text-zinc-400">Thinking...</p>}
      </div>

      <form
        className="flex gap-2"
        onSubmit={(event) => {
          event.preventDefault();
          submit();
        }}
      >
        <input
          type="text"
          className="flex-1 rounded border border-zinc-300 bg-white px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          placeholder="Ask a question..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="rounded bg-zinc-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
          disabled={isLoading || question.trim().length === 0}
        >
          Ask
        </button>
      </form>
    </div>
  );
}
