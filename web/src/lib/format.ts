import type { ProblemSummary } from '../types'

export const PROBLEM_COLORS: Record<string, string> = {
  'no-three-in-line-75': '#3DF5FF',
  'spencer-discrepancy': '#A98BFF',
  'hadamard-det-51': '#6CF29A',
  'sidon-45-set': '#FF5DA8',
  'two-deletion-code-16': '#5B8CFF',
  'snake-in-the-box-13': '#E9E36B',
  'ring-loading-15': '#3FD0C9',
}
const FALLBACK = ['#7DD3FC', '#C084FC', '#F472B6', '#34D399', '#FBBF24', '#60A5FA']

export function problemColor(slug: string | null | undefined): string {
  if (!slug) return '#3A4252'
  if (PROBLEM_COLORS[slug]) return PROBLEM_COLORS[slug]
  let h = 0
  for (const c of slug) h = (h * 31 + c.charCodeAt(0)) >>> 0
  return FALLBACK[h % FALLBACK.length]
}

const SHORT: Record<string, string> = {
  'no-three-in-line-75': 'No-three-in-line 75',
  'spencer-discrepancy': 'Spencer discrepancy',
  'hadamard-det-51': 'Hadamard det 51',
  'sidon-45-set': 'Sidon (4,5)-sets',
  'two-deletion-code-16': 'Two-deletion code 16',
  'snake-in-the-box-13': 'Snake-in-the-box 13',
  'ring-loading-15': 'Ring loading 15',
}
export function shortName(slug: string | null | undefined): string {
  if (!slug) return 'global'
  return SHORT[slug] ?? slug
}

/** Format a score with enough precision to show differences vs the record. */
export function fmtScore(v: number | null | undefined, digits?: number): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  if (Number.isInteger(v)) return v.toLocaleString('en-US')
  if (digits !== undefined) return v.toFixed(digits)
  const a = Math.abs(v)
  if (a >= 1e6) return v.toLocaleString('en-US', { maximumFractionDigits: 1 })
  if (a < 1e-4) return v.toExponential(3)
  // enough significant digits to tell near-record scores apart
  return v.toPrecision(12).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '')
}

export function fmtInt(v: number | null | undefined): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  return Math.round(v).toLocaleString('en-US')
}

export function fmtCompact(v: number | null | undefined): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  const a = Math.abs(v)
  if (a >= 1e6) return (v / 1e6).toFixed(1) + 'M'
  if (a >= 1e4) return (v / 1e3).toFixed(1) + 'k'
  return fmtScore(v)
}

export function fmtPct(v: number | null | undefined, digits = 0): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  return (v * 100).toFixed(digits) + '%'
}

export function fmtUsd(v: number | null | undefined): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  if (v < 0.01) return '$' + v.toFixed(4)
  return '$' + v.toFixed(3)
}

export function fmtMs(v: number | null | undefined): string {
  if (v === null || v === undefined || Number.isNaN(v)) return '--'
  if (v >= 1000) return (v / 1000).toFixed(1) + ' s'
  return Math.round(v) + ' ms'
}

export function timeAgo(iso: string | null | undefined, now = Date.now()): string {
  if (!iso) return '--'
  const t = Date.parse(iso)
  if (Number.isNaN(t)) return '--'
  const s = Math.round((now - t) / 1000)
  if (s < -5) return 'in ' + dur(-s)
  if (s < 5) return 'just now'
  return dur(s) + ' ago'
}

export function dur(s: number): string {
  s = Math.max(0, Math.round(s))
  if (s < 60) return `${s}s`
  const m = Math.floor(s / 60)
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`
  const h = Math.floor(m / 60)
  if (h < 48) return `${h}h ${String(m % 60).padStart(2, '0')}m`
  return `${Math.floor(h / 24)}d ${h % 24}h`
}

export function clockTime(iso: string | null | undefined): string {
  if (!iso) return '--'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '--'
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
}

export function dateTime(iso: string | null | undefined): string {
  if (!iso) return '--'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '--'
  return d.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZoneName: 'short' })
}

/** Signed gap between ours and the record, positive = we are ahead. */
export function gapToRecord(p: ProblemSummary): number | null {
  if (!p.ours) return null
  const d = p.ours.score - p.record.score
  return p.scoring === 'maximize' ? d : -d
}

export const STATUS_STYLE: Record<string, { label: string; cls: string; dot: string }> = {
  searching: { label: 'searching', cls: 'text-cyan border-cyan/30 bg-cyan/5', dot: 'bg-cyan' },
  stalled: { label: 'stalled', cls: 'text-fg-muted border-ink-400 bg-ink-700', dot: 'bg-fg-muted' },
  record: { label: 'record', cls: 'text-amber border-amber/50 bg-amber/10', dot: 'bg-amber' },
  idle: { label: 'idle', cls: 'text-fg-dim border-ink-500 bg-ink-800', dot: 'bg-fg-dim' },
  'proved-negative': { label: 'proved negative', cls: 'text-[#C9A8FF] border-[#A98BFF]/40 bg-[#A98BFF]/10', dot: 'bg-[#A98BFF]' },
}

export const AGENT_COLORS: Record<string, string> = {
  planner: '#5B8CFF',
  proposer: '#3DF5FF',
  critic: '#FF8A5B',
  executor: '#6CF29A',
  literature: '#E9E36B',
  memory: '#A98BFF',
  sandbox: '#3FD0C9',
  learning: '#FF5DA8',
  referee: '#FFB547',
  toolsmith: '#B8F55B',
  system: '#8B95A7',
}
export function agentColor(a: string): string {
  if (a.startsWith('agent:')) return problemColor(a.slice(6))
  return AGENT_COLORS[a] ?? '#8B95A7'
}

export function cx(...xs: (string | false | null | undefined)[]): string {
  return xs.filter(Boolean).join(' ')
}

/** Only http(s) URLs from external data (Exa results) become links; anything else (javascript:, data:) is dropped. */
export function safeHref(url: string | null | undefined): string | undefined {
  if (!url) return undefined
  try {
    const u = new URL(url)
    return u.protocol === 'http:' || u.protocol === 'https:' ? u.href : undefined
  } catch {
    return undefined
  }
}
