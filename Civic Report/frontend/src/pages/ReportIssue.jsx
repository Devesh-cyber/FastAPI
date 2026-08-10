import { useState, useRef } from 'react'
import { Link } from 'react-router-dom'
import { Camera, X, CheckCircle2, KeyRound, ArrowRight } from 'lucide-react'
import {
  createCitizen, createIssue, getStoredCitizen, storeCitizen,
  clearStoredCitizen, getApiKey, setApiKey,
} from '../lib/api'
import { CATEGORIES } from '../lib/constants'
import Notice from '../components/Notice'

function refNo(id) {
  return `#ISS-${String(id).padStart(6, '0')}`
}

export default function ReportIssue() {
  const [citizen, setCitizen] = useState(getStoredCitizen())
  const [apiKey, setApiKeyState] = useState(getApiKey())

  // Registration form state
  const [regForm, setRegForm] = useState({ name: '', contact_no: '', locality: '' })
  const [regError, setRegError] = useState('')
  const [regLoading, setRegLoading] = useState(false)

  // Issue form state
  const [category, setCategory] = useState('')
  const [location, setLocation] = useState('')
  const [description, setDescription] = useState('')
  const [image, setImage] = useState(null)
  const [preview, setPreview] = useState(null)
  const [issueError, setIssueError] = useState('')
  const [issueLoading, setIssueLoading] = useState(false)
  const [submitted, setSubmitted] = useState(null)
  const fileRef = useRef(null)

  function handleApiKeyChange(v) {
    setApiKeyState(v)
    setApiKey(v)
  }

  async function handleRegister(e) {
    e.preventDefault()
    setRegError('')
    if (!/^\d{10}$/.test(regForm.contact_no)) {
      setRegError('Mobile number must be exactly 10 digits.')
      return
    }
    if (!apiKey) {
      setRegError('Enter the access key issued by your ward office first.')
      return
    }
    setRegLoading(true)
    try {
      const created = await createCitizen(regForm)
      storeCitizen(created)
      setCitizen(created)
    } catch (err) {
      setRegError(
        err.response?.status === 403
          ? 'That access key was rejected by the server.'
          : 'Could not register. Check that the backend is running and try again.'
      )
    } finally {
      setRegLoading(false)
    }
  }

  function handleFile(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setImage(file)
    setPreview(URL.createObjectURL(file))
  }

  function resetIssueForm() {
    setCategory('')
    setLocation('')
    setDescription('')
    setImage(null)
    setPreview(null)
    if (fileRef.current) fileRef.current.value = ''
  }

  async function handleSubmitIssue(e) {
    e.preventDefault()
    setIssueError('')
    if (!category) return setIssueError('Pick a category for the issue.')
    if (!location.trim()) return setIssueError('Add a location so it can be located and fixed.')
    if (!description.trim()) return setIssueError('Describe what you saw.')
    if (!image) return setIssueError('Attach a photo of the issue.')

    setIssueLoading(true)
    try {
      const created = await createIssue({
        category, location, description, citizen_id: citizen.id, image,
      })
      setSubmitted(created)
      resetIssueForm()
    } catch (err) {
      setIssueError(
        err.response?.status === 403
          ? 'That access key was rejected by the server.'
          : 'Could not submit the report. Check your connection and try again.'
      )
    } finally {
      setIssueLoading(false)
    }
  }

  function switchCitizen() {
    clearStoredCitizen()
    setCitizen(null)
    setSubmitted(null)
  }

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <div className="mb-9">
        <p className="font-mono text-xs uppercase tracking-widest text-amber mb-2">
          Ward complaint counter
        </p>
        <h1 className="font-display font-extrabold text-3xl sm:text-4xl text-ink leading-tight tracking-tight">
          File a civic complaint.<br />Get a ticket. Track it through.
        </h1>
        <p className="text-ink-soft mt-3 text-[15px] leading-relaxed max-w-lg">
          Garbage, potholes, streetlights, drainage — report it once and follow its
          status from open to resolved, the same way you would at a physical
          ward office.
        </p>
      </div>

      {!citizen ? (
        <form onSubmit={handleRegister} className="ticket p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-display font-bold text-ink">Register once</h2>
            <span className="font-mono text-[11px] text-ink-soft/60">STEP 1 / 2</span>
          </div>
          <p className="text-sm text-ink-soft -mt-2">
            Your details stay on this device and are attached to every report you file.
          </p>

          <div className="grid gap-3">
            <label className="text-sm font-medium text-ink">
              Full name
              <input
                required
                value={regForm.name}
                onChange={(e) => setRegForm({ ...regForm, name: e.target.value })}
                placeholder="e.g. Priya Sharma"
                className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none"
              />
            </label>

            <label className="text-sm font-medium text-ink">
              Mobile number
              <input
                required
                inputMode="numeric"
                value={regForm.contact_no}
                onChange={(e) => setRegForm({ ...regForm, contact_no: e.target.value.replace(/\D/g, '').slice(0, 10) })}
                placeholder="10 digit number"
                className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none font-mono"
              />
            </label>

            <label className="text-sm font-medium text-ink">
              Locality
              <input
                required
                value={regForm.locality}
                onChange={(e) => setRegForm({ ...regForm, locality: e.target.value })}
                placeholder="e.g. Mulund West"
                className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none"
              />
            </label>

            <label className="text-sm font-medium text-ink">
              <span className="flex items-center gap-1.5">
                <KeyRound size={13} /> Access key
              </span>
              <input
                required
                type="password"
                value={apiKey}
                onChange={(e) => handleApiKeyChange(e.target.value)}
                placeholder="Issued by your ward office"
                className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none font-mono"
              />
              <span className="block text-xs text-ink-soft/70 mt-1 font-normal">
                Matches the API_KEY configured on the backend. Ask whoever runs the
                server if you don't have it.
              </span>
            </label>
          </div>

          <Notice tone="error">{regError}</Notice>

          <button
            type="submit"
            disabled={regLoading}
            className="w-full inline-flex items-center justify-center gap-1.5 bg-ink text-paper font-medium text-sm rounded-md py-2.5 hover:bg-ink-soft transition-colors disabled:opacity-60"
          >
            {regLoading ? 'Registering…' : 'Continue to report an issue'}
            <ArrowRight size={15} />
          </button>
        </form>
      ) : submitted ? (
        <div className="ticket p-6 sm:p-7 text-center">
          <CheckCircle2 size={30} className="text-moss mx-auto mb-3" strokeWidth={1.75} />
          <h2 className="font-display font-bold text-lg text-ink">Report filed</h2>
          <p className="text-sm text-ink-soft mt-1">
            Keep this reference number to track its progress.
          </p>
          <p className="font-mono text-2xl font-semibold text-ink mt-4 tracking-wide">
            {refNo(submitted.id)}
          </p>
          <div className="ticket-perf my-5" />
          <div className="flex flex-col sm:flex-row gap-2 justify-center">
            <Link
              to={`/issues/${submitted.id}`}
              className="inline-flex items-center justify-center gap-1.5 bg-ink text-paper text-sm font-medium rounded-md px-4 py-2 hover:bg-ink-soft transition-colors"
            >
              View this ticket
            </Link>
            <button
              onClick={() => setSubmitted(null)}
              className="inline-flex items-center justify-center gap-1.5 border border-rule text-ink text-sm font-medium rounded-md px-4 py-2 hover:bg-white transition-colors"
            >
              File another report
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmitIssue} className="ticket p-6 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-display font-bold text-ink">Report an issue</h2>
              <p className="text-xs text-ink-soft mt-0.5">
                Filing as <span className="font-medium text-ink">{citizen.name}</span> · {citizen.locality}{' '}
                <button type="button" onClick={switchCitizen} className="underline hover:text-ink">
                  not you?
                </button>
              </p>
            </div>
            <span className="font-mono text-[11px] text-ink-soft/60 flex-shrink-0">STEP 2 / 2</span>
          </div>

          <div>
            <p className="text-sm font-medium text-ink mb-2">Category</p>
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
              {CATEGORIES.map(({ value, label, icon: Icon }) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setCategory(value)}
                  className={`flex flex-col items-center gap-1.5 rounded-md border py-2.5 px-1 text-[11px] font-medium transition-colors ${
                    category === value
                      ? 'border-amber bg-amber-soft text-ink'
                      : 'border-rule bg-white text-ink-soft hover:border-ink-soft/40'
                  }`}
                >
                  <Icon size={17} strokeWidth={2} />
                  {label}
                </button>
              ))}
            </div>
          </div>

          <label className="text-sm font-medium text-ink block">
            Location
            <input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Street, landmark, or intersection"
              className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none"
            />
          </label>

          <label className="text-sm font-medium text-ink block">
            Description
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              maxLength={1000}
              placeholder="What's wrong, and since when?"
              className="mt-1 w-full rounded-md border border-rule bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-soft/40 focus:border-amber outline-none resize-none"
            />
          </label>

          <div>
            <p className="text-sm font-medium text-ink mb-2">Photo</p>
            {preview ? (
              <div className="relative w-full h-44 rounded-md overflow-hidden border border-rule">
                <img src={preview} alt="Preview" className="w-full h-full object-cover" />
                <button
                  type="button"
                  onClick={() => { setImage(null); setPreview(null); if (fileRef.current) fileRef.current.value = '' }}
                  className="absolute top-2 right-2 bg-ink/80 text-paper rounded-full p-1 hover:bg-ink"
                >
                  <X size={14} />
                </button>
              </div>
            ) : (
              <button
                type="button"
                onClick={() => fileRef.current?.click()}
                className="w-full h-28 rounded-md border border-dashed border-rule flex flex-col items-center justify-center gap-1.5 text-ink-soft hover:border-ink-soft/50 hover:text-ink transition-colors"
              >
                <Camera size={20} strokeWidth={1.75} />
                <span className="text-xs">Attach a photo of the issue</span>
              </button>
            )}
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={handleFile} />
          </div>

          <Notice tone="error">{issueError}</Notice>

          <button
            type="submit"
            disabled={issueLoading}
            className="w-full inline-flex items-center justify-center gap-1.5 bg-ink text-paper font-medium text-sm rounded-md py-2.5 hover:bg-ink-soft transition-colors disabled:opacity-60"
          >
            {issueLoading ? 'Filing report…' : 'Submit report'}
          </button>
        </form>
      )}
    </div>
  )
}
