import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'
import { Mic, MicOff, Bell } from 'lucide-react'

export default function UniqueTools() {
  const [listening, setListening] = useState(false)

  const cardCls = 'bg-slate-900/60 border border-slate-700/60 shadow-xl'
  const outlineBtn =
    'rounded-xl border-slate-700 text-slate-200 hover:bg-slate-800/60 hover:border-sky-500/50'
  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400'
  const dangerBtn =
    'rounded-xl bg-gradient-to-r from-red-600 to-rose-500 text-white hover:from-red-500 hover:to-rose-400'
  const softRow =
    'flex items-center justify-between rounded-xl px-3 py-2 bg-slate-800/70 border border-slate-700 text-slate-200'
  const softBadge =
    'px-2 py-0.5 text-xs rounded-md bg-sky-600/20 text-sky-300 border border-sky-500/30'

  return (
    <div className="grid lg:grid-cols-2 gap-6 text-slate-100">
      {/* Dialect-aware Voice Narrator */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Mic className="h-5 w-5 text-sky-300" /> Dialect-aware Voice Narrator
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="text-sm text-slate-300">
            Record story snippets in your dialect; AI aligns pronunciation and prosody to your region
            and generates multilingual captions.
          </div>
          <div className="flex items-center gap-3">
            <Button
              onClick={() => setListening((v) => !v)}
              className={listening ? dangerBtn : primaryBtn}
            >
              {listening ? (
                <>
                  <MicOff className="h-4 w-4 mr-1" /> Stop
                </>
              ) : (
                <>
                  <Mic className="h-4 w-4 mr-1" /> Record
                </>
              )}
            </Button>
            <Button variant="outline" className={outlineBtn}>
              Preview
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Trending Alerts */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5 text-sky-300" /> Trending Alerts
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className={softRow}>
            <span>"Festival decor" searches up 35% in North India</span>
            <span className={softBadge}>Now</span>
          </div>
          <div className={softRow}>
            <span>High demand: Block-print dupattas</span>
            <span className={softBadge}>Today</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
