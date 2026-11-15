// Dev-only simulated backend (VITE_FIXTURES=1). Mirrors SPEC section 4 so the UI can be built and demoed
// without the Python server. Everything it returns is labeled "fixture" in the UI banner.
import type {
  Decision,
  GalleryItem,
  LearningResponse,
  LiteratureItem,
  MemoryResponse,
  Phase,
  ProblemDetail,
  SandboxRun,
  StateResponse,
  Strategy,
} from '../types'
// JSON is loaded through import.meta.glob so TypeScript does not infer types for the (large) fixture files.
const files = import.meta.glob('./*.json', { eager: true, import: 'default' }) as Record<string, unknown>
const problemFiles = import.meta.glob('./problems/*.json', { eager: true, import: 'default' }) as Record<string, unknown>
const state0 = files['./state.json']
const decisions0 = files['./decisions.json']
const memory0 = files['./memory.json']
const literature0 = files['./literature.json']
const learning0 = files['./learning.json']
const sandboxes0 = files['./sandboxes.json']
const gallery0 = files['./gallery.json'] ?? []

const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/
const OFFSET = Date.now() - Date.parse((state0 as { now: string }).now)
function rebase<T>(v: T): T {
  if (typeof v === 'string') return (ISO.test(v) ? new Date(Date.parse(v) + OFFSET).toISOString() : v) as T
  if (Array.isArray(v)) return v.map(rebase) as T
  if (v && typeof v === 'object') {
    const o: Record<string, unknown> = {}
    for (const [k, x] of Object.entries(v)) o[k] = rebase(x)
    return o as T
  }
  return v
}

const db = {
  state: rebase(state0 as unknown as StateResponse),
  problems: Object.fromEntries(
    Object.values(problemFiles).map((p) => {
      const d = rebase(p as ProblemDetail)
      return [d.slug, d]
    }),
  ) as Record<string, ProblemDetail>,
  decisions: rebase(decisions0 as unknown as Decision[]),
  memory: rebase(memory0 as unknown as MemoryResponse),
  literature: rebase(literature0 as unknown as LiteratureItem[]),
  learning: rebase(learning0 as unknown as LearningResponse),
  sandboxes: rebase(sandboxes0 as unknown as SandboxRun[]),
  gallery: gallery0 as unknown as GalleryItem[],
}

const SIM_INTERVAL_S = 60
db.state.loop.interval_s = SIM_INTERVAL_S
db.state.loop.next_cycle_at = new Date(Date.now() + 20000).toISOString()

type Listener = (event: string, data: unknown) => void
const listeners = new Set<Listener>()
function emit(event: string, data: unknown) {
  listeners.forEach((l) => l(event, data))
}
export function subscribe(fn: Listener): () => void {
  listeners.add(fn)
  return () => listeners.delete(fn)
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))
const nowIso = () => new Date().toISOString()
let nextDecisionId = Math.max(...db.decisions.map((d) => d.id)) + 1

function pushDecision(d: Omit<Decision, 'id' | 'time' | 'cycle'> & Partial<Pick<Decision, 'cycle'>>) {
  const full: Decision = { ...d, id: nextDecisionId++, time: nowIso(), cycle: d.cycle ?? db.state.loop.cycle } as Decision
  db.decisions.unshift(full)
  db.state.totals.decisions += 1
  emit('decision', full)
  return full
}

function syncSummaries() {
  db.state.problems = db.state.problems.map((p) => {
    const d = db.problems[p.slug]
    if (!d) return p
    d.strategies = p.strategies
    d.metric = p.metric
    d.status = p.status
    d.ours = p.ours
    return p
  })
}

// ---- the simulated loop ----
const PHASES: Phase[] = ['telemetry', 'critic', 'memory', 'literature', 'propose', 'plan', 'execute']
let running = false

async function runCycle() {
  if (running) return
  running = true
  const loop = db.state.loop
  loop.cycle += 1
  db.state.totals.cycles += 1
  pushDecision({
    agent: 'system', problem: null, action: 'cycle_start', params: { interval_s: SIM_INTERVAL_S },
    rationale: `Cycle ${loop.cycle} started (fixture simulation).`, prediction: null, outcome: null, sources: [],
    memory_reads: [], memory_writes: [], model: null, tokens: null, latency_ms: null,
  })
  for (const ph of PHASES) {
    loop.phase = ph
    emit('phase', { phase: ph, cycle: loop.cycle })
    await sleep(2200 + Math.random() * 1400)
    if (ph === 'memory') {
      pushDecision({
        agent: 'memory', problem: null, action: 'recall', params: { k: 6 },
        rationale: 'Recalled 6 facts from shared space phoenixastar-lab (fixture).', prediction: null, outcome: null, sources: [],
        memory_reads: db.memory.facts.slice(0, 4).map((f) => f.id), memory_writes: [], model: null, tokens: null, latency_ms: 380,
      })
    }
    if (ph === 'propose') {
      const nt = db.state.problems.find((p) => p.slug === 'no-three-in-line-75')
      const cur = nt?.metric.value ?? 131
      pushDecision({
        agent: 'proposer', problem: 'no-three-in-line-75', action: 'keep', params: {},
        rationale: `rot180-150 still declining (${cur} violated lines). Keep allocation; expect a further drop of ~6 lines within 30 minutes.`,
        prediction: { metric: 'min_violated_lines', expected: Math.max(0, (cur as number) - 6), horizon_min: 30 },
        outcome: { observed: null, verdict: 'pending', note: '' },
        sources: db.literature.slice(1, 2).map((l) => ({ id: l.id, title: l.title, url: l.url, published: l.published })),
        memory_reads: ['f_001', 'f_013'], memory_writes: [], model: loop.proposer_model, tokens: 6400 + Math.round(Math.random() * 900), latency_ms: 8000 + Math.round(Math.random() * 3000),
      })
    }
    if (ph === 'plan') {
      pushDecision({
        agent: 'planner', problem: null, action: 'priorities', params: { free_gpus: 0, free_cores: 3 },
        rationale: 'UCB priorities recomputed; budgets respected, no action exceeds free resources.', prediction: null, outcome: null,
        sources: [], memory_reads: ['f_006'], memory_writes: [], model: null, tokens: null, latency_ms: null,
      })
    }
  }
  loop.phase = 'idle'
  loop.next_cycle_at = new Date(Date.now() + SIM_INTERVAL_S * 1000).toISOString()
  emit('phase', { phase: 'idle', cycle: loop.cycle })
  running = false
}

setInterval(() => {
  const loop = db.state.loop
  if (loop.status === 'running' && !running && loop.next_cycle_at && Date.parse(loop.next_cycle_at) <= Date.now()) void runCycle()
}, 1000)

// telemetry jitter every 5 s
setInterval(() => {
  const c = db.state.compute
  c.gpus = c.gpus.map((g) => ({ ...g, util: Math.max(0, Math.min(100, Math.round(g.util + (Math.random() - 0.5) * 6))) }))
  c.load1 = Math.round((118 + Math.random() * 4) * 100) / 100
  const metrics: Record<string, number | null> = {}
  for (const p of db.state.problems) {
    if (p.slug === 'no-three-in-line-75' && typeof p.metric.value === 'number' && Math.random() < 0.25) p.metric.value -= 1
    if (p.slug === 'two-deletion-code-16' && typeof p.metric.value === 'number' && Math.random() < 0.05 && p.metric.value < 225) p.metric.value += 1
    metrics[p.slug] = p.metric.value
    const d = db.problems[p.slug]
    if (d && p.metric.value != null) d.metric_history.push([nowIso(), p.metric.value])
  }
  syncSummaries()
  emit('telemetry', { ...c, metrics })
}, 5000)

// ---- request router ----
function json<T>(v: T): T {
  return JSON.parse(JSON.stringify(v))
}

class FixtureHttpError extends Error {}

export async function fixtureFetch(method: string, path: string, body?: unknown): Promise<unknown> {
  await sleep(120 + Math.random() * 180)
  const url = new URL(path, 'http://fixture')
  const p = url.pathname
  const q = url.searchParams
  const b = (body ?? {}) as Record<string, unknown>

  if (method === 'GET') {
    if (p === '/api/state') return json({ ...db.state, now: nowIso() })
    const m = p.match(/^\/api\/problems\/([^/]+)$/)
    if (m) {
      const d = db.problems[decodeURIComponent(m[1])]
      if (!d) throw new FixtureHttpError('404 unknown problem')
      const s = db.state.problems.find((x) => x.slug === d.slug)
      return json({ ...d, ...s })
    }
    if (p === '/api/decisions') {
      let rows = db.decisions
      if (q.get('problem')) rows = rows.filter((d) => d.problem === q.get('problem'))
      if (q.get('agent')) rows = rows.filter((d) => d.agent === q.get('agent'))
      if (q.get('before')) rows = rows.filter((d) => d.id < Number(q.get('before')))
      return json(rows.slice(0, Number(q.get('limit') || 100)))
    }
    if (p === '/api/memory') return json(db.memory)
    if (p === '/api/literature') return json(q.get('problem') ? db.literature.filter((l) => l.problem === q.get('problem')) : db.literature)
    if (p === '/api/learning') return json(db.learning)
    if (p === '/api/sandboxes') return json(db.sandboxes.slice(0, Number(q.get('limit') || 200)))
    if (p === '/api/gallery') {
      try {
        const r = await fetch('/gallery/gallery.json')
        if (r.ok) return await r.json()
      } catch {
        /* fall through */
      }
      return json(db.gallery)
    }
  }

  if (method === 'POST') {
    const loop = db.state.loop
    if (p === '/api/loop/pause') {
      loop.status = 'paused'
      return { ok: true, loop: json(loop) }
    }
    if (p === '/api/loop/resume') {
      loop.status = 'running'
      if (!loop.next_cycle_at || Date.parse(loop.next_cycle_at) < Date.now()) loop.next_cycle_at = new Date(Date.now() + SIM_INTERVAL_S * 1000).toISOString()
      return { ok: true, loop: json(loop) }
    }
    if (p === '/api/loop/run-now') {
      void runCycle()
      return { ok: true, loop: json(loop) }
    }
    const v = p.match(/^\/api\/problems\/([^/]+)\/verify$/)
    if (v) {
      const s = db.state.problems.find((x) => x.slug === decodeURIComponent(v[1]))
      await sleep(1400)
      if (!s?.ours) return { ok: false, score: null, beats_record: false, error: 'no solution to verify yet', seconds: 0.0, source: null }
      pushDecision({
        agent: 'critic', problem: s.slug, action: 'verify', params: { score: s.ours.score },
        rationale: `Manual verify: official verifier returned ${s.ours.score} (fixture).`, prediction: null, outcome: null,
        sources: [], memory_reads: [], memory_writes: [], model: null, tokens: null, latency_ms: 1400,
      })
      return { ok: true, score: s.ours.score, beats_record: s.beats_record, error: null, seconds: 1.4, source: 'ours' }
    }
    if (p === '/api/strategies') {
      const slug = String(b.problem)
      const d = db.problems[slug]
      const s = db.state.problems.find((x) => x.slug === slug)
      const t = d?.templates.find((x) => x.name === b.template)
      if (!d || !s || !t) return { ok: false, id: null, error: 'Unknown problem or template' }
      const params = (b.params || {}) as Record<string, unknown>
      for (const [k, spec] of Object.entries(t.params)) {
        const val = params[k]
        if (spec.type === 'enum' && !spec.values?.includes(val as never)) return { ok: false, id: null, error: `${k} must be one of ${spec.values?.join(', ')}` }
        if (spec.type !== 'enum') {
          const n = Number(val)
          if (!Number.isFinite(n)) return { ok: false, id: null, error: `${k} must be a number` }
          if (spec.type === 'int' && !Number.isInteger(n)) return { ok: false, id: null, error: `${k} must be an integer` }
          if ((spec.min != null && n < spec.min) || (spec.max != null && n > spec.max)) return { ok: false, id: null, error: `${k} out of range [${spec.min}, ${spec.max}]` }
        }
      }
      if (t.resource === 'gpu') return { ok: false, id: null, error: 'No free GPU: all 8 are owned by running strategies' }
      const id = `manual-${t.name}-${Math.random().toString(36).slice(2, 7)}`
      const st: Strategy = { id, template: t.name, params, resource: 'cpu', started_at: nowIso(), adopted: false, metric_value: null }
      s.strategies = [st, ...s.strategies]
      s.compute.cpu_procs += 1
      db.state.compute.cpu_procs[slug] = (db.state.compute.cpu_procs[slug] || 0) + 1
      db.state.totals.experiments_run += 1
      syncSummaries()
      pushDecision({
        agent: 'executor', problem: slug, action: 'launch', params: { strategy_id: id, template: t.name, ...params },
        rationale: `Manual launch from the UI (fixture).`, prediction: null, outcome: null, sources: [], memory_reads: [], memory_writes: [], model: null, tokens: null, latency_ms: null,
      })
      return { ok: true, id, error: null }
    }
    if (p === '/api/learning/start') {
      const steps = Number(b.steps)
      if (!Number.isInteger(steps) || steps < 1) return { ok: false }
      db.learning.status = 'running'
      let left = Math.min(steps, 30)
      const timer = setInterval(() => {
        const last = db.learning.steps[db.learning.steps.length - 1]
        const s = (last?.step ?? -1) + 1
        const rm = Math.min(0.95, (last?.reward_mean ?? 0.1) + (Math.random() - 0.3) * 0.02)
        db.learning.steps.push({ step: s, reward_mean: +rm.toFixed(4), reward_best: +Math.min(1, rm + 0.18).toFixed(4), valid_rate: +Math.min(1, (last?.valid_rate ?? 0.3) + 0.003).toFixed(4), time: nowIso() })
        if (--left <= 0) {
          clearInterval(timer)
          db.learning.status = 'done'
        }
      }, 2000)
      return { ok: true }
    }
    if (p === '/api/memory/benchmark') {
      setTimeout(() => {
        if (db.memory.benchmark) db.memory.benchmark = { ...db.memory.benchmark, time: nowIso() }
      }, 3500)
      return { ok: true }
    }
    if (p === '/api/sandboxes/run') {
      const n = Math.max(1, Math.min(16, Number(b.n) || 1))
      const problem = String(b.problem)
      setTimeout(() => {
        const dec = pushDecision({
          agent: 'sandbox', problem, action: 'sandbox', params: { n },
          rationale: `Ran ${n} Modal sandboxes (fixture simulation).`, prediction: null, outcome: null, sources: [], memory_reads: [], memory_writes: [], model: null, tokens: null, latency_ms: null,
        })
        const base = db.sandboxes[0]
        for (let i = 0; i < n; i++) {
          const ok = Math.random() > 0.25
          db.sandboxes.unshift({
            id: (db.sandboxes[0]?.id ?? 0) + 1, problem, time: nowIso(), code: base?.code ?? '# program', status: ok ? 'ok' : 'invalid',
            score: ok ? +(0.6 + Math.random() * 0.1).toFixed(4) : null, seconds: +(20 + Math.random() * 90).toFixed(1), decision_id: dec.id,
          })
        }
        db.state.totals.sandboxes_run += n
      }, 4000)
      return { ok: true }
    }
  }

  if (method === 'DELETE') {
    const m = p.match(/^\/api\/strategies\/([^/]+)$/)
    if (m) {
      const id = decodeURIComponent(m[1])
      for (const s of db.state.problems) {
        const st = s.strategies.find((x) => x.id === id)
        if (st) {
          s.strategies = s.strategies.filter((x) => x.id !== id)
          if (st.resource === 'cpu') {
            s.compute.cpu_procs = Math.max(0, s.compute.cpu_procs - 1)
            db.state.compute.cpu_procs[s.slug] = Math.max(0, (db.state.compute.cpu_procs[s.slug] || 1) - 1)
          }
          syncSummaries()
          pushDecision({
            agent: 'executor', problem: s.slug, action: 'stop', params: { strategy_id: id },
            rationale: 'Manual stop from the UI (fixture).', prediction: null, outcome: null, sources: [], memory_reads: [], memory_writes: [], model: null, tokens: null, latency_ms: null,
          })
          return { ok: true, error: null }
        }
      }
      return { ok: false, error: `Unknown strategy ${id}` }
    }
  }
  throw new Error(`fixture: no route for ${method} ${path}`)
}
