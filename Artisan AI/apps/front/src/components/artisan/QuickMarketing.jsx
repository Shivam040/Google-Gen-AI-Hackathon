// front/src/components/artisan/QuickMarketing.jsx
import { useState } from 'react'
import Button from '../ui/Button'

const TONES = [
  'Professional','Friendly','Playful','Narrative','Persuasive',
  'Empathetic','Luxury','Minimal','Gen Z / Casual'
]

// Pick from envs you’ve used elsewhere
const BASE =
  import.meta.env.VITE_API_BASE ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8080'

export default function QuickMarketing({ productId = 'p1', channel = 'instagram', lang = 'en' }) {
  const [tone, setTone] = useState('Professional')
  const [hashtags, setHashtags] = useState('#Handmade #Local #Craft')
  const [copy, setCopy] = useState('')
  const [busy, setBusy] = useState(false)

  async function gen() {
    setBusy(true)
    setCopy('Generating...')
    try {
      // Call the lightweight suggest endpoint we added on the API
      const qs = new URLSearchParams({ product_id: productId, channel, lang })
      const res = await fetch(`${BASE}/v1/marketing/suggest?${qs}`)
      const text = await res.text()
      const body = (res.headers.get('content-type') || '').includes('application/json')
        ? (text ? JSON.parse(text) : {})
        : {}

      if (!res.ok) throw new Error(body?.detail || `${res.status} ${res.statusText}`)

      // API shape: { hashtags: [...], best_time: "ISO8601" }
      const tags = Array.isArray(body.hashtags) ? body.hashtags.join(' ') : hashtags
      const when = body.best_time ? new Date(body.best_time).toLocaleString() : '—'
      setHashtags(tags)
      setCopy(`Best time to post: ${when}\n\n${tags}\n\n(${tone})`)
    } catch (e) {
      // Fallback to the simple local mock
      setCopy(
        `Elevate your space with artisan-made pieces. (${tone})\n` +
        `${hashtags}\n\n[Hint: ${e.message || 'backend not available'}]`
      )
    } finally {
      setBusy(false)
    }
  }

  const inputBase =
    'w-full px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700 ' +
    'text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-sky-500/60 ' +
    'focus:outline-none transition'
  const textareaBase =
    'w-full px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700 ' +
    'text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-sky-500/60 ' +
    'focus:outline-none transition'
  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white ' +
    'hover:from-sky-500 hover:to-cyan-400 disabled:opacity-60 disabled:cursor-not-allowed'

  return (
    <div className="space-y-3 text-slate-100">
      <select value={tone} onChange={(e)=>setTone(e.target.value)} className={inputBase}>
        {TONES.map(t => <option key={t} value={t}>{t}</option>)}
      </select>

      <input
        className={inputBase}
        value={hashtags}
        onChange={(e)=>setHashtags(e.target.value)}
        placeholder="#Handmade #Local #Craft"
      />

      <Button onClick={gen} className={primaryBtn} disabled={busy}>
        {busy ? 'Generating…' : 'Generate'}
      </Button>

      <textarea
        rows={4}
        className={textareaBase}
        value={copy}
        onChange={(e)=>setCopy(e.target.value)}
        placeholder="Your generated post will appear here..."
      />
    </div>
  )
}

