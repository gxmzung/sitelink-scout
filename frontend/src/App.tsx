import { useEffect, useState } from 'react'

type Health = {
  status: string
  service: string
  version: string
}

function App() {
  const [health, setHealth] = useState<Health | null>(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then((res) => res.json())
      .then(setHealth)
      .catch(() => setHealth(null))
  }, [])

  return (
    <main className="app">
      <header className="header">
        <div>
          <p className="eyebrow">SiteLink</p>
          <h1>Field Console</h1>
          <p className="subtitle">
            Construction-site wireless coverage validation
          </p>
        </div>

        <div className={`backend-status ${health ? 'online' : 'offline'}`}>
          <span className="dot" />
          {health ? 'BACKEND ONLINE' : 'BACKEND OFFLINE'}
        </div>
      </header>

      <section className="stats">
        <article className="card">
          <span>Coverage</span>
          <strong>-- %</strong>
          <small>Waiting for Scout telemetry</small>
        </article>

        <article className="card">
          <span>Average RSSI</span>
          <strong>-- dBm</strong>
          <small>No measurements yet</small>
        </article>

        <article className="card">
          <span>Active Scouts</span>
          <strong>0 / 3</strong>
          <small>Prototype target</small>
        </article>

        <article className="card">
          <span>Dead Zones</span>
          <strong>0</strong>
          <small>RSSI threshold-based</small>
        </article>
      </section>

      <section className="workspace">
        <article className="panel coverage">
          <div className="panel-title">
            <div>
              <p className="eyebrow">LIVE SITE</p>
              <h2>Coverage Map</h2>
            </div>
            <span>ZONE GRID</span>
          </div>

          <div className="grid-placeholder">
            <div>A01</div>
            <div>A02</div>
            <div>A03</div>
            <div>B01</div>
            <div>B02</div>
            <div>B03</div>
            <div>C01</div>
            <div>C02</div>
            <div>C03</div>
          </div>
        </article>

        <article className="panel scouts">
          <div className="panel-title">
            <div>
              <p className="eyebrow">DEVICES</p>
              <h2>Scout Status</h2>
            </div>
          </div>

          <div className="empty">
            No Scout measurements received yet.
          </div>
        </article>
      </section>

      <section className="panel recommendation">
        <div>
          <p className="eyebrow">RECOMMENDATION ENGINE</p>
          <h2>AP Relocation</h2>
        </div>
        <p>
          Coverage recommendations will appear after measurement data is
          collected.
        </p>
      </section>
    </main>
  )
}

export default App
