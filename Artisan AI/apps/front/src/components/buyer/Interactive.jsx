

import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'

export default function Interactive() {
  const cardCls =
    'bg-slate-900/60 border border-slate-700/60 shadow-xl text-slate-100'
  const placeholderCls =
    'rounded-xl border border-slate-700 bg-slate-800/60 h-48 grid place-content-center text-slate-400'
  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400'
  const outlineBtn =
    'rounded-xl border-slate-700 text-slate-200 hover:bg-slate-800/60 hover:border-sky-500/50'
  const textareaCls =
    'w-full px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700 text-slate-100 ' +
    'placeholder-slate-400 focus:ring-2 focus:ring-sky-500/60 focus:outline-none transition'

  return (
    <div className="grid lg:grid-cols-2 gap-6 text-slate-100">
      {/* Video Shopping */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>Video Shopping</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className={placeholderCls}>Stream Placeholder</div>
          <div className="flex gap-2">
            <Button variant="outline" className={outlineBtn}>
              Schedule Demo
            </Button>
            <Button className={primaryBtn}>Join Live</Button>
          </div>
        </CardContent>
      </Card>

      {/* AR Preview */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>AR Preview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className={placeholderCls}>360° / AR Placeholder</div>
          <Button variant="outline" className={outlineBtn}>
            Open AR Viewer
          </Button>
        </CardContent>
      </Card>

      {/* Co-creation */}
      <Card className={`lg:col-span-2 ${cardCls}`}>
        <CardHeader>
          <CardTitle>Co-creation (AI-guided)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <textarea
            className={textareaCls}
            rows={3}
            placeholder="Describe your custom idea (colors, motifs, size)..."
          />
          <div className="flex gap-2">
            <Button variant="outline" className={outlineBtn}>
              Suggest Designs
            </Button>
            <Button className={primaryBtn}>Message Artisan</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
