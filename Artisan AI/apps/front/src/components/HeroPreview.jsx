import { Card, CardContent } from './ui/Card'
import SectionTitle from './ui/SectionTitle'
import { Handshake, LineChart } from 'lucide-react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

export default function HeroPreview() {
  const data = [
    { name: 'Jan', sales: 2400 },
    { name: 'Feb', sales: 1398 },
    { name: 'Mar', sales: 2800 },
    { name: 'Apr', sales: 3908 },
  ]

  return (
    <Card className="p-6 bg-slate-900/60 border border-slate-700/60 shadow-2xl text-slate-100">
      <CardContent className="p-0">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Sales */}
          <div>
            <SectionTitle icon={LineChart} title="Trending Sales" />
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={data}
                  margin={{ top: 10, right: 10, left: -10, bottom: 0 }}
                >
                  <defs>
                    <linearGradient id="gradSales" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.95" />
                      <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.75" />
                    </linearGradient>
                  </defs>

                  <XAxis
                    dataKey="name"
                    tick={{ fill: '#cbd5e1', fontSize: 12 }}
                    axisLine={{ stroke: '#334155' }}
                    tickLine={{ stroke: '#334155' }}
                  />
                  <YAxis
                    tick={{ fill: '#cbd5e1', fontSize: 12 }}
                    axisLine={{ stroke: '#334155' }}
                    tickLine={{ stroke: '#334155' }}
                  />
                  <Tooltip
                    wrapperStyle={{ outline: 'none' }}
                    contentStyle={{
                      background: '#0f172a',
                      border: '1px solid #334155',
                      borderRadius: '0.75rem',
                      color: '#e2e8f0',
                    }}
                    labelStyle={{ color: '#94a3b8' }}
                    itemStyle={{ color: '#e2e8f0' }}
                    cursor={{ fill: 'rgba(148,163,184,0.15)' }}
                  />
                  <Bar dataKey="sales" fill="url(#gradSales)" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Matches */}
          <div>
            <SectionTitle icon={Handshake} title="Collaboration Matches" />
            <div className="space-y-3">
              {['Textile × Pottery', 'Metalwork × Wood', 'Embroidery × Jewelry'].map((s) => (
                <div
                  key={s}
                  className="flex items-center justify-between rounded-xl px-3 py-2 bg-slate-800/70 border border-slate-700"
                >
                  <span className="text-slate-200">{s}</span>
                  <button
                    className="px-3 py-1 text-sm rounded-lg border border-sky-500/30 bg-sky-600/20 text-sky-300 hover:bg-sky-600/30 transition-colors"
                  >
                    View
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
