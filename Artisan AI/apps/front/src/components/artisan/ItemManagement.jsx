// front/src/components/artisan/ItemManagement.jsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '../ui/Button'
import SectionTitle from '../ui/SectionTitle'
import Empty from '../ui/Empty'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Badge from '../ui/Badge'
import { Plus, Megaphone, Hash, Store } from 'lucide-react'
import QuickMarketing from './QuickMarketing'
import CreateItem from './CreateItem'

const BASE =
  import.meta.env.VITE_API_BASE ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8080'

const PLACEHOLDER = '/placeholder-640x360.png' // local fallback

export default function ItemManagement() {
  const [items, setItems] = useState([])
  const nav = useNavigate()
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')
  const [next, setNext] = useState(null) // { ts, id } from API

  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400'
  const outlineBtn =
    'rounded-xl border-slate-700 text-slate-200 hover:bg-slate-800/60 hover:border-sky-500/50'
  const dangerBtn =
    'rounded-xl border border-red-500/40 text-red-300 hover:bg-red-500/10'
  const cardCls = 'bg-slate-900/60 border border-slate-700/60 shadow-xl'

  // --- load from backend (supports pagination) ---
  async function loadProducts({ append = false } = {}) {
    setLoading(true)
    setErr('')
    try {
      const url = new URL(`${BASE}/v1/products/`)
      url.searchParams.set('limit', '24')
      if (append && next?.ts && next?.id) {
        url.searchParams.set('cursor_ts', next.ts)
        url.searchParams.set('cursor_id', next.id)
      }

      const res = await fetch(url.toString())
      const text = await res.text()
      const looksJson = (res.headers.get('content-type') || '').includes('application/json')
      const body = looksJson && text ? JSON.parse(text) : {}

      if (!res.ok) throw new Error(body?.detail || `${res.status} ${res.statusText}`)

      const mapped = (body.items || []).map((p) => ({
        id: p.id,
        name: p.title || 'Untitled',
        theme: p.category || '—', // saved in `category`
        type: (Array.isArray(p.materials) && p.materials[0]) || p.attributes?.type || p.category || 'craft',
        preview: (Array.isArray(p.images) && p.images[0]) || p.preview_image || PLACEHOLDER,
        inventory: p.inventory ?? null,
      }))

      setItems((prev) => (append ? [...prev, ...mapped] : mapped))
      setNext(body.next || null)
    } catch (e) {
      setErr(e.message || 'Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProducts()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // --- soft delete on backend (is_active=false) ---
  async function removeItem(idx, item) {
    const prev = items
    setItems((p) => p.filter((_, i) => i !== idx))
    if (!item?.id) return
    try {
      const res = await fetch(`${BASE}/v1/products/${encodeURIComponent(item.id)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: false }),
      })
      if (!res.ok) setItems(prev) // revert on server error
    } catch {
      setItems(prev) // revert on network error
    }
  }

  return (
    <div className="grid lg:grid-cols-3 gap-6 text-slate-100">
      {/* Left: Items */}
      <div className="lg:col-span-2 space-y-4">
        <SectionTitle
          icon={Store}
          title="Your Store Items"
          right={
            <div className="flex items-center gap-3">
              {loading ? <span className="text-xs text-slate-400">Loading…</span> : null}
              {err ? <span className="text-xs text-rose-400">{err}</span> : null}
              <Button onClick={() => nav('/artisan/new')} className={primaryBtn}>
                <Plus className="h-4 w-4 mr-1" />
                Add Product
              </Button>
            </div>
          }
        />

        {items.length === 0 ? (
          <Empty
            icon={Store}
            title={loading ? 'Loading products…' : 'No products yet'}
            subtitle={
              loading
                ? 'Fetching your catalog from the server.'
                : 'Add your first craft item. Upload images, choose theme & type, and let AI help with descriptions, marketing, and storytelling.'
            }
            cta={
              !loading && (
                <Button onClick={() => nav('/artisan/new')} className={primaryBtn}>
                  <Plus className="h-4 w-4 mr-1" />
                  Add Product
                </Button>
              )
            }
          />
        ) : (
          <>
            <div className="grid md:grid-cols-2 gap-4">
              {items.map((it, idx) => (
                <Card key={(it.id ?? idx) + it.name} className={cardCls}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="text-slate-100">{it.name}</span>
                      <div className="flex items-center gap-2">
                        {it.inventory != null ? (
                          <Badge className="bg-emerald-600/20 text-emerald-300 border border-emerald-500/30">
                            Stock {it.inventory}
                          </Badge>
                        ) : null}
                        <Badge className="bg-sky-600/20 text-sky-300 border border-sky-500/30">
                          {it.theme}
                        </Badge>
                      </div>
                    </CardTitle>
                  </CardHeader>

                  <CardContent className="space-y-3">
                    <img
                      src={it.preview || PLACEHOLDER}
                      alt={`${it.name} preview`}
                      className="w-full h-40 object-cover rounded-xl border border-slate-700"
                      onError={(e) => {
                        e.currentTarget.onerror = null
                        e.currentTarget.src = PLACEHOLDER
                      }}
                    />
                    <div className="text-sm text-slate-400">{it.type}</div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" className={outlineBtn}>
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => removeItem(idx, it)}
                        className={dangerBtn}
                      >
                        Remove
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Load more */}
            <div className="pt-2">
              {next ? (
                <Button onClick={() => loadProducts({ append: true })} className={primaryBtn}>
                  Load more
                </Button>
              ) : (
                <span className="text-xs text-slate-500">End of list</span>
              )}
            </div>
          </>
        )}
      </div>

      {/* Right: Marketing + Hashtags */}
      <div className="space-y-4">
        <SectionTitle icon={Megaphone} title="Quick Marketing" />
        <div className={cardCls + ' rounded-2xl p-4'}>
          <QuickMarketing />
        </div>

        <div className="h-px bg-slate-700/60 my-2" />

        <SectionTitle icon={Hash} title="Trending Hashtags" />
        <div className="flex flex-wrap gap-2">
          {['#HandloomLove', '#VocalForLocal', '#FestiveEdit', '#SustainableCraft'].map((h) => (
            <Badge
              key={h}
              variant="outline"
              className="bg-slate-800/70 border-slate-700 text-slate-300 hover:text-sky-300 hover:border-sky-500/50"
            >
              {h}
            </Badge>
          ))}
        </div>
      </div>
    </div>
  )
}

