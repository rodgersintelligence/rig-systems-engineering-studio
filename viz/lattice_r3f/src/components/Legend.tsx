import { MODE_COLORS, Mode } from '../types/lattice';

export function Legend() {
  return (
    <div style={panel}>
      <div style={{ fontSize: 11, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 6 }}>
        Mode
      </div>
      {(Object.keys(MODE_COLORS) as Mode[]).map((m) => (
        <div key={m} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, fontSize: 12 }}>
          <span style={{ width: 12, height: 12, borderRadius: 2, background: MODE_COLORS[m] }} />
          <span style={{ color: '#e5e5e5' }}>{m}</span>
        </div>
      ))}
    </div>
  );
}

const panel: React.CSSProperties = {
  position: 'absolute',
  bottom: 16,
  right: 16,
  padding: 12,
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  zIndex: 10,
};
