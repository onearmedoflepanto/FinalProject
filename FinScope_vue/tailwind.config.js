/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#38bdf8', // sky-400
          DEFAULT: '#0ea5e9', // sky-500
          dark: '#0284c7',  // sky-600
        },
        // You can add other custom colors here if needed
      },
    },
  },
  plugins: [],
}
