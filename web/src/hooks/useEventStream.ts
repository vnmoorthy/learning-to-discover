import { useEffect, useRef, useState } from 'react'
import { FIXTURES, STATIC } from '../mode'

export type StreamStatus = 'connecting' | 'live' | 'reconnecting' | 'off'
export const SSE_EVENTS = ['phase', 'decision', 'telemetry', 'record', 'log'] as const
export type SseEventName = (typeof SSE_EVENTS)[number]

/**
 * Subscribes to GET /api/events (SSE) with auto-reconnect and exponential backoff.
 * In fixture mode it subscribes to the in-browser simulator; in static mode it is off.
 */
export function useEventStream(onEvent: (event: SseEventName, data: unknown) => void): { status: StreamStatus; lastEventAt: number | null } {
  const [status, setStatus] = useState<StreamStatus>(STATIC ? 'off' : 'connecting')
  const [lastEventAt, setLastEventAt] = useState<number | null>(null)
  const handler = useRef(onEvent)
  handler.current = onEvent

  useEffect(() => {
    if (STATIC) return
    let disposed = false
    let lastStamp = 0
    const deliver = (ev: SseEventName, data: unknown) => {
      const t = Date.now()
      if (t - lastStamp > 1000) {
        lastStamp = t
        setLastEventAt(t)
      }
      try {
        handler.current(ev, data)
      } catch (e) {
        console.error('event handler failed', ev, e)
      }
    }

    if (FIXTURES) {
      let unsub: (() => void) | null = null
      import('../fixtures/server').then((m) => {
        if (disposed) return
        setStatus('live')
        unsub = m.subscribe((ev, data) => deliver(ev as SseEventName, data))
      })
      return () => {
        disposed = true
        unsub?.()
      }
    }

    let es: EventSource | null = null
    let retry = 0
    let timer: ReturnType<typeof setTimeout> | null = null

    const connect = () => {
      if (disposed) return
      es = new EventSource('/api/events')
      es.onopen = () => {
        retry = 0
        setStatus('live')
      }
      es.onerror = () => {
        es?.close()
        es = null
        if (disposed) return
        setStatus('reconnecting')
        const wait = Math.min(15000, 1000 * 2 ** Math.min(retry, 4))
        retry += 1
        timer = setTimeout(connect, wait)
      }
      for (const name of SSE_EVENTS) {
        es.addEventListener(name, (msg) => {
          const raw = (msg as MessageEvent).data
          let data: unknown = raw
          try {
            data = JSON.parse(raw)
          } catch {
            /* keep raw string */
          }
          deliver(name, data)
        })
      }
      // Some servers send unnamed events shaped {event|type, data}.
      es.onmessage = (msg) => {
        try {
          const obj = JSON.parse(msg.data)
          const name = obj?.event ?? obj?.type
          if (SSE_EVENTS.includes(name)) deliver(name, obj.data ?? obj)
        } catch {
          /* ignore keepalives */
        }
      }
    }
    connect()
    return () => {
      disposed = true
      if (timer) clearTimeout(timer)
      es?.close()
    }
  }, [])

  return { status, lastEventAt }
}
