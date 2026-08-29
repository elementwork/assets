# Feature List: Asset Inventory Generator

> **Product strategy / North Star:** See `product_strategy.md` before adding or re-packaging major features. It is the strategic source of truth for positioning, edition roles, working pricing principles, continuity lifecycle and product guardrails.
> **Status:** Living document · Last updated 2026-08-19 12:59:00
> **Legend:** ✅ Shipped (verified by `tests/e2e_visual_test.py`)
> **Roadmap:** Planned / in-progress features → see `future_plan.md`

A self-contained, offline-first asset inventory tool for Canadian families in Ontario —
generates Markdown, multi-sheet Excel, and a single-file HTML dashboard in English and
Chinese. No server, no external libraries, no data leaves the user's device.

---

## 1. Core generator (Python)

| # | Feature | Status |
|---|---------|--------|
| 1.1 | 517 asset types across 32 categories with icons/colors | ✅ |
| 1.2 | 116-field schema per asset (ownership, registration/tax, beneficiaries, insurance, digital, crypto, notes…) | ✅ |
| 1.3 | Markdown output — human-readable reference (en/zh) | ✅ |
| 1.4 | Excel output — 8 sheets: All Assets, By Category, Summary, Access, Financial Summary, Insurance, Beneficiaries, Estate (en/zh) | ✅ |
| 1.5 | Self-contained HTML dashboard (en/zh) | ✅ |
| 1.6 | CLI filters: `--owner`, `--category`, `--status`, `--lang en\|zh`, `-o md\|excel\|html\|all` | ✅ |
| 1.7 | Demo fixture (`--demo`) — realistic Ontario family (James & Mei Chen, house, TFSAs/RRSPs/RESP, dormant crypto) | ✅ |

## 2. Dashboard rendering

| # | Feature | Status |
|---|---------|--------|
| 2.1 | 5 visual templates: EstateON, Lumina, Cardinal, Atlantic, Monarch | ✅ |
| 2.2 | Light / dark mode toggle (persisted) | ✅ |
| 2.3 | 9 layouts: Dashboard, Table, Kanban, Timeline, Detail, Compact, Audit, Annual Review, Charts | ✅ |
| 2.4 | Stats cards: total assets, FMV, income, categories, status counts | ✅ |
| 2.5 | Search across name/institution/owner/category/id (debounced) | ✅ |
| 2.6 | Category / owner filters + status toggles (all apply to every layout) | ✅ |
| 2.7 | Table: sortable columns (type-aware), pagination (50/page) | ✅ |
| 2.8 | Timeline: date-ordered view with empty state | ✅ |
| 2.9 | Detail: master-detail with all 116 fields | ✅ |
| 2.10 | Print estate binder (`@media print`): Emergency Access Guide (page 1), Master Asset Index, cover, per-category sections, beneficiary/insurance summaries | ✅ |

## 2a. Tier-aware product navigation

| # | Feature | Status |
|---|---------|--------|
| 2a.1 | Tier-aware product navigation — Free / Family / Professional display names while internal key remains `planning` | ✅ |
| 2a.2 | Primary header reduced to clickable logo-menu + Add + Save + Last Updated; all other actions live in the logo menu and all search/filter controls live in one filter bar | ✅ |
| 2a.3 | Free continuously previews locked Family + Professional capabilities; Family previews Professional; Professional has no upsell UI | ✅ |
| 2a.4 | Summary separates Asset Types, Categories and recorded Assets; Assets card includes Add Asset and With Value context; All / With Value remain quick filters | ✅ |
| 2a.5 | Active / Dormant / Pending / Closed controls are directly visible and right-aligned in the unified filter bar; standalone workspace/layout-switcher chrome is removed | ✅ |
| 2a.6 | Effective-tier UI follows verified license state; invalid paid licenses downgrade branding, workspace, templates and persisted layouts to Free | ✅ |
| 2a.7 | Clicking the top-left EstateON logo icon opens the Features menu; layout choices retain the original SVG icon set, with explicit close/focus-return behavior and bilingual Professional terminology | ✅ |

## 3. Data entry & editing

| # | Feature | Status |
|---|---------|--------|
| 3.1 | Schema-driven edit modal — currency/percent → number, date → date-picker, select → dropdown, url, password with eye-toggle, textarea | ✅ |
| 3.2 | Form validation: required id/name, numeric currency/percent, valid dates, in-option selects — inline errors, save blocked | ✅ |
| 3.3 | Duplicate asset — new id, credentials cleared | ✅ |
| 3.4 | Delete asset (confirm dialog) | ✅ |
| 3.5 | Undo / redo — 50-entry snapshot stack, Ctrl+Z / Ctrl+Shift+Z, toast actions | ✅ |
| 3.6 | Unsaved-changes indicator (●) + **auto-save** to browser storage (debounced 1.5s, toggleable, throttled toast) | ✅ |
| 3.7 | Quick-add wizard — type → institution → owner → value, auto-fill defaults | ✅ |
| 3.8 | Bulk edit — set shared field across selected rows | ✅ |
| 3.9 | Inline table editing (dbl-click cell) | ✅ |
| 3.10 | Kanban drag-and-drop between status columns | ✅ |
| 3.11 | Column configuration for table view | ✅ |
| 3.12 | Markdown rendering for notes/alert/todo fields | ✅ |

## 4. Security & privacy

| # | Feature | Status |
|---|---------|--------|
| 4.1 | Data-block encryption (File Lock, default off) — AES-256-GCM via Web Crypto, PBKDF2 100k, family-word key; only the `assets` payload is encrypted | ✅ |
| 4.2 | Lock UX: birth date (YYYYMMDD) + family word, confirm, enable → data staged encrypted; in-page unlock gate on reopen | ✅ |
| 4.3 | Locked file: reopen shows unlock gate; text editor sees ciphertext in the data block; wrong-passphrase rejected | ✅ |
| 4.4 | XSS-safe rendering — event delegation, HTML-escaped ids | ✅ |
| 4.5 | CSV formula-injection guard (`= + - @` prefix) + RFC-4180 escaping | ✅ |

## 4b. Versioning & save model

| # | Feature | Status |
|---|---------|--------|
| 4.6 | `INVENTORY_DATA` versioned data block — format/version/schema_version/tier/key_version/generated/assets; file = single source of truth | ✅ |
| 4.7 | Tiered build (`--tier free\|family\|planning`) — lower tiers physically strip higher-tier code (export/print/charts/audit/table/timeline) | ✅ |
| 4.8 | Signed license (`--license-secret`) + watermark (`--buyer`) for paid tiers; invalid license downgrades to free capability | ✅ |
| 4.9 | Direct Save: Chromium File System Access API writes back to a bound file; authorized handle persists in IndexedDB across reopen; Inventory ID prevents cross-inventory overwrite; staged Ctrl+S/download remains the fallback | ✅ |
| 4.10 | Auto-save (1.5s debounce) to localStorage (session cache) + `beforeunload` flush; localStorage skipped when file is locked | ✅ |

## 5. Export, import & persistence

| # | Feature | Status |
|---|---------|--------|
| 5.1 | Export Markdown / CSV / JSON / self-contained HTML (downloads) | ✅ |
| 5.2 | Save-HTML carries edits — downloaded file contains current data (file = database) | ✅ |
| 5.3 | JSON import with validation, undoable | ✅ |
| 5.4 | localStorage persistence across sessions | ✅ |

## 6. Charts & analytics

| # | Feature | Status |
|---|---------|--------|
| 6.1 | Pure-SVG charts (no library, offline): FMV by category donut, by registration bar, top-10 institutions, liquidity ladder | ✅ |
| 6.2 | Charts respond to search/filters and live edits | ✅ |

## 7. Audit, planning & estate intelligence

| # | Feature | Status |
|---|---------|--------|
| 7.1 | Audit view — traffic-light validation incl. beneficiary/value/data quality plus Access Readiness and blocked incapacity/death paths | ✅ |
| 7.2 | Access Readiness score (0–100) from locator, recovery contact, handoff instructions, incapacity/death readiness and annual access test | ✅ |
| 7.3 | Annual Family Review layout — overall score, due/overdue reviews, critical handoff assets and access gaps | ✅ |
| 7.4 | Emergency & Handoff schema — priority, recovery location/contact, incapacity/death paths, instructions, last test/next review | ✅ |

## 8. Platform & engineering

| # | Feature | Status |
|---|---------|--------|
| 8.1 | End-to-end visual test — 258 checks: planning-tier generation/static/demo/browser E2E (en/zh) incl. file-lock data-block encryption/unlock, Ctrl+S save guide, exports, quick-add, bulk, inline, kanban, columns, markdown, auto-save; plus tier-gating checks (free/family/planning counts, stripped-code assertions, layout/template/export visibility, license valid/invalid, watermark), screenshots | ✅ |
| 8.2 | Full en/zh localization (UI + categories + fields) | ✅ |
