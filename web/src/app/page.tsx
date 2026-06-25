"use client";

import Link from "next/link";
import { useProfile } from "@/context/ProfileContext";
import { MODULES, PROJECT, TECH_STACK } from "@/lib/project-meta";

export default function HomePage() {
  const { loadDemo } = useProfile();

  return (
    <div className="space-y-8">
      <section className="text-center">
        <span className="inline-block rounded-full border border-accent/30 bg-accent/10 px-3 py-1 text-xs text-accent">
          🎓 {PROJECT.batch} · {PROJECT.academic_year}
        </span>
        <h1 className="mt-4 bg-gradient-to-r from-accent to-accent-purple bg-clip-text text-4xl font-bold text-transparent md:text-5xl">
          {PROJECT.title}
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-slate-400">{PROJECT.subtitle}</p>
        <p className="mt-2 text-sm text-slate-500">
          by <span className="text-accent">{PROJECT.student_name}</span> · {PROJECT.department}
        </p>
      </section>

      <div className="grid gap-3 sm:grid-cols-3">
        <button type="button" onClick={loadDemo} className="btn-primary">
          🎬 Start demo walkthrough
        </button>
        <Link href="/profile" className="btn-secondary text-center">
          ⚙️ Set target & best plan
        </Link>
        <Link href="/advisor" className="btn-secondary text-center">
          🧠 Open AI Advisor
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {[
          ["8", "Integrated modules"],
          ["Live", "Market data"],
          ["500+", "MC simulations"],
          ["5", "Health pillars"],
          ["100", "Health score max"],
        ].map(([num, lbl]) => (
          <div key={lbl} className="stat-box">
            <div className="num">{num}</div>
            <div className="lbl">{lbl}</div>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap justify-center gap-2">
        {TECH_STACK.map(([name]) => (
          <span
            key={name}
            className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300"
          >
            {name}
          </span>
        ))}
      </div>

      <section>
        <h2 className="mb-4 text-xl font-semibold">🚀 Explore the platform</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MODULES.map((m) => (
            <Link key={m.href} href={m.href} className="glass-card block transition hover:border-accent/40">
              <span className="text-2xl">{m.icon}</span>
              <p className="mt-2 font-semibold">{m.name}</p>
              <p className="mt-1 text-sm text-slate-400">{m.desc}</p>
            </Link>
          ))}
        </div>
      </section>

      <div className="glass-card">
        <h3 className="font-semibold">💡 Why this project stands out</h3>
        <ul className="mt-3 list-inside list-disc space-y-2 text-sm text-slate-300">
          <li>
            <strong>Unified</strong> — MF + crypto + goals in one app
          </li>
          <li>
            <strong>Data-driven</strong> — real Binance & Nifty/Sensex feeds
          </li>
          <li>
            <strong>Quantitative</strong> — Monte Carlo with percentile bands
          </li>
          <li>
            <strong>Explainable</strong> — rule-based AI advisor
          </li>
          <li>
            <strong>Production-style</strong> — Next.js on Vercel + Streamlit locally
          </li>
        </ul>
      </div>

      <p className="rounded-xl border border-accent/20 bg-accent/5 p-4 text-sm text-slate-300">
        Start with <Link href="/profile" className="text-accent underline">Profile & Plan</Link>, set your
        wealth or profit target, click <strong>Apply best plan</strong> — SIP, goals, MF hints, and AI Advisor
        update everywhere.
      </p>
    </div>
  );
}
