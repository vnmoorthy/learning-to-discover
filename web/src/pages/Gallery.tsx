import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { IconClose } from '../components/icons'
import { Portal } from '../components/Portal'
import { Empty, ErrorNote, Skeleton } from '../components/ui'
import { useApi } from '../hooks/useApi'
import { assetUrl } from '../mode'
import type { GalleryItem } from '../types'

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
  return <img src={src} alt={item.title} loading="lazy" className={full ? 'max-h-[78vh] w-auto max-w-full rounded-xl' : 'h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.03]'} />
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
    <div className="space-y-5">
      <div>
        <h1 className="text-[22px] font-semibold leading-7 tracking-[-0.02em]">Gallery</h1>
        <p className="mt-1.5 max-w-3xl text-[14px] leading-6 text-fg-muted">Renders made from the lab's real artifacts: Blender scenes scripted by GPT-6 Astra and hero art from gpt-image-2.</p>
      </div>
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
          {g.data.map((item, i) => (
            <motion.button
              key={item.src + i}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: Math.min(i, 9) * 0.04 }}
              onClick={() => setOpen(item)}
              className="panel panel-hover group overflow-hidden rounded-xl text-left"
            >
              <div className="aspect-[4/3] overflow-hidden bg-black">
                <Media item={item} />
              </div>
              <div className="p-4">
                <div className="flex items-center justify-between gap-2">
                  <div className="truncate text-[13.5px] font-semibold text-fg">{item.title}</div>
                  <span className="shrink-0 rounded-md border border-white/10 px-1.5 py-0.5 font-mono text-[10px] text-fg-dim">{item.kind}</span>
                </div>
                <div className="mt-0.5 font-mono text-[10.5px] text-cyan/80">{item.made_with}</div>
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
              <div className="font-mono text-[11px] text-cyan/80">{open.made_with}</div>
              {open.caption && <p className="mt-1 text-sm text-fg-muted">{open.caption}</p>}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      </Portal>
    </div>
  )
}
