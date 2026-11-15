/** @type {import('tailwindcss').Config} */
// Phoenixastar design tokens: graphite surfaces, hairline borders, one calm accent, desaturated semantics.
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // surfaces: 900 page, 850 sunken, 800 panel, 700 raised, 600 hover, 500/400 strong borders
        ink: { DEFAULT: '#0B0D10', 900: '#0B0D10', 850: '#0E1014', 800: '#111418', 700: '#171B21', 600: '#1E232B', 500: '#2A303A', 400: '#3A424F' },
        fg: { DEFAULT: '#E7E9EC', muted: '#9BA3AF', dim: '#7A838F' },
        cyan: { DEFAULT: '#4FD1E0', soft: '#4FD1E026' },
        amber: { DEFAULT: '#E2B25C', soft: '#E2B25C26', 300: '#E2B25C' },
        bad: '#E5676B',
        good: '#4CC38A',
        violet: '#A99BEA',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
        display: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        // legacy names kept so call sites stay valid: now 1px rings, no bloom
        glow: '0 0 0 1px rgba(79,209,224,0.28)',
        amber: '0 0 0 1px rgba(226,178,92,0.22)',
        pop: '0 1px 0 rgba(255,255,255,0.03) inset, 0 12px 32px -12px rgba(0,0,0,0.6)',
      },
      keyframes: {
        pulseDot: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.45' } },
        scan: { '0%': { transform: 'translateX(-100%)' }, '100%': { transform: 'translateX(100%)' } },
      },
      animation: {
        pulseDot: 'pulseDot 2.4s ease-in-out infinite',
        scan: 'scan 2.4s linear infinite',
      },
    },
  },
  plugins: [],
}
