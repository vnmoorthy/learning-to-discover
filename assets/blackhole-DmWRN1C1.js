import{r as n,j as e}from"./vendor-P-kBGxpi.js";import{u as T,V as w,M as S,a as C,f as M}from"./three-roeo-AJ4.js";import{E as D,S as U}from"./Stage-CmAeWKgs.js";import{c as z}from"./index-aLKidagE.js";const L=`
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}
`,q=`
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
`,x=3,E=13,A=(()=>{let t=0;for(let a=0;a<=4e3;a++){const i=x+(E-x)*a/4e3;t=Math.max(t,(x/i)**.75*Math.max(1-Math.sqrt(x/i),0)**.25)}return t})();function N({opts:t,onFail:a,readout:i,maxDpr:l}){const y=n.useRef(null),v=T(r=>r.gl),g=T(r=>r.invalidate),p=T(r=>r.setDpr),u=n.useMemo(()=>({uCamPos:{value:new w},uRight:{value:new w},uUp:{value:new w},uFwd:{value:new w},uTanX:{value:1},uTanY:{value:1},uTime:{value:0},uDoppler:{value:1},uLensing:{value:1},uExposure:{value:.36},uRin:{value:x},uRout:{value:E},uTpeak:{value:4800},uTmaxNorm:{value:A}}),[]);n.useEffect(()=>{const r=v.debug.onShaderError;return v.debug.onShaderError=(c,s)=>{console.error("black hole shader failed:",c.getProgramInfoLog(s)),a()},()=>{v.debug.onShaderError=r}},[v,a]),n.useEffect(()=>{u.uDoppler.value=t.doppler?1:0,u.uLensing.value=t.lensing?1:0,g()},[t.doppler,t.lensing,u,g]);const b=n.useRef({acc:0,n:0,dpr:Math.min(l,1),frame:0});n.useEffect(()=>p(b.current.dpr),[p]);const f=n.useMemo(()=>new S,[]);return C(({camera:r,size:c},s)=>{const d=u,k=r;k.updateMatrixWorld(),f.copy(k.matrixWorld),d.uCamPos.value.setFromMatrixPosition(f),d.uRight.value.setFromMatrixColumn(f,0).normalize(),d.uUp.value.setFromMatrixColumn(f,1).normalize(),d.uFwd.value.setFromMatrixColumn(f,2).normalize().negate();const j=Math.tan(M.degToRad(k.fov)/2)/k.zoom;d.uTanY.value=j,d.uTanX.value=j*(c.width/Math.max(1,c.height)),t.motion&&(d.uTime.value+=Math.min(s,.05));const o=b.current;if(o.frame++,s>0&&s<.25&&(o.acc+=s,o.n++,o.n>=24)){const h=o.acc/o.n,m=h>.045?Math.max(.35,o.dpr*.8):h<.022?Math.min(l,o.dpr*1.12):o.dpr;Math.abs(m-o.dpr)>.02&&(o.dpr=m,p(m)),o.acc=0,o.n=0}if(i!=null&&i.current&&o.frame%6===0){const h=d.uCamPos.value,m=h.length(),F=M.radToDeg(Math.acos(M.clamp(h.y/m,-1,1)));i.current.textContent=`r = ${m.toFixed(1)} r_s · inclination ${F.toFixed(0)}° · ${Math.round(c.width*o.dpr)}×${Math.round(c.height*o.dpr)} rays/frame`}}),e.jsxs("mesh",{frustumCulled:!1,renderOrder:-1,children:[e.jsx("planeGeometry",{args:[2,2]}),e.jsx("shaderMaterial",{ref:y,vertexShader:L,fragmentShader:q,uniforms:u,depthWrite:!1,depthTest:!1,toneMapped:!1})]})}const R=({on:t,onClick:a,children:i,title:l})=>e.jsx("button",{type:"button","aria-pressed":t,title:l,onClick:a,className:z("h-7 rounded-md border px-2.5 text-[11.5px] font-medium backdrop-blur transition-colors",t?"border-cyan/40 bg-cyan/[0.12] text-fg":"border-white/10 bg-ink-800/80 text-fg-muted hover:border-white/20 hover:text-fg"),children:i}),P=()=>{var t;return typeof window<"u"&&!!((t=window.matchMedia)!=null&&t.call(window,"(pointer: coarse)").matches)};function _({fallback:t,compact:a=!1,spin:i=!0}){const[l,y]=n.useState({lensing:!0,doppler:!0,motion:!0}),[v,g]=n.useState(!1),p=n.useRef(null),u=n.useMemo(()=>Math.min(typeof window<"u"&&window.devicePixelRatio||1,P()?.8:1.5),[]),b=n.useMemo(()=>()=>g(!0),[]),f=t??e.jsx("div",{className:"absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim",children:"3D view unavailable (WebGL disabled)"});if(v)return e.jsx(e.Fragment,{children:f});const r=c=>y(s=>({...s,[c]:!s[c]}));return e.jsx(D,{fallback:f,children:e.jsx(U,{camera:[0,2.6,29.9],target:[0,0,0],fov:26,zoomSpeed:2.2,spin:i,animating:l.motion,autoRotateSpeed:.25,focusZoom:!0,pan:!1,minDistance:3.4,maxDistance:90,maxPolar:Math.PI-.02,dpr:[.35,u],hintClass:a?"right-3 bottom-3":"left-3 top-3",hint:P()?"Drag to orbit · pinch to zoom":"Drag to orbit · click, then scroll to zoom",overlay:e.jsxs(e.Fragment,{children:[!a&&e.jsxs("div",{className:"absolute bottom-3 left-3 flex flex-wrap items-center gap-1.5",children:[e.jsx(R,{on:l.lensing,onClick:()=>r("lensing"),title:"Bend light with gravity (off: straight rays, as if spacetime were flat)",children:"Lensing"}),e.jsx(R,{on:l.doppler,onClick:()=>r("doppler"),title:"Doppler beaming of the orbiting gas (off: gravitational redshift only)",children:"Doppler"}),e.jsx(R,{on:l.motion,onClick:()=>r("motion"),title:"Keplerian rotation of the gas",children:"Gas motion"})]}),!a&&e.jsx("div",{className:"pointer-events-none absolute right-3 bottom-3 hidden rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur sm:block",children:e.jsx("span",{ref:p,children:"ray tracing…"})})]}),children:e.jsx(N,{opts:l,onFail:b,readout:a?void 0:p,maxDpr:u})})})}export{_ as BlackHoleViewer};
