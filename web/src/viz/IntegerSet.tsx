import { useMemo, useState } from 'react'
import { fmtScore } from '../lib/format'

/** Number line of an integer set, with pairwise-difference histogram of the set below. */
export default function IntegerSet({ elements, h, score, color = '#FF5DA8' }: { elements: number[]; h?: number | null; score?: number | null; color?: string }) {
  const els = useMemo(() => [...elements].sort((a, b) => a - b), [elements])
  const [hover, setHover] = useState<number | null>(null)
  const lo = els[0] ?? 0
  const hi = els[els.length - 1] ?? 1
  const span = hi - lo || 1
  const W = 760
  const H = 112
  const padX = 30
  const X = (v: number) => padX + ((v - lo) / span) * (W - padX * 2)
  const ticks = useMemo(() => {
    const raw = span / 6
    const p = Math.pow(10, Math.floor(Math.log10(raw)))
    const m = raw / p
    const step = Math.max(1, (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p)
    const out: number[] = []
    for (let t = Math.ceil(lo / step) * step; t <= hi; t += step) out.push(t)
    return out
  }, [lo, hi, span])
  const diffs = useMemo(() => {
    const m = new Map<number, number>()
    for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
      const d = els[j] - els[i]
      m.set(d, (m.get(d) ?? 0) + 1)
    }
    return m
  }, [els])
  const repeated = [...diffs.values()].filter((c) => c > 1).length

  return (
    <div>
      <div className="mb-3 flex flex-wrap gap-x-5 gap-y-1 font-mono text-[11.5px] text-fg-muted">
        <span>
          |A| <span className="text-fg">{els.length}</span>
        </span>
        {h != null && (
          <span>
            h(A) <span style={{ color }}>{h}</span>
          </span>
        )}
        {score != null && (
          <span>
            score h/|A| <span className="text-cyan">{fmtScore(score)}</span>
          </span>
        )}
        <span>
          distinct differences <span className="text-fg">{diffs.size}</span> ({repeated} repeated)
        </span>
        <span>
          span <span className="text-fg">[{lo}, {hi}]</span>
        </span>
      </div>
      <div className="overflow-x-auto">
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full min-w-[480px]" role="img" aria-label="number line of the integer set">
          <defs>
            <filter id="isglow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="3" result="b" />
              <feMerge>
                <feMergeNode in="b" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <line x1={padX - 10} x2={W - padX + 10} y1={70} y2={70} stroke="rgba(255,255,255,0.18)" />
          {ticks.map((t) => (
            <g key={t}>
              <line x1={X(t)} x2={X(t)} y1={66} y2={74} stroke="rgba(255,255,255,0.22)" />
              <text x={X(t)} y={92} textAnchor="middle" fontSize="11" className="fill-fg-dim font-mono">
                {t}
              </text>
            </g>
          ))}
          {els.map((v, i) => (
            <g key={v} onMouseEnter={() => setHover(v)} onMouseLeave={() => setHover(null)} className="cursor-pointer">
              <line x1={X(v)} x2={X(v)} y1={70} y2={hover === v ? 30 : 44} stroke={color} strokeOpacity={0.5} />
              <circle cx={X(v)} cy={70} r={hover === v ? 7 : 5} fill={color} filter="url(#isglow)" />
              <text x={X(v)} y={i % 2 ? 24 : 38} textAnchor="middle" fontSize="11" className="fill-fg font-mono" opacity={hover == null || hover === v ? 1 : 0.35}>
                {v}
              </text>
              <rect x={X(v) - 10} y={10} width={20} height={80} fill="transparent" />
            </g>
          ))}
        </svg>
      </div>
      {hover != null && (
        <div className="mt-1 font-mono text-[11px] text-fg-muted">
          differences from {hover}:{' '}
          <span className="text-fg">
            {els
              .filter((x) => x !== hover)
              .map((x) => Math.abs(x - hover))
              .sort((a, b) => a - b)
              .join(', ')}
          </span>
        </div>
      )}
    </div>
  )
}
