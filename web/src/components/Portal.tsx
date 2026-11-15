import { createPortal } from 'react-dom'

/** Renders children into document.body so fixed overlays escape transformed / backdrop-filtered ancestors. */
export function Portal({ children }: { children: React.ReactNode }) {
  if (typeof document === 'undefined') return null
  return createPortal(children, document.body)
}
