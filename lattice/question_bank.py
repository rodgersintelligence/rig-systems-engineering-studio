"""30-question / 30-criterion banks per Y-cell (21 cells x 30 = 630 entries).

One bank per (Diamond, IQRSQPI step). The runtime evaluates all 30 at each
Z-axis confidence element so a single invocation answers 30 questions per cell.

Doctrine: D1 questions probe diversity. D2 questions probe mechanism + sourcing.
D3 questions probe drift + reproducibility.
"""
from __future__ import annotations

from .build_card import Diamond, IQRSQPI, Question


def _q(cell_prefix: str, n: int, text: str, pass_cond: str,
       kind: str = "question", severity: str = "warning") -> Question:
    return Question(
        id=f"{cell_prefix}.Q{n:02d}",
        kind=kind,  # type: ignore[arg-type]
        text=text,
        pass_condition=pass_cond,
        severity=severity,  # type: ignore[arg-type]
    )


# Template patterns. The runtime substitutes {cell_prefix} per cell when
# materializing a card's bank. Each pattern produces ~30 entries.

D1_PATTERN: list[tuple[str, str, str, str]] = [
    # (text, pass_condition, kind, severity)
    ("Did we generate >=5 distinct framings?", "len(framings) >= 5", "criterion", "blocker"),
    ("Is the deviation distribution mean >= +3 sigma?", "stats.mean(deviations) >= 3.0", "criterion", "blocker"),
    ("Did we include >=1 contrarian source?", "any(s.tier == 'contrarian' for s in sources)", "criterion", "warning"),
    ("Are abandoned paths explicitly logged with reasons?", "all(p.reason for p in abandoned)", "criterion", "blocker"),
    ("What stakeholder perspectives are missing?", "len(missed_perspectives) == 0", "question", "warning"),
    ("Are any orthodox framings present that should be ruptured?", "rupture_engine_sigma >= +5", "criterion", "warning"),
    ("Does the IntentSpace contain mutually exclusive candidates?", "exclusivity_check passes", "criterion", "info"),
    ("Have we sourced beyond peer-reviewed (e.g., dead frameworks)?", "source_diversity_index >= 0.7", "criterion", "warning"),
    ("Did we run frame_collision against >=3 orthogonal frames?", "frame_collision_count >= 3", "criterion", "blocker"),
    ("Are the unresolved questions explicitly named?", "len(unresolved_questions) >= 3", "criterion", "warning"),
    ("What would the contrarian say next?", "contrarian_response captured", "question", "info"),
    ("Is the volt sigma >= +5 for emotional voltage?", "volt_sigma >= 5", "criterion", "warning"),
    ("Did the breaker engine identify an orthodoxy to demolish?", "breaker_orthodoxy_named is not None", "criterion", "blocker"),
    ("Are any low-signal slop tokens present?", "slop_token_count <= 5", "criterion", "warning"),
    ("Does each candidate have a falsifier hypothesis?", "all(c.falsifier for c in candidates)", "criterion", "warning"),
    ("Did we sample sources from >=3 epistemic tiers?", "len(set(s.tier for s in sources)) >= 3", "criterion", "warning"),
    ("Are the candidate intents grounded in user context?", "context_grounding_score >= 0.6", "criterion", "info"),
    ("What dead end did we deliberately walk into?", "deliberate_dead_end logged", "question", "info"),
    ("Is the coverage report computed against stakeholder_map?", "coverage_vs_stakeholder is not None", "criterion", "blocker"),
    ("Have we tagged each candidate with its dominant DV engine?", "all(c.dv_engine for c in candidates)", "criterion", "info"),
    ("Did the surprise engine score >=+5 sigma anywhere?", "max(surprise_sigmas) >= 5", "criterion", "warning"),
    ("Are we beyond the comfort region (anti-status-quo)?", "comfort_region_distance >= 0.5", "criterion", "warning"),
    ("Did wider research yield contradiction pairs?", "len(conflicting_evidence) >= 2", "criterion", "info"),
    ("Is the rupture engine output non-trivial?", "len(rupture_targets) >= 1", "criterion", "warning"),
    ("Are abandoned paths reachable for future agents?", "abandoned written to phronema://exploration/", "criterion", "blocker"),
    ("Did we record divergence metrics for retrospective?", "divergence_metrics persisted", "criterion", "info"),
    ("What probability would we have assigned to each candidate?", "prior_probabilities captured", "question", "info"),
    ("Did we hit the +30 sigma rung on at least one engine?", "any(s >= 30 for s in engine_sigmas)", "criterion", "warning"),
    ("Are we satisfied with the breadth before narrowing?", "breadth_satisfaction_score >= 0.7", "criterion", "info"),
    ("Have we logged the proof receipt before frame selection?", "exploration_receipt.hash is not None", "criterion", "blocker"),
]

D2_PATTERN: list[tuple[str, str, str, str]] = [
    ("Is the mechanism explicit and graph-bound?", "mechanism_graph is not None", "criterion", "blocker"),
    ("Does the solution have a written falsifier?", "falsifier_text is not None", "criterion", "blocker"),
    ("Are all claims backed by >=1 source?", "len(unsourced_claims) == 0", "criterion", "blocker"),
    ("Does the schema validate without retry?", "schema_validation_attempts <= 1", "criterion", "warning"),
    ("Did the physics gate stack pass cleanly?", "physics_hard_blocks == 0", "criterion", "blocker"),
    ("Is the cognitive sigma >= +5 across the top 6 pulls?", "rig_l >= 5.0", "criterion", "warning"),
    ("Are the sub-questions coverage-checked >= 0.85?", "coverage >= 0.85", "criterion", "blocker"),
    ("Does the falsification charter include dated kill criteria?", "charter.kill_criteria_dated", "criterion", "warning"),
    ("Are MiroFish 6-criterion scores >= 8.5/10?", "mirofish.overall >= 8.5", "criterion", "warning"),
    ("Did MiroShark return calibrated probability with confidence?", "miroshark.confidence > 0", "criterion", "warning"),
    ("Is the audit row prepared before dispatch?", "audit_row.draft_exists", "criterion", "blocker"),
    ("What is the predicted Brier score?", "brier_prediction in (0, 1)", "question", "warning"),
    ("Are the action's side effects bounded and reversible?", "blast_radius_score <= 3", "criterion", "warning"),
    ("Does approval policy match the risk classification?", "policy.matches(risk_class)", "criterion", "blocker"),
    ("Are the sources allowlist-restricted (D2 mode)?", "all(s in D2_ALLOWLIST for s in sources)", "criterion", "blocker"),
    ("Did the anchor engine reach >= +5 sigma?", "anchor_sigma >= 5", "criterion", "warning"),
    ("Does the forge engine show explicit mechanism chains?", "forge_sigma >= 5", "criterion", "warning"),
    ("Are decomposed sub-questions DAG-acyclic?", "is_dag(question_dag)", "criterion", "blocker"),
    ("Does the solution body type-check against Solution schema?", "isinstance(solution, Solution)", "criterion", "blocker"),
    ("Are 6+ strongest engine pulls non-zero?", "len([s for s in pulls if abs(s)>0]) >= 6", "criterion", "warning"),
    ("Did the shield engine pre-empt at least 3 attacks?", "len(shield.attacks_preempted) >= 3", "criterion", "warning"),
    ("Are the predictions Brier-trackable?", "all(p.observable_at for p in predictions)", "criterion", "blocker"),
    ("Did we generate >=5 candidate solutions before judging?", "len(candidates) >= 5", "criterion", "warning"),
    ("Is the proof_packet content-addressed and signed?", "proof_packet.hash and proof_packet.signer", "criterion", "blocker"),
    ("Are research rows attached as ClaimWithSources?", "all(isinstance(r, ClaimWithSources) for r in rows)", "criterion", "blocker"),
    ("What is the expected execution latency?", "latency_estimate_ms is not None", "question", "info"),
    ("Did the bayes engine decompose probabilities into 2-3 factors?", "bayes.factor_count in (2,3)", "criterion", "warning"),
    ("Is the audit path Phronema-compatible?", "audit_path.startswith('phronema://')", "criterion", "blocker"),
    ("Are there explicit unknowns flagged for D3 follow-up?", "len(explicit_unknowns) >= 1", "criterion", "info"),
    ("Does the integration step honor requires_approval?", "respects_approval_flag", "criterion", "blocker"),
]

D3_PATTERN: list[tuple[str, str, str, str]] = [
    ("What drift metric triggered this evolution pass?", "drift_signal.metric is not None", "criterion", "blocker"),
    ("Is the baseline reference reproducible?", "baseline_ref.hash and baseline_ref.timestamp", "criterion", "blocker"),
    ("Did Brier score worsen vs baseline?", "brier_now > brier_baseline", "criterion", "warning"),
    ("Are rollback events forensically documented?", "all(r.cause for r in rollback_events)", "criterion", "blocker"),
    ("Did MiroShark detect calibration drift?", "miroshark.drift_detected is True", "criterion", "warning"),
    ("Is the regression class identified?", "regression_class in KNOWN_REGRESSIONS", "criterion", "warning"),
    ("Does the patch follow minimum-diff principle?", "patch.diff_size <= patch.threshold", "criterion", "warning"),
    ("Did the regression check pass against last 30 days?", "regression_report.pass is True", "criterion", "blocker"),
    ("Are adjacent cells impact-checked?", "len(adjacent_impact) >= 0", "criterion", "warning"),
    ("Is the re-score receipt append-only?", "audit_appendonly.verified", "criterion", "blocker"),
    ("What downstream cells will be cascade-updated?", "len(cascade_cells) >= 0", "question", "warning"),
    ("Did the patch include rationale text?", "patch.rationale is not None", "criterion", "blocker"),
    ("Are prior_scores preserved in the receipt?", "receipt.prior_scores is not None", "criterion", "blocker"),
    ("Did approval-mandatory cascade go through AionUI?", "aionui.decision is not None", "criterion", "blocker"),
    ("Is the viz refresh URL populated?", "viz_refresh_url is not None", "criterion", "info"),
    ("Have we documented why the patch is minimum-diff?", "patch.minimality_argument", "criterion", "warning"),
    ("Did MilkyWay's long-horizon forecast confirm the patch?", "milkyway.endorses_patch", "criterion", "warning"),
    ("Are we within the 90-day rescore cadence?", "(now - last_rescore).days <= 90", "criterion", "info"),
    ("Did the phase_transition engine flag a regime shift?", "physics_33.regime_shift", "criterion", "warning"),
    ("Are downstream alerts wired to the right surfaces?", "all(a.surface in KNOWN_SURFACES for a in alerts)", "criterion", "blocker"),
    ("What is the predicted post-patch Brier score?", "patch.predicted_brier in (0, 1)", "question", "warning"),
    ("Is the forensic pack hash-chained from prior cell state?", "hash_chain_verified", "criterion", "blocker"),
    ("Did we sample the last N invocations for replay?", "replay_sample_size >= 30", "criterion", "blocker"),
    ("Are time_window deltas computed correctly?", "delta_window.start < delta_window.end", "criterion", "warning"),
    ("Does the patch change BuildMode? If so, justify.", "mode_change.justification or not mode_change", "criterion", "warning"),
    ("Are the failure_mode questions answered explicitly?", "all(q.answer for q in failure_mode_questions)", "criterion", "blocker"),
    ("Is the cascade synchronized with the viz layer?", "viz.lattice_index.refreshed_at >= cascade.completed_at", "criterion", "warning"),
    ("Did we run anti_slop on the patch rationale?", "anti_slop.score(patch.rationale) >= 4", "criterion", "warning"),
    ("Are stakeholders notified of the score change?", "len(stakeholders_notified) >= 1", "criterion", "info"),
    ("What is the next scheduled re-score date?", "next_rescore is not None", "criterion", "blocker"),
]

PATTERNS: dict[Diamond, list[tuple[str, str, str, str]]] = {
    Diamond.D1: D1_PATTERN,
    Diamond.D2: D2_PATTERN,
    Diamond.D3: D3_PATTERN,
}


def bank_for_cell(diamond: Diamond, step: IQRSQPI) -> list[Question]:
    """Materialize the 30-question bank for a (diamond, step) Y-cell."""
    cell_prefix = f"{diamond.value}.{step.value}"
    pattern = PATTERNS[diamond]
    return [
        _q(cell_prefix, i + 1, text=text, pass_cond=pc, kind=kind, severity=sev)
        for i, (text, pc, kind, sev) in enumerate(pattern)
    ]


# Sanity asserts
for _d, _p in PATTERNS.items():
    assert len(_p) == 30, f"Diamond {_d.value} has {len(_p)} entries, expected 30"
