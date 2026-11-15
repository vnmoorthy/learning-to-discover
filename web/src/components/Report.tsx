// A verified study rendered as a report: figures with captions and classification, expandable research cycles,
// a tests badge and links to the paper and notebook. Used by the Physics page and by "report" problem artifacts.
import { useState } from 'react'
import { assetUrl } from '../mode'
import type { EHCycle, EHFigure, ReportArtifact } from '../types'
import { IconChevron, IconExternal } from './icons'
import { cx } from '../lib/format'
import { BlackHoleViewer, SafeLazy } from '../viz3d/lazy'

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

function VerificationBlock({ v }: { v: unknown }) {
  if (!v || typeof v !== 'object' || Array.isArray(v)) return null
  const o = v as Record<string, unknown>
  const num = (x: unknown) => (typeof x === 'number' && Number.isFinite(x) ? x : null)
  const checked = num(o.claims_checked)
  const agree = num(o.agree)
  const disagree = num(o.disagree)
  const notes = Object.entries(o).filter(([, x]) => typeof x === 'string' && x)
  if (checked == null && agree == null && disagree == null && !notes.length) return null
  return (
    <div className="mt-2 max-w-4xl rounded-lg border border-white/[0.07] bg-white/[0.02] px-3 py-2 text-[12.5px] leading-5 text-fg-dim">
      {(checked != null || agree != null) && (
        <div>
          <span className="text-fg-muted">Independent verifier:</span> {agree ?? '?'}/{checked ?? '?'} claims agree
          {disagree != null && <>; {disagree} corrected</>}
        </div>
      )}
      {notes.map(([k, x]) => (
        <div key={k} className="mt-1">
          <span className="text-fg-muted">{k.replace(/_/g, ' ')}:</span> {String(x)}
        </div>
      ))}
    </div>
  )
}

export function FigureGrid({ figures }: { figures: EHFigure[] }) {
  if (!figures.length) return null
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {figures.map((f, i) => (
        <figure key={i} className="flex flex-col overflow-hidden rounded-lg border border-white/[0.07] bg-ink-850">
          <a href={assetUrl(f.src ?? '')} target="_blank" rel="noreferrer" title="Open full size in a new tab" className="block cursor-zoom-in bg-black/20">
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

function ReportHero({ art }: { art: ReportArtifact }) {
  const [mode, setMode] = useState<'live' | 'still'>(art.interactive === 'blackhole' ? 'live' : 'still')
  const still = <img src={assetUrl(art.hero!)} alt={art.title ?? 'hero'} className="absolute inset-0 h-full w-full object-cover" />
  return (
    <figure className="overflow-hidden rounded-xl border border-white/[0.07] bg-[#050608]">
      {art.interactive === 'blackhole' && (
        <div className="flex items-center justify-between gap-3 border-b border-white/[0.06] px-3 py-2">
          <div className="inline-flex rounded-lg border border-white/10 bg-white/[0.03] p-0.5" role="tablist" aria-label="Black hole view">
            {(['live', 'still'] as const).map((m) => (
              <button
                key={m}
                type="button"
                role="tab"
                aria-selected={mode === m}
                onClick={() => setMode(m)}
                className={cx('h-7 whitespace-nowrap rounded-md px-3 text-[12px] font-medium transition-colors', mode === m ? 'bg-white/[0.09] text-fg' : 'text-fg-muted hover:text-fg')}
              >
                {m === 'live' ? (
                  <><span className="sm:hidden">Live</span><span className="hidden sm:inline">Interactive (live ray tracing)</span></>
                ) : (
                  <><span className="sm:hidden">A100 still</span><span className="hidden sm:inline">A100 render (24M rays)</span></>
                )}
              </button>
            ))}
          </div>
          <span className="hidden text-[11px] text-fg-dim sm:inline">Same physics in both: Schwarzschild null geodesics</span>
        </div>
      )}
      {mode === 'live' ? (
        <div className="relative h-[360px] w-full sm:h-[520px]">
          <SafeLazy fallback={still}>
            <BlackHoleViewer fallback={still} />
          </SafeLazy>
        </div>
      ) : (
        <img src={assetUrl(art.hero!)} alt={art.title ?? 'hero'} className="w-full object-cover" />
      )}
      <figcaption className="px-4 py-2 text-[11.5px] leading-5 text-fg-dim">
        {mode === 'live'
          ? 'Ray-traced live in your browser, one light ray per pixel per frame, with the same equations as the A100 render: drag to orbit (go below the disk too); click the view, then scroll to zoom in to the photon ring (or pinch on a touch screen or trackpad); tap to pause the gas. Toggle lensing off to see the disk as it would look in flat spacetime.'
          : art.hero_caption}
      </figcaption>
    </figure>
  )
}

export function ReportView({ art }: { art: ReportArtifact }) {
  return (
    <div className="space-y-6">
      {art.hero && <ReportHero art={art} />}
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
        <VerificationBlock v={art.verification} />
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
