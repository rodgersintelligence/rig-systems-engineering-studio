import { create } from 'zustand';
import {
  ALTITUDE_ORDER, DIAMOND_ORDER, IMPL_COLORS, ImplStatus, LatticeCell,
  MODE_COLORS, MODE_ORDER, Mode, STEP_ORDER, STRETCH_COLORS,
  bmsGradientColor, driftGradientColor,
} from '../types/lattice';

export type ColorMode = 'mode' | 'coverage' | 'natural_bms' | 'stretch' | 'rubric_drift';

interface FilterState {
  modes: Set<Mode>;
  altitudes: Set<string>;
  diamonds: Set<string>;
  steps: Set<string>;
  implStatuses: Set<ImplStatus>;
  bmsRange: [number, number];

  // Visual modes
  coverageMode: boolean;             // legacy boolean kept for backwards compat
  colorMode: ColorMode;
  selectedCellId: string | null;

  toggleMode: (m: Mode) => void;
  toggleAltitude: (a: string) => void;
  toggleDiamond: (d: string) => void;
  toggleStep: (s: string) => void;
  toggleImpl: (s: ImplStatus) => void;
  setBmsRange: (r: [number, number]) => void;
  setCoverageMode: (on: boolean) => void;
  setColorMode: (m: ColorMode) => void;
  selectCell: (id: string | null) => void;
  reset: () => void;

  isCellVisible: (cell: LatticeCell) => boolean;
  colorFor: (cell: LatticeCell) => string;
}

const allModes = new Set<Mode>(MODE_ORDER);
const allAltitudes = new Set<string>(ALTITUDE_ORDER);
const allDiamonds = new Set<string>(DIAMOND_ORDER);
const allSteps = new Set<string>(STEP_ORDER);
const allImpls = new Set<ImplStatus>(
  ['implemented', 'spec_authored', 'planned', 'not_started']
);

export const useFilters = create<FilterState>((set, get) => ({
  modes: new Set(allModes),
  altitudes: new Set(allAltitudes),
  diamonds: new Set(allDiamonds),
  steps: new Set(allSteps),
  implStatuses: new Set(allImpls),
  bmsRange: [0, 1],

  coverageMode: false,
  colorMode: 'mode',
  selectedCellId: null,

  toggleMode: (m) => set((s) => {
    const next = new Set(s.modes);
    next.has(m) ? next.delete(m) : next.add(m);
    return { modes: next };
  }),
  toggleAltitude: (a) => set((s) => {
    const next = new Set(s.altitudes);
    next.has(a) ? next.delete(a) : next.add(a);
    return { altitudes: next };
  }),
  toggleDiamond: (d) => set((s) => {
    const next = new Set(s.diamonds);
    next.has(d) ? next.delete(d) : next.add(d);
    return { diamonds: next };
  }),
  toggleStep: (st) => set((s) => {
    const next = new Set(s.steps);
    next.has(st) ? next.delete(st) : next.add(st);
    return { steps: next };
  }),
  toggleImpl: (i) => set((s) => {
    const next = new Set(s.implStatuses);
    next.has(i) ? next.delete(i) : next.add(i);
    return { implStatuses: next };
  }),
  setBmsRange: (bmsRange) => set({ bmsRange }),
  setCoverageMode: (coverageMode) => set({
    coverageMode,
    colorMode: coverageMode ? 'coverage' : 'mode',
  }),
  setColorMode: (colorMode) => set({
    colorMode,
    coverageMode: colorMode === 'coverage',
  }),
  selectCell: (selectedCellId) => set({ selectedCellId }),
  reset: () => set({
    modes: new Set(allModes),
    altitudes: new Set(allAltitudes),
    diamonds: new Set(allDiamonds),
    steps: new Set(allSteps),
    implStatuses: new Set(allImpls),
    bmsRange: [0, 1],
    coverageMode: false,
    colorMode: 'mode',
    selectedCellId: null,
  }),

  isCellVisible: (cell) => {
    const s = get();
    return s.modes.has(cell.mode)
      && s.altitudes.has(cell.altitude)
      && s.diamonds.has(cell.diamond)
      && s.steps.has(cell.step)
      && s.implStatuses.has(cell.implementation_status)
      && cell.bms_score >= s.bmsRange[0] && cell.bms_score <= s.bmsRange[1];
  },

  colorFor: (cell) => {
    const s = get();
    switch (s.colorMode) {
      case 'coverage':
        return IMPL_COLORS[cell.implementation_status];
      case 'natural_bms':
        return bmsGradientColor(cell.natural_bms_score ?? cell.bms_score);
      case 'stretch':
        return STRETCH_COLORS[cell.stretch_direction ?? 'aligned'];
      case 'rubric_drift':
        return driftGradientColor(cell.rubric_drift_magnitude ?? 0);
      case 'mode':
      default:
        return MODE_COLORS[cell.mode];
    }
  },
}));
