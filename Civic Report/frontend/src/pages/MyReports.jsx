import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ClipboardList } from 'lucide-react'
import { getStoredCitizen, getCitizenIssues } from '../lib/api'
import IssueTicket from '../components/IssueTicket'
import EmptyState from '../components/EmptyState'
import Notice from '../components/Notice'

export default function MyReports() {
  const citizen = getStoredCitizen()
  const [issues, setIssues] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!citizen) { setLoading(false); return }
    getCitizenIssues(citizen.id)
      .then(setIssues)
      .catch((err) => {
        if (err.response?.status !== 404) setError('Could not load your reports right now.')
      })
      .finally(() => setLoading(false))
  }, [citizen?.id])

  if (!citizen) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-14">
        <EmptyState
          icon={ClipboardList}
          title="You haven't registered on this device yet"
          hint="Register while filing your first report to start tracking it here."
        />
        <div className="text-center mt-4">
          <Link to="/" className="text-sm font-medium text-ink underline">
            Report an issue →
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <p className="font-mono text-xs uppercase tracking-widest text-amber mb-2">
        {citizen.name} · {citizen.locality}
      </p>
      <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-ink tracking-tight mb-6">
        My reports
      </h1>

      <Notice tone="error">{error}</Notice>

      {loading ? (
        <p className="text-sm text-ink-soft">Loading your reports…</p>
      ) : issues.length === 0 ? (
        <EmptyState
          icon={ClipboardList}
          title="No reports filed yet"
          hint="Anything you report will show up here with a live status."
        />
      ) : (
        <div className="flex flex-col gap-3">
          {issues
            .slice()
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .map((issue) => (
              <IssueTicket key={issue.id} issue={issue} />
            ))}
        </div>
      )}
    </div>
  )
}
