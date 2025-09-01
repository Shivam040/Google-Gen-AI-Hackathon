// front/src/components/artisan/Insights.jsx
import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Bar, BarChart } from 'recharts'

const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export default function Insights() {
  // Mocked charts for now (replace later with real analytics/BigQuery)
  const [sales] = useState([
    { month: 'May', value: 120 },
    { month: 'Jun', value: 180 },
    { month: 'Jul', value: 260 },
    { month: 'Aug', value: 220 },
    { month: 'Sep', value: 310 },
  ])
  const [feedback] = useState([
    { day: 'Mon', score: 4.1 },
    { day: 'Tue', score: 4.4 },
    { day: 'Wed', score: 4.6 },
    { day: 'Thu', score: 4.3 },
    { day: 'Fri', score: 4.7 },
  ])

  // Product performance from backend
  const [perf, setPerf] = useState([])
  const [err, setErr] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancel = false
    ;(async () => {
      setLoading(true); setErr('')
      try {
        const res = await fetch(`${BASE}/v1/recs/popular?limit=6`)
        const txt = await res.text()
        const isJSON = (res.headers.get('content-type') || '').includes('application/json')
        const body = isJSON && txt ? JSON.parse(txt) : {}

        if (!res.ok) throw new Error(body?.detail || `${res.status} ${res.statusText}`)

        const items = (body.items || []).map(p => ({
          id: p.id,
          title: p.title || 'Untitled',
          // Use whatever you have as quick health signals
          stat: `Popularity ${p.popularity ?? 0} • Stock ${p.inventory ?? 0}`,
        }))
        if (!cancel) setPerf(items)
      } catch (e) {
        if (!cancel) {
          setErr(e.message || 'Failed to load product performance')
          // Fallback showcase
          setPerf([
            { id: 'p1', title: 'Pottery Vase', stat: 'Popularity 11 • Stock 1' },
            { id: 'p2', title: 'Embroidered Stole', stat: 'Popularity 2 • Stock 5' },
            { id: 'p3', title: 'Brass Anklet', stat: 'Popularity 7 • Stock 3' },
          ])
        }
      } finally {
        if (!cancel) setLoading(false)
      }
    })()
    return () => { cancel = true }
  }, [])

  return (
    <div className="grid lg:grid-cols-3 gap-6 text-slate-100">
      {/* Sales Trends */}
      <Card className="lg:col-span-2 bg-slate-900/60 border border-slate-700/60 shadow-xl">
        <CardHeader>
          <CardTitle>Sales Trends</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sales} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="gradLine" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#38bdf8" />
                  <stop offset="100%" stopColor="#22d3ee" />
                </linearGradient>
              </defs>
              <XAxis dataKey="month" tick={{ fill: '#cbd5e1', fontSize: 12 }} axisLine={{ stroke: '#334155' }} tickLine={{ stroke: '#334155' }} />
              <YAxis tick={{ fill: '#cbd5e1', fontSize: 12 }} axisLine={{ stroke: '#334155' }} tickLine={{ stroke: '#334155' }} />
              <Tooltip
                wrapperStyle={{ outline: 'none' }}
                contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '0.75rem', color: '#e2e8f0' }}
                labelStyle={{ color: '#94a3b8' }}
                itemStyle={{ color: '#e2e8f0' }}
                cursor={{ stroke: 'rgba(148,163,184,0.25)', strokeWidth: 30 }}
              />
              <Line type="monotone" dataKey="value" stroke="url(#gradLine)" strokeWidth={3} dot={{ r: 3, stroke: '#22d3ee', fill: '#0f172a' }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Feedback */}
      <Card className="bg-slate-900/60 border border-slate-700/60 shadow-xl">
        <CardHeader>
          <CardTitle>Customer Feedback (avg)</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={feedback} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="gradBar" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.95" />
                  <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.75" />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" tick={{ fill: '#cbd5e1', fontSize: 12 }} axisLine={{ stroke: '#334155' }} tickLine={{ stroke: '#334155' }} />
              <YAxis domain={[0, 5]} tick={{ fill: '#cbd5e1', fontSize: 12 }} axisLine={{ stroke: '#334155' }} tickLine={{ stroke: '#334155' }} />
              <Tooltip
                wrapperStyle={{ outline: 'none' }}
                contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '0.75rem', color: '#e2e8f0' }}
                labelStyle={{ color: '#94a3b8' }}
                itemStyle={{ color: '#e2e8f0' }}
                cursor={{ fill: 'rgba(148,163,184,0.15)' }}
              />
              <Bar dataKey="score" fill="url(#gradBar)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Product Performance */}
      <Card className="lg:col-span-3 bg-slate-900/60 border border-slate-700/60 shadow-xl">
        <CardHeader>
          <CardTitle>
            Product Performance {loading ? <span className="text-xs text-slate-400">• loading…</span> : null}
            {err ? <span className="ml-2 text-xs text-rose-400">{err}</span> : null}
          </CardTitle>
        </CardHeader>
        <CardContent className="grid md:grid-cols-3 gap-4">
          {perf.map((p) => (
            <div key={p.id || p.title} className="rounded-xl border border-slate-700 bg-slate-800/60 p-4 space-y-2">
              <div className="font-medium text-slate-100">{p.title}</div>
              <div className="text-sm text-slate-400">{p.stat}</div>
              <Button className="rounded-lg bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400">
                Boost
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}



