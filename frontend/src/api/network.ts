import { client } from "./client";
import type { NetworkGraph } from "@/types/api";

export async function getNetworkGraph(citizenId: string) {
  const res = await client.get<NetworkGraph>(`/network/${citizenId}`);
  return res.data;
}
