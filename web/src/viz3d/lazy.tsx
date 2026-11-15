// Lazy entry points so three.js stays out of the main bundle.
import { lazy, Suspense, useState } from 'react'
import { ErrorBoundary } from '../components/ErrorBoundary'
import { cx } from '../lib/format'

export const LatticeViewer = lazy(() => import('./index').then((m) => ({ default: m.LatticeViewer })))
export const CityViewer = lazy(() => import('./index').then((m) => ({ default: m.CityViewer })))
export const SnakeViewer = lazy(() => import('./index').then((m) => ({ default: m.SnakeViewer })))
export const OrbitsViewer = lazy(() => import('./index').then((m) => ({ default: m.OrbitsViewer })))
export const NeutronStarViewer = lazy(() => import('./neutronstar').then((m) => ({ default: m.NeutronStarViewer })))
export const BlackHoleViewer = lazy(() => import('./blackhole').then((m) => ({ default: m.BlackHoleViewer })))

/** Positioned box that hosts a viewer (viewers fill their parent). */
export function ViewerFrame({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cx('relative overflow-hidden rounded-lg border border-white/[0.07] bg-ink-850', className)}>
      <Suspense fallback={<div className="absolute inset-0 skeleton" />}>{children}</Suspense>
    </div>
  )
}

/** 2D / 3D switch for artifacts that have both views. */
export function DimSwitch({ flat, solid }: { flat: React.ReactNode; solid: React.ReactNode }) {
  const [mode, setMode] = useState<'2d' | '3d'>('2d')
  return (
    <div>
      <div className="mb-3 inline-flex rounded-lg border border-white/10 bg-white/[0.03] p-0.5" role="tablist" aria-label="View">
        {(['2d', '3d'] as const).map((m) => (
          <button
            key={m}
            type="button"
            role="tab"
            aria-selected={mode === m}
            onClick={() => setMode(m)}
            className={cx('h-7 rounded-md px-3 text-[12px] font-medium transition-colors', mode === m ? 'bg-white/[0.09] text-fg' : 'text-fg-muted hover:text-fg')}
          >
            {m === '2d' ? '2D map' : 'Interactive 3D'}
          </button>
        ))}
      </div>
      {mode === '2d' ? flat : solid}
    </div>
  )
}

/** Error boundary + Suspense around a lazy viewer: a failed chunk load (e.g. a stale deploy) shows the fallback
 * instead of taking the page down. */
export function SafeLazy({ fallback, children }: { fallback: React.ReactNode; children: React.ReactNode }) {
  return (
    <ErrorBoundary fallback={fallback}>
      <Suspense fallback={fallback}>{children}</Suspense>
    </ErrorBoundary>
  )
}
