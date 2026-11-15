// A verified study rendered as a report: figures with captions and classification, expandable research cycles,
// a tests badge and links to the paper and notebook. Used by the Physics page and by "report" problem artifacts.
import { useState } from 'react'
import { assetUrl } from '../mode'
import type { EHCycle, EHFigure, ReportArtifact } from '../types'
import { IconChevron, IconExternal } from './icons'
import { cx } from '../lib/format'

const REPO = 'https://github.com/vnmoorthy/phoenixastar/blob/main/'
const CLASS_LABEL: Record<string, string> = {
  '1': 'reproduction',
  '2': 'verified known relation',
  '3': 'new computational observation',
  '4': 'new conjecture',
  '5': 'potentially novel (needs work)',
}
export function classOf(c: unknown) {
  const k = String(c ?? '').trim().charAt(0)
  return CLASS_LABEL[k] ? `${k} · ${CLASS_LABEL[k]}` : String(c ?? '')
}
function txt(v: unknown): string {
  if (v == null) return ''
  if (typeof v === 'string') return v
  if (Array.isArray(v)) return v.map(txt).join(' · ')
  return JSON.stringify(v)
}

const Badge = ({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'neutral' | 'good' }) => (
  <span
    className={cx(
      'inline-flex shrink-0 items-center gap-1.5 rounded-full border px-2 py-0.5 text-[11px] font-medium leading-4',
      tone === 'good' ? 'border-good/30 bg-good/[0.08] text-good' : 'border-white/10 bg-white/[0.03] text-fg-muted',
    )}
  >
    {children}
  </span>
)

export function TestsBadge({ tests }: { tests?: { passed?: number; failed?: number; total?: number } | null }) {
  if (!tests) return null
  return (
    <Badge tone={tests.failed ? 'neutral' : 'good'}>
      <span className={cx('h-1.5 w-1.5 rounded-full', tests.failed ? 'bg-amber' : 'bg-good')} />
      Tests {tests.passed ?? '?'}/{tests.total ?? '?'} passed
    </Badge>
  )
}

export function Cycle({ c, i }: { c: EHCycle; i: number }) {
  const [open, setOpen] = useState(i === 0)
  const rows: [string, unknown][] = [
    ['Hypothesis', c.hypothesis],
    ['Derivation', c.derivation_summary ?? (c as Record<string, unknown>).derivation],
    ['Prediction', c.prediction],
    ['Result', c.result],
    ['Independent verification', c.verification],
    ['Critic', c.critic_objections],
    ['Revised hypothesis', c.revised_hypothesis],
    ['Conclusion', c.conclusion],
  ]
  return (
    <div className="rounded-lg border border-white/[0.07] bg-white/[0.015]">
      <button onClick={() => setOpen(!open)} aria-expanded={open} className="flex w-full items-start gap-3 px-4 py-3 text-left transition-colors hover:bg-white/[0.02]">
        <IconChevron className={cx('mt-0.5 h-4 w-4 shrink-0 text-fg-dim transition-transform duration-150', open && 'rotate-90')} />
        <div className="min-w-0 flex-1">
          <div className="font-mono text-[11px] text-fg-dim">Cycle {String(c.id ?? i + 1)}</div>
          <div className="mt-0.5 text-[13.5px] leading-5 text-fg">{txt(c.question) || txt(c.hypothesis)}</div>
        </div>
        {c.classification != null && <Badge>{classOf(c.classification)}</Badge>}
      </button>
      {open && (
        <dl className="grid gap-x-4 gap-y-2.5 border-t border-white/[0.07] px-4 py-3 text-[13px] leading-5 sm:grid-cols-[170px_1fr]">
          {rows
            .filter(([, v]) => txt(v))
            .map(([k, v]) => (
              <div key={k} className="contents">
                <dt className="label pt-px">{k}</dt>
                <dd className="whitespace-pre-wrap break-words text-fg-muted">{txt(v)}</dd>
              </div>
            ))}
        </dl>
      )}
    </div>
  )
}

export function FigureGrid({ figures }: { figures: EHFigure[] }) {
  if (!figures.length) return null
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {figures.map((f, i) => (
        <figure key={i} className="flex flex-col overflow-hidden rounded-lg border border-white/[0.07] bg-ink-850">
          <a href={assetUrl(f.src ?? '')} target="_blank" rel="noreferrer" className="block bg-black/20">
            <img src={assetUrl(f.src ?? '')} alt={f.title} className="w-full" loading="lazy" />
          </a>
          <figcaption className="flex flex-1 flex-col gap-1.5 border-t border-white/[0.07] px-3 py-2.5 text-[12.5px] leading-5">
            <div className="font-medium text-fg">{f.title}</div>
            {f.caption && <div className="text-fg-muted">{f.caption}</div>}
            {f.classification != null && (
              <div className="mt-auto pt-1">
                <Badge>{classOf(f.classification)}</Badge>
              </div>
            )}
          </figcaption>
        </figure>
      ))}
    </div>
  )
}

function RepoLink({ path, children }: { path?: string; children: React.ReactNode }) {
  if (!path) return null
  return (
    <a
      href={REPO + path.replace(/^\/+/, '')}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex h-8 items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.03] px-3 text-[12.5px] font-medium text-fg transition-colors hover:border-white/20 hover:bg-white/[0.06]"
    >
      {children}
      <IconExternal className="h-3 w-3 text-fg-dim" />
    </a>
  )
}

export function ReportView({ art }: { art: ReportArtifact }) {
  return (
    <div className="space-y-6">
      <div>
        {art.question && <p className="max-w-4xl text-[14px] font-medium leading-6 text-fg">{art.question}</p>}
        {art.summary && <p className="mt-2 max-w-4xl text-[13.5px] leading-6 text-fg-muted">{art.summary}</p>}
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <TestsBadge tests={art.tests} />
          <RepoLink path={art.paper}>Paper</RepoLink>
          <RepoLink path={art.notebook}>Notebook</RepoLink>
        </div>
        {art.hardware && <p className="mt-3 font-mono text-[11px] text-fg-dim">hardware: {art.hardware}</p>}
        {typeof art.verification === 'string' && art.verification && (
          <p className="mt-2 max-w-4xl text-[12.5px] leading-5 text-fg-dim">
            <span className="text-fg-muted">Verification:</span> {art.verification}
          </p>
        )}
      </div>
      {!!art.figures?.length && (
        <div>
          <div className="label mb-2">Figures</div>
          <FigureGrid figures={art.figures} />
        </div>
      )}
      {!!art.cycles?.length && (
        <div className="space-y-2">
          <div className="label">Research cycles</div>
          {art.cycles.map((c, i) => (
            <Cycle key={i} c={c} i={i} />
          ))}
        </div>
      )}
    </div>
  )
}
