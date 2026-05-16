// Shape of one entry in viz/lattice_index.json.
// Source of truth: lattice/generator.py write_index().

export type Mode = 'PYTHON_ONLY' | 'HYBRID' | 'AGENT_BOUNDED' | 'LLM_AGENT_FREE';

export interface LatticeCell {
  cell_id: string;
  altitude: string;            // "L1".."L7"
  altitude_index: number;      // 0..6, L1=0
  diamond_y: string;           // "D1" | "D2" | "D3"
  step_y: string;              // "I1" | "Q1" | "R" | "S" | "Q2" | "P" | "I2"
  confidence_element_z: string; // "RAW" | "ADJ_FAILURE" | "ADJ_VOLUME"
  step_z: string;              // same as step_y values
  bms: number;
  mode: Mode;
  contribution: number;
}

export const MODE_COLORS: Record<Mode, string> = {
  PYTHON_ONLY: '#22c55e',
  HYBRID: '#eab308',
  AGENT_BOUNDED: '#f97316',
  LLM_AGENT_FREE: '#ef4444',
};

export const ALTITUDE_ORDER = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'] as const;
export const STEP_ORDER = ['I1', 'Q1', 'R', 'S', 'Q2', 'P', 'I2'] as const;
export const DIAMOND_ORDER = ['D1', 'D2', 'D3'] as const;
export const CONFIDENCE_ORDER = ['RAW', 'ADJ_FAILURE', 'ADJ_VOLUME'] as const;
