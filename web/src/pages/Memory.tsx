import { motion } from 'framer-motion'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { api, ensureOk } from '../api'
import { axisProps, tooltipStyle } from '../components/charts'
import { useToast } from '../components/Toast'
import { ActionButton, Chip, Empty, ErrorNote, Panel, Skeleton, Spinner } from '../components/ui'
import { useAction, useApi } from '../hooks/useApi'
import { agentColor, cx, dateTime, fmtMs, fmtPct, fmtUsd, problemColor, timeAgo } from '../lib/format'
import type { MemoryResponse } from '../types'

function AgentGraph({ mem, selected, onSelect }: { mem: MemoryResponse; selected: string | null; onSelect: (a: string | null) => void }) {
  const W = 640
  const H = 460
  const { nodes, edges } = useMemo(() => {
    const names = new Set<string>(mem.agents)
    for (const l of mem.links) {
      names.add(l.from_agent)
      names.add(l.to_agent)
    }
    for (const f of mem.facts) names.add(f.agent)
    const list = [...names]
    // core agents in the middle ring, per-problem agents on the outer ring
    const core = list.filter((a) => !a.startsWith('agent:'))
    const outer = list.filter((a) => a.startsWith('agent:'))
    const pos: Record<string, { x: number; y: number }> = {}
    const cx0 = W / 2
    const cy0 = H / 2
    core.forEach((a, i) => {
      const t = (i / Math.max(1, core.length)) * Math.PI * 2 - Math.PI / 2
      const r = core.length > 1 ? 92 : 0
      pos[a] = { x: cx0 + r * Math.cos(t), y: cy0 + r * Math.sin(t) }
    })
    outer.forEach((a, i) => {
      const t = (i / Math.max(1, outer.length)) * Math.PI * 2 - Math.PI / 2 + Math.PI / Math.max(1, outer.length)
      pos[a] = { x: cx0 + 250 * Math.cos(t), y: cy0 + 178 * Math.sin(t) }
    })
    const written: Record<string, number> = {}
    for (const f of mem.facts) written[f.agent] = (written[f.agent] ?? 0) + 1
    const nodes = list.map((a) => ({ id: a, ...pos[a], written: written[a] ?? 0 }))
    const agg = new Map<string, { from: string; to: string; n: number }>()
    for (const l of mem.links) {
      if (l.from_agent === l.to_agent) continue
      const k = `${l.from_agent}->${l.to_agent}`
      const e = agg.get(k) ?? { from: l.from_agent, to: l.to_agent, n: 0 }
      e.n++
      agg.set(k, e)
    }
    return { nodes, edges: [...agg.values()], pos }
  }, [mem])
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]))
  const maxN = Math.max(1, ...edges.map((e) => e.n))
  const maxW = Math.max(1, ...nodes.map((n) => n.written))

  return (
    <div className="relative">
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="agent memory graph">
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="rgba(169,139,255,0.8)" />
          </marker>
          <radialGradient id="nodeglow">
            <stop offset="0%" stopColor="white" stopOpacity="0.25" />
            <stop offset="100%" stopColor="white" stopOpacity="0" />
          </radialGradient>
        </defs>
        {edges.map((e) => {
          const a = byId[e.from]
          const b = byId[e.to]
          if (!a || !b) return null
          const dx = b.x - a.x
          const dy = b.y - a.y
          const len = Math.hypot(dx, dy) || 1
          const rb = 12 + (b.written / maxW) * 10
          const ex = b.x - (dx / len) * (rb + 4)
          const ey = b.y - (dy / len) * (rb + 4)
          const mx = (a.x + ex) / 2 - (dy / len) * 26
          const my = (a.y + ey) / 2 + (dx / len) * 26
          const active = !selected || selected === e.from || selected === e.to
          const w = 0.8 + (e.n / maxN) * 3
          return (
            <g key={e.from + e.to} opacity={active ? 1 : 0.1}>
              <path d={`M${a.x},${a.y} Q${mx},${my} ${ex},${ey}`} fill="none" stroke="rgba(169,139,255,0.35)" strokeWidth={w} markerEnd="url(#arrow)" />
              <path d={`M${a.x},${a.y} Q${mx},${my} ${ex},${ey}`} fill="none" stroke={agentColor(e.from)} strokeWidth={Math.max(1, w * 0.6)} strokeDasharray="3 14" className="flow-dash" opacity={0.9} />
              <title>
                {e.to} read {e.n} fact(s) written by {e.from}
              </title>
            </g>
          )
        })}
        {nodes.map((n) => {
          const c = agentColor(n.id)
          const r = 12 + (n.written / maxW) * 10
          const on = selected === n.id
          const dim = selected && !on && !edges.some((e) => (e.from === selected && e.to === n.id) || (e.to === selected && e.from === n.id))
          return (
            <g key={n.id} transform={`translate(${n.x},${n.y})`} className="cursor-pointer" onClick={() => onSelect(on ? null : n.id)} opacity={dim ? 0.3 : 1}>
              <circle r={r * 2.2} fill="url(#nodeglow)" />
              <circle r={r} fill={c + '26'} stroke={c} strokeWidth={on ? 2.5 : 1.5} />
              <text y={4} textAnchor="middle" fontSize="11" className="font-mono" fill={c} fontWeight={600}>
                {n.written}
              </text>
              <text y={r + 15} textAnchor="middle" fontSize="11" className="font-mono" fill="#C5CAD1" stroke="#0E1014" strokeWidth={4} paintOrder="stroke">
                {n.id.replace('agent:', '')}
              </text>
            </g>
          )
        })}
      </svg>
      <div className="mt-1 text-[11px] text-fg-dim">
        Nodes are agents (number = facts written). An arrow A to B means B read a fact that A wrote, through the shared past.dev space. Click a node to filter.
      </div>
    </div>
  )
}

function Benchmark({ mem, onRefresh }: { mem: MemoryResponse; onRefresh: () => Promise<MemoryResponse | null> }) {
  const toast = useToast()
  const a = useAction(async () => ensureOk(await api.runMemoryBenchmark()))
  const [waiting, setWaiting] = useState(false)
  const startTime = useRef<string | null>(null)
  const b = mem.benchmark

  const run = async () => {
    startTime.current = b?.time ?? null
    const r = await a.run()
    if (!r) return toast.push({ kind: 'error', title: 'Benchmark failed to start', msg: a.lastError() ?? '' })
    toast.push({ kind: 'info', title: 'Memory benchmark started', msg: 'past.dev vs markdown vs RAG' })
    setWaiting(true)
  }

  useEffect(() => {
    if (!waiting) return
    const started = Date.now()
    const t = setInterval(async () => {
      const m = await onRefresh()
      if (m?.benchmark && m.benchmark.time !== startTime.current) {
        setWaiting(false)
        toast.push({ kind: 'success', title: 'Benchmark finished' })
      } else if (Date.now() - started > 10 * 60 * 1000) {
        setWaiting(false)
        toast.push({ kind: 'error', title: 'Benchmark still running after 10 min', msg: 'results will appear when it finishes' })
      }
    }, 3000)
    return () => clearInterval(t)
  }, [waiting, onRefresh, toast])

  const sysColor = (n: string) => (n === 'past.dev' ? '#4FD1E0' : n === 'rag' ? '#A99BEA' : '#9BA3AF')
  const charts: { key: 'accuracy' | 'latency_ms' | 'cost_usd'; label: string; fmt: (v: number) => string; better: string }[] = [
    { key: 'accuracy', label: 'Accuracy', fmt: (v) => fmtPct(v, 0), better: 'higher is better' },
    { key: 'latency_ms', label: 'Latency', fmt: fmtMs, better: 'lower is better' },
    { key: 'cost_usd', label: 'Cost / query', fmt: fmtUsd, better: 'lower is better' },
  ]

  return (
    <Panel
      title="Memory benchmark"
      subtitle={b ? `QA over the lab's own facts, LLM-judged | ${dateTime(b.time)} (${timeAgo(b.time)})` : 'past.dev vs markdown file vs RAG'}
      right={
        <ActionButton variant="primary" onClick={run} status={waiting ? 'loading' : a.status} error={a.error} successLabel="Started">
          {waiting ? 'Running' : 'Run benchmark'}
        </ActionButton>
      }
    >
      {waiting && (
        <div className="mb-4 flex items-center gap-2 rounded-lg border border-cyan/20 bg-cyan/[0.05] px-3 py-2 text-xs text-cyan">
          <Spinner className="h-3.5 w-3.5" /> Benchmark running on the server; results refresh automatically.
        </div>
      )}
      {!b ? (
        <Empty>No benchmark has been run yet.</Empty>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            {charts.map((c) => (
              <div key={c.key} className="rounded-xl border border-white/[0.05] bg-black/20 p-3">
                <div className="flex items-baseline justify-between">
                  <div className="text-[11px] font-semibold text-fg">{c.label}</div>
                  <div className="text-[10px] text-fg-dim">{c.better}</div>
                </div>
                <div className="mt-2 h-40">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={b.systems} margin={{ top: 16, right: 4, left: -8, bottom: 0 }}>
                      <XAxis dataKey="name" {...axisProps} />
                      <YAxis {...axisProps} width={48} tickFormatter={(v) => c.fmt(v)} />
                      <Tooltip {...tooltipStyle} cursor={{ fill: 'rgba(255,255,255,0.03)' }} formatter={(v: number) => [c.fmt(v), c.label]} />
                      <Bar dataKey={c.key} radius={[6, 6, 0, 0]} isAnimationActive label={{ position: 'top', fill: '#C5CAD1', fontSize: 10.5, formatter: (v: number) => c.fmt(v) }}>
                        {b.systems.map((s) => (
                          <Cell key={s.name} fill={sysColor(s.name)} fillOpacity={s.name === 'past.dev' ? 0.95 : 0.55} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[460px] text-left text-[12.5px]">
              <thead>
                <tr className="border-b border-white/[0.06] text-[11px] font-medium text-fg-dim">
                  <th className="py-2 font-semibold">System</th>
                  <th className="py-2 text-right font-semibold">Accuracy</th>
                  <th className="py-2 text-right font-semibold">Latency</th>
                  <th className="py-2 text-right font-semibold">Cost / query</th>
                  <th className="py-2 text-right font-semibold">Questions</th>
                </tr>
              </thead>
              <tbody className="font-mono">
                {b.systems.map((s) => (
                  <tr key={s.name} className="border-b border-white/[0.04]">
                    <td className="py-2" style={{ color: sysColor(s.name) }}>
                      {s.name}
                    </td>
                    <td className="py-2 text-right">{fmtPct(s.accuracy, 1)}</td>
                    <td className="py-2 text-right">{fmtMs(s.latency_ms)}</td>
                    <td className="py-2 text-right">{fmtUsd(s.cost_usd)}</td>
                    <td className="py-2 text-right text-fg-muted">{s.n}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </Panel>
  )
}

export default function MemoryPage() {
  const mem = useApi(() => api.memory(), [], 15000)
  const [sp] = useSearchParams()
  const focusFact = sp.get('fact')
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    if (!focusFact || !mem.data) return
    const el = document.getElementById(`fact-${focusFact}`)
    if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'center' }), 200)
  }, [focusFact, mem.data])

  const refreshMem = useMemo(
    () => async () => {
      try {
        const m = await api.memory()
        mem.setData(m)
        return m
      } catch {
        return null
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  )

  if (mem.error && !mem.data) return <ErrorNote error={mem.error} onRetry={mem.reload} />
  if (!mem.data)
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-96" />
      </div>
    )
  const m = mem.data
  const facts = [...m.facts].filter((f) => !selected || f.agent === selected || f.read_by.includes(selected)).sort((a, b) => Date.parse(b.time) - Date.parse(a.time))

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-[22px] font-semibold leading-7 tracking-[-0.02em]">Multi-agent memory</h1>
        <p className="mt-1.5 max-w-3xl text-[14px] leading-6 text-fg-muted">
          Planner, proposer, critic and one agent per problem share one past.dev space. Facts written by one agent are recalled by others; every read is recorded.
        </p>
      </div>
      <div className="grid gap-5 xl:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]">
        <Panel title="Agent graph" subtitle={`${m.agents.length} agents | ${m.facts.length} facts | ${m.links.length} reads`} right={selected && <button onClick={() => setSelected(null)} className="text-xs text-cyan hover:underline">Clear filter</button>}>
          <AgentGraph mem={m} selected={selected} onSelect={setSelected} />
        </Panel>
        <Panel title="Facts" subtitle={selected ? `written or read by ${selected}` : 'newest first'} bodyClass="p-3">
          <div className="max-h-[520px] space-y-2 overflow-y-auto pr-1">
            {facts.length === 0 && <Empty>No facts</Empty>}
            {facts.map((f) => (
              <motion.div
                layout
                key={f.id}
                id={`fact-${f.id}`}
                className={cx('rounded-xl border bg-white/[0.015] px-3 py-2.5', focusFact === f.id ? 'border-cyan/50 shadow-glow' : 'border-white/[0.05]')}
              >
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="font-mono text-[10.5px] text-fg-dim">{f.id}</span>
                  <Chip color={agentColor(f.agent)}>{f.agent}</Chip>
                  {f.problem && <Chip color={problemColor(f.problem)}>{f.problem}</Chip>}
                  <span className="ml-auto font-mono text-[10px] text-fg-dim" title={f.time}>
                    {timeAgo(f.time)}
                  </span>
                </div>
                <p className="mt-1.5 text-[12.5px] leading-relaxed text-fg-muted">{f.text}</p>
                {f.read_by.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap items-center gap-1 text-[10.5px] text-fg-dim">
                    read by
                    {f.read_by.map((r) => (
                      <Chip key={r} color={agentColor(r)}>
                        {r.replace('agent:', '')}
                      </Chip>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </Panel>
      </div>
      <Benchmark mem={m} onRefresh={refreshMem} />
    </div>
  )
}
