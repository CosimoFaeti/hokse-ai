const API_URL = import.meta.env.VITE_API_URL as string | undefined
  ?? 'http://localhost:8080'

export const stravaAuthUrl = `${API_URL}/auth/strava`

export async function ping(): Promise<boolean> {
  try {
    const r = await fetch(`${API_URL}/healthz`, { method: 'POST' })
    return r.status === 204
  } catch {
    return false
  }
}

export async function getAthletes(): Promise<number[]> {
  try {
    const r = await fetch(`${API_URL}/auth/athletes`)
    return r.ok ? (r.json() as Promise<number[]>) : []
  } catch {
    return []
  }
}

export async function syncActivities(athleteId: number): Promise<number> {
  const r = await fetch(`${API_URL}/agent/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ athlete_id: athleteId, pages: 3 }),
  })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  const data = await r.json() as unknown[]
  return Array.isArray(data) ? data.length : 0
}

export async function sendMessage(athleteId: number, message: string): Promise<string> {
  const r = await fetch(`${API_URL}/agent/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ athlete_id: athleteId, message }),
  })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  const data = await r.json() as { message?: string }
  return data.message ?? 'No response.'
}
