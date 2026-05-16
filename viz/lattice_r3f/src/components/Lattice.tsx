import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { LatticeCell } from '../types/lattice';
import { cellGridPosition } from '../lib/positions';
import { useFilters } from '../store/filters';

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

  useEffect(() => {
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
  }, [cells, filters, dummy, color, isCellVisible, colorFor]);

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
