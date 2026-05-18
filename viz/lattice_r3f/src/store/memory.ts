// RGI Memory Graph integration — Move 10.
// Connects to the private runtime server's /memory/* endpoints.
// Soft-fails to enabled=false if the server is unreachable.
import { create } from 'zustand';
import { useEvents } from './events';

export interface RecallResult {
  source: string;
  distance: number;
  snippet: string;      // first 80 chars of content
  timestamp: string;
  metadata: Record<string, unknown>;
}

interface MemoryState {
  enabled: boolean;
  backend: 'pgvector' | 'sqlite' | 'hash' | null;
  rowsTotal: number;
  lastEmbedAt: string | null;
  recallCache: Map<string, { results: RecallResult[]; cachedAt: number }>;
  recallInflight: Set<string>;

  connect: () => Promise<void>;
  refreshStatus: () => Promise<void>;
  recall: (coord: string) => Promise<RecallResult[]>;
}

const CACHE_TTL_MS = 60_000;

function resolveMemoryEndpoint(): string {
  // Reuse the same base endpoint as the events store, but allow an override.
  const env = (import.meta as any).env?.VITE_RIG_MEMORY_URL;
  if (env) return env;
  // Fall back to the events endpoint base (strip any trailing path).
  // We do this lazily at call-time since events store may not be initialized yet.
  return 'http://localhost:8780';
}

function getEndpoint(): string {
  // Try to read from events store first for consistent base URL.
  try {
    const eventsEndpoint = useEvents.getState().endpoint;
    if (eventsEndpoint) {
      // The events endpoint may be port 8765; memory is on 8780 by default.
      // Use explicit override only, otherwise stick with 8780.
      return resolveMemoryEndpoint();
    }
  } catch { /* not initialized */ }
  return resolveMemoryEndpoint();
}

export const useMemory = create<MemoryState>((set, get) => ({
  enabled: false,
  backend: null,
  rowsTotal: 0,
  lastEmbedAt: null,
  recallCache: new Map(),
  recallInflight: new Set(),

  connect: async () => {
    await get().refreshStatus();
  },

  refreshStatus: async () => {
    const base = getEndpoint();
    try {
      const r = await fetch(`${base}/memory/status`, { signal: AbortSignal.timeout(4000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      set({
        enabled: true,
        backend: data.backend ?? null,
        rowsTotal: data.row_count ?? data.rows_total ?? 0,
        lastEmbedAt: data.last_embed_at ?? null,
      });
    } catch {
      set({ enabled: false });
    }
  },

  recall: async (coord: string): Promise<RecallResult[]> => {
    const state = get();
    const cached = state.recallCache.get(coord);
    if (cached && Date.now() - cached.cachedAt < CACHE_TTL_MS) {
      return cached.results;
    }
    if (state.recallInflight.has(coord)) {
      // Another call is in flight — poll briefly or return empty.
      return [];
    }

    const base = getEndpoint();
    set((s) => {
      const next = new Set(s.recallInflight);
      next.add(coord);
      return { recallInflight: next };
    });

    try {
      const r = await fetch(
        `${base}/memory/recall?coord=${encodeURIComponent(coord)}&k=3`,
        { signal: AbortSignal.timeout(6000) },
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();

      // Normalise: server may return { results: [...] } or a raw array.
      const raw: any[] = Array.isArray(data) ? data : (data.results ?? []);
      const results: RecallResult[] = raw.map((item: any) => ({
        source: item.source ?? item.id ?? 'unknown',
        distance: typeof item.distance === 'number' ? item.distance : 0,
        snippet: String(item.content ?? item.text ?? item.snippet ?? '').slice(0, 80),
        timestamp: item.timestamp ?? item.ts ?? '',
        metadata: item.metadata ?? {},
      }));

      set((s) => {
        const cache = new Map(s.recallCache);
        cache.set(coord, { results, cachedAt: Date.now() });
        const inflight = new Set(s.recallInflight);
        inflight.delete(coord);
        return { recallCache: cache, recallInflight: inflight, enabled: true };
      });
      return results;
    } catch {
      set((s) => {
        const recallInflight = new Set(s.recallInflight);
        recallInflight.delete(coord);
        return { recallInflight };
      });
      return [];
    }
  },
}));
