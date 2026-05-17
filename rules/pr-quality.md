# PR Quality

Good engineering practices that also happen to score well on quality and contribution metrics. The goal is production safety and clean code — metrics are a signal, not the objective. Never let metric optimization override good engineering judgment.

---

## Tests are mandatory

Every implementation change must include corresponding tests. The only exceptions are pure config changes, documentation, or build file updates. If you're unsure whether tests apply, they do.

When delegating to workers, include "add tests" in the brief. When reviewing, flag missing tests as ⚠️ Warning.

---

## Self-review before surfacing

Before returning work (as a worker) or creating a PR, review every changed file from a reviewer's perspective:

1. **Would someone unfamiliar with this code ask "why?" at any line?**
2. **If yes:** simplify the code, improve naming, or add a brief inline comment
3. **Are there any decisions that aren't obvious from the code?** Document them in the PR description under "Key Decisions"

The goal is zero surprises for the reviewer. Every comment thread that could have been prevented by clearer code or a better description is a failure.

---

## Keep PRs focused, not artificially small

- **One logical concern per PR.** Don't mix unrelated changes.
- **Do NOT split a single concern into multiple PRs just to keep diffs small.** If "add integration tests for untested code path" is the goal, one PR covering all of them is better engineering than 4 tiny PRs.
  - Size thresholds are signals, not limits. A 20-file PR that's all the same mechanical fix is fine. A 3-file PR that mixes a feature, a refactor, and a config change is not.
- **When in doubt, ask:** "Would a reviewer understand this PR as one coherent effort?" If yes, it's the right size.

---

## First publish is the draft that counts

Review Churn % is 50% of the CRIT Index and is measured from first PR publication to merge — only non-merge commits by the author after the first human review. Run tests, lint, and self-review **before** the first push. Post-push fixups directly inflate churn.

**Guardrails to know:** PRs under 10 LOC are excluded from churn entirely. Per-PR churn is capped at 500%. Averaging is LOC-weighted — a sloppy large PR hurts more than a sloppy small one.

**Comment threads are normalized per PR** (threads / merged PR count) — having more PRs doesn't hurt this metric. Only human reviewer `review_comment` threads count: self-comments, bot comments (HAE, svc-o accounts), and approvals are excluded. The goal: write code and descriptions clear enough that reviewers don't need to ask questions.

**Tests Added counts PRs that touch test files** (binary per PR). Including even one test file change counts. This reinforces "tests are mandatory" — it's also measured.

---

## PR descriptions prompt questions

The Summary section should answer the top 3 questions a reviewer would ask. Include:

- **Why** this change exists (not just what it does)
- **Key Decisions:** when non-obvious choices were made and what alternatives were considered
- **What's NOT changing:** when the scope boundary might be unclear
