import type { ScoutDevice } from '../types/scout'
import SignalBadge from './SignalBadge'

interface Props {
  scout: ScoutDevice
}

export default function ScoutCard({ scout }: Props) {
  return (
    <article className="scout-card">
      <div className="scout-card-header">
        <div>
          <p className="eyebrow">{scout.zone_id}</p>
          <h3>{scout.device_id}</h3>
        </div>

        <SignalBadge status={scout.signal_status} />
      </div>

      <div className="scout-rssi">
        {scout.rssi}
        <span>dBm</span>
      </div>

      <dl className="scout-meta">
        <div>
          <dt>SSID</dt>
          <dd>{scout.ssid}</dd>
        </div>

        <div>
          <dt>Channel</dt>
          <dd>{scout.channel}</dd>
        </div>

        <div>
          <dt>BSSID</dt>
          <dd>{scout.bssid}</dd>
        </div>
      </dl>
    </article>
  )
}
