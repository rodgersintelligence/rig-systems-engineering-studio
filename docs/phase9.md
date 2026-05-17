# Phase 9 — Watcher, Brief, Inbox, Composio Bridges, Phronema

Shipped 2026-05-17. Five edges that complete the closed-loop runtime in the
private repo and surface observable signals into the public viewer.

---

## What shipped

### 1. Watcher launchd (always-on cell executor)

A macOS launchd daemon that keeps the rig.runtime server running at all times.
Three binaries (`rig-cell-watcher`, `rig-runtime-server`, `rig-launchd-install`)
and one `.plist` give the private runtime the same always-on posture as a system
service. On reboot the server restarts within a few seconds; SSE subscribers
reconnect transparently.

Public surface: the SSE stream at `${RIG_EVENT_URL}/events/stream` is now
continuously available (not just when someone launches manually). The viewer's
live dot stays green by default on the rig LAN.

### 2. Weekly brief (markdown digest)

A scheduler-triggered script (`scripts/weekly_brief.py`) that runs every Sunday
and emits a single markdown document summarising the prior 7 days:

- Outcome tallies by archetype and diamond
- Top events from the audit store
- Phronema rubric drift summary
- Any pending inbox items

The brief is written to `~/.rig/briefs/` in the private runtime. It is
generated from the same stores exposed by the SSE stream — audit rows,
prediction outcomes, rubric tuning events — so the viewer and the brief are
always in sync.

### 3. AionUI inbox (`/inbox`)

Three new private-runtime endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/inbox/pending` | GET | JSON list of unresolved approval requests |
| `/inbox/{id}/resolve` | POST | Resolve a request with approved/blocked + note |
| `/inbox` | GET | HTML page — mobile-friendly operator console |

The inbox replaces the previous auto-approve-only flow with a human-operator
path. High-altitude A4 cells that cross a configurable confidence threshold are
held for explicit sign-off. Auto-approve remains the fallback when no operator
is reachable.

The public viewer links to `/inbox` when the SSE socket is connected (see App.tsx
changes below). Clicking a `prediction.resolved` event in the EventTicker also
opens the inbox in a new tab.

### 4. Composio bridges (publisher promotion)

`rig/runtime/composio_bridge.py` in the private repo auto-promotes the six
`publisher.*` stub classes to live Composio-backed integrations when a
`COMPOSIO_API_KEY` env var is present. The bridge is fully backwards-compatible:
if the key is absent the stubs continue to function with log-only output.

The six publishers that gain live connectors: `linear`, `notion`, `slack`,
`github`, `google_calendar`, `airtable`.

Public surface: `publisher.completed` events in the EventTicker now carry a
`composio_action_id` field in their payload when the bridge is active.

### 5. Phronema unification (central DB layer)

`rig/runtime/phronema.py` consolidates the seven previously independent SQLite
stores into a single runtime-managed registry:

| Store | Previous path | Now |
|---|---|---|
| audit | `~/.rig/audit.sqlite` | `Phronema.audit` |
| approval | `~/.rig/approval.sqlite` | `Phronema.approval` |
| miroshark | `~/.rig/miroshark.sqlite` | `Phronema.miroshark` |
| milkyway | `~/.rig/milkyway.sqlite` | `Phronema.milkyway` |
| scheduler | `~/.rig/scheduler.sqlite` | `Phronema.scheduler` |
| brief history | `~/.rig/briefs/*.md` | `Phronema.briefs` |
| phronema index | `~/.rig/phronema.sqlite` | (root) |

`scripts/phronema_migrate.py` is a one-time idempotent migrator that moves
existing rows into the unified schema without data loss. Rollback: the old
individual SQLite files are preserved until the migrator is explicitly confirmed
complete.

---

## Public viewer changes (this repo)

Two minimal additions — both feature-flagged on the SSE connection state so they
are invisible when no runtime is reachable:

1. **Inbox link** — a small "inbox →" text link appears in the EventTicker header
   when `connected === true`. Navigates to `${endpoint}/inbox` in a new tab.

2. **prediction.resolved click-through** — clicking a `prediction.resolved` row
   in the EventTicker opens `${endpoint}/inbox` in a new tab, giving quick access
   to the resolution detail.

---

## Architecture relationship

```
Private repo (closed)              Public repo (this)
─────────────────────              ──────────────────
rig.runtime.server  :8765 ──SSE──> EventTicker (R3F viewer)
  /events/stream                   App.tsx connect()
  /inbox/pending                   "inbox →" link (connected only)
  /inbox/{id}/resolve              prediction.resolved click-through
  /inbox (HTML)
weekly_brief.py ──────────────────> (referenced in docs only)
phronema.py (unified DB)
composio_bridge.py
launchd/*.plist
```

The private runtime is the execution surface; the public viewer is a read-only
observable window into it. No private code paths, credentials, or store schemas
are exposed by the viewer.

---

## Rollback

- Watcher: `launchctl unload` the plist, revert to manual server start
- Brief: cron entry removal; no viewer dependency
- Inbox: endpoints are additive; removing them reverts to auto-approve silently
- Composio bridges: unset `COMPOSIO_API_KEY`; stubs resume automatically
- Phronema: individual SQLite files preserved; remove `phronema.sqlite` to revert
- Viewer: the inbox link and click-through are behind `connected === true`;
  reverting `EventTicker.tsx` and `App.tsx` to pre-Phase-9 state restores
  the prior UX with no other side effects
