/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-hero': 'linear-gradient(135deg, #FF6B35 0%, #F59E0B 50%, #7C3AED 100%)',
      },
    },
  },
  plugins: [],
}