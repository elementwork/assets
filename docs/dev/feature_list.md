# EstateON Asset Inventory — Feature List

> **Product strategy / North Star:** See `product_strategy.md` before adding or re-packaging major features. It is the strategic source of truth for positioning, edition roles, working pricing principles, continuity lifecycle and product guardrails.

> **Generated product state:** This file documents implemented product capabilities. `future_plan.md` documents roadmap ideas; `versioning_plan.md` documents build/tier mechanics.

## 1. Core platform

| # | Feature | Status |
|---|---------|--------|
| 1.1 | Self-contained offline HTML dashboard; file acts as application + database | ✅ |
| 1.2 | English / Chinese generation | ✅ |
| 1.3 | Asset taxonomy + category metadata generated from source schema | ✅ |
| 1.4 | Structured asset field schema | ✅ |
| 1.5 | Local browser cache + embedded file data model | ✅ |
| 1.6 | Direct Save using File System Access API where supported; staged save/download fallback elsewhere | ✅ |
| 1.7 | Inventory ID family/file binding and overwrite mismatch protection | ✅ |
| 1.8 | Whole-file lock/encryption workflow | ✅ |

## 2. Dashboard, views & navigation

| # | Feature | Status |
|---|---------|--------|
| 2.1 | Dashboard/category view | ✅ |
| 2.2 | Compact view | ✅ |
| 2.3 | Kanban view | ✅ |
| 2.4 | Detail view | ✅ |
| 2.5 | Table view | ✅ Family+ |
| 2.6 | Timeline view | ✅ Family+ |
| 2.7 | Charts view | ✅ Family+ |
| 2.8 | Audit view | ✅ Professional |
| 2.9 | Annual Review view | ✅ Professional |

## 2a. Tier-aware product navigation

| # | Feature | Status |
|---|---------|--------|
| 2a.1 | Tier-aware product navigation — Free / Family / Professional display names while internal key remains `planning` | ✅ |
| 2a.2 | Primary header reduced to Search + Add + Print (paid) + Save + Features; secondary controls grouped in the Features menu | ✅ |
| 2a.3 | Free continuously previews locked Family + Professional capabilities; Family previews Professional; Professional has no upsell UI | ✅ |
| 2a.4 | Asset Catalog card distinguishes global catalog size, current Showing count, and With Value count; one-click All / With Value scope filters apply across layouts | ✅ |
| 2a.5 | Status controls collapsed into an accessible dropdown; workspace uses measured sticky geometry and becomes non-sticky on narrow mobile screens | ✅ |
| 2a.6 | Effective-tier UI follows verified license state; invalid paid licenses downgrade branding, workspace, templates and persisted layouts to Free | ✅ |
| 2a.7 | Feature menu has explicit close/focus-return behavior and Professional zh labels retain bilingual professional terminology | ✅ |

## 3. Data entry & editing

| # | Feature | Status |
|---|---------|--------|
| 3.1 | Quick-add asset wizard | ✅ |
| 3.2 | Search asset types in quick-add | ✅ |
| 3.3 | Full asset edit modal with schema-driven fields | ✅ |
| 3.4 | Required/type validation | ✅ |
| 3.5 | Duplicate asset | ✅ |
| 3.6 | Delete asset | ✅ |
| 3.7 | Undo / redo | ✅ |
| 3.8 | Bulk selection / bulk edit | ✅ Family+ table |
| 3.9 | Inline table editing | ✅ Family+ |
| 3.10 | Kanban drag-and-drop status updates | ✅ |
| 3.11 | Configurable table columns | ✅ Family+ |
| 3.12 | Markdown rendering for notes/alerts/todos | ✅ |

## 4. Filtering & analysis

| # | Feature | Status |
|---|---------|--------|
| 4.1 | Search across asset name/institution/owner/category/id | ✅ |
| 4.2 | Category filter | ✅ |
| 4.3 | Owner filter | ✅ |
| 4.4 | Status filter | ✅ |
| 4.5 | All / With Value scope filter | ✅ |
| 4.6 | With Value uses current-value fields including FMV / USD FMV / market value / current balance / equity | ✅ |
| 4.7 | Table sorting | ✅ Family+ |
| 4.8 | FMV/income/category/status summary metrics | ✅ |
| 4.9 | Professional audit rules including access-readiness flags | ✅ Professional |
| 4.10 | Access Readiness score | ✅ Family print + Professional intelligence |

## 5. Estate continuity / handoff

| # | Feature | Status |
|---|---------|--------|
| 5.1 | Emergency-priority field | ✅ |
| 5.2 | Access-location field | ✅ |
| 5.3 | Access/recovery contact field | ✅ |
| 5.4 | Incapacity-access state | ✅ |
| 5.5 | Death-access state | ✅ |
| 5.6 | Handoff instructions | ✅ |
| 5.7 | Last access test / next access review | ✅ |
| 5.8 | Emergency Access Guide print page | ✅ Family+ |
| 5.9 | Master Asset Index print page | ✅ Family+ |
| 5.10 | Annual Review summary workspace | ✅ Professional |

## 6. Export / print / portability

| # | Feature | Status |
|---|---------|--------|
| 6.1 | Estate Binder print output | ✅ Family+ |
| 6.2 | Print stylesheet hides application chrome | ✅ |
| 6.3 | Markdown export | ✅ Professional |
| 6.4 | Excel/CSV-compatible export | ✅ Professional |
| 6.5 | JSON export | ✅ Professional |
| 6.6 | JSON import | ✅ |
| 6.7 | Save As / Direct Save / staged fallback | ✅ |

## 7. Security, localization & UX

| # | Feature | Status |
|---|---------|--------|
| 7.1 | Whole-file AES-GCM lock workflow | ✅ |
| 7.2 | PBKDF2 passphrase derivation | ✅ |
| 7.3 | Account/policy reference masking in continuity outputs | ✅ |
| 7.4 | Full EN/ZH UI generation | ✅ |
| 7.5 | Tier-aware bilingual Professional labels | ✅ |
| 7.6 | Responsive/mobile layout treatment | ✅ |
| 7.7 | Explicit Features menu close/focus return | ✅ |
| 7.8 | Status `aria-pressed` semantics | ✅ |
| 7.9 | Effective-tier downgrade after invalid paid license | ✅ |
| 7.10 | Current HMAC license verification architecture | ⚠️ Functional but not commercially tamper-resistant; asymmetric-signature redesign recommended |

## 8. Tests & quality gates

| # | Feature | Status |
|---|---------|--------|
| 8.1 | End-to-end visual test — 233 checks: planning-tier generation/static/demo/browser E2E (en/zh) incl. file-lock data-block encryption/unlock, Ctrl+S save guide, exports, quick-add, bulk, inline, kanban, columns, markdown, auto-save; plus tier-gating checks (free/family/planning counts, stripped-code assertions, layout/template/export visibility, license valid/invalid, watermark), responsive geometry, print media, localization, screenshots | ✅ |
| 8.2 | Full en/zh localization (UI + categories + fields) | ✅ |
| 8.3 | `git diff --check` clean regeneration gate | ✅ |

## 9. Current generated edition footprint

| Edition | Internal key | Approx. catalog size | Categories | Fields |
|---|---|---:|---:|---:|
| Free | `free` | 256 | 15 | 116 |
| Family | `family` | 324 | 20 | 116 |
| Professional | `planning` | 517 | 32 | 116 |

Catalog counts are generated data, not product promises; UI should use actual generated counts rather than hard-coded marketing numbers.

## 10. Known strategic / implementation follow-ups

These are intentionally not represented as shipped features:

- Explicit persisted “confirmed owned / recorded / not owned / needs review” state instead of inferring ownership from pre-populated rows.
- Material-asset filtering for Master Asset Index / Annual Review so catalog rows do not receive equal weight.
- Workflow-level Annual Review metadata (`review_completed_at`, `access_verified`, backup verification, etc.).
- Executor / Incapacity operational modes.
- Asymmetric license signatures before relying on the license boundary commercially.
- More explicit backup / recovery guidance.

See `product_strategy.md` for the product rationale and `future_plan.md` for roadmap treatment.
