import { useFilters } from '../store/filters';
import {
  ALTITUDE_ORDER, DIAMOND_ORDER, IMPL_COLORS, ImplStatus, LatticeCell,
  MODE_COLORS, MODE_LONG_NAMES, MODE_ORDER, Mode, STEP_ORDER,
} from '../types/lattice';

interface Props {
  cells: LatticeCell[];
}

const IMPL_ORDER: ImplStatus[] = ['implemented', 'spec_authored', 'planned', 'not_started'];

export function Sidebar({ cells }: Props) {
  const f = useFilters();
  const visible = cells.filter(f.isCellVisible);

  const byMode = (m: Mode) => visible.filter((c) => c.mode === m).length;
  const byImpl = (i: ImplStatus) => visible.filter((c) => c.implementation_status === i).length;

  return (
    <div style={panel}>
      <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 4 }}>
        RIG Lattice
      </div>
      <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 14 }}>
        7 × 3 × 4 × 7 = <b style={{ color: '#e5e5e5' }}>588 cells</b><br />
        <b style={{ color: '#e5e5e5' }}>{visible.length.toLocaleString()}</b> shown
      </div>

      <Section title="Color by">
        <Toggle
          active={f.colorMode === 'mode'}
          onClick={() => f.setColorMode('mode')}
          label="Mode (A1-A4)"
        />
        <Toggle
          active={f.colorMode === 'coverage'}
          onClick={() => f.setColorMode('coverage')}
          label="Coverage (impl)"
        />
        <Toggle
          active={f.colorMode === 'natural_bms'}
          onClick={() => f.setColorMode('natural_bms')}
          label="Natural BMS"
        />
        <Toggle
          active={f.colorMode === 'stretch'}
          onClick={() => f.setColorMode('stretch')}
          label="Stretch"
        />
      </Section>

      <Section title="Mode">
        {MODE_ORDER.map((m) => (
          <Toggle
            key={m}
            active={f.modes.has(m)}
            onClick={() => f.toggleMode(m)}
            color={MODE_COLORS[m]}
            label={`${m} ${MODE_LONG_NAMES[m]}`}
            count={byMode(m)}
          />
        ))}
      </Section>

      <Section title="Implementation status">
        {IMPL_ORDER.map((i) => (
          <Toggle
            key={i}
            active={f.implStatuses.has(i)}
            onClick={() => f.toggleImpl(i)}
            color={IMPL_COLORS[i]}
            label={i.replace('_', ' ')}
            count={byImpl(i)}
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

      <Section title="Diamond">
        {DIAMOND_ORDER.map((d) => (
          <Toggle
            key={d}
            active={f.diamonds.has(d)}
            onClick={() => f.toggleDiamond(d)}
            label={d}
          />
        ))}
      </Section>

      <Section title="IQRSQPI step">
        {STEP_ORDER.map((s) => (
          <Toggle
            key={s}
            active={f.steps.has(s)}
            onClick={() => f.toggleStep(s)}
            label={s}
          />
        ))}
      </Section>

      <Section title="BMS range">
        <div style={{ width: '100%' }}>
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
          <div style={{ fontSize: 11, color: '#94a3b8' }}>
            {f.bmsRange[0].toFixed(2)} → {f.bmsRange[1].toFixed(2)}
          </div>
        </div>
      </Section>

      <button onClick={f.reset} style={resetBtn}>Reset filters</button>

      <div style={{ marginTop: 16, fontSize: 10, color: '#64748b', lineHeight: 1.4 }}>
        Click a cube to open its BuildCard. Drag to rotate. Scroll to zoom.
        <br />
        Toggle <i>Coverage (impl)</i> to color-code which archetypes are built vs spec-only.
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ fontSize: 10, textTransform: 'uppercase', color: '#94a3b8', letterSpacing: 0.5, marginBottom: 6 }}>
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
        padding: '3px 7px',
        borderRadius: 4,
        fontSize: 11,
        cursor: 'pointer',
        fontFamily: 'inherit',
        whiteSpace: 'nowrap',
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
  width: 300,
  padding: 14,
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  color: '#e5e5e5',
  fontSize: 12,
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
  fontSize: 11,
  cursor: 'pointer',
  fontFamily: 'inherit',
  width: '100%',
  marginTop: 4,
};
