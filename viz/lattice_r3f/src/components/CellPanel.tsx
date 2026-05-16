import { LatticeCell, MODE_COLORS, Mode } from '../types/lattice';
import { useFilters } from '../store/filters';

interface Props {
  cells: LatticeCell[];
}

export function CellPanel({ cells }: Props) {
  const selectedId = useFilters((s) => s.selectedCellId);
  const selectCell = useFilters((s) => s.selectCell);

  if (!selectedId) return null;
  const cell = cells.find((c) => c.cell_id === selectedId);
  if (!cell) return null;

  const accent = MODE_COLORS[cell.mode as Mode];

  return (
    <div style={panel}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ fontSize: 11, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 0.5 }}>
            Cell
          </div>
          <div style={{ fontSize: 18, fontWeight: 600, fontFamily: 'monospace', marginTop: 2 }}>
            {cell.cell_id}
          </div>
        </div>
        <button onClick={() => selectCell(null)} style={closeBtn}>×</button>
      </div>

      <div style={{ marginTop: 14, padding: '6px 10px', background: accent, color: '#0a0a0a', borderRadius: 4, fontSize: 12, fontWeight: 600, display: 'inline-block' }}>
        {cell.mode}  ·  BMS {cell.bms.toFixed(3)}
      </div>

      <Row label="X / Altitude" value={cell.altitude} />
      <Row label="Y / Diamond.Step" value={`${cell.diamond_y}.${cell.step_y}`} />
      <Row label="Z / Confidence.Step" value={`${cell.confidence_element_z}.${cell.step_z}`} />
      <Row label="Z contribution" value={cell.contribution.toFixed(4)} />

      <div style={{ marginTop: 16, fontSize: 11, color: '#94a3b8' }}>
        Open the full BuildCard:{' '}
        <a
          href={`https://github.com/rodgersintelligence/rig-systems-engineering-studio/blob/main/lattice/cards/${cell.cell_id}.md`}
          target="_blank"
          rel="noreferrer"
          style={{ color: accent }}
        >
          /lattice/cards/{cell.cell_id}.md
        </a>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ marginTop: 10, fontSize: 12 }}>
      <div style={{ color: '#94a3b8', fontSize: 10, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
      <div style={{ color: '#e5e5e5', fontFamily: 'monospace' }}>{value}</div>
    </div>
  );
}

const panel: React.CSSProperties = {
  position: 'absolute',
  top: 16,
  right: 16,
  width: 320,
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
