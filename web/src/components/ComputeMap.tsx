import { motion } from 'framer-motion'
import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { cx, fmtInt, problemColor, shortName } from '../lib/format'
import type { ComputeState } from '../types'

const A100_MB = 40960

function GpuTile({ g }: { g: ComputeState['gpus'][number] }) {
  const color = problemColor(g.problem)
  const util = Math.max(0, Math.min(100, g.util ?? 0))
  const mem = Math.max(0, g.mem_mb ?? 0)
  const r = 19
  const c = 2 * Math.PI * r
  const body = (
    <div
      className="group relative h-full overflow-hidden rounded-xl border p-3 transition-colors"
      style={{ borderColor: g.problem ? color + '38' : 'rgba(255,255,255,0.06)', background: g.problem ? `linear-gradient(160deg, ${color}14, transparent 60%)` : 'rgba(255,255,255,0.015)' }}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="font-mono label">GPU {g.idx}</div>
        <svg viewBox="0 0 48 48" className="-mr-1 -mt-1 h-11 w-11 shrink-0">
          <circle cx="24" cy="24" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="4" />
          <motion.circle
            cx="24"
            cy="24"
            r={r}
            fill="none"
            stroke={g.problem ? color : '#7A838F'}
            strokeWidth="4"
            strokeLinecap="round"
            transform="rotate(-90 24 24)"
            strokeDasharray={c}
            initial={false}
            animate={{ strokeDashoffset: c * (1 - util / 100) }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            style={{ filter: g.problem ? `drop-shadow(0 0 4px ${color})` : undefined }}
          />
          <text x="24" y="27.5" textAnchor="middle" className="fill-fg font-mono" fontSize="11" fontWeight="600">
            {util}
          </text>
        </svg>
      </div>
      <div className="-mt-2 truncate text-[12px] font-semibold" style={{ color: g.problem ? color : '#7A838F' }}>
        {g.problem ? shortName(g.problem) : 'free'}
      </div>
      <div className="mt-0.5 truncate font-mono text-[10px] text-fg-dim" title={(g.strategy_ids ?? [g.strategy_id]).filter(Boolean).join(', ')}>
        {g.strategy_id ?? '--'}
        {g.strategy_ids && g.strategy_ids.length > 1 && <span className="text-fg-muted"> +{g.strategy_ids.length - 1}</span>}
      </div>
      <div className="mt-2">
        <div className="h-1 overflow-hidden rounded-full bg-white/[0.06]">
          <motion.div className="h-full rounded-full" style={{ background: g.problem ? color : '#7A838F' }} initial={false} animate={{ width: `${Math.min(100, (mem / A100_MB) * 100)}%` }} />
        </div>
        <div className="mt-1 font-mono text-[10px] text-fg-dim">{(mem / 1024).toFixed(1)} / 40 GB</div>
      </div>
    </div>
  )
  return g.problem ? (
    <Link to={`/problems/${g.problem}`} className="block h-full">
      {body}
    </Link>
  ) : (
    body
  )
}

export function GpuGrid({ compute }: { compute: ComputeState }) {
  const gpus = compute.gpus.length ? compute.gpus : Array.from({ length: 8 }, (_, i) => ({ idx: i, util: 0, mem_mb: 0, problem: null, strategy_id: null }))
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
      {gpus.map((g) => (
        <GpuTile key={g.idx} g={g} />
      ))}
    </div>
  )
}

export function CpuGrid({ compute }: { compute: ComputeState }) {
  const total = compute.cpus || 124
  const { cells, legend } = useMemo(() => {
    const entries = Object.entries(compute.cpu_procs || {})
      .filter(([, n]) => n > 0)
      .sort((a, b) => b[1] - a[1])
    const cells: (string | null)[] = []
    for (const [slug, n] of entries) for (let i = 0; i < n && cells.length < total; i++) cells.push(slug)
    const assigned = cells.length
    while (cells.length < total) cells.push(null)
    return { cells, legend: { entries, assigned } }
  }, [compute.cpu_procs, total])
  const loadPct = Math.min(1, (compute.load1 || 0) / total)

  return (
    <div>
      <div className="grid gap-[3px]" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(13px, 1fr))' }}>
        {cells.map((slug, i) => {
          const color = problemColor(slug)
          return (
            <div
              key={i}
              title={slug ? `core ${i}: ${slug}` : `core ${i}: idle`}
              className={cx('aspect-square rounded-[3px] transition-colors duration-700', slug && 'cpu-cell')}
              style={{
                background: slug ? color : 'rgba(255,255,255,0.045)',
                boxShadow: slug ? `0 0 6px ${color}55` : undefined,
                animationDelay: `${(i * 137) % 3000}ms`,
              }}
            />
          )
        })}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-[11px]">
        {legend.entries.map(([slug, n]) => (
          <Link key={slug} to={`/problems/${slug}`} className="flex items-center gap-1.5 text-fg-muted hover:text-fg">
            <span className="h-2 w-2 rounded-sm" style={{ background: problemColor(slug) }} />
            <span>{shortName(slug)}</span>
            <span className="font-mono text-fg">{n}</span>
          </Link>
        ))}
        <span className="flex items-center gap-1.5 text-fg-dim">
          <span className="h-2 w-2 rounded-sm bg-white/10" /> idle <span className="font-mono">{Math.max(0, total - legend.assigned)}</span>
        </span>
        <span className="ml-auto flex items-center gap-2 font-mono text-fg-muted">
          load1 <span className="text-fg">{fmtInt(compute.load1)}</span> / {total}
          <span className="relative inline-block h-1 w-16 overflow-hidden rounded-full bg-white/10">
            <span className="absolute inset-y-0 left-0 rounded-full bg-cyan/70" style={{ width: `${loadPct * 100}%` }} />
          </span>
        </span>
      </div>
    </div>
  )
}


export function ModalFleet({ compute }: { compute: ComputeState }) {
  const m = compute.modal
  if (!m) return null
  const entries = Object.entries(m.by_problem || {}).filter(([, n]) => n > 0).sort((a, b) => b[1] - a[1])
  const cells: (string | null)[] = []
  for (const [slug, n] of entries) for (let i = 0; i < n && cells.length < m.max; i++) cells.push(slug)
  while (cells.length < m.max) cells.push(null)
  return (
    <div>
      <div className="mb-2 flex items-baseline justify-between label">
        <span>Modal fleet (elastic, planner-controlled)</span>
        <span className="font-mono normal-case tracking-normal text-fg">{m.containers}/{m.max} containers</span>
      </div>
      <div className="grid gap-[3px]" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(9px, 1fr))' }}>
        {cells.map((slug, i) => {
          const color = problemColor(slug)
          return (
            <div key={i} title={slug ? `modal container ${i}: ${slug}` : 'free slot'}
              className={cx('aspect-square rounded-full transition-colors duration-700', slug && 'cpu-cell')}
              style={{ background: slug ? color : 'rgba(255,255,255,0.04)', boxShadow: slug ? `0 0 5px ${color}66` : undefined,
                       animationDelay: `${(i * 211) % 3000}ms` }} />
          )
        })}
      </div>
      <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-fg-dim">
        {entries.map(([slug, n]) => (
          <span key={slug} className="inline-flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full" style={{ background: problemColor(slug) }} />
            {slug} <span className="font-mono text-fg">{n}</span>
          </span>
        ))}
        {m.error ? <span className="text-amber">telemetry: {m.error}</span> : null}
      </div>
    </div>
  )
}
