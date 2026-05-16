// Shape of one entry in viz/lattice_index.json (corrected geometry).
// Source: lattice/generator.py write_index().
//
// Geometry: 7 altitudes x 3 diamonds x 4 modes x 7 IQRSQPI steps = 588 cells.

export type Mode = 'A1' | 'A2' | 'A3' | 'A4';

export type ImplStatus = 'implemented' | 'spec_authored' | 'planned' | 'not_started';

export interface LatticeCell {
  cell_id: string;
  coordinate_id: string;       // L<n>-D<n>-A<n>

  altitude: string;            // "L1".."L7"
  altitude_index: number;      // 0..6
  diamond: string;             // "D1" | "D2" | "D3"
  diamond_index: number;       // 0..2
  mode: Mode;
  mode_long: string;           // "PYTHON_ONLY" | "HYBRID" | "AGENT_BOUNDED" | "LLM_AGENT_FREE"
  mode_index: number;          // 0..3
  step: string;                // "I1" | "Q1" | "R" | "S" | "Q2" | "P" | "I2"
  step_index: number;          // 0..6

  bms_score: number;
  confidence_band: 'HIGH' | 'MEDIUM' | 'LOW' | 'OPEN';
  archetype: string;           // "A1.7"
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
  implemented: '#10b981',     // teal
  spec_authored: '#3b82f6',   // blue
  planned: '#a3a3a3',         // gray
  not_started: '#525252',     // dark gray
};

export const ALTITUDE_ORDER = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'] as const;
export const DIAMOND_ORDER = ['D1', 'D2', 'D3'] as const;
export const MODE_ORDER: Mode[] = ['A1', 'A2', 'A3', 'A4'];
export const STEP_ORDER = ['I1', 'Q1', 'R', 'S', 'Q2', 'P', 'I2'] as const;
