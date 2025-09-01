import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'
import { MapPin } from 'lucide-react'

export default function Social() {
  const cardCls =
    'bg-slate-900/60 border border-slate-700/60 shadow-xl text-slate-100'
  const softRow =
    'flex items-center justify-between rounded-xl px-3 py-2 bg-slate-800/70 ' +
    'border border-slate-700 text-slate-200'
  const primaryBtn =
    'rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white ' +
    'hover:from-sky-500 hover:to-cyan-400'

  return (
    <div className="grid lg:grid-cols-2 gap-6 text-slate-100">
      {/* Festival Bundles */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>Festival Bundles</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[
            { name: 'Diwali Home Set', items: 5 },
            { name: 'Eid Gift Box', items: 3 },
            { name: 'Pongal Kitchen Kit', items: 4 },
          ].map((b) => (
            <div key={b.name} className={softRow}>
              <span>{b.name}</span>
              <Button size="sm" className={primaryBtn}>
                View ({b.items})
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Community Events & Workshops */}
      <Card className={cardCls}>
        <CardHeader>
          <CardTitle>Community Events &amp; Workshops</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className={softRow}>
            <span>Handloom Market • Dehradun</span>
            <Button size="sm" className={primaryBtn}>
              <MapPin className="h-4 w-4 mr-1" />
              Details
            </Button>
          </div>
          <div className={softRow}>
            <span>Pottery Workshop • Rishikesh</span>
            <Button size="sm" className={primaryBtn}>
              <MapPin className="h-4 w-4 mr-1" />
              Details
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
