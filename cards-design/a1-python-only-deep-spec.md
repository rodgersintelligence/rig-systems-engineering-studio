# A1 PYTHON_ONLY Archetype — Deep Spec (7 Files, L1–L2)

**Status**: ✅ COMPLETE (imported from canonical source).
**Cells unlocked**: ~30 (all of L1, most of L2). First A-card to ship.
**Cost band**: $0–$0.001 / invocation. **Run frequency**: 1000s/day.

This card is fully authored. See the canonical source: `A1 PYTHON_ONLY Archetype — Complete Code Implementation (7 Files, L1–L2)`.

The 7 archetype files live in the private companion repo:
`github.com/rodgersintelligence/rig-systems-engineering-private/archetypes/a1_python_only/`

## Doctrine for A1

1. **No model in the decision path.** The only LLM touch is the ≤60-word personalization shim at A1.4.
2. **Escalate, don't fail.** When deterministic matchers miss, return `UNKNOWN` and let Hermes route up to A3.1.
3. **Source-per-claim is free here** — claims come from structured sources (CRM, DB, MCP), not generative text.
4. **Approval is conditional**, not mandatory (unlike A3+). Most A1 actions auto-execute; only flagged actions hit AionUI.

## Build Checklist (Weeks 3–4 of overall 13-week plan)

- [ ] `_types.py` finalized and frozen for A1.
- [ ] `intent_maps/<studio>.yaml` populated for each studio targeting L1–L2.
- [ ] Jinja templates seeded under `templates/queries/` and `templates/artifacts/`.
- [ ] Haiku shim wrapper with `max_tokens=120` enforced.
- [ ] Claim validator wired to source corpora.
- [ ] AionUI approval surface live with 24h timeout policy.
- [ ] Postgres append-only audit table migrated.
- [ ] Hermes escalation path A1.1 → A3.1 tested.
- [ ] Promptfoo evals green for A1.4 and A1.5.
