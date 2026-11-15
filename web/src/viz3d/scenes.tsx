// Real-time scenes built from the lab's real artifacts. Everything is instanced: one draw call per layer.
import { Line } from '@react-three/drei'
import type { ThreeEvent } from '@react-three/fiber'
import { useLayoutEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { clipLine, conflictCounts, onLine, symmetryKind } from '../lib/geometry'
import type { GridArtifact, SignMatrixArtifact } from '../types'
import { C, radialTexture } from './Stage'

const SIZE = 6

function Floor({ size = SIZE * 1.06, tint = C.cyan, glow = 0.16 }: { size?: number; tint?: string; glow?: number }) {
  const tex = useMemo(() => radialTexture(), [])
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.012, 0]}>
        <planeGeometry args={[size, size]} />
        <meshBasicMaterial color={C.floor} />
      </mesh>
      {/* pool of light: reads as a soft volumetric glow under the data */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.008, 0]}>
        <planeGeometry args={[size * 1.9, size * 1.9]} />
        <meshBasicMaterial map={tex} color={tint} transparent opacity={glow} depthWrite={false} blending={THREE.AdditiveBlending} />
      </mesh>
    </group>
  )
}

/** The 75 x 75 no-three-in-line model: chosen points as lit pillars, violated lines as thin beams. */
export function LatticeScene({ art, selected, onSelect }: { art: GridArtifact | null; selected?: number | null; onSelect?: (i: number | null) => void }) {
  const n = art?.n ?? 75
  const s = SIZE / n
  const pillars = useRef<THREE.InstancedMesh>(null)
  const caps = useRef<THREE.InstancedMesh>(null)

  const d = useMemo(() => {
    const h = (n - 1) / 2
    const W = (x: number, y: number, z = 0): [number, number, number] => [(x - h) * s, z, (y - h) * s]
    const lattice = new Float32Array(n * n * 3)
    let k = 0
    for (let x = 0; x < n; x++) for (let y = 0; y < n; y++) { lattice.set(W(x, y), k); k += 3 }
    const points = art?.points ?? []
    const vl = art?.violated_lines ?? []
    const conf = conflictCounts(points, vl)
    const beams: number[] = []
    for (const [p1, p2] of vl) {
      const seg = clipLine(p1, p2, n)
      if (seg) beams.push(...W(seg[0][0], seg[0][1], 0.012), ...W(seg[1][0], seg[1][1], 0.012))
    }
    const axis: number[] = []
    const sk = symmetryKind(art?.sym)
    if (sk === 'mirror') axis.push(...W(h, -1.5, 0.01), ...W(h, n + 0.5, 0.01))
    if (sk === 'diag') axis.push(...W(-1.5, -1.5, 0.01), ...W(n + 0.5, n + 0.5, 0.01))
    if (sk === 'rot180') axis.push(...W(h, h, -0.2), ...W(h, h, 1.5))
    return { W, points, vl, conf, lattice, beams: new Float32Array(beams), axis: new Float32Array(axis) }
  }, [art, n, s])

  const height = (c: number) => 0.1 + Math.min(c, 6) * 0.065

  useLayoutEffect(() => {
    const m = new THREE.Matrix4()
    const col = new THREE.Color()
    const clean = new THREE.Color(C.cyan)
    const bad = new THREE.Color(C.red)
    const hot = new THREE.Color(C.amber)
    d.points.forEach(([x, y], i) => {
      const hgt = height(d.conf[i])
      const [a, , c] = d.W(x, y)
      m.makeScale(1, hgt, 1).setPosition(a, hgt / 2, c)
      pillars.current?.setMatrixAt(i, m)
      col.copy(d.conf[i] >= 4 ? hot : d.conf[i] > 0 ? bad : clean)
      pillars.current?.setColorAt(i, (d.conf[i] >= 4 ? hot : clean).clone().multiplyScalar(d.conf[i] >= 4 ? 0.6 : 0.42))
      m.makeScale(1, 1, 1).setPosition(a, hgt + 0.012, c)
      caps.current?.setMatrixAt(i, m)
      caps.current?.setColorAt(i, d.conf[i] > 0 ? col.clone() : col.clone().lerp(new THREE.Color('#ffffff'), 0.6))
    })
    for (const ref of [pillars, caps]) {
      if (!ref.current) continue
      ref.current.instanceMatrix.needsUpdate = true
      if (ref.current.instanceColor) ref.current.instanceColor.needsUpdate = true
      ref.current.computeBoundingSphere()
    }
  }, [d])

  const sel = useMemo(() => {
    if (selected == null || !d.points[selected]) return null
    const p = d.points[selected]
    const lines: number[] = []
    for (const [a, b] of d.vl) {
      if (!onLine(p, a, b)) continue
      const seg = clipLine(a, b, n)
      if (seg) lines.push(...d.W(seg[0][0], seg[0][1], 0.02), ...d.W(seg[1][0], seg[1][1], 0.02))
    }
    const hgt = height(d.conf[selected])
    return { pos: d.W(p[0], p[1], hgt + 0.02), lines: new Float32Array(lines) }
  }, [selected, d, n])

  const count = d.points.length
  const pick = (e: ThreeEvent<MouseEvent>) => {
    if (!onSelect || e.instanceId == null) return
    e.stopPropagation()
    onSelect(e.instanceId === selected ? null : e.instanceId)
  }

  return (
    <group>
      <Floor />
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" count={d.lattice.length / 3} array={d.lattice} itemSize={3} />
        </bufferGeometry>
        <pointsMaterial size={0.02} color={C.dot} transparent opacity={0.5} sizeAttenuation depthWrite={false} />
      </points>
      {d.beams.length > 0 && (
        <lineSegments key={'b' + d.beams.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={d.beams.length / 3} array={d.beams} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color={C.red} transparent opacity={sel ? 0.04 : 0.1} depthWrite={false} blending={THREE.AdditiveBlending} />
        </lineSegments>
      )}
      {d.axis.length > 0 && (
        <lineSegments key={'a' + d.axis.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={d.axis.length / 3} array={d.axis} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color={C.fg} transparent opacity={0.28} />
        </lineSegments>
      )}
      {count > 0 && (
        <group key={'p' + count}>
          <instancedMesh ref={pillars} args={[undefined, undefined, count]} onClick={pick}>
            <boxGeometry args={[s * 0.46, 1, s * 0.46]} />
            <meshBasicMaterial toneMapped={false} />
          </instancedMesh>
          <instancedMesh ref={caps} args={[undefined, undefined, count]} onClick={pick}>
            <boxGeometry args={[s * 0.66, 0.018, s * 0.66]} />
            <meshBasicMaterial toneMapped={false} />
          </instancedMesh>
        </group>
      )}
      {sel && (
        <group>
          {sel.lines.length > 0 && (
            <lineSegments key={'s' + selected + sel.lines.length}>
              <bufferGeometry>
                <bufferAttribute attach="attributes-position" count={sel.lines.length / 3} array={sel.lines} itemSize={3} />
              </bufferGeometry>
              <lineBasicMaterial color={C.red} transparent opacity={0.95} />
            </lineSegments>
          )}
          <mesh position={sel.pos} rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[s * 0.9, s * 1.25, 32]} />
            <meshBasicMaterial color={C.fg} side={THREE.DoubleSide} toneMapped={false} />
          </mesh>
        </group>
      )}
    </group>
  )
}

/** The 51 x 51 sign matrix as a city: +1 entries are towers, -1 entries low plinths. */
export function CityScene({ art, selected, onSelect }: { art: SignMatrixArtifact | null; selected?: number | null; onSelect?: (i: number | null) => void }) {
  const M = art?.matrix ?? []
  const n = M.length
  const mesh = useRef<THREE.InstancedMesh>(null)
  const cell = n ? SIZE / n : 1

  const heights = useMemo(() => {
    const out = new Float32Array(n * n)
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++) {
        if (M[r][c] <= 0) { out[r * n + c] = 0.035; continue }
        let sum = 0, cnt = 0
        for (let dr = -2; dr <= 2; dr++)
          for (let dc = -2; dc <= 2; dc++) {
            const v = M[r + dr]?.[c + dc]
            if (v !== undefined) { sum += v; cnt++ }
          }
        out[r * n + c] = 0.16 + 0.85 * ((sum / cnt + 1) / 2)
      }
    return out
  }, [M, n])

  useLayoutEffect(() => {
    if (!mesh.current || !n) return
    const m = new THREE.Matrix4()
    const lo = new THREE.Color('#22525C')
    const hi = new THREE.Color('#8FE4EE')
    const plinth = new THREE.Color('#6E5A33')
    const col = new THREE.Color()
    const h = (n - 1) / 2
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++) {
        const i = r * n + c
        const hg = heights[i]
        m.makeScale(1, hg, 1).setPosition((c - h) * cell, hg / 2, (r - h) * cell)
        mesh.current.setMatrixAt(i, m)
        if (M[r][c] > 0) col.copy(lo).lerp(hi, Math.min(1, (hg - 0.16) / 0.85))
        else col.copy(plinth)
        mesh.current.setColorAt(i, col)
      }
    mesh.current.instanceMatrix.needsUpdate = true
    if (mesh.current.instanceColor) mesh.current.instanceColor.needsUpdate = true
    mesh.current.computeBoundingSphere()
  }, [M, n, cell, heights])

  const selPos = useMemo(() => {
    if (selected == null || !n) return null
    const r = Math.floor(selected / n), c = selected % n, h = (n - 1) / 2
    return [(c - h) * cell, heights[selected] + 0.02, (r - h) * cell] as [number, number, number]
  }, [selected, n, cell, heights])

  if (!n) return <Floor />
  return (
    <group>
      <ambientLight intensity={0.55} />
      <hemisphereLight args={['#BFE9F0', '#0B0D10', 0.9]} />
      <directionalLight position={[5, 9, 4]} intensity={2.2} />
      <directionalLight position={[-6, 4, -5]} intensity={0.5} color="#E2B25C" />
      <Floor glow={0.1} />
      <instancedMesh
        key={n}
        ref={mesh}
        args={[undefined, undefined, n * n]}
        onClick={(e) => {
          if (!onSelect || e.instanceId == null) return
          e.stopPropagation()
          onSelect(e.instanceId === selected ? null : e.instanceId)
        }}
      >
        <boxGeometry args={[cell * 0.84, 1, cell * 0.84]} />
        <meshStandardMaterial roughness={0.45} metalness={0.25} />
      </instancedMesh>
      {selPos && (
        <mesh position={selPos} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[cell * 0.7, cell * 0.95, 4, 1, Math.PI / 4]} />
          <meshBasicMaterial color={C.fg} side={THREE.DoubleSide} toneMapped={false} />
        </mesh>
      )}
    </group>
  )
}

export interface SnakeData {
  holder: string
  edges: number
  dimension: number
  path: number[][]
  dust: number[][]
}

/** kgrey's 2950-edge snake, linearly projected from the 13-cube to 3D. Colour runs amber (start) to cyan (end). */
export function SnakeScene({ data, upTo }: { data: SnakeData; upTo?: number }) {
  const d = useMemo(() => {
    const box = new THREE.Box3()
    const v = new THREE.Vector3()
    for (const p of data.path) box.expandByPoint(v.set(p[0], p[1], p[2]))
    const c = box.getCenter(new THREE.Vector3())
    const a = new THREE.Color(C.amber)
    const b = new THREE.Color(C.cyan)
    const pts: [number, number, number][] = data.path.map((p) => [p[0] - c.x, p[2] - c.z, p[1] - c.y])
    const cols: [number, number, number][] = data.path.map((_, i) => {
      const t = a.clone().lerp(b, i / (data.path.length - 1))
      return [t.r, t.g, t.b]
    })
    const dust = new Float32Array(data.dust.length * 3)
    data.dust.forEach((p, i) => dust.set([p[0] - c.x, p[2] - c.z, p[1] - c.y], i * 3))
    return { pts, cols, dust }
  }, [data])
  const k = Math.max(2, Math.min(d.pts.length, upTo ?? d.pts.length))
  const head = d.pts[k - 1]
  return (
    <group>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" count={d.dust.length / 3} array={d.dust} itemSize={3} />
        </bufferGeometry>
        <pointsMaterial size={0.035} color={C.dot} transparent opacity={0.4} sizeAttenuation depthWrite={false} />
      </points>
      <Line points={k === d.pts.length ? d.pts : d.pts.slice(0, k)} vertexColors={k === d.pts.length ? d.cols : d.cols.slice(0, k)} lineWidth={1.6} transparent opacity={0.95} toneMapped={false} />
      <mesh position={d.pts[0]}>
        <sphereGeometry args={[0.07, 16, 16]} />
        <meshBasicMaterial color={C.amber} toneMapped={false} />
      </mesh>
      <mesh position={head}>
        <sphereGeometry args={[0.07, 16, 16]} />
        <meshBasicMaterial color={C.ice} toneMapped={false} />
      </mesh>
    </group>
  )
}
