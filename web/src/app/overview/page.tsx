import { OBJECTIVES, PROJECT, TECH_STACK } from "@/lib/project-meta";
import Link from "next/link";

export default function OverviewPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">🎓 Project Overview</h1>
        <p className="mt-2 text-slate-400">FYP documentation & architecture</p>
      </div>

      <div className="glass-card grid gap-4 sm:grid-cols-2">
        <div>
          <p className="text-xs uppercase text-slate-500">Student</p>
          <p className="font-semibold">{PROJECT.student_name}</p>
          <p className="text-sm text-slate-400">{PROJECT.roll_number}</p>
        </div>
        <div>
          <p className="text-xs uppercase text-slate-500">Guide</p>
          <p className="font-semibold">{PROJECT.guide_name}</p>
          <p className="text-sm text-slate-400">{PROJECT.institution}</p>
        </div>
      </div>

      <section>
        <h2 className="mb-3 text-xl font-semibold">Objectives</h2>
        <ol className="list-inside list-decimal space-y-2 text-slate-300">
          {OBJECTIVES.map((o, i) => (
            <li key={i}>{o}</li>
          ))}
        </ol>
      </section>

      <section>
        <h2 className="mb-3 text-xl font-semibold">System Architecture</h2>
        <pre className="overflow-x-auto rounded-xl border border-white/10 bg-black/30 p-4 text-sm text-accent">
{`Next.js UI (Vercel)  →  lib/ (TypeScript)  →  Binance | Yahoo Finance APIs
Streamlit UI (local)  →  lib/ (Python)      →  Allocation Engine | Monte Carlo`}
        </pre>
      </section>

      <section>
        <h2 className="mb-3 text-xl font-semibold">Tech Stack</h2>
        <div className="grid gap-2 sm:grid-cols-2">
          {TECH_STACK.map(([name, desc]) => (
            <div key={name} className="glass-card text-sm">
              <span className="font-semibold text-accent">{name}</span>
              <span className="text-slate-400"> — {desc}</span>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-xl font-semibold">Demo mode</h2>
        <p className="text-slate-300">
          Click <strong>Start demo walkthrough</strong> on the home page, then walk through{" "}
          <Link href="/command-center" className="text-accent underline">Command Center</Link> →{" "}
          <Link href="/goals" className="text-accent underline">Goal Planner</Link> →{" "}
          <Link href="/advisor" className="text-accent underline">AI Advisor</Link>.
        </p>
      </section>
    </div>
  );
}
