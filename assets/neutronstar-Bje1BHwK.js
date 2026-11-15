import{r as c,j as e}from"./vendor-P-kBGxpi.js";import{S as m,D as d}from"./three-DctUVgaD.js";import{Q as v,c as x}from"./index-CJ21_E7C.js";import{S as f}from"./Stage-C05qYdD5.js";const u={m14:{R_km:11.709,M_msun:1.4,pc_MeVfm3:85.27604349022039,r:[0,.0141,.0282,.0423,.0563,.0704,.0845,.0986,.1127,.1268,.1408,.1549,.169,.1831,.1972,.2113,.2254,.2394,.2535,.2676,.2817,.2958,.3099,.3239,.338,.3521,.3662,.3803,.3944,.4085,.4225,.4366,.4507,.4648,.4789,.493,.507,.5211,.5352,.5493,.5634,.5775,.5915,.6056,.6197,.6338,.6479,.662,.6761,.6901,.7042,.7183,.7324,.7465,.7606,.7746,.7887,.8028,.8169,.831,.8451,.8592,.8732,.8873,.9014,.9155,.9296,.9437,.9577,.9718,.9859,1],n_over_nsat:[3.3663,3.3658,3.3642,3.3616,3.358,3.3534,3.3477,3.341,3.3333,3.3245,3.3147,3.3038,3.2919,3.2789,3.2649,3.2498,3.2337,3.2165,3.1982,3.1789,3.1584,3.1369,3.1143,3.0906,3.0658,3.0398,3.0128,2.9845,2.9552,2.9247,2.893,2.8601,2.826,2.7906,2.7541,2.7162,2.6771,2.6367,2.595,2.5519,2.5074,2.4615,2.4141,2.3652,2.3148,2.2628,2.2091,2.1537,2.0965,2.0374,1.9763,1.9132,1.848,1.7805,1.7105,1.6376,1.5616,1.482,1.3986,1.3105,1.2171,1.1171,1.0088,.8894,.7541,.5925,.2805,.0876,.0129,7e-4,1e-4,0]},mmax:{R_km:9.973,M_msun:2.0484,pc_MeVfm3:866.9,r:[0,.0141,.0282,.0423,.0563,.0704,.0845,.0986,.1127,.1268,.1408,.1549,.169,.1831,.1972,.2113,.2254,.2394,.2535,.2676,.2817,.2958,.3099,.3239,.338,.3521,.3662,.3803,.3944,.4085,.4225,.4366,.4507,.4648,.4789,.493,.507,.5211,.5352,.5493,.5634,.5775,.5915,.6056,.6197,.6338,.6479,.662,.6761,.6901,.7042,.7183,.7324,.7465,.7606,.7746,.7887,.8028,.8169,.831,.8451,.8592,.8732,.8873,.9014,.9155,.9296,.9437,.9577,.9718,.9859,1],n_over_nsat:[7.5523,7.5506,7.5453,7.5367,7.5245,7.5089,7.4899,7.4675,7.4417,7.4125,7.3799,7.3441,7.305,7.2627,7.2172,7.1685,7.1167,7.0618,7.004,6.9431,6.8794,6.8128,6.7434,6.6712,6.5963,6.5188,6.4387,6.3561,6.2709,6.1834,6.0935,6.0012,5.9067,5.81,5.7111,5.6101,5.507,5.4019,5.2948,5.1857,5.0747,4.9618,4.8471,4.7305,4.6121,4.4919,4.3699,4.2462,4.1206,3.9932,3.864,3.7343,3.6071,3.4775,3.3454,3.2107,3.073,2.9321,2.7878,2.6395,2.4867,2.3287,2.1645,1.9928,1.812,1.6193,1.4091,1.1723,.8882,.4169,.0059,0]}},h={stars:u},p=h.stars,b=12,i=72,g=`
uniform float uN[${i}];
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
  float f = clamp(x, 0.0, 1.0) * float(${i-1});
  int i = int(floor(f));
  int j = min(i + 1, ${i-1});
  float a = 0.0, b = 0.0;
  for (int k = 0; k < ${i}; k++) { if (k == i) a = uN[k]; if (k == j) b = uN[k]; }
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
`,M=`
varying vec2 vP;
void main() { vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`,j=`
${g}
varying vec2 vP;
void main() { gl_FragColor = vec4(pow(shade(length(vP)), vec3(1.0 / 2.2)), 1.0); }
`,y=`
varying vec3 vL; varying vec3 vN; varying vec3 vV;
void main() {
  vL = position;
  vec4 w = modelMatrix * vec4(position, 1.0);
  vN = normalize(mat3(modelMatrix) * normal);
  vV = normalize(cameraPosition - w.xyz);
  gl_Position = projectionMatrix * viewMatrix * w;
}
`,_=`
varying vec3 vL; varying vec3 vN; varying vec3 vV;
void main() {
  if (vL.x > 0.0 && vL.z > 0.0) discard;          // the cut-away wedge
  float fr = pow(1.0 - max(dot(vN, vV), 0.0), 2.5);
  vec3 base = vec3(0.55, 0.62, 0.72) * (0.35 + 0.65 * max(dot(vN, normalize(vec3(0.4, 0.8, 0.6))), 0.0));
  vec3 col = base + vec3(0.45, 0.75, 1.0) * fr * 0.9;
  gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
}
`;function w({star:s}){const a=s.R_km/b,n=c.useMemo(()=>({uN:{value:s.n_over_nsat.slice(0,i)},uMaxN:{value:8}}),[s]),o=(r,l)=>new m({vertexShader:l,fragmentShader:r,uniforms:n,side:d}),t=c.useMemo(()=>({disk:o(j,M),shell:o(_,y)}),[n]);return c.useEffect(()=>()=>{t.disk.dispose(),t.shell.dispose()},[t]),e.jsxs("group",{scale:[a,a,a],children:[e.jsx("mesh",{material:t.shell,children:e.jsx("sphereGeometry",{args:[1,96,64]})}),e.jsx("mesh",{material:t.disk,rotation:[0,-Math.PI/2,0],children:e.jsx("circleGeometry",{args:[1,128,-Math.PI/2,Math.PI]})}),e.jsx("mesh",{material:t.disk,children:e.jsx("circleGeometry",{args:[1,128,-Math.PI/2,Math.PI]})})]})}function R({fallback:s}){const[a,n]=c.useState("m14"),o=p[a],t=s??e.jsx("div",{className:"absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim",children:"3D view unavailable (WebGL disabled)"});return e.jsx(v,{fallback:t,children:e.jsx(f,{camera:[2.4,1.3,2.4],target:[0,0,0],fov:36,focusZoom:!0,minDistance:1.3,maxDistance:8,maxPolar:Math.PI-.02,autoRotateSpeed:.6,overlay:e.jsxs(e.Fragment,{children:[e.jsx("div",{className:"absolute bottom-3 left-3 flex flex-wrap items-center gap-1.5",children:["m14","mmax"].map(r=>e.jsx("button",{type:"button","aria-pressed":a===r,onClick:()=>n(r),className:x("h-7 whitespace-nowrap rounded-md border px-2.5 text-[11.5px] font-medium backdrop-blur transition-colors",a===r?"border-cyan/40 bg-cyan/[0.12] text-fg":"border-white/10 bg-ink-800/80 text-fg-muted hover:border-white/20 hover:text-fg"),children:r==="m14"?"1.40 M☉ star":"Maximum mass 2.05 M☉"},r))}),e.jsxs("div",{className:"pointer-events-none absolute right-3 bottom-3 rounded-md border border-white/[0.08] bg-ink-800/85 px-2.5 py-1.5 font-mono text-[11px] text-fg-muted backdrop-blur",children:["SLy · M = ",o.M_msun.toFixed(2)," M☉ · R = ",o.R_km.toFixed(2)," km · centre ",o.n_over_nsat[0].toFixed(1)," n_sat"]}),e.jsxs("div",{className:"pointer-events-none absolute right-3 top-12 w-40 rounded-md border border-white/[0.08] bg-ink-800/85 p-2 text-[10.5px] text-fg-muted backdrop-blur",children:[e.jsx("div",{className:"mb-1",children:"baryon density n / n_sat"}),e.jsx("div",{className:"h-2 rounded",style:{background:"linear-gradient(90deg,#1a0510,#bf2e14,#fa9e2e,#fff2bf,#b3e0ff)"}}),e.jsxs("div",{className:"mt-0.5 flex justify-between font-mono",children:[e.jsx("span",{children:"0.01"}),e.jsx("span",{children:"8"})]}),e.jsx("div",{className:"mt-1 text-fg-dim",children:"cyan rings: 0.5, 1, 2, 4 n_sat"})]})]}),children:e.jsx(w,{star:o})})})}export{R as NeutronStarViewer};
