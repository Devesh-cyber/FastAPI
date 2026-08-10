import { NavLink } from 'react-router-dom'
import { FileText, ClipboardList, ListChecks, LayoutDashboard } from 'lucide-react'

const links = [
  { to: '/', label: 'Report', icon: FileText },
  { to: '/my-reports', label: 'My reports', icon: ClipboardList },
  { to: '/browse', label: 'Browse', icon: ListChecks },
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
]

export default function Navbar() {
  return (
    <header className="sticky top-0 z-20 bg-paper/95 backdrop-blur border-b border-rule">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
        <NavLink to="/" className="flex items-center gap-2">
          <span className="font-mono text-xs font-semibold tracking-widest border border-ink rounded px-1.5 py-0.5">
            CR
          </span>
          <span className="font-display font-bold text-lg tracking-tight">Civic Report</span>
        </NavLink>
        <nav className="flex items-center gap-1">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-1.5 px-2.5 sm:px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-ink text-paper'
                    : 'text-ink-soft hover:bg-ink/5 hover:text-ink'
                }`
              }
            >
              <Icon size={15} strokeWidth={2} />
              <span className="hidden sm:inline">{label}</span>
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}
