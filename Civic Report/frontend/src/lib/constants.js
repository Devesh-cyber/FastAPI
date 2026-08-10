import {
  Trash2, Droplet, Construction, Lightbulb, Waves,
  RectangleEllipsis, FlaskConical, ShieldAlert, HelpCircle,
} from 'lucide-react'

export const CATEGORIES = [
  { value: 'garbage', label: 'Garbage', icon: Trash2 },
  { value: 'water', label: 'Water supply', icon: Droplet },
  { value: 'pothole', label: 'Pothole', icon: Construction },
  { value: 'streetlight', label: 'Streetlight', icon: Lightbulb },
  { value: 'drainage', label: 'Drainage', icon: Waves },
  { value: 'road_damage', label: 'Road damage', icon: RectangleEllipsis },
  { value: 'sewage', label: 'Sewage', icon: FlaskConical },
  { value: 'public_safety', label: 'Public safety', icon: ShieldAlert },
  { value: 'other', label: 'Other', icon: HelpCircle },
]

export function categoryMeta(value) {
  return CATEGORIES.find((c) => c.value === value) || CATEGORIES[CATEGORIES.length - 1]
}

export const STATUSES = [
  { value: 'open', label: 'Open', className: 'text-amber bg-amber-soft' },
  { value: 'in_progress', label: 'In progress', className: 'text-steel bg-steel-soft' },
  { value: 'resolved', label: 'Resolved', className: 'text-moss bg-moss-soft' },
]

export function statusMeta(value) {
  return STATUSES.find((s) => s.value === value) || STATUSES[0]
}
