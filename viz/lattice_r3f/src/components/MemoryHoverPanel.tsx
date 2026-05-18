// Move 10 — Memory hover panel.
// Shown next to the cursor when a lattice cell has been hovered for > 400ms.
// Calls useMemory.recall(coord) and renders top-3 results.
// Controlled entirely by the hoveredCell state atom passed from Lattice via App.
import { useEffect, useRef, useState } from 'react';
import { useMemory } from '../store/memory';
import type { RecallResult } from '../store/memory';

interface Props {
  coord: string;       // coordinate_id of the hovered cell, e.g. "L3-D1-A2"
  cellId: string;      // cell_id for the header
  altitudeName?: string;
  mouseX: number;
  mouseY: number;
  onClose: () => void;
}

export function MemoryHoverPanel({ coord, cellId, altitudeName, mouseX, mouseY, onClose }: Props) {
  const recall = useMemory((s) => s.recall);
  const enabled = useMemory((s) => s.enabled);
  const backend = useMemory((s) => s.backend);
  const rowsTotal = useMemory((s) => s.rowsTotal);

  const [results, setResults] = useState<RecallResult[]>([]);
  const [loading, setLoading] = useState(true);
  const fetchedRef = useRef<string | null>(null);

  useEffect(() => {
    if (fetchedRef.current === coord) return;
    fetchedRef.current = coord;
    setLoading(true);
    recall(coord).then((r) => {
      setResults(r);
      setLoading(false);
    });
  }, [coord, recall]);

  // Offset panel so it doesn't sit directly under cursor.
  const panelX = mouseX + 16;
  const panelY = mouseY - 12;

  const altLabel = altitudeName ? ` · ${altitudeName}` : '';

  return (
    <div
      style={{
        ...panel,
        left: panelX,
        top: panelY,
      }}
      onPointerEnter={(e) => e.stopPropagation()}
    >
      {/* Header */}
      <div style={headerRow}>
        <div>
          <div style={{ fontSize: 10, color: '#64748b', textTransform: 'uppercase', letterSpacing: 0.5 }}>
            Memory recall
          </div>
          <div style={{ fontSize: 12, fontWeight: 600, fontFamily: 'monospace', marginTop: 2, color: '#e5e5e5' }}>
            {cellId}
          </div>
          <div style={{ fontSize: 10, color: '#94a3b8', fontFamily: 'monospace' }}>
            {coord}{altLabel}
          </div>
        </div>
        <button onClick={onClose} style={closeBtn}>×</button>
      </div>

      {/* Body */}
      <div style={{ marginTop: 8 }}>
        {!enabled ? (
          <div style={offlineMsg}>memory offline</div>
        ) : loading ? (
          <div style={offlineMsg}>loading…</div>
        ) : results.length === 0 ? (
          <div style={offlineMsg}>no memories indexed for this coord</div>
        ) : (
          results.map((r, i) => (
            <div key={i} style={resultRow}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                <span style={{ fontSize: 10, fontFamily: 'monospace', color: '#10b981', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: 170 }}>
                  {r.source}
                </span>
                <span style={{ fontSize: 10, color: '#64748b', flexShrink: 0, marginLeft: 6 }}>
                  d={r.distance.toFixed(3)}
                </span>
              </div>
              <div style={{ fontSize: 11, color: '#cbd5e1', marginTop: 2, lineHeight: 1.4, wordBreak: 'break-word' }}>
                {r.snippet || '—'}
              </div>
              {r.timestamp && (
                <div style={{ fontSize: 9, color: '#475569', marginTop: 2 }}>
                  {formatTs(r.timestamp)}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div style={footer}>
        <span style={{ color: '#475569' }}>backend: </span>
        <span style={{ color: '#94a3b8' }}>{backend ?? 'unknown'}</span>
        <span style={{ color: '#334155', margin: '0 6px' }}>·</span>
        <span style={{ color: '#475569' }}>{rowsTotal.toLocaleString()} rows indexed</span>
      </div>
    </div>
  );
}

function formatTs(ts: string): string {
  try {
    return new Date(ts).toLocaleString();
  } catch {
    return ts;
  }
}

const panel: React.CSSProperties = {
  position: 'fixed',
  width: 280,
  padding: '10px 12px',
  background: 'rgba(15, 23, 42, 0.96)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  zIndex: 40,
  pointerEvents: 'auto',
  fontFamily: 'system-ui, sans-serif',
  boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
};

const headerRow: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'flex-start',
  borderBottom: '1px solid #1e293b',
  paddingBottom: 8,
};

const closeBtn: React.CSSProperties = {
  background: 'transparent',
  color: '#94a3b8',
  border: 'none',
  fontSize: 18,
  cursor: 'pointer',
  lineHeight: 1,
  padding: 0,
  marginTop: -2,
};

const resultRow: React.CSSProperties = {
  padding: '6px 0',
  borderBottom: '1px solid #0f172a',
};

const footer: React.CSSProperties = {
  marginTop: 8,
  paddingTop: 6,
  borderTop: '1px solid #1e293b',
  fontSize: 10,
  color: '#475569',
};

const offlineMsg: React.CSSProperties = {
  fontSize: 11,
  color: '#475569',
  padding: '6px 0',
  fontStyle: 'italic',
};
