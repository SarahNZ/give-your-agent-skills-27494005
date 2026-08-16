---
name: repo-readiness
description: Evaluate whether a repository is prepared for AI-assisted development and guide the user toward the highest-impact improvements. Use this skill whenever the user asks whether a repo is AI-ready, agent-ready, well-instructed, or easy for coding agents to work in, or asks what AGENTS.md, CLAUDE.md, copilot instructions, skills, prompts, or other agent context is missing. Always use the bundled deterministic audit script for scoring; do not invent or recalculate the score.
compatibility: Requires Python 3.9+ and permission to read the repository being audited.
---

# Repository Readiness

Assess a repository's discoverable support for AI-assisted development, then turn the audit into an actionable improvement sequence. The score belongs to the script, not to the agent: run the script first, preserve its reported values, and explain them without changing the arithmetic.

## Workflow

1. Identify the repository root. If the user names a path, use it. Otherwise use the current working directory.
2. Run the bundled audit from this skill directory:

   ```bash
   python scripts/check_readiness.py /path/to/repository
   ```

   The command emits JSON. Use `--pretty` only when a human-readable terminal report is useful. Never replace the script with a manual file search or an agent-estimated score.

3. Read the complete JSON result. Report the exact `score`, `max_score`, `percentage`, and `rating`, followed by the checks and their discovered paths.
4. Explain the score as a measure of repository signals that make agent work easier to start and repeat. It is not a measure of code quality, security, correctness, or team maturity.
5. Recommend improvements in descending order of the script's `priority` and `points`. Use the script's recommendation text as the source of truth, adding practical context from the listed missing signals.
6. Separate observed facts from suggestions. Do not claim that an artifact is useful merely because its filename exists; mention that the script checks presence and that content quality still needs human review.
7. If the user asks to improve the repository, confirm the target artifact and scope, then create the smallest useful artifact using the repository's conventions. Re-run the script after changes and report the new deterministic result.

## Output format

Use this order:

- **Readiness:** `score/max_score` (`percentage`), `rating`
- **What it checks:** one sentence explaining the five dimensions
- **Evidence:** each check, its points, status, and discovered paths
- **Highest-impact improvements:** missing checks first, using the script's priorities
- **Caveat:** presence is deterministic; the script does not judge whether instructions are accurate, complete, or followed

Keep the explanation concise unless the user asks for a deeper audit. When there are no missing signals, say so and suggest reviewing the clarity and freshness of the existing artifacts rather than inventing more files.

## Deterministic scoring contract

The script owns the scoring model. It awards 3 points for agent context, 3 for agent instructions/rules, 2 for repeatable AI workflows, 1 for project documentation, and 1 for development automation, for a maximum of 10. A dimension earns its full points when at least one recognized signal is found and zero otherwise. Ratings are `not-ready` for 0-2, `developing` for 3-5, `ready` for 6-8, and `strong` for 9-10. These labels and weights must not be changed in the prose without changing the script and its tests together.

## Helping create artifacts

Prefer one focused artifact at a time:

- Agent context: capture repository purpose, layout, conventions, validation commands, and important constraints in `AGENTS.md` or the repository's established equivalent.
- Agent rules: add scoped instructions where the chosen agent expects them, such as `.github/copilot-instructions.md` or `.github/instructions/*.instructions.md`.
- Repeatable workflow: add a focused `SKILL.md` or `.prompt.md` only when a workflow is recurring and its inputs and outputs can be described clearly.
- Documentation: improve `README.md` or `CONTRIBUTING.md` with setup and verification steps.
- Automation: document or add the repository's normal test, lint, build, or CI entry point.

Do not create several empty marker files just to raise the score. A short, accurate artifact that an agent can act on is more valuable than nominal coverage.
