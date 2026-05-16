import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useEffect, useState } from 'react';
import { Axes } from './components/Axes';
import { CellPanel } from './components/CellPanel';
import { Lattice } from './components/Lattice';
import { Legend } from './components/Legend';
import { Sidebar } from './components/Sidebar';
import { LatticeCell } from './types/lattice';
import { gridCenter } from './lib/positions';

const INDEX_URL = `${import.meta.env.BASE_URL}lattice_index.json`;

export default function App() {
  const [cells, setCells] = useState<LatticeCell[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(INDEX_URL)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setCells)
      .catch((e) => setError(String(e)));
  }, []);

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

        <Lattice cells={cells} />
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
    </>
  );
}

function LoadingScreen() {
  return (
    <div style={center}>
      <div>Loading 3,087 cells…</div>
    </div>
  );
}

function ErrorScreen({ error }: { error: string }) {
  return (
    <div style={center}>
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

const center: React.CSSProperties = {
  width: '100%',
  height: '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: '#e5e5e5',
  fontFamily: 'inherit',
  textAlign: 'center',
};
