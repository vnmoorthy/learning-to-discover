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
  success: 'bg-good',
  error: 'bg-bad',
  info: 'bg-cyan',
  record: 'bg-amber',
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
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 4 }}
              transition={{ duration: 0.18, ease: 'easeOut' }}
              className="pointer-events-auto flex gap-3 rounded-xl border border-white/10 bg-ink-700 px-4 py-3 shadow-pop"
            >
              <span className={`mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full ${STYLE[t.kind]}`} />
              <div className="min-w-0">
                <div className="text-[13px] font-medium text-fg">{t.title}</div>
                {t.msg && <div className="mt-0.5 break-words font-mono text-[11.5px] text-fg-muted">{t.msg}</div>}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </Ctx.Provider>
  )
}
