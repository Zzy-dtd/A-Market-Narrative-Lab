import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        lab: {
          background: "#F7F2EA",
          text: "#1F2937",
          table: "#D8C3A5",
          value: "#2F6B4F",
          trader: "#5B4B8A",
          contrarian: "#B75D2A",
        },
      },
      boxShadow: {
        bubble: "0 18px 50px rgba(31, 41, 55, 0.10)",
        scene: "0 28px 90px rgba(66, 50, 30, 0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
