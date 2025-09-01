// front/src/components/artisan/CollaborationHub.jsx
import { useEffect, useMemo, useState } from 'react'
import SectionTitle from '../ui/SectionTitle'
import Button from '../ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Badge from '../ui/Badge'
import { Filter, Handshake, Sparkles } from 'lucide-react'

const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export default function CollaborationHub() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setLoading(true)
      setError('')
      try {
        const res = await fetch(`${BASE}/v1/recs/popular?limit=6`, {
          headers: { 'content-type': 'application/json' },
        })
        const txt = await res.text()
        const isJSON = (res.headers.get('content-type') || '').includes('application/json')
        const body = isJSON && txt ? JSON.parse(txt) : {}
        if (!res.ok) throw new Error(body?.detail || `${res.status} ${res.statusText}`)

        if (!cancelled) {
          // Map products -> “collab cards”
          const mapped =
            (body.items || []).map((p) => ({
              key: p.id || p.title,
              name: `${p.title ?? 'Untitled'} (${p.category ?? 'craft'})`,
              themes:
                Array.isArray(p.materials) && p.materials.length
                  ? p.materials
                  : [p.category].filter(Boolean),
              portfolio: p.popularity ?? p.inventory ?? 0,
              raw: p,
            })) ?? []
          setItems(mapped)
        }
      } catch (e) {
        if (!cancelled) {
          setError(e?.message || 'Failed to load suggestions')
          // Fallback to your previous static seed
          setItems([
            { key: 'Meera', name: 'Meera (Textiles)', themes: ['Traditional', 'Heritage'], portfolio: 24 },
            { key: 'Arun', name: 'Arun (Pottery)', themes: ['Modern', 'Fusion'], portfolio: 18 },
            { key: 'Lata', name: 'Lata (Jewelry)', themes: ['Festival', 'Luxury'], portfolio: 31 },
          ])
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  const headerRight = useMemo(
    () => (
      <div className="flex items-center gap-2">
        {error ? (
          <span className="text-xs text-rose-400/90">{error}</span>
        ) : null}
        <Button
          variant="outline"
          className="rounded-xl border-slate-700 text-slate-200 hover:bg-slate-800/50 hover:border-sky-500/50"
          onClick={() => window.location.reload()}
          title="Refresh suggestions"
        >
          <Filter className="h-4 w-4 mr-1" />
          Refresh
        </Button>
      </div>
    ),
    [error]
  )

  return (
    <div className="grid lg:grid-cols-3 gap-6 text-slate-100">
      {/* Left: list */}
      <div className="lg:col-span-2 space-y-4">
        <SectionTitle title="Browse Artisans" right={headerRight} />

        {loading ? (
          <div className="text-sm text-slate-400 px-1">Loading suggestions…</div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {items.map((a) => (
              <Card
                key={a.key || a.name}
                className="bg-slate-900/60 border border-slate-700/60 shadow-xl"
              >
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="text-slate-100">{a.name}</span>
                    <Badge className="bg-sky-600/20 text-sky-300 border border-sky-500/30">
                      {a.portfolio} items
                    </Badge>
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex gap-2 flex-wrap">
                    {(a.themes || []).map((t) => (
                      <Badge
                        key={t}
                        className="bg-slate-800/70 border border-slate-700 text-slate-300"
                      >
                        {t}
                      </Badge>
                    ))}
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    <Button
                      size="sm"
                      variant="outline"
                      className="rounded-lg border-slate-700 text-slate-200 hover:bg-slate-800/60 hover:border-sky-500/50"
                      onClick={() => {
                        // If you add a product page, navigate using a.raw.id
                        // e.g., navigate(`/products/${a.raw?.id}`)
                      }}
                    >
                      View Portfolio
                    </Button>

                    <Button
                      size="sm"
                      className="rounded-lg bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400"
                      onClick={() => {
                        // Placeholder action
                        alert('Collab request sent (stub). Hook to your collab API later.')
                      }}
                    >
                      <Handshake className="h-4 w-4 mr-1" />
                      Request Collab
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Right: ideas */}
      <div className="space-y-4">
        <SectionTitle icon={Sparkles} title="AI Fusion Ideas" />
        <Card className="bg-slate-900/60 border border-slate-700/60 shadow-xl">
          <CardContent className="space-y-3 text-sm">
            <div className="font-semibold text-slate-200">Suggested pairings</div>
            <ul className="list-disc pl-5 space-y-1 text-slate-300">
              <li>Block-print textiles with terracotta motif buttons</li>
              <li>Carved wooden frames with inlaid metal filigree</li>
              <li>Minimal pottery with embroidered sleeve wraps</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

