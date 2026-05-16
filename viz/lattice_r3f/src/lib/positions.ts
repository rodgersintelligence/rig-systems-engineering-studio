import { DIAMOND_ORDER, LatticeCell, MODE_ORDER, STEP_ORDER } from '../types/lattice';

const stepIdx = new Map<string, number>(STEP_ORDER.map((s, i) => [s, i]));
const diamondIdx = new Map<string, number>(DIAMOND_ORDER.map((d, i) => [d, i]));
const modeIdx = new Map<string, number>(MODE_ORDER.map((m, i) => [m, i]));

/** Map a cell to (x, y, z) grid coordinates.
 *
 * X = altitude_index           (0..6,  7 wide)
 * Y = diamond * 7 + step       (0..20, 21 tall)
 * Z = mode_index               (0..3,  4 deep)
 */
export function cellGridPosition(cell: LatticeCell): [number, number, number] {
  const x = cell.altitude_index;
  const y = (diamondIdx.get(cell.diamond) ?? 0) * 7 + (stepIdx.get(cell.step) ?? 0);
  const z = modeIdx.get(cell.mode) ?? 0;
  return [x, y, z];
}

/** Center the grid roughly at origin so OrbitControls feel natural. */
export function gridCenter(): [number, number, number] {
  return [3, 10, 1.5];
}
