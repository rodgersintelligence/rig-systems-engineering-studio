import {
  IMPL_COLORS, ImplStatus, MODE_COLORS, MODE_LONG_NAMES, MODE_ORDER, Mode,
  STRETCH_COLORS, StretchDirection,
} from '../types/lattice';
import { useFilters } from '../store/filters';

const IMPL_ORDER: ImplStatus[] = ['implemented', 'spec_authored', 'planned', 'not_started'];
const STRETCH_ORDER: StretchDirection[] = ['aligned', 'heavy', 'tight'];

const STRETCH_LABELS: Record<StretchDirection, string> = {
  aligned: 'aligned (mode matches rubric)',
  heavy: 'heavy (chose stronger mode than needed)',
  tight: 'tight (chose lighter mode than rubric)',
};

const NATURAL_BMS_RANGES: { label: string; color: string }[] = [
  { label: '≥ 0.75 → A1 PYTHON_ONLY', color: '#22c55e' },
  { label: '0.45–0.74 → A2 HYBRID', color: '#eab308' },
  { label: '0.25–0.44 → A3 AGENT_BOUNDED', color: '#f97316' },
  { label: '< 0.25 → A4 LLM_AGENT_FREE', color: '#ef4444' },
];

export function Legend() {
  const colorMode = useFilters((s) => s.colorMode);

  let title = 'Mode';
  let swatches: { color: string; label: string }[] = MODE_ORDER.map((m) => ({
    color: MODE_COLORS[m],
    label: `${m} · ${MODE_LONG_NAMES[m]}`,
  }));

  if (colorMode === 'coverage') {
    title = 'Coverage';
    swatches = IMPL_ORDER.map((i) => ({ color: IMPL_COLORS[i], label: i.replace('_', ' ') }));
  } else if (colorMode === 'natural_bms') {
    title = 'Natural BMS (20-criterion rubric)';
    swatches = NATURAL_BMS_RANGES;
  } else if (colorMode === 'stretch') {
    title = 'Stretch direction';
    swatches = STRETCH_ORDER.map((s) => ({
      color: STRETCH_COLORS[s],
      label: STRETCH_LABELS[s],
    }));
  }

  return (
    <div style={panel}>
      <div style={titleStyle}>{title}</div>
      {swatches.map((s) => (
        <Swatch key={s.label} color={s.color} label={s.label} />
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
  maxWidth: 320,
};
