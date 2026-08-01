# Feature List: Asset Inventory Generator

> **Status:** Living document · Last updated 2026-07-31 23:08:58
> **Legend:** ✅ Shipped (verified by `tests/e2e_visual_test.py`) · 🔜 Planned (see `future_plan.md` for roadmap detail)

A self-contained, offline-first asset inventory tool for Canadian families in Ontario —
generates Markdown, multi-sheet Excel, and a single-file HTML dashboard in English and
Chinese. No server, no external libraries, no data leaves the user's device.

---

## 1. Core generator (Python)

| # | Feature | Status |
|---|---------|--------|
| 1.1 | 517 asset types across 32 categories with icons/colors | ✅ |
| 1.2 | 109-field schema per asset (ownership, registration/tax, beneficiaries, insurance, digital, crypto, notes…) | ✅ |
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
| 2.3 | 8 layouts: Dashboard, Table, Kanban, Timeline, Detail, Compact, Audit, Charts | ✅ |
| 2.4 | Stats cards: total assets, FMV, income, categories, status counts | ✅ |
| 2.5 | Search across name/institution/owner/category/id (debounced) | ✅ |
| 2.6 | Category / owner filters + status toggles (all apply to every layout) | ✅ |
| 2.7 | Table: sortable columns (type-aware), pagination (50/page) | ✅ |
| 2.8 | Timeline: date-ordered view with empty state | ✅ |
| 2.9 | Detail: master-detail with all 109 fields | ✅ |
| 2.10 | Print estate binder (`@media print`): cover, per-category sections, beneficiary/insurance summaries | ✅ |

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
| 4.1 | AES-256-GCM credential vault (Web Crypto) — PBKDF2 100k, per-field salt/IV, ciphertext at rest | ✅ |
| 4.2 | Vault UX: set/confirm passphrase, lock, unlock, wrong-passphrase rejection, "no passphrase = no recovery" warning | ✅ |
| 4.3 | Sensitive-field masking — masked read-only placeholders, password inputs, account-number masking | ✅ |
| 4.4 | XSS-safe rendering — event delegation, HTML-escaped ids | ✅ |
| 4.5 | CSV formula-injection guard (`= + - @` prefix) + RFC-4180 escaping | ✅ |
| 4.6 | Master lock screen — encrypt entire dataset, gate whole dashboard | 🔜 |
| 4.7 | Session timeout auto-lock | 🔜 |
| 4.8 | Secure clipboard (auto-clear after 30 s) | 🔜 |
| 4.9 | Panic/privacy toggle — blur values + mask account numbers | 🔜 |
| 4.10 | Tamper evidence — content hash + timestamp, verified on load | 🔜 |
| 4.11 | Redacted sharing profiles (Advisor / Executor / Family / Accountant / Insurance) | 🔜 |
| 4.12 | Password health audit (strength, reuse) | 🔜 |

## 5. Export, import & persistence

| # | Feature | Status |
|---|---------|--------|
| 5.1 | Export Markdown / CSV / JSON / self-contained HTML (downloads) | ✅ |
| 5.2 | Save-HTML carries edits — downloaded file contains current data (file = database) | ✅ |
| 5.3 | JSON import with validation, undoable | ✅ |
| 5.4 | localStorage persistence across sessions | ✅ |
| 5.5 | CSV import from Canadian institutions with column mapping + merge screen | 🔜 |
| 5.6 | Live FX rates (opt-in) + crypto price fetch (opt-in) | 🔜 |
| 5.7 | iCal export of renewals/maturities/deadlines | 🔜 |
| 5.8 | QR emergency card (locations only, no secrets) | 🔜 |
| 5.9 | Advisor handoff pack (redacted Excel + binder + reports) | 🔜 |

## 6. Charts & analytics

| # | Feature | Status |
|---|---------|--------|
| 6.1 | Pure-SVG charts (no library, offline): FMV by category donut, by registration bar, top-10 institutions, liquidity ladder | ✅ |
| 6.2 | Charts respond to search/filters and live edits | ✅ |
| 6.3 | Net worth trend over time (snapshots + line chart) | 🔜 |
| 6.4 | Risk dashboard — liquidity, concentration, volatility, insurance ratio, estate exposure | 🔜 |
| 6.5 | Income stream visualization (monthly by source) | 🔜 |
| 6.6 | Tax-loss harvesting detector | 🔜 |
| 6.7 | Asset location optimizer (tax-efficient placement) | 🔜 |
| 6.8 | Rebalancing alerts | 🔜 |
| 6.9 | Concentration risk detector | 🔜 |
| 6.10 | Dividend income tracker | 🔜 |
| 6.11 | Mortgage amortization tracker | 🔜 |
| 6.12 | Rental cash-flow analysis (cap rate, cash-on-cash) | 🔜 |

## 7. Audit, planning & estate intelligence

| # | Feature | Status |
|---|---------|--------|
| 7.1 | Audit view — traffic-light validation: missing beneficiary (red), missing FMV/ACB/institution/owner (yellow), bad selects, TFSA over-contribution, stale >12 months | ✅ |
| 7.2 | Audit gaps: beneficiary % ≠ 100, minors as beneficiaries, stale designations, estate-bound assets, will inconsistencies | 🔜 |
| 7.3 | Family profiles + ownership/tenancy model | 🔜 |
| 7.4 | Liabilities & true net worth (mortgages, HELOCs, loans…) | 🔜 |
| 7.5 | Computed-field engine (gain/%, equity, LTV, coverage gap…) | 🔜 |
| 7.6 | "What if I die today?" simulator — net-to-heirs waterfall | 🔜 |
| 7.7 | Scenario sandbox — fork & diff outcomes | 🔜 |
| 7.8 | Insurance gap analysis + life-insurance needs | 🔜 |
| 7.9 | Will & estate document checklist | 🔜 |
| 7.10 | Annual review generator | 🔜 |
| 7.11 | Executor Mode (first 72 h / 30 days / year) | 🔜 |
| 7.12 | POA (incapacity) Mode | 🔜 |
| 7.13 | Estate equalization planner | 🔜 |
| 7.14 | Estate Readiness Score (0–100) with top-3 fixes | 🔜 |
| 7.15 | EAT (probate) exposure calculator — Ontario rates, restructuring opportunities | 🔜 |
| 7.16 | Deemed-disposition death-tax estimator | 🔜 |
| 7.17 | Registered-account rules engine (TFSA/RRSP/RRIF/RESP/FHSA) | 🔜 |
| 7.18 | T1135/T1141/T1142 foreign-asset compliance + deadlines | 🔜 |
| 7.19 | Government benefits optimizer (CPP/OAS/GIS/ODSP) | 🔜 |
| 7.20 | Life-event wizards (child, marriage/separation, home, retirement, death) | 🔜 |
| 7.21 | Ontario extras: health premium, OTPP/HOOPP, LTB, UVIC, land transfer tax | 🔜 |
| 7.22 | Legal registry — POA holders, will versions, trust docs, landlord compliance | 🔜 |
| 7.23 | CRA audit-readiness score | 🔜 |
| 7.24 | Retirement income projection (CPP/OAS start-age breakeven) | 🔜 |
| 7.25 | Survivor cash-flow stress test | 🔜 |
| 7.26 | Benchmark card (StatCan net worth by age decile, offline) | 🔜 |

## 8. Digital estate & lifestyle

| # | Feature | Status |
|---|---------|--------|
| 8.1 | Digital estate planner — recovery method + digital executor per account | 🔜 |
| 8.2 | Subscription & recurring-cost radar (cancel candidates) | 🔜 |
| 8.3 | Backup status audit for digital assets | 🔜 |
| 8.4 | Crypto inheritance protocol — seed-phrase locations, multisig, recovery card | 🔜 |
| 8.5 | Education & insurance: RESP beneficiary tracker, insurance audit, insurance needs | 🔜 |
| 8.6 | Student loan tracker | 🔜 |

## 9. Platform & engineering

| # | Feature | Status |
|---|---------|--------|
| 9.1 | End-to-end visual test — 113 checks: generation, static artifacts, demo fixture, headless-Chromium interaction incl. quick-add wizard, bulk edit, inline edit, kanban DnD, column config, markdown, auto-save (en/zh), screenshots | ✅ |
| 9.2 | Full en/zh localization (UI + categories + fields) | ✅ |
| 9.3 | Schema as data (`data/*.json`) shared by generator, dashboard, tests | 🔜 |
| 9.4 | Schema versioning + migration | 🔜 |
| 9.5 | Golden-file tests, Python/JS parity vectors, round-trip tests | 🔜 |
| 9.6 | Cleanup of dead code + locale-hardcoded strings | 🔜 |
| 9.7 | Real .xlsx export in-browser (or honest CSV labeling) | 🔜 |
| 9.8 | PWA wrapper — installable, offline, home-screen | 🔜 |
| 9.9 | French (fr-CA) localization | 🔜 |
