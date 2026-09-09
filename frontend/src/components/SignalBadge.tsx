import type { SignalStatus } from '../types/scout'

interface Props {
  status: SignalStatus
}

export default function SignalBadge({ status }: Props) {
  return (
    <span className={`signal-badge signal-${status.toLowerCase()}`}>
      {status}
    </span>
  )
}
