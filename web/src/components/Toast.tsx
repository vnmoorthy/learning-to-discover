import { createContext, useCallback, useContext, useMemo, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

export interface ToastInput {
  kind: 'success' | 'error' | 'info' | 'record'
  title: string
  msg?: string
  ttl?: number
}
interface ToastItem extends ToastInput {
  id: number
}

const Ctx = createContext<{ push: (t: ToastInput) => void } | null>(null)

export function useToast() {
  const c = useContext(Ctx)
  if (!c) throw new Error('useToast outside ToastProvider')
  return c
}

const STYLE: Record<ToastInput['kind'], string> = {
  success: 'border-good/40 text-good',
  error: 'border-bad/50 text-bad',
  info: 'border-cyan/40 text-cyan',
  record: 'border-amber/60 text-amber shadow-amber',
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([])
  const seq = useRef(0)
  const push = useCallback((t: ToastInput) => {
    const id = ++seq.current
    setItems((xs) => [...xs.slice(-4), { ...t, id }])
    setTimeout(() => setItems((xs) => xs.filter((x) => x.id !== id)), t.ttl ?? 5000)
  }, [])
  const value = useMemo(() => ({ push }), [push])
  return (
    <Ctx.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed bottom-4 right-4 z-[100] flex w-[min(380px,calc(100vw-32px))] flex-col gap-2" aria-live="polite">
        <AnimatePresence initial={false}>
          {items.map((t) => (
            <motion.div
              key={t.id}
              layout
              initial={{ opacity: 0, y: 16, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, x: 40 }}
              transition={{ type: 'spring', stiffness: 380, damping: 30 }}
              className={`pointer-events-auto rounded-xl border bg-ink-800/95 px-4 py-3 backdrop-blur ${STYLE[t.kind]}`}
            >
              <div className="text-sm font-semibold">{t.title}</div>
              {t.msg && <div className="mt-0.5 break-words font-mono text-xs text-fg-muted">{t.msg}</div>}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </Ctx.Provider>
  )
}
