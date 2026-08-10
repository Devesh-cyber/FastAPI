import { useEffect, useState } from 'react'
import { Search, ListChecks } from 'lucide-react'
import { listIssues } from '../lib/api'
import { CATEGORIES, STATUSES } from '../lib/constants'
import IssueTicket from '../components/IssueTicket'
import EmptyState from '../components/EmptyState'
import Notice from '../components/Notice'

export default function Browse() {
  const [issues, setIssues] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('')
  const [location, setLocation] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')
    const timer = setTimeout(() => {
      listIssues({ category, status, location: location.trim() || undefined })
        .then(setIssues)
        .catch((err) => {
          if (err.response?.status === 404) setIssues([])
          else setError('Could not load issues right now.')
        })
        .finally(() => setLoading(false))
    }, 250)
    return () => clearTimeout(timer)
  }, [category, status, location])

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <p className="font-mono text-xs uppercase tracking-widest text-amber mb-2">
        Ward register
      </p>
      <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-ink tracking-tight mb-6">
        Browse reported issues
      </h1>

      <div className="ticket p-4 mb-6 flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft/50" />
          <input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Search by location"
            className="w-full pl-8 pr-3 py-2 rounded-md border border-rule bg-white text-sm focus:border-amber outline-none"
          />
        </div>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="rounded-md border border-rule bg-white text-sm px-3 py-2 focus:border-amber outline-none"
        >
          <option value="">All categories</option>
          {CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>{c.label}</option>
          ))}
        </select>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="rounded-md border border-rule bg-white text-sm px-3 py-2 focus:border-amber outline-none"
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>

      <Notice tone="error">{error}</Notice>

      {loading ? (
        <p className="text-sm text-ink-soft">Loading issues…</p>
      ) : issues.length === 0 ? (
        <EmptyState
          icon={ListChecks}
          title="No issues match these filters"
          hint="Try clearing a filter, or check back once more reports come in."
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
