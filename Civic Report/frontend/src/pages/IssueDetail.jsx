import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, MapPin, Calendar, Check } from 'lucide-react'
import { getIssue, imageUrl } from '../lib/api'
import { categoryMeta, STATUSES } from '../lib/constants'
import Notice from '../components/Notice'

function refNo(id) {
  return `#ISS-${String(id).padStart(6, '0')}`
}

export default function IssueDetail() {
  const { id } = useParams()
  const [issue, setIssue] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    getIssue(id)
      .then(setIssue)
      .catch(() => setError('This ticket could not be found.'))
      .finally(() => setLoading(false))
  }, [id])

  const stepIndex = issue ? STATUSES.findIndex((s) => s.value === issue.status) : -1

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <Link to="/browse" className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink mb-6">
        <ArrowLeft size={14} /> Back to register
      </Link>

      <Notice tone="error">{error}</Notice>

      {loading ? (
        <p className="text-sm text-ink-soft">Loading ticket…</p>
      ) : issue ? (
        <div className="ticket overflow-hidden">
          {issue.image_path && (
            <img
              src={imageUrl(issue.image_path)}
              alt={categoryMeta(issue.category).label}
              className="w-full h-56 sm:h-72 object-cover"
            />
          )}

          <div className="p-6 sm:p-7">
            <div className="flex items-start justify-between gap-3 mb-4">
              <div className="flex items-center gap-2 text-ink-soft text-xs font-mono uppercase tracking-wide">
                {(() => {
                  const Icon = categoryMeta(issue.category).icon
                  return <Icon size={14} strokeWidth={2} />
                })()}
                {categoryMeta(issue.category).label}
              </div>
              <span className="font-mono text-xs text-ink-soft/70">{refNo(issue.id)}</span>
            </div>

            <p className="text-ink text-[15px] leading-relaxed">{issue.description}</p>

            <div className="flex flex-wrap gap-4 mt-4 text-sm text-ink-soft">
              <span className="flex items-center gap-1.5">
                <MapPin size={14} /> {issue.location}
              </span>
              <span className="flex items-center gap-1.5">
                <Calendar size={14} />
                {new Date(issue.created_at).toLocaleDateString('en-IN', {
                  day: 'numeric', month: 'short', year: 'numeric',
                })}
              </span>
            </div>

            <div className="ticket-perf my-6" />

            <p className="text-xs font-medium text-ink-soft uppercase tracking-wide mb-4">
              Status
            </p>
            <ol className="flex items-center">
              {STATUSES.map((s, i) => (
                <li key={s.value} className="flex items-center flex-1 last:flex-initial">
                  <div className="flex flex-col items-center gap-1.5 flex-shrink-0">
                    <div
                      className={`w-7 h-7 rounded-full flex items-center justify-center border-2 text-xs font-semibold ${
                        i <= stepIndex
                          ? 'bg-ink border-ink text-paper'
                          : 'border-rule text-ink-soft/50'
                      }`}
                    >
                      {i < stepIndex ? <Check size={13} /> : i + 1}
                    </div>
                    <span className={`text-[11px] whitespace-nowrap ${i <= stepIndex ? 'text-ink font-medium' : 'text-ink-soft/60'}`}>
                      {s.label}
                    </span>
                  </div>
                  {i < STATUSES.length - 1 && (
                    <div className={`h-0.5 flex-1 mx-1.5 -mt-4 ${i < stepIndex ? 'bg-ink' : 'bg-rule'}`} />
                  )}
                </li>
              ))}
            </ol>
          </div>
        </div>
      ) : null}
    </div>
  )
}
