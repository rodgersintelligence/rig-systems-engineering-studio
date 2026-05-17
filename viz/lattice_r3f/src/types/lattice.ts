// Shape of one entry in viz/lattice_index.json (corrected geometry).
// Source: lattice/generator.py write_index().
//
// Geometry: 7 altitudes x 3 diamonds x 4 modes x 7 IQRSQPI steps = 588 cells.

export type Mode = 'A1' | 'A2' | 'A3' | 'A4';

export type ImplStatus = 'implemented' | 'spec_authored' | 'planned' | 'not_started';

export type StretchDirection = 'aligned' | 'heavy' | 'tight';

export interface LatticeCell {
  cell_id: string;
  coordinate_id: string;       // L<n>-D<n>-A<n>

  altitude: string;            // "L1".."L7"
  altitude_index: number;      // 0..6
  altitude_name?: string;      // "Artifacts".."Vision"
  diamond: string;             // "D1" | "D2" | "D3"
  diamond_index: number;       // 0..2
  mode: Mode;
  mode_long: string;
  mode_index: number;
  step: string;
  step_index: number;

  bms_score: number;
  natural_bms_score?: number;        // real 20-criterion BMS
  natural_mode?: Mode;               // mode the rubric suggests
  bms_alignment?: number;            // natural_bms_score - mode_floor
  stretch_direction?: StretchDirection;
  confidence_band: 'HIGH' | 'MEDIUM' | 'LOW' | 'OPEN';
  archetype: string;
  implementation_status: ImplStatus;
  diamond_step_semantic: string;
}

export const MODE_COLORS: Record<Mode, string> = {
  A1: '#22c55e', // green
  A2: '#eab308', // yellow
  A3: '#f97316', // orange
  A4: '#ef4444', // red
};

export const MODE_LONG_NAMES: Record<Mode, string> = {
  A1: 'PYTHON_ONLY',
  A2: 'HYBRID',
  A3: 'AGENT_BOUNDED',
  A4: 'LLM_AGENT_FREE',
};

export const IMPL_COLORS: Record<ImplStatus, string> = {
  implemented: '#10b981',
  spec_authored: '#3b82f6',
  planned: '#a3a3a3',
  not_started: '#525252',
};

export const STRETCH_COLORS: Record<StretchDirection, string> = {
  aligned: '#22c55e',     // green — natural mode equals chosen mode
  heavy: '#a855f7',       // purple — paying for a heavier mode than rubric needs
  tight: '#f59e0b',       // amber — stretched a lighter mode upward
};

export const ALTITUDE_ORDER = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'] as const;
export const DIAMOND_ORDER = ['D1', 'D2', 'D3'] as const;
export const MODE_ORDER: Mode[] = ['A1', 'A2', 'A3', 'A4'];
export const STEP_ORDER = ['I1', 'Q1', 'R', 'S', 'Q2', 'P', 'I2'] as const;

/** Map a natural_bms_score in [0,1] to a color along a gradient. */
export function bmsGradientColor(score: number): string {
  // 0.0 (red) -> 0.25 (orange) -> 0.5 (yellow) -> 0.75 (green) -> 1.0 (teal)
  const s = Math.max(0, Math.min(1, score));
  if (s >= 0.75) return '#22c55e';      // A1 (deterministic)
  if (s >= 0.45) return '#eab308';      // A2 (hybrid)
  if (s >= 0.25) return '#f97316';      // A3 (agent)
  return '#ef4444';                      // A4 (strategic)
}
