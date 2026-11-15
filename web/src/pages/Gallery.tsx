import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { IconClose } from '../components/icons'
import { Portal } from '../components/Portal'
import { Empty, ErrorNote, Skeleton } from '../components/ui'
import { useApi } from '../hooks/useApi'
import { assetUrl } from '../mode'
import type { GalleryItem, GridArtifact, SignMatrixArtifact } from '../types'
import { CityViewer, LatticeViewer, OrbitsViewer, SnakeViewer, ViewerFrame } from '../viz3d/lazy'

type SceneId = 'lattice' | 'city' | 'snake' | 'orbits'

/** Looping MP4 kept only as the fallback when WebGL is unavailable. */
function VideoFallback({ src, poster }: { src?: string; poster?: string }) {
  if (!src && !poster) return <div className="absolute inset-0 flex items-center justify-center text-xs text-fg-dim">3D view unavailable (WebGL disabled)</div>
  return src ? (
    <video src={assetUrl(src)} poster={poster ? assetUrl(poster) : undefined} className="absolute inset-0 h-full w-full object-cover" muted loop playsInline autoPlay preload="metadata" />
  ) : (
    <img src={assetUrl(poster!)} alt="" className="absolute inset-0 h-full w-full object-cover" />
  )
}

function Interactive({ items }: { items: GalleryItem[] }) {
  const lattice = useApi(() => api.problem('no-three-in-line-75'), [], 0)
  const hadamard = useApi(() => api.problem('hadamard-det-51'), [], 0)
  const physics = useApi(() => api.physics(), [], 0)
  const [full, setFull] = useState<SceneId | null>(null)
  const grid = lattice.data?.artifact?.kind === 'grid' ? (lattice.data.artifact as GridArtifact) : null
  const mat = hadamard.data?.artifact?.kind === 'sign_matrix' ? (hadamard.data.artifact as SignMatrixArtifact) : null
  const orbits = physics.data?.threebody?.orbits ?? []
  const has = (name: string) => items.find((i) => i.src.endsWith(name))?.src
  useEffect(() => {
    const k = (e: KeyboardEvent) => e.key === 'Escape' && setFull(null)
    window.addEventListener('keydown', k)
    return () => window.removeEventListener('keydown', k)
  }, [])

  const scenes: { id: SceneId; title: string; data: string; caption: string; node: React.ReactNode }[] = [
    {
      id: 'lattice',
      title: 'The lattice',
      data: grid ? `live SAT model · ${grid.count ?? grid.points.length} points · ${grid.violated_lines.length} violated lines` : 'no-three-in-line-75 artifact',
      caption: 'The current no-three-in-line model on the 75 x 75 grid. Chosen points are lit pillars; each red beam is a line through three or more of them. Tap a pillar to isolate its lines.',
      node: <LatticeViewer art={grid} fallback={<VideoFallback src={has('lattice_orbit.mp4')} poster={has('hero.jpg')} />} />,
    },
    {
      id: 'city',
      title: 'Hadamard city',
      data: mat ? `${mat.n} x ${mat.n} sign matrix${mat.log10_det != null ? ` · log10|det| = ${mat.log10_det.toFixed(4)}` : ''}` : 'hadamard-det-51 artifact',
      caption: 'The 51 x 51 +-1 matrix as a city: +1 entries are towers whose height follows the mean sign of their 5 x 5 neighbourhood, -1 entries are low plinths. Tap an entry to read it.',
      node: <CityViewer art={mat} fallback={<VideoFallback poster={has('hadamard_city.jpg')} />} />,
    },
    {
      id: 'snake',
      title: 'Snake in the 13-cube',
      data: 'record 2950-edge snake (kgrey) · linear projection 13D to 3D',
      caption: 'The record snake-in-the-box path, coloured amber (start) to cyan (end), with dust marking cube vertices. Drag the slider to walk along the path.',
      node: <SnakeViewer fallback={<VideoFallback src={has('snake_turntable.mp4')} poster={has('snake.jpg')} />} />,
    },
    {
      id: 'orbits',
      title: 'Three-body candidates',
      data: orbits.length ? `${orbits.length} verified periodic orbits · integrated in your browser (RK4)` : 'three-body orbits',
      caption: 'Each candidate periodic orbit of the planar three-body problem, re-integrated live from its verified initial conditions. Pick a candidate, scrub time, tap to pause.',
      node: <OrbitsViewer orbits={orbits} fallback={<VideoFallback poster={has('threebody_candidates.png')} />} />,
    },
  ]
  const open = scenes.find((s) => s.id === full)

  return (
    <section>
      <div className="mb-3 flex items-baseline justify-between gap-3">
        <h2 className="text-[14px] font-semibold tracking-[-0.01em]">Interactive scenes</h2>
        <span className="text-[12px] text-fg-dim">Real-time 3D from the lab's data · drag, pinch, tap</span>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {scenes.map((s) => (
          <div key={s.id} className="panel overflow-hidden rounded-xl" data-scene={s.id}>
            <div className="relative aspect-[4/3] sm:aspect-[16/10]">
              {full === s.id ? <div className="absolute inset-0 flex items-center justify-center bg-ink-850 text-xs text-fg-dim">Open in full view</div> : <ViewerFrame className="absolute inset-0 !rounded-none !border-0">{s.node}</ViewerFrame>}
            </div>
            <div className="flex items-start justify-between gap-3 border-t border-white/[0.07] p-4">
              <div className="min-w-0">
                <div className="text-[13.5px] font-semibold tracking-[-0.01em] text-fg">{s.title}</div>
                <div className="mt-0.5 font-mono text-[10.5px] text-fg-dim">{s.data}</div>
                <p className="mt-1.5 text-[12.5px] leading-5 text-fg-muted">{s.caption}</p>
              </div>
              <button
                type="button"
                onClick={() => setFull(s.id)}
                className="h-8 shrink-0 rounded-lg border border-white/10 bg-white/[0.03] px-3 text-[12.5px] font-medium text-fg transition-colors hover:border-white/20 hover:bg-white/[0.06]"
              >
                Expand
              </button>
            </div>
          </div>
        ))}
      </div>
      <Portal>
        <AnimatePresence>
          {open && (
            <motion.div className="fixed inset-0 z-50 flex flex-col bg-ink-900/95 p-3 backdrop-blur sm:p-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.18 }}>
              <div className="mb-3 flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <div className="truncate text-[15px] font-semibold tracking-[-0.01em] text-fg">{open.title}</div>
                  <div className="truncate font-mono text-[11px] text-fg-dim">{open.data}</div>
                </div>
                <button className="rounded-lg border border-white/10 p-2 text-fg-muted transition-colors hover:border-white/20 hover:text-fg" aria-label="Close" onClick={() => setFull(null)}>
                  <IconClose />
                </button>
              </div>
              <ViewerFrame className="min-h-0 flex-1">{open.node}</ViewerFrame>
            </motion.div>
          )}
        </AnimatePresence>
      </Portal>
    </section>
  )
}

function Media({ item, full }: { item: GalleryItem; full?: boolean }) {
  const src = assetUrl(item.src)
  if (item.kind === 'video')
    return (
      <video
        src={src}
        className={full ? 'max-h-[78vh] w-auto max-w-full rounded-xl' : 'h-full w-full object-cover'}
        muted
        loop
        playsInline
        autoPlay={!full}
        controls={full}
        preload="metadata"
      />
    )
  return <img src={src} alt={item.title} loading="lazy" className={full ? 'max-h-[78vh] w-auto max-w-full rounded-xl' : 'h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.015]'} />
}

export default function GalleryPage() {
  const g = useApi(() => api.gallery(), [], 60000)
  const [open, setOpen] = useState<GalleryItem | null>(null)
  useEffect(() => {
    const k = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(null)
    window.addEventListener('keydown', k)
    return () => window.removeEventListener('keydown', k)
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-[22px] font-semibold leading-7 tracking-[-0.02em]">Gallery</h1>
        <p className="mt-1.5 max-w-3xl text-[14px] leading-6 text-fg-muted">Everything here is made from the lab's real artifacts: interactive real-time scenes you can rotate and zoom, then Blender renders scripted by GPT-6 Astra and hero art from gpt-image-2.</p>
      </div>
      <Interactive items={g.data ?? []} />
      <h2 className="!mt-8 text-[14px] font-semibold tracking-[-0.01em]">Renders</h2>
      {g.error && !g.data && <ErrorNote error={g.error} onRetry={g.reload} />}
      {g.loading && !g.data ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 6 }, (_, i) => (
            <Skeleton key={i} className="aspect-[4/3]" />
          ))}
        </div>
      ) : !g.data?.length ? (
        <Empty>No renders yet. The visuals pipeline writes them to the gallery as they finish.</Empty>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {g.data.filter((item) => item.kind !== 'video').map((item, i) => (
            <motion.button
              key={item.src + i}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: Math.min(i, 8) * 0.02, duration: 0.2 }}
              onClick={() => setOpen(item)}
              className="panel panel-hover group overflow-hidden rounded-xl text-left"
            >
              <div className="aspect-[4/3] overflow-hidden bg-ink-850">
                <Media item={item} />
              </div>
              <div className="p-4">
                <div className="flex items-center justify-between gap-2">
                  <div className="truncate text-[13.5px] font-semibold text-fg">{item.title}</div>
                  
                </div>
                <div className="mt-0.5 font-mono text-[10.5px] text-fg-dim">{item.made_with}</div>
                {item.caption && <p className="mt-1.5 line-clamp-2 text-[12px] text-fg-muted">{item.caption}</p>}
              </div>
            </motion.button>
          ))}
        </div>
      )}
      <Portal>
      <AnimatePresence>
        {open && (
          <motion.div className="fixed inset-0 z-50 flex flex-col items-center justify-center gap-3 bg-black/85 p-4 backdrop-blur" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setOpen(null)}>
            <button className="absolute right-4 top-4 rounded-full border border-white/15 p-2 text-fg hover:bg-white/10" aria-label="Close" onClick={() => setOpen(null)}>
              <IconClose />
            </button>
            <motion.div initial={{ scale: 0.96 }} animate={{ scale: 1 }} onClick={(e) => e.stopPropagation()}>
              <Media item={open} full />
            </motion.div>
            <div className="max-w-2xl text-center" onClick={(e) => e.stopPropagation()}>
              <div className="font-semibold text-fg">{open.title}</div>
              <div className="font-mono text-[11px] text-fg-dim">{open.made_with}</div>
              {open.caption && <p className="mt-1 text-sm text-fg-muted">{open.caption}</p>}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      </Portal>
    </div>
  )
}
