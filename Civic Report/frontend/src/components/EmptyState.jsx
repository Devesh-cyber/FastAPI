export default function EmptyState({ icon: Icon, title, hint }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 px-6 border border-dashed border-rule rounded-lg">
      {Icon && <Icon size={28} strokeWidth={1.5} className="text-ink-soft/50 mb-3" />}
      <p className="font-display font-semibold text-ink">{title}</p>
      {hint && <p className="text-sm text-ink-soft mt-1 max-w-xs">{hint}</p>}
    </div>
  )
}
