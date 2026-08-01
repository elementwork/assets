---
description: Run pre-push validation sequence: type check, lint, status, diff summary, then prompt for commit and push.
last_updated: 2026-07-31 23:08:58
---

# Pre-Push Validation

Run the standard pre-push validation sequence for this project.

## Steps

1. **Type check**: `python3 -m py_compile src/*.py tests/*.py 2>&1` — must pass with zero errors
2. **Lint**: `python3 -m pyflakes src/*.py 2>&1` — must pass (or skip if pyflakes not installed; pre-existing warnings are acceptable)
3. **E2E visual test**: `python3 tests/e2e_visual_test.py 2>&1` — must finish with `0 failed` (regenerates outputs, validates Markdown/Excel/HTML, and drives both dashboards in headless Chromium)
4. **Status**: `git status` — identify uncommitted changes
5. **Diff summary**: `git diff --stat` — review scope of changes
6. **Commit** (only if user approves): `git add -A && git commit -m "<message>"`
7. **Squash** (if multiple local commits): `git rebase -i HEAD~N` to squash into one
8. **Push** (only if user explicitly says "push"): `git push origin <branch>`

## Rules

- NEVER commit without user's explicit permission — always ask first
- NEVER push without user explicitly saying "push"
- Always run check AND lint AND the E2E visual test before pushing — all must pass
- Squash all local commits into one before pushing
- Use project-configured git identity for commits

## Arguments

$ARGUMENTS — optional: branch name to push to (default: current branch)
