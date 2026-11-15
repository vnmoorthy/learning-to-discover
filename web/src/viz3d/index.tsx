// Interactive viewers (lazy chunk): each wraps a scene in the shared Stage and adds its own read-outs.
import { useFrame, useThree } from '@react-three/fiber'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'
import { ErrorBoundary } from '../components/ErrorBoundary'
import { conflictCounts } from '../lib/geometry'
import { cx } from '../lib/format'
import type { GridArtifact, SignMatrixArtifact } from '../types'
import { CityScene, LatticeScene, SnakeScene, type SnakeData } from './scenes'
import snakeJson from './snake.json'
import { C, Stage } from './Stage'
import { integrate, type Orbit } from './threebody'

const NoGL = ({ children }: { children?: React.ReactNode }) => (
  <div className="absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim">{children ?? '3D view unavailable (WebGL disabled)'}</div>
)

const Readout = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cx('pointer-events-none absolute bottom-3 left-3 max-w-[calc(100%-24px)] rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur', className)}>{children}</div>
)

export function LatticeViewer({ art, hero, fallback, readout = true }: { art: GridArtifact | null; hero?: boolean; fallback?: React.ReactNode; readout?: boolean }) {
  const [sel, setSel] = useState<number | null>(null)
  const conf = useMemo(() => (art ? conflictCounts(art.points, art.violated_lines) : []), [art])
  useEffect(() => setSel(null), [art])
  const p = sel != null ? art?.points[sel] : null
  return (
    <ErrorBoundary fallback={fallback ?? <NoGL />}>
      <Stage
        camera={hero ? [0, 4.6, 8.4] : [0, 5.4, 8.2]}
        target={[0, 0.1, 0]}
        focusZoom
        overlay={
          readout && (
            <Readout className={hero ? '!bottom-auto !left-auto right-3 top-12' : undefined}>
              {p ? (
                <>
                  <span className="text-fg">({p[0]}, {p[1]})</span>{' '}
                  {conf[sel!] > 0 ? <span className="text-bad">on {conf[sel!]} violated {conf[sel!] === 1 ? 'line' : 'lines'}</span> : <span className="text-cyan">clean point</span>}
                </>
              ) : art ? (
                hero ? 'Tap a pillar to inspect it' : <>{art.count ?? art.points.length} points · {art.violated_lines.length} violated lines · tap a pillar</>
              ) : (
                'waiting for model'
              )}
            </Readout>
          )
        }
      >
        <LatticeScene art={art} selected={sel} onSelect={setSel} />
      </Stage>
    </ErrorBoundary>
  )
}

export function CityViewer({ art, fallback }: { art: SignMatrixArtifact | null; fallback?: React.ReactNode }) {
  const [sel, setSel] = useState<number | null>(null)
  const n = art?.matrix.length ?? 0
  const plus = useMemo(() => art?.matrix.reduce((s, r) => s + r.filter((v) => v > 0).length, 0) ?? 0, [art])
  return (
    <ErrorBoundary fallback={fallback ?? <NoGL />}>
      <Stage
        camera={[5.2, 5.4, 6.6]}
        target={[0, 0.2, 0]}
        focusZoom
        overlay={
          <Readout>
            {sel != null && n ? (
              <>
                <span className="text-fg">row {Math.floor(sel / n)}, col {sel % n}</span> entry <span className={art!.matrix[Math.floor(sel / n)][sel % n] > 0 ? 'text-cyan' : 'text-amber'}>{art!.matrix[Math.floor(sel / n)][sel % n] > 0 ? '+1' : '-1'}</span>
              </>
            ) : n ? (
              <>{n} x {n} · {plus} towers (+1) · {n * n - plus} plinths (-1) · tap an entry</>
            ) : (
              'no matrix'
            )}
          </Readout>
        }
      >
        <CityScene art={art} selected={sel} onSelect={setSel} />
      </Stage>
    </ErrorBoundary>
  )
}

export function SnakeViewer({ fallback }: { fallback?: React.ReactNode }) {
  const data = snakeJson as SnakeData
  const [upTo, setUpTo] = useState(data.path.length)
  return (
    <ErrorBoundary fallback={fallback ?? <NoGL />}>
      <Stage
        camera={[0, 3.2, 12.5]}
        target={[0, 0, 0]}
        fov={36}
        focusZoom
        minDistance={3}
        maxDistance={30}
        maxPolar={Math.PI}
        overlay={
          <div className="absolute inset-x-3 bottom-3 flex items-center gap-3 rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur">
            <span className="shrink-0">
              edge <span className="text-fg">{Math.max(0, upTo - 1)}</span> / {data.edges}
            </span>
            <input type="range" aria-label="Walk along the snake" min={2} max={data.path.length} value={upTo} onChange={(e) => setUpTo(Number(e.target.value))} className="h-1 min-w-0 flex-1 accent-[#4FD1E0]" />
          </div>
        }
      >
        <SnakeScene data={data} upTo={upTo} />
      </Stage>
    </ErrorBoundary>
  )
}

const BODY = [C.cyan, C.violet, C.amber]

function OrbitBodies({ traj, time, playing, speed, onTick, shown }: { shown: number; traj: ReturnType<typeof integrate>; time: React.MutableRefObject<number>; playing: boolean; speed: number; onTick: (t: number) => void }) {
  const lines = useMemo(() => {
    const mk = (b: number, opacity: number) => {
      const arr = new Float32Array((traj.samples + 1) * 3)
      for (let i = 0; i <= traj.samples; i++) {
        arr[i * 3] = traj.pos[i * 6 + 2 * b]
        arr[i * 3 + 1] = 0
        arr[i * 3 + 2] = -traj.pos[i * 6 + 2 * b + 1]
      }
      const g = new THREE.BufferGeometry()
      g.setAttribute('position', new THREE.BufferAttribute(arr, 3))
      return new THREE.Line(g, new THREE.LineBasicMaterial({ color: BODY[b], transparent: true, opacity, depthWrite: false, toneMapped: false }))
    }
    return [0, 1, 2].map((b) => ({ full: mk(b, 0.2), head: mk(b, 1) }))
  }, [traj])
  useEffect(() => () => lines.forEach((l) => { l.full.geometry.dispose(); l.head.geometry.dispose() }), [lines])
  const balls = useRef<(THREE.Mesh | null)[]>([])
  const invalidate = useThree((s) => s.invalidate)
  useEffect(() => invalidate(), [shown, invalidate])
  const TAIL = Math.round(traj.samples * 0.12)

  useFrame((_, dt) => {
    if (playing) {
      time.current = (time.current + Math.min(dt, 0.05) * speed) % traj.T
      onTick(time.current)
    }
    const f = (time.current / traj.T) * traj.samples
    const i = Math.min(traj.samples - 1, Math.floor(f))
    const u = f - i
    for (let b = 0; b < 3; b++) {
      const x = traj.pos[i * 6 + 2 * b] * (1 - u) + traj.pos[(i + 1) * 6 + 2 * b] * u
      const y = traj.pos[i * 6 + 2 * b + 1] * (1 - u) + traj.pos[(i + 1) * 6 + 2 * b + 1] * u
      balls.current[b]?.position.set(x, 0, -y)
      const start = Math.max(0, i - TAIL)
      lines[b].head.geometry.setDrawRange(start, i - start + 2)
    }
  })

  return (
    <group>
      {lines.map((l, b) => (
        <group key={b}>
          <primitive object={l.full} />
          <primitive object={l.head} />
          <mesh ref={(m) => (balls.current[b] = m)}>
            <sphereGeometry args={[b === 2 ? 0.075 : 0.09, 24, 24]} />
            <meshBasicMaterial color={BODY[b]} toneMapped={false} />
          </mesh>
        </group>
      ))}
      <gridHelper args={[Math.ceil(traj.extent) * 2 + 2, Math.ceil(traj.extent) * 2 + 2, '#2A303A', '#1A1E25']} position={[0, -0.02, 0]} />
    </group>
  )
}

/** The candidate three-body orbits, re-integrated in the browser, with play / pause, time scrub and a candidate picker. */
export function OrbitsViewer({ orbits, fallback, className }: { orbits: Orbit[]; fallback?: React.ReactNode; className?: string }) {
  const [idx, setIdx] = useState(0)
  const [playing, setPlaying] = useState(true)
  const [shown, setShown] = useState(0)
  const time = useRef(0)
  const lastUi = useRef(0)
  const o = orbits[Math.min(idx, orbits.length - 1)]
  const traj = useMemo(() => (o ? integrate(o) : null), [o])
  useEffect(() => {
    time.current = 0
    setShown(0)
  }, [idx])
  if (!o || !traj) return <NoGL>No orbits to show</NoGL>
  const dist = Math.max(4.5, traj.extent * 3.1)
  const onTick = (t: number) => {
    const now = performance.now()
    if (now - lastUi.current > 80) {
      lastUi.current = now
      setShown(t)
    }
  }
  return (
    <div className={cx('absolute inset-0 flex flex-col', className)}>
      <div className="relative min-h-0 flex-1">
        <ErrorBoundary fallback={fallback ?? <NoGL />}>
          <Stage
            key={idx}
            camera={[0, dist * 0.82, dist * 0.58]}
            target={[0, 0, 0]}
            spin={false}
            animating={playing}
            focusZoom
            onTap={() => setPlaying((p) => !p)}
            minDistance={1.5}
            maxDistance={dist * 3}
            maxPolar={Math.PI}
            overlay={
              <Readout>
                candidate <span className="text-fg">{idx + 1}</span> · T <span className="text-fg">{o.T.toFixed(4)}</span> · m3 <span className="text-fg">{o.m3 ?? 1}</span> · RK4 closure <span className="text-fg">{traj.closure.toExponential(1)}</span>
              </Readout>
            }
          >
            <OrbitBodies traj={traj} time={time} playing={playing} speed={Math.max(1.2, traj.T / 18)} onTick={onTick} shown={shown} />
          </Stage>
        </ErrorBoundary>
      </div>
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2 border-t border-white/[0.07] bg-ink-800 px-3 py-2">
        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          aria-label={playing ? 'Pause' : 'Play'}
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-white/10 bg-white/[0.03] text-fg transition-colors hover:border-white/20 hover:bg-white/[0.06]"
        >
          {playing ? (
            <svg viewBox="0 0 16 16" className="h-3 w-3" fill="currentColor" aria-hidden><rect x="3.5" y="3" width="3" height="10" rx="0.8" /><rect x="9.5" y="3" width="3" height="10" rx="0.8" /></svg>
          ) : (
            <svg viewBox="0 0 16 16" className="h-3 w-3" fill="currentColor" aria-hidden><path d="M4.5 2.8v10.4a.6.6 0 0 0 .9.5l8.3-5.2a.6.6 0 0 0 0-1L5.4 2.3a.6.6 0 0 0-.9.5z" /></svg>
          )}
        </button>
        <input
          type="range"
          aria-label="Time"
          min={0}
          max={1000}
          value={Math.round((shown / traj.T) * 1000)}
          onChange={(e) => {
            time.current = (Number(e.target.value) / 1000) * traj.T * 0.9999
            setShown(time.current)
            setPlaying(false)
          }}
          className="h-1 min-w-[120px] flex-1 accent-[#4FD1E0]"
        />
        <span className="shrink-0 font-mono text-[11px] tabular-nums text-fg-muted">
          t = <span className="text-fg">{shown.toFixed(2)}</span> / {traj.T.toFixed(2)}
        </span>
        <div className="flex shrink-0 items-center gap-1" role="group" aria-label="Candidate">
          {orbits.map((_, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setIdx(i)}
              aria-pressed={i === idx}
              className={cx(
                'h-7 w-7 rounded-md border font-mono text-[11.5px] transition-colors',
                i === idx ? 'border-cyan/50 bg-cyan/[0.1] text-cyan' : 'border-white/10 text-fg-muted hover:border-white/20 hover:text-fg',
              )}
            >
              {i + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
