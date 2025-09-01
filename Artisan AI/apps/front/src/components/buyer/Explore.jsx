// front/src/components/buyer/Explore.jsx
import { useEffect, useMemo, useState } from 'react'
import { Card, CardContent } from '../ui/Card'
import Button from '../ui/Button'
import Badge from '../ui/Badge'
import { Filter, ShieldCheck } from 'lucide-react'

const BASE =
  import.meta.env.VITE_API_BASE ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8080'

const PLACEHOLDER = 'https://picsum.photos/600/400'

export default function Explore() {
  const [query, setQuery] = useState('')
  const [items, setItems] = useState([])        // fetched from API
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setLoading(true); setErr('')
      try {
        // Use trailing slash to avoid 307
        const res = await fetch(`${BASE}/v1/products/?limit=24`)
        const text = await res.text()
        const looksJson = (res.headers.get('content-type') || '').includes('application/json')
        const body = looksJson && text ? JSON.parse(text) : {}
        if (!res.ok) throw new Error(body?.detail || `${res.status} ${res.statusText}`)

        const mapped = (body.items || []).map(p => ({
          id: p.id,
          title: p.title || 'Untitled',
          artisan: p.artisan_name || 'Artisan',
          theme: p.category || '—',
          price: p.price ?? null,
          img: (Array.isArray(p.images) && p.images[0]) || PLACEHOLDER,
        }))
        if (!cancelled) setItems(mapped)
      } catch (e) {
        if (!cancelled) {
          setErr(e.message || 'Failed to load products')
          setItems([]) // keep UI clean
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => { cancelled = true }
  }, [])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return items
    return items.filter(r =>
      (r.title || '').toLowerCase().includes(q) ||
      (r.theme || '').toLowerCase().includes(q) ||
      (r.artisan || '').toLowerCase().includes(q)
    )
  }, [items, query])

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-3 mb-4">
          <input
            className="input"
            placeholder="Search by theme, artisan, culture, festival"
            value={query}
            onChange={(e)=>setQuery(e.target.value)}
          />
          <Button variant="secondary">
            <Filter className="h-4 w-4 mr-1" />
            Filters
          </Button>
        </div>

        {err ? (
          <div className="text-sm text-rose-400 mb-3">Error: {err}</div>
        ) : null}
        {loading ? (
          <div className="text-sm text-slate-400">Loading products…</div>
        ) : null}

        <div className="grid md:grid-cols-3 gap-4">
          {filtered.map((r) => (
            <div key={r.id || r.title} className="card overflow-hidden">
              <img
                src={r.img}
                className="w-full h-40 object-cover"
                alt={r.title || 'Product'}
                onError={(e) => {
                  e.currentTarget.onerror = null;
                  e.currentTarget.src = PLACEHOLDER;
                }}
              />
              <div className="card-content space-y-2">
                <div className="flex items-center justify-between">
                  <div className="font-medium">{r.title}</div>
                  <Badge>{r.theme}</Badge>
                </div>
                <div className="text-sm text-slate-500">by {r.artisan}</div>
                <div className="text-sm font-semibold">
                  {r.price != null ? <>₹ {r.price}</> : <span className="text-slate-400">Price on request</span>}
                </div>

                <div className="bg-slate-100 bg-gradient-to-r from-sky-600 to-cyan-500 rounded-xl p-3 text-sm">
                  <div className="font-medium flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4" /> Provenance
                  </div>
                  <div>Verified journey from artisan to you. View story &amp; certificates.</div>
                </div>

                <div className="flex gap-2 pt-1">
                  <Button size="sm">Add to Cart</Button>
                  <Button size="sm" variant="secondary">View Story</Button>
                </div>
              </div>
            </div>
          ))}
          {!loading && !err && filtered.length === 0 ? (
            <div className="text-sm text-slate-400">No items match “{query}”.</div>
          ) : null}
        </div>
      </CardContent>
    </Card>
  )
}

