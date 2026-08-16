# Repository readiness assessment

## Scope

Repository assessed: `/workspaces/give-your-agent-skills-27494005`.

This evaluation intentionally did **not** use the `repo-readiness` skill. It inspected the checked-out files and ran lightweight read-only Git/search commands. The requested output directory was created; no source files were edited.

## Assessment

**Readiness: low to moderate, with partial signals.**

The repository has enough context for a human to understand its purpose and branch-oriented course workflow, but it does not yet give an AI agent a reliable local contract for making or validating changes.

### Positive signals

- `README.md` explains the course repository, branch naming convention, beginning/end branch states, and the manual branch-switching process.
- `.devcontainer/devcontainer.json` defines a reproducible editor environment and installs useful HTML/CSS/JavaScript tooling.
- `.github/workflows/main.yml` exists and automates copying the main state to branches, although it is only manually triggered.
- `.vscode/settings.json` enables format-on-save/paste and records editor defaults.
- `.github/CODEOWNERS`, issue guidance, and contribution policy provide some repository governance.

### Gaps and risks

- No `AGENTS.md` exists anywhere in the tracked tree.
- The stated `.github/copilot-instructions.md` and `package.json` signals were not present in this checkout. There is no package manifest or lockfile for a JavaScript toolchain.
- There is no documented build, test, lint, formatting, preview, or acceptance command that an agent can run to verify a change.
- The only workflow is `workflow_dispatch`; there is no change-triggered validation workflow.
- The repository explicitly says it does not accept pull requests, so standard PR-based agent workflows are not the primary operating model here.
- The branch model is unusually broad and course-specific. Agents need explicit rules about which branch may be changed, how `main` relates to beginning/end branches, and whether generated/lesson artifacts should be modified together.
- The branch-copy action uses old major versions (`actions/checkout@v2` and `copy-to-branches@v1.2`), which is operational maintenance risk, though updating it is separate from the first readiness improvement.

## What to add first

### 1. Add a root `AGENTS.md`

This is the highest-leverage first addition because it supplies the missing operating contract at the repository boundary. Keep it short and concrete. It should state:

- Repository purpose and the HTML/CSS/JavaScript-only shape.
- The source-of-truth branch and the meaning of `01_01b`/`01_01e`-style branches.
- Which files and directories agents may modify.
- Required checks for webpage changes, such as opening `before-skills/index.html` and `after-skills/index.html`, checking browser-console errors, and verifying desktop/mobile layout.
- The fact that there is no package manager or test suite unless one is intentionally added.
- The manual branch-copy and refresh workflow, including when not to run it.
- A concise instruction to avoid editing generated or unrelated lesson artifacts.

A root `AGENTS.md` should come before a skill because these rules apply to every agent task in this repository and are discoverable without depending on a particular installed skill.

### 2. Encode the two recurring workflows

After the agent contract, make the repeated operations executable and documented:

- **Branch propagation:** retain or improve the manually dispatched `Copy To Branches` workflow, document its source/target behavior, and pin or update its actions deliberately.
- **Environment refresh:** document the `git pull --all` post-attach behavior and provide a safe, explicit command or task for refreshing branch references. It should not silently overwrite local work.

These should be represented as a small documented workflow/task, not merely prose copied into multiple places. Because this repository does not accept pull requests, the automation should fit the existing branch-publishing model rather than assume CI gates on PRs.

### 3. Add a minimal validation contract

A full package setup is not the first requirement. First define a cheap acceptance checklist for the static pages, then optionally add a package manifest and scripts if the project wants repeatable linting or browser checks. Useful initial checks include HTML validity, CSS linting, JavaScript syntax checking for `after-skills/script.js`, and a browser smoke check at desktop and mobile widths.

## Recommended order

1. Root `AGENTS.md` with branch rules, allowed scope, and validation commands.
2. One documented, safe task for branch refresh plus a documented branch-propagation workflow.
3. Minimal static-site validation scripts and a CI workflow triggered by relevant changes.
4. Only then consider adding `package.json` and broader agent skills if the validation/tooling needs justify them.

## Read-only evidence

Observed tracked signals:

```text
.agents/skills/frontend-design/LICENSE.txt
.agents/skills/frontend-design/SKILL.md
.agents/skills/recursive-code-review/SKILL.md
.devcontainer/devcontainer.json
.github/CODEOWNERS
.github/ISSUE_TEMPLATE.md
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/main.yml
.gitignore
.vscode/settings.json
CONTRIBUTING.md
LICENSE
NOTICE
README.md
after-skills/index.html
after-skills/script.js
after-skills/styles.css
before-skills/index.html
before-skills/styles.css
favicon.ico
skills-lock.json
```

No `AGENTS.md`, `package.json`, `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock` was found.

Workflow contents:

```yaml
name: Copy To Branches
on:
  workflow_dispatch:
jobs:
  copy-to-branches:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      - name: Copy To Branches Action
        uses: planetoftheweb/copy-to-branches@v1.2
        env:
          key: main
```

Relevant local workflow evidence:

```json
// .devcontainer/devcontainer.json
// Pull all branches
"postAttachCommand": "git pull --all"
```

Relevant README evidence: branch names follow `CHAPTER#_MOVIE#`, beginning/end states use `b`/`e`, `main` is the final state, and switching branches may require committing or stashing local changes first.

## Worktree note

At assessment time, `git status --short` reported pre-existing changes/untracked content:

```text
 M skills-lock.json
?? .agents/skills/repo-readiness-workspace/
?? .agents/skills/repo-readiness/
?? .agents/skills/skill-creator/
```

These were not modified or reverted. The requested result file is under the newly requested evaluation output directory.
