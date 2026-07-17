import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppLayout({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="min-h-screen bg-canvas">
      <Sidebar />
      <div className="ml-[260px] flex flex-col min-h-screen">
        <Topbar title={title} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
