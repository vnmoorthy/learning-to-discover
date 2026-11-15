import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, ensureOk } from '../api'
import { MetricChart } from '../components/charts'
import { DecisionCard } from '../components/Decision'
import { IconArrowLeft } from '../components/icons'
import Markdown from '../components/Markdown'
import { useToast } from '../components/Toast'
import { ActionButton, Chip, Empty, ErrorNote, Panel, Skeleton, StatusBadge } from '../components/ui'
import { useAction, useApi } from '../hooks/useApi'
import { cx, dateTime, fmtScore, gapToRecord, problemColor, timeAgo } from '../lib/format'
import { useLive } from '../live'
import { READ_ONLY } from '../mode'
import type { Artifact, Decision, ProblemDetail, Strategy, Template } from '../types'
import BitWall from '../viz/BitWall'
import IntegerSet from '../viz/IntegerSet'
import NoThreeCanvas from '../viz/NoThreeCanvas'
import SignMatrix from '../viz/SignMatrix'

function ArtifactView({ art, color }: { art: Artifact | null; color: string }) {
  if (!art) return <Empty>No artifact yet for this problem. It appears once a search writes its current best construction.</Empty>
  switch (art.kind) {
    case 'grid':
      return <NoThreeCanvas art={art} />
    case 'sign_matrix':
      return <SignMatrix art={art} />
    case 'integer_set':
      return <IntegerSet elements={art.elements} h={art.h} score={art.score} color={color} />
    case 'code':
      return <BitWall art={art} color={color} />
    default:
      return <pre className="max-h-80 overflow-auto rounded-lg bg-black/30 p-3 font-mono text-[11px] text-fg-muted">{JSON.stringify(art, null, 1)}</pre>
  }
}

/** Whose solution the backend verified (VerifyResponse.source), in words; null when nothing was checked. */
function verifiedWhat(source: string | null | undefined): string | null {
  if (source === 'ours') return 'our best solution'
  if (source === 'record') return "the record holder's construction (not ours, shown for reference)"
  if (source === 'candidate') return 'the current search state (candidate, not a claimed solution)'
  if (!source || source === 'none') return null
  return `the ${source} solution`
}

function VerifyBox({ slug }: { slug: string }) {
  const toast = useToast()
  const { refresh } = useLive()
  const v = useAction(() => api.verify(slug), { resetMs: 4000 })
  const r = v.result
  const run = async () => {
    const res = await v.run()
    if (res) {
      const what = verifiedWhat(res.source)
      const secs = typeof res.seconds === 'number' ? `${res.seconds.toFixed(2)} s` : ''
      toast.push(
        res.ok
          ? {
              kind: res.beats_record ? 'record' : 'success',
              title: res.beats_record ? 'Verified: beats the record' : 'Official verifier accepted it',
              msg: `${what ?? 'solution'}: score ${res.score}${secs ? ` in ${secs}` : ''}`,
            }
          : what
            ? { kind: 'error', title: 'Official verifier did not accept it', msg: `${what}: ${res.error ?? 'invalid'}` }
            : { kind: 'info', title: 'Nothing to verify', msg: res.error ?? 'no solution stored for this problem yet' },
      )
      void refresh()
    } else toast.push({ kind: 'error', title: 'Verify failed', msg: v.lastError() ?? '' })
  }
  return (
    <div className="flex flex-col items-end gap-2">
      <ActionButton variant="amber" onClick={run} status={v.status} error={v.error} successLabel="Verified">
        Verify now
      </ActionButton>
      <AnimatePresence>
        {r && (
          <motion.div data-testid="verify-result" initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className={cx('max-w-[360px] rounded-lg border px-3 py-2 font-mono text-[11px] leading-snug', r.ok ? (r.beats_record ? 'border-amber/50 bg-amber/10 text-amber' : 'border-good/30 bg-good/[0.06] text-good') : 'border-bad/40 bg-bad/10 text-bad')}>
            {verifiedWhat(r.source) ? <div className="mb-0.5 text-fg-dim">checked {verifiedWhat(r.source)}</div> : null}
            {!r.ok && !verifiedWhat(r.source) ? (
              <span className="text-fg-muted">nothing to verify: {r.error ?? 'no solution yet'}</span>
            ) : r.ok ? (
              <>
                official verifier: <span className="text-fg">{r.score}</span> | {r.beats_record ? 'BEATS RECORD' : 'does not beat record'}
                {typeof r.seconds === 'number' && ` | ${r.seconds.toFixed(2)} s`}
              </>
            ) : (
              <>not accepted: {r.error}</>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function StopButton({ s, onDone }: { s: Strategy; onDone: () => void }) {
  const toast = useToast()
  const [confirm, setConfirm] = useState(false)
  const a = useAction(async () => ensureOk(await api.stopStrategy(s.id)))
  useEffect(() => {
    if (!confirm) return
    const t = setTimeout(() => setConfirm(false), 4000)
    return () => clearTimeout(t)
  }, [confirm])
  const go = async () => {
    if (!confirm) return setConfirm(true)
    setConfirm(false)
    const r = await a.run()
    if (r) {
      toast.push({ kind: 'success', title: `Stopped ${s.id}` })
      onDone()
    } else toast.push({ kind: 'error', title: `Stop failed: ${s.id}`, msg: a.lastError() ?? '' })
  }
  return (
    <ActionButton size="sm" variant="danger" onClick={go} status={a.status} error={a.error} successLabel="Stopped">
      {confirm ? 'Confirm stop' : 'Stop'}
    </ActionButton>
  )
}

function StrategiesTable({ strategies, onChange }: { strategies: Strategy[]; onChange: () => void }) {
  const [showAll, setShowAll] = useState(false)
  if (!strategies.length) return <Empty>No strategies running on this problem.</Empty>
  const rows = showAll ? strategies : strategies.slice(0, 12)
  return (
    <div>
      <div className="-mx-4 overflow-x-auto sm:-mx-5">
        <table className="w-full min-w-[540px] text-left text-[12px]">
          <thead>
            <tr className="border-b border-white/[0.06] text-[10px] uppercase tracking-[0.12em] text-fg-dim">
              <th className="px-4 py-2 font-semibold sm:px-5">Strategy</th>
              <th className="px-2 py-2 font-semibold">Params</th>
              <th className="px-2 py-2 font-semibold">Started</th>
              <th className="px-2 py-2 text-right font-semibold">Metric</th>
              <th className="px-4 py-2 text-right font-semibold sm:px-5" />
            </tr>
          </thead>
          <tbody>
            {rows.map((s) => (
              <tr key={s.id} className="border-b border-white/[0.04] align-top hover:bg-white/[0.015]">
                <td className="px-4 py-2 sm:px-5">
                  <div className="break-all font-mono text-[11.5px] text-fg">{s.id}</div>
                  <div className="mt-0.5 flex items-center gap-1.5 text-[10.5px] text-fg-dim">
                    {s.template}
                    {s.adopted && <Chip color="#8B95A7">adopted</Chip>}
                  </div>
                </td>
                <td className="max-w-[260px] px-2 py-2">
                  <div className="flex flex-wrap gap-1">
                    {Object.entries(s.params || {}).map(([k, v]) => (
                      <span key={k} className="rounded bg-white/[0.04] px-1.5 py-0.5 font-mono text-[10.5px] text-fg-muted">
                        {k}={String(v)}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="whitespace-nowrap px-2 py-2 font-mono text-[11px] text-fg-muted" title={s.started_at ?? ''}>
                  <div className="uppercase text-fg-dim">{s.resource}</div>
                  {timeAgo(s.started_at)}
                </td>
                <td className="px-2 py-2 text-right font-mono text-[12px] text-fg">{fmtScore(s.metric_value)}</td>
                <td className="px-4 py-2 text-right sm:px-5">
                  <StopButton s={s} onDone={onChange} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {strategies.length > 12 && (
        <button onClick={() => setShowAll((x) => !x)} className="mt-3 text-xs text-cyan hover:underline">
          {showAll ? 'Show fewer' : `Show all ${strategies.length}`}
        </button>
      )}
    </div>
  )
}

function defaultParams(t: Template | undefined): Record<string, string> {
  const out: Record<string, string> = {}
  if (!t) return out
  for (const [k, spec] of Object.entries(t.params)) out[k] = spec.default != null ? String(spec.default) : spec.type === 'enum' ? String(spec.values?.[0] ?? '') : String(spec.min ?? 0)
  return out
}

function LaunchForm({ slug, templates, onLaunched }: { slug: string; templates: Template[]; onLaunched: () => void }) {
  const toast = useToast()
  const [tname, setTname] = useState(templates[0]?.name ?? '')
  const t = templates.find((x) => x.name === tname) ?? templates[0]
  const [vals, setVals] = useState<Record<string, string>>(() => defaultParams(t))
  const tKey = t ? t.name + JSON.stringify(t.params) : ''
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => setVals(defaultParams(t)), [tKey])
  const a = useAction(async (params: Record<string, unknown>) => ensureOk(await api.launchStrategy({ problem: slug, template: t!.name, params })), { resetMs: 4000 })

  if (!templates.length) return <Empty>No search templates registered for this problem.</Empty>
  if (!t) return null

  const errors: Record<string, string> = {}
  const parsed: Record<string, unknown> = {}
  for (const [k, spec] of Object.entries(t.params)) {
    const raw = vals[k] ?? ''
    if (spec.type === 'enum') {
      const match = spec.values?.find((v) => String(v) === raw)
      if (match === undefined) errors[k] = 'choose a value'
      parsed[k] = match
    } else {
      const num = Number(raw)
      if (raw.trim() === '' || !Number.isFinite(num)) errors[k] = 'number required'
      else if (spec.type === 'int' && !Number.isInteger(num)) errors[k] = 'integer required'
      else if (spec.min != null && num < spec.min) errors[k] = `min ${spec.min}`
      else if (spec.max != null && num > spec.max) errors[k] = `max ${spec.max}`
      parsed[k] = num
    }
  }
  const invalid = Object.keys(errors).length > 0

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (invalid) return
    const r = await a.run(parsed)
    if (r) {
      toast.push({ kind: 'success', title: 'Strategy launched', msg: r.id ?? '' })
      onLaunched()
    } else toast.push({ kind: 'error', title: 'Launch rejected', msg: a.lastError() ?? '' })
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      {templates.length > 1 && (
        <div className="flex flex-wrap gap-1.5">
          {templates.map((x) => (
            <button
              type="button"
              key={x.name}
              onClick={() => setTname(x.name)}
              className={cx('rounded-lg border px-2.5 py-1 font-mono text-[11.5px]', x.name === t.name ? 'border-cyan/40 bg-cyan/[0.08] text-cyan' : 'border-white/10 text-fg-muted hover:text-fg')}
            >
              {x.name}
            </button>
          ))}
        </div>
      )}
      <div className="flex items-center gap-2 font-mono text-[11px] text-fg-dim">
        template <span className="text-fg">{t.name}</span> | resource <span className="uppercase text-fg">{t.resource}</span>
      </div>
      {Object.keys(t.params).length === 0 && <div className="text-xs text-fg-muted">This template takes no parameters.</div>}
      <div className="grid gap-3 sm:grid-cols-2">
        {Object.entries(t.params).map(([k, spec]) => (
          <label key={k} className="block">
            <div className="mb-1 flex items-baseline justify-between gap-2">
              <span className="font-mono text-[11.5px] text-fg">{k}</span>
              <span className="font-mono text-[10px] text-fg-dim">
                {spec.type}
                {spec.type !== 'enum' && (spec.min != null || spec.max != null) && ` [${spec.min ?? '-inf'}, ${spec.max ?? 'inf'}]`}
              </span>
            </div>
            {spec.type === 'enum' ? (
              <select
                value={vals[k] ?? ''}
                onChange={(e) => setVals((v) => ({ ...v, [k]: e.target.value }))}
                disabled={READ_ONLY}
                className="h-9 w-full rounded-lg border border-white/10 bg-ink-800 px-2 font-mono text-[12px] text-fg outline-none focus:border-cyan/50 disabled:opacity-50"
              >
                {spec.values?.map((o) => (
                  <option key={String(o)} value={String(o)}>
                    {String(o)}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="number"
                inputMode="decimal"
                step={spec.type === 'int' ? 1 : 'any'}
                min={spec.min}
                max={spec.max}
                value={vals[k] ?? ''}
                disabled={READ_ONLY}
                onChange={(e) => setVals((v) => ({ ...v, [k]: e.target.value }))}
                className={cx('h-9 w-full rounded-lg border bg-ink-800 px-2 font-mono text-[12px] text-fg outline-none focus:border-cyan/50 disabled:opacity-50', errors[k] ? 'border-bad/50' : 'border-white/10')}
              />
            )}
            {errors[k] && <div className="mt-0.5 text-[10.5px] text-bad">{errors[k]}</div>}
          </label>
        ))}
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <ActionButton type="submit" variant="primary" status={a.status} error={a.error} disabled={invalid} successLabel={a.result?.id ? `Launched ${a.result.id}` : 'Launched'}>
          Launch strategy
        </ActionButton>
        <span className="text-[11px] text-fg-dim">Validated against the template schema here and again by the planner on the server.</span>
      </div>
    </form>
  )
}

function Leaderboard({ p }: { p: ProblemDetail }) {
  const rows = useMemo(() => {
    const base = p.leaderboard.map((r) => ({ ...r, ours: false }))
    if (p.ours) {
      base.push({ rank: 0, agent: 'Phoenixastar (ours)', score: p.ours.score, ours: true })
      base.sort((a, b) => (p.scoring === 'maximize' ? b.score - a.score : a.score - b.score) || (a.ours ? 1 : -1))
    }
    return base.slice(0, 12)
  }, [p])
  if (!rows.length) return <Empty>No leaderboard entries</Empty>
  return (
    <ol className="space-y-1">
      {rows.map((r, i) => (
        <li key={r.agent + i} className={cx('flex items-center gap-3 rounded-lg px-2.5 py-1.5', r.ours ? 'border border-cyan/30 bg-cyan/[0.06]' : i === 0 ? 'bg-amber/[0.06]' : '')}>
          <span className={cx('w-6 font-mono text-[11px]', i === 0 ? 'text-amber' : 'text-fg-dim')}>{r.ours ? '--' : `#${r.rank}`}</span>
          <span className={cx('flex-1 truncate text-[12.5px]', r.ours ? 'font-semibold text-cyan' : 'text-fg')}>{r.agent}</span>
          <span className={cx('font-mono text-[12px]', i === 0 && !r.ours ? 'text-amber' : 'text-fg-muted')}>{fmtScore(r.score)}</span>
        </li>
      ))}
    </ol>
  )
}

export default function ProblemPage() {
  const { slug = '' } = useParams()
  const live = useLive()
  const detail = useApi(() => api.problem(slug), [slug], 10000)
  const decisions = useApi(() => api.decisions({ problem: slug, limit: 30 }), [slug], 15000)
  const [descOpen, setDescOpen] = useState(false)

  const summary = live.state?.problems.find((p) => p.slug === slug)
  const p: ProblemDetail | null = detail.data ? { ...detail.data, ...(summary ? { metric: summary.metric, status: summary.status } : {}) } : null
  const color = problemColor(slug)
  const series = live.series[slug]?.length ? live.series[slug] : (detail.data?.metric_history ?? []).map(([t, v]) => [Date.parse(t), v] as [number, number])

  const decs = useMemo(() => {
    const map = new Map<number, Decision>()
    for (const d of [...(decisions.data ?? []), ...live.feed.filter((d) => d.problem === slug)]) map.set(d.id, d)
    return [...map.values()].sort((a, b) => b.id - a.id).slice(0, 30)
  }, [decisions.data, live.feed, slug])

  const reloadAll = () => {
    void detail.reload()
    void live.refresh()
  }

  if (detail.error && !detail.data)
    return (
      <div className="space-y-4">
        <BackLink />
        <ErrorNote error={detail.error} onRetry={detail.reload} />
      </div>
    )
  if (!p)
    return (
      <div className="space-y-4">
        <BackLink />
        <Skeleton className="h-28" />
        <Skeleton className="h-[480px]" />
      </div>
    )

  const gap = gapToRecord(p)

  return (
    <div className="space-y-5">
      <BackLink />
      <section className={cx('panel relative overflow-hidden rounded-2xl p-5 sm:p-6', p.beats_record && '!border-amber/60 shadow-amber')}>
        <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: `linear-gradient(90deg, ${color}, transparent 70%)` }} />
        <div className="flex flex-wrap items-start justify-between gap-5">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-[11px]" style={{ color }}>
                {p.slug}
              </span>
              <StatusBadge status={p.beats_record ? 'record' : p.status} />
              <span className="font-mono text-[10.5px] uppercase text-fg-dim">{p.scoring}</span>
            </div>
            <h1 className="mt-1.5 font-display text-2xl font-semibold tracking-tight sm:text-[28px]">{p.title}</h1>
            <div className="mt-4 flex flex-wrap gap-x-8 gap-y-3">
              <div>
                <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Record</div>
                <div className="font-mono text-xl font-semibold text-amber">{fmtScore(p.record.score)}</div>
                <div className="text-[11px] text-fg-dim">{p.record.holder}</div>
              </div>
              <div>
                <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Ours</div>
                <div className={cx('font-mono text-xl font-semibold', p.beats_record ? 'text-amber glow-amber' : 'text-fg')}>{p.ours ? fmtScore(p.ours.score) : '--'}</div>
                <div className="text-[11px] text-fg-dim">
                  {p.ours ? `${p.ours.verified ? 'verified' : 'unverified'} ${dateTime(p.ours.at)}` : 'no valid solution yet'}
                  {gap != null && gap !== 0 && <span className={gap > 0 ? ' text-amber' : ''}> | gap {gap > 0 ? '+' : ''}{fmtScore(gap, Math.abs(gap) < 1 ? 8 : 0)}</span>}
                </div>
              </div>
              <div>
                <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">{p.metric.name}</div>
                <div className="font-mono text-xl font-semibold" style={{ color }}>
                  {fmtScore(p.metric.value)}
                </div>
                <div className="text-[11px] text-fg-dim">
                  target {fmtScore(p.metric.target)} | {p.metric.lower_is_better ? 'lower is better' : 'higher is better'}
                </div>
              </div>
              <div>
                <div className="text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-dim">Compute</div>
                <div className="font-mono text-xl font-semibold text-fg">
                  {p.compute.gpus} <span className="text-sm text-fg-dim">GPU</span> {p.compute.cpu_procs} <span className="text-sm text-fg-dim">cores</span>
                </div>
                <div className="text-[11px] text-fg-dim">{(p.compute.share * 100).toFixed(1)}% of the lab</div>
              </div>
            </div>
          </div>
          <VerifyBox slug={slug} />
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,1.45fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-5">
          <Panel title="Current construction" subtitle={p.artifact?.label ?? 'Live artifact from the search (verified only when the critic says so)'}>
            <ArtifactView art={p.artifact} color={color} />
          </Panel>
          <Panel title="Metric history" subtitle={`${p.metric.name}: the live progress signal`}>
            {series.length > 1 ? <MetricChart data={series} color={color} name={p.metric.name} target={p.metric.target} /> : <Empty>Not enough history yet</Empty>}
          </Panel>
          <Panel title="Running strategies" subtitle={`${p.strategies.length} on the box`}>
            <StrategiesTable strategies={p.strategies} onChange={reloadAll} />
          </Panel>
          <Panel title="Launch strategy" subtitle="Form generated from the template parameter schema">
            <LaunchForm slug={slug} templates={p.templates} onLaunched={reloadAll} />
          </Panel>
        </div>
        <div className="min-w-0 space-y-5">
          <Panel title="Leaderboard" subtitle="EinsteinArena, with our best verified score inserted">
            <Leaderboard p={p} />
          </Panel>
          <Panel
            title="Problem statement"
            right={
              <button onClick={() => setDescOpen((o) => !o)} className="text-xs text-cyan hover:underline">
                {descOpen ? 'Collapse' : 'Expand'}
              </button>
            }
          >
            <div className={cx('relative', !descOpen && 'max-h-[340px] overflow-hidden')}>
              <Markdown>{p.description_md || '_No description._'}</Markdown>
              {!descOpen && <div className="pointer-events-none absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-[#0d1015] to-transparent" />}
            </div>
          </Panel>
          <Panel title="Decisions on this problem" right={<Link to={`/decisions?problem=${slug}`} className="text-xs text-cyan hover:underline">All</Link>}>
            {decisions.error && !decisions.data && <ErrorNote error={decisions.error} onRetry={decisions.reload} />}
            <div className="space-y-2">
              {decs.length ? decs.map((d) => <DecisionCard key={d.id} d={d} />) : !decisions.loading && <Empty>No decisions about this problem yet</Empty>}
            </div>
          </Panel>
        </div>
      </div>
    </div>
  )
}

function BackLink() {
  return (
    <Link to="/" className="inline-flex items-center gap-1 text-xs text-fg-muted hover:text-cyan">
      <IconArrowLeft className="h-3.5 w-3.5" /> Mission control
    </Link>
  )
}
