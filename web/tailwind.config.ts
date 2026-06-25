import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        accent: { DEFAULT: "#00d4aa", purple: "#8b5cf6", gold: "#fbbf24", rose: "#f43f5e" },
        surface: { deep: "#0a0e17", card: "rgba(255,255,255,0.04)", glass: "rgba(255,255,255,0.06)" },
      },
      fontFamily: {
        sans: ["var(--font-dm-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-jetbrains)", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
