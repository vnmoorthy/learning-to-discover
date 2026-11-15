import { AnimatePresence, motion } from 'framer-motion'
import { lazy, Suspense } from 'react'
import { BrowserRouter, HashRouter, NavLink, Route, Routes, useLocation } from 'react-router-dom'
import { ConnectionBadge, LoopPill } from './components/LoopStatus'
import { IconBook, IconDecisions, IconGallery, IconLearn, IconMemory, IconMission } from './components/icons'
import { ToastProvider } from './components/Toast'
import { Skeleton } from './components/ui'
import { cx, dateTime } from './lib/format'
import { LiveProvider, useLive } from './live'
import { MODE, STATIC } from './mode'
import MissionControl from './pages/MissionControl'

const ProblemPage = lazy(() => import('./pages/Problem'))
const DecisionsPage = lazy(() => import('./pages/Decisions'))
const MemoryPage = lazy(() => import('./pages/Memory'))
const LiteraturePage = lazy(() => import('./pages/Literature'))
const LearningPage = lazy(() => import('./pages/Learning'))
const GalleryPage = lazy(() => import('./pages/Gallery'))
const PhysicsPage = lazy(() => import('./pages/Physics'))

const NAV = [
  { to: '/', label: 'Mission Control', icon: IconMission, end: true },
  { to: '/decisions', label: 'Decisions', icon: IconDecisions },
  { to: '/memory', label: 'Memory', icon: IconMemory },
  { to: '/literature', label: 'Literature', icon: IconBook },
  { to: '/learning', label: 'Self-improvement', icon: IconLearn },
  { to: '/physics', label: 'Physics', icon: IconBook },
  { to: '/gallery', label: 'Gallery', icon: IconGallery },
]

function Brand() {
  return (
    <NavLink to="/" className="group flex items-center gap-2.5">
      <svg viewBox="0 0 32 32" className="h-7 w-7 shrink-0 sm:h-8 sm:w-8" aria-hidden>
        <rect width="32" height="32" rx="9" fill="#0E1116" stroke="rgba(61,245,255,0.25)" />
        <g fill="#3DF5FF">
          <circle cx="9.5" cy="9.5" r="2.1" />
          <circle cx="22.5" cy="12" r="2.1" />
          <circle cx="12.5" cy="22" r="2.1" />
        </g>
        <circle cx="22" cy="22.5" r="2.6" fill="#FFB547" />
      </svg>
      <div className="leading-tight">
        <div className="whitespace-nowrap font-display text-[14px] font-semibold tracking-tight text-fg sm:text-[15px]">Phoenixastar</div>
        <div className="hidden text-[10.5px] text-fg-dim sm:block">autonomous math lab</div>
      </div>
    </NavLink>
  )
}

function ModeBanner() {
  const { state, error } = useLive()
  if (MODE === 'static')
    return (
      <div className="border-b border-amber/25 bg-amber/[0.07] px-4 py-2 text-center text-xs text-amber">
        Replay of a live run{state ? `, snapshot ${dateTime(state.snapshot?.generated_at ?? state.now)}` : ''}. Controls are disabled; every number comes from the recorded run.
      </div>
    )
  if (MODE === 'fixtures')
    return (
      <div className="border-b border-[#A98BFF]/30 bg-[#A98BFF]/[0.08] px-4 py-2 text-center text-xs text-[#C9A8FF]">
        Fixture mode (VITE_FIXTURES=1): simulated backend for development. These are not live results.
      </div>
    )
  if (error)
    return (
      <div className="border-b border-bad/30 bg-bad/[0.08] px-4 py-2 text-center text-xs text-bad">
        Backend unreachable ({error}). Retrying every 5 s; start it with <code className="font-mono">python3 -m ltd.server</code>.
      </div>
    )
  return null
}

function Sidebar() {
  const { state } = useLive()
  return (
    <aside className="sticky top-0 hidden h-screen w-[232px] shrink-0 flex-col border-r border-white/[0.06] bg-ink-900/70 px-4 py-5 backdrop-blur lg:flex">
      <Brand />
      <nav className="mt-8 flex flex-col gap-1">
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cx(
                'relative flex items-center gap-3 rounded-lg px-3 py-2 text-[13px] font-medium transition-colors',
                isActive ? 'text-cyan' : 'text-fg-muted hover:bg-white/[0.03] hover:text-fg',
              )
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.span
                    layoutId="nav-active"
                    className="absolute inset-0 rounded-lg border border-cyan/25 bg-cyan/[0.07]"
                    transition={{ type: 'spring', stiffness: 420, damping: 34 }}
                  />
                )}
                <Icon className="relative h-4 w-4" />
                <span className="relative">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
      <div className="mt-6 border-t border-white/[0.06] pt-4">
        <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-fg-dim">Problems</div>
        <div className="flex flex-col gap-0.5">
          {state?.problems.map((p) => (
            <NavLink
              key={p.slug}
              to={`/problems/${p.slug}`}
              className={({ isActive }) =>
                cx('flex items-center gap-2 truncate rounded-md px-2 py-1 font-mono text-[11px] transition-colors', isActive ? 'bg-white/[0.05] text-fg' : 'text-fg-muted hover:text-fg')
              }
            >
              <span className={cx('h-1.5 w-1.5 shrink-0 rounded-full', p.beats_record ? 'bg-amber' : p.status === 'searching' ? 'bg-cyan animate-pulseDot' : 'bg-fg-dim')} />
              <span className="truncate">{p.slug}</span>
            </NavLink>
          )) ?? <Skeleton className="h-24" />}
        </div>
      </div>
      <div className="mt-auto space-y-1 pt-4 text-[10.5px] leading-relaxed text-fg-dim">
        <div>An AI lab that gets better at discovering mathematics by doing it.</div>
        <div className="font-mono">mode: {MODE}</div>
      </div>
    </aside>
  )
}

function TopBar() {
  return (
    <div className="sticky top-0 z-30 border-b border-white/[0.06] bg-ink-900/80 backdrop-blur-md">
      <div className="flex h-14 items-center justify-between gap-2 px-4 sm:px-6">
        <div className="lg:hidden">
          <Brand />
        </div>
        <div className="hidden lg:block" />
        <div className="flex items-center gap-2">
          <span className="hidden sm:inline-flex">
            <LoopPill />
          </span>
          <span className="sm:hidden">
            <LoopPill compact />
          </span>
          <ConnectionBadge />
        </div>
      </div>
      <nav className="no-scrollbar flex gap-1 overflow-x-auto px-3 pb-2 lg:hidden">
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cx(
                'flex shrink-0 items-center gap-1.5 rounded-lg border px-2.5 py-1.5 text-xs font-medium',
                isActive ? 'border-cyan/30 bg-cyan/[0.08] text-cyan' : 'border-transparent text-fg-muted',
              )
            }
          >
            <Icon className="h-3.5 w-3.5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </div>
  )
}

function PageFallback() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-10 w-72" />
      <Skeleton className="h-64" />
      <Skeleton className="h-40" />
    </div>
  )
}

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.22, ease: [0.2, 0.8, 0.2, 1] }}
      >
        <Suspense fallback={<PageFallback />}>
          <Routes location={location}>
            <Route path="/" element={<MissionControl />} />
            <Route path="/problems/:slug" element={<ProblemPage />} />
            <Route path="/decisions" element={<DecisionsPage />} />
            <Route path="/memory" element={<MemoryPage />} />
            <Route path="/literature" element={<LiteraturePage />} />
            <Route path="/learning" element={<LearningPage />} />
            <Route path="/physics" element={<PhysicsPage />} />
            <Route path="/gallery" element={<GalleryPage />} />
            <Route
              path="*"
              element={
                <div className="py-24 text-center">
                  <div className="font-display text-2xl">Not found</div>
                  <NavLink to="/" className="mt-3 inline-block text-sm text-cyan underline">
                    Back to Mission Control
                  </NavLink>
                </div>
              }
            />
          </Routes>
        </Suspense>
      </motion.div>
    </AnimatePresence>
  )
}

function Shell() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <ModeBanner />
        <TopBar />
        <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 pb-16 pt-5 sm:px-6 lg:px-8">
          <AnimatedRoutes />
        </main>
      </div>
    </div>
  )
}

export default function App() {
  const Router = STATIC ? HashRouter : BrowserRouter
  return (
    <ToastProvider>
      <LiveProvider>
        <Router>
          <Shell />
        </Router>
      </LiveProvider>
    </ToastProvider>
  )
}
