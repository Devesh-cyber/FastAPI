import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import ReportIssue from './pages/ReportIssue'
import MyReports from './pages/MyReports'
import Browse from './pages/Browse'
import IssueDetail from './pages/IssueDetail'
import Dashboard from './pages/Dashboard'

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<ReportIssue />} />
          <Route path="/my-reports" element={<MyReports />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/issues/:id" element={<IssueDetail />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  )
}
