import { CONFIDENCE_ORDER, DIAMOND_ORDER, LatticeCell, STEP_ORDER } from '../types/lattice';

const stepIdx = new Map(STEP_ORDER.map((s, i) => [s, i]));
const diamondIdx = new Map(DIAMOND_ORDER.map((d, i) => [d, i]));
const confIdx = new Map(CONFIDENCE_ORDER.map((c, i) => [c, i]));

/** Map a cell to (x, y, z) grid coordinates in [0..6, 0..20, 0..20]. */
export function cellGridPosition(cell: LatticeCell): [number, number, number] {
  const x = cell.altitude_index;
  const y = (diamondIdx.get(cell.diamond_y) ?? 0) * 7 + (stepIdx.get(cell.step_y) ?? 0);
  const z = (confIdx.get(cell.confidence_element_z) ?? 0) * 7 + (stepIdx.get(cell.step_z) ?? 0);
  return [x, y, z];
}

/** Center the grid roughly at origin so OrbitControls feel natural. */
export function gridCenter(): [number, number, number] {
  return [3, 10, 10];
}
