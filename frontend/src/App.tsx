import { useEffect, useState } from 'react'

import {
  getCoverage,
  getDevices,
  getHealth,
} from './api/scout'

import CoverageHeatmap from './components/CoverageHeatmap'
import ScoutCard from './components/ScoutCard'

import type {
  CoverageSummary,
  ScoutDevice,
} from './types/scout'

const POLL_INTERVAL_MS = 2000

function App() {
  const [backendOnline, setBackendOnline] =
    useState(false)

  const [devices, setDevices] =
    useState<ScoutDevice[]>([])

  const [coverage, setCoverage] =
    useState<CoverageSummary | null>(null)

  const [error, setError] =
    useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function load() {
      try {
        const [
          health,
          devicesData,
          coverageData,
        ] = await Promise.all([
          getHealth(),
          getDevices(),
          getCoverage(),
        ])

        if (!mounted) {
          return
        }

        setBackendOnline(health.status === 'ok')
        setDevices(devicesData)
        setCoverage(coverageData)
        setError(null)
      } catch (err) {
        if (!mounted) {
          return
        }

        setBackendOnline(false)

        setError(
          err instanceof Error
            ? err.message
            : 'Unknown API error'
        )
      }
    }

    load()

    const timer = window.setInterval(
      load,
      POLL_INTERVAL_MS
    )

    return () => {
      mounted = false
      window.clearInterval(timer)
    }
  }, [])

  return (
    <main className="app-shell">
      <header className="header">
        <div>
          <p className="eyebrow">
            SITELINK SCOUT
          </p>

          <h1>Field Console</h1>

          <p className="subtitle">
            Construction-site Wi-Fi coverage
            validation
          </p>
        </div>

        <div
          className={
            backendOnline
              ? 'backend-status online'
              : 'backend-status offline'
          }
        >
          <span />
          BACKEND{' '}
          {backendOnline
            ? 'ONLINE'
            : 'OFFLINE'}
        </div>
      </header>

      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}

      <section className="stats">
        <article className="metric-card">
          <p>Coverage</p>
          <strong>
            {coverage
              ? `${coverage.coverage_percent}%`
              : '--'}
          </strong>
        </article>

        <article className="metric-card">
          <p>Average RSSI</p>
          <strong>
            {coverage?.average_rssi != null
              ? `${coverage.average_rssi} dBm`
              : '--'}
          </strong>
        </article>

        <article className="metric-card">
          <p>Scouts Online</p>
          <strong>{devices.length}</strong>
        </article>

        <article className="metric-card">
          <p>Dead Zones</p>
          <strong>
            {coverage?.dead_zones ?? '--'}
          </strong>
        </article>
      </section>

      <section className="workspace">
        <article className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">
                LIVE COVERAGE
              </p>
              <h2>Zone Map</h2>
            </div>

            <span className="threshold">
              Usable ≥{' '}
              {coverage?.usable_threshold_dbm ??
                -75}{' '}
              dBm
            </span>
          </div>

          <CoverageHeatmap
            zones={coverage?.zones ?? []}
          />
        </article>

        <article className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">
                FIELD NODES
              </p>
              <h2>Scout Status</h2>
            </div>
          </div>

          <div className="scout-list">
            {devices.length > 0 ? (
              devices.map((device) => (
                <ScoutCard
                  key={device.device_id}
                  scout={device}
                />
              ))
            ) : (
              <div className="empty">
                No Scout measurements received
                yet.
              </div>
            )}
          </div>
        </article>
      </section>

      <section className="panel recommendation">
        <div>
          <p className="eyebrow">
            RECOMMENDATION ENGINE
          </p>
          <h2>AP Relocation</h2>
        </div>

        <p>
          {coverage &&
          coverage.dead_zones > 0
            ? `${coverage.dead_zones} uncovered zone detected. Review AP placement near the weakest measured zone.`
            : 'No uncovered zones detected in the latest measurements.'}
        </p>
      </section>
    </main>
  )
}

export default App
