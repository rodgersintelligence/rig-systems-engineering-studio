// Move 10 — RGI health status tile. Top-right floating widget.
// Polls /rgi/health (30s) and /phronema/proactive/status (30s).
// Click to expand drawer with all 11 checks and link to /rgi/sla.
import { useEffect, useRef, useState } from 'react';

interface HealthCheck {
  name: string;
  ok: boolean;
  detail?: string;
}

interface HealthData {
  overall: 'green' | 'amber' | 'red';
  checks: HealthCheck[];
}

interface PhronemaData {
  sensors: string[];
  signals_today: number;
  signals_total: number;
  compiler_fired_today: boolean;
  compiler_stats?: Record<string, unknown>;
}

interface Props {
  endpoint: string;   // base URL e.g. http://localhost:8780
}

const POLL_MS = 30_000;

export function RGIStatusTile({ endpoint }: Props) {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [phronema, setPhronema] = useState<PhronemaData | null>(null);
  const [offline, setOffline] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  async function fetchAll() {
    try {
      const [hr, pr] = await Promise.all([
        fetch(`${endpoint}/rgi/health`, { signal: AbortSignal.timeout(5000) }),
        fetch(`${endpoint}/phronema/proactive/status`, { signal: AbortSignal.timeout(5000) }),
      ]);

      if (hr.ok) {
        const hData = await hr.json();
        setHealth(normaliseHealth(hData));
        setOffline(false);
      }
      if (pr.ok) {
        const pData = await pr.json();
        setPhronema(normalisePhronema(pData));
      }
    } catch {
      setOffline(true);
    }
  }

  useEffect(() => {
    fetchAll();
    timerRef.current = setInterval(fetchAll, POLL_MS);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endpoint]);

  const overallColor = offline
    ? '#525252'
    : health?.overall === 'green'
    ? '#22c55e'
    : health?.overall === 'amber'
    ? '#f59e0b'
    : health?.overall === 'red'
    ? '#ef4444'
    : '#525252';

  const overallSymbol = offline ? '?' : health?.overall === 'green' ? '✓' : health?.overall === 'amber' ? '!' : '✗';

  const sensorCount = phronema?.sensors?.length ?? 0;
  const signalsTotal = phronema?.signals_today ?? phronema?.signals_total ?? 0;
  const compilerFired = phronema?.compiler_fired_today ?? false;

  return (
    <div style={tileOuter}>
      {/* Collapsed header — always visible */}
      <div style={tileHeader} onClick={() => setExpanded((x) => !x)}>
        <span style={{ ...dot, background: overallColor }}>{overallSymbol}</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 11, color: '#e5e5e5', fontWeight: 600 }}>
            RGI Health {offline ? '— offline' : ''}
          </div>
          {!offline && (
            <div style={{ fontSize: 10, color: '#64748b', marginTop: 1 }}>
              {sensorCount} sensors · {signalsTotal} signals
              {compilerFired ? ' · compiler ✓' : ''}
            </div>
          )}
        </div>
        <span style={{ fontSize: 10, color: '#475569' }}>{expanded ? '▲' : '▼'}</span>
      </div>

      {/* Expanded drawer */}
      {expanded && (
        <div style={drawer}>
          {offline ? (
            <div style={offlineRow}>endpoint not reachable</div>
          ) : (
            <>
              {health && health.checks.length > 0 && (
                <div>
                  <div style={sectionLabel}>health checks</div>
                  {health.checks.map((c, i) => (
                    <div key={i} style={checkRow}>
                      <span style={{ color: c.ok ? '#22c55e' : '#ef4444', fontSize: 10 }}>
                        {c.ok ? '✓' : '✗'}
                      </span>
                      <span style={{ fontSize: 11, color: '#cbd5e1', marginLeft: 6 }}>{c.name}</span>
                      {c.detail && (
                        <span style={{ fontSize: 10, color: '#475569', marginLeft: 6 }}>{c.detail}</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
              {phronema && (
                <div style={{ marginTop: 8 }}>
                  <div style={sectionLabel}>phronema sensors</div>
                  <div style={{ fontSize: 10, color: '#94a3b8', marginTop: 2 }}>
                    {phronema.sensors.length > 0
                      ? phronema.sensors.join(', ')
                      : 'none registered'}
                  </div>
                  <div style={{ fontSize: 10, color: '#64748b', marginTop: 4 }}>
                    signals today: {phronema.signals_today ?? '—'} &nbsp;·&nbsp;
                    total: {phronema.signals_total ?? '—'}
                  </div>
                </div>
              )}
              <a
                href={`${endpoint}/rgi/sla`}
                target="_blank"
                rel="noopener noreferrer"
                style={slaLink}
              >
                open /rgi/sla →
              </a>
            </>
          )}
        </div>
      )}
    </div>
  );
}

// ── normalise helpers ────────────────────────────────────────────────────────

function normaliseHealth(raw: any): HealthData {
  // Accept both {overall, checks:[]} and {status, components:{}}
  let overall: 'green' | 'amber' | 'red' = 'green';
  const raw_overall = (raw.overall ?? raw.status ?? '').toLowerCase();
  if (raw_overall === 'red' || raw_overall === 'unhealthy' || raw_overall === 'error') overall = 'red';
  else if (raw_overall === 'amber' || raw_overall === 'degraded' || raw_overall === 'warn') overall = 'amber';
  else overall = 'green';

  let checks: HealthCheck[] = [];
  if (Array.isArray(raw.checks)) {
    checks = raw.checks.map((c: any) => ({
      name: c.name ?? c.id ?? 'check',
      ok: c.ok != null ? Boolean(c.ok) : c.status === 'ok' || Boolean(c.healthy),
      detail: c.detail ?? c.message,
    }));
  } else if (raw.components && typeof raw.components === 'object') {
    checks = Object.entries(raw.components).map(([k, v]: [string, any]) => ({
      name: k,
      ok: typeof v === 'boolean' ? v : (v?.ok != null ? Boolean(v.ok) : v?.status === 'ok'),
      detail: typeof v === 'object' ? v?.detail : undefined,
    }));
  }

  return { overall, checks };
}

function normalisePhronema(raw: any): PhronemaData {
  return {
    sensors: Array.isArray(raw.sensors) ? raw.sensors : (raw.sensor_list ?? []),
    signals_today: raw.signals_today ?? raw.events_today ?? 0,
    signals_total: raw.signals_total ?? raw.total_signals ?? 0,
    compiler_fired_today: raw.compiler_fired_today ?? raw.compiler_ran ?? false,
    compiler_stats: raw.compiler_stats,
  };
}

// ── styles ────────────────────────────────────────────────────────────────────

const tileOuter: React.CSSProperties = {
  background: 'rgba(15, 23, 42, 0.92)',
  border: '1px solid #1e293b',
  borderRadius: 8,
  backdropFilter: 'blur(8px)',
  overflow: 'hidden',
  cursor: 'pointer',
  userSelect: 'none',
};

const tileHeader: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  padding: '8px 12px',
};

const dot: React.CSSProperties = {
  width: 20,
  height: 20,
  borderRadius: 10,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: 11,
  fontWeight: 700,
  color: '#0a0a0a',
  flexShrink: 0,
};

const drawer: React.CSSProperties = {
  padding: '8px 12px 10px',
  borderTop: '1px solid #1e293b',
};

const sectionLabel: React.CSSProperties = {
  fontSize: 9,
  color: '#475569',
  textTransform: 'uppercase',
  letterSpacing: 0.6,
  marginBottom: 4,
};

const checkRow: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  padding: '2px 0',
};

const offlineRow: React.CSSProperties = {
  fontSize: 11,
  color: '#475569',
  fontStyle: 'italic',
  padding: '4px 0',
};

const slaLink: React.CSSProperties = {
  display: 'inline-block',
  marginTop: 8,
  fontSize: 10,
  color: '#10b981',
  textDecoration: 'none',
};
