import { useFilters } from '../store/filters';
import {
  ALTITUDE_ORDER, CONFIDENCE_ORDER, DIAMOND_ORDER, LatticeCell, MODE_COLORS, Mode,
} from '../types/lattice';

interface Props {
  cells: LatticeCell[];
}

export function Sidebar({ cells }: Props) {
  const f = useFilters();
  const visible = cells.filter(f.isCellVisible);

  const byMode = (m: Mode) => visible.filter((c) => c.mode === m).length;

  return (
    <div style={panel}>
      <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>
        RIG Lattice
      </div>
      <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 16 }}>
        7 × 21 × 21 = 3,087 cells · <b style={{ color: '#e5e5e5' }}>{visible.length.toLocaleString()}</b> shown
      </div>

      <Section title="Mode">
        {(Object.keys(MODE_COLORS) as Mode[]).map((m) => (
          <Toggle
            key={m}
            active={f.modes.has(m)}
            onClick={() => f.toggleMode(m)}
            color={MODE_COLORS[m]}
            label={m}
            count={byMode(m)}
          />
        ))}
      </Section>

      <Section title="Altitude (X)">
        {ALTITUDE_ORDER.map((a) => (
          <Toggle
            key={a}
            active={f.altitudes.has(a)}
            onClick={() => f.toggleAltitude(a)}
            label={a}
          />
        ))}
      </Section>

      <Section title="Diamond (Y)">
        {DIAMOND_ORDER.map((d) => (
          <Toggle
            key={d}
            active={f.diamonds.has(d)}
            onClick={() => f.toggleDiamond(d)}
            label={d}
          />
        ))}
      </Section>

      <Section title="Confidence element (Z)">
        {CONFIDENCE_ORDER.map((c) => (
          <Toggle
            key={c}
            active={f.confidence.has(c)}
            onClick={() => f.toggleConfidence(c)}
            label={c}
          />
        ))}
      </Section>

      <Section title="BMS range">
        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={f.bmsRange[0]}
          onChange={(e) => f.setBmsRange([parseFloat(e.target.value), f.bmsRange[1]])}
          style={{ width: '100%' }}
        />
        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={f.bmsRange[1]}
          onChange={(e) => f.setBmsRange([f.bmsRange[0], parseFloat(e.target.value)])}
          style={{ width: '100%' }}
        />
        <div style={{ fontSize: 12, color: '#94a3b8' }}>
          {f.bmsRange[0].toFixed(2)} → {f.bmsRange[1].toFixed(2)}
        </div>
      </Section>

      <button onClick={f.reset} style={resetBtn}>Reset filters</button>

      <div style={{ marginTop: 24, fontSize: 11, color: '#64748b' }}>
        Click a cell to open its card. Drag to rotate. Scroll to zoom.
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 11, textTransform: 'uppercase', color: '#94a3b8', letterSpacing: 0.5, marginBottom: 6 }}>
        {title}
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>{children}</div>
    </div>
  );
}

function Toggle({
  active, onClick, label, color, count,
}: {
  active: boolean; onClick: () => void; label: string; color?: string; count?: number;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        background: active ? (color ?? '#1e293b') : 'transparent',
        color: active ? (color ? '#0a0a0a' : '#e5e5e5') : '#64748b',
        border: `1px solid ${active ? (color ?? '#475569') : '#334155'}`,
        padding: '4px 8px',
        borderRadius: 4,
        fontSize: 11,
        cursor: 'pointer',
        fontFamily: 'inherit',
      }}
    >
      {label}{count !== undefined ? ` (${count.toLocaleString()})` : ''}
    </button>
  );
}

const panel: React.CSSProperties = {
  position: 'absolute',
  top: 16,
  left: 16,
  width: 280,
  padding: 16,
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  color: '#e5e5e5',
  fontSize: 13,
  zIndex: 10,
  maxHeight: 'calc(100vh - 32px)',
  overflowY: 'auto',
};

const resetBtn: React.CSSProperties = {
  background: '#1e293b',
  color: '#e5e5e5',
  border: '1px solid #334155',
  padding: '6px 12px',
  borderRadius: 4,
  fontSize: 12,
  cursor: 'pointer',
  fontFamily: 'inherit',
  width: '100%',
  marginTop: 8,
};
