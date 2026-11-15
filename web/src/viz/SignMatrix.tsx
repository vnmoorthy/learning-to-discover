import { useEffect, useMemo, useRef, useState } from 'react'
import { fmtInt, fmtPct } from '../lib/format'
import type { SignMatrixArtifact } from '../types'
import { prepCanvas, useWidth } from './useCanvas'

export default function SignMatrix({ art }: { art: SignMatrixArtifact }) {
  const [wrap, width] = useWidth<HTMLDivElement>()
  const canvas = useRef<HTMLCanvasElement>(null)
  const [hover, setHover] = useState<[number, number] | null>(null)
  const M = art.matrix || []
  const rows = M.length
  const cols = rows ? M[0].length : 0
  const size = Math.min(width, cols <= 24 ? 460 : 640)
  const cell = cols ? size / cols : 0
  const h = cell * rows

  const rowSums = useMemo(() => M.map((r) => r.reduce((a, b) => a + b, 0)), [M])
  const colSums = useMemo(() => (cols ? Array.from({ length: cols }, (_, j) => M.reduce((a, r) => a + r[j], 0)) : []), [M, cols])
  const plus = useMemo(() => M.reduce((a, r) => a + r.filter((v) => v === 1).length, 0), [M])

  useEffect(() => {
    const c = canvas.current
    if (!c || size <= 0 || !rows) return
    const ctx = prepCanvas(c, size, h)
    if (!ctx) return
    ctx.fillStyle = '#06070A'
    ctx.fillRect(0, 0, size, h)
    const gap = cell > 6 ? 1 : 0
    for (let i = 0; i < rows; i++)
      for (let j = 0; j < cols; j++) {
        const v = M[i][j]
        const inRow = hover && hover[0] === i
        const inCol = hover && hover[1] === j
        if (v === 1) ctx.fillStyle = inRow || inCol ? '#A6FBFF' : '#3DF5FF'
        else ctx.fillStyle = inRow || inCol ? '#2A3444' : '#121821'
        ctx.fillRect(j * cell + gap / 2, i * cell + gap / 2, cell - gap, cell - gap)
      }
    if (hover) {
      ctx.strokeStyle = '#FFB547'
      ctx.lineWidth = 1.5
      ctx.strokeRect(0.75, hover[0] * cell + 0.75, size - 1.5, cell - 1.5)
      ctx.strokeRect(hover[1] * cell + 0.75, 0.75, cell - 1.5, h - 1.5)
    }
  }, [M, rows, cols, size, cell, h, hover])

  const onMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = e.currentTarget.getBoundingClientRect()
    const j = Math.floor((e.clientX - r.left) / cell)
    const i = Math.floor((e.clientY - r.top) / cell)
    if (i < 0 || j < 0 || i >= rows || j >= cols) setHover(null)
    else if (!hover || hover[0] !== i || hover[1] !== j) setHover([i, j])
  }

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-x-5 gap-y-2 font-mono text-[11.5px] text-fg-muted">
        <span>
          order <span className="text-fg">{rows}x{cols}</span>
        </span>
        {art.D != null && (
          <span>
            target D <span className="text-amber">{art.D}</span>
          </span>
        )}
        {art.bad_vectors != null && (
          <span>
            bad vectors <span className={art.bad_vectors === 0 ? 'text-good' : 'text-bad'}>{fmtInt(art.bad_vectors)}</span>
            {art.total_vectors ? <span className="text-fg-dim"> / {fmtInt(art.total_vectors)} ({fmtPct(art.bad_vectors / art.total_vectors, 2)})</span> : null}
          </span>
        )}
        {art.log10_det != null && (
          <span>
            log10|det| <span className="text-cyan">{art.log10_det}</span>
          </span>
        )}
        <span>
          +1 entries <span className="text-cyan">{plus}</span> / {rows * cols}
        </span>
      </div>
      <div ref={wrap} className="relative">
        <canvas ref={canvas} onMouseMove={onMove} onMouseLeave={() => setHover(null)} className="block cursor-crosshair rounded-lg border border-white/[0.06]" />
        {hover && (
          <div className="pointer-events-none absolute right-2 top-2 rounded-lg border border-white/10 bg-ink-900/90 px-2.5 py-1.5 font-mono text-[11px] backdrop-blur">
            <div>
              A[{hover[0]}][{hover[1]}] = <span className={M[hover[0]][hover[1]] === 1 ? 'text-cyan' : 'text-fg-muted'}>{M[hover[0]][hover[1]] === 1 ? '+1' : '-1'}</span>
            </div>
            <div className="text-fg-dim">
              row sum {rowSums[hover[0]]} | col sum {colSums[hover[1]]}
            </div>
          </div>
        )}
      </div>
      <div className="mt-2 flex items-center gap-4 text-[11px] text-fg-dim">
        <span className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-sm bg-cyan" /> +1
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-sm border border-white/10 bg-[#121821]" /> -1
        </span>
        <span>Hover to inspect a row and column.</span>
      </div>
    </div>
  )
}
