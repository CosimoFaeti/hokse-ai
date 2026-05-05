import { useEffect, useState } from 'react'
import { ping, getAthletes, syncActivities, stravaAuthUrl } from './api'
import Chat from './Chat'

type Status = 'loading' | 'unavailable' | 'unauthenticated' | 'ready'

export default function App() {
  const [status, setStatus] = useState<Status>('loading')
  const [athleteId, setAthleteId] = useState<number | null>(null)
  const [syncing, setSyncing] = useState(false)
  const [syncMsg, setSyncMsg] = useState<string | null>(null)

  useEffect(() => {
    async function init() {
      const up = await ping()
      if (!up) { setStatus('unavailable'); return }

      const params = new URLSearchParams(window.location.search)
      const paramId = params.get('athlete_id')
      if (paramId) {
        setAthleteId(parseInt(paramId, 10))
        window.history.replaceState({}, '', window.location.pathname)
        setStatus('ready')
        return
      }

      const ids = await getAthletes()
      if (ids.length > 0) {
        setAthleteId(ids[0])
        setStatus('ready')
      } else {
        setStatus('unauthenticated')
      }
    }
    void init()
  }, [])

  async function handleSync() {
    if (!athleteId) return
    setSyncing(true)
    setSyncMsg(null)
    try {
      const count = await syncActivities(athleteId)
      setSyncMsg(`Synced ${count} activities.`)
    } catch (e) {
      setSyncMsg(`Sync failed: ${e instanceof Error ? e.message : 'unknown error'}`)
    } finally {
      setSyncing(false)
    }
  }

  if (status === 'loading') return (
    <div className="center-screen">
      <p className="muted">Connecting to server...</p>
    </div>
  )

  if (status === 'unavailable') return (
    <div className="center-screen">
      <p className="error">Backend unavailable. Please try again in a moment.</p>
    </div>
  )

  if (status === 'unauthenticated') return (
    <div className="center-screen">
      <h2>Connect your Strava account</h2>
      <p className="muted">No account found. Authorise once to get started.</p>
      <a href={stravaAuthUrl} className="btn btn-primary">Connect with Strava</a>
    </div>
  )

  return (
    <div className="app">
      <header>
        <h1>Hokse-ai 🏃 Strava AI Agent</h1>
        <p className="muted">Your personal training coach, powered by AI</p>
        <p className="success">Connected — Athlete ID: {athleteId}</p>
      </header>
      <div className="toolbar">
        <button className="btn" onClick={() => void handleSync()} disabled={syncing}>
          {syncing ? 'Syncing...' : 'Sync latest activities'}
        </button>
        {syncMsg && (
          <span className={syncMsg.startsWith('Sync failed') ? 'error' : 'success'}>
            {syncMsg}
          </span>
        )}
      </div>
      <Chat athleteId={athleteId!} />
    </div>
  )
}
