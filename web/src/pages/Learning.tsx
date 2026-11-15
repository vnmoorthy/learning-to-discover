import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { api, ensureOk } from '../api'
import { axisProps, tooltipStyle } from '../components/charts'
import { IconClose } from '../components/icons'
import { Portal } from '../components/Portal'
import { useToast } from '../components/Toast'
import { ActionButton, Empty, ErrorNote, Panel, Select, Skeleton, Spinner } from '../components/ui'
import { useAction, useApi } from '../hooks/useApi'
import { highlightPython } from '../lib/highlight'
import { cx, fmtPct, fmtScore, problemColor, timeAgo } from '../lib/format'
import { READ_ONLY } from '../mode'
import type { LearningResponse, SandboxRun } from '../types'
import IntegerSet from '../viz/IntegerSet'
import SignMatrix from '../viz/SignMatrix'

const SANDBOX_PROBLEMS = ['sidon-45-set', 'spencer-discrepancy', 'ring-loading-15']

function StatusPill({ status }: { status: LearningResponse['status'] }) {
  const map = {
    idle: 'border-white/10 text-fg-muted',
    running: 'border-cyan/40 bg-cyan/[0.08] text-cyan',
    done: 'border-good/40 bg-good/[0.08] text-good',
    error: 'border-bad/40 bg-bad/10 text-bad',
  }
  return (
    <span className={cx('inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[11px]', map[status])}>
      {status === 'running' && <span className="h-1.5 w-1.5 animate-pulseDot rounded-full bg-cyan" />}
      {status}
    </span>
  )
}

function BestConstruction({ best, problem }: { best: NonNullable<LearningResponse['best']>; problem: string }) {
  const sol = best.solution as Record<string, unknown>
  if (Array.isArray(sol.elements)) return <IntegerSet elements={sol.elements as number[]} score={best.score} color={problemColor(problem)} />
  if (Array.isArray(sol.matrix)) {
    const m = sol.matrix as number[][]
    return <SignMatrix art={{ kind: 'sign_matrix', n: m.length, matrix: m }} />
  }
  return <pre className="max-h-64 overflow-auto rounded-lg bg-black/30 p-3 font-mono text-[11px] text-fg-muted">{JSON.stringify(sol, null, 1)}</pre>
}

function Training() {
  const toast = useToast()
  const [fast, setFast] = useState(false)
  const learn = useApi(() => api.learning(), [], fast ? 3000 : 15000)
  const [steps, setSteps] = useState('40')
  const start = useAction(async (n: number) => ensureOk(await api.startLearning(n)))
  const L = learn.data

  useEffect(() => setFast(L?.status === 'running'), [L?.status])

  const nSteps = Number(steps)
  const stepsValid = Number.isInteger(nSteps) && nSteps >= 1 && nSteps <= 1000
  const go = async () => {
    if (!stepsValid) return
    const r = await start.run(nSteps)
    if (r) {
      toast.push({ kind: 'success', title: 'Tinker training started', msg: `${nSteps} GRPO steps` })
      setFast(true)
      void learn.reload()
    } else toast.push({ kind: 'error', title: 'Training did not start', msg: start.lastError() ?? '' })
  }

  if (learn.error && !L) return <ErrorNote error={learn.error} onRetry={learn.reload} />
  if (!L) return <Skeleton className="h-96" />

  const last = L.steps[L.steps.length - 1]
  const g0 = L.eval?.gen0
  const gN = L.eval?.genN

  return (
    <div className="space-y-5">
      <Panel
        title="Tinker RL self-training"
        subtitle={`${L.base_model} LoRA, GRPO on ${L.problem} (reward from the official verifier)`}
        right={
          <div className="flex flex-wrap items-center gap-2">
            <StatusPill status={L.status} />
            <label className="flex items-center gap-1.5 text-xs text-fg-muted">
              steps
              <input
                type="number"
                min={1}
                max={1000}
                value={steps}
                disabled={READ_ONLY}
                onChange={(e) => setSteps(e.target.value)}
                className={cx('h-8 w-20 rounded-lg border bg-ink-800 px-2 font-mono text-xs text-fg outline-none focus:border-cyan/50 disabled:opacity-50', stepsValid ? 'border-white/10' : 'border-bad/50')}
              />
            </label>
            <ActionButton variant="primary" onClick={go} status={start.status} error={start.error} disabled={!stepsValid || L.status === 'running'} title={L.status === 'running' ? 'A run is in progress' : undefined} successLabel="Started">
              Start training
            </ActionButton>
          </div>
        }
      >
        <div className="grid gap-4 sm:grid-cols-4">
          <MiniStat label="steps" value={L.steps.length ? String(last.step) : '--'} />
          <MiniStat label="reward mean" value={last ? fmtScore(last.reward_mean, 3) : '--'} color="#4FD1E0" />
          <MiniStat label="reward best" value={last ? fmtScore(last.reward_best, 3) : '--'} color="#E2B25C" />
          <MiniStat label="valid rate" value={last ? fmtPct(last.valid_rate, 0) : '--'} color="#6FBF8E" />
        </div>
        {L.steps.length < 2 ? (
          <div className="mt-4">
            <Empty>{L.status === 'idle' ? 'No training run yet. Start one above.' : 'Waiting for the first steps...'}</Empty>
          </div>
        ) : (
          <div className="mt-5 grid gap-5 lg:grid-cols-2">
            <div>
              <div className="mb-2 label">Reward per step</div>
              <div className="h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={L.steps} margin={{ top: 6, right: 8, left: -12, bottom: 0 }}>
                    <CartesianGrid stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis dataKey="step" {...axisProps} />
                    <YAxis {...axisProps} domain={[0, 'auto']} />
                    <Tooltip {...tooltipStyle} formatter={(v: number, n: string) => [fmtScore(v, 4), n]} labelFormatter={(s) => `step ${s}`} />
                    <Legend wrapperStyle={{ fontSize: 11, fontFamily: 'JetBrains Mono, monospace' }} />
                    <Line type="monotone" dataKey="reward_mean" name="mean" stroke="#4FD1E0" strokeWidth={2} dot={false} isAnimationActive={false} />
                    <Line type="monotone" dataKey="reward_best" name="best" stroke="#E2B25C" strokeWidth={1.5} strokeDasharray="4 3" dot={false} isAnimationActive={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div>
              <div className="mb-2 label">Valid-construction rate</div>
              <div className="h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={L.steps} margin={{ top: 6, right: 8, left: -12, bottom: 0 }}>
                    <CartesianGrid stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis dataKey="step" {...axisProps} />
                    <YAxis {...axisProps} domain={[0, 1]} tickFormatter={(v) => fmtPct(v)} />
                    <Tooltip {...tooltipStyle} formatter={(v: number) => [fmtPct(v, 1), 'valid']} labelFormatter={(s) => `step ${s}`} />
                    <Line type="monotone" dataKey="valid_rate" name="valid" stroke="#6FBF8E" strokeWidth={2} dot={false} isAnimationActive={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </Panel>

      <div className="grid gap-5 lg:grid-cols-2">
        <Panel title="Gen-0 vs gen-N" subtitle={L.eval ? `transfer eval on held-out ${L.eval.heldout}, same sampling budget` : 'transfer evaluation'}>
          {!g0 || !gN ? (
            <Empty>The transfer eval runs at the end of a training run.</Empty>
          ) : (
            <div className="space-y-4">
              {(
                [
                  // score: relative change; valid rate: change in percentage points (gen-0 is often exactly 0%)
                  ['score', g0.score, gN.score, (v: number) => fmtScore(v, 3), (a: number, b: number) => (a ? `${b >= a ? '+' : ''}${(((b - a) / Math.abs(a)) * 100).toFixed(0)}%` : `${b >= a ? '+' : ''}${fmtScore(b - a, 3)}`)],
                  ['valid rate', g0.valid_rate, gN.valid_rate, (v: number) => fmtPct(v, 0), (a: number, b: number) => `${b >= a ? '+' : ''}${((b - a) * 100).toFixed(0)} pts`],
                ] as const
              ).map(([label, a, b, f, delta]) => {
                const max = Math.max(a, b, 1e-9)
                return (
                  <div key={label}>
                    <div className="mb-1.5 flex items-baseline justify-between text-[11px]">
                      <span className="font-semibold text-fg-dim">{label}</span>
                      <span className={cx('font-mono', b >= a ? 'text-good' : 'text-bad')}>{delta(a, b)}</span>
                    </div>
                    {[
                      ['gen-0', a, '#7A838F'],
                      ['gen-N', b, '#4FD1E0'],
                    ].map(([n, v, c]) => (
                      <div key={n as string} className="mb-1 flex items-center gap-3">
                        <span className="w-12 font-mono text-[11px] text-fg-muted">{n}</span>
                        <div className="h-5 flex-1 overflow-hidden rounded bg-white/[0.04]">
                          <motion.div className="h-full rounded" style={{ background: c as string }} initial={{ width: 0 }} animate={{ width: `${((v as number) / max) * 100}%` }} transition={{ duration: 0.8 }} />
                        </div>
                        <span className="w-14 text-right font-mono text-[12px] text-fg">{f(v as number)}</span>
                      </div>
                    ))}
                  </div>
                )
              })}
            </div>
          )}
        </Panel>
        <Panel title="Best construction from the trained model" subtitle={L.best ? `score ${fmtScore(L.best.score)} (official verifier)` : undefined}>
          {L.best ? <BestConstruction best={L.best} problem={L.problem} /> : <Empty>No valid construction sampled yet.</Empty>}
        </Panel>
      </div>
    </div>
  )
}

function MiniStat({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div className="rounded-xl border border-white/[0.05] bg-black/20 px-3 py-2.5">
      <div className="label">{label}</div>
      <div className="mt-0.5 font-mono text-lg font-semibold" style={color ? { color } : undefined}>
        {value}
      </div>
    </div>
  )
}

const SB_STATUS: Record<SandboxRun['status'], string> = {
  ok: 'text-good border-good/30 bg-good/[0.06]',
  invalid: 'text-amber border-amber/30 bg-amber/[0.06]',
  timeout: 'text-[#B9AEEF] border-[#A99BEA]/30 bg-[#A99BEA]/[0.06]',
  error: 'text-bad border-bad/30 bg-bad/[0.06]',
}

function CodeViewer({ run, onClose }: { run: SandboxRun; onClose: () => void }) {
  const html = useMemo(() => highlightPython(run.code || ''), [run.code])
  useEffect(() => {
    const k = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    window.addEventListener('keydown', k)
    return () => window.removeEventListener('keydown', k)
  }, [onClose])
  return (
    <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-3 backdrop-blur-sm sm:p-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose}>
      <motion.div
        initial={{ y: 20, scale: 0.98 }}
        animate={{ y: 0, scale: 1 }}
        exit={{ y: 10, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="panel flex max-h-[88vh] w-full max-w-4xl flex-col overflow-hidden rounded-xl"
      >
        <div className="flex flex-wrap items-center gap-3 border-b border-white/[0.06] px-4 py-3">
          <span className="font-mono text-sm text-fg">sandbox #{run.id}</span>
          <span className={cx('rounded-full border px-2 py-0.5 text-[11px] font-medium capitalize', SB_STATUS[run.status])}>{run.status}</span>
          <span className="font-mono text-[11px]" style={{ color: problemColor(run.problem) }}>
            {run.problem}
          </span>
          <span className="font-mono text-[11px] text-fg-muted">
            score {fmtScore(run.score)} | {run.seconds.toFixed(1)} s
          </span>
          <Link to={`/decisions?focus=${run.decision_id}`} className="font-mono text-[11px] text-cyan hover:underline">
            decision #{run.decision_id}
          </Link>
          <button onClick={onClose} className="ml-auto rounded-md p-1 text-fg-muted hover:bg-white/5 hover:text-fg" aria-label="Close">
            <IconClose />
          </button>
        </div>
        <div className="overflow-auto bg-[#0E1014] p-4">
          <pre className="code-view">
            <code dangerouslySetInnerHTML={{ __html: html }} />
          </pre>
        </div>
        <div className="border-t border-white/[0.06] px-4 py-2 text-[11px] text-fg-dim">Program written by the proposer, run in a Modal sandbox (no network, no secrets, 120 s), output verified locally with the official verifier.</div>
      </motion.div>
    </motion.div>
  )
}

function Sandboxes() {
  const toast = useToast()
  const [watchUntil, setWatchUntil] = useState(0)
  const watching = watchUntil > Date.now()
  const sb = useApi(() => api.sandboxes(200), [], watching ? 3000 : 20000)
  const [open, setOpen] = useState<SandboxRun | null>(null)
  const [problem, setProblem] = useState(SANDBOX_PROBLEMS[0])
  const [n, setN] = useState('8')
  const run = useAction(async (p: string, k: number) => ensureOk(await api.runSandboxes(p, k)))
  const baseline = useRef<number>(0)
  const [, tick] = useState(0)

  const rows = sb.data ?? []
  const maxId = rows.reduce((a, r) => Math.max(a, r.id), 0)
  const nn = Number(n)
  // the backend clamps a batch to 32 programs
  const nValid = Number.isInteger(nn) && nn >= 1 && nn <= 32

  useEffect(() => {
    if (!watching) return
    if (maxId > baseline.current && baseline.current > 0) {
      setWatchUntil(0)
      toast.push({ kind: 'success', title: 'Sandbox results arrived' })
    }
    const t = setTimeout(() => tick((x) => x + 1), 3000)
    return () => clearTimeout(t)
  }, [watching, maxId, toast])

  const go = async () => {
    if (!nValid) return
    baseline.current = Math.max(1, maxId)
    const r = await run.run(problem, nn)
    if (r) {
      toast.push({ kind: 'info', title: `Proposer is writing ${nn} programs`, msg: `then running them on Modal for ${problem}` })
      setWatchUntil(Date.now() + 5 * 60 * 1000)
    } else toast.push({ kind: 'error', title: 'Sandbox run failed to start', msg: run.lastError() ?? '' })
  }

  const stats = useMemo(() => {
    const s = { ok: 0, invalid: 0, timeout: 0, error: 0 }
    for (const r of rows) s[r.status]++
    return s
  }, [rows])

  return (
    <Panel
      title="Modal agent sandboxes"
      subtitle="Parallel search programs written by the proposer"
      right={
        <div className="flex flex-wrap items-center gap-2">
          <Select value={problem} onChange={setProblem} options={SANDBOX_PROBLEMS.map((p) => ({ value: p, label: p }))} />
          <label className="flex items-center gap-1.5 text-xs text-fg-muted">
            N
            <input
              type="number"
              min={1}
              max={32}
              value={n}
              disabled={READ_ONLY}
              onChange={(e) => setN(e.target.value)}
              className={cx('h-8 w-16 rounded-lg border bg-ink-800 px-2 font-mono text-xs text-fg outline-none focus:border-cyan/50 disabled:opacity-50', nValid ? 'border-white/10' : 'border-bad/50')}
            />
          </label>
          <ActionButton variant="primary" onClick={go} status={watching ? 'loading' : run.status} error={run.error} disabled={!nValid} successLabel="Started">
            {watching ? 'Running' : `Run ${nValid ? nn : 'N'} sandboxes`}
          </ActionButton>
        </div>
      }
    >
      {watching && (
        <div className="mb-3 flex items-center gap-2 rounded-lg border border-cyan/20 bg-cyan/[0.05] px-3 py-2 text-xs text-cyan">
          <Spinner className="h-3.5 w-3.5" /> Waiting for sandbox results (polling every 3 s)
        </div>
      )}
      <div className="mb-3 flex flex-wrap gap-4 font-mono text-[11px] text-fg-muted">
        <span>
          <span className="text-fg">{rows.length}</span> runs
        </span>
        <span>
          <span className="text-good">{stats.ok}</span> ok
        </span>
        <span>
          <span className="text-amber">{stats.invalid}</span> invalid
        </span>
        <span>
          <span className="text-[#B9AEEF]">{stats.timeout}</span> timeout
        </span>
        <span>
          <span className="text-bad">{stats.error}</span> error
        </span>
      </div>
      {sb.error && !sb.data && <ErrorNote error={sb.error} onRetry={sb.reload} />}
      {!sb.data && sb.loading ? (
        <Skeleton className="h-40" />
      ) : rows.length === 0 ? (
        <Empty>No sandbox runs yet.</Empty>
      ) : (
        <div className="-mx-4 max-h-[460px] overflow-auto sm:-mx-5">
          <table className="w-full min-w-[640px] text-left text-[12px]">
            <thead className="sticky top-0 bg-[#111418]">
              <tr className="border-b border-white/[0.06] text-[11px] font-medium text-fg-dim">
                <th className="px-4 py-2 font-semibold sm:px-5">Run</th>
                <th className="px-2 py-2 font-semibold">Problem</th>
                <th className="px-2 py-2 font-semibold">Status</th>
                <th className="px-2 py-2 text-right font-semibold">Score</th>
                <th className="px-2 py-2 text-right font-semibold">Seconds</th>
                <th className="px-2 py-2 font-semibold">When</th>
                <th className="px-4 py-2 text-right font-semibold sm:px-5">Code</th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence initial={false}>
                {rows.map((r) => (
                  <motion.tr key={r.id} initial={{ opacity: 0, backgroundColor: 'rgba(79,209,224,0.12)' }} animate={{ opacity: 1, backgroundColor: 'rgba(0,0,0,0)' }} transition={{ duration: 1.2 }} className="cursor-pointer border-b border-white/[0.04] hover:!bg-white/[0.02]" onClick={() => setOpen(r)}>
                    <td className="px-4 py-2 font-mono text-fg sm:px-5">#{r.id}</td>
                    <td className="px-2 py-2 font-mono text-[11px]" style={{ color: problemColor(r.problem) }}>
                      {r.problem}
                    </td>
                    <td className="px-2 py-2">
                      <span className={cx('rounded-full border px-2 py-0.5 text-[11px] font-medium capitalize', SB_STATUS[r.status])}>{r.status}</span>
                    </td>
                    <td className="px-2 py-2 text-right font-mono text-fg">{fmtScore(r.score)}</td>
                    <td className="px-2 py-2 text-right font-mono text-fg-muted">{r.seconds.toFixed(1)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-fg-dim">{timeAgo(r.time)}</td>
                    <td className="px-4 py-2 text-right sm:px-5">
                      <span className="text-[11px] text-cyan">view</span>
                    </td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            </tbody>
          </table>
        </div>
      )}
      <Portal>
        <AnimatePresence>{open && <CodeViewer run={open} onClose={() => setOpen(null)} />}</AnimatePresence>
      </Portal>
    </Panel>
  )
}

export default function LearningPage() {
  return (
    <div className="space-y-5">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight">Self-improvement</h1>
        <p className="mt-1 max-w-3xl text-sm text-fg-muted">
          The lab trains its own model with Tinker: RL on a cheap verifiable problem with the official verifier as reward, then checks whether the skill transfers to a held-out problem. Modal
          sandboxes let the proposer test many small search programs in parallel.
        </p>
      </div>
      <Training />
      <Sandboxes />
    </div>
  )
}
