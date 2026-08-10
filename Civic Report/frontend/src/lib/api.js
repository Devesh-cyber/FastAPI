import axios from 'axios'

// Base URL of the FastAPI backend. Override at build time with
// VITE_API_URL if the backend isn't running on localhost:8000.
export const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const client = axios.create({ baseURL: BASE_URL })

// The backend guards writes (create/update/delete) behind a fixed
// header api_key (see auth.py — API_KEY = '123'). There's no per-user
// login, so this is a shared write-key, not a secret. Citizens type
// it once when reporting an issue; admins type it once to unlock the
// dashboard's manage actions. Both are cached in localStorage below.
export function getApiKey() {
  return localStorage.getItem('civic_api_key') || ''
}
export function setApiKey(key) {
  localStorage.setItem('civic_api_key', key)
}

function authHeaders() {
  // FastAPI's Header() converts the parameter name api_key -> the
  // actual HTTP header "api-key" (underscores become hyphens), so
  // that's what auth.py is really checking for.
  return { 'api-key': getApiKey() }
}

// ---- Citizens ----
export async function createCitizen({ name, contact_no, locality }) {
  const { data } = await client.post('/Citizens/', { name, contact_no, locality }, {
    headers: authHeaders(),
  })
  return data
}

export async function getCitizen(id) {
  const { data } = await client.get(`/Citizens/${id}`)
  return data
}

export async function getCitizenIssues(id) {
  const { data } = await client.get(`/Citizens/${id}/issues`)
  return data
}

// ---- Issues ----
export async function createIssue({ category, location, description, citizen_id, image }) {
  const form = new FormData()
  form.append('category', category)
  form.append('location', location)
  form.append('description', description)
  form.append('citizen_id', citizen_id)
  form.append('image', image)

  const { data } = await client.post('/Issues/', form, {
    headers: { ...authHeaders(), 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function listIssues({ category, status, location } = {}) {
  const params = {}
  if (category) params.filter_category = category
  if (status) params.filter_status = status
  if (location) params.filter_location = location
  const { data } = await client.get('/Issues/', { params })
  return data
}

export async function getIssue(id) {
  const { data } = await client.get(`/Issues/${id}`)
  return data
}

export async function updateIssue(id, patch) {
  const { data } = await client.patch(`/Issues/${id}`, patch, {
    headers: authHeaders(),
  })
  return data
}

export async function deleteIssue(id) {
  const { data } = await client.delete(`/Issues/${id}`, { headers: authHeaders() })
  return data
}

// ---- Analysis ----
export async function getStats() {
  const { data } = await client.get('/Analysis/stats')
  return data
}

export function imageUrl(path) {
  if (!path) return null
  // image_path is stored like "images/<uuid>.jpg" relative to the
  // backend's working directory — FastAPI needs to serve that folder
  // as static files for this to resolve (see the setup steps).
  return `${BASE_URL}/${path}`
}

// ---- Local citizen profile (so people don't re-register every visit) ----
const PROFILE_KEY = 'civic_citizen_profile'

export function getStoredCitizen() {
  const raw = localStorage.getItem(PROFILE_KEY)
  return raw ? JSON.parse(raw) : null
}

export function storeCitizen(citizen) {
  localStorage.setItem(PROFILE_KEY, JSON.stringify(citizen))
}

export function clearStoredCitizen() {
  localStorage.removeItem(PROFILE_KEY)
}
