import { useEffect, useMemo, useRef, useState } from 'react'
import { clipLine, conflictCounts, onLine, symmetryKind } from '../lib/geometry'
import type { GridArtifact, Point } from '../types'
import { prepCanvas, useWidth } from './useCanvas'

export default function NoThreeCanvas({ art }: { art: GridArtifact }) {
  const [wrap, width] = useWidth<HTMLDivElement>()
  const canvas = useRef<HTMLCanvasElement>(null)
  const [hover, setHover] = useState<Point | null>(null)
  const [showLines, setShowLines] = useState(true)
  const [showAxis, setShowAxis] = useState(true)
  const n = art.n || 75
  const size = Math.min(width, 760)
  const pad = 14
  const cell = size > 0 ? (size - pad * 2) / (n - 1) : 0

  const conf = useMemo(() => conflictCounts(art.points, art.violated_lines), [art])
  const pointSet = useMemo(() => new Set(art.points.map(([x, y]) => `${x},${y}`)), [art])
  const clipped = useMemo(() => art.violated_lines.map(([a, b, m]) => ({ a, b, m, seg: clipLine(a, b, n) })), [art, n])
  const sk = symmetryKind(art.sym)
  const hoverPoint = hover && pointSet.has(`${hover[0]},${hover[1]}`) ? hover : null
  const hoverLines = useMemo(() => (hoverPoint ? clipped.filter((l) => onLine(hoverPoint, l.a, l.b)) : []), [hoverPoint, clipped])

  useEffect(() => {
    const c = canvas.current
    if (!c || size <= 0) return
    const ctx = prepCanvas(c, size, size)
    if (!ctx) return
    // canvas y grows downward; draw y=0 at the bottom like a math plot
    const X = (x: number) => pad + x * cell
    const Y = (y: number) => size - pad - y * cell
    ctx.clearRect(0, 0, size, size)
    ctx.fillStyle = '#080A0E'
    ctx.fillRect(0, 0, size, size)

    // lattice
    ctx.fillStyle = 'rgba(140,150,170,0.22)'
    const r0 = Math.max(0.6, cell * 0.09)
    for (let x = 0; x < n; x++) for (let y = 0; y < n; y++) ctx.fillRect(X(x) - r0 / 2, Y(y) - r0 / 2, r0, r0)

    // symmetry axis
    if (showAxis) {
      ctx.save()
      ctx.strokeStyle = 'rgba(255,181,71,0.75)'
      ctx.setLineDash([6, 5])
      ctx.lineWidth = 1.2
      ctx.beginPath()
      const m = (n - 1) / 2
      if (sk === 'mirror') {
        ctx.moveTo(X(m), Y(-0.5))
        ctx.lineTo(X(m), Y(n - 0.5))
      } else if (sk === 'diag') {
        ctx.moveTo(X(-0.3), Y(-0.3))
        ctx.lineTo(X(n - 0.7), Y(n - 0.7))
      }
      ctx.stroke()
      if (sk === 'rot180') {
        ctx.setLineDash([])
        ctx.beginPath()
        ctx.arc(X(m), Y(m), 7, 0, Math.PI * 2)
        ctx.moveTo(X(m) - 11, Y(m))
        ctx.lineTo(X(m) + 11, Y(m))
        ctx.moveTo(X(m), Y(m) - 11)
        ctx.lineTo(X(m), Y(m) + 11)
        ctx.stroke()
      }
      ctx.restore()
    }

    // violated lines across the grid
    if (showLines) {
      ctx.save()
      ctx.globalCompositeOperation = 'lighter'
      ctx.lineWidth = 1
      for (const l of clipped) {
        if (!l.seg) continue
        const alpha = Math.min(0.55, 0.16 + (l.m - 3) * 0.12)
        ctx.strokeStyle = `rgba(255,77,94,${hoverPoint ? alpha * 0.35 : alpha})`
        ctx.beginPath()
        ctx.moveTo(X(l.seg[0][0]), Y(l.seg[0][1]))
        ctx.lineTo(X(l.seg[1][0]), Y(l.seg[1][1]))
        ctx.stroke()
      }
      ctx.restore()
    }
    if (hoverLines.length) {
      ctx.save()
      ctx.strokeStyle = 'rgba(255,90,110,0.95)'
      ctx.lineWidth = 1.8
      ctx.shadowColor = '#FF4D5E'
      ctx.shadowBlur = 8
      for (const l of hoverLines) {
        if (!l.seg) continue
        ctx.beginPath()
        ctx.moveTo(X(l.seg[0][0]), Y(l.seg[0][1]))
        ctx.lineTo(X(l.seg[1][0]), Y(l.seg[1][1]))
        ctx.stroke()
      }
      ctx.restore()
    }

    // points with glow
    const pr = Math.max(1.8, cell * 0.36)
    ctx.save()
    ctx.globalCompositeOperation = 'lighter'
    art.points.forEach(([x, y], i) => {
      const bad = conf[i] > 0
      const g = ctx.createRadialGradient(X(x), Y(y), 0, X(x), Y(y), pr * 3.2)
      g.addColorStop(0, bad ? 'rgba(255,120,130,0.55)' : 'rgba(61,245,255,0.55)')
      g.addColorStop(1, 'rgba(0,0,0,0)')
      ctx.fillStyle = g
      ctx.beginPath()
      ctx.arc(X(x), Y(y), pr * 3.2, 0, Math.PI * 2)
      ctx.fill()
    })
    ctx.restore()
    art.points.forEach(([x, y], i) => {
      ctx.fillStyle = conf[i] > 0 ? '#FFB3BA' : '#C8FCFF'
      ctx.beginPath()
      ctx.arc(X(x), Y(y), pr, 0, Math.PI * 2)
      ctx.fill()
    })
    if (hoverPoint) {
      ctx.strokeStyle = '#FFFFFF'
      ctx.lineWidth = 1.5
      ctx.beginPath()
      ctx.arc(X(hoverPoint[0]), Y(hoverPoint[1]), pr + 3, 0, Math.PI * 2)
      ctx.stroke()
    }
  }, [art, size, cell, n, conf, clipped, sk, showLines, showAxis, hoverPoint, hoverLines])

  const onMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = e.currentTarget.getBoundingClientRect()
    const x = Math.round((e.clientX - r.left - pad) / cell)
    const y = Math.round((size - (e.clientY - r.top) - pad) / cell)
    if (x < 0 || y < 0 || x >= n || y >= n) setHover(null)
    else if (!hover || hover[0] !== x || hover[1] !== y) setHover([x, y])
  }

  const badPoints = conf.filter((c) => c > 0).length
  const hoverConf = hoverPoint ? conf[art.points.findIndex(([x, y]) => x === hoverPoint[0] && y === hoverPoint[1])] : 0

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-x-5 gap-y-2 font-mono text-[11.5px] text-fg-muted">
        <span>
          points <span className="text-cyan">{art.count ?? art.points.length}</span>
        </span>
        <span>
          violated lines <span className="text-bad">{art.violated_lines.length}</span>
        </span>
        <span>
          conflicted points <span className="text-fg">{badPoints}</span>
        </span>
        <span>
          symmetry <span className="text-amber">{art.sym}</span>
        </span>
        <span>
          SAT round <span className="text-fg">{art.round}</span>
        </span>
        <span className="ml-auto flex gap-3">
          <label className="flex cursor-pointer items-center gap-1.5">
            <input type="checkbox" checked={showLines} onChange={(e) => setShowLines(e.target.checked)} className="accent-[#FF4D5E]" /> lines
          </label>
          <label className="flex cursor-pointer items-center gap-1.5">
            <input type="checkbox" checked={showAxis} onChange={(e) => setShowAxis(e.target.checked)} className="accent-[#FFB547]" /> axis
          </label>
        </span>
      </div>
      <div ref={wrap} className="relative w-full">
        <canvas ref={canvas} onMouseMove={onMove} onMouseLeave={() => setHover(null)} className="mx-auto block cursor-crosshair rounded-xl border border-white/[0.06]" />
        {hover && (
          <div className="pointer-events-none absolute left-3 top-3 rounded-lg border border-white/10 bg-ink-900/90 px-2.5 py-1.5 font-mono text-[11px] text-fg backdrop-blur">
            ({hover[0]}, {hover[1]}) {hoverPoint ? (hoverConf > 0 ? <span className="text-bad">on {hoverConf} violated line(s)</span> : <span className="text-cyan">clean point</span>) : <span className="text-fg-dim">empty</span>}
          </div>
        )}
      </div>
      <p className="mt-2 text-[11.5px] text-fg-dim">
        Current SAT model with the fewest violated lines. Red: lines through 3+ chosen points (extended across the grid; brighter = more points). Amber: symmetry {sk === 'rot180' ? 'centre (180 degree rotation)' : 'axis'}. Hover a point to isolate its lines.
      </p>
    </div>
  )
}
