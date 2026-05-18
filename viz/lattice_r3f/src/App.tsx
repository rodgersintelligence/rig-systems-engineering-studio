import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Axes } from './components/Axes';
import { CellPanel } from './components/CellPanel';
import { EventTicker } from './components/EventTicker';
import { Lattice } from './components/Lattice';
import type { HoveredCellInfo } from './components/Lattice';
import { Legend } from './components/Legend';
import { MemoryHoverPanel } from './components/MemoryHoverPanel';
import { RGIStatusTile } from './components/RGIStatusTile';
import { Sidebar } from './components/Sidebar';
import { V3PipelineMini } from './components/V3PipelineMini';
import { LatticeCell } from './types/lattice';
import { gridCenter } from './lib/positions';
import { useEvents } from './store/events';
import { useMemory } from './store/memory';

const INDEX_URL = `${import.meta.env.BASE_URL}lattice_index.json`;

// Runtime server base URL for memory + health endpoints.
// Default: port 8780. Override via VITE_RIG_RUNTIME_URL build var or
// ?runtime=http://host:port query param.
function resolveRuntimeEndpoint(): string {
  const url = new URL(window.location.href);
  const q = url.searchParams.get('runtime');
  if (q) return q;
  const env = (import.meta as any).env?.VITE_RIG_RUNTIME_URL;
  if (env) return env;
  return 'http://localhost:8780';
}

const MEMORY_ENABLED = (import.meta as any).env?.VITE_RIG_MEMORY_ENABLED !== 'false';

export default function App() {
  const [cells, setCells] = useState<LatticeCell[]>([]);
  const [error, setError] = useState<string | null>(null);
  const connect = useEvents((s) => s.connect);
  const disconnect = useEvents((s) => s.disconnect);
  const connected = useEvents((s) => s.connected);
  const endpoint = useEvents((s) => s.endpoint);

  const memoryConnect = useMemory((s) => s.connect);

  // Hovered cell for memory panel — tracked outside the Canvas to avoid
  // causing re-renders on the 588-cell InstancedMesh.
  const [hoveredCell, setHoveredCell] = useState<HoveredCellInfo | null>(null);
  const hoverClearTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const runtimeEndpoint = resolveRuntimeEndpoint();

  useEffect(() => {
    const url = `${INDEX_URL}?v=${(import.meta as any).env?.VITE_BUILD_ID ?? Date.now()}`;
    fetch(url, { cache: 'no-store' })
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setCells)
      .catch((e) => setError(String(e)));
  }, []);

  useEffect(() => {
    // Move 5 — subscribe to the rig.runtime SSE event stream so the lattice
    // pulses when cells fire / outcomes resolve / rubric tunes. Configurable
    // via ?events=http://host:8765 query or VITE_RIG_EVENT_URL build var.
    // Silently no-ops if the runtime server isn't reachable.
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  useEffect(() => {
    // Move 10 — connect memory store on mount if enabled.
    if (MEMORY_ENABLED) {
      memoryConnect();
    }
  }, [memoryConnect]);

  const handleCellHover = (info: HoveredCellInfo | null) => {
    if (hoverClearTimer.current) {
      clearTimeout(hoverClearTimer.current);
      hoverClearTimer.current = null;
    }
    setHoveredCell(info);
  };

  const handlePanelClose = () => {
    setHoveredCell(null);
  };

  if (error) {
    return <ErrorScreen error={error} />;
  }
  if (cells.length === 0) {
    return <LoadingScreen />;
  }

  const center = gridCenter();

  return (
    <>
      <Canvas
        camera={{ position: [12, 12, 12], fov: 50, near: 0.1, far: 200 }}
        dpr={[1, 2]}
        gl={{ antialias: true, alpha: false }}
        style={{ background: '#0a0a0a' }}
      >
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 15, 10]} intensity={0.8} />
        <directionalLight position={[-10, -5, -10]} intensity={0.3} />

        <Lattice
          cells={cells}
          onCellHover={MEMORY_ENABLED ? handleCellHover : undefined}
        />
        <Axes />

        <OrbitControls
          target={center}
          enableDamping
          dampingFactor={0.08}
          minDistance={5}
          maxDistance={50}
        />
      </Canvas>

      <Sidebar cells={cells} />
      <CellPanel cells={cells} />
      <Legend />
      <EventTicker />

      {/* Move 10 — top-right status cluster: RGI health + V3 pipeline */}
      <div style={statusCluster}>
        <RGIStatusTile endpoint={runtimeEndpoint} />
        <V3PipelineMini />
      </div>

      {/* Move 10 — memory hover panel rendered as a portal so it floats above Canvas */}
      {MEMORY_ENABLED && hoveredCell &&
        createPortal(
          <MemoryHoverPanel
            coord={hoveredCell.cell.coordinate_id}
            cellId={hoveredCell.cell.cell_id}
            altitudeName={hoveredCell.cell.altitude_name}
            mouseX={hoveredCell.mouseX}
            mouseY={hoveredCell.mouseY}
            onClose={handlePanelClose}
          />,
          document.body,
        )
      }

      {/* Phase 9 — inbox link: only render when SSE runtime is connected */}
      {connected && endpoint && (
        <a
          href={`${endpoint}/inbox`}
          target="_blank"
          rel="noopener noreferrer"
          style={inboxLink}
        >
          inbox →
        </a>
      )}
    </>
  );
}

function LoadingScreen() {
  return (
    <div style={centerStyle}>
      <div>Loading 588 cells…</div>
    </div>
  );
}

function ErrorScreen({ error }: { error: string }) {
  return (
    <div style={centerStyle}>
      <div>
        <div style={{ color: '#ef4444', marginBottom: 8 }}>Failed to load lattice_index.json</div>
        <div style={{ fontSize: 12, color: '#94a3b8' }}>{error}</div>
        <div style={{ fontSize: 12, color: '#94a3b8', marginTop: 12 }}>
          Run <code style={{ color: '#22c55e' }}>python -m lattice.generator</code> to produce viz/lattice_index.json,<br />
          then copy it to <code style={{ color: '#22c55e' }}>viz/lattice_r3f/public/lattice_index.json</code>.
        </div>
      </div>
    </div>
  );
}

const inboxLink: React.CSSProperties = {
  position: 'absolute',
  bottom: 16,
  right: 16,
  fontSize: 11,
  fontFamily: 'monospace',
  color: '#10b981',
  textDecoration: 'none',
  background: 'rgba(15, 23, 42, 0.88)',
  border: '1px solid #1e293b',
  borderRadius: 4,
  padding: '3px 8px',
  zIndex: 10,
  letterSpacing: '0.02em',
};

const statusCluster: React.CSSProperties = {
  position: 'absolute',
  top: 16,
  right: 16,
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
  zIndex: 20,
  width: 240,
};

const centerStyle: React.CSSProperties = {
  width: '100%',
  height: '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: '#e5e5e5',
  fontFamily: 'inherit',
  textAlign: 'center',
};
