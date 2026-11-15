import { AnimatePresence, motion } from 'framer-motion'
import { lazy, Suspense, useEffect } from 'react'
import { BrowserRouter, HashRouter, NavLink, Route, Routes, useLocation } from 'react-router-dom'
import { ConnectionBadge, LoopPill } from './components/LoopStatus'
import { IconBook, IconDecisions, IconGallery, IconLearn, IconMemory, IconMission } from './components/icons'
import { ToastProvider } from './components/Toast'
import { Skeleton } from './components/ui'
import { cx, dateTime, problemColor, shortName } from './lib/format'
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

export function LogoMark({ className = 'h-7 w-7' }: { className?: string }) {
  // four-point star (the "astar") cut by a rising diagonal: one accent, no gradients
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <rect x="0.5" y="0.5" width="31" height="31" rx="8" fill="#171B21" stroke="rgba(255,255,255,0.1)" />
      <path d="M16 6.5l2.5 7 7 2.5-7 2.5-2.5 7-2.5-7-7-2.5 7-2.5z" fill="#4FD1E0" />
      <circle cx="16" cy="16" r="2" fill="#171B21" />
    </svg>
  )
}

function Brand() {
  return (
    <NavLink to="/" className="flex items-center gap-2.5">
      <LogoMark className="h-7 w-7 shrink-0" />
      <div className="whitespace-nowrap text-[15px] font-semibold tracking-[-0.02em] text-fg">Phoenixastar</div>
    </NavLink>
  )
}

function ModeBanner() {
  const { state, error } = useLive()
  if (MODE === 'static')
    return (
      <div className="border-b border-white/[0.07] px-4 py-2 text-center text-[12.5px] bg-amber/[0.06] text-amber">
        Replay of a live run{state ? `, snapshot ${dateTime(state.snapshot?.generated_at ?? state.now)}` : ''}. Controls are disabled; every number comes from the recorded run.
      </div>
    )
  if (MODE === 'fixtures')
    return (
      <div className="border-b border-white/[0.07] px-4 py-2 text-center text-[12.5px] bg-violet/[0.07] text-violet">
        Fixture mode (VITE_FIXTURES=1): simulated backend for development. These are not live results.
      </div>
    )
  if (error)
    return (
      <div className="border-b border-white/[0.07] px-4 py-2 text-center text-[12.5px] bg-bad/[0.07] text-bad">
        Backend unreachable ({error}). Retrying every 5 s; start it with <code className="font-mono">python3 -m phoenixastar.server</code>.
      </div>
    )
  return null
}

function Sidebar() {
  const { state } = useLive()
  return (
    <aside className="sticky top-0 hidden h-screen w-[240px] shrink-0 flex-col overflow-y-auto border-r border-white/[0.07] bg-ink-850 px-3 py-4 lg:flex">
      <div className="px-2 py-1">
        <Brand />
      </div>
      <nav className="mt-6 flex flex-col gap-0.5">
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cx(
                'relative flex h-8 items-center gap-2.5 rounded-md px-2 text-[13px] font-medium transition-colors duration-150',
                isActive ? 'bg-white/[0.06] text-fg' : 'text-fg-muted hover:bg-white/[0.03] hover:text-fg',
              )
            }
          >
            {({ isActive }) => (
              <>
                <Icon className={cx('relative h-4 w-4', isActive ? 'text-cyan' : 'text-fg-dim')} />
                <span className="relative">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
      <div className="mt-6">
        <div className="label mb-1.5 px-2">Problems</div>
        <div className="flex flex-col gap-0.5">
          {state?.problems.map((p) => (
            <NavLink
              key={p.slug}
              to={`/problems/${p.slug}`}
              className={({ isActive }) =>
                cx('flex h-7 items-center gap-2.5 truncate rounded-md px-2 text-[12.5px] transition-colors duration-150', isActive ? 'bg-white/[0.06] text-fg' : 'text-fg-muted hover:bg-white/[0.03] hover:text-fg')
              }
            >
              <span className="mx-1 h-2 w-2 shrink-0 rounded-[2px]" style={{ background: problemColor(p.slug), opacity: p.status === 'idle' && !p.beats_record ? 0.45 : 1 }} />
              <span className="truncate">{shortName(p.slug)}</span>
              {p.beats_record && <span className="ml-auto h-1.5 w-1.5 shrink-0 rounded-full bg-amber" title="Record beaten" />}
            </NavLink>
          )) ?? <Skeleton className="h-24" />}
        </div>
      </div>
      <div className="mt-auto flex items-center justify-between px-2 pt-6 text-[11.5px] text-fg-dim">
        <span>Autonomous math lab</span>
        <span className="rounded border border-white/[0.08] px-1.5 py-0.5 font-mono text-[10.5px]">{MODE}</span>
      </div>
    </aside>
  )
}

function TopBar() {
  const { pathname } = useLocation()
  const { state } = useLive()
  const slug = pathname.startsWith('/problems/') ? pathname.slice('/problems/'.length) : null
  const here = slug ? state?.problems.find((p) => p.slug === slug)?.title ?? shortName(slug) : NAV.find((n) => (n.end ? pathname === n.to : pathname.startsWith(n.to)))?.label
  return (
    <div className="sticky top-0 z-30 border-b border-white/[0.07] bg-ink-900/90 backdrop-blur-md">
      <div className="flex h-12 items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
        <div className="lg:hidden">
          <Brand />
        </div>
        <div className="hidden min-w-0 items-center gap-2 text-[13px] lg:flex">
          {slug && (
            <>
              <span className="text-fg-dim">Problems</span>
              <span className="text-ink-400">/</span>
            </>
          )}
          <span className="truncate font-medium text-fg">{here ?? 'Not found'}</span>
        </div>
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
                'flex h-8 shrink-0 items-center gap-1.5 rounded-md px-2.5 text-[12.5px] font-medium',
                isActive ? 'bg-white/[0.07] text-fg' : 'text-fg-muted',
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
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [location.pathname])
  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.16, ease: 'easeOut' }}
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
                  <div className="text-xl font-semibold tracking-tight">Not found</div>
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
        <main className="mx-auto w-full max-w-[1560px] flex-1 px-4 pb-16 pt-6 sm:px-6 lg:px-8">
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
