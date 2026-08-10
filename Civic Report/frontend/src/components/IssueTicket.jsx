import { Link } from 'react-router-dom'
import { MapPin, Calendar } from 'lucide-react'
import { categoryMeta } from '../lib/constants'
import StatusStamp from './StatusStamp'
import { imageUrl } from '../lib/api'

function refNo(id) {
  return `#ISS-${String(id).padStart(6, '0')}`
}

export default function IssueTicket({ issue }) {
  const meta = categoryMeta(issue.category)
  const Icon = meta.icon
  const date = new Date(issue.created_at)

  return (
    <Link
      to={`/issues/${issue.id}`}
      className="ticket flex flex-col sm:flex-row overflow-hidden hover:-translate-y-0.5 hover:shadow-md transition-all duration-150 group"
    >
      <div className="w-full sm:w-36 h-36 sm:h-auto bg-paper-dark flex-shrink-0 overflow-hidden">
        {issue.image_path ? (
          <img
            src={imageUrl(issue.image_path)}
            alt={meta.label}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-ink-soft/40">
            <Icon size={30} strokeWidth={1.5} />
          </div>
        )}
      </div>

      <div className="flex-1 p-4 flex flex-col gap-2 min-w-0">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-1.5 text-ink-soft text-xs font-mono">
            <Icon size={13} strokeWidth={2} />
            <span className="uppercase tracking-wide">{meta.label}</span>
          </div>
          <span className="font-mono text-[11px] text-ink-soft/70 whitespace-nowrap">
            {refNo(issue.id)}
          </span>
        </div>

        <p className="text-sm text-ink leading-snug line-clamp-2">
          {issue.description}
        </p>

        <div className="ticket-perf pb-2 flex items-center gap-1.5 text-xs text-ink-soft">
          <MapPin size={12} />
          <span className="truncate">{issue.location}</span>
        </div>

        <div className="flex items-center justify-between pt-0.5">
          <div className="flex items-center gap-1 text-[11px] text-ink-soft/70">
            <Calendar size={11} />
            {date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
          </div>
          <StatusStamp status={issue.status} />
        </div>
      </div>
    </Link>
  )
}
