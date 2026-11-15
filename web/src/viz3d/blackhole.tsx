// Interactive black hole: a Schwarzschild ray tracer running live in a WebGL fragment shader.
//
// Same physics as viz/blackhole/raytrace.py (the 24M-ray A100 render), one light ray per pixel, every frame:
//   units r_s = 2M = 1; each ray is traced backwards from the camera with the photon-orbit equation in Cartesian form,
//   x'' = -(3/2) h^2 x / r^5 (h = |x cross v| conserved), i.e. the Binet equation u'' + u = 3 M u^2 of Schwarzschild null
//   geodesics, integrated with RK4 and a step that shrinks as r^2 near the hole.
//   Thin opaque Keplerian disk from the ISCO (r = 3) outward, temperature T ~ r^-3/4 (1 - sqrt(r_in/r))^1/4,
//   observed temperature scaled by g = sqrt(1 - 3M/r) / (1 - Omega L) (gravitational redshift + Doppler shift),
//   observed intensity by g^4. Escaping rays sample a procedural star field, so the sky is lensed too.
// The camera is the shared Stage's orbit camera: drag to orbit (including below the disk), scroll or pinch to zoom.
import { useFrame, useThree } from '@react-three/fiber'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'
import { ErrorBoundary } from '../components/ErrorBoundary'
import { cx } from '../lib/format'
import { Stage } from './Stage'

const VERT = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}
`

const FRAG = /* glsl */ `
precision highp float;
varying vec2 vUv;
uniform vec3 uCamPos;
uniform vec3 uRight;
uniform vec3 uUp;
uniform vec3 uFwd;
uniform float uTanX;
uniform float uTanY;
uniform float uTime;
uniform float uDoppler;
uniform float uLensing;
uniform float uExposure;
uniform float uRin;
uniform float uRout;
uniform float uTpeak;
uniform float uTmaxNorm;

const int MAX_STEPS = 320;
const float PI = 3.14159265358979;
const vec3 LUMA = vec3(0.2126, 0.7152, 0.0722);

float hash13(vec3 p) {
  p = fract(p * 0.1031);
  p += dot(p, p.zyx + 31.32);
  return fract((p.x + p.y) * p.z);
}

float vnoise(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  float a = mix(hash13(i), hash13(i + vec3(1, 0, 0)), f.x);
  float b = mix(hash13(i + vec3(0, 1, 0)), hash13(i + vec3(1, 1, 0)), f.x);
  float c = mix(hash13(i + vec3(0, 0, 1)), hash13(i + vec3(1, 0, 1)), f.x);
  float d = mix(hash13(i + vec3(0, 1, 1)), hash13(i + vec3(1, 1, 1)), f.x);
  return mix(mix(a, b, f.y), mix(c, d, f.y), f.z);
}

float fbm(vec3 p) {
  float s = 0.0, a = 0.5;
  for (int i = 0; i < 5; i++) {
    s += a * vnoise(p);
    p = p * 2.03 + vec3(1.7, 9.2, 3.1);
    a *= 0.5;
  }
  return s / 0.96875;
}

// Blackbody colour (Tanner Helland fit) in linear RGB, normalised to unit luminance.
vec3 kelvin(float T) {
  float t = clamp(T / 100.0, 10.0, 400.0);
  vec3 c;
  c.r = t <= 66.0 ? 1.0 : 329.698727446 * pow(max(t - 60.0, 1e-3), -0.1332047592) / 255.0;
  c.g = t <= 66.0 ? (99.4708025861 * log(t) - 161.1195681661) / 255.0
                  : 288.1221695283 * pow(max(t - 60.0, 1e-3), -0.0755148492) / 255.0;
  c.b = t >= 66.0 ? 1.0 : (t <= 19.0 ? 0.0 : (138.5177312231 * log(max(t - 10.0, 1e-3)) - 305.0447927307) / 255.0);
  c = pow(clamp(c, 1e-4, 1.0), vec3(2.2));
  return c / dot(c, LUMA);
}

vec3 stars(vec3 d) {
  vec3 col = vec3(0.0);
  for (int l = 0; l < 3; l++) {
    float sc = 80.0 + 70.0 * float(l);
    vec3 p = d * sc;
    vec3 id = floor(p);
    vec3 f = fract(p) - 0.5;
    float h = hash13(id + float(l) * 17.0);
    if (h > 0.962) {
      vec3 o = vec3(hash13(id + 3.1), hash13(id + 7.7), hash13(id + 11.3)) - 0.5;
      vec3 q = f - o * 0.6;
      float b = 0.035 + 1.4 * pow((h - 0.962) / 0.038, 7.0);
      col += kelvin(3400.0 + 8500.0 * hash13(id + 5.0)) * b * exp(-dot(q, q) * 110.0);
    }
  }
  return col;
}

vec3 acc(vec3 p, float h2) {
  float r2 = dot(p, p);
  return -1.5 * h2 * p / (r2 * r2 * sqrt(r2));
}

// Turbulent gas: anisotropic fBm on (azimuth circle, log r), carried around at the Keplerian rate. Two phases are
// cross-faded so differential rotation never winds the pattern up indefinitely.
float turbulence(float rc, float ph) {
  float om = sqrt(0.5 / (rc * rc * rc));
  float P = 36.0;
  float speed = 4.5;
  float p1 = fract(uTime / P);
  float p2 = fract(uTime / P + 0.5);
  float w1 = 1.0 - abs(2.0 * p1 - 1.0);
  float lr = log(rc);
  float a1 = ph - om * p1 * P * speed + 2.4 * lr;
  float a2 = ph - om * p2 * P * speed + 2.4 * lr;
  float n1 = fbm(vec3(cos(a1) * 2.2, sin(a1) * 2.2, lr * 13.0));
  float n2 = fbm(vec3(cos(a2) * 2.2 + 5.3, sin(a2) * 2.2 - 2.1, lr * 13.0 + 7.7));
  float n = mix(n2, n1, w1);
  return clamp((n - 0.22) / 0.56, 0.0, 1.0);
}

vec3 aces(vec3 x) {
  return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}

void main() {
  vec2 ndc = vUv * 2.0 - 1.0;
  vec3 dir = normalize(uFwd + ndc.x * uTanX * uRight + ndc.y * uTanY * uUp);
  vec3 x = uCamPos;
  vec3 v = dir;
  vec3 hv = cross(x, v);
  float h2 = dot(hv, hv) * uLensing;
  float r0 = length(x);
  float vinf = sqrt(max(1.0 - h2 / (r0 * r0 * r0), 1e-6));
  float L = -hv.y / vinf;                       // photon angular momentum about the disk axis (physical direction)
  // An outward-moving photon outside the photon sphere (r > 1.5) never turns back, so once it is beyond the disk
  // it can only escape: stop there and use its current direction (the remaining weak-field bend is tiny).
  float rEsc = uRout + 2.0;
  int state = 0;                                 // 0 running, 1 disk, 2 captured, 3 escaped
  float rc = 0.0, phc = 0.0;
  for (int i = 0; i < MAX_STEPS; i++) {
    float r = length(x);
    float dt = clamp(0.03 * r * r, 0.004, 0.08 * r + 0.2);
    vec3 k1x = v;                   vec3 k1v = acc(x, h2);
    vec3 k2x = v + 0.5 * dt * k1v;  vec3 k2v = acc(x + 0.5 * dt * k1x, h2);
    vec3 k3x = v + 0.5 * dt * k2v;  vec3 k3v = acc(x + 0.5 * dt * k2x, h2);
    vec3 k4x = v + dt * k3v;        vec3 k4v = acc(x + dt * k3x, h2);
    vec3 xn = x + dt / 6.0 * (k1x + 2.0 * k2x + 2.0 * k3x + k4x);
    vec3 vn = v + dt / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v);
    if (x.y * xn.y <= 0.0 && x.y != xn.y) {
      float t = x.y / (x.y - xn.y);
      vec3 p = mix(x, xn, t);
      float rr = length(p.xz);
      if (rr >= uRin && rr <= uRout) { state = 1; rc = rr; phc = atan(p.z, p.x); break; }
    }
    float rn = length(xn);
    if (rn < 1.0) { state = 2; break; }
    if (rn > rEsc && dot(xn, vn) > 0.0) { state = 3; v = vn; break; }
    x = xn;
    v = vn;
  }
  vec3 col = vec3(0.0);
  if (state == 1) {
    float Tn = pow(uRin / rc, 0.75) * pow(max(1.0 - sqrt(uRin / rc), 0.0), 0.25) / uTmaxNorm;
    float om = sqrt(0.5 / (rc * rc * rc));
    float grav = sqrt(1.0 - 1.5 / rc);
    float g = uDoppler > 0.5 ? grav / (1.0 - om * L) : grav;
    float turb = turbulence(rc, phc);
    float fade = pow(clamp((uRout - rc) / (uRout * 0.45), 0.0, 1.0), 1.5);
    float I = pow(g * Tn, 4.0) * (0.22 + 1.6 * pow(turb, 1.7)) * fade;
    col = kelvin(g * Tn * uTpeak) * I * uExposure;
  } else if (state == 3) {
    col = stars(normalize(v)) * 0.55;
  }
  col = aces(col);
  float l = dot(col, LUMA);
  col = clamp(l + 1.2 * (col - l), 0.0, 1.0);
  gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
}
`

export interface BlackHoleOptions {
  lensing: boolean
  doppler: boolean
  motion: boolean
}

const RIN = 3
const ROUT = 13
const TMAX = (() => {
  let m = 0
  for (let i = 0; i <= 4000; i++) {
    const r = RIN + ((ROUT - RIN) * i) / 4000
    m = Math.max(m, (RIN / r) ** 0.75 * Math.max(1 - Math.sqrt(RIN / r), 0) ** 0.25)
  }
  return m
})()

function BlackHoleScene({ opts, onFail, readout, maxDpr }: { opts: BlackHoleOptions; onFail: () => void; readout?: React.RefObject<HTMLSpanElement>; maxDpr: number }) {
  const mat = useRef<THREE.ShaderMaterial>(null)
  const gl = useThree((s) => s.gl)
  const invalidate = useThree((s) => s.invalidate)
  const setDpr = useThree((s) => s.setDpr)
  const uniforms = useMemo(
    () => ({
      uCamPos: { value: new THREE.Vector3() },
      uRight: { value: new THREE.Vector3() },
      uUp: { value: new THREE.Vector3() },
      uFwd: { value: new THREE.Vector3() },
      uTanX: { value: 1 },
      uTanY: { value: 1 },
      uTime: { value: 0 },
      uDoppler: { value: 1 },
      uLensing: { value: 1 },
      uExposure: { value: 0.36 },
      uRin: { value: RIN },
      uRout: { value: ROUT },
      uTpeak: { value: 4800 },
      uTmaxNorm: { value: TMAX },
    }),
    [],
  )
  // shader compile/link failures do not throw in three.js: catch them and fall back to the A100 still
  useEffect(() => {
    const prev = gl.debug.onShaderError
    gl.debug.onShaderError = (ctx: WebGLRenderingContext, program: WebGLProgram) => {
      console.error('black hole shader failed:', ctx.getProgramInfoLog(program))
      onFail()
    }
    return () => {
      gl.debug.onShaderError = prev
    }
  }, [gl, onFail])
  useEffect(() => {
    uniforms.uDoppler.value = opts.doppler ? 1 : 0
    uniforms.uLensing.value = opts.lensing ? 1 : 0
    invalidate()
  }, [opts.doppler, opts.lensing, uniforms, invalidate])

  // adaptive resolution: drop the pixel ratio while frames are slow, raise it again when there is headroom
  const perf = useRef({ acc: 0, n: 0, dpr: Math.min(maxDpr, 1), frame: 0 })
  useEffect(() => setDpr(perf.current.dpr), [setDpr])

  const m = useMemo(() => new THREE.Matrix4(), [])
  useFrame(({ camera, size }, delta) => {
    const u = uniforms
    const cam = camera as THREE.PerspectiveCamera
    cam.updateMatrixWorld()
    m.copy(cam.matrixWorld)
    u.uCamPos.value.setFromMatrixPosition(m)
    u.uRight.value.setFromMatrixColumn(m, 0).normalize()
    u.uUp.value.setFromMatrixColumn(m, 1).normalize()
    u.uFwd.value.setFromMatrixColumn(m, 2).normalize().negate()
    const ty = Math.tan(THREE.MathUtils.degToRad(cam.fov) / 2) / cam.zoom
    u.uTanY.value = ty
    u.uTanX.value = ty * (size.width / Math.max(1, size.height))
    if (opts.motion) u.uTime.value += Math.min(delta, 0.05)
    const p = perf.current
    p.frame++
    if (delta > 0 && delta < 0.25) {
      p.acc += delta
      p.n++
      if (p.n >= 24) {
        const avg = p.acc / p.n
        const next = avg > 0.045 ? Math.max(0.35, p.dpr * 0.8) : avg < 0.022 ? Math.min(maxDpr, p.dpr * 1.12) : p.dpr
        if (Math.abs(next - p.dpr) > 0.02) {
          p.dpr = next
          setDpr(next)
        }
        p.acc = 0
        p.n = 0
      }
    }
    if (readout?.current && p.frame % 6 === 0) {
      const pos = u.uCamPos.value
      const r = pos.length()
      const incl = THREE.MathUtils.radToDeg(Math.acos(THREE.MathUtils.clamp(pos.y / r, -1, 1)))
      readout.current.textContent = `r = ${r.toFixed(1)} r_s · inclination ${incl.toFixed(0)}° · ${Math.round(size.width * p.dpr)}×${Math.round(size.height * p.dpr)} rays/frame`
    }
  })
  return (
    <mesh frustumCulled={false} renderOrder={-1}>
      <planeGeometry args={[2, 2]} />
      <shaderMaterial ref={mat} vertexShader={VERT} fragmentShader={FRAG} uniforms={uniforms} depthWrite={false} depthTest={false} toneMapped={false} />
    </mesh>
  )
}

const Toggle = ({ on, onClick, children, title }: { on: boolean; onClick: () => void; children: React.ReactNode; title: string }) => (
  <button
    type="button"
    aria-pressed={on}
    title={title}
    onClick={onClick}
    className={cx(
      'h-7 rounded-md border px-2.5 text-[11.5px] font-medium backdrop-blur transition-colors',
      on ? 'border-cyan/40 bg-cyan/[0.12] text-fg' : 'border-white/10 bg-ink-800/80 text-fg-muted hover:border-white/20 hover:text-fg',
    )}
  >
    {children}
  </button>
)

const coarse = () => typeof window !== 'undefined' && !!window.matchMedia?.('(pointer: coarse)').matches

/** Live ray-traced black hole. `compact` hides the physics toggles (for small cards). */
export function BlackHoleViewer({ fallback, compact = false, spin = true }: { fallback?: React.ReactNode; compact?: boolean; spin?: boolean }) {
  const [opts, setOpts] = useState<BlackHoleOptions>({ lensing: true, doppler: true, motion: true })
  const [failed, setFailed] = useState(false)
  const readout = useRef<HTMLSpanElement>(null)
  const maxDpr = useMemo(() => Math.min(typeof window !== 'undefined' ? window.devicePixelRatio || 1 : 1, coarse() ? 0.8 : 1.5), [])
  const onFail = useMemo(() => () => setFailed(true), [])
  const still = fallback ?? <div className="absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim">3D view unavailable (WebGL disabled)</div>
  if (failed) return <>{still}</>
  const flip = (k: keyof BlackHoleOptions) => setOpts((o) => ({ ...o, [k]: !o[k] }))
  return (
    <ErrorBoundary fallback={still}>
      <Stage
        camera={[0, 2.6, 29.9]}
        target={[0, 0, 0]}
        fov={26}
        zoomSpeed={2.2}
        spin={spin}
        animating={opts.motion}
        autoRotateSpeed={0.25}
        focusZoom
        pan={false}
        minDistance={3.4}
        maxDistance={90}
        maxPolar={Math.PI - 0.02}
        dpr={[0.35, maxDpr]}
        hintClass={compact ? 'right-3 bottom-3' : 'left-3 top-3'}
        hint={coarse() ? 'Drag to orbit · pinch to zoom' : 'Drag to orbit · click, then scroll to zoom'}
        overlay={
          <>
            {!compact && (
              <div className="absolute bottom-3 left-3 flex flex-wrap items-center gap-1.5">
                <Toggle on={opts.lensing} onClick={() => flip('lensing')} title="Bend light with gravity (off: straight rays, as if spacetime were flat)">
                  Lensing
                </Toggle>
                <Toggle on={opts.doppler} onClick={() => flip('doppler')} title="Doppler beaming of the orbiting gas (off: gravitational redshift only)">
                  Doppler
                </Toggle>
                <Toggle on={opts.motion} onClick={() => flip('motion')} title="Keplerian rotation of the gas">
                  Gas motion
                </Toggle>
              </div>
            )}
            {!compact && (
              <div className="pointer-events-none absolute right-3 bottom-3 hidden rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur sm:block">
                <span ref={readout}>ray tracing…</span>
              </div>
            )}
          </>
        }
      >
        <BlackHoleScene opts={opts} onFail={onFail} readout={compact ? undefined : readout} maxDpr={maxDpr} />
      </Stage>
    </ErrorBoundary>
  )
}
