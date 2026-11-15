// Typed API client matching SPEC.md section 4 exactly.
// live: fetch /api/*; static: read ./data/*.json under base; fixtures: in-browser simulated backend.
import { BASE, FIXTURES, STATIC } from './mode'
import type {
  PhysicsResponse,
  Decision,
  GalleryItem,
  LearningResponse,
  LiteratureItem,
  LoopActionResponse,
  MemoryResponse,
  OkErrResponse,
  OkIdResponse,
  OkResponse,
  ProblemDetail,
  SandboxRun,
  StateResponse,
  VerifyResponse,
} from './types'

export class ApiError extends Error {
  status: number
  constructor(message: string, status = 0) {
    super(message)
    this.status = status
  }
}

export class ReplayError extends ApiError {
  constructor() {
    super('Disabled: this is a static replay of a live run', 0)
  }
}

type Method = 'GET' | 'POST' | 'DELETE'

async function fixtureRequest<T>(method: Method, path: string, body?: unknown): Promise<T> {
  const mod = await import('./fixtures/server')
  return mod.fixtureFetch(method, path, body) as Promise<T>
}

async function liveRequest<T>(method: Method, path: string, body?: unknown, timeoutMs = 30000): Promise<T> {
  const ctrl = new AbortController()
  const timer = setTimeout(() => ctrl.abort(), timeoutMs)
  try {
    const res = await fetch(path, {
      method,
      headers: body !== undefined ? { 'Content-Type': 'application/json' } : undefined,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: ctrl.signal,
    })
    const text = await res.text()
    let data: unknown = null
    let isJson = false
    try {
      data = text ? JSON.parse(text) : null
      isJson = true
    } catch {
      data = null
    }
    // Something that is not ltd.server answered (e.g. another dev app bound to :8787 returns an HTML 404).
    if (!isJson || data === null) {
      const ct = res.headers.get('content-type') || 'no content type'
      throw new ApiError(
        `${method} ${path}: HTTP ${res.status}, not a JSON reply (${ct.split(';')[0]}). Is ltd.server running on 127.0.0.1:8787, or is another app answering on that port?`,
        res.status,
      )
    }
    if (!res.ok) {
      const detail =
        (typeof data === 'object' && ('detail' in (data as object) || 'error' in (data as object))
          ? String((data as Record<string, unknown>).detail ?? (data as Record<string, unknown>).error)
          : text.slice(0, 200)) || res.statusText
      throw new ApiError(`${res.status} ${detail}`, res.status)
    }
    return data as T
  } catch (e) {
    if (e instanceof ApiError) throw e
    if ((e as Error).name === 'AbortError') throw new ApiError(`Request timed out: ${method} ${path}`)
    throw new ApiError(`Backend unreachable (${(e as Error).message})`)
  } finally {
    clearTimeout(timer)
  }
}

const staticCache = new Map<string, Promise<unknown>>()
async function staticJson<T>(file: string): Promise<T> {
  if (!staticCache.has(file)) {
    const p = fetch(`${BASE}data/${file}`).then(async (r) => {
      if (!r.ok) throw new ApiError(`Snapshot file missing: data/${file}`, r.status)
      return r.json()
    })
    p.catch(() => staticCache.delete(file))
    staticCache.set(file, p)
  }
  return staticCache.get(file) as Promise<T>
}

function qs(params: Record<string, string | number | undefined | null>): string {
  const u = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== null && v !== '') u.set(k, String(v))
  const s = u.toString()
  return s ? `?${s}` : ''
}

function get<T>(path: string): Promise<T> {
  return FIXTURES ? fixtureRequest<T>('GET', path) : liveRequest<T>('GET', path)
}

function mutate<T>(method: Method, path: string, body?: unknown, timeoutMs?: number): Promise<T> {
  if (STATIC) return Promise.reject(new ReplayError())
  return FIXTURES ? fixtureRequest<T>(method, path, body) : liveRequest<T>(method, path, body, timeoutMs)
}

export interface DecisionQuery {
  problem?: string | null
  agent?: string | null
  limit?: number
  before?: number | null
}

export const api = {
  // ---- reads ----
  state(): Promise<StateResponse> {
    return STATIC ? staticJson<StateResponse>('state.json') : get('/api/state')
  },
  problem(slug: string): Promise<ProblemDetail> {
    return STATIC
      ? staticJson<ProblemDetail>(`problems/${encodeURIComponent(slug)}.json`)
      : get(`/api/problems/${encodeURIComponent(slug)}`)
  },
  async decisions(q: DecisionQuery = {}): Promise<Decision[]> {
    if (STATIC) {
      const all = await staticJson<Decision[]>('decisions.json')
      let rows = [...all].sort((a, b) => b.id - a.id)
      if (q.problem) rows = rows.filter((d) => d.problem === q.problem)
      if (q.agent) rows = rows.filter((d) => d.agent === q.agent)
      if (q.before != null) rows = rows.filter((d) => d.id < (q.before as number))
      return rows.slice(0, q.limit ?? 100)
    }
    return get(`/api/decisions${qs({ problem: q.problem, agent: q.agent, limit: q.limit, before: q.before })}`)
  },
  memory(): Promise<MemoryResponse> {
    return STATIC ? staticJson<MemoryResponse>('memory.json') : get('/api/memory')
  },
  async literature(problem?: string | null): Promise<LiteratureItem[]> {
    if (STATIC) {
      const all = await staticJson<LiteratureItem[]>('literature.json')
      return problem ? all.filter((l) => l.problem === problem) : all
    }
    return get(`/api/literature${qs({ problem })}`)
  },
  learning(): Promise<LearningResponse> {
    return STATIC ? staticJson<LearningResponse>('learning.json') : get('/api/learning')
  },
  async sandboxes(limit?: number): Promise<SandboxRun[]> {
    if (STATIC) {
      const all = await staticJson<SandboxRun[]>('sandboxes.json')
      return limit ? all.slice(0, limit) : all
    }
    return get(`/api/sandboxes${qs({ limit })}`)
  },
  physics(): Promise<PhysicsResponse> {
    return STATIC ? staticJson<PhysicsResponse>('physics.json') : get('/api/physics')
  },
  async gallery(): Promise<GalleryItem[]> {
    if (STATIC) {
      try {
        return await staticJson<GalleryItem[]>('gallery.json')
      } catch {
        const r = await fetch(`${BASE}gallery/gallery.json`)
        if (!r.ok) throw new ApiError('No gallery in this snapshot', r.status)
        return r.json()
      }
    }
    return get('/api/gallery')
  },

  // ---- mutations ----
  pause(): Promise<LoopActionResponse> {
    return mutate('POST', '/api/loop/pause')
  },
  resume(): Promise<LoopActionResponse> {
    return mutate('POST', '/api/loop/resume')
  },
  runNow(): Promise<LoopActionResponse> {
    return mutate('POST', '/api/loop/run-now')
  },
  verify(slug: string): Promise<VerifyResponse> {
    // the backend allows the official verifier up to 600 s for the heavy problems
    return mutate('POST', `/api/problems/${encodeURIComponent(slug)}/verify`, undefined, 620000)
  },
  launchStrategy(body: { problem: string; template: string; params: Record<string, unknown> }): Promise<OkIdResponse> {
    return mutate('POST', '/api/strategies', body, 60000)
  },
  stopStrategy(id: string): Promise<OkErrResponse> {
    return mutate('DELETE', `/api/strategies/${encodeURIComponent(id)}`, undefined, 60000)
  },
  startLearning(steps: number): Promise<OkResponse> {
    return mutate('POST', '/api/learning/start', { steps })
  },
  runMemoryBenchmark(): Promise<OkResponse> {
    return mutate('POST', '/api/memory/benchmark')
  },
  runSandboxes(problem: string, n: number): Promise<OkResponse> {
    return mutate('POST', '/api/sandboxes/run', { problem, n })
  },
}

/** Throws if an {ok:false,...} response came back so callers can surface it as an error state. */
export function ensureOk<T extends { ok: boolean; error?: string | null }>(r: T): T {
  if (!r || r.ok !== true) throw new ApiError(r?.error || 'Backend returned ok=false')
  return r
}
