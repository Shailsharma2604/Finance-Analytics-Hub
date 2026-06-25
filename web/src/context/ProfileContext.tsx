"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { DEFAULT_PROFILE } from "@/lib/constants";
import { buildBestPlan } from "@/lib/plan-engine";
import { applyDemoProfile } from "@/lib/demo-data";
import type { GoalRow, Profile } from "@/lib/types";

const STORAGE_KEY = "fah_profile";
const GOALS_KEY = "fah_goals";
const PAPER_KEY = "fah_paper_portfolio";

interface ProfileContextValue {
  profile: Profile;
  goals: GoalRow[];
  goalsGapTotal: number;
  updateProfile: (patch: Partial<Profile>) => void;
  applyBestPlan: () => void;
  loadDemo: () => void;
  setGoals: (goals: GoalRow[]) => void;
  paperPortfolio: Record<string, number>;
  setPaperQty: (symbol: string, qty: number) => void;
}

const ProfileContext = createContext<ProfileContextValue | null>(null);

const DEFAULT_GOALS: GoalRow[] = [
  {
    id: "1",
    goal: "Wealth target",
    target: 5_000_000,
    years: 15,
    priority: 1,
    saved: 500_000,
    sip: 25_000,
  },
];

function loadJson<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function ProfileProvider({ children }: { children: ReactNode }) {
  const [profile, setProfile] = useState<Profile>(DEFAULT_PROFILE);
  const [goals, setGoalsState] = useState<GoalRow[]>(DEFAULT_GOALS);
  const [paperPortfolio, setPaperPortfolio] = useState<Record<string, number>>({});
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setProfile(loadJson(STORAGE_KEY, DEFAULT_PROFILE));
    setGoalsState(loadJson(GOALS_KEY, DEFAULT_GOALS));
    setPaperPortfolio(loadJson(PAPER_KEY, {}));
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  }, [profile, hydrated]);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(GOALS_KEY, JSON.stringify(goals));
  }, [goals, hydrated]);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(PAPER_KEY, JSON.stringify(paperPortfolio));
  }, [paperPortfolio, hydrated]);

  const updateProfile = useCallback((patch: Partial<Profile>) => {
    setProfile((p) => ({ ...p, ...patch }));
  }, []);

  const applyBestPlan = useCallback(() => {
    setProfile((p) => {
      const plan = buildBestPlan(p);
      const updated: Profile = {
        ...p,
        profile_sip: plan.recommended_sip,
        profile_equity: plan.equity_pct,
        profile_risk: plan.risk_profile as Profile["profile_risk"],
        profile_mf_risk: plan.risk_profile,
        profile_equity_strategy: plan.equity_strategy as Profile["profile_equity_strategy"],
        profile_wealth_target: plan.wealth_target,
        profile_profit_target: plan.profit_target_annual,
        plan_applied: true,
        recommended_plan: plan,
      };
      setGoalsState((g) => {
        if (g.length === 0) {
          return [
            {
              id: "1",
              goal: "Wealth target (from profile)",
              target: plan.wealth_target,
              years: plan.target_years,
              priority: 1,
              saved: plan.current_wealth,
              sip: plan.recommended_sip,
            },
          ];
        }
        return g.map((row, i) =>
          i === 0
            ? {
                ...row,
                goal: "Wealth target (from profile)",
                target: plan.wealth_target,
                years: plan.target_years,
                saved: plan.current_wealth,
                sip: plan.recommended_sip,
              }
            : row
        );
      });
      return updated;
    });
  }, []);

  const loadDemo = useCallback(() => {
    setProfile((p) => applyDemoProfile(p));
    setGoalsState([
      {
        id: "1",
        goal: "Wealth target (demo)",
        target: 3_000_000,
        years: 12,
        priority: 1,
        saved: 185_000 + 850 * 83.5,
        sip: 12_000,
      },
    ]);
  }, []);

  const setGoals = useCallback((g: GoalRow[]) => setGoalsState(g), []);

  const setPaperQty = useCallback((symbol: string, qty: number) => {
    setPaperPortfolio((prev) => {
      const next = { ...prev };
      if (qty <= 0) delete next[symbol];
      else next[symbol] = qty;
      return next;
    });
  }, []);

  const goalsGapTotal = useMemo(() => {
    return profile.recommended_plan?.gap_monthly ?? 0;
  }, [profile.recommended_plan]);

  const value = useMemo(
    () => ({
      profile,
      goals,
      goalsGapTotal,
      updateProfile,
      applyBestPlan,
      loadDemo,
      setGoals,
      paperPortfolio,
      setPaperQty,
    }),
    [
      profile,
      goals,
      goalsGapTotal,
      updateProfile,
      applyBestPlan,
      loadDemo,
      setGoals,
      paperPortfolio,
      setPaperQty,
    ]
  );

  if (!hydrated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-deep text-slate-400">
        Loading…
      </div>
    );
  }

  return <ProfileContext.Provider value={value}>{children}</ProfileContext.Provider>;
}

export function useProfile() {
  const ctx = useContext(ProfileContext);
  if (!ctx) throw new Error("useProfile must be used within ProfileProvider");
  return ctx;
}
