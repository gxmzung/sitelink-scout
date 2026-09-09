import type { CoverageZone } from '../types/scout'
import SignalBadge from './SignalBadge'

interface Props {
  zones: CoverageZone[]
}

export default function CoverageHeatmap({ zones }: Props) {
  if (zones.length === 0) {
    return (
      <div className="empty">
        No zone measurements available.
      </div>
    )
  }

  return (
    <div className="heatmap">
      {zones.map((zone) => (
        <div
          className={`heatmap-cell signal-bg-${zone.signal_status.toLowerCase()}`}
          key={zone.zone_id}
        >
          <div>
            <strong>{zone.zone_id}</strong>
            <span>{zone.device_id}</span>
          </div>

          <div className="heatmap-value">
            {zone.rssi} dBm
          </div>

          <SignalBadge status={zone.signal_status} />
        </div>
      ))}
    </div>
  )
}
