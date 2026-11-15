import { Area, AreaChart, CartesianGrid, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { clockTime, fmtScore } from '../lib/format'
import type { Series } from '../live'

export const axisProps = {
  stroke: 'rgba(255,255,255,0.12)',
  tick: { fill: '#7A838F', fontSize: 10.5, fontFamily: 'JetBrains Mono, monospace' },
  tickLine: false,
  axisLine: { stroke: 'rgba(255,255,255,0.08)' },
}

export const tooltipStyle = {
  contentStyle: { background: 'rgba(10,12,16,0.95)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, fontSize: 12, fontFamily: 'JetBrains Mono, monospace' },
  labelStyle: { color: '#9BA3AF' },
  itemStyle: { color: '#E7E9EC' },
  cursor: { stroke: 'rgba(79,209,224,0.3)' },
}

export function MetricChart({ data, color, name, target, height = 220 }: { data: Series; color: string; name: string; target?: number | null; height?: number }) {
  const rows = data.map(([t, v]) => ({ t, v }))
  const gid = 'mc' + color.replace('#', '')
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={rows} margin={{ top: 8, right: 20, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id={gid} x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.35} />
              <stop offset="100%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="rgba(255,255,255,0.04)" vertical={false} />
          <XAxis dataKey="t" type="number" scale="time" domain={['dataMin', 'dataMax']} tickFormatter={(t) => clockTime(new Date(t).toISOString()).slice(0, 5)} {...axisProps} minTickGap={40} />
          <YAxis domain={['auto', 'auto']} tickFormatter={(v) => fmtScore(v)} width={64} {...axisProps} />
          <Tooltip {...tooltipStyle} labelFormatter={(t) => new Date(t as number).toLocaleString()} formatter={(v: number) => [fmtScore(v), name]} />
          {target != null && <ReferenceLine y={target} stroke="#E2B25C" strokeDasharray="4 4" label={{ value: 'target', fill: '#E2B25C', fontSize: 10, position: 'insideTopRight' }} />}
          <Area type="monotone" dataKey="v" stroke={color} strokeWidth={2} fill={`url(#${gid})`} isAnimationActive={false} dot={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
