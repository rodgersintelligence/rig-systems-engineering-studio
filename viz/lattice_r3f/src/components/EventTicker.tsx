// Move 5 — live event ticker. Bottom-left HUD that streams the last 12
// rig.runtime events. Click a row to focus the viewer on the cell.
import { useEvents } from '../store/events';
import { useFilters } from '../store/filters';

const KIND_COLOR: Record<string, string> = {
  'cell.scheduled': '#94a3b8',
  'cell.started': '#22c55e',
  'cell.completed': '#22c55e',
  'cell.failed': '#ef4444',
  'publisher.completed': '#eab308',
  'prediction.scheduled': '#3b82f6',
  'prediction.resolved': '#10b981',
  'rubric.tuned': '#a855f7',
};

export function EventTicker() {
  const recent = useEvents((s) => s.recentEvents);
  const connected = useEvents((s) => s.connected);
  const endpoint = useEvents((s) => s.endpoint);
  const totalSeen = useEvents((s) => s.totalSeen);
  const selectCell = useFilters((s) => s.selectCell);

  const visible = recent.slice(0, 12);

  return (
    <div style={panel}>
      <div style={header}>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <span style={{
            width: 8, height: 8, borderRadius: 4,
            background: connected ? '#22c55e' : '#525252',
          }} />
          <span style={{ fontSize: 11, color: connected ? '#22c55e' : '#94a3b8' }}>
            {connected ? 'live' : 'offline'}
          </span>
        </div>
        <div style={{ fontSize: 10, color: '#64748b' }}>
          {totalSeen.toLocaleString()} events · {endpoint || 'no endpoint'}
        </div>
      </div>
      {visible.length === 0 ? (
        <div style={{ fontSize: 11, color: '#64748b', padding: '6px 4px' }}>
          {connected
            ? 'waiting for events…'
            : 'no rig.runtime server reachable. start with: `uvicorn rig.runtime.server:app --host 0.0.0.0 --port 8765`'}
        </div>
      ) : visible.map((e) => (
        <div
          key={e.id}
          onClick={() => e.cell_id && selectCell(e.cell_id)}
          style={{
            display: 'grid',
            gridTemplateColumns: '8px 1fr auto',
            gap: 8,
            alignItems: 'center',
            padding: '2px 4px',
            fontSize: 11,
            cursor: e.cell_id ? 'pointer' : 'default',
            borderRadius: 3,
          }}
          title={JSON.stringify(e.payload).slice(0, 200)}
        >
          <span style={{
            width: 8, height: 8, borderRadius: 4,
            background: KIND_COLOR[e.kind] || '#94a3b8',
          }} />
          <span style={{ fontFamily: 'monospace', color: '#e5e5e5', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            <span style={{ color: KIND_COLOR[e.kind] || '#94a3b8' }}>{e.kind}</span>
            {e.cell_id ? <span style={{ color: '#cbd5e1' }}> · {e.cell_id}</span> : null}
          </span>
          <span style={{ color: '#64748b', fontSize: 10 }}>
            {new Date(e.ts).toLocaleTimeString()}
          </span>
        </div>
      ))}
    </div>
  );
}

const panel: React.CSSProperties = {
  position: 'absolute',
  bottom: 16,
  left: 16,
  width: 360,
  padding: 10,
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  zIndex: 10,
  maxHeight: 280,
  overflow: 'hidden',
};

const header: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: 6,
  paddingBottom: 4,
  borderBottom: '1px solid #1e293b',
};
