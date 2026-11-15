import type { Point, ViolatedLine } from '../types'

/** Clip the infinite line through p1,p2 to the box [0,n-1]^2. Returns the two endpoints, or null. */
export function clipLine(p1: Point, p2: Point, n: number): [Point, Point] | null {
  const [x1, y1] = p1
  const dx = p2[0] - x1
  const dy = p2[1] - y1
  if (dx === 0 && dy === 0) return null
  let t0 = -Infinity
  let t1 = Infinity
  const lo = 0
  const hi = n - 1
  const clip = (p: number, d: number) => {
    if (d === 0) return p >= lo && p <= hi
    let a = (lo - p) / d
    let b = (hi - p) / d
    if (a > b) [a, b] = [b, a]
    t0 = Math.max(t0, a)
    t1 = Math.min(t1, b)
    return t0 <= t1
  }
  if (!clip(x1, dx) || !clip(y1, dy)) return null
  return [
    [x1 + t0 * dx, y1 + t0 * dy],
    [x1 + t1 * dx, y1 + t1 * dy],
  ]
}

export function onLine(p: Point, a: Point, b: Point): boolean {
  return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) === 0
}

/** For each point, how many violated lines pass through it. */
export function conflictCounts(points: Point[], lines: ViolatedLine[]): number[] {
  const out = new Array(points.length).fill(0)
  for (const [a, b] of lines) {
    for (let i = 0; i < points.length; i++) if (onLine(points[i], a, b)) out[i]++
  }
  return out
}

/** Symmetry axes for a nothree symmetry class name like "mirror-149" / "rot180-150" / "diag-149". */
export function symmetryKind(sym: string | undefined | null): 'mirror' | 'rot180' | 'diag' | 'none' {
  const s = (sym || '').toLowerCase()
  if (s.startsWith('mirror')) return 'mirror'
  if (s.startsWith('rot')) return 'rot180'
  if (s.startsWith('diag')) return 'diag'
  return 'none'
}
