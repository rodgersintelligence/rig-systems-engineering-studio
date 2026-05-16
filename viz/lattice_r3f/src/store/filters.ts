import { create } from 'zustand';
import {
  ALTITUDE_ORDER, CONFIDENCE_ORDER, DIAMOND_ORDER, LatticeCell, MODE_COLORS, Mode,
} from '../types/lattice';

interface FilterState {
  modes: Set<Mode>;
  altitudes: Set<string>;
  diamonds: Set<string>;
  confidence: Set<string>;
  bmsRange: [number, number];
  selectedCellId: string | null;

  toggleMode: (m: Mode) => void;
  toggleAltitude: (a: string) => void;
  toggleDiamond: (d: string) => void;
  toggleConfidence: (c: string) => void;
  setBmsRange: (r: [number, number]) => void;
  selectCell: (id: string | null) => void;
  reset: () => void;

  isCellVisible: (cell: LatticeCell) => boolean;
}

const allModes = new Set(Object.keys(MODE_COLORS) as Mode[]);
const allAltitudes = new Set(ALTITUDE_ORDER);
const allDiamonds = new Set(DIAMOND_ORDER);
const allConfidence = new Set(CONFIDENCE_ORDER);

export const useFilters = create<FilterState>((set, get) => ({
  modes: new Set(allModes),
  altitudes: new Set(allAltitudes),
  diamonds: new Set(allDiamonds),
  confidence: new Set(allConfidence),
  bmsRange: [0, 1],
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
  toggleConfidence: (c) => set((s) => {
    const next = new Set(s.confidence);
    next.has(c) ? next.delete(c) : next.add(c);
    return { confidence: next };
  }),
  setBmsRange: (bmsRange) => set({ bmsRange }),
  selectCell: (selectedCellId) => set({ selectedCellId }),
  reset: () => set({
    modes: new Set(allModes),
    altitudes: new Set(allAltitudes),
    diamonds: new Set(allDiamonds),
    confidence: new Set(allConfidence),
    bmsRange: [0, 1],
    selectedCellId: null,
  }),

  isCellVisible: (cell) => {
    const s = get();
    return s.modes.has(cell.mode as Mode)
      && s.altitudes.has(cell.altitude)
      && s.diamonds.has(cell.diamond_y)
      && s.confidence.has(cell.confidence_element_z)
      && cell.bms >= s.bmsRange[0] && cell.bms <= s.bmsRange[1];
  },
}));
