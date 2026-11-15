import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { api } from './api'
import { STATIC } from './mode'
import { useEventStream, type SseEventName, type StreamStatus } from './hooks/useEventStream'
import { useToast } from './components/Toast'
import type { ComputeState, Decision, LogEvent, LoopState, PhaseEvent, ProblemDetail, RecordEvent, StateResponse } from './types'

export type Series = [number, number][]

interface LiveCtx {
  state: StateResponse | null
  error: string | null
  stream: StreamStatus
  lastEventAt: number | null
  updatedAt: number | null
  feed: Decision[]
  series: Record<string, Series>
  details: Record<string, ProblemDetail>
  logs: (LogEvent & { at: number })[]
  records: RecordEvent[]
  refresh: () => Promise<void>
  refreshDetail: (slug: string) => Promise<ProblemDetail | null>
  applyLoop: (loop: LoopState) => void
}

const Ctx = createContext<LiveCtx | null>(null)

export function useLive(): LiveCtx {
  const c = useContext(Ctx)
  if (!c) throw new Error('useLive outside LiveProvider')
  return c
}

const MAX_FEED = 200
const MAX_SERIES = 600

function toSeries(h: [string, number][] | undefined): Series {
  if (!h) return []
  return h
    .map(([t, v]) => [Date.parse(t), v] as [number, number])
    .filter(([t, v]) => Number.isFinite(t) && typeof v === 'number' && Number.isFinite(v))
    .sort((a, b) => a[0] - b[0])
}

/** Extract {slug: value} from a telemetry payload; tolerant of a few plausible shapes. */
function telemetryMetrics(d: Record<string, unknown>): Record<string, number | null> {
  const out: Record<string, number | null> = {}
  const take = (slug: string, v: unknown) => {
    if (typeof v === 'number' || v === null) out[slug] = v as number | null
    else if (v && typeof v === 'object') {
      const o = v as Record<string, unknown>
      const m = (o.metric as Record<string, unknown> | undefined)?.value ?? o.value ?? o.metric_value
      if (typeof m === 'number' || m === null) out[slug] = m as number | null
    }
  }
  const src = d.metrics ?? d.problems
  if (Array.isArray(src)) for (const p of src) take(String((p as Record<string, unknown>).slug), p)
  else if (src && typeof src === 'object') for (const [k, v] of Object.entries(src)) take(k, v)
  return out
}

export function LiveProvider({ children }: { children: React.ReactNode }) {
  const toast = useToast()
  const [state, setState] = useState<StateResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [updatedAt, setUpdatedAt] = useState<number | null>(null)
  const [feed, setFeed] = useState<Decision[]>([])
  const [series, setSeries] = useState<Record<string, Series>>({})
  const [details, setDetails] = useState<Record<string, ProblemDetail>>({})
  const [logs, setLogs] = useState<(LogEvent & { at: number })[]>([])
  const [records, setRecords] = useState<RecordEvent[]>([])
  const detailsLoaded = useRef(false)

  const refresh = useCallback(async () => {
    try {
      const s = await api.state()
      setState(s)
      setError(null)
      setUpdatedAt(Date.now())
      // seed series with live metric values
      setSeries((prev) => {
        const next = { ...prev }
        const t = Date.parse(s.now) || Date.now()
        for (const p of s.problems) {
          if (typeof p.metric.value !== 'number') continue
          const arr = next[p.slug] ?? []
          const last = arr[arr.length - 1]
          if (!last || (t > last[0] && (last[1] !== p.metric.value || t - last[0] > 60000))) next[p.slug] = [...arr, [t, p.metric.value] as [number, number]].slice(-MAX_SERIES)
        }
        return next
      })
    } catch (e) {
      setError((e as Error).message)
    }
  }, [])

  const refreshDetail = useCallback(async (slug: string) => {
    try {
      const d = await api.problem(slug)
      setDetails((prev) => ({ ...prev, [slug]: d }))
      setSeries((prev) => {
        const hist = toSeries(d.metric_history)
        const cur = prev[slug] ?? []
        const lastHist = hist.length ? hist[hist.length - 1][0] : 0
        const merged = [...hist, ...cur.filter(([t]) => t > lastHist)].slice(-MAX_SERIES)
        return { ...prev, [slug]: merged }
      })
      return d
    } catch {
      return null
    }
  }, [])

  const loadFeed = useCallback(async () => {
    try {
      const rows = await api.decisions({ limit: 60 })
      setFeed((prev) => {
        const map = new Map<number, Decision>()
        for (const d of [...prev, ...rows]) map.set(d.id, d)
        return [...map.values()].sort((a, b) => b.id - a.id).slice(0, MAX_FEED)
      })
    } catch {
      /* state error banner covers connectivity */
    }
  }, [])

  const onEvent = useCallback(
    (ev: SseEventName, data: unknown) => {
      if (ev === 'phase') {
        const p = data as PhaseEvent
        setState((s) =>
          s
            ? {
                ...s,
                loop: {
                  ...s.loop,
                  phase: p.phase ?? s.loop.phase,
                  cycle: p.cycle ?? s.loop.cycle,
                  // pause / resume events carry the new loop status (another viewer may have clicked)
                  ...(p.status === 'running' || p.status === 'paused' ? { status: p.status } : {}),
                },
              }
            : s,
        )
        if (p.status) void refresh()
        if (p.phase === 'idle') void refresh()
      } else if (ev === 'decision') {
        const d = data as Decision
        if (!d || typeof d.id !== 'number') return
        setFeed((prev) => (prev.some((x) => x.id === d.id) ? prev : [d, ...prev].slice(0, MAX_FEED)))
        setState((s) => (s ? { ...s, totals: { ...s.totals, decisions: s.totals.decisions + 1 } } : s))
      } else if (ev === 'telemetry') {
        const d = (data ?? {}) as Record<string, unknown>
        const comp = (d.compute ?? (Array.isArray(d.gpus) ? d : null)) as Partial<ComputeState> | null
        const metrics = telemetryMetrics(d)
        const t = Date.now()
        setState((s) => {
          if (!s) return s
          const compute = comp
            ? {
                ...s.compute,
                ...(Array.isArray(comp.gpus) ? { gpus: comp.gpus.map((g) => ({ ...(s.compute.gpus.find((x) => x.idx === g.idx) ?? {}), ...g, mem_mb: g.mem_mb ?? (g as unknown as { mem?: number }).mem ?? 0 })) } : {}),
                ...(typeof comp.load1 === 'number' ? { load1: comp.load1 } : {}),
                ...(typeof comp.cpus === 'number' ? { cpus: comp.cpus } : {}),
                ...(comp.cpu_procs ? { cpu_procs: comp.cpu_procs } : {}),
                ...(comp.box ? { box: comp.box } : {}),
              }
            : s.compute
          const problems = s.problems.map((p) => (p.slug in metrics ? { ...p, metric: { ...p.metric, value: metrics[p.slug] } } : p))
          return { ...s, compute, problems }
        })
        setSeries((prev) => {
          const next = { ...prev }
          for (const [slug, v] of Object.entries(metrics)) {
            if (typeof v !== 'number') continue
            next[slug] = [...(next[slug] ?? []), [t, v] as [number, number]].slice(-MAX_SERIES)
          }
          return next
        })
      } else if (ev === 'record') {
        const r = data as RecordEvent
        setRecords((prev) => [r, ...prev].slice(0, 20))
        toast.push({
          kind: 'record',
          title: r.verified ? 'New verified record' : 'Candidate record (unverified)',
          msg: `${r.slug}: ${r.score}`,
          ttl: 12000,
        })
        void refresh()
        void refreshDetail(r.slug)
      } else if (ev === 'log') {
        const l = data as LogEvent
        setLogs((prev) => [{ ...l, at: Date.now() }, ...prev].slice(0, 100))
        if (l.level === 'error') toast.push({ kind: 'error', title: 'Loop error', msg: l.msg })
      }
    },
    [refresh, refreshDetail, toast],
  )

  const { status: stream, lastEventAt } = useEventStream(onEvent)

  // state polling: 5 s fallback while the stream is down, slower refresh while live
  useEffect(() => {
    void refresh()
    void loadFeed()
    if (STATIC) return
    const ms = stream === 'live' ? 15000 : 5000
    const t = setInterval(() => {
      if (document.visibilityState !== 'visible') return
      void refresh()
      if (stream !== 'live') void loadFeed()
    }, ms)
    return () => clearInterval(t)
  }, [stream, refresh, loadFeed])

  // problem details for sparklines + hero artifact
  useEffect(() => {
    if (!state || detailsLoaded.current) return
    detailsLoaded.current = true
    const slugs = state.problems.map((p) => p.slug)
    void Promise.all(slugs.map((s) => refreshDetail(s)))
    if (STATIC) return
    const t = setInterval(() => {
      if (document.visibilityState === 'visible') slugs.forEach((s) => void refreshDetail(s))
    }, 60000)
    return () => clearInterval(t)
  }, [state, refreshDetail])

  const applyLoop = useCallback((loop: LoopState) => {
    setState((s) => (s && loop ? { ...s, loop: { ...s.loop, ...loop } } : s))
  }, [])

  const value = useMemo<LiveCtx>(
    () => ({ state, error, stream, lastEventAt, updatedAt, feed, series, details, logs, records, refresh, refreshDetail, applyLoop }),
    [state, error, stream, lastEventAt, updatedAt, feed, series, details, logs, records, refresh, refreshDetail, applyLoop],
  )
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}
