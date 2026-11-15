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
    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: Math.min(0.02 * index, 0.16), duration: 0.2 }}>
      <Link
        to={`/problems/${p.slug}`}
        className={cx('panel panel-hover group relative flex h-full flex-col overflow-hidden rounded-xl p-4', record && '!border-amber/30')}
      >
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 font-mono text-[11px] text-fg-dim">
              <span className="h-2 w-2 shrink-0 rounded-[2px]" style={{ background: color }} />
              <span className="truncate">{p.slug}</span>
            </div>
            <div className="mt-1 line-clamp-2 text-[13.5px] font-semibold leading-snug tracking-[-0.01em] text-fg">{p.title}</div>
          </div>
          <StatusBadge status={record ? 'record' : p.status} />
        </div>

        <div className="mt-4 grid grid-cols-2 gap-3">
          <div className="min-w-0">
            <div className="label">Record</div>
            <div className="mt-0.5 truncate font-mono text-[15px] font-medium text-fg-muted" title={String(p.record.score)}>
              {fmtScore(p.record.score)}
            </div>
            <div className="truncate text-[10.5px] text-fg-dim">{p.record.holder}</div>
          </div>
          <div className="min-w-0">
            <div className="label">Ours</div>
            <div className={cx('mt-0.5 truncate font-mono text-[15px] font-medium', record ? 'text-amber' : p.ours ? 'text-fg' : 'text-fg-dim')} title={p.ours ? String(p.ours.score) : ''}>
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

        <div className="mt-4 rounded-lg border border-white/[0.06] bg-ink-850 px-3 pb-2 pt-2">
          <div className="flex items-baseline justify-between gap-2">
            <span className="truncate font-mono text-[10.5px] text-fg-muted">{m.name}</span>
            <span className="font-mono text-[12.5px] font-medium text-fg">
              {fmtScore(m.value)}
              {m.target != null && <span className="text-[10.5px] font-normal text-fg-dim"> / {fmtScore(m.target)}</span>}
            </span>
          </div>
          <Sparkline data={series ?? []} color={color} height={34} className="mt-1" target={m.target} />
        </div>

        <div className="mt-auto pt-3">
          <div className="flex items-center justify-between text-[11px] text-fg-muted">
            <span className="font-mono">
              {p.compute.gpus > 0 && <span>{p.compute.gpus} GPU</span>}
              {p.compute.gpus > 0 && p.compute.cpu_procs > 0 && ' '}
              {p.compute.cpu_procs > 0 && <span>{p.compute.cpu_procs} cores</span>}
              {p.compute.gpus === 0 && p.compute.cpu_procs === 0 && <span>no compute</span>}
              <span className="text-fg-dim"> | {p.strategies.length} strategies</span>
            </span>
            <span className="font-mono">{fmtPct(p.compute.share)}</span>
          </div>
          <div className="mt-1.5 h-[3px] overflow-hidden rounded-full bg-white/[0.07]">
            <motion.div className="h-full rounded-full" style={{ background: color }} initial={{ width: 0 }} animate={{ width: `${Math.min(100, p.compute.share * 100)}%` }} transition={{ duration: 0.25 }} />
          </div>
        </div>
      </Link>
    </motion.div>
  )
}
