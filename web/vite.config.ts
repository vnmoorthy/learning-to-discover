import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const STATIC = process.env.VITE_STATIC === '1'
// In fixture mode there is no backend: serve /gallery from public/ instead of proxying.
const FIXTURES = process.env.VITE_FIXTURES === '1'
const BACKEND = process.env.LTD_BACKEND || 'http://127.0.0.1:8787'

export default defineConfig({
  plugins: [react()],
  base: STATIC ? '/phoenixastar/' : '/',
  server: {
    port: 5173,
    strictPort: false,
    proxy: FIXTURES
      ? undefined
      : {
          '/api': { target: BACKEND, changeOrigin: true },
          // only gallery FILES (/gallery/x.png): the SPA route /gallery itself must stay with Vite, or a reload of
          // the Gallery page would be sent to the backend
          '^/gallery/.+': { target: BACKEND, changeOrigin: true },
        },
  },
  build: {
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        // Keep React in the entry vendor chunk so lazy pages (3D, charts, markdown) stay lazy.
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined
          if (/[\\/]node_modules[\\/](three|@react-three)[\\/]/.test(id)) return 'three'
          if (/[\\/]node_modules[\\/](recharts|recharts-scale|d3-[^\\/]+|victory-vendor|lodash|decimal\.js-light)[\\/]/.test(id)) return 'charts'
          if (/[\\/]node_modules[\\/](katex|react-markdown|remark-[^\\/]+|rehype-[^\\/]+|micromark[^\\/]*|mdast-[^\\/]+|hast-[^\\/]+|unified|unist-[^\\/]+|vfile[^\\/]*)[\\/]/.test(id)) return 'md'
          if (/[\\/]node_modules[\\/](react|react-dom|scheduler|react-router|react-router-dom|@remix-run|framer-motion|motion-dom|motion-utils)[\\/]/.test(id)) return 'vendor'
          return undefined
        },
      },
    },
  },
})
