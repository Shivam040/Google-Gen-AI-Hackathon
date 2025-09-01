// src/components/ui/SectionTitle.jsx
export default function SectionTitle({ icon: Icon, title, right, divider = true, className = '' }) {
  return (
    <div
      className={[
        'flex items-center justify-between mb-3',
        divider ? 'border-b border-slate-700/60 pb-2' : '',
        className,
      ].join(' ')}
    >
      <div className="flex items-center gap-2 text-slate-100">
        {Icon && <Icon className="h-5 w-5 text-sky-300" />}
        <h3 className="text-lg font-semibold tracking-tight">{title}</h3>
      </div>
      <div className="flex items-center gap-2">{right}</div>
    </div>
  );
}
