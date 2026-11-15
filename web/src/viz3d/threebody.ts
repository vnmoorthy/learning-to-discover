// Planar Newtonian three-body integrator (G = 1, m1 = m2 = 1). Classical RK4 with a step that shrinks near close
// encounters, sampled on a uniform time grid. This is a browser re-integration for display: the official numbers on
// the page come from the float64 Dormand-Prince verifier, not from here.
export interface Orbit {
  vx: number
  vy: number
  T: number
  m3?: number
}
export interface Trajectory {
  /** samples x 6: x1,y1,x2,y2,x3,y3 */
  pos: Float32Array
  samples: number
  T: number
  /** |state(T) - state(0)|, how well this re-integration closes */
  closure: number
  /** half-extent of the motion, for framing */
  extent: number
}

type S = Float64Array // x1,y1,x2,y2,x3,y3, vx1,vy1,vx2,vy2,vx3,vy3

function deriv(s: S, m: number[], out: S): number {
  let rmin = Infinity
  for (let i = 0; i < 6; i++) out[i] = s[6 + i]
  for (let i = 6; i < 12; i++) out[i] = 0
  for (let a = 0; a < 3; a++)
    for (let b = a + 1; b < 3; b++) {
      const dx = s[2 * b] - s[2 * a]
      const dy = s[2 * b + 1] - s[2 * a + 1]
      const r2 = dx * dx + dy * dy
      const r = Math.sqrt(r2)
      if (r < rmin) rmin = r
      const k = 1 / (r2 * r)
      out[6 + 2 * a] += m[b] * dx * k
      out[7 + 2 * a] += m[b] * dy * k
      out[6 + 2 * b] -= m[a] * dx * k
      out[7 + 2 * b] -= m[a] * dy * k
    }
  return rmin
}

export function integrate(o: Orbit, samples = 2400): Trajectory {
  const m3 = o.m3 ?? 1
  const m = [1, 1, m3]
  const s = new Float64Array([-1, 0, 1, 0, 0, 0, o.vx, o.vy, o.vx, o.vy, (-2 * o.vx) / m3, (-2 * o.vy) / m3])
  const s0 = Float64Array.from(s)
  const k1 = new Float64Array(12), k2 = new Float64Array(12), k3 = new Float64Array(12), k4 = new Float64Array(12), tmp = new Float64Array(12)
  const pos = new Float32Array((samples + 1) * 6)
  const dtOut = o.T / samples
  let extent = 1
  let steps = 0
  for (let i = 0; i <= samples; i++) {
    for (let j = 0; j < 6; j++) {
      pos[i * 6 + j] = s[j]
      const a = Math.abs(s[j])
      if (a > extent) extent = a
    }
    if (i === samples) break
    let left = dtOut
    while (left > 1e-14 && steps < 4e6) {
      const rmin = deriv(s, m, k1)
      const h = Math.min(left, 0.004 * Math.pow(Math.min(rmin, 1), 1.5) + 1e-7)
      for (let j = 0; j < 12; j++) tmp[j] = s[j] + 0.5 * h * k1[j]
      deriv(tmp, m, k2)
      for (let j = 0; j < 12; j++) tmp[j] = s[j] + 0.5 * h * k2[j]
      deriv(tmp, m, k3)
      for (let j = 0; j < 12; j++) tmp[j] = s[j] + h * k3[j]
      deriv(tmp, m, k4)
      for (let j = 0; j < 12; j++) s[j] += (h / 6) * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j])
      left -= h
      steps++
    }
  }
  let c = 0
  for (let j = 0; j < 12; j++) c += (s[j] - s0[j]) ** 2
  return { pos, samples, T: o.T, closure: Math.sqrt(c), extent }
}
