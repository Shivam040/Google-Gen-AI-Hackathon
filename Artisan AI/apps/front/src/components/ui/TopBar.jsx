import { Layers3, Bell, Globe2 } from 'lucide-react'
import Badge from './Badge'
import Button from './Button'

export default function TopBar({ role }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Layers3 className="h-5 w-5" />
        <span className="font-semibold">ArtisanMarket</span>
        <Badge variant="soft" className="ml-2">{role}</Badge>
      </div>
      <div className="flex items-center gap-3">
        <Button variant="outline" size="sm"><Bell className="h-4 w-4 mr-1" /> Alerts</Button>
        <Button variant="outline" size="sm"><Globe2 className="h-4 w-4 mr-1" /> Multilingual</Button>
      </div>
    </div>
  )
}