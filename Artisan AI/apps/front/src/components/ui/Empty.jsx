import { Card, CardContent } from './Card'

export default function Empty({ icon: Icon, title, subtitle, cta, className = '' }) {
  return (
    <Card
      className={[
        'bg-slate-900/60 border border-slate-700/60 border-dashed',
        'rounded-2xl shadow-xl',
        className,
      ].join(' ')}
    >
      <CardContent className="py-12 flex flex-col items-center gap-3 text-center">
        {Icon && <Icon className="h-10 w-10 text-sky-300" />}
        <div className="text-2xl font-semibold text-slate-100">{title}</div>
        {subtitle && (
          <div className="text-slate-400 max-w-xl">
            {subtitle}
          </div>
        )}
        {cta}
      </CardContent>
    </Card>
  )
}
