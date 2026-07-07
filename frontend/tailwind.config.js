/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 20px 60px rgba(15, 23, 42, 0.18)",
      },
      colors: {
        ink: {
          950: "#07111f",
          900: "#0d1728",
          800: "#15233b",
        },
        teal: {
          500: "#14b8a6",
          600: "#0f9f8e",
        },
        amber: {
          400: "#fbbf24",
          500: "#f59e0b",
        },
      },
      backgroundImage: {
        "hero-radial": "radial-gradient(circle at top left, rgba(20, 184, 166, 0.22), transparent 34%), radial-gradient(circle at top right, rgba(251, 191, 36, 0.18), transparent 30%), linear-gradient(135deg, #07111f 0%, #0d1728 52%, #12253b 100%)",
      },
    },
  },
  plugins: [],
};
