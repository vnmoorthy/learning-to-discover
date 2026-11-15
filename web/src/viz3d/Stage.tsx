// Shared real-time 3D stage: orbit controls for mouse and touch (drag = rotate, scroll / pinch = zoom,
// right-drag / two fingers = pan, tap = pause), dpr capped at 2, renders on demand when nothing moves.
import { OrbitControls } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { useEffect, useRef, useState, type ReactNode } from 'react'
import * as THREE from 'three'
import { cx } from '../lib/format'

export const C = {
  bg: '#0E1014',
  floor: '#12161B',
  dot: '#566070',
  cyan: '#4FD1E0',
  ice: '#CFF5FA',
  red: '#E5676B',
  amber: '#E2B25C',
  violet: '#A99BEA',
  fg: '#E7E9EC',
}

/** Soft radial falloff, used for the pool of light under each scene. */
export function radialTexture(inner = 'rgba(255,255,255,1)', mid = 'rgba(255,255,255,0.22)'): THREE.Texture {
  const c = document.createElement('canvas')
  c.width = c.height = 128
  const g = c.getContext('2d')!
  const grd = g.createRadialGradient(64, 64, 0, 64, 64, 64)
  grd.addColorStop(0, inner)
  grd.addColorStop(0.45, mid)
  grd.addColorStop(1, 'rgba(255,255,255,0)')
  g.fillStyle = grd
  g.fillRect(0, 0, 128, 128)
  const t = new THREE.CanvasTexture(c)
  t.needsUpdate = true
  return t
}

const reducedMotion = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

export interface StageProps {
  children: ReactNode
  camera?: [number, number, number]
  target?: [number, number, number]
  fov?: number
  /** slow auto-rotation until the viewer taps to pause */
  spin?: boolean
  /** keep the frame loop running (scene animates on its own) */
  animating?: boolean
  /** only capture the scroll wheel after the viewer has pressed the scene (for scenes embedded in a scrolling page) */
  focusZoom?: boolean
  /** replaces the default tap action (pause / resume rotation) */
  onTap?: () => void
  minDistance?: number
  maxDistance?: number
  maxPolar?: number
  className?: string
  /** DOM overlay drawn above the canvas */
  overlay?: ReactNode
  controlsClass?: string
}

export function Stage({
  children,
  camera = [0, 5.2, 8.2],
  target = [0, 0, 0],
  fov = 38,
  spin = true,
  animating = false,
  focusZoom = false,
  onTap,
  minDistance = 2.5,
  maxDistance = 22,
  maxPolar = Math.PI / 2.02,
  className,
  overlay,
  controlsClass = 'right-3 top-3',
}: StageProps) {
  const wrap = useRef<HTMLDivElement>(null)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const controls = useRef<any>(null)
  const down = useRef<{ x: number; y: number; t: number } | null>(null)
  const [spinning, setSpinning] = useState(spin && !reducedMotion())
  const [active, setActive] = useState(false)
  const [touched, setTouched] = useState(false)
  const [visible, setVisible] = useState(true)
  const [tabVisible, setTabVisible] = useState(typeof document === 'undefined' || document.visibilityState === 'visible')

  useEffect(() => {
    const el = wrap.current
    if (!el) return
    const io = new IntersectionObserver(([e]) => setVisible(e.isIntersecting), { threshold: 0.01 })
    io.observe(el)
    const onVis = () => setTabVisible(document.visibilityState === 'visible')
    document.addEventListener('visibilitychange', onVis)
    return () => {
      io.disconnect()
      document.removeEventListener('visibilitychange', onVis)
    }
  }, [])

  const loop = visible && tabVisible && (spinning || animating)

  return (
    <div ref={wrap} className={cx('absolute inset-0 select-none overflow-hidden', className)} onPointerLeave={() => setActive(false)}>
      <div
        className="absolute inset-0 cursor-grab active:cursor-grabbing"
        data-stage-canvas
        onPointerDown={(e) => {
          down.current = { x: e.clientX, y: e.clientY, t: performance.now() }
          setActive(true)
          setTouched(true)
        }}
        onPointerUp={(e) => {
          const d = down.current
          down.current = null
          if (!d || Math.hypot(e.clientX - d.x, e.clientY - d.y) > 6 || performance.now() - d.t > 400) return
          if (onTap) onTap()
          else setSpinning((s) => !s)
        }}
      >
        <Canvas
          frameloop={loop ? 'always' : 'demand'}
          dpr={[1, 2]}
          gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
          camera={{ position: camera, fov, near: 0.1, far: 200 }}
        >
          <fog attach="fog" args={[C.bg, maxDistance * 0.7, maxDistance * 2.2]} />
          {children}
          <OrbitControls
            ref={controls}
            makeDefault
            target={target}
            enableDamping
            dampingFactor={0.08}
            rotateSpeed={0.7}
            zoomSpeed={0.8}
            enableZoom={!focusZoom || active}
            enablePan
            autoRotate={spinning}
            autoRotateSpeed={0.45}
            minDistance={minDistance}
            maxDistance={maxDistance}
            maxPolarAngle={maxPolar}
            touches={{ ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN }}
          />
        </Canvas>
      </div>
      {/* depth: vignette above the canvas, below the UI */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_50%_42%,transparent_45%,rgba(11,13,16,0.55)_100%)]" />
      <div className={cx('absolute flex items-center gap-1', controlsClass)}>
        {spin && !onTap && (
          <button
            type="button"
            onClick={() => setSpinning((s) => !s)}
            aria-label={spinning ? 'Pause rotation' : 'Resume rotation'}
            title={spinning ? 'Pause rotation' : 'Resume rotation'}
            className="flex h-7 w-7 items-center justify-center rounded-md border border-white/10 bg-ink-800/80 text-fg-muted backdrop-blur transition-colors hover:border-white/20 hover:text-fg"
          >
            {spinning ? (
              <svg viewBox="0 0 16 16" className="h-3 w-3" fill="currentColor" aria-hidden><rect x="3.5" y="3" width="3" height="10" rx="0.8" /><rect x="9.5" y="3" width="3" height="10" rx="0.8" /></svg>
            ) : (
              <svg viewBox="0 0 16 16" className="h-3 w-3" fill="currentColor" aria-hidden><path d="M4.5 2.8v10.4a.6.6 0 0 0 .9.5l8.3-5.2a.6.6 0 0 0 0-1L5.4 2.3a.6.6 0 0 0-.9.5z" /></svg>
            )}
          </button>
        )}
        <button
          type="button"
          onClick={() => controls.current?.reset()}
          aria-label="Reset view"
          title="Reset view"
          className="flex h-7 w-7 items-center justify-center rounded-md border border-white/10 bg-ink-800/80 text-fg-muted backdrop-blur transition-colors hover:border-white/20 hover:text-fg"
        >
          <svg viewBox="0 0 16 16" className="h-3 w-3" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M2.5 8a5.5 5.5 0 1 0 1.7-4" /><path d="M2.5 2.5v3h3" /></svg>
        </button>
      </div>
      <div
        className={cx(
          'pointer-events-none absolute left-3 top-3 rounded-md border border-white/[0.08] bg-ink-800/70 px-2 py-1 text-[11px] text-fg-muted backdrop-blur transition-opacity duration-300',
          touched ? 'opacity-0' : 'opacity-100',
        )}
      >
        Drag to rotate · {focusZoom ? 'click, then scroll to zoom' : 'scroll or pinch to zoom'}
      </div>
      {overlay}
    </div>
  )
}
