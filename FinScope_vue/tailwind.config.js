/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html", 
    "./src/**/*.{vue,js,ts,jsx,tsx}" 
    // Ensure all view files are covered by this pattern
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb', // A vibrant blue, similar to Gemini's accent
          light: '#3b82f6',
          dark: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
