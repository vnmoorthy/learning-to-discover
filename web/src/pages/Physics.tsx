import { motion } from 'framer-motion'
import { useState } from 'react'
import { api } from '../api'
import { Empty, ErrorNote, Panel, Skeleton } from '../components/ui'
import { useApi } from '../hooks/useApi'
import { assetUrl } from '../mode'
import type { EHCycle } from '../types'

const CLASS_LABEL: Record<string, string> = {
  '1': 'reproduction',
  '2': 'verified known relation',
  '3': 'new computational observation',
  '4': 'new conjecture',
  '5': 'potentially novel (needs work)',
}
function classOf(c: unknown) {
  const k = String(c ?? '').trim().charAt(0)
  return CLASS_LABEL[k] ? `${k} · ${CLASS_LABEL[k]}` : String(c ?? '')
}
function txt(v: unknown): string {
  if (v == null) return ''
  if (typeof v === 'string') return v
  if (Array.isArray(v)) return v.map(txt).join(' · ')
  return JSON.stringify(v)
}

function Cycle({ c, i }: { c: EHCycle; i: number }) {
  const [open, setOpen] = useState(i === 0)
  const rows: [string, unknown][] = [
    ['Hypothesis', c.hypothesis],
    ['Derivation', c.derivation_summary],
    ['Prediction', c.prediction],
    ['Result', c.result],
    ['Independent verification', c.verification],
    ['Critic', c.critic_objections],
    ['Revised hypothesis', c.revised_hypothesis],
    ['Conclusion', c.conclusion],
  ]
  return (
    <div className="rounded-xl border border-white/[0.07] bg-white/[0.02]">
      <button onClick={() => setOpen(!open)} className="flex w-full items-start justify-between gap-3 px-4 py-3 text-left">
        <div className="min-w-0">
          <div className="font-mono text-[10px] uppercase tracking-[0.14em] text-fg-dim">cycle {String(c.id ?? i + 1)}</div>
          <div className="mt-0.5 text-sm text-fg">{txt(c.question)}</div>
        </div>
        {c.classification != null && (
          <span className="shrink-0 rounded-full border border-cyan/30 bg-cyan/10 px-2 py-0.5 text-[10px] text-cyan">{classOf(c.classification)}</span>
        )}
      </button>
      {open && (
        <dl className="grid gap-2 border-t border-white/[0.06] px-4 py-3 text-[13px] sm:grid-cols-[170px_1fr]">
          {rows.filter(([, v]) => txt(v)).map(([k, v]) => (
            <div key={k} className="contents">
              <dt className="text-[11px] uppercase tracking-[0.1em] text-fg-dim">{k}</dt>
              <dd className="whitespace-pre-wrap text-fg-muted">{txt(v)}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  )
}

export default function PhysicsPage() {
  const ph = useApi(() => api.physics(), [], 60000)
  const tb = ph.data?.threebody
  const eh = ph.data?.event_horizon
  return (
    <div className="space-y-5">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight">Physics</h1>
        <p className="mt-1 max-w-3xl text-sm text-fg-muted">
          The same loop, pointed beyond EinsteinArena: an open problem in celestial mechanics (periodic orbits of the three-body
          problem) and EVENT HORIZON, a verified quantum-information study of the black hole information problem on the A100s.
          Every claim below is classified; nothing here claims to settle an open problem.
        </p>
      </div>
      {ph.error && !ph.data && <ErrorNote error={ph.error} onRetry={ph.reload} />}
      {ph.loading && !ph.data ? (
        <Skeleton className="h-96" />
      ) : (
        <>
          <Panel
            title="Three-body periodic orbits · candidates"
            subtitle={tb ? `${tb.orbits.length} verified periodic orbits whose topological families are absent from the ${tb.catalog_entries.toLocaleString()} catalogued orbits checked` : 'no data'}
            right={tb?.score != null ? <span className="rounded-full border border-amber-300/30 bg-amber-300/10 px-2 py-0.5 font-mono text-[11px] text-amber-200">{tb.score} candidate families</span> : null}
          >
            {!tb ? (
              <Empty>No verified orbits yet.</Empty>
            ) : (
              <div className="grid gap-5 lg:grid-cols-[1.4fr_1fr]">
                <motion.img initial={{ opacity: 0 }} animate={{ opacity: 1 }} src={assetUrl(tb.image)} alt="candidate orbits" className="w-full rounded-xl border border-white/[0.06]" />
                <div className="space-y-3 text-[13px]">
                  <table className="w-full font-mono text-[12px]">
                    <thead className="text-fg-dim">
                      <tr><th className="text-left">#</th><th className="text-right">vx</th><th className="text-right">vy</th><th className="text-right">T</th><th className="text-right">m3</th></tr>
                    </thead>
                    <tbody>
                      {tb.orbits.map((o, i) => (
                        <tr key={i} className="border-t border-white/[0.05]">
                          <td>{i + 1}</td>
                          <td className="text-right">{o.vx.toFixed(6)}</td>
                          <td className="text-right">{o.vy.toFixed(6)}</td>
                          <td className="text-right">{o.T.toFixed(4)}</td>
                          <td className="text-right">{o.m3 ?? 1}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {tb.verification && <p className="text-fg-muted"><span className="text-fg">Verification:</span> {tb.verification}</p>}
                  {tb.novelty && <p className="text-fg-muted"><span className="text-fg">What “candidate” means:</span> {tb.novelty}</p>}
                  {tb.caveats && <p className="text-fg-dim">{tb.caveats}</p>}
                </div>
              </div>
            )}
          </Panel>
          <Panel
            title="EVENT HORIZON · black hole information"
            subtitle={eh?.question ?? 'Page curve, Page’s theorem, sequential evaporation, Bell-pair toy model, scrambling and Hayden-Preskill'}
            right={
              eh?.tests ? (
                <span className="rounded-full border border-emerald-300/30 bg-emerald-300/10 px-2 py-0.5 font-mono text-[11px] text-emerald-200">
                  tests {eh.tests.passed ?? '?'}/{eh.tests.total ?? '?'} passed
                </span>
              ) : null
            }
          >
            {!eh ? (
              <Empty>EVENT HORIZON results are still being produced on the A100 (GPU 0).</Empty>
            ) : (
              <div className="space-y-5">
                {eh.summary && <p className="max-w-4xl text-sm text-fg-muted">{eh.summary}</p>}
                {eh.hardware && <p className="font-mono text-[11px] text-fg-dim">hardware: {eh.hardware}</p>}
                <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                  {(eh.figures ?? []).map((f, i) => (
                    <figure key={i} className="overflow-hidden rounded-xl border border-white/[0.06] bg-black/30">
                      <img src={assetUrl(f.src ?? '')} alt={f.title} className="w-full" loading="lazy" />
                      <figcaption className="space-y-1 px-3 py-2 text-[12px]">
                        <div className="text-fg">{f.title}</div>
                        {f.caption && <div className="text-fg-dim">{f.caption}</div>}
                        {f.classification != null && <div className="text-cyan">{classOf(f.classification)}</div>}
                      </figcaption>
                    </figure>
                  ))}
                </div>
                <div className="space-y-2">
                  <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Research cycles</div>
                  {(eh.cycles ?? []).map((c, i) => <Cycle key={i} c={c} i={i} />)}
                </div>
              </div>
            )}
          </Panel>
        </>
      )}
    </div>
  )
}
