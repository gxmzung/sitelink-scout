export type SignalStatus =
  | 'EXCELLENT'
  | 'GOOD'
  | 'FAIR'
  | 'POOR'
  | 'DEAD'

export interface ScoutDevice {
  device_id: string
  zone_id: string
  ssid: string
  bssid: string
  rssi: number
  channel: number
  signal_status: SignalStatus
  received_at: string
}

export interface CoverageZone {
  zone_id: string
  device_id: string
  rssi: number
  signal_status: SignalStatus
  received_at: string
}

export interface CoverageSummary {
  total_zones: number
  covered_zones: number
  uncovered_zones: number
  dead_zones: number
  coverage_percent: number
  average_rssi: number | null
  usable_threshold_dbm: number
  zones: CoverageZone[]
}
