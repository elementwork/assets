---
description: Run pre-push validation sequence: update docs, type check, lint, E2E, status, diff summary, then prompt for commit and push.
last_updated: 2026-08-10 01:10:36
---

# Pre-Push Validation

Run the standard pre-push validation sequence for this project.

## Steps

1. **Docs update**: update ALL relevant documents to reflect the code change and refresh their timestamps to `YYYY-MM-DD HH:MM:SS` — including (as applicable) `README.md`, `docs/dev/feature_list.md` (shipped features / check counts), `docs/dev/future_plan.md` (roadmap statuses ✅/⬜), `docs/dev/promotion_plan.md`, `docs/dev/ASSET_FIELDS.md`, `docs/user/ADMIN_GUIDE.md`, and the in-dashboard help strings in `src/translations.py` + `templates/dashboard.html`. Regenerate outputs so the embedded online docs reflect the change.
2. **Type check**: `python3 -m py_compile src/*.py tests/*.py 2>&1` — must pass with zero errors
3. **Lint**: `python3 -m pyflakes src/*.py 2>&1` — must pass (or skip if pyflakes not installed; pre-existing warnings are acceptable)
4. **E2E visual test**: `python3 tests/e2e_visual_test.py 2>&1` — must finish with `0 failed` (regenerates outputs, validates Markdown/Excel/HTML, and drives both dashboards in headless Chromium)
5. **Status**: `git status` — identify uncommitted changes
6. **Diff summary**: `git diff --stat` — review scope of changes
7. **Commit** (only if user approves): `git add -A && git commit -m "<message>"`
8. **Squash** (if multiple local commits): `git rebase -i HEAD~N` to squash into one
9. **Push** (only if user explicitly says "push"): `git push origin <branch>`

## Rules

- NEVER commit without user's explicit permission — always ask first
- NEVER push without user explicitly saying "push"
- ALWAYS update relevant docs + timestamps before committing — no doc change, no commit
- Always run check AND lint AND the E2E visual test before pushing — all must pass
- Squash all local commits into one before pushing
- Use project-configured git identity for commits

## Arguments

$ARGUMENTS — optional: branch name to push to (default: current branch)
