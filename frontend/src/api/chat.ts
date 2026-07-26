import { client } from "./client";
import type { ChatQueryResponse, ChatHistory } from "@/types/api";

export async function sendChatQuery(question: string, sessionId?: string) {
  const form = new URLSearchParams();
  form.append("question", question);
  if (sessionId) form.append("session_id", sessionId);

  const res = await client.post<ChatQueryResponse>("/chat/query", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });
  return res.data;
}

export async function getChatHistory(sessionId: string) {
  const res = await client.get<ChatHistory>(`/chat/history/${sessionId}`);
  return res.data;
}

export async function exportChat(sessionId: string) {
  const form = new URLSearchParams();
  form.append("session_id", sessionId);

  const res = await client.post("/chat/export", form, {
    responseType: "blob",
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });
  return res.data as Blob;
}
