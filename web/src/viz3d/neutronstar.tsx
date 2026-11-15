// Interactive neutron-star cutaway from a real STARFORGE solution: the SLy equation of state integrated through the
// TOV equations (problems/neutron-star-eos). A wedge is cut out so the interior shows: colour = baryon density
// n(r)/n_sat along the solved profile, contours at 0.5, 1, 2 and 4 n_sat. Drag to orbit, scroll or pinch to zoom.
import { useEffect, useMemo, useState } from 'react'
import * as THREE from 'three'
import { ErrorBoundary } from '../components/ErrorBoundary'
import { cx } from '../lib/format'
import data from './neutronstar.json'
import { Stage } from './Stage'

type Star = { R_km: number; M_msun: number; pc_MeVfm3: number; r: number[]; n_over_nsat: number[] }
const STARS = (data as { stars: Record<string, Star> }).stars
const R_UNIT = 12 // km per scene unit
const N = 72

const COMMON = /* glsl */ `
uniform float uN[${N}];
uniform float uMaxN;
vec3 ramp(float t) {               // dark red -> orange -> yellow -> white-blue (hot, dense)
  vec3 a = vec3(0.10, 0.02, 0.04), b = vec3(0.75, 0.18, 0.08), c = vec3(0.98, 0.62, 0.18), d = vec3(1.0, 0.95, 0.75), e = vec3(0.70, 0.88, 1.0);
  t = clamp(t, 0.0, 1.0);
  if (t < 0.25) return mix(a, b, t / 0.25);
  if (t < 0.5) return mix(b, c, (t - 0.25) / 0.25);
  if (t < 0.8) return mix(c, d, (t - 0.5) / 0.3);
  return mix(d, e, (t - 0.8) / 0.2);
}
float density(float x) {           // x = r / R in [0, 1]
  float f = clamp(x, 0.0, 1.0) * float(${N - 1});
  int i = int(floor(f));
  int j = min(i + 1, ${N - 1});
  float a = 0.0, b = 0.0;
  for (int k = 0; k < ${N}; k++) { if (k == i) a = uN[k]; if (k == j) b = uN[k]; }
  return mix(a, b, fract(f));
}
vec3 shade(float x) {
  float n = max(density(x), 1e-3);
  float t = log(n / 0.01) / log(uMaxN / 0.01);
  vec3 col = ramp(t);
  float l = log2(n);                              // contours at 0.5, 1, 2, 4 n_sat
  float w = fwidth(l) * 1.2;
  float c = 1.0 - smoothstep(0.0, w, abs(fract(l + 0.5) - 0.5));
  if (n > 0.4 && n < 5.0) col = mix(col, vec3(0.31, 0.82, 0.88), c * 0.85);
  return col;
}
`

const DISK_VERT = /* glsl */ `
varying vec2 vP;
void main() { vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`
const DISK_FRAG = /* glsl */ `
${COMMON}
varying vec2 vP;
void main() { gl_FragColor = vec4(pow(shade(length(vP)), vec3(1.0 / 2.2)), 1.0); }
`
const SHELL_VERT = /* glsl */ `
varying vec3 vL; varying vec3 vN; varying vec3 vV;
void main() {
  vL = position;
  vec4 w = modelMatrix * vec4(position, 1.0);
  vN = normalize(mat3(modelMatrix) * normal);
  vV = normalize(cameraPosition - w.xyz);
  gl_Position = projectionMatrix * viewMatrix * w;
}
`
const SHELL_FRAG = /* glsl */ `
varying vec3 vL; varying vec3 vN; varying vec3 vV;
void main() {
  if (vL.x > 0.0 && vL.z > 0.0) discard;          // the cut-away wedge
  float fr = pow(1.0 - max(dot(vN, vV), 0.0), 2.5);
  vec3 base = vec3(0.55, 0.62, 0.72) * (0.35 + 0.65 * max(dot(vN, normalize(vec3(0.4, 0.8, 0.6))), 0.0));
  vec3 col = base + vec3(0.45, 0.75, 1.0) * fr * 0.9;
  gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
}
`

function StarMesh({ star }: { star: Star }) {
  const s = star.R_km / R_UNIT
  const uniforms = useMemo(() => ({ uN: { value: star.n_over_nsat.slice(0, N) }, uMaxN: { value: 8 } }), [star])
  const mk = (frag: string, vert: string) => new THREE.ShaderMaterial({ vertexShader: vert, fragmentShader: frag, uniforms, side: THREE.DoubleSide })
  const mats = useMemo(() => ({ disk: mk(DISK_FRAG, DISK_VERT), shell: mk(SHELL_FRAG, SHELL_VERT) }), [uniforms]) // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => { mats.disk.dispose(); mats.shell.dispose() }, [mats])
  return (
    <group scale={[s, s, s]}>
      <mesh material={mats.shell}>
        <sphereGeometry args={[1, 96, 64]} />
      </mesh>
      {/* the two cut faces: x = 0 (z > 0) and z = 0 (x > 0), as half disks */}
      <mesh material={mats.disk} rotation={[0, -Math.PI / 2, 0]}>
        <circleGeometry args={[1, 128, -Math.PI / 2, Math.PI]} />
      </mesh>
      <mesh material={mats.disk}>
        <circleGeometry args={[1, 128, -Math.PI / 2, Math.PI]} />
      </mesh>
    </group>
  )
}

export function NeutronStarViewer({ fallback }: { fallback?: React.ReactNode }) {
  const [which, setWhich] = useState<'m14' | 'mmax'>('m14')
  const star = STARS[which]
  const still = fallback ?? <div className="absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim">3D view unavailable (WebGL disabled)</div>
  return (
    <ErrorBoundary fallback={still}>
      <Stage
        camera={[2.4, 1.3, 2.4]}
        target={[0, 0, 0]}
        fov={36}
        focusZoom
        minDistance={1.3}
        maxDistance={8}
        maxPolar={Math.PI - 0.02}
        autoRotateSpeed={0.6}
        overlay={
          <>
            <div className="absolute bottom-3 left-3 flex flex-wrap items-center gap-1.5">
              {(['m14', 'mmax'] as const).map((k) => (
                <button
                  key={k}
                  type="button"
                  aria-pressed={which === k}
                  onClick={() => setWhich(k)}
                  className={cx(
                    'h-7 whitespace-nowrap rounded-md border px-2.5 text-[11.5px] font-medium backdrop-blur transition-colors',
                    which === k ? 'border-cyan/40 bg-cyan/[0.12] text-fg' : 'border-white/10 bg-ink-800/80 text-fg-muted hover:border-white/20 hover:text-fg',
                  )}
                >
                  {k === 'm14' ? '1.40 M☉ star' : 'Maximum mass 2.05 M☉'}
                </button>
              ))}
            </div>
            <div className="pointer-events-none absolute right-3 bottom-3 rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur">
              SLy · M = {star.M_msun.toFixed(2)} M☉ · R = {star.R_km.toFixed(2)} km · centre {star.n_over_nsat[0].toFixed(1)} n_sat
            </div>
            <div className="pointer-events-none absolute right-3 top-12 w-40 rounded-md border border-white/[0.08] bg-ink-800/85 p-2 text-[10.5px] text-fg-muted backdrop-blur">
              <div className="mb-1">baryon density n / n_sat</div>
              <div className="h-2 rounded" style={{ background: 'linear-gradient(90deg,#1a0510,#bf2e14,#fa9e2e,#fff2bf,#b3e0ff)' }} />
              <div className="mt-0.5 flex justify-between font-mono"><span>0.01</span><span>8</span></div>
              <div className="mt-1 text-fg-dim">cyan rings: 0.5, 1, 2, 4 n_sat</div>
            </div>
          </>
        }
      >
        <StarMesh star={star} />
      </Stage>
    </ErrorBoundary>
  )
}
