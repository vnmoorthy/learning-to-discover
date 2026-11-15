import { useCallback, useEffect, useRef, useState } from 'react'
import { STATIC } from '../mode'

export interface ApiState<T> {
  data: T | null
  error: string | null
  loading: boolean
  reload: () => Promise<void>
  setData: React.Dispatch<React.SetStateAction<T | null>>
  updatedAt: number | null
}

/** Load data from the API, optionally polling (paused while the tab is hidden; disabled in static mode). */
export function useApi<T>(fn: () => Promise<T>, deps: unknown[], pollMs?: number): ApiState<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [updatedAt, setUpdatedAt] = useState<number | null>(null)
  const fnRef = useRef(fn)
  fnRef.current = fn
  const seq = useRef(0)

  const reload = useCallback(async () => {
    const my = ++seq.current
    try {
      const d = await fnRef.current()
      if (my !== seq.current) return
      setData(d)
      setError(null)
      setUpdatedAt(Date.now())
    } catch (e) {
      if (my !== seq.current) return
      setError((e as Error).message || String(e))
    } finally {
      if (my === seq.current) setLoading(false)
    }
  }, [])

  useEffect(() => {
    setLoading(true)
    void reload()
    if (!pollMs || STATIC) return
    const t = setInterval(() => {
      if (document.visibilityState === 'visible') void reload()
    }, pollMs)
    return () => clearInterval(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, pollMs])

  return { data, error, loading, reload, setData, updatedAt }
}

export type ActionStatus = 'idle' | 'loading' | 'success' | 'error'

/** Wraps a mutating API call with loading / success / error state for buttons. */
export function useAction<A extends unknown[], R>(fn: (...args: A) => Promise<R>, opts: { resetMs?: number } = {}) {
  const [status, setStatus] = useState<ActionStatus>('idle')
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<R | null>(null)
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const errRef = useRef<string | null>(null)
  const fnRef = useRef(fn)
  fnRef.current = fn

  useEffect(() => () => {
    if (timer.current) clearTimeout(timer.current)
  }, [])

  const run = useCallback(
    async (...args: A): Promise<R | null> => {
      if (timer.current) clearTimeout(timer.current)
      setStatus('loading')
      setError(null)
      errRef.current = null
      try {
        const r = await fnRef.current(...args)
        setResult(r)
        setStatus('success')
        timer.current = setTimeout(() => setStatus('idle'), opts.resetMs ?? 2600)
        return r
      } catch (e) {
        const msg = (e as Error).message || String(e)
        errRef.current = msg
        setError(msg)
        setStatus('error')
        timer.current = setTimeout(() => setStatus('idle'), (opts.resetMs ?? 2600) * 2.5)
        return null
      }
    },
    [opts.resetMs],
  )

  const lastError = useCallback(() => errRef.current, [])
  return { run, status, error, result, lastError, reset: () => setStatus('idle') }
}
