// src/components/ui/Card.jsx

export function Card({ className = '', children }) {
  return (
    <div
      className={[
        'rounded-2xl bg-slate-900/60 border border-slate-700/60 shadow-xl',
        'text-slate-100', // default text color inside cards
        className,
      ].join(' ')}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className = '', children }) {
  return (
    <div
      className={[
        'px-4 py-3',
        'border-b border-slate-700/60 bg-slate-900/60',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  );
}

export function CardTitle({ className = '', as: Tag = 'h3', children }) {
  return (
    <Tag
      className={[
        'text-lg font-semibold tracking-tight',
        'text-slate-100',
        className,
      ].join(' ')}
    >
      {children}
    </Tag>
  );
}

export function CardContent({ className = '', children }) {
  return (
    <div
      className={[
        'p-4',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  );
}
