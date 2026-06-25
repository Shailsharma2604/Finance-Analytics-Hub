"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "./ThemeProvider";
import { useProfile } from "@/context/ProfileContext";
import { formatINR } from "@/lib/format";
import { MODULES, PROJECT } from "@/lib/project-meta";

const NAV = [
  { href: "/", label: "Home", icon: "🎓" },
  { href: "/overview", label: "Overview", icon: "📋" },
  ...MODULES.map((m) => ({ href: m.href, label: m.name, icon: m.icon })),
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { profile } = useProfile();
  const plan = profile.recommended_plan;

  return (
    <div className="flex min-h-screen">
      <aside className="hidden w-64 shrink-0 flex-col border-r border-white/10 bg-black/30 p-4 lg:flex">
        <div className="mb-6">
          <p className="text-xs text-accent">🎓 {PROJECT.batch}</p>
          <h1 className="text-lg font-bold leading-tight">{PROJECT.title}</h1>
          <p className="text-xs text-slate-400">FYP · {PROJECT.academic_year}</p>
        </div>

        {plan && profile.plan_applied && (
          <div className="mb-4 rounded-xl border border-accent/35 bg-accent/10 p-3 text-xs">
            <p className="font-semibold text-accent">Active plan</p>
            <p className="text-slate-300">
              SIP {formatINR(plan.recommended_sip)} · {plan.equity_pct}% equity
            </p>
            <p className="text-slate-400">{plan.plan_grade}</p>
          </div>
        )}

        <nav className="flex flex-1 flex-col gap-1 overflow-y-auto">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-lg px-3 py-2 text-sm transition ${
                  active
                    ? "bg-accent/15 font-semibold text-accent"
                    : "text-slate-300 hover:bg-white/5"
                }`}
              >
                {item.icon} {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="mt-4 space-y-2 border-t border-white/10 pt-4">
          <ThemeToggle />
          <p className="text-[10px] text-slate-500">Educational use only — not financial advice.</p>
        </div>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-white/10 px-4 py-3 lg:hidden">
          <Link href="/" className="font-bold text-accent">
            {PROJECT.title}
          </Link>
          <ThemeToggle />
        </header>
        <main className="mx-auto w-full max-w-6xl flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
