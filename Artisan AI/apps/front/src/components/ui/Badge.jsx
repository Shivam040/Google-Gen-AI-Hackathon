// src/components/ui/Badge.jsx
export default function Badge({ variant = 'outline', className = '', children, ...props }) {
  const base =
    'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium';
  const variants = {
    outline: 'text-slate-300 border border-slate-700 bg-slate-800/50',
    soft:    'bg-sky-600/20 text-sky-300 border border-sky-500/30',
  };
  return (
    <span
      className={[base, variants[variant] || variants.outline, className].join(' ')}
      {...props}
    >
      {children}
    </span>
  );
}
