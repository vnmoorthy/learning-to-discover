# Phoenixastar: web UI

React 18 + Vite + TypeScript + Tailwind, framer-motion, recharts, @react-three/fiber. Contract: `../SPEC.md` sections 4 to 6.

```bash
npm install
npm run dev                 # :5173 (next free port if taken), proxies /api and /gallery/* to 127.0.0.1:8787
npm run dev:fixtures        # VITE_FIXTURES=1: in-browser simulated backend, no server needed (purple banner)
npm run build               # tsc + vite build -> dist/ (served by `python3 -m ltd.server` at /)
npm run build:static        # static replay -> dist-static/ for GitHub Pages under /phoenixastar/
```

- `LTD_BACKEND=http://host:port npm run dev` points the proxy at another backend.
- Static mode reads `public/data/*.json` (written by `python3 -m ltd.snapshot`), uses HashRouter, disables every
  mutating button and shows a "Replay of a live run" banner. `dist-static` copies `public/data` at build time, so
  run `npm run build:static` again after the final `python3 -m ltd.snapshot`.
- Fixture JSON lives in `src/fixtures/` (shapes match the API exactly). It is only bundled when `VITE_FIXTURES=1`.

## Smoke test (headless Chromium, Python Playwright)

```bash
python3 e2e/smoke.py --url http://127.0.0.1:8787                       # real backend: read-only, clicks nothing
python3 e2e/smoke.py --url http://localhost:5173 --mutate              # fixture dev server: also clicks every button
python3 e2e/smoke.py --url <url printed by `VITE_STATIC=1 npx vite preview --outDir dist-static`> --static
```

It visits all pages at 1440 px and 390 px and fails on page errors, console errors, failed `/api` or data requests,
horizontal scroll, or a page that never renders. Never pass `--mutate` against the real `ltd.server`.

## Known gotcha: port 8787

Another local app (a Node/Express server) also listens on `*:8787`. `ltd.server` binds `127.0.0.1:8787`, which wins
while it runs, but when `ltd.server` is down the other app answers with HTML 404s. The UI then says
"not a JSON reply ... is another app answering on that port?" instead of rendering data.

Layout: `src/api.ts` (typed client), `src/types.ts` (contract types), `src/live.tsx` (state + SSE + 5 s polling
fallback), `src/hooks/useEventStream.ts` (SSE with reconnect/backoff), `src/pages/*`, `src/viz/*` (lattice hero,
no-three canvas, sign-matrix heatmap, integer set, bit wall), `e2e/smoke.py`.
