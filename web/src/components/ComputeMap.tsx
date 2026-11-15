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
  const body = (
    <div className={cx('h-full rounded-lg border border-white/[0.07] bg-white/[0.02] p-3 transition-colors duration-150', g.problem && 'hover:border-white/[0.14] hover:bg-white/[0.035]')}>
      <div className="flex items-baseline justify-between gap-2">
        <div className="text-[11px] font-medium text-fg-dim">GPU {g.idx}</div>
        <div className="font-mono text-[12px] font-medium tabular-nums text-fg">
          {util}
          <span className="text-fg-dim">%</span>
        </div>
      </div>
      <div className="mt-2 flex items-center gap-1.5">
        <span className="h-2 w-2 shrink-0 rounded-[2px]" style={{ background: g.problem ? color : 'rgba(255,255,255,0.12)' }} />
        <span className={cx('truncate text-[12.5px] font-medium', g.problem ? 'text-fg' : 'text-fg-dim')}>{g.problem ? shortName(g.problem) : 'Free'}</span>
      </div>
      <div className="mt-0.5 truncate font-mono text-[10.5px] text-fg-dim" title={(g.strategy_ids ?? [g.strategy_id]).filter(Boolean).join(', ')}>
        {g.strategy_id ?? '--'}
        {g.strategy_ids && g.strategy_ids.length > 1 && <span className="text-fg-muted"> +{g.strategy_ids.length - 1}</span>}
      </div>
      <div className="mt-3" title={`utilization ${util}%`}>
        <div className="h-[3px] overflow-hidden rounded-full bg-white/[0.07]">
          <motion.div className="h-full rounded-full" style={{ background: g.problem ? color : '#3A424F' }} initial={false} animate={{ width: `${util}%` }} transition={{ duration: 0.25, ease: 'easeOut' }} />
        </div>
        <div className="mt-1.5 font-mono text-[10.5px] text-fg-dim">{(mem / 1024).toFixed(1)} / {(A100_MB / 1024).toFixed(0)} GB</div>
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
      <div className="grid gap-[3px]" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(12px, 1fr))' }}>
        {cells.map((slug, i) => {
          const color = problemColor(slug)
          return (
            <div
              key={i}
              title={slug ? `core ${i}: ${slug}` : `core ${i}: idle`}
              className="aspect-square rounded-[2px] transition-colors duration-200"
              style={{
                background: slug ? color : 'rgba(255,255,255,0.06)',
                opacity: slug ? 0.85 : 1,
              }}
            />
          )
        })}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-[11.5px]">
        {legend.entries.map(([slug, n]) => (
          <Link key={slug} to={`/problems/${slug}`} className="flex items-center gap-1.5 text-fg-muted hover:text-fg">
            <span className="h-2 w-2 rounded-[2px]" style={{ background: problemColor(slug) }} />
            <span>{shortName(slug)}</span>
            <span className="font-mono text-fg">{n}</span>
          </Link>
        ))}
        <span className="flex items-center gap-1.5 text-fg-dim">
          <span className="h-2 w-2 rounded-[2px] bg-white/10" /> Idle <span className="font-mono">{Math.max(0, total - legend.assigned)}</span>
        </span>
        <span className="ml-auto flex items-center gap-2 font-mono text-fg-muted">
          load1 <span className="text-fg">{fmtInt(compute.load1)}</span> / {total}
          <span className="relative inline-block h-1 w-16 overflow-hidden rounded-full bg-white/10">
            <span className="absolute inset-y-0 left-0 rounded-full bg-fg-muted" style={{ width: `${loadPct * 100}%` }} />
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
      <div className="label mb-2 flex items-baseline justify-between">
        <span>Modal fleet (elastic, planner-controlled)</span>
        <span className="font-mono text-fg-muted"><span className="text-fg">{m.containers}</span> / {m.max} containers</span>
      </div>
      <div className="grid gap-[3px]" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(9px, 1fr))' }}>
        {cells.map((slug, i) => {
          const color = problemColor(slug)
          return (
            <div key={i} title={slug ? `modal container ${i}: ${slug}` : 'free slot'}
              className="aspect-square rounded-[2px] transition-colors duration-200"
              style={{ background: slug ? color : 'rgba(255,255,255,0.06)', opacity: slug ? 0.85 : 1 }} />
          )
        })}
      </div>
      <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1.5 text-[11.5px] text-fg-muted">
        {entries.map(([slug, n]) => (
          <span key={slug} className="inline-flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-[2px]" style={{ background: problemColor(slug) }} />
            {shortName(slug)} <span className="font-mono text-fg">{n}</span>
          </span>
        ))}
        {m.error ? <span className="text-amber">telemetry: {m.error}</span> : null}
      </div>
    </div>
  )
}
