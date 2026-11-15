import { AnimatePresence, motion } from 'framer-motion'
import { Suspense, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { CpuGrid, GpuGrid, ModalFleet } from '../components/ComputeMap'
import { FeedItem } from '../components/Decision'
import { LoopControls, PhaseStepper } from '../components/LoopStatus'
import { ProblemCard } from '../components/ProblemCard'
import { Counter, Empty, ErrorNote, Panel, Skeleton } from '../components/ui'
import { dateTime, fmtScore, timeAgo } from '../lib/format'
import { useLive } from '../live'
import { STATIC, assetUrl } from '../mode'
import { LatticeViewer } from '../viz3d/lazy'
import type { GridArtifact } from '../types'


function Totals() {
  const { state } = useLive()
  const t = state?.totals
  const items: { label: string; value: number | undefined; accent?: boolean }[] = [
    { label: 'records', value: t?.records, accent: true },
    { label: 'cycles', value: t?.cycles },
    { label: 'decisions', value: t?.decisions },
    { label: 'experiments', value: t?.experiments_run },
    { label: 'sandboxes', value: t?.sandboxes_run },
    { label: 'facts', value: t?.facts },
    { label: 'sources', value: t?.sources },
  ]
  return (
    <div className="grid grid-cols-3 gap-x-6 gap-y-4 sm:grid-cols-4">
      {items.map((it) => (
        <div key={it.label} className="min-w-0">
          <div className="label truncate capitalize">{it.label}</div>
          <div className={`mt-1 font-mono text-[20px] font-medium leading-6 tracking-tight ${it.accent && (it.value ?? 0) > 0 ? 'text-amber' : 'text-fg'}`}>
            {it.value === undefined ? <span className="text-fg-dim">--</span> : <Counter value={it.value} />}
          </div>
        </div>
      ))}
    </div>
  )
}

function Hero() {
  const { state, details } = useLive()
  const art = useMemo(() => {
    const a = details['no-three-in-line-75']?.artifact
    if (a && a.kind === 'grid') return a as GridArtifact
    for (const d of Object.values(details)) if (d.artifact?.kind === 'grid') return d.artifact as GridArtifact
    return null
  }, [details])
  const nt = state?.problems.find((p) => p.slug === 'no-three-in-line-75')
  const recordCount = state?.problems.filter((p) => p.beats_record).length ?? 0

  return (
    <section className="panel relative overflow-hidden rounded-xl">
      <div className="grid lg:grid-cols-[1fr_1.15fr]">
        <div className="relative z-10 flex flex-col justify-between gap-8 p-5 sm:p-8">
          <div>
            <div className="flex flex-wrap items-center gap-2 text-[12.5px] font-medium text-fg-muted">
              <span className="text-cyan">Mission Control</span>
              <span className="text-ink-400">/</span>
              <span className="text-fg-dim">{state ? `${state.problems.length} open problems` : 'connecting'}</span>
            </div>
            <h1 className="mt-3 max-w-[540px] text-[24px] font-semibold leading-[1.18] tracking-[-0.025em] text-fg sm:text-[30px]">
              An AI lab that gets better at <span className="text-cyan">discovering mathematics</span> by doing it.
            </h1>
            <p className="mt-4 max-w-[520px] text-[14px] leading-6 text-fg-muted">
              A closed loop of planner, proposer and critic agents runs searches on 8 A100s and 124 cores, reads the literature with Exa, remembers across agents with past.dev, spawns
              Modal sandboxes and trains itself with Tinker. Every decision below is logged and auditable.
            </p>
          </div>
          <Totals />
          <div className="flex flex-wrap items-center gap-3">
            <LoopControls />
            {recordCount > 0 && (
              <span className="inline-flex h-7 items-center gap-2 rounded-full border border-amber/30 bg-amber/[0.08] px-2.5 text-[12px] font-medium text-amber">
                <span className="h-1.5 w-1.5 rounded-full bg-amber" />
                {recordCount} {recordCount === 1 ? 'record' : 'records'} beaten
              </span>
            )}
          </div>
        </div>
        <div className="relative min-h-[300px] border-t border-white/[0.07] bg-ink-850 sm:min-h-[380px] lg:border-l lg:border-t-0">
          <Suspense fallback={<div className="absolute inset-0 skeleton" />}>
            <LatticeViewer art={art} hero />
          </Suspense>
          <Link
            to="/problems/no-three-in-line-75"
            className="absolute bottom-3 left-3 right-3 flex flex-wrap items-center gap-x-3 gap-y-1 rounded-lg border border-white/[0.08] bg-ink-800/90 px-3 py-2 font-mono text-[11px] text-fg-muted backdrop-blur transition-colors hover:border-white/20"
          >
            <span className="text-fg">no-three-in-line-75</span>
            {art ? (
              <>
                <span>
                  <span className="text-fg">{art.count}</span> points
                </span>
                <span>
                  <span className="text-bad">{art.violated_lines.length}</span> violated lines
                </span>
                <span>
                  {art.sym} round {art.round}
                </span>
              </>
            ) : (
              <span>waiting for model</span>
            )}
            {nt && (
              <span className="ml-auto">
                record <span className="text-fg">{fmtScore(nt.record.score)}</span>
              </span>
            )}
          </Link>
        </div>
      </div>
    </section>
  )
}

function Feed() {
  const { feed, stream } = useLive()
  return (
    <Panel
      title="Live decisions"
      subtitle={STATIC ? 'recorded decision log' : stream === 'live' ? 'streaming over SSE' : 'polling every 5 s'}
      right={
        <Link to="/decisions" className="text-[12.5px] font-medium text-fg-muted transition-colors hover:text-fg">
          Full audit log
        </Link>
      }
      className="xl:sticky xl:top-20"
      bodyClass="p-3"
    >
      <div className="max-h-[calc(100vh-200px)] min-h-[200px] space-y-2 overflow-y-auto pr-1">
        {feed.length === 0 ? (
          <Empty>No decisions yet</Empty>
        ) : (
          <AnimatePresence initial={false}>
            {feed.slice(0, 40).map((d) => (
              <motion.div key={d.id} layout initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
                <FeedItem d={d} />
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </Panel>
  )
}

function PhysicsFeature() {
  const { state } = useLive()
  const eh = state?.problems.find((p) => p.slug === 'event-horizon')
  const tb = state?.problems.find((p) => p.slug === 'three-body-periodic-orbits')
  return (
    <Link to="/problems/event-horizon" className="group relative block overflow-hidden rounded-2xl border border-white/[0.07] bg-[#07080A]">
      <img src={assetUrl('/gallery/blackhole.jpg')} alt="Event Horizon: a black hole drawn from the measured Page curve"
        className="block h-[200px] w-full object-cover opacity-90 transition-opacity duration-300 group-hover:opacity-100 sm:absolute sm:inset-y-0 sm:right-0 sm:h-full sm:w-[72%]"
        loading="lazy" />
      <div className="pointer-events-none absolute inset-0 hidden bg-gradient-to-r from-[#07080A] from-30% via-[#07080A]/60 via-40% to-transparent to-60% sm:block" />
      <div className="relative flex flex-col gap-3 p-6 sm:min-h-[340px] sm:max-w-[48%] sm:justify-center sm:p-8">
        <div className="text-[11px] font-medium uppercase tracking-[0.14em] text-cyan">Physics · Event Horizon</div>
        <h2 className="text-[22px] font-semibold leading-tight tracking-[-0.02em] text-fg sm:text-[26px]">How does information survive a black hole&rsquo;s evaporation?</h2>
        <p className="text-[13px] leading-6 text-fg-muted">
          Exact numerics on an A100: the Page curve to 24 qubits, evaporation to 27, Hayden-Preskill recovery, every key claim re-derived by an independent verifier
          {eh?.metric?.value != null ? ` (${eh.metric.value} of ${eh.metric.target ?? '?'} verified)` : ''}.
          {tb?.metric?.value != null ? ` Plus ${tb.metric.value} candidate new three-body orbit families.` : ''}
        </p>
        <div className="text-[12px] font-medium text-cyan">Open the study &rarr;</div>
      </div>
      <div className="relative px-6 pb-4 text-[10.5px] text-fg-dim sm:absolute sm:bottom-3 sm:right-4 sm:p-0">Disk rings = measured S(R) per evaporation step (N = 26). Artwork from data.</div>
    </Link>
  )
}

export default function MissionControl() {
  const { state, error, series, refresh } = useLive()
  return (
    <div className="space-y-6">
      {error && !state && <ErrorNote error={error} onRetry={refresh} />}
      <Hero />
      <PhysicsFeature />
      <Panel title="Autonomous loop" subtitle={STATIC ? 'The seven phases of every cycle (recorded run; live, they animate as the server publishes them)' : 'Phases animate live as the server publishes them'}>
        <PhaseStepper />
      </Panel>
      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_380px]">
        <div className="min-w-0 space-y-6">

          <Panel
            title="Compute map"
            subtitle={state ? `8 x A100 40GB and ${state.compute.cpus} CPU cores, colored by the problem that owns them` : 'loading'}
            right={
              state && (
                <span className="font-mono text-[11px] text-fg-dim">
                  {STATIC
                    ? `recorded ${dateTime(state.compute.telemetry_at ?? state.snapshot?.telemetry_at ?? state.now)}`
                    : `box ${state.compute.box}${state.compute.telemetry_at ? `, read ${timeAgo(state.compute.telemetry_at)}` : ''}`}
                </span>
              )
            }
          >
            {state ? (
              <div className="grid gap-6 2xl:grid-cols-[1.1fr_1fr]">
                <div>
                  <div className="mb-2 label">GPUs</div>
                  <GpuGrid compute={state.compute} />
                </div>
                <div>
                  <div className="mb-2 label">CPU cores</div>
                  <CpuGrid compute={state.compute} />
                </div>
                <div className="2xl:col-span-2">
                  <ModalFleet compute={state.compute} />
                </div>
              </div>
            ) : (
              <Skeleton className="h-48" />
            )}
          </Panel>

          <div>
            <div className="mb-3 flex items-end justify-between px-1">
              <div>
                <h2 className="text-[14px] font-semibold tracking-[-0.01em]">Problem portfolio</h2>
                <p className="mt-0.5 text-[12.5px] text-fg-muted">Best-known record vs our best verified score, with the live progress metric</p>
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 2xl:grid-cols-3">
              {state
                ? state.problems.map((p, i) => <ProblemCard key={p.slug} p={p} series={series[p.slug]} index={i} />)
                : Array.from({ length: 6 }, (_, i) => <Skeleton key={i} className="h-64" />)}
            </div>
          </div>
        </div>
        <div className="min-w-0">
          <Feed />
        </div>
      </div>
    </div>
  )
}
