// Build-time mode flags.
//  live      : talks to the backend under /api (default)
//  static    : VITE_STATIC=1, reads ./data/*.json relative to base, read-only replay
//  fixtures  : VITE_FIXTURES=1, in-browser simulated backend for development without the server
export const STATIC = import.meta.env.VITE_STATIC === '1'
export const FIXTURES = !STATIC && import.meta.env.VITE_FIXTURES === '1'
export const MODE: 'live' | 'static' | 'fixtures' = STATIC ? 'static' : FIXTURES ? 'fixtures' : 'live'
export const BASE = import.meta.env.BASE_URL || '/'
export const READ_ONLY = STATIC

/** Resolve a server-absolute asset path (e.g. "/gallery/x.png") for the current mode. */
export function assetUrl(src: string): string {
  if (!src) return src
  if (/^(https?:|data:|blob:)/.test(src)) return src
  if (STATIC) return BASE + src.replace(/^\/+/, '')
  return src.startsWith('/') ? src : '/' + src
}
