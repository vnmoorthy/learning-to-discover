// Types mirroring SPEC.md section 4 (HTTP API contract). Keep in lockstep with the backend.

export type Phase = 'idle' | 'telemetry' | 'critic' | 'memory' | 'literature' | 'propose' | 'referee' | 'plan' | 'execute'

export interface LoopState {
  status: 'running' | 'paused'
  cycle: number
  phase: Phase
  next_cycle_at: string | null
  interval_s: number
  proposer_model: string
  started_at: string
  /** optional extra: PHOENIX_TEST_MODE=1 on the server (launches get test- ids, stops of adopted runs are dry runs) */
  test_mode?: boolean
}

export interface GpuInfo {
  idx: number
  util: number
  mem_mb: number
  problem: string | null
  strategy_id: string | null
  /** optional extras the backend may send when several strategies share a GPU */
  strategy_ids?: string[]
  problems?: string[]
}

export interface ComputeState {
  gpus: GpuInfo[]
  cpus: number
  load1: number
  cpu_procs: Record<string, number>
  box: 'online' | 'offline'
  /** optional extra from the backend: when the box telemetry was last read */
  telemetry_at?: string | null
  /** the elastic Modal CPU fleet the planner launches/cancels */
  modal?: { containers: number; by_problem: Record<string, number>; max: number; cpu_only?: boolean; error?: string | null; note?: string } | null
}

export interface Strategy {
  id: string
  template: string
  params: Record<string, unknown>
  resource: 'gpu' | 'cpu'
  started_at: string | null
  adopted: boolean
  metric_value: number | null
}

export type ProblemStatus = 'searching' | 'stalled' | 'record' | 'idle' | 'proved-negative' | 'verified'

export interface ProblemSummary {
  slug: string
  title: string
  scoring: 'maximize' | 'minimize'
  /** score is null for verified studies that have no leaderboard record (e.g. event-horizon) */
  record: { score: number | null; holder: string | null }
  ours: { score: number; verified: boolean; at: string; strategy_id: string | null } | null
  beats_record: boolean
  metric: { name: string; value: number | null; target: number | null; lower_is_better: boolean }
  status: ProblemStatus
  compute: { gpus: number; cpu_procs: number; share: number }
  strategies: Strategy[]
}

export interface Totals {
  decisions: number
  cycles: number
  experiments_run: number
  sandboxes_run: number
  facts: number
  sources: number
  records: number
}

export interface StateResponse {
  now: string
  loop: LoopState
  compute: ComputeState
  problems: ProblemSummary[]
  totals: Totals
  /** present only in static snapshots written by `python3 -m phoenixastar.snapshot` */
  snapshot?: { generated_at: string; label?: string; telemetry_at?: string | null }
}

export type Point = [number, number]
export type ViolatedLine = [Point, Point, number]

export interface GridArtifact {
  kind: 'grid'
  n: number
  points: Point[]
  violated_lines: ViolatedLine[]
  count: number
  sym: string
  round: number
}

export interface SignMatrixArtifact {
  kind: 'sign_matrix'
  n: number
  D?: number
  matrix: number[][]
  bad_vectors?: number
  total_vectors?: number
  log10_det?: number
}

export interface IntegerSetArtifact {
  kind: 'integer_set'
  elements: number[]
  h: number
  score: number
}

export interface CodeArtifact {
  kind: 'code'
  words: string[]
  count: number
}

export interface ReportArtifact {
  hero?: string
  hero_caption?: string
  interactive?: 'blackhole' | 'neutronstar'
  kind: 'report'
  title?: string
  question?: string
  summary?: string
  figures?: EHFigure[]
  cycles?: EHCycle[]
  tests?: { passed?: number; failed?: number; total?: number }
  verification?: unknown
  hardware?: string
  paper?: string
  notebook?: string
}

export type Artifact = (GridArtifact | SignMatrixArtifact | IntegerSetArtifact | CodeArtifact | ReportArtifact) & {
  /** optional provenance note from the backend, e.g. "current SAT model ..., not yet valid" */
  label?: string
  source?: string
}

export interface ParamSpec {
  type: 'int' | 'float' | 'enum'
  min?: number
  max?: number
  values?: (string | number)[]
  default?: string | number
}

export interface Template {
  name: string
  resource: string
  params: Record<string, ParamSpec>
}

export interface ProblemDetail extends ProblemSummary {
  description_md: string
  leaderboard: { rank: number; agent: string; score: number }[]
  metric_history: [string, number][]
  artifact: Artifact | null
  templates: Template[]
}

export type Agent =
  | 'planner'
  | 'proposer'
  | 'critic'
  | 'executor'
  | 'literature'
  | 'memory'
  | 'sandbox'
  | 'learning'
  | 'referee'
  | 'toolsmith'
  | 'system'

export const AGENTS: Agent[] = ['planner', 'proposer', 'referee', 'critic', 'executor', 'literature', 'memory', 'sandbox', 'toolsmith', 'learning', 'system']

export interface Source {
  id: number
  title: string
  url: string
  published: string | null
}

export interface Decision {
  id: number
  cycle: number
  time: string
  agent: Agent
  problem: string | null
  action: string
  params: Record<string, unknown>
  rationale: string
  prediction: { metric: string; expected: number; horizon_min: number } | null
  outcome: { observed: number | null; verdict: 'confirmed' | 'refuted' | 'pending' | 'n/a'; note: string } | null
  sources: Source[]
  memory_reads: string[]
  memory_writes: string[]
  model: string | null
  tokens: number | null
  latency_ms: number | null
}

export interface Fact {
  id: string
  agent: string
  problem: string | null
  text: string
  time: string
  read_by: string[]
}

export interface BenchmarkSystem {
  name: 'past.dev' | 'markdown' | 'rag' | string
  accuracy: number
  latency_ms: number
  cost_usd: number
  n: number
}

export interface MemoryResponse {
  facts: Fact[]
  agents: string[]
  links: { from_agent: string; to_agent: string; fact_id: string }[]
  benchmark: { systems: BenchmarkSystem[]; time: string } | null
}

export interface LiteratureItem {
  id: number
  problem: string
  query: string
  title: string
  url: string
  published: string | null
  highlight: string
  cited_by: number[]
}

export interface LearningStep {
  step: number
  reward_mean: number
  reward_best: number
  valid_rate: number
  time: string
}

export interface LearningResponse {
  status: 'idle' | 'running' | 'done' | 'error'
  base_model: string
  problem: string
  steps: LearningStep[]
  eval: { gen0: { score: number; valid_rate: number }; genN: { score: number; valid_rate: number }; heldout: string } | null
  best: { solution: Record<string, unknown>; score: number } | null
}

export interface SandboxRun {
  id: number
  problem: string
  time: string
  code: string
  status: 'ok' | 'invalid' | 'timeout' | 'error'
  score: number | null
  seconds: number
  decision_id: number
}

export interface GalleryItem {
  title: string
  src: string
  kind: 'image' | 'video'
  made_with: string
  caption: string
}

export interface LoopActionResponse {
  ok: boolean
  loop: LoopState
}

export interface VerifyResponse {
  ok: boolean
  score: number | null
  beats_record: boolean
  error: string | null
  seconds: number
  /** optional extra from the backend: whose solution was verified ("ours" | "candidate" | "record" | null) */
  source?: string | null
}

export interface OkIdResponse {
  ok: boolean
  id: string | null
  error: string | null
}

export interface OkErrResponse {
  ok: boolean
  error: string | null
}

export interface OkResponse {
  ok: boolean
  /** the backend adds an error message when ok is false */
  error?: string | null
}

// SSE event payloads
export interface PhaseEvent {
  phase: Phase
  cycle: number
  /** sent by the backend on pause / resume */
  status?: 'running' | 'paused'
}
export interface RecordEvent {
  slug: string
  score: number
  verified: boolean
}
export interface LogEvent {
  level: string
  msg: string
}


export interface ThreeBodyOrbit { vx: number; vy: number; T: number; m3?: number }
export interface EHFigure { title: string; path?: string; src?: string; caption?: string; classification?: number | string }
export interface EHCycle {
  id?: string | number
  question?: string
  hypothesis?: string
  derivation_summary?: string
  prediction?: string
  experiment?: unknown
  result?: string
  verification?: string
  critic_objections?: string | string[]
  revised_hypothesis?: string
  conclusion?: string
  classification?: number | string
}
export interface PhysicsResponse {
  threebody: {
    title?: string
    score?: number | null
    verified?: boolean
    time?: string | null
    orbits: ThreeBodyOrbit[]
    catalog_entries: number
    not_checked?: unknown
    image: string
    verification?: string
    novelty?: string
    caveats?: string
  } | null
  event_horizon: {
    title?: string
    question?: string
    summary?: string
    cycles?: EHCycle[]
    figures?: EHFigure[]
    tests?: { passed?: number; failed?: number; total?: number }
    verification?: unknown
    hardware?: string
  } | null
  /** STARFORGE: neutron-star equation of state (same report schema) */
  neutron_star?: PhysicsResponse['event_horizon']
}
