# Feature List: Asset Inventory Generator

> **Status:** Living document · Last updated 2026-08-09 16:30:38
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
| 1.2 | 108-field schema per asset (ownership, registration/tax, beneficiaries, insurance, digital, crypto, notes…) | ✅ |
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
| 2.9 | Detail: master-detail with all 108 fields | ✅ |
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
| 4.1 | Whole-file encryption (File Lock, default off) — AES-256-GCM via Web Crypto, PBKDF2 100k, bootloader unlock gate | ✅ |
| 4.2 | Lock UX: birth date (YYYYMMDD) + family word, confirm, enable → downloads encrypted copy; disable → plain copy | ✅ |
| 4.3 | Locked file: browser shows unlock gate; text editor sees only ciphertext; wrong-passphrase backoff (exponential wait) | ✅ |
| 4.4 | XSS-safe rendering — event delegation, HTML-escaped ids | ✅ |
| 4.5 | CSV formula-injection guard (`= + - @` prefix) + RFC-4180 escaping | ✅ |

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
| 7.1 | Audit view — traffic-light validation: missing beneficiary (red), missing FMV/ACB/institution/owner (yellow), bad selects, TFSA over-contribution, stale >12 months | ✅ |

## 8. Platform & engineering

| # | Feature | Status |
|---|---------|--------|
| 8.1 | End-to-end visual test — 125 checks: generation, static artifacts, demo fixture, headless-Chromium interaction incl. quick-add wizard, bulk edit, inline edit, kanban DnD, column config, markdown, auto-save (en/zh), plus file-lock (encrypt/unlock/backoff/re-save) and regression coverage for CSV injection, numeric-id import, audit filters, compact collapse (en/zh), screenshots | ✅ |
| 8.2 | Full en/zh localization (UI + categories + fields) | ✅ |
