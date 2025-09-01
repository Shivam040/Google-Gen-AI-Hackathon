// front/src/components/buyer/Commerce.jsx
import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'

const BASE =
  import.meta.env.VITE_API_BASE ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8080'

export default function Commerce() {
  const cardCls = 'bg-slate-900/60 border border-slate-700/60 shadow-xl'
  const inputCls =
    'w-full px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700 ' +
    'text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-sky-500/60 ' +
    'focus:outline-none transition'
  const softRow =
    'flex items-center justify-between rounded-xl px-3 py-2 bg-slate-800/70 ' +
    'border border-slate-700 text-slate-200'
  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white ' +
    'hover:from-sky-500 hover:to-cyan-400 disabled:opacity-60 disabled:cursor-not-allowed'

  // --- simple local state (with persistence for language) ---
  const [lang, setLang] = useState(() => localStorage.getItem('ui_lang') || 'en')
  const [savingLang, setSavingLang] = useState(false)
  const [following, setFollowing] = useState(false)
  const [joining, setJoining] = useState(false)

  useEffect(() => {
    localStorage.setItem('ui_lang', lang)
  }, [lang])

  async function onLangChange(e) {
    const next = e.target.value
    setLang(next)
    setSavingLang(true)
    try {
      // When user accounts are ready, persist preference to backend.
      // await fetch(`${BASE}/v1/users/me`, {
      //   method: 'PATCH',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ ui_lang: next }),
      // })
      // Optionally: warm up translation/voice models here.
      // await fetch(`${BASE}/v1/voice/lang?lang=${encodeURIComponent(next)}`)
    } catch {
      // ignore for now; UI still reflects local choice
    } finally {
      setSavingLang(false)
    }
  }

  async function onFollow() {
    setFollowing(true)
    try {
      // TODO: replace with real artisan/user IDs when auth is wired up
      // await fetch(`${BASE}/v1/users/me/follow`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ artisan_id: 'demo-artisan' }),
      // })
      await new Promise(r => setTimeout(r, 400)) // smooth UX
    } finally {
      setFollowing(false)
    }
  }

  async function onJoin() {
    setJoining(true)
    try {
      // await fetch(`${BASE}/v1/community/join`, { method: 'POST' })
      await new Promise(r => setTimeout(r, 400))
    } finally {
      setJoining(false)
    }
  }

  return (
    <div className="grid lg:grid-cols-2 gap-6 text-slate-100">
      {/* Multilingual Interface */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>Multilingual Interface</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select value={lang} onChange={onLangChange} className={inputCls} disabled={savingLang}>
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="bn">বাংলা</option>
            <option value="mr">मराठी</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
          </select>
          <div className="text-sm text-slate-300">
            UI strings and voiceover will adapt to your language preference.
            {savingLang ? <span className="ml-2 text-slate-400">Saving…</span> : null}
          </div>
        </CardContent>
      </Card>

      {/* Follow & Support */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>Follow &amp; Support</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className={softRow}>
            <span>Follow artisans for updates</span>
            <Button className={primaryBtn} onClick={onFollow} disabled={following}>
              {following ? 'Following…' : 'Follow'}
            </Button>
          </div>
          <div className={softRow}>
            <span>Join community innovation lab</span>
            <Button className={primaryBtn} onClick={onJoin} disabled={joining}>
              {joining ? 'Joining…' : 'Join'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
