import { create } from 'zustand';

// Live event surface — Move 5. The viewer subscribes to the FastAPI SSE
// stream at `${RIG_EVENT_URL}/events/stream`. Each event tags one cell;
// the Lattice component animates a pulse on that cell for ~3s.
//
// Configure via `?events=http://your-host:8765` query string or the
// VITE_RIG_EVENT_URL build var. Default: localhost:8765 (rig.runtime server).

export interface LiveEvent {
  id: string;
  ts: string;
  kind: string;
  cell_id: string | null;
  source: string;
  payload: Record<string, any>;
}

interface CellPulse {
  cell_id: string;
  kind: string;
  ts: number;       // monotonic ms — when the pulse started
  decay_ms: number; // how long the pulse should be visible
}

interface EventsState {
  connected: boolean;
  endpoint: string;
  recentEvents: LiveEvent[];
  pulses: Record<string, CellPulse>;
  totalSeen: number;

  connect: (endpoint?: string) => void;
  disconnect: () => void;
  pushEvent: (e: LiveEvent) => void;
  pulseFor: (cell_id: string) => number;  // 0..1 intensity
  prune: () => void;
}

const PULSE_DECAY: Record<string, number> = {
  'cell.started': 5000,
  'cell.completed': 4000,
  'cell.failed': 6000,
  'publisher.completed': 2500,
  'prediction.scheduled': 2000,
  'prediction.resolved': 5000,
  'rubric.tuned': 8000,
};

let _eventSource: EventSource | null = null;

function resolveEndpoint(explicit?: string): string {
  if (explicit) return explicit;
  const url = new URL(window.location.href);
  const q = url.searchParams.get('events');
  if (q) return q;
  const env = (import.meta as any).env?.VITE_RIG_EVENT_URL;
  if (env) return env;
  return 'http://localhost:8765';
}

export const useEvents = create<EventsState>((set, get) => ({
  connected: false,
  endpoint: '',
  recentEvents: [],
  pulses: {},
  totalSeen: 0,

  connect: (endpoint?: string) => {
    const url = resolveEndpoint(endpoint);
    if (_eventSource) {
      try { _eventSource.close(); } catch {}
    }
    try {
      const es = new EventSource(`${url}/events/stream`);
      _eventSource = es;
      set({ endpoint: url, connected: false });

      es.onopen = () => set({ connected: true });
      es.onerror = () => set({ connected: false });

      const handler = (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data) as LiveEvent;
          get().pushEvent(data);
        } catch { /* malformed */ }
      };
      // Listen to known kinds + the generic message event.
      ['cell.started', 'cell.completed', 'cell.failed', 'publisher.completed',
       'prediction.scheduled', 'prediction.resolved', 'rubric.tuned',
       'cell.scheduled'].forEach((k) => es.addEventListener(k, handler));
      es.onmessage = handler;
    } catch {
      set({ connected: false });
    }
  },

  disconnect: () => {
    if (_eventSource) {
      try { _eventSource.close(); } catch {}
      _eventSource = null;
    }
    set({ connected: false });
  },

  pushEvent: (evt) => set((s) => {
    const recent = [evt, ...s.recentEvents].slice(0, 80);
    const pulses = { ...s.pulses };
    if (evt.cell_id) {
      pulses[evt.cell_id] = {
        cell_id: evt.cell_id,
        kind: evt.kind,
        ts: performance.now(),
        decay_ms: PULSE_DECAY[evt.kind] ?? 3000,
      };
    }
    return { recentEvents: recent, pulses, totalSeen: s.totalSeen + 1 };
  }),

  pulseFor: (cell_id) => {
    const p = get().pulses[cell_id];
    if (!p) return 0;
    const age = performance.now() - p.ts;
    if (age >= p.decay_ms) return 0;
    return 1 - age / p.decay_ms;
  },

  prune: () => set((s) => {
    const now = performance.now();
    const next: Record<string, CellPulse> = {};
    for (const [k, p] of Object.entries(s.pulses)) {
      if (now - p.ts < p.decay_ms) next[k] = p;
    }
    return { pulses: next };
  }),
}));
