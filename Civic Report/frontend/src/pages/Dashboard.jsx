import { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import { Users, FileStack, KeyRound, Trash2 } from 'lucide-react'
import { getStats, listIssues, updateIssue, deleteIssue, getApiKey, setApiKey } from '../lib/api'
import { categoryMeta, STATUSES } from '../lib/constants'
import Notice from '../components/Notice'
import EmptyState from '../components/EmptyState'

function refNo(id) {
  return `#ISS-${String(id).padStart(6, '0')}`
}

function StatPill({ label, value, icon: Icon }) {
  return (
    <div className="ticket p-4 flex items-center gap-3">
      <div className="w-9 h-9 rounded-md bg-amber-soft text-amber flex items-center justify-center flex-shrink-0">
        <Icon size={17} />
      </div>
      <div>
        <p className="font-display font-bold text-xl text-ink leading-none">{value}</p>
        <p className="text-xs text-ink-soft mt-0.5">{label}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [issues, setIssues] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [apiKey, setApiKeyState] = useState(getApiKey())
  const [actionError, setActionError] = useState('')
  const [busyId, setBusyId] = useState(null)

  function load() {
    setLoading(true)
    Promise.all([
      getStats(),
      listIssues().catch((err) => (err.response?.status === 404 ? [] : Promise.reject(err))),
    ])
      .then(([s, i]) => { setStats(s); setIssues(i) })
      .catch(() => setError('Could not reach the backend. Is it running on the configured URL?'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  function handleApiKeyChange(v) {
    setApiKeyState(v)
    setApiKey(v)
  }

  async function handleStatusChange(id, status) {
    setActionError('')
    setBusyId(id)
    try {
      const updated = await updateIssue(id, { status })
      setIssues((prev) => prev.map((it) => (it.id === id ? updated : it)))
    } catch (err) {
      setActionError(err.response?.status === 403
        ? 'Access key rejected — enter the correct key to manage issues.'
        : 'Could not update that issue.')
    } finally {
      setBusyId(null)
    }
  }

  async function handleDelete(id) {
    setActionError('')
    setBusyId(id)
    try {
      await deleteIssue(id)
      setIssues((prev) => prev.filter((it) => it.id !== id))
    } catch (err) {
      setActionError(err.response?.status === 403
        ? 'Access key rejected — enter the correct key to manage issues.'
        : 'Could not delete that issue.')
    } finally {
      setBusyId(null)
    }
  }

  const categoryData = stats
    ? Object.entries(stats.issues_by_category).map(([key, count]) => ({
        name: categoryMeta(key).label,
        count,
      }))
    : []

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <p className="font-mono text-xs uppercase tracking-widest text-amber mb-2">
        Ward office
      </p>
      <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-ink tracking-tight mb-6">
        Dashboard
      </h1>

      <Notice tone="error">{error}</Notice>

      {loading ? (
        <p className="text-sm text-ink-soft">Loading dashboard…</p>
      ) : stats ? (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <StatPill label="Citizens registered" value={stats.total_citizens} icon={Users} />
            <StatPill label="Issues logged" value={stats.total_issues} icon={FileStack} />
            {STATUSES.map((s) => (
              <StatPill
                key={s.value}
                label={s.label}
                value={stats.issues_by_status[s.value] || 0}
                icon={FileStack}
              />
            ))}
          </div>

          {categoryData.length > 0 && (
            <div className="ticket p-4 sm:p-5 mb-8">
              <p className="text-sm font-semibold text-ink mb-3">Issues by category</p>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={categoryData} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#3C4A63' }} interval={0} angle={-20} textAnchor="end" height={50} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#3C4A63' }} />
                  <Tooltip
                    cursor={{ fill: '#EDEBE2' }}
                    contentStyle={{ fontSize: 12, borderRadius: 6, border: '1px solid #D3CEBC' }}
                  />
                  <Bar dataKey="count" fill="#C97A2E" radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-ink">Manage issues</p>
            <div className="flex items-center gap-2">
              <KeyRound size={13} className="text-ink-soft" />
              <input
                type="password"
                value={apiKey}
                onChange={(e) => handleApiKeyChange(e.target.value)}
                placeholder="Access key"
                className="rounded-md border border-rule bg-white text-xs px-2.5 py-1.5 w-32 font-mono focus:border-amber outline-none"
              />
            </div>
          </div>

          <Notice tone="error">{actionError}</Notice>

          {issues.length === 0 ? (
            <EmptyState title="No issues logged yet" />
          ) : (
            <div className="ticket overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs text-ink-soft uppercase tracking-wide border-b border-rule">
                    <th className="py-2.5 px-4 font-medium">Ref</th>
                    <th className="py-2.5 px-3 font-medium">Category</th>
                    <th className="py-2.5 px-3 font-medium">Location</th>
                    <th className="py-2.5 px-3 font-medium">Status</th>
                    <th className="py-2.5 px-3 font-medium text-right">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  {issues
                    .slice()
                    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    .map((issue) => (
                      <tr key={issue.id} className="border-b border-rule/60 last:border-0">
                        <td className="py-2.5 px-4 font-mono text-xs text-ink-soft">{refNo(issue.id)}</td>
                        <td className="py-2.5 px-3">{categoryMeta(issue.category).label}</td>
                        <td className="py-2.5 px-3 text-ink-soft truncate max-w-[160px]">{issue.location}</td>
                        <td className="py-2.5 px-3">
                          <select
                            value={issue.status}
                            disabled={busyId === issue.id}
                            onChange={(e) => handleStatusChange(issue.id, e.target.value)}
                            className="rounded-md border border-rule bg-white text-xs px-2 py-1 focus:border-amber outline-none"
                          >
                            {STATUSES.map((s) => (
                              <option key={s.value} value={s.value}>{s.label}</option>
                            ))}
                          </select>
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <button
                            onClick={() => handleDelete(issue.id)}
                            disabled={busyId === issue.id}
                            className="text-rust hover:bg-rust-soft rounded-md p-1.5 disabled:opacity-50"
                            aria-label="Delete issue"
                          >
                            <Trash2 size={14} />
                          </button>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      ) : null}
    </div>
  )
}
