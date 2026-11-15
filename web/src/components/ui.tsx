import { animate, motion, useMotionValue, useTransform } from 'framer-motion'
import { useEffect } from 'react'
import { READ_ONLY } from '../mode'
import type { ActionStatus } from '../hooks/useApi'
import { cx, STATUS_STYLE } from '../lib/format'

export function Panel({
  title,
  subtitle,
  right,
  children,
  className,
  bodyClass,
}: {
  title?: React.ReactNode
  subtitle?: React.ReactNode
  right?: React.ReactNode
  children: React.ReactNode
  className?: string
  bodyClass?: string
}) {
  return (
    <section className={cx('panel relative overflow-hidden rounded-xl', className)}>
      {(title || right) && (
        <header className="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.07] px-4 py-3 sm:px-5">
          <div className="min-w-0">
            {title && <h2 className="text-[14px] font-semibold leading-5 tracking-[-0.01em] text-fg">{title}</h2>}
            {subtitle && <p className="mt-0.5 text-[12.5px] leading-5 text-fg-muted">{subtitle}</p>}
          </div>
          {right && <div className="flex flex-wrap items-center gap-2">{right}</div>}
        </header>
      )}
      <div className={cx('p-4 sm:p-5', bodyClass)}>{children}</div>
    </section>
  )
}

export function Spinner({ className }: { className?: string }) {
  return (
    <svg className={cx('h-4 w-4 animate-spin', className)} viewBox="0 0 24 24" fill="none" aria-hidden>
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeOpacity="0.25" strokeWidth="3" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  )
}

const BTN = {
  primary: 'bg-cyan text-ink-900 hover:bg-[#6FDCE8] border border-transparent',
  ghost: 'border border-white/10 bg-white/[0.03] text-fg hover:border-white/20 hover:bg-white/[0.06]',
  danger: 'border border-bad/30 bg-bad/[0.08] text-bad hover:bg-bad/[0.14]',
  amber: 'border border-amber/30 bg-amber/[0.1] text-amber hover:bg-amber/[0.16]',
}

/**
 * Button for mutating API calls: shows loading, success and error states inline.
 * Disabled in static replay mode.
 */
export function ActionButton({
  onClick,
  status = 'idle',
  error,
  children,
  variant = 'ghost',
  size = 'md',
  disabled,
  className,
  successLabel = 'Done',
  title,
  mutating = true,
  type = 'button',
}: {
  onClick?: () => void
  status?: ActionStatus
  error?: string | null
  children: React.ReactNode
  variant?: keyof typeof BTN
  size?: 'sm' | 'md'
  disabled?: boolean
  className?: string
  successLabel?: string
  title?: string
  mutating?: boolean
  type?: 'button' | 'submit'
}) {
  const replay = mutating && READ_ONLY
  const isDisabled = disabled || replay || status === 'loading'
  return (
    <span className="relative inline-flex flex-col items-start">
      <button
        type={type}
        onClick={onClick}
        disabled={isDisabled}
        title={replay ? 'Disabled in replay mode' : error ?? title}
        className={cx(
          'inline-flex select-none items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-45',
          size === 'sm' ? 'h-8 px-3 text-[12.5px]' : 'h-9 px-3.5 text-[13px]',
          status === 'error' ? BTN.danger : status === 'success' ? 'border border-good/30 bg-good/[0.08] text-good' : BTN[variant],
          className,
        )}
      >
        {status === 'loading' && <Spinner className="h-3.5 w-3.5" />}
        {status === 'success' && <CheckIcon />}
        {status === 'error' && <span aria-hidden>!</span>}
        <span className="inline-flex items-center gap-1.5">{status === 'success' ? successLabel : status === 'error' ? 'Failed' : children}</span>
      </button>
      {status === 'error' && error && (
        <span className="absolute left-0 top-full z-20 mt-1 w-max max-w-[280px] rounded-md border border-bad/30 bg-ink-700 px-2 py-1 font-mono text-[11px] leading-snug text-bad shadow-pop">
          {error}
        </span>
      )}
    </span>
  )
}

export function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={cx('h-3.5 w-3.5', className)} viewBox="0 0 16 16" fill="none" aria-hidden>
      <path d="M3 8.5l3 3 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function StatusBadge({ status }: { status: string }) {
  const s = STATUS_STYLE[status] ?? STATUS_STYLE.idle
  return (
    <span className={cx('inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-full border px-2 py-0.5 text-[11px] font-medium leading-4', s.cls)}>
      <span className={cx('h-1.5 w-1.5 rounded-full', s.dot)} />
      {s.label}
    </span>
  )
}

export function Chip({ children, color, className, title }: { children: React.ReactNode; color?: string; className?: string; title?: string }) {
  return (
    <span
      title={title}
      className={cx('inline-flex max-w-full items-center gap-1.5 truncate rounded-md border border-white/[0.08] px-1.5 py-0.5 font-mono text-[10.5px]', className)}
      style={color ? { color, borderColor: color + '33', background: color + '0F' } : undefined}
    >
      {children}
    </span>
  )
}

export function Dot({ color, pulse }: { color: string; pulse?: boolean }) {
  return <span className={cx('inline-block h-2 w-2 shrink-0 rounded-full', pulse && 'animate-pulseDot')} style={{ background: color }} />
}

export function Verdict({ verdict }: { verdict: string | undefined | null }) {
  if (!verdict) return null
  const map: Record<string, string> = {
    confirmed: 'text-good border-good/30 bg-good/[0.08]',
    refuted: 'text-bad border-bad/30 bg-bad/[0.08]',
    pending: 'text-amber border-amber/30 bg-amber/[0.08]',
    'n/a': 'text-fg-dim border-white/[0.08] bg-transparent',
  }
  return <span className={cx('whitespace-nowrap rounded-full border px-2 py-0.5 text-[11px] font-medium capitalize leading-4', map[verdict] ?? map['n/a'])}>{verdict}</span>
}

export function ErrorNote({ error, onRetry }: { error: string; onRetry?: () => void }) {
  return (
    <div className="flex flex-wrap items-center gap-3 rounded-xl border border-bad/25 bg-bad/[0.06] px-4 py-3 text-sm text-bad">
      <span className="font-mono text-xs">{error}</span>
      {onRetry && (
        <button onClick={onRetry} className="rounded-md border border-bad/40 px-2 py-0.5 text-xs hover:bg-bad/10">
          Retry
        </button>
      )}
    </div>
  )
}

export function Empty({ children }: { children: React.ReactNode }) {
  return <div className="rounded-xl border border-dashed border-white/10 px-4 py-10 text-center text-[13px] text-fg-dim">{children}</div>
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cx('skeleton rounded-lg', className)} />
}

/** Number that animates to its new value. */
export function Counter({ value, format = (v) => Math.round(v).toLocaleString('en-US'), className }: { value: number; format?: (v: number) => string; className?: string }) {
  const mv = useMotionValue(value)
  const text = useTransform(mv, (v) => format(v))
  useEffect(() => {
    const c = animate(mv, value, { duration: 0.8, ease: 'easeOut' })
    return () => c.stop()
  }, [value, mv])
  return <motion.span className={cx('tabular-nums', className)}>{text}</motion.span>
}

/** Tiny dependency-free sparkline. */
export function Sparkline({
  data,
  color = '#4FD1E0',
  height = 36,
  className,
  target,
}: {
  data: [number, number][]
  color?: string
  height?: number
  className?: string
  target?: number | null
}) {
  const w = 200
  const h = height
  if (data.length < 2) {
    return (
      <svg viewBox={`0 0 ${w} ${h}`} className={cx('w-full', className)} style={{ height: h }} preserveAspectRatio="none">
        <line x1="0" x2={w} y1={h / 2} y2={h / 2} stroke="#ffffff14" strokeDasharray="3 4" />
      </svg>
    )
  }
  const xs = data.map((d) => d[0])
  const ys = data.map((d) => d[1])
  const x0 = Math.min(...xs)
  const x1 = Math.max(...xs)
  let y0 = Math.min(...ys)
  let y1 = Math.max(...ys)
  if (y1 - y0 < 1e-12) {
    y0 -= 1
    y1 += 1
  }
  const px = (x: number) => ((x - x0) / (x1 - x0 || 1)) * w
  const py = (y: number) => h - 3 - ((y - y0) / (y1 - y0)) * (h - 6)
  const path = data.map((d, i) => `${i ? 'L' : 'M'}${px(d[0]).toFixed(1)},${py(d[1]).toFixed(1)}`).join('')
  const id = 'sg' + color.replace('#', '')
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className={cx('w-full overflow-visible', className)} style={{ height: h }} preserveAspectRatio="none">
      <defs>
        <linearGradient id={id} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.14" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      {target != null && target >= y0 && target <= y1 && (
        <line x1="0" x2={w} y1={py(target)} y2={py(target)} stroke="#E2B25C" strokeOpacity="0.5" strokeDasharray="2 3" vectorEffect="non-scaling-stroke" />
      )}
      <path d={`${path}L${w},${h}L0,${h}Z`} fill={`url(#${id})`} />
      <path d={path} fill="none" stroke={color} strokeWidth="1.5" vectorEffect="non-scaling-stroke" strokeLinejoin="round" />
      
    </svg>
  )
}

export function Stat({ label, value, sub, accent }: { label: string; value: React.ReactNode; sub?: React.ReactNode; accent?: string }) {
  return (
    <div className="min-w-0">
      <div className="label">{label}</div>
      <div className="mt-1 truncate font-mono text-[19px] font-medium tracking-tight tabular-nums" style={accent ? { color: accent } : undefined}>
        {value}
      </div>
      {sub && <div className="mt-0.5 truncate text-[11px] text-fg-muted">{sub}</div>}
    </div>
  )
}

export function Select({
  value,
  onChange,
  options,
  label,
  className,
}: {
  value: string
  onChange: (v: string) => void
  options: { value: string; label: string }[]
  label?: string
  className?: string
}) {
  return (
    <label className={cx('inline-flex items-center gap-2 text-xs text-fg-muted', className)}>
      {label && <span>{label}</span>}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="h-8 max-w-[220px] rounded-lg border border-white/10 bg-ink-700 px-2 text-[12.5px] text-fg outline-none transition-colors hover:border-white/20 focus:border-cyan/60"
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  )
}
