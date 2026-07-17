import { client } from "./client";
import type { ChatQueryResponse, ChatHistory } from "@/types/api";

export async function sendChatQuery(question: string, sessionId?: string) {
  const res = await client.post<ChatQueryResponse>("/chat/query", {
    question,
    session_id: sessionId,
  });
  return res.data;
}

export async function getChatHistory(sessionId: string) {
  const res = await client.get<ChatHistory>(`/chat/history/${sessionId}`);
  return res.data;
}

export async function exportChat(sessionId: string) {
  const res = await client.post("/chat/export", { session_id: sessionId }, { responseType: "blob" });
  return res.data as Blob;
}
