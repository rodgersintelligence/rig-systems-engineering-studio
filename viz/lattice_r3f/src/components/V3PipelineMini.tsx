// Move 10 — V3 pipeline mini strip.
// 5-stage horizontal indicator: Capture → Process → Create → Engage → Convert → Autonomize.
// Each stage dot pulses when a matching event kind fires in the SSE stream.
import { useEffect, useRef, useState } from 'react';
import { useEvents } from '../store/events';
import type { LiveEvent } from '../store/events';

// Stage → event kinds that trigger a pulse on that stage.
const STAGE_EVENTS: Record<string, string[]> = {
  Capture:    ['sensor.observed'],
  Process:    [],   // reserved for future event kinds
  Create:     ['policy.fired', 'cell.compiled'],
  Engage:     ['cell.scheduled', 'cell.started'],
  Convert:    ['cell.completed', 'publisher.completed'],
  Autonomize: ['prediction.resolved', 'rubric.tuned'],
};

const STAGES = Object.keys(STAGE_EVENTS) as (keyof typeof STAGE_EVENTS)[];

const PULSE_DECAY_MS = 3000;

interface StageState {
  pulsedAt: number | null;
}

export function V3PipelineMini() {
  const [stages, setStages] = useState<Record<string, StageState>>(
    () => Object.fromEntries(STAGES.map((s) => [s, { pulsedAt: null }])),
  );

  // Subscribe to recentEvents, trigger pulse on matching kinds.
  const recentEvents = useEvents((s) => s.recentEvents);
  const prevCountRef = useRef(0);

  useEffect(() => {
    const newEvents = recentEvents.slice(0, recentEvents.length - prevCountRef.current);
    prevCountRef.current = recentEvents.length;

    if (newEvents.length === 0) return;

    setStages((prev) => {
      const next = { ...prev };
      let changed = false;
      for (const evt of newEvents) {
        for (const stage of STAGES) {
          if (STAGE_EVENTS[stage].includes(evt.kind)) {
            next[stage] = { pulsedAt: Date.now() };
            changed = true;
          }
        }
      }
      return changed ? next : prev;
    });
  // Only re-run when recentEvents length changes or total changes.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [recentEvents]);

  // Tick to clear expired pulses.
  useEffect(() => {
    const id = setInterval(() => {
      setStages((prev) => {
        const now = Date.now();
        let changed = false;
        const next = { ...prev };
        for (const stage of STAGES) {
          const p = prev[stage].pulsedAt;
          if (p && now - p > PULSE_DECAY_MS) {
            next[stage] = { pulsedAt: null };
            changed = true;
          }
        }
        return changed ? next : prev;
      });
    }, 250);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={strip}>
      <div style={label}>V3 PIPELINE</div>
      <div style={stageRow}>
        {STAGES.map((stage, i) => {
          const { pulsedAt } = stages[stage];
          const isActive = pulsedAt !== null && Date.now() - pulsedAt < PULSE_DECAY_MS;
          const age = pulsedAt ? Date.now() - pulsedAt : PULSE_DECAY_MS;
          const intensity = isActive ? Math.max(0, 1 - age / PULSE_DECAY_MS) : 0;

          return (
            <div key={stage} style={{ display: 'flex', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
                <div
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: 5,
                    background: isActive
                      ? `rgba(16, 185, 129, ${0.4 + intensity * 0.6})`
                      : '#1e293b',
                    border: `1px solid ${isActive ? '#10b981' : '#334155'}`,
                    boxShadow: isActive ? `0 0 ${6 + intensity * 8}px rgba(16,185,129,${intensity * 0.8})` : 'none',
                    transition: 'background 0.15s, box-shadow 0.15s',
                  }}
                />
                <div style={{ fontSize: 8, color: isActive ? '#10b981' : '#475569', whiteSpace: 'nowrap', letterSpacing: 0.2 }}>
                  {stage}
                </div>
              </div>
              {i < STAGES.length - 1 && (
                <div style={{ width: 14, height: 1, background: '#1e293b', margin: '0 2px', marginBottom: 14 }} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

const strip: React.CSSProperties = {
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  padding: '8px 12px',
};

const label: React.CSSProperties = {
  fontSize: 9,
  color: '#334155',
  letterSpacing: 0.8,
  textTransform: 'uppercase',
  marginBottom: 6,
};

const stageRow: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
};
