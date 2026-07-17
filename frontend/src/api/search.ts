import { client } from "./client";
import type { SearchResponse } from "@/types/api";

export async function searchEntity(value: string, entityType?: string) {
  const res = await client.get<SearchResponse>("/search", {
    params: { value, entity_type: entityType },
  });
  return res.data;
}

export async function searchByFir(firNumber: string) {
  const res = await client.get(`/search/fir/${firNumber}`);
  return res.data;
}
