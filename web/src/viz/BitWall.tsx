import { useEffect, useMemo, useRef, useState } from 'react'
import type { CodeArtifact } from '../types'
import { prepCanvas, useWidth } from './useCanvas'

/** Wall of codewords: each row of cells is one 16-bit word, words are laid out in columns. */
export default function BitWall({ art, color = '#5B8CFF' }: { art: CodeArtifact; color?: string }) {
  const [wrap, width] = useWidth<HTMLDivElement>()
  const canvas = useRef<HTMLCanvasElement>(null)
  const [hover, setHover] = useState<number | null>(null)
  const words = art.words || []
  const L = words[0]?.length || 16
  const cellPx = width < 500 ? 4 : 5
  const wordW = L * cellPx + 6
  const perCol = Math.max(1, Math.floor(width / wordW))
  const rowsN = Math.ceil(words.length / perCol)
  const rowH = cellPx + 2
  const H = rowsN * rowH
  const ones = useMemo(() => words.reduce((a, w) => a + [...w].filter((c) => c === '1').length, 0), [words])

  useEffect(() => {
    const c = canvas.current
    if (!c || width <= 0) return
    const ctx = prepCanvas(c, width, Math.max(H, 1))
    if (!ctx) return
    ctx.clearRect(0, 0, width, H)
    words.forEach((w, k) => {
      const col = k % perCol
      const row = Math.floor(k / perCol)
      const x0 = col * wordW
      const y0 = row * rowH
      const hot = hover === k
      for (let b = 0; b < w.length; b++) {
        ctx.fillStyle = w[b] === '1' ? (hot ? '#FFFFFF' : color) : hot ? '#3A4252' : '#161B24'
        ctx.fillRect(x0 + b * cellPx, y0, cellPx - 1, cellPx)
      }
    })
  }, [words, width, H, perCol, wordW, rowH, cellPx, color, hover])

  const onMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = e.currentTarget.getBoundingClientRect()
    const col = Math.floor((e.clientX - r.left) / wordW)
    const row = Math.floor((e.clientY - r.top) / rowH)
    const k = row * perCol + col
    setHover(col < perCol && k >= 0 && k < words.length ? k : null)
  }

  return (
    <div>
      <div className="mb-3 flex flex-wrap gap-x-5 gap-y-1 font-mono text-[11.5px] text-fg-muted">
        <span>
          codewords <span style={{ color }}>{art.count ?? words.length}</span>
        </span>
        <span>
          length <span className="text-fg">{L}</span>
        </span>
        <span>
          density of 1s <span className="text-fg">{words.length ? ((ones / (words.length * L)) * 100).toFixed(1) : '--'}%</span>
        </span>
        <span className="min-w-[180px]">{hover != null ? <span className="text-fg">#{hover}: {words[hover]}</span> : <span className="text-fg-dim">hover a word</span>}</span>
      </div>
      <div ref={wrap} className="max-h-[520px] overflow-y-auto">
        <canvas ref={canvas} onMouseMove={onMove} onMouseLeave={() => setHover(null)} className="block cursor-crosshair" />
      </div>
    </div>
  )
}
