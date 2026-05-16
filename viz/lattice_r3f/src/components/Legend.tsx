import { IMPL_COLORS, ImplStatus, MODE_COLORS, MODE_LONG_NAMES, MODE_ORDER, Mode } from '../types/lattice';
import { useFilters } from '../store/filters';

const IMPL_ORDER: ImplStatus[] = ['implemented', 'spec_authored', 'planned', 'not_started'];

export function Legend() {
  const coverageMode = useFilters((s) => s.coverageMode);

  if (coverageMode) {
    return (
      <div style={panel}>
        <div style={titleStyle}>Coverage</div>
        {IMPL_ORDER.map((i) => (
          <Swatch key={i} color={IMPL_COLORS[i]} label={i.replace('_', ' ')} />
        ))}
      </div>
    );
  }

  return (
    <div style={panel}>
      <div style={titleStyle}>Mode</div>
      {MODE_ORDER.map((m) => (
        <Swatch key={m} color={MODE_COLORS[m]} label={`${m} · ${MODE_LONG_NAMES[m]}`} />
      ))}
    </div>
  );
}

function Swatch({ color, label }: { color: string; label: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, fontSize: 11 }}>
      <span style={{ width: 12, height: 12, borderRadius: 2, background: color }} />
      <span style={{ color: '#e5e5e5' }}>{label}</span>
    </div>
  );
}

const titleStyle: React.CSSProperties = {
  fontSize: 10, color: '#94a3b8',
  textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 6,
};

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
