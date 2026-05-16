import { IMPL_COLORS, LatticeCell, MODE_COLORS, MODE_LONG_NAMES } from '../types/lattice';
import { useFilters } from '../store/filters';

interface Props {
  cells: LatticeCell[];
}

const IMPL_EMOJI: Record<string, string> = {
  implemented: '✅',
  spec_authored: '📋',
  planned: '🟡',
  not_started: '⚪',
};

export function CellPanel({ cells }: Props) {
  const selectedId = useFilters((s) => s.selectedCellId);
  const selectCell = useFilters((s) => s.selectCell);

  if (!selectedId) return null;
  const cell = cells.find((c) => c.cell_id === selectedId);
  if (!cell) return null;

  const modeColor = MODE_COLORS[cell.mode];
  const implColor = IMPL_COLORS[cell.implementation_status];

  return (
    <div style={panel}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 0.5 }}>
            Cell
          </div>
          <div style={{ fontSize: 17, fontWeight: 600, fontFamily: 'monospace', marginTop: 2 }}>
            {cell.cell_id}
          </div>
          <div style={{ fontSize: 11, color: '#94a3b8', fontFamily: 'monospace', marginTop: 1 }}>
            {cell.coordinate_id} · {cell.step}
          </div>
        </div>
        <button onClick={() => selectCell(null)} style={closeBtn}>×</button>
      </div>

      <div style={{ marginTop: 14, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        <Pill color={modeColor}>
          {cell.mode} {MODE_LONG_NAMES[cell.mode]} · BMS {cell.bms_score.toFixed(3)}
        </Pill>
        <Pill color={implColor}>
          {IMPL_EMOJI[cell.implementation_status]} {cell.implementation_status.replace('_', ' ')}
        </Pill>
      </div>

      <Row label="Archetype" value={cell.archetype} />
      <Row label="Altitude × Diamond × Step" value={`${cell.altitude} × ${cell.diamond} × ${cell.step}`} />
      <Row label="Confidence band" value={cell.confidence_band} />
      <Row label="Diamond × Step semantic" value={cell.diamond_step_semantic} small />

      <div style={{ marginTop: 14, fontSize: 11, color: '#94a3b8' }}>
        Open the full BuildCard:{' '}
        <a
          href={`https://github.com/rodgersintelligence/rig-systems-engineering-studio/blob/main/lattice/cards/${cell.cell_id}.md`}
          target="_blank"
          rel="noreferrer"
          style={{ color: modeColor }}
        >
          /lattice/cards/{cell.cell_id}.md
        </a>
      </div>
    </div>
  );
}

function Pill({ color, children }: { color: string; children: React.ReactNode }) {
  return (
    <div style={{ padding: '4px 9px', background: color, color: '#0a0a0a', borderRadius: 4, fontSize: 11, fontWeight: 600 }}>
      {children}
    </div>
  );
}

function Row({ label, value, small }: { label: string; value: string; small?: boolean }) {
  return (
    <div style={{ marginTop: 10, fontSize: small ? 11 : 12 }}>
      <div style={{ color: '#94a3b8', fontSize: 10, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
      <div style={{ color: '#e5e5e5', fontFamily: small ? 'inherit' : 'monospace', lineHeight: 1.4 }}>{value}</div>
    </div>
  );
}

const panel: React.CSSProperties = {
  position: 'absolute',
  top: 16,
  right: 16,
  width: 340,
  padding: 16,
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  color: '#e5e5e5',
  zIndex: 10,
};

const closeBtn: React.CSSProperties = {
  background: 'transparent',
  color: '#94a3b8',
  border: 'none',
  fontSize: 22,
  cursor: 'pointer',
  lineHeight: 1,
};
