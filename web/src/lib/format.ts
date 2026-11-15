import type { ProblemSummary } from '../types'
import { STATIC } from '../mode'

/** In STATIC replay, relative times are measured against the snapshot clock, not the viewer's wall clock. */
let nowRef: number | null = null
export function setNowRef(ms: number | null | undefined): void {
  if (STATIC && typeof ms === 'number' && Number.isFinite(ms)) nowRef = ms
}
function refNow(): number {
  return STATIC && nowRef != null ? nowRef : Date.now()
}

export const PROBLEM_COLORS: Record<string, string> = {
  'no-three-in-line-75': '#4FD1E0',
  'spencer-discrepancy': '#A99BEA',
  'hadamard-det-51': '#6FBF8E',
  'sidon-45-set': '#D684A9',
  'two-deletion-code-16': '#7096E0',
  'snake-in-the-box-13': '#CDB866',
  'ring-loading-15': '#DE9A6E',
  'event-horizon': '#A99BEA',
}
const FALLBACK = ['#7FB8D8', '#B490D8', '#D48AAE', '#62B894', '#D6AE5A', '#7096E0']

export function problemColor(slug: string | null | undefined): string {
  if (!slug) return '#3A424F'
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
  'event-horizon': 'Event Horizon',
  'first-autocorrelation-inequality': 'First autocorrelation',
  'kakeya-needle-128': 'Kakeya needle 128',
  'kissing-number-d12-842': 'Kissing number d12',
  'kissing-number-d11-605': 'Kissing number d11',
  'three-body-periodic-orbits': 'Three-body orbits',
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

export function timeAgo(iso: string | null | undefined, now = refNow()): string {
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
  if (!p.ours || p.record.score == null) return null
  const d = p.ours.score - p.record.score
  return p.scoring === 'maximize' ? d : -d
}

export const STATUS_STYLE: Record<string, { label: string; cls: string; dot: string }> = {
  searching: { label: 'Searching', cls: 'text-fg border-white/10 bg-white/[0.03]', dot: 'bg-cyan' },
  stalled: { label: 'Stalled', cls: 'text-fg-muted border-white/10 bg-white/[0.03]', dot: 'bg-amber' },
  record: { label: 'Record', cls: 'text-amber border-amber/30 bg-amber/[0.08]', dot: 'bg-amber' },
  verified: { label: 'Verified', cls: 'text-good border-good/30 bg-good/[0.08]', dot: 'bg-good' },
  candidates: { label: 'Candidates', cls: 'text-amber border-amber/30 bg-amber/[0.08]', dot: 'bg-amber' },
  idle: { label: 'Idle', cls: 'text-fg-dim border-white/[0.08] bg-transparent', dot: 'bg-ink-400' },
  'proved-negative': { label: 'Proved negative', cls: 'text-violet border-violet/30 bg-violet/[0.08]', dot: 'bg-violet' },
}

export const AGENT_COLORS: Record<string, string> = {
  planner: '#7096E0',
  proposer: '#4FD1E0',
  critic: '#DE9A6E',
  executor: '#6FBF8E',
  literature: '#CDB866',
  memory: '#A99BEA',
  sandbox: '#5FB8AE',
  learning: '#D684A9',
  referee: '#E2B25C',
  toolsmith: '#A5C76B',
  system: '#9BA3AF',
}
export function agentColor(a: string): string {
  if (a.startsWith('agent:')) return problemColor(a.slice(6))
  return AGENT_COLORS[a] ?? '#9BA3AF'
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
