import { useEffect, useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { LatticeCell } from '../types/lattice';
import { cellGridPosition } from '../lib/positions';
import { useFilters } from '../store/filters';
import { useEvents } from '../store/events';

interface Props {
  cells: LatticeCell[];
}

const SCALE_MIN = 0.2;
const SCALE_MAX = 0.85;

export function Lattice({ cells }: Props) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const isCellVisible = useFilters((s) => s.isCellVisible);
  const colorFor = useFilters((s) => s.colorFor);
  const selectCell = useFilters((s) => s.selectCell);
  const filters = useFilters();

  const geo = useMemo(() => new THREE.BoxGeometry(1, 1, 1), []);
  const mat = useMemo(() => new THREE.MeshStandardMaterial({
    transparent: true,
    roughness: 0.4,
    metalness: 0.05,
    vertexColors: false,
  }), []);

  const dummy = useMemo(() => new THREE.Object3D(), []);
  const color = useMemo(() => new THREE.Color(), []);

  // Static layout (mode/color/visibility) — recompute when filters change.
  const renderLayout = () => {
    const mesh = meshRef.current;
    if (!mesh) return;
    cells.forEach((cell, i) => {
      const [x, y, z] = cellGridPosition(cell);
      dummy.position.set(x, y, z);
      const visible = isCellVisible(cell);
      const scale = visible
        ? SCALE_MIN + cell.bms_score * (SCALE_MAX - SCALE_MIN)
        : SCALE_MIN * 0.4;
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);

      color.set(colorFor(cell));
      if (!visible) color.multiplyScalar(0.18);
      mesh.setColorAt(i, color);
    });
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  };

  useEffect(renderLayout, [cells, filters, dummy, color, isCellVisible, colorFor]);

  // Per-frame: overlay live pulses on cells that just emitted events.
  const pulseFor = useEvents((s) => s.pulseFor);
  const prune = useEvents((s) => s.prune);
  const baseColor = useMemo(() => new THREE.Color(), []);
  const pulseColor = useMemo(() => new THREE.Color('#ffffff'), []);

  useFrame(() => {
    const mesh = meshRef.current;
    if (!mesh) return;
    let anyPulse = false;
    cells.forEach((cell, i) => {
      const intensity = pulseFor(cell.cell_id);
      if (intensity <= 0) return;
      anyPulse = true;
      baseColor.set(colorFor(cell));
      const visible = isCellVisible(cell);
      if (!visible) baseColor.multiplyScalar(0.18);
      baseColor.lerp(pulseColor, intensity * 0.8);
      mesh.setColorAt(i, baseColor);

      const [x, y, z] = cellGridPosition(cell);
      dummy.position.set(x, y, z);
      const scaleBase = visible
        ? SCALE_MIN + cell.bms_score * (SCALE_MAX - SCALE_MIN)
        : SCALE_MIN * 0.4;
      dummy.scale.setScalar(scaleBase * (1 + intensity * 0.6));
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    });
    if (anyPulse) {
      mesh.instanceMatrix.needsUpdate = true;
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
    } else {
      // Periodically prune expired pulses.
      prune();
    }
  });

  const handleClick = (e: any) => {
    e.stopPropagation();
    const id = cells[e.instanceId]?.cell_id;
    if (id) selectCell(id);
  };

  return (
    <instancedMesh
      ref={meshRef}
      args={[geo, mat, cells.length]}
      onClick={handleClick}
    />
  );
}
