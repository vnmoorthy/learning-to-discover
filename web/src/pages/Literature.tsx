import { motion } from 'framer-motion'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { IconExternal } from '../components/icons'
import { Empty, ErrorNote, Panel, Select, Skeleton } from '../components/ui'
import { useApi } from '../hooks/useApi'
import { problemColor, safeHref, shortName } from '../lib/format'
import { useLive } from '../live'
import type { LiteratureItem } from '../types'

function host(url: string) {
  try {
    return new URL(url).hostname.replace(/^www\./, '')
  } catch {
    return url
  }
}

export default function LiteraturePage() {
  const { state } = useLive()
  const [problem, setProblem] = useState('')
  const lit = useApi(() => api.literature(problem || null), [problem], 30000)

  const groups = useMemo(() => {
    const g = new Map<string, LiteratureItem[]>()
    for (const l of lit.data ?? []) {
      const arr = g.get(l.problem) ?? []
      arr.push(l)
      g.set(l.problem, arr)
    }
    for (const arr of g.values()) arr.sort((a, b) => b.cited_by.length - a.cited_by.length || b.id - a.id)
    return [...g.entries()].sort((a, b) => b[1].length - a[1].length)
  }, [lit.data])

  const total = lit.data?.length ?? 0
  const cited = lit.data?.filter((l) => l.cited_by.length > 0).length ?? 0

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight">Literature</h1>
          <p className="mt-1 max-w-3xl text-sm text-fg-muted">
            Sources found by Exa inside the main loop. The proposer writes the queries when a problem is new or stalls; cited sources are linked to the decisions that used them.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <span className="font-mono text-[11px] text-fg-muted">
            <span className="text-fg">{total}</span> sources | <span className="text-[#CDB866]">{cited}</span> cited
          </span>
          <Select
            label="problem"
            value={problem}
            onChange={setProblem}
            options={[{ value: '', label: 'all problems' }, ...(state?.problems.map((p) => ({ value: p.slug, label: p.slug })) ?? [])]}
          />
        </div>
      </div>
      {lit.error && !lit.data && <ErrorNote error={lit.error} onRetry={lit.reload} />}
      {lit.loading && !lit.data ? (
        <Skeleton className="h-96" />
      ) : groups.length === 0 ? (
        <Empty>No sources yet. The literature agent runs when a problem is new or stalled.</Empty>
      ) : (
        groups.map(([slug, items]) => (
          <Panel
            key={slug}
            title={
              <span className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full" style={{ background: problemColor(slug), boxShadow: `0 0 8px ${problemColor(slug)}` }} />
                {shortName(slug)}
              </span>
            }
            subtitle={`${items.length} source(s)`}
            right={
              <Link to={`/problems/${slug}`} className="text-xs text-cyan hover:underline">
                Problem
              </Link>
            }
          >
            <div className="grid gap-3 lg:grid-cols-2">
              {items.map((l, i) => (
                <motion.article
                  key={l.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(i, 8) * 0.03 }}
                  className="flex flex-col rounded-xl border border-white/[0.06] bg-white/[0.015] p-4"
                >
                  <a href={safeHref(l.url)} target="_blank" rel="noopener noreferrer" className="group inline-flex items-start gap-1.5 text-[13.5px] font-semibold leading-snug text-fg hover:text-cyan">
                    <span>{l.title}</span>
                    <IconExternal className="mt-1 h-3 w-3 shrink-0 text-fg-dim group-hover:text-cyan" />
                  </a>
                  <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-[10.5px] text-fg-dim">
                    <span>{host(l.url)}</span>
                    <span>{l.published ? `published ${l.published.slice(0, 10)}` : 'no publish date'}</span>
                    <span>#{l.id}</span>
                  </div>
                  {l.highlight && <p className="mt-2.5 border-l-2 border-[#CDB866]/40 pl-3 text-[12.5px] leading-relaxed text-fg-muted">{l.highlight}</p>}
                  <div className="mt-auto pt-3">
                    <div className="truncate font-mono text-[10.5px] text-fg-dim" title={l.query}>
                      query: <span className="text-fg-muted">{l.query}</span>
                    </div>
                    <div className="mt-1.5 flex flex-wrap items-center gap-1.5 text-[10.5px] text-fg-dim">
                      {l.cited_by.length ? (
                        <>
                          cited by
                          {l.cited_by.map((id) => (
                            <Link key={id} to={`/decisions?focus=${id}`} className="rounded border border-[#CDB866]/30 bg-[#CDB866]/10 px-1.5 py-0.5 font-mono text-[#CDB866] hover:bg-[#CDB866]/20">
                              decision #{id}
                            </Link>
                          ))}
                        </>
                      ) : (
                        <span>not cited yet</span>
                      )}
                    </div>
                  </div>
                </motion.article>
              ))}
            </div>
          </Panel>
        ))
      )}
    </div>
  )
}
