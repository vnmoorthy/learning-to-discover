import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { agentColor, clockTime, cx, fmtInt, fmtMs, fmtScore, problemColor, safeHref, timeAgo } from '../lib/format'
import type { Decision } from '../types'
import { IconChevron, IconExternal } from './icons'
import { Chip, Verdict } from './ui'

function AgentTag({ agent }: { agent: string }) {
  const c = agentColor(agent)
  return (
    <span className="inline-flex items-center gap-1.5 rounded-md px-1.5 py-0.5 font-mono text-[10.5px] font-semibold uppercase tracking-wider" style={{ color: c, background: c + '14', border: `1px solid ${c}33` }}>
      {agent}
    </span>
  )
}

export function FeedItem({ d }: { d: Decision }) {
  return (
    <Link to={`/decisions?focus=${d.id}`} className="group block rounded-xl border border-white/[0.05] bg-white/[0.015] px-3 py-2.5 transition-colors hover:border-cyan/25 hover:bg-cyan/[0.03]">
      <div className="flex items-center gap-2">
        <AgentTag agent={d.agent} />
        <span className="truncate font-mono text-[11.5px] text-fg">{d.action}</span>
        {d.outcome && d.outcome.verdict !== 'n/a' && <Verdict verdict={d.outcome.verdict} />}
        <span className="ml-auto shrink-0 font-mono text-[10px] text-fg-dim" title={d.time}>
          {timeAgo(d.time)}
        </span>
      </div>
      {d.problem && (
        <div className="mt-1 truncate font-mono text-[10.5px]" style={{ color: problemColor(d.problem) }}>
          {d.problem}
        </div>
      )}
      <p className="mt-1 line-clamp-2 text-[12px] leading-snug text-fg-muted group-hover:text-fg">{d.rationale}</p>
    </Link>
  )
}

function ParamList({ params }: { params: Record<string, unknown> }) {
  const entries = Object.entries(params || {})
  if (!entries.length) return null
  return (
    <div className="flex flex-wrap gap-1.5">
      {entries.map(([k, v]) => (
        <span key={k} className="rounded-md border border-white/[0.07] bg-black/20 px-1.5 py-0.5 font-mono text-[10.5px] text-fg-muted">
          {k}=<span className="text-fg">{typeof v === 'object' ? JSON.stringify(v) : String(v)}</span>
        </span>
      ))}
    </div>
  )
}

export function DecisionCard({ d, defaultOpen = false, highlight = false }: { d: Decision; defaultOpen?: boolean; highlight?: boolean }) {
  const [open, setOpen] = useState(defaultOpen)
  const pred = d.prediction
  const out = d.outcome
  return (
    <motion.article
      layout="position"
      id={`decision-${d.id}`}
      className={cx('panel overflow-hidden rounded-xl transition-colors', highlight && '!border-cyan/50 shadow-glow')}
    >
      <button onClick={() => setOpen((o) => !o)} className="flex w-full items-start gap-3 px-4 py-3 text-left hover:bg-white/[0.015]" aria-expanded={open}>
        <IconChevron className={cx('mt-0.5 h-4 w-4 shrink-0 text-fg-dim transition-transform', open && 'rotate-90 text-cyan')} />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-[10.5px] text-fg-dim">#{d.id}</span>
            <AgentTag agent={d.agent} />
            <span className="font-mono text-[12.5px] font-semibold text-fg">{d.action}</span>
            {d.problem && (
              <Chip color={problemColor(d.problem)} className="max-w-[220px]">
                {d.problem}
              </Chip>
            )}
            {out && out.verdict !== 'n/a' && <Verdict verdict={out.verdict} />}
            {d.sources.length > 0 && <span className="font-mono text-[10px] text-[#E9E36B]">{d.sources.length} src</span>}
            <span className="ml-auto font-mono text-[10.5px] text-fg-dim" title={d.time}>
              cycle {d.cycle} | {clockTime(d.time)} | {timeAgo(d.time)}
            </span>
          </div>
          <p className={cx('mt-1.5 text-[13px] leading-relaxed text-fg-muted', !open && 'line-clamp-2')}>{d.rationale}</p>
        </div>
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.22 }}>
            <div className="space-y-4 border-t border-white/[0.05] px-4 py-4 pl-11">
              {Object.keys(d.params || {}).length > 0 && (
                <Section label="Params">
                  <ParamList params={d.params} />
                </Section>
              )}
              {(pred || out) && (
                <Section label="Prediction vs outcome">
                  <div className="grid gap-2 sm:grid-cols-2">
                    <div className="rounded-lg border border-white/[0.06] bg-black/20 p-3">
                      <div className="text-[10px] uppercase tracking-wider text-fg-dim">predicted</div>
                      {pred ? (
                        <div className="mt-1 font-mono text-[12.5px] text-fg">
                          {pred.metric} = <span className="text-cyan">{fmtScore(pred.expected)}</span>
                          <span className="text-fg-dim"> within {pred.horizon_min} min</span>
                        </div>
                      ) : (
                        <div className="mt-1 text-xs text-fg-dim">no prediction</div>
                      )}
                    </div>
                    <div className="rounded-lg border border-white/[0.06] bg-black/20 p-3">
                      <div className="flex items-center gap-2 text-[10px] uppercase tracking-wider text-fg-dim">
                        observed <Verdict verdict={out?.verdict ?? 'pending'} />
                      </div>
                      <div className="mt-1 font-mono text-[12.5px] text-fg">{out?.observed != null ? fmtScore(out.observed) : '--'}</div>
                      {out?.note && <div className="mt-0.5 text-[11.5px] text-fg-muted">{out.note}</div>}
                    </div>
                  </div>
                </Section>
              )}
              {d.sources.length > 0 && (
                <Section label="Sources (Exa)">
                  <ul className="space-y-1.5">
                    {d.sources.map((s) => (
                      <li key={s.id}>
                        <a href={safeHref(s.url)} target="_blank" rel="noopener noreferrer" className="group inline-flex items-start gap-1.5 text-[12.5px] text-cyan hover:underline">
                          <IconExternal className="mt-1 h-3 w-3 shrink-0" />
                          <span>{s.title}</span>
                          {s.published && <span className="font-mono text-[10.5px] text-fg-dim">{s.published.slice(0, 10)}</span>}
                        </a>
                      </li>
                    ))}
                  </ul>
                </Section>
              )}
              {(d.memory_reads.length > 0 || d.memory_writes.length > 0) && (
                <Section label="Memory">
                  <div className="flex flex-wrap items-center gap-1.5">
                    {d.memory_reads.map((f) => (
                      <Link key={'r' + f} to={`/memory?fact=${encodeURIComponent(f)}`}>
                        <Chip color="#A98BFF">read {f}</Chip>
                      </Link>
                    ))}
                    {d.memory_writes.map((f) => (
                      <Link key={'w' + f} to={`/memory?fact=${encodeURIComponent(f)}`}>
                        <Chip color="#6CF29A">wrote {f}</Chip>
                      </Link>
                    ))}
                  </div>
                </Section>
              )}
              <div className="flex flex-wrap gap-x-5 gap-y-1 font-mono text-[11px] text-fg-dim">
                <span>
                  model <span className="text-fg-muted">{d.model ?? 'deterministic'}</span>
                </span>
                <span>
                  tokens <span className="text-fg-muted">{fmtInt(d.tokens)}</span>
                </span>
                <span>
                  latency <span className="text-fg-muted">{fmtMs(d.latency_ms)}</span>
                </span>
                <span>{d.time}</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.article>
  )
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">{label}</div>
      {children}
    </div>
  )
}
