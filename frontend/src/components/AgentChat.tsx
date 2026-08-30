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
    <div className="flex flex-col gap-3 rounded-xl border border-line bg-surface p-4 shadow-sm">
      <h2 className="text-sm font-medium text-ink-secondary">Ask the Fantasy Analyst</h2>

      <div className="flex flex-col gap-3">
        {messages.length === 0 && (
          <p className="text-sm text-muted">
            Try: &quot;Should I start CeeDee Lamb or Puka Nacua?&quot;
          </p>
        )}

        {messages.map((message, index) => (
          <div key={index}>
            {message.role === "user" && (
              <div className="flex justify-end">
                <p className="max-w-[85%] rounded-2xl rounded-br-sm bg-accent px-3 py-2 text-sm text-white">
                  {message.text}
                </p>
              </div>
            )}
            {message.role === "agent" && (
              <div className="flex justify-start">
                <div className="max-w-[85%] rounded-2xl rounded-bl-sm border-l-4 border-l-secondary bg-background px-3 py-2 text-sm">
                  <p className="whitespace-pre-wrap">{message.text}</p>
                  {message.trace.length > 0 && (
                    <p className="mt-2 inline-flex items-center gap-1 rounded-full bg-secondary/10 px-2 py-0.5 text-xs font-medium text-secondary">
                      Tools used:{" "}
                      {message.trace
                        .filter((line) => line.startsWith("called tool:"))
                        .map((line) => line.replace("called tool: ", ""))
                        .join(", ")}
                    </p>
                  )}
                </div>
              </div>
            )}
            {message.role === "error" && (
              <p className="text-sm text-red-600">{message.text}</p>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex w-fit items-center gap-1 rounded-2xl rounded-bl-sm border-l-4 border-l-secondary bg-background px-3 py-2.5">
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-secondary" />
          </div>
        )}
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
          className="flex-1 rounded-lg border border-line bg-surface px-3 py-2 text-sm outline-none transition-colors focus:border-accent focus:ring-2 focus:ring-accent/30"
          placeholder="Ask a question..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="rounded-full bg-accent px-4 py-2 text-sm font-medium text-white transition-all hover:scale-105 hover:bg-accent-strong active:scale-95 disabled:opacity-50 disabled:hover:scale-100"
          disabled={isLoading || question.trim().length === 0}
        >
          Ask
        </button>
      </form>
    </div>
  );
}
