import { statusMeta } from '../lib/constants'

export default function StatusStamp({ status, className = '' }) {
  const meta = statusMeta(status)
  return (
    <span className={`stamp ${meta.className} ${className}`}>
      {meta.label}
    </span>
  )
}
