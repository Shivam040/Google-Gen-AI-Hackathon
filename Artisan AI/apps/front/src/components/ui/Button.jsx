// src/components/ui/Button.jsx
export default function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  type = 'button',
  ...props
}) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-xl font-medium transition ' +
    'focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500/60 ' +
    'disabled:opacity-60 disabled:cursor-not-allowed select-none';

  const variants = {
    primary:
      'bg-gradient-to-r from-sky-600 to-cyan-500 text-white ' +
      'hover:from-sky-500 hover:to-cyan-400 shadow-sm',
    secondary:
      'bg-slate-800/70 text-slate-100 border border-slate-700 ' +
      'hover:bg-slate-800 hover:border-sky-500/50',
    outline:
      'bg-transparent text-slate-200 border border-slate-700 ' +
      'hover:bg-slate-800/60 hover:border-sky-500/50',
    destructive:
      'bg-transparent text-rose-300 border border-rose-500/40 ' +
      'hover:bg-rose-500/10',
    ghost:
      'bg-transparent text-slate-300 hover:text-sky-300 hover:bg-slate-800/40',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <button
      type={type}
      className={[
        base,
        variants[variant] || '',
        sizes[size] || '',
        className,
      ].join(' ')}
      {...props}
    >
      {children}
    </button>
  );
}
