import{r as n,j as t}from"./vendor-P-kBGxpi.js";import{u as S,V as E,M as A,f as N,a as B,g as p}from"./three-33aIcrB3.js";import{N as X,c as L}from"./index-Yz3Wed_g.js";import{S as I}from"./Stage-Bd85V4vB.js";const _=`
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}
`,$=`
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
  // Photon angular momentum about the disk axis, sign chosen so the gas orbits in the +phi = atan(z, x) sense:
  // the same sense the turbulence texture is advected in, and the same bright side as the A100 render.
  float L = hv.y / vinf;
  // An outward-moving photon outside the photon sphere (r > 1.5) never turns back, so once it is beyond the disk it
  // can only escape: stop there and add the remaining weak-field bend analytically (below).
  float rEsc = uRout + 2.0;
  int state = 0;                                 // 0 running, 1 disk, 2 captured, 3 escaped
  float rc = 0.0, phc = 0.0;
  // a camera far outside rEsc: move along the (nearly straight) ray to the rEsc sphere first, or escape at once
  if (r0 > rEsc) {
    float bq = dot(x, v);
    float disc = bq * bq - (r0 * r0 - rEsc * rEsc);
    if (disc < 0.0 || bq > 0.0) { state = 3; }
    else { x += (-bq - sqrt(disc)) * v; }
  }
  for (int i = 0; i < MAX_STEPS; i++) {
    if (state != 0) break;
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
    if (rn > rEsc && dot(xn, vn) > 0.0) { state = 3; x = xn; v = vn; break; }
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
    // remaining weak-field deflection from the exit point to infinity (first order in M/b), towards the hole
    vec3 vh = normalize(v);
    float rr = length(x);
    float s = dot(x, vh);
    vec3 bv = x - s * vh;
    float b = max(length(bv), 1e-4);
    float del = uLensing * (1.0 / b) * (1.0 - s * (3.0 * b * b + 2.0 * s * s) / (2.0 * rr * rr * rr));
    vec3 d = vh * cos(del) - (bv / b) * sin(del);
    col = stars(normalize(d)) * 0.55;
  }
  col = aces(col);
  float l = dot(col, LUMA);
  col = clamp(l + 1.2 * (col - l), 0.0, 1.0);
  gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
}
`,w=3,U=13,G=(()=>{let e=0;for(let r=0;r<=4e3;r++){const a=w+(U-w)*r/4e3;e=Math.max(e,(w/a)**.75*Math.max(1-Math.sqrt(w/a),0)**.25)}return e})(),D=8;function V({opts:e,onFail:r,readout:a,maxDpr:d,dpr:v,onDpr:y}){const x=q()?.35:.55,M=n.useRef(null),c=S(i=>i.gl),T=S(i=>i.invalidate),u=n.useMemo(()=>({uCamPos:{value:new E},uRight:{value:new E},uUp:{value:new E},uFwd:{value:new E},uTanX:{value:1},uTanY:{value:1},uTime:{value:0},uDoppler:{value:1},uLensing:{value:1},uExposure:{value:.36},uRin:{value:w},uRout:{value:U},uTpeak:{value:4800},uTmaxNorm:{value:G}}),[]);n.useEffect(()=>{const i=c.debug.onShaderError;return c.debug.onShaderError=(g,z)=>{console.error("black hole shader failed:",g.getProgramInfoLog(z)),r()},()=>{c.debug.onShaderError=i}},[c,r]),n.useEffect(()=>{u.uDoppler.value=e.doppler?1:0,u.uLensing.value=e.lensing?1:0,T()},[e.doppler,e.lensing,u,T]);const m=n.useRef({acc:0,n:0,skip:1,init:!1,frame:0});n.useEffect(()=>{m.current.acc=0,m.current.n=0,m.current.skip=1},[v]);const s=n.useMemo(()=>new A,[]),h=n.useMemo(()=>new N,[]);return B((i,g)=>{const{camera:z,size:b}=i,l=u,R=z;R.updateMatrixWorld(),s.copy(R.matrixWorld),l.uCamPos.value.setFromMatrixPosition(s);const C=l.uCamPos.value.length(),k=C<D?C/D:1;k<1&&l.uCamPos.value.multiplyScalar(1/k),l.uRight.value.setFromMatrixColumn(s,0).normalize(),l.uUp.value.setFromMatrixColumn(s,1).normalize(),l.uFwd.value.setFromMatrixColumn(s,2).normalize().negate();const F=Math.tan(p.degToRad(R.fov)/2)/R.zoom*k;l.uTanY.value=F,l.uTanX.value=F*(b.width/Math.max(1,b.height)),e.motion&&(l.uTime.value+=Math.min(g,.05));const o=m.current;if(o.frame++,!o.init&&b.width>0){o.init=!0;const f=p.clamp(Math.sqrt(42e4/(b.width*b.height)),x,d);Math.abs(f-v)>.02&&y(f)}else if(i.frameloop==="always"){if(o.skip>0)o.skip--;else if(g<.2&&(o.acc+=g,o.n++,o.acc>=.5&&o.n>=4)){const f=o.acc/o.n,P=p.clamp(v*p.clamp(Math.sqrt(1/30/f),.7,1.1),x,d);Math.abs(P-v)>.03&&y(P),o.acc=0,o.n=0}}else o.acc=0,o.n=0;if(a!=null&&a.current&&o.frame%6===0){const f=l.uCamPos.value,P=p.radToDeg(Math.acos(p.clamp(f.y/f.length(),-1,1)));c.getDrawingBufferSize(h),a.current.textContent=`r = ${f.length().toFixed(1)} r_s${k<1?` · ×${(1/k).toFixed(1)} zoom`:""} · inclination ${P.toFixed(0)}° · ${h.x}×${h.y} rays/frame`}}),t.jsxs("mesh",{frustumCulled:!1,renderOrder:-1,children:[t.jsx("planeGeometry",{args:[2,2]}),t.jsx("shaderMaterial",{ref:M,vertexShader:_,fragmentShader:$,uniforms:u,depthWrite:!1,depthTest:!1,toneMapped:!1})]})}const j=({on:e,onClick:r,children:a,title:d})=>t.jsx("button",{type:"button","aria-pressed":e,title:d,onClick:r,className:L("h-7 whitespace-nowrap rounded-md border px-2.5 text-[11.5px] font-medium backdrop-blur transition-colors",e?"border-cyan/40 bg-cyan/[0.12] text-fg":"border-white/10 bg-ink-800/80 text-fg-muted hover:border-white/20 hover:text-fg"),children:a}),q=()=>{var e;return typeof window<"u"&&!!((e=window.matchMedia)!=null&&e.call(window,"(pointer: coarse)").matches)},W=()=>{var e;return typeof window<"u"&&!!((e=window.matchMedia)!=null&&e.call(window,"(prefers-reduced-motion: reduce)").matches)};function Z({fallback:e,compact:r=!1}){const[a,d]=n.useState(()=>({lensing:!0,doppler:!0,motion:!W()})),[v,y]=n.useState(!1),x=n.useRef(null),M=n.useMemo(()=>Math.min(typeof window<"u"&&window.devicePixelRatio||1,q()?.8:1.5),[]),[c,T]=n.useState(()=>Math.min(M,.75)),u=n.useMemo(()=>()=>y(!0),[]),m=e??t.jsx("div",{className:"absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim",children:"3D view unavailable (WebGL disabled)"});if(v)return t.jsx(t.Fragment,{children:m});const s=h=>d(i=>({...i,[h]:!i[h]}));return t.jsx(X,{fallback:m,children:t.jsx(I,{camera:[0,2.6,29.9],target:[0,0,0],fov:26,zoomSpeed:1,spin:!1,onTap:()=>s("motion"),animating:a.motion,focusZoom:!0,pan:!1,minDistance:2.5,maxDistance:90,maxPolar:Math.PI-.02,dpr:c,hintClass:r?"right-3 bottom-3":"left-3 top-3",hint:q()?"Drag to orbit · pinch to zoom · tap to pause":"Drag to orbit · click, then scroll to zoom · tap to pause",overlay:t.jsxs(t.Fragment,{children:[t.jsxs("div",{className:L("absolute flex flex-wrap items-center gap-1.5",r?"right-[4.5rem] top-3":"bottom-3 left-3"),children:[t.jsx(j,{on:a.motion,onClick:()=>s("motion"),title:"Keplerian rotation of the gas (tap the view to pause or resume)",children:a.motion?"Pause gas":"Play gas"}),!r&&t.jsxs(t.Fragment,{children:[t.jsx(j,{on:a.lensing,onClick:()=>s("lensing"),title:"Bend light with gravity (off: straight rays, as if spacetime were flat)",children:"Lensing"}),t.jsx(j,{on:a.doppler,onClick:()=>s("doppler"),title:"Doppler beaming of the orbiting gas (off: no beaming; gravitational redshift and time dilation remain)",children:"Doppler"})]})]}),!r&&t.jsx("div",{className:"pointer-events-none absolute right-3 bottom-3 hidden rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur sm:block",children:t.jsx("span",{ref:x,children:"ray tracing…"})})]}),children:t.jsx(V,{opts:a,onFail:u,readout:r?void 0:x,maxDpr:M,dpr:c,onDpr:T})})})}export{Z as BlackHoleViewer};
