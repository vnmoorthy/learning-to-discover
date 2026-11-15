import { useEffect, useMemo, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../api'
import { DecisionCard } from '../components/Decision'
import { ActionButton, Empty, ErrorNote, Panel, Select, Skeleton } from '../components/ui'
import { agentColor, cx } from '../lib/format'
import { useLive } from '../live'
import { AGENTS, type Decision } from '../types'

const PAGE = 50

export default function DecisionsPage() {
  const [sp, setSp] = useSearchParams()
  const problem = sp.get('problem') || ''
  const agent = sp.get('agent') || ''
  const focus = sp.get('focus') ? Number(sp.get('focus')) : null
  const [q, setQ] = useState('')
  const [verdict, setVerdict] = useState('')
  const { state, feed } = useLive()
  const [rows, setRows] = useState<Decision[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [more, setMore] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const scrolled = useRef<number | null>(null)

  const load = async () => {
    setLoading(true)
    try {
      const r = await api.decisions({ problem: problem || null, agent: agent || null, limit: focus ? 300 : PAGE })
      setRows(r)
      setMore(r.length >= (focus ? 300 : PAGE))
      setError(null)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [problem, agent])

  const loadMore = async () => {
    if (!rows.length) return
    setLoadingMore(true)
    try {
      const before = Math.min(...rows.map((d) => d.id))
      const r = await api.decisions({ problem: problem || null, agent: agent || null, limit: PAGE, before })
      setRows((x) => [...x, ...r])
      setMore(r.length >= PAGE)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoadingMore(false)
    }
  }

  const merged = useMemo(() => {
    const map = new Map<number, Decision>()
    const live = feed.filter((d) => (!problem || d.problem === problem) && (!agent || d.agent === agent))
    for (const d of [...rows, ...live]) map.set(d.id, d)
    let out = [...map.values()].sort((a, b) => b.id - a.id)
    if (verdict) out = out.filter((d) => (d.outcome?.verdict ?? 'none') === verdict)
    if (q.trim()) {
      const s = q.toLowerCase()
      out = out.filter((d) => `${d.action} ${d.rationale} ${d.problem ?? ''} ${JSON.stringify(d.params)}`.toLowerCase().includes(s))
    }
    return out
  }, [rows, feed, problem, agent, verdict, q])

  useEffect(() => {
    if (!focus || scrolled.current === focus) return
    const el = document.getElementById(`decision-${focus}`)
    if (el) {
      scrolled.current = focus
      setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'center' }), 250)
    }
  }, [focus, merged])

  const setParam = (k: string, v: string) => {
    const n = new URLSearchParams(sp)
    if (v) n.set(k, v)
    else n.delete(k)
    n.delete('focus')
    setSp(n, { replace: true })
  }

  const counts = useMemo(() => {
    const c = { confirmed: 0, refuted: 0, pending: 0 }
    for (const d of merged) if (d.outcome && d.outcome.verdict in c) c[d.outcome.verdict as keyof typeof c]++
    return c
  }, [merged])

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-[22px] font-semibold leading-7 tracking-[-0.02em]">Decision audit log</h1>
        <p className="mt-1.5 max-w-3xl text-[14px] leading-6 text-fg-muted">
          Every action any agent takes is a row: rationale, the prediction it made, what was later observed, the Exa sources it cited and the memory facts it read or wrote.
        </p>
      </div>

      <Panel bodyClass="p-3 sm:p-4">
        <div className="flex flex-wrap items-center gap-3">
          <Select
            label="problem"
            value={problem}
            onChange={(v) => setParam('problem', v)}
            options={[{ value: '', label: 'all problems' }, ...(state?.problems.map((p) => ({ value: p.slug, label: p.slug })) ?? [])]}
          />
          <Select
            label="verdict"
            value={verdict}
            onChange={setVerdict}
            options={[
              { value: '', label: 'any' },
              { value: 'confirmed', label: 'confirmed' },
              { value: 'refuted', label: 'refuted' },
              { value: 'pending', label: 'pending' },
            ]}
          />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="search rationale, action, params"
            className="h-8 min-w-0 flex-1 rounded-lg border border-white/10 bg-ink-800 px-3 text-xs text-fg outline-none placeholder:text-fg-dim focus:border-cyan/50 sm:max-w-xs"
          />
          <div className="ml-auto flex gap-3 font-mono text-[11px] text-fg-muted">
            <span>
              <span className="text-good">{counts.confirmed}</span> confirmed
            </span>
            <span>
              <span className="text-bad">{counts.refuted}</span> refuted
            </span>
            <span>
              <span className="text-amber">{counts.pending}</span> pending
            </span>
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          <button onClick={() => setParam('agent', '')} className={cx('rounded-md border px-2 py-1 font-mono text-[11px]', !agent ? 'border-cyan/40 bg-cyan/[0.08] text-cyan' : 'border-white/10 text-fg-muted hover:text-fg')}>
            all agents
          </button>
          {AGENTS.map((a) => {
            const c = agentColor(a)
            const on = agent === a
            return (
              <button
                key={a}
                onClick={() => setParam('agent', on ? '' : a)}
                className="rounded-md border px-2 py-1 font-mono text-[11px] transition-colors"
                style={on ? { color: c, borderColor: c + '66', background: c + '18' } : { color: '#9BA3AF', borderColor: 'rgba(255,255,255,0.1)' }}
              >
                {a}
              </button>
            )
          })}
        </div>
      </Panel>

      {error && <ErrorNote error={error} onRetry={load} />}
      {loading && !rows.length ? (
        <div className="space-y-2">
          {Array.from({ length: 6 }, (_, i) => (
            <Skeleton key={i} className="h-20" />
          ))}
        </div>
      ) : merged.length === 0 ? (
        <Empty>No decisions match these filters</Empty>
      ) : (
        <div className="space-y-2">
          {merged.map((d) => (
            <DecisionCard key={d.id} d={d} defaultOpen={d.id === focus} highlight={d.id === focus} />
          ))}
        </div>
      )}
      {more && rows.length > 0 && (
        <div className="flex justify-center">
          <ActionButton mutating={false} onClick={loadMore} status={loadingMore ? 'loading' : 'idle'}>
            Load older decisions
          </ActionButton>
        </div>
      )}
    </div>
  )
}
