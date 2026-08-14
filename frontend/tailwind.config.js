export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1B2A2E",
        paper: "#F4F7F5",
        deep: "#0F3D3E",
        teal: "#2A9D8F",
        coral: "#E76F51",
        stone: "#8FA3A0",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
    },
  },
  plugins: [],
}