import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { sendChatQuery, exportChat } from "@/api/chat";
import { Icon } from "@/components/ui/Icon";
import type { ChatSource } from "@/types/api";

interface DisplayMessage {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}

export default function AssistantPage() {
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || sending) return;
    const question = input.trim();
    setMessages((m) => [...m, { role: "user", content: question }]);
    setInput("");
    setSending(true);
    setError(null);
    try {
      const res = await sendChatQuery(question, sessionId);
      setSessionId(res.session_id);
      setMessages((m) => [...m, { role: "assistant", content: res.answer, sources: res.sources }]);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? "The assistant couldn't process that. Please try again.");
    } finally {
      setSending(false);
    }
  }

  async function handleExport() {
    if (!sessionId) return;
    const blob = await exportChat(sessionId);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ksp-conversation-${sessionId}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <AppLayout title="AI Investigation Assistant">
      <div className="card flex flex-col h-[calc(100vh-8rem)]">
        <div className="flex items-center justify-between px-4 py-3 border-b border-outline-variant">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-on-surface">Investigation Copilot</h2>
          </div>
          <button
            onClick={handleExport}
            disabled={!sessionId}
            className="text-xs font-semibold text-secondary flex items-center gap-1 disabled:opacity-40"
          >
            <Icon name="picture_as_pdf" className="text-sm" /> Export Conversation
          </button>
        </div>

        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-sm text-on-surface-variant py-12">
              <Icon name="psychology" className="text-3xl opacity-40 mb-2" />
              <p>Ask about a case, a pattern, or a citizen — e.g. "Summarize case CASE005312" or "What UPI fraud patterns are trending?"</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[75%] rounded-lg px-4 py-3 text-sm ${
                  m.role === "user"
                    ? "bg-primary-container text-on-primary"
                    : "ai-panel text-on-surface"
                }`}
              >
                <p className="whitespace-pre-wrap">{m.content}</p>
                {m.sources && m.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-outline-variant/30 space-y-1">
                    {m.sources.map((s) => (
                      <Link
                        key={s.case_id}
                        to={`/cases/${s.case_id}`}
                        className="block text-xs text-secondary hover:underline"
                      >
                        {s.fir_number}: {s.snippet}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {sending && (
            <div className="flex justify-start">
              <div className="px-4 py-2 flex items-center gap-2 text-sm text-on-surface-variant opacity-70">
                <Icon name="progress_activity" className="animate-spin text-base" />
                Thinking...
              </div>
            </div>
          )}
          {error && (
            <div className="text-center text-sm text-error">{error}</div>
          )}
        </div>

        <form onSubmit={handleSend} className="flex items-center gap-2 p-4 border-t border-outline-variant">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask the investigation assistant..."
            className="flex-1 border border-outline-variant rounded-md px-4 py-2.5 text-sm"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            className="bg-primary-container text-on-primary w-10 h-10 rounded-md flex items-center justify-center disabled:opacity-40"
          >
            <Icon name="send" />
          </button>
        </form>
      </div>
    </AppLayout>
  );
}
