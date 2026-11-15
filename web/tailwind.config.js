/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: '#07080B', 900: '#07080B', 850: '#0A0C10', 800: '#0E1116', 700: '#141820', 600: '#1B2029', 500: '#262C38', 400: '#3A4252' },
        fg: { DEFAULT: '#E6EDF5', muted: '#8B95A7', dim: '#5A6375' },
        cyan: { DEFAULT: '#3DF5FF', soft: '#3DF5FF33' },
        amber: { DEFAULT: '#FFB547', soft: '#FFB54733' },
        bad: '#FF4D5E',
        good: '#43F0A0',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
        display: ['"Space Grotesk"', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(61,245,255,0.25), 0 0 24px -4px rgba(61,245,255,0.35)',
        amber: '0 0 0 1px rgba(255,181,71,0.35), 0 0 28px -4px rgba(255,181,71,0.45)',
      },
      keyframes: {
        pulseDot: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.35' } },
        scan: { '0%': { transform: 'translateX(-100%)' }, '100%': { transform: 'translateX(100%)' } },
      },
      animation: {
        pulseDot: 'pulseDot 1.6s ease-in-out infinite',
        scan: 'scan 2.4s linear infinite',
      },
    },
  },
  plugins: [],
}
