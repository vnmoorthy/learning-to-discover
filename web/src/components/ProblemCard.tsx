import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { cx, fmtPct, fmtScore, gapToRecord, problemColor, timeAgo } from '../lib/format'
import type { Series } from '../live'
import type { ProblemSummary } from '../types'
import { Sparkline, StatusBadge } from './ui'

export function ProblemCard({ p, series, index = 0 }: { p: ProblemSummary; series: Series | undefined; index?: number }) {
  const color = problemColor(p.slug)
  const gap = gapToRecord(p)
  const record = p.beats_record
  const m = p.metric
  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.04 * index, duration: 0.35 }}>
      <Link
        to={`/problems/${p.slug}`}
        className={cx('panel panel-hover group relative flex h-full flex-col overflow-hidden rounded-2xl p-4', record && '!border-amber/60 shadow-amber')}
      >
        <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: `linear-gradient(90deg, ${record ? '#FFB547' : color}, transparent)` }} />
        {record && (
          <div className="absolute right-3 top-3 rounded-full bg-amber px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-ink-900">new record</div>
        )}
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <div className="truncate font-mono text-[10.5px]" style={{ color }}>
              {p.slug}
            </div>
            <div className="mt-0.5 line-clamp-2 text-[13.5px] font-semibold leading-snug text-fg">{p.title}</div>
          </div>
          {!record && <StatusBadge status={p.status} />}
        </div>

        <div className="mt-3 grid grid-cols-2 gap-3">
          <div className="min-w-0">
            <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Record</div>
            <div className="truncate font-mono text-[15px] font-semibold text-amber" title={String(p.record.score)}>
              {fmtScore(p.record.score)}
            </div>
            <div className="truncate text-[10.5px] text-fg-dim">{p.record.holder}</div>
          </div>
          <div className="min-w-0">
            <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Ours</div>
            <div className={cx('truncate font-mono text-[15px] font-semibold', record ? 'text-amber glow-amber' : p.ours ? 'text-fg' : 'text-fg-dim')} title={p.ours ? String(p.ours.score) : ''}>
              {p.ours ? fmtScore(p.ours.score) : '--'}
            </div>
            <div className="truncate text-[10.5px] text-fg-dim">
              {p.ours ? (
                <>
                  {p.ours.verified ? 'verified' : 'unverified'} {timeAgo(p.ours.at)}
                  {gap != null && Math.abs(gap) > 0 && (
                    <span className={gap > 0 ? 'text-amber' : 'text-fg-muted'}>
                      {' '}
                      ({gap > 0 ? '+' : ''}
                      {fmtScore(gap, Math.abs(gap) < 1 ? 6 : 0)})
                    </span>
                  )}
                </>
              ) : (
                'no valid solution yet'
              )}
            </div>
          </div>
        </div>

        <div className="mt-3 rounded-xl border border-white/[0.05] bg-black/20 px-3 pb-2 pt-2">
          <div className="flex items-baseline justify-between gap-2">
            <span className="truncate font-mono text-[10.5px] text-fg-muted">{m.name}</span>
            <span className="font-mono text-[13px] font-semibold" style={{ color }}>
              {fmtScore(m.value)}
              {m.target != null && <span className="text-[10.5px] font-normal text-fg-dim"> / {fmtScore(m.target)}</span>}
            </span>
          </div>
          <Sparkline data={series ?? []} color={color} height={34} className="mt-1" target={m.target} />
        </div>

        <div className="mt-auto pt-3">
          <div className="flex items-center justify-between text-[10.5px] text-fg-muted">
            <span className="font-mono">
              {p.compute.gpus > 0 && <span>{p.compute.gpus} GPU</span>}
              {p.compute.gpus > 0 && p.compute.cpu_procs > 0 && ' '}
              {p.compute.cpu_procs > 0 && <span>{p.compute.cpu_procs} cores</span>}
              {p.compute.gpus === 0 && p.compute.cpu_procs === 0 && <span>no compute</span>}
              <span className="text-fg-dim"> | {p.strategies.length} strategies</span>
            </span>
            <span className="font-mono">{fmtPct(p.compute.share)}</span>
          </div>
          <div className="mt-1 h-1 overflow-hidden rounded-full bg-white/[0.05]">
            <motion.div className="h-full rounded-full" style={{ background: color }} initial={{ width: 0 }} animate={{ width: `${Math.min(100, p.compute.share * 100)}%` }} transition={{ duration: 0.8 }} />
          </div>
        </div>
      </Link>
    </motion.div>
  )
}
