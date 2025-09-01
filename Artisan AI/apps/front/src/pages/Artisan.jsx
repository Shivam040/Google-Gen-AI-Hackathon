import TopBar from '../components/ui/TopBar'
import { Store, Handshake, LineChart as LineIcon, Sparkles } from 'lucide-react'
import ItemManagement from '../components/artisan/ItemManagement'
import CollaborationHub from '../components/artisan/CollaborationHub'
import Insights from '../components/artisan/Insights'
import UniqueTools from '../components/artisan/UniqueTools'
import { useState } from 'react'

export default function Artisan() {
  const [tab, setTab] = useState('items')
  const tabs = [
    { id: 'items', title: 'Item Management', icon: Store },
    { id: 'collab', title: 'Collaboration', icon: Handshake },
    { id: 'insights', title: 'Insights', icon: LineIcon },
    { id: 'unique', title: 'Unique', icon: Sparkles },
  ]

  const baseBtn =
    'w-full rounded-xl px-4 py-2 text-sm border transition-colors ' +
    'bg-slate-800/60 border-slate-700 text-slate-300 hover:bg-slate-700/60 ' +
    'focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500/70'

  const activeBtn =
    'bg-gradient-to-r from-sky-600 to-cyan-500 text-white border-sky-500 shadow ' +
    'hover:from-sky-500 hover:to-cyan-400'

  return (
    <div className="min-h-screen w-screen relative overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-800 text-slate-100">
      {/* subtle ambient glow */}
      <div className="absolute inset-0 -z-10 opacity-60 blur-3xl bg-gradient-to-b from-sky-900/20 via-transparent to-transparent" />

      <div className="max-w-6xl mx-auto px-4 md:px-8 py-6 space-y-8 relative z-10">
        <TopBar role="Artisan" />

        {/* Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-900/60 border border-slate-700/60 rounded-2xl p-2">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              aria-current={tab === t.id ? 'page' : undefined}
              className={`${baseBtn} ${tab === t.id ? activeBtn : ''} flex items-center justify-center gap-2`}
            >
              <t.icon className="h-4 w-4" />
              {t.title}
            </button>
          ))}
        </div>

        {/* Views */}
        <div>
          {tab === 'items' && <ItemManagement />}
          {tab === 'collab' && <CollaborationHub />}
          {tab === 'insights' && <Insights />}
          {tab === 'unique' && <UniqueTools />}
        </div>
      </div>
    </div>
  )
}
