import type {
  CoverageSummary,
  ScoutDevice,
} from '../types/scout'

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'
).replace(/\/$/, '')

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`)

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status}`
    )
  }

  return response.json()
}

export function getDevices(): Promise<ScoutDevice[]> {
  return request<ScoutDevice[]>('/devices')
}

export function getCoverage(): Promise<CoverageSummary> {
  return request<CoverageSummary>('/coverage')
}

export function getHealth() {
  return request<{
    status: string
    service: string
    version: string
  }>('/health')
}
