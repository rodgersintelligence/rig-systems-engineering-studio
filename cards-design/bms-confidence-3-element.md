# BMS Confidence — 3-Element Card (Z-Axis Source of Truth)

**Status**: 🟢 v1 authored (2026-05-16).
**Drives**: `lattice/confidence_elements.py` — every BuildCard's `confidence_step_semantic` field.
**Z-axis source of truth.**

The Build Mode Score (BMS) is composed of one base + two adjustments:

```
BMS = clamp(RAW + ADJ_failure + ADJ_volume + ADJ_altitude, 0, 1)
```

`ADJ_altitude` is implicit in the X-axis (it shifts with altitude position), so the Z-axis exposes the **three independent confidence contributors**:

1. **RAW** = `Σ(C_i / 5) / 20` — the unadjusted average of all 20 scoring criteria.
2. **ADJ_failure** = `+0.15 if C1 ≥ 4 else +0.05 if C1 == 3 else 0` — failure-cost lift.
3. **ADJ_volume** = `0.10 × (C11 / 5)` — throughput lift.

Each is evaluated **per IQRSQPI step**, giving 3 × 7 = 21 Z-axis positions. Each entry below has:

- **What**: signal this contributor measures at this step
- **Why**: why this contributor matters at this step
- **Raises**: levers that lift it
- **Lowers**: signals/anti-patterns that drag it down
- **Failure mode**: what happens when this is the *limiting* contributor

---

## RAW × IQRSQPI (7 entries)

RAW measures *base scoreability* — can the 20-criterion rubric even apply cleanly at this step?

### RAW @ I1 — Intent
- **What**: Can we score the intent against the rubric at all? Are matcher patterns and prior similar intents available?
- **Why**: If intent is fuzzy, scoring breaks downstream — no determinism is possible.
- **Raises**: Crisp intent boundaries, deterministic matcher coverage, prior similar intents in Phronema.
- **Lowers**: Multimodal ambiguity, no matching pattern, novel domain.
- **Failure mode**: Score is impossible to compute → cell forces escalation to A3.1.

### RAW @ Q1 — Question
- **What**: Can we type the question? Does it fit a Phronema query template?
- **Why**: Untypeable questions become open-ended agent loops — cost spikes by 100×.
- **Raises**: Known question shape, parametric variation, prior query templates exist.
- **Lowers**: Novel question structure, multi-hop reasoning required.
- **Failure mode**: Falls back to LLM-driven decomposition → mode demotion to AGENT_BOUNDED.

### RAW @ R — Research
- **What**: Source determinism. Are sources structured APIs/DBs or open-web search?
- **Why**: Structured sources are scoreable; open web isn't (no per-call determinism).
- **Raises**: Internal DB hits, CRM lookups, deterministic MCP calls.
- **Lowers**: Web search required, contrarian sourcing, dead frameworks.
- **Failure mode**: Research step exceeds latency budget; retries deplete cost cap.

### RAW @ S — Solution
- **What**: Can the solution render from a template, or does it require generation?
- **Why**: Templated solutions are deterministic; generated ones aren't.
- **Raises**: Stable solution schema, Jinja template available, no creative variation needed.
- **Lowers**: Novel artifact required, schema evolution mid-flight, persona-bound output.
- **Failure mode**: Template fails to render → falls to LLM synthesis at full cost.

### RAW @ Q2 — Quality
- **What**: Can the gate stack score this deterministically?
- **Why**: Heuristic gates pass/fail; rubric judges add variance and cost.
- **Raises**: Hard physics gates apply, schema validation strict, claim corpus reachable.
- **Lowers**: Anti-slop subjective, novel quality dimensions, qualitative judgment needed.
- **Failure mode**: Quality scoring requires LLM judge — bumps cost band by 10–100×.

### RAW @ P — Proof
- **What**: Can we hash-and-sign the artifact without further reasoning?
- **Why**: Proof should be free — pure audit, no generation.
- **Raises**: Sources are URIs, gates-fired list is finite, content-addressable.
- **Lowers**: Charter requires generation (D2), mechanism map demanded (A3+).
- **Failure mode**: Charter requires LLM authoring → cost band bumps.

### RAW @ I2 — Integrate
- **What**: Does the dispatcher have a deterministic path to execute?
- **Why**: Unknown actions need approval routing; known kinds are auto-routed.
- **Raises**: action.kind in `{smtp, slack, stripe, noop, audit_only}`, dispatcher pre-registered, idempotent.
- **Lowers**: Novel action class, side effects unknown, blast radius unclear.
- **Failure mode**: Falls to AionUI approval (delay) or human dispatch.

---

## ADJ_FAILURE × IQRSQPI (7 entries)

`ADJ_failure` lifts BMS upward when C1 (Failure Cost) is high — we demand MORE determinism when failure is expensive. Each step has its own definition of "failure" and its own cost shape.

### ADJ_FAILURE @ I1 — Intent
- **What**: How much extra determinism is demanded if MIS-INTENT is high-cost?
- **Why**: Mis-intent at L1 = bad email; at L7 = wrong company direction.
- **Raises**: Customer-facing action downstream, regulatory exposure, irreversible financial commitment.
- **Lowers**: Internal-only output, reversible, audit-only.
- **Failure mode**: Cell mis-classified to PYTHON_ONLY but should be HYBRID for safety.

### ADJ_FAILURE @ Q1 — Question
- **What**: How costly is asking the WRONG question?
- **Why**: Wrong question → correct answer to wrong thing → action wastes capital.
- **Raises**: One-shot decision contexts, time pressure, irreversibility.
- **Lowers**: Iterative refinement allowed, low-cost retry, exploration phase.
- **Failure mode**: Premature convergence on canned question; deviation engines never fire.

### ADJ_FAILURE @ R — Research
- **What**: How bad is researching from WRONG sources?
- **Why**: Bad sources poison everything downstream — every claim becomes suspect.
- **Raises**: Compliance-sensitive domain, claim attribution required, legal exposure.
- **Lowers**: Internal research, low-stakes domain, summary-only output.
- **Failure mode**: Allowlist too permissive at D2 → unsourced claims slip into Solution.

### ADJ_FAILURE @ S — Solution
- **What**: How costly is shipping the WRONG solution?
- **Why**: Wrong artifact = blast radius. Recall is expensive.
- **Raises**: External-facing, signed contracts, broadcast comms, automated dispatch.
- **Lowers**: Internal preview, single-user, reversible action.
- **Failure mode**: A1 ships at scale before A1.7 conditional approval catches the error.

### ADJ_FAILURE @ Q2 — Quality
- **What**: How bad is a FALSE PASS in quality?
- **Why**: False pass = bad artifact ships *with proof of "quality"* — worst combination.
- **Raises**: Public-facing artifact, customer-facing, audit/regulatory.
- **Lowers**: Internal-only, sandboxed test, reviewer-in-loop.
- **Failure mode**: Anti-slop accepts slop; claim validator misses unsourced numerics.

### ADJ_FAILURE @ P — Proof
- **What**: How bad is signing a WRONG receipt?
- **Why**: Falsified proof breaks the audit chain — the entire lattice loses credibility.
- **Raises**: Audit-critical, regulator-visible, financial reconciliation.
- **Lowers**: Internal record, low-stakes attestation.
- **Failure mode**: Hash collision, signer impersonation, audit row truncated.

### ADJ_FAILURE @ I2 — Integrate
- **What**: How catastrophic is dispatching the WRONG action?
- **Why**: This is the irreversibility step. Wrong dispatch is the worst single outcome.
- **Raises**: External email send, payment, broadcast, infrastructure change.
- **Lowers**: Internal log, idempotent action, sandbox.
- **Failure mode**: Action executed before approval timeout returns.

---

## ADJ_VOLUME × IQRSQPI (7 entries)

`ADJ_volume` lifts BMS upward when C11 (Volume per Day) is high — high-throughput cells demand cheaper, more deterministic execution. Each step has different cost-per-invocation shape.

### ADJ_VOLUME @ I1 — Intent
- **What**: Throughput pressure on intent resolution.
- **Why**: 1000s/day mandates ~ms-class intent matching, not an LLM round-trip.
- **Raises**: Production hot path, real-time response, batch backlog.
- **Lowers**: Daily cron, weekly reports, ad-hoc.
- **Failure mode**: Intent resolution becomes the latency bottleneck for the entire studio.

### ADJ_VOLUME @ Q1 — Question
- **What**: Throughput pressure on question building.
- **Why**: Repeat queries should be CACHED, not re-decomposed each time.
- **Raises**: Same query shape across many requests, high parametric repetition.
- **Lowers**: Novel question each time, no parametric structure.
- **Failure mode**: Question building burns CPU on identical workloads.

### ADJ_VOLUME @ R — Research
- **What**: Throughput pressure on research fan-out.
- **Why**: Source APIs have rate limits and per-call costs.
- **Raises**: Source caching available, batch-eligible, idempotent fetches.
- **Lowers**: Per-request external API hit, billed-per-call sources.
- **Failure mode**: Rate limit blows up; cost overruns; cell mode demoted.

### ADJ_VOLUME @ S — Solution
- **What**: Throughput pressure on solution composition.
- **Why**: Jinja rendering is microseconds; LLM is seconds — 10⁶× difference per invocation.
- **Raises**: Same template across many invocations, output stable.
- **Lowers**: Personalization required per invocation, novel artifact each time.
- **Failure mode**: Solution step becomes the dominant cost driver at scale.

### ADJ_VOLUME @ Q2 — Quality
- **What**: Throughput pressure on quality scoring.
- **Why**: Heuristic anti-slop is free; LLM judge costs per invocation.
- **Raises**: Hard gates dominant, schema-only validation, no LLM judge needed.
- **Lowers**: Subjective quality dimensions, novel artifact types requiring rubric judges.
- **Failure mode**: Quality eats the cost margin at high volume.

### ADJ_VOLUME @ P — Proof
- **What**: Throughput pressure on audit writes.
- **Why**: Postgres handles 10⁵ writes/sec but content-addressing requires hashing.
- **Raises**: Append-only writes, batched commits, idempotent hashing.
- **Lowers**: Synchronous attestation required, multi-signer protocols.
- **Failure mode**: Audit log becomes the bottleneck under burst load.

### ADJ_VOLUME @ I2 — Integrate
- **What**: Throughput pressure on dispatch.
- **Why**: External APIs throttle; batched dispatch is the answer.
- **Raises**: Batch-eligible (e.g., SES email send), idempotent dispatch, queueable.
- **Lowers**: Real-time required, sync-only APIs, manual approval per item.
- **Failure mode**: Dispatch queue grows unbounded; downstream backpressure.

---

## The shape, in one sentence

**RAW asks "can we score it?", ADJ_failure asks "what does it cost to be wrong here?", and ADJ_volume asks "what does it cost to do this at scale?" — all evaluated through the 7-step IQRSQPI lens to produce the 21-position Z-axis that completes the lattice.**

## After authoring

1. Replace stubs in `lattice/confidence_elements.py` with content from this card.
2. Run `python3 -m lattice.generator` to regenerate all 3,087 cards.
3. View the 3D viz — Z-axis tooltips now carry real content.
