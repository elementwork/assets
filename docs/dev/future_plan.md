# Future Plan: Asset Inventory Generator (Merged)

> **Status:** Living document · Last updated 2026-08-09 16:49:47
> **Sources merged (now superseded by this file):** `Improve_plans.md` (Imp-*), `Qoder-plan.md` (Q-*), `Implement_plan.md` (Impl-*)
> **Scope:** Roadmap only — this document plans features; it does not implement them.
> **Legend:** ✅ Done (implemented, see `feature_list.md`) · ⬜ Not started · 🟡 Partial (core exists, gaps remain)
> **Shipped:** Features already implemented are tracked in `feature_list.md`; items here marked ✅ are done and retained for traceability.

The tool generates a structured asset inventory (517 assets, 32 categories, 108 fields)
as Markdown, multi-sheet Excel, and a self-contained HTML dashboard for Canadian families
in Ontario, in English and Chinese. No server, no dependencies, offline-first.

---

## 1. Audit view gaps (finish what exists)

The Audit layout exists but only covers a subset of the planned beneficiary audit (Imp-D2, Q-B3).

- ⬜ **Audit: beneficiary % must sum to 100%** — flag `beneficiary_pct_primary + beneficiary_pct_contingent ≠ 100`
- ⬜ **Audit: minors named as direct beneficiaries** — flag if beneficiary is a minor (needs custodian/trust note)
- ⬜ **Audit: outdated designations** — beneficiary `last reviewed > 2 years`
- ⬜ **Audit: assets bound for estate** — no POD/TOD and no beneficiary → goes through probate
- ⬜ **Audit: will-vs-asset inconsistency** — e.g. designation says 100% spouse but notes say 50/50

## 2. Future roadmap (grouped by theme)

### 2.1 Security & data integrity (P0 — table stakes)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| SEC-1 | **File lock (whole-file encryption)** — AES-256-GCM encrypts the entire dashboard HTML (bootloader gate); birth-date + family-word passphrase; browser unlock with backoff; file becomes email/USB-safe; implemented (default off) | ✅ | Imp-B2, Impl-3.3 |
| SEC-2 | **Schema versioning & migration** — `schema_version` in localStorage/embedded JSON; migration map on load | ⬜ | Imp-G5, Q-F1 |
| SEC-3 | **Session timeout auto-lock** — inactivity (default 15 min) re-locks the vault/master screen | ⬜ | Imp-B5 |
| SEC-4 | **Secure clipboard** — clear clipboard 30 s after copying a credential | ⬜ | Imp-B4 |
| SEC-5 | **Panic/privacy toggle** — one keystroke blurs all currency values + masks account numbers | ⬜ | Q-D5 |
| SEC-6 | **Tamper evidence** — content hash + timestamp embedded on save, verified on load | ⬜ | Q-D6 |
| SEC-7 | **Redacted sharing profiles** — Advisor (no credentials), Executor (all), Family (existence only), Accountant (tax fields), Insurance (insured only); applied to exports | ⬜ | Q-D2, Imp-H3 |
| SEC-8 | **Password health audit** — length/pattern/reuse check on decrypted credentials | ⬜ | Imp-L3 |
| SEC-9 | **Honest CSV naming / real .xlsx** — rename "Excel" export to CSV, or ship a tiny in-browser xlsx writer | ⬜ | Q-F3/F5 |

### 2.2 Ontario tax & estate intelligence (P1 — the moat)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| ON-1 | **EAT (probate) exposure calculator** — 1.5% ≤ $50K + 2.5% above; `probate_excluded` aware; joint-tenancy/POD/TOD auto-exclusion; ranked restructuring opportunities | ⬜ | Imp-A1, Q-B1 |
| ON-2 | **Deemed-disposition death-tax estimator** — (FMV−ACB) × inclusion × marginal rate per non-registered asset; RRSP/RRIF full-inclusion; principal-residence exemption; LCGE; per-spouse rollover scenarios | ⬜ | Imp-A2, Q-B2 |
| ON-3 | **Registered-account rules engine** — TFSA over-contribution 1%/mo penalty + room carryforward; RRIF min-withdrawal by age; RRSP→RRIF at 71; RESP CESG 20%/500/7,200 catch-up; FHSA 15-yr clock; spousal-RRSP 3-yr attribution | ⬜ | Imp-A3/A4, Q-B3 |
| ON-4 | **Estate Readiness Score (0–100)** — beneficiaries named, will location/date, executor+access, POAs, credentials escrowed, insurance in force, guardianship; top-3 fixes | ⬜ | Q-B4 |
| ON-5 | **T1135 foreign-asset compliance** — sum specified foreign property; >$100K CAD → filing banner + per-country table; US-situs exposure; ancillary probate warnings | ⬜ | Q-B5, Imp-A6 |
| ON-6 | **Government benefits optimizer** — OAS clawback, CPP survivor estimate, $2,500 death benefit checklist, GIS hint, ODSP/Henson-trust warning | ⬜ | Q-B6 |
| ON-7 | **Life-event wizards** — new child, marriage/separation (Ontario: separation does NOT revoke designations), home purchase, emigration, retirement, death of spouse | ⬜ | Q-B7 |
| ON-8 | **Ontario extras** — health premium tracker, OTPP/HOOPP DB-pension fields, LTB rent-increase/case tracker, UVIC vehicle certification, land transfer tax (incl. Toronto double-LTT) | ⬜ | Imp-I1–I4, A7 |

### 2.3 Planning & scenarios (P1–P2)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| PL-1 | **Family profile system** — `family_members: [{name, age, relationship, residency}]`, link assets to members, age-based milestones | ⬜ | Imp-H2, Q-A4, Impl-4.2 |
| PL-2 | **"What if I die today?" simulator** — tenancy → probate flow → final tax → survivor benefits → insurance offset → net-to-heirs waterfall per beneficiary | ⬜ | Imp-D1, Q-E1 |
| PL-3 | **Scenario sandbox** — fork data into named scenarios, diff net worth/EAT/death tax side-by-side | ⬜ | Q-E2 |
| PL-4 | **Insurance gap analysis** — total need (debt + income replacement + education + final expenses) − existing coverage = gap card; umbrella check; life-vs-final-tax comparison | ⬜ | Imp-D3, Q-C10 |
| PL-5 | **Will & estate document checklist** — personalized: will, POA ×2, trusts, corporate will, insurance trust, cross-border, pre-nup | ⬜ | Imp-D4 |
| PL-6 | **Annual review generator** — GIC maturities, policy renewals, TFSA/RESP room, stale assets, beneficiary review, will update | ⬜ | Imp-D5, Q-C8 |
| PL-7 | **Executor Mode (first 72h/30d/year timeline)** — insurance claims, CPP death benefit, subscriptions to cancel, institution contacts | ⬜ | Q-C6 |
| PL-8 | **POA (incapacity) Mode** — attorney access per account, POA doc locations, recurring bills, CRA authorization | ⬜ | Q-C7 |
| PL-9 | **Estate equalization planner** — per-beneficiary totals, imbalance flags, strategy suggestions | ⬜ | Imp-8.3 |
| PL-10 | **Retirement income projection** — CPP/OAS start-age model + breakeven; income at 65/70/75 vs desired; RRSP-vs-TFSA guidance | ⬜ | Imp-A8, D6 |
| PL-11 | **Survivor cash-flow stress test** — which income stops/continues, months of runway from liquid assets | ⬜ | Q-E3 |
| PL-12 | **Net worth trend** — `snapshots: [{date, total_fmv, total_acb}]`, auto-snapshot on save, line chart, "what changed since Jan" diff | ⬜ | Imp-C2, Q-A3 |

### 2.4 Liabilities, ownership & computed fields (P1 — net-worth core)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| NW-1 | **Liabilities & true net worth** — `LIABILITY_CATEGORIES` (mortgages, HELOCs, loans, cards, CRA, family loans, co-signs), Net Worth card, debt-to-asset ratio, Excel Liabilities sheet | ⬜ | Q-A1 |
| NW-2 | **Computed-field engine** — declarative registry mirrored in Python+JS: unrealized gain/%, equity, yield, LTV, days-to-renewal, coverage gap | ⬜ | Q-A2 |
| NW-3 | **Ownership model & tenancy** — `owners: [{name, pct, tenancy}]`; sole-ownership concentration warnings; survivor-control simulation | ⬜ | Q-A4 |
| NW-4 | **Asset relationships** — `linked_ids` (mortgage↔property, policy↔insured, box↔contents); delete-orphan warnings | ⬜ | Q-A5 |
| NW-5 | **Multi-currency roll-up** — per-asset currency + FX table; all roll-ups to CAD with as-of date; FX exposure card | ⬜ | Q-A6, Imp-C5 |
| NW-6 | **Attachments & document vault** — base64 attachments (deeds, statements, photos) with size meter; `documents/` folder on generator side | ⬜ | Q-A7 |

### 2.5 Portfolio analytics (P2)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| PA-1 | **Risk dashboard** — liquidity, concentration (institution/category/holding/sector/currency), volatility, insurance ratio, estate exposure gauges | ⬜ | Imp-C3, J4 |
| PA-2 | **Income stream visualization** — monthly income stacked bar by source (interest/dividends/rental/pension/benefits) | ⬜ | Imp-C4 |
| PA-3 | **Tax-loss harvesting detector** — non-registered FMV < ACB, harvestable-loss total, "sell before Dec 31" | ⬜ | Imp-J1 |
| PA-4 | **Asset location optimizer** — current vs tax-optimal placement (equities→TFSA, bonds→RRSP, CDN dividends→non-reg, foreign→RRSP) | ⬜ | Imp-J2 |
| PA-5 | **Rebalancing alerts** — target vs current allocation, drift >5% alert | ⬜ | Imp-J3 |
| PA-6 | **Dividend income tracker** — payment calendar, monthly projection, growth rate, yield-on-cost vs current | ⬜ | Imp-J5 |
| PA-7 | **Mortgage amortization tracker** — balance/equity buildup, prepayment strategy, renewal-date reminder | ⬜ | Imp-J6, M5, Impl-5.4 |
| PA-8 | **Rental property cash flow** — rent/expenses → net cash flow, cap rate, cash-on-cash; portfolio yield; best/worst performers | ⬜ | Imp-M1, Impl-6.1 |
| PA-9 | **Property tax tracking** — assessment, installments, due-date alerts | ⬜ | Imp-M3, Impl-6.2 |
| PA-10 | **HELOC tracker** — limit/balance/rate, draw-period end, repayment schedule | ⬜ | Imp-M2 |
| PA-11 | **Renovation ROI** — history, total invested, ROI per project, ACB impact | ⬜ | Imp-M4 |
| PA-12 | **Benchmark card (offline)** — StatCan net-worth-by-age-decile comparison | ⬜ | Q-E4 |

### 2.6 Data import & interoperability (P2–P3)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| IO-1 | **CSV import from Canadian institutions** — Wealthsimple/Questrade/TD/RBC column-mapper → 108 fields; merge screen (new/changed/unchanged) instead of blind replace | ⬜ | Imp-E1, Q-C3 |
| IO-2 | **Live FX rates (opt-in)** — Bank of Canada or exchangerate-api fetch, timestamped; dashboard stays offline-pure | ⬜ | Imp-E2, Q-G1 |
| IO-3 | **Live crypto prices (opt-in)** — CoinGecko fetch for the 41 crypto assets, green/red price deltas | ⬜ | Imp-E3 |
| IO-4 | **iCal export** — renewals/maturities/RRIF conversion/review dates → downloadable `.ics` | ⬜ | Q-G4 |
| IO-5 | **QR emergency card** — wallet card: inventory location, executor, will location + QR | ⬜ | Q-G3 |
| IO-6 | **Advisor handoff pack** — one command bundles redacted Excel + binder PDF + readiness report + what-if summary into dated `handoff/` | ⬜ | Q-G5 |
| IO-7 | **Print/PDF professional output** — cover, TOC, one page per high-value asset, signature lines, executor appendix (extends existing binder) | ⬜ | Imp-E5, Q-G2 |

### 2.7 UX & workflows (P2)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| UX-4 | **Search highlights** — `<mark>` around matching substrings | ⬜ | Imp-F7 |
| UX-8 | **Virtual scrolling** — IntersectionObserver lazy render for table/compact with 517+ rows | ⬜ | Imp-G6 |
| UX-9 | **Read-only share mode** — copy with edit functions disabled + watermark | ⬜ | Imp-H1 |
| UX-10 | **Subscription & recurring-cost radar** — `annual_fee`/renewals → recurring burn card + next-renewal calendar (executor's cancellation list) | ⬜ | Imp-L2, Q-C9 |
| UX-11 | **Digital estate planner** — recovery method + digital executor per online account; no-recovery red flags; legacy-contact checklist (Google/Apple/Facebook) | ⬜ | Imp-L1, 8.1, Q-D4 |
| UX-12 | **Backup status audit** — backed-up/not/unknown per digital asset + critical-asset alerts | ⬜ | Imp-L4 |
| UX-13 | **Education & insurance deep dive** — RESP beneficiary tracker (age, CESG, years to post-secondary), insurance audit (coverage by type, premium efficiency), life-insurance needs analysis | ⬜ | Imp-N1, 7.1–7.3 |
| UX-14 | **Student loan tracker** — NSLSC/interest/grace/repayment + interest tax deduction | ⬜ | Imp-N2 |
| UX-15 | **Legal registry** — POA holders + alternates + review dates; will versions/locations/lawyer; trust docs; >3yr stale alerts; landlord compliance (Ontario Standard Lease, rent guidelines, LTB) | ⬜ | Imp-K1–K3 |
| UX-16 | **CRA audit readiness score** — % ACB documented, valuation dates, source docs, registration; "Audit Readiness: 78%" | ⬜ | Imp-K5 |
| UX-17 | **Compliance deadlines calendar** — T1135/T1141/T1142 April-15 countdowns | ⬜ | Imp-K4, Q-B5-lite |
| UX-18 | **Crypto inheritance protocol** — per-wallet custody type, seed-phrase *location* (never phrase), multisig quorum, dead-man's-switch notes, printable recovery card | ⬜ | Q-D3 |

### 2.8 Engineering & platform (P2)

| ID | Feature | Status | Source |
|----|---------|--------|--------|
| EN-1 | **Schema as data** — `data/*.json` (categories/fields) consumed by generator, dashboard, and tests; `schema_version` + migrations | ⬜ | Q-F1 |
| EN-3 | **Cleanup** — drop unused `os`, `Any`, `translate_categories`, `active_count`; remove hardcoded zh in Excel Sheet 3; route currency/date formatting through locale | ⬜ | Q-F3 |
| EN-4 | **Test expansion** — schema invariants (field/category counts, unique ids, selects have options), golden-file Markdown/Excel, Python/JS parity vectors, import→export round-trip | ⬜ | Q-F4 |
| EN-5 | **PWA wrapper (optional)** — manifest + service worker over the same single file; installable, offline, iOS home-screen | ⬜ | Q-F6 |
| EN-6 | **French (fr-CA) localization** — third locale on existing i18n rails | ⬜ | Q-F7 |

---

## 3. Suggested build order

1. **Foundation (P0):** ~~SEC-1 file lock (done)~~, SEC-2 schema versioning, SEC-9 honest CSV/xlsx, EN-3 cleanup, EN-4 test expansion — hardens what exists before adding surface area.
2. **Net-worth core:** NW-1 liabilities, NW-2 computed fields, NW-3 ownership/tenancy, PL-1 family profiles, IO-1 CSV import, PL-12 net worth trend.
3. **Ontario estate brain (the differentiator):** ON-1 EAT, ON-2 death tax, ON-4 readiness score, PL-2 death simulator, PL-7 Executor Mode.
4. **Trust layer:** SEC-7 sharing profiles, SEC-8 password health, UX-18 crypto protocol, IO-7 professional binder, ON-5 T1135.
5. **Depth & delight:** PA-1…12 analytics, UX-10…17 (subscriptions, digital estate, legal, deadlines), PL-3/4/6/8 scenarios, IO-2…6 feeds/exports, EN-5/6 platform.

## 4. Verification

- `python3 tests/e2e_visual_test.py` — all 125 checks green after every change (regenerates outputs, validates Markdown/Excel/HTML, drives both dashboards headless)
- Golden path per feature: load demo fixture → act → save HTML → reopen in a fresh browser → state persists
- Security: locked file is ciphertext in a text editor (bootloader gate); wrong birth date/family word rejected with backoff; save-HTML in a locked session stays encrypted
- Docs: every new field documented in `docs/dev/ASSET_FIELDS.md`
