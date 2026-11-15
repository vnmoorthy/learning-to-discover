// 3D hero: the current no-three-in-line model as a slowly rotating lattice.
// Cheap on CPU: three draw calls of points/lines, dpr capped, rendering stops when offscreen or tab hidden.
import { Canvas, useFrame } from '@react-three/fiber'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'
import { clipLine, conflictCounts, symmetryKind } from '../lib/geometry'
import type { GridArtifact } from '../types'

const SCALE = 6 / 75

function glowTexture(): THREE.Texture {
  const c = document.createElement('canvas')
  c.width = c.height = 64
  const g = c.getContext('2d')!
  const grd = g.createRadialGradient(32, 32, 0, 32, 32, 32)
  grd.addColorStop(0, 'rgba(255,255,255,1)')
  grd.addColorStop(0.18, 'rgba(255,255,255,0.9)')
  grd.addColorStop(0.42, 'rgba(255,255,255,0.25)')
  grd.addColorStop(1, 'rgba(255,255,255,0)')
  g.fillStyle = grd
  g.fillRect(0, 0, 64, 64)
  const t = new THREE.CanvasTexture(c)
  t.needsUpdate = true
  return t
}

function toWorld(x: number, y: number, n: number, z = 0): [number, number, number] {
  const h = (n - 1) / 2
  return [(x - h) * SCALE, z, (y - h) * SCALE]
}

function Lattice({ art }: { art: GridArtifact | null }) {
  const group = useRef<THREE.Group>(null)
  const n = art?.n ?? 75
  const tex = useMemo(() => glowTexture(), [])

  const { lattice, pts, ptsColor, lines, pins, axis } = useMemo(() => {
    const lattice = new Float32Array(n * n * 3)
    let k = 0
    for (let x = 0; x < n; x++)
      for (let y = 0; y < n; y++) {
        const [a, b, c] = toWorld(x, y, n)
        lattice[k++] = a
        lattice[k++] = b
        lattice[k++] = c
      }
    const points = art?.points ?? []
    const vl = art?.violated_lines ?? []
    const conf = conflictCounts(points, vl)
    const pts = new Float32Array(points.length * 3)
    const ptsColor = new Float32Array(points.length * 3)
    const pins: number[] = []
    const cyan = new THREE.Color('#3DF5FF')
    const red = new THREE.Color('#FF4D5E')
    points.forEach(([x, y], i) => {
      const h = 0.06 + Math.min(conf[i], 6) * 0.12
      const [a, b, c] = toWorld(x, y, n, h)
      pts.set([a, b, c], i * 3)
      const col = conf[i] > 0 ? red.clone().lerp(cyan, 0.15) : cyan
      ptsColor.set([col.r, col.g, col.b], i * 3)
      pins.push(...toWorld(x, y, n, 0), a, b, c)
    })
    const lines: number[] = []
    for (const [p1, p2] of vl) {
      const seg = clipLine(p1, p2, n)
      if (!seg) continue
      lines.push(...toWorld(seg[0][0], seg[0][1], n, 0.01), ...toWorld(seg[1][0], seg[1][1], n, 0.01))
    }
    const sk = symmetryKind(art?.sym)
    const axis: number[] = []
    const m = (n - 1) / 2
    if (sk === 'mirror') axis.push(...toWorld(m, -2, n, 0.02), ...toWorld(m, n + 1, n, 0.02))
    if (sk === 'diag') axis.push(...toWorld(-2, -2, n, 0.02), ...toWorld(n + 1, n + 1, n, 0.02))
    if (sk === 'rot180') axis.push(...toWorld(m, m, n, -0.6), ...toWorld(m, m, n, 1.4))
    return { lattice, pts, ptsColor, lines: new Float32Array(lines), pins: new Float32Array(pins), axis: new Float32Array(axis) }
  }, [art, n])

  useFrame((_, dt) => {
    if (group.current) group.current.rotation.y += Math.min(dt, 0.05) * 0.09
  })

  return (
    <group ref={group} rotation={[0, 0.6, 0]}>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" count={lattice.length / 3} array={lattice} itemSize={3} />
        </bufferGeometry>
        <pointsMaterial size={0.028} color="#4A5568" transparent opacity={0.55} sizeAttenuation depthWrite={false} />
      </points>
      {lines.length > 0 && (
        <lineSegments key={'l' + lines.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={lines.length / 3} array={lines} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color="#FF4D5E" transparent opacity={0.16} depthWrite={false} blending={THREE.AdditiveBlending} />
        </lineSegments>
      )}
      {pins.length > 0 && (
        <lineSegments key={'p' + pins.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={pins.length / 3} array={pins} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color="#3DF5FF" transparent opacity={0.28} depthWrite={false} />
        </lineSegments>
      )}
      {axis.length > 0 && (
        <lineSegments key={'a' + axis.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={axis.length / 3} array={axis} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color="#FFB547" transparent opacity={0.8} />
        </lineSegments>
      )}
      {pts.length > 0 && (
        <points key={'g' + pts.length}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={pts.length / 3} array={pts} itemSize={3} />
            <bufferAttribute attach="attributes-color" count={ptsColor.length / 3} array={ptsColor} itemSize={3} />
          </bufferGeometry>
          <pointsMaterial size={0.34} map={tex} vertexColors transparent depthWrite={false} blending={THREE.AdditiveBlending} sizeAttenuation />
        </points>
      )}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.005, 0]}>
        <planeGeometry args={[6.3, 6.3]} />
        <meshBasicMaterial color="#0B1018" transparent opacity={0.55} />
      </mesh>
    </group>
  )
}

export default function LatticeHero({ art }: { art: GridArtifact | null }) {
  const wrap = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(true)
  const [tabVisible, setTabVisible] = useState(document.visibilityState === 'visible')

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

  const reduced = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

  return (
    <div ref={wrap} className="absolute inset-0">
      <Canvas
        frameloop={visible && tabVisible && !reduced ? 'always' : 'demand'}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true, powerPreference: 'low-power' }}
        camera={{ position: [0, 5.6, 8.3], fov: 40, near: 0.1, far: 100 }}
        onCreated={({ camera }) => camera.lookAt(0, -0.6, 0)}
      >
        <fog attach="fog" args={['#07080B', 8.5, 15]} />
        <Lattice art={art} />
      </Canvas>
    </div>
  )
}
