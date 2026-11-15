import { motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import { api, ensureOk } from '../api'
import { useAction } from '../hooks/useApi'
import { dateTime, dur, cx } from '../lib/format'
import { useLive } from '../live'
import { MODE } from '../mode'
import type { Phase } from '../types'
import { ActionButton } from './ui'
import { IconBolt, IconPause, IconPlay } from './icons'
import { useToast } from './Toast'

export const PHASES: { key: Phase; label: string; hint: string }[] = [
  { key: 'telemetry', label: 'Telemetry', hint: 'GPUs, cores, search logs' },
  { key: 'critic', label: 'Critic', hint: 'verify artifacts, score predictions' },
  { key: 'memory', label: 'Memory', hint: 'recall facts (past.dev)' },
  { key: 'literature', label: 'Literature', hint: 'Exa search' },
  { key: 'propose', label: 'Propose', hint: 'GPT-6 Astra proposes actions' },
  { key: 'referee', label: 'Referee', hint: 'Claude Fable 5.2 approves / vetoes' },
  { key: 'plan', label: 'Plan', hint: 'validate, budget, prioritize' },
  { key: 'execute', label: 'Execute', hint: 'launch / stop on the box + Modal' },
]

export function useNow(ms = 1000) {
  const [now, setNow] = useState(Date.now())
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), ms)
    return () => clearInterval(t)
  }, [ms])
  return now
}

export function LoopPill({ compact }: { compact?: boolean }) {
  const { state } = useLive()
  if (!state) return <span className="h-7 w-32 rounded-full skeleton" />
  const { loop } = state
  if (MODE === 'static')
    return (
      <span className="inline-flex h-7 items-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.03] px-2.5 text-[12px] font-medium text-fg-muted">
        <span className="h-1.5 w-1.5 rounded-full bg-amber" />
        {compact ? 'Replay' : <>Recorded run<span className="text-ink-400">/</span><span className="font-mono text-[11.5px] text-fg">{state.totals.cycles} cycles</span></>}
      </span>
    )
  const running = loop.status === 'running'
  const active = loop.phase !== 'idle'
  return (
    <span
      className={cx(
        'inline-flex h-7 items-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.03] px-2.5 text-[12px] font-medium text-fg-muted',
      )}
    >
      <span className={cx('h-1.5 w-1.5 rounded-full', running ? 'bg-good' : 'bg-amber')} />
      <span className="text-fg">{compact ? (running ? 'Running' : 'Paused') : running ? 'Loop running' : 'Loop paused'}</span>
      {!compact && (
        <>
          <span className="text-ink-400">/</span>
          <span>Cycle <span className="font-mono text-[11.5px] text-fg">{loop.cycle}</span></span>
          {loop.test_mode && (
            <>
              <span className="text-ink-400">/</span>
              <span className="text-violet" title="Server runs with PHOENIX_TEST_MODE=1: launches get test- ids, stops of non-test runs are dry runs">
                Test mode
              </span>
            </>
          )}
          {active && (
            <>
              <span className="text-ink-400">/</span>
              <span className="capitalize text-cyan">{loop.phase}</span>
            </>
          )}
        </>
      )}
    </span>
  )
}

export function ConnectionBadge() {
  const { stream, error, state } = useLive()
  let label = 'SSE live'
  let dot = 'bg-good'
  if (MODE === 'static') {
    label = 'Replay'
    dot = 'bg-amber'
  } else if (MODE === 'fixtures') {
    label = 'Fixtures'
    dot = 'bg-violet'
  } else if (error) {
    label = 'Backend offline'
    dot = 'bg-bad'
  } else if (stream !== 'live') {
    label = 'Polling 5s'
    dot = 'bg-amber'
  }
  // the snapshot marks the box offline (it is a recording); do not show a red "box offline" in the replay
  const box = MODE === 'static' ? undefined : state?.compute.box
  return (
    <span className="flex items-center gap-1.5">
      <span className="inline-flex h-7 items-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.03] px-2.5 text-[12px] font-medium text-fg-muted">
        <span className={cx('h-1.5 w-1.5 rounded-full', dot)} />
        {label}
      </span>
      {box && (
        <span
          className={cx(
            'hidden h-7 items-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.03] px-2.5 text-[12px] font-medium text-fg-muted sm:inline-flex',
          )}
          title="GPU box SSH reachability"
        >
          <span className={cx('h-1.5 w-1.5 rounded-full', box === 'online' ? 'bg-good' : 'bg-bad')} />
          Box {box}
        </span>
      )}
    </span>
  )
}

export function PhaseStepper() {
  const { state } = useLive()
  const now = useNow(1000)
  const scroller = useRef<HTMLDivElement>(null)
  const phase = state?.loop.phase
  // keep the active step visible when the stepper scrolls horizontally (phones)
  useEffect(() => {
    const el = scroller.current
    if (!el || !phase || phase === 'idle' || el.scrollWidth <= el.clientWidth) return
    const li = el.querySelector<HTMLElement>(`[data-phase="${phase}"]`)
    if (li) el.scrollTo({ left: li.offsetLeft - el.clientWidth / 2 + li.clientWidth / 2, behavior: 'smooth' })
  }, [phase])
  if (!state) return <div className="h-[74px] skeleton rounded-xl" />
  const { loop } = state
  const idx = PHASES.findIndex((p) => p.key === loop.phase)
  const idle = loop.phase === 'idle'
  const next = loop.next_cycle_at ? Date.parse(loop.next_cycle_at) : null
  const remaining = next ? Math.max(0, (next - now) / 1000) : null
  const progress = remaining != null && loop.interval_s ? 1 - Math.min(1, remaining / loop.interval_s) : 0

  return (
    <div>
      <div ref={scroller} className="no-scrollbar relative -mx-1 overflow-x-auto px-1">
        <ol className="flex min-w-[680px] items-stretch gap-2">
          {PHASES.map((p, i) => {
            const done = !idle && i < idx
            const current = !idle && i === idx
            return (
              <li key={p.key} data-phase={p.key} className="relative min-w-0 flex-1">
                <div
                  className={cx(
                    'relative h-full overflow-hidden rounded-lg border px-3 py-2.5 transition-colors duration-200',
                    current ? 'border-cyan/40 bg-cyan/[0.06]' : 'border-white/[0.07] bg-white/[0.015]',
                  )}
                >
                  {current && (
                    <motion.div layoutId="phase-glow" className="pointer-events-none absolute inset-x-0 top-0 h-[2px] bg-cyan" transition={{ duration: 0.2, ease: 'easeOut' }} />
                  )}
                  <div className="relative flex items-center gap-2">
                    <span
                      className={cx(
                        'flex h-[18px] w-[18px] shrink-0 items-center justify-center rounded-full border font-mono text-[10px]',
                        current ? 'border-cyan bg-cyan text-ink-900' : done ? 'border-white/15 bg-white/[0.06] text-fg' : 'border-white/10 text-fg-dim',
                      )}
                    >
                      {done ? '✓' : i + 1}
                    </span>
                    <span className={cx('truncate text-[12.5px] font-medium', current || done ? 'text-fg' : 'text-fg-muted')}>{p.label}</span>
                  </div>
                  <div className="relative mt-1 truncate pl-[26px] text-[11px] text-fg-dim" title={p.hint}>{p.hint}</div>
                </div>
              </li>
            )
          })}
        </ol>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-1 font-mono text-[11px] text-fg-dim">
        {MODE === 'static' ? (
          <span className="text-amber">
            Recorded run: {state.totals.cycles} cycles, {state.totals.decisions} decisions (snapshot {dateTime(state.snapshot?.generated_at ?? state.now)})
          </span>
        ) : idle ? (
          loop.status === 'paused' ? (
            <span className="text-amber">Loop paused: no new cycles until resumed</span>
          ) : remaining != null ? (
            <span className="flex items-center gap-2">
              <span>next cycle in</span>
              <span className="text-fg">{remaining > 0 ? dur(remaining) : 'starting...'}</span>
              <span className="relative inline-block h-1 w-28 overflow-hidden rounded-full bg-white/10">
                <span className="absolute inset-y-0 left-0 rounded-full bg-cyan" style={{ width: `${progress * 100}%` }} />
              </span>
            </span>
          ) : (
            <span>idle</span>
          )
        ) : (
          <span>
            cycle <span className="text-fg">{loop.cycle}</span> in progress: <span className="text-fg">{loop.phase}</span>
          </span>
        )}
        <span>interval {dur(loop.interval_s)}</span>
        <span>
          proposer <span className="text-fg">{loop.proposer_model}</span>
        </span>
        {MODE !== 'static' && <span className="hidden sm:inline">running since {dateTime(loop.started_at)}</span>}
      </div>
    </div>
  )
}

export function LoopControls() {
  const { state, applyLoop, refresh } = useLive()
  const toast = useToast()
  const pause = useAction(async () => ensureOk(await api.pause()))
  const resume = useAction(async () => ensureOk(await api.resume()))
  const runNow = useAction(async () => ensureOk(await api.runNow()))
  const running = state?.loop.status === 'running'

  const go = async (a: typeof pause, label: string) => {
    const r = await a.run()
    if (r) {
      applyLoop(r.loop)
      toast.push({ kind: 'success', title: label })
      void refresh()
    } else toast.push({ kind: 'error', title: `${label} failed`, msg: a.lastError() ?? undefined })
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      {running ? (
        <ActionButton onClick={() => go(pause, 'Loop paused')} status={pause.status} error={pause.error} successLabel="Paused" disabled={!state}>
          <IconPause className="h-3.5 w-3.5" /> Pause
        </ActionButton>
      ) : (
        <ActionButton onClick={() => go(resume, 'Loop resumed')} status={resume.status} error={resume.error} successLabel="Resumed" disabled={!state}>
          <IconPlay className="h-3.5 w-3.5" /> Resume
        </ActionButton>
      )}
      <ActionButton
        variant="primary"
        onClick={() => go(runNow, 'Cycle triggered')}
        status={runNow.status}
        error={runNow.error}
        successLabel="Triggered"
        disabled={!state || (state.loop.phase !== 'idle')}
        title={state && state.loop.phase !== 'idle' ? 'A cycle is already running' : 'Run one cycle now'}
      >
        <IconBolt className="h-3.5 w-3.5" /> Run cycle now
      </ActionButton>
    </div>
  )
}
