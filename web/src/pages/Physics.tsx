import { api } from '../api'
import { Empty, ErrorNote, Panel, Skeleton } from '../components/ui'
import { useApi } from '../hooks/useApi'
import { assetUrl } from '../mode'
import { Link } from 'react-router-dom'
import { Cycle, FigureGrid, TestsBadge } from '../components/Report'
import { BlackHoleViewer, OrbitsViewer, ViewerFrame } from '../viz3d/lazy'

export default function PhysicsPage() {
  const ph = useApi(() => api.physics(), [], 60000)
  const tb = ph.data?.threebody
  const eh = ph.data?.event_horizon
  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-[22px] font-semibold leading-7 tracking-[-0.02em]">Physics</h1>
        <p className="mt-1.5 max-w-3xl text-[14px] leading-6 text-fg-muted">
          The same loop, pointed beyond EinsteinArena: an open problem in celestial mechanics (periodic orbits of the three-body
          problem) and EVENT HORIZON, a verified quantum-information study of the black hole information problem on the A100s.
          Every claim below is classified; nothing here claims to settle an open problem.
        </p>
      </div>
      {ph.error && !ph.data && <ErrorNote error={ph.error} onRetry={ph.reload} />}
      {ph.loading && !ph.data ? (
        <Skeleton className="h-96" />
      ) : (
        <>
          <Panel
            title="EVENT HORIZON · black hole information"
            subtitle={eh?.question ?? 'Page curve, Page’s theorem, sequential evaporation, Bell-pair toy model, scrambling and Hayden-Preskill'}
            right={
              <span className="flex flex-wrap items-center gap-2">
                <TestsBadge tests={eh?.tests} />
                <Link to="/problems/event-horizon" className="inline-flex h-8 items-center rounded-lg border border-white/10 bg-white/[0.03] px-3 text-[12.5px] font-medium text-fg transition-colors hover:border-white/20 hover:bg-white/[0.06]">
                  Open problem page
                </Link>
              </span>
            }
          >
            {!eh ? (
              <Empty>EVENT HORIZON results are still being produced on the A100 (GPU 0).</Empty>
            ) : (
              <div className="space-y-5">
                <div>
                  <ViewerFrame className="h-[380px] w-full bg-[#050608] sm:h-[540px]">
                    <BlackHoleViewer fallback={<img src={assetUrl('/gallery/blackhole.jpg')} alt="ray-traced black hole" className="h-full w-full object-cover" />} />
                  </ViewerFrame>
                  <p className="mt-2 text-[12px] text-fg-dim">
                    A Schwarzschild black hole ray-traced live in your browser: one light ray per pixel per frame along exact null geodesics,
                    thin Keplerian disk from the ISCO, gravitational redshift and Doppler beaming, lensed star field. Drag to orbit (below the disk too),
                    scroll or pinch to zoom in to the photon ring. Same equations as the{' '}
                    <a href={assetUrl('/gallery/blackhole.jpg')} target="_blank" rel="noreferrer" className="text-fg-muted underline decoration-white/20 underline-offset-2 hover:text-fg">
                      24M-ray A100 render
                    </a>
                    .
                  </p>
                </div>
                {eh.summary && <p className="max-w-4xl text-sm text-fg-muted">{eh.summary}</p>}
                {eh.hardware && <p className="font-mono text-[11px] text-fg-dim">hardware: {eh.hardware}</p>}
                <FigureGrid figures={eh.figures ?? []} />
                <div className="space-y-2">
                  <div className="label">Research cycles</div>
                  {(eh.cycles ?? []).map((c, i) => <Cycle key={i} c={c} i={i} />)}
                </div>
              </div>
            )}
          </Panel>
          <Panel
            title="Three-body periodic orbits · candidates"
            subtitle={tb ? `${tb.orbits.length} verified periodic orbits whose topological families are absent from the ${tb.catalog_entries.toLocaleString()} catalogued orbits checked` : 'no data'}
            right={tb?.score != null ? <span className="rounded-full border border-amber/30 bg-amber/[0.08] px-2 py-0.5 text-[11px] font-medium text-amber">{tb.score} candidate families</span> : null}
          >
            {!tb ? (
              <Empty>No verified orbits yet.</Empty>
            ) : (
              <div className="grid gap-5 lg:grid-cols-[1.4fr_1fr]">
                <div className="min-w-0">
                  <ViewerFrame className="h-[420px] w-full sm:h-[520px]">
                    <OrbitsViewer orbits={tb.orbits} fallback={<img src={assetUrl(tb.image)} alt="candidate orbits" className="h-full w-full object-contain" />} />
                  </ViewerFrame>
                  <p className="mt-2 text-[12px] text-fg-dim">
                    Integrated live in your browser (RK4, G = 1, m1 = m2 = 1) from the verified initial conditions. Drag to rotate, scroll or pinch to zoom, tap to pause.{' '}
                    <a href={assetUrl(tb.image)} target="_blank" rel="noreferrer" className="text-fg-muted underline decoration-white/20 underline-offset-2 hover:text-fg">
                      Verifier plot of all {tb.orbits.length}
                    </a>
                  </p>
                </div>
                <div className="space-y-3 text-[13px]">
                  <table className="w-full font-mono text-[12px] [&_td]:py-1.5 [&_th]:pb-1.5 [&_th]:font-sans [&_th]:text-[11px] [&_th]:font-medium">
                    <thead className="text-fg-dim">
                      <tr><th className="text-left">#</th><th className="text-right">vx</th><th className="text-right">vy</th><th className="text-right">T</th><th className="text-right">m3</th></tr>
                    </thead>
                    <tbody>
                      {tb.orbits.map((o, i) => (
                        <tr key={i} className="border-t border-white/[0.06]">
                          <td>{i + 1}</td>
                          <td className="text-right">{o.vx.toFixed(6)}</td>
                          <td className="text-right">{o.vy.toFixed(6)}</td>
                          <td className="text-right">{o.T.toFixed(4)}</td>
                          <td className="text-right">{o.m3 ?? 1}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {tb.verification && <p className="text-fg-muted"><span className="text-fg">Verification:</span> {tb.verification}</p>}
                  {tb.novelty && <p className="text-fg-muted"><span className="text-fg">What “candidate” means:</span> {tb.novelty}</p>}
                  {tb.caveats && <p className="text-fg-dim">{tb.caveats}</p>}
                </div>
              </div>
            )}
          </Panel>
        </>
      )}
    </div>
  )
}
