import { AlertTriangle, CheckCircle2 } from 'lucide-react'

export default function Notice({ tone = 'error', children }) {
  if (!children) return null
  const isError = tone === 'error'
  const Icon = isError ? AlertTriangle : CheckCircle2
  return (
    <div
      className={`flex items-start gap-2 rounded-md border px-3 py-2.5 text-sm ${
        isError
          ? 'border-rust/40 bg-rust-soft text-rust'
          : 'border-moss/40 bg-moss-soft text-moss'
      }`}
      role={isError ? 'alert' : 'status'}
    >
      <Icon size={16} className="mt-0.5 flex-shrink-0" />
      <span>{children}</span>
    </div>
  )
}
