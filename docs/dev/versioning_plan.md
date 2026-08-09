# Versioning Plan: Free / Plus / Pro

> **Status:** Living document · Last updated 2026-08-09 17:31:28
> **Product:** Self-contained, offline-first asset inventory for Canadian families in Ontario
> (single-file HTML dashboard, en/zh). Generator is **closed-source**; artifacts are the product.
> **Companion docs:** `feature_list.md` (what exists), `future_plan.md` (what's next),
> `promotion_plan.md` (go-to-market). This document defines how features split into paid tiers.

---

## 1. Decisions (locked)

1. **Buy-out = perpetual, no forced expiry.** A one-time purchase stays usable forever;
   only policy figures (CPP/OAS/TFSA limits, tax rates, etc.) change yearly and are refreshed
   via an **optional annual update pack ($19/yr)**.
2. **Generator is closed-source.** Users cannot produce paid files themselves. Free files are
   downloaded from a landing page; paid files are delivered by email with an embedded license.
3. **Plus price anchor: $49 one-time.**
4. **Export is paid.** The in-dashboard Export MD/CSV/JSON buttons AND the generator's
   Markdown/Excel artifacts are paid-tier only. **Save HTML and Print stay free** (they preserve
   the "file = database" promise and browser-native printing).
5. **Free catalog: cut whole categories** (15 / 256 items); kept categories remain complete.
6. **Free gets all core dashboard features** (except Export). Differentiation = catalog size +
   paid intelligence modules.
7. **Copy protection = family binding + signed license + watermark.** Honest boundary: an
   offline HTML file cannot be made truly uncopyable; the goal is "copies are unusable and
   traceable", not "cannot be copied".

---

## 2. Feature → tier map

### 🟢 Free ($0)
- **Catalog:** 15 categories / 256 items — Cash (10), Fixed Income (15), Equities (15),
  Registered Accounts (15), Pension (17), Insurance (28), Real Estate (15), Vehicles (13),
  Valuables (15), Household (15), Loyalty (31), Deposits (14), Joint (9), Gov Benefits (25),
  Gov Programs (19).
- **Features:** all core dashboard — 8 layouts, full editing, undo/redo, quick-add, bulk,
  inline, kanban, column config, markdown notes, search/filters, stats, 4 SVG charts, basic
  audit, print estate binder, **Save HTML** (carries edits), localStorage, en/zh.
- **Excluded:** Export MD/CSV/JSON buttons (upgrade prompt instead), generator MD/Excel
  artifacts (HTML only), File Lock, Ontario calculators, PDF/iCal/QR, any advisor features.
- **Distribution:** free HTML download from landing page.
- **Support:** FAQ, in-app help, community form.

### 🟡 Plus ($49 one-time; optional $19/yr update pack)
- **Catalog:** 32 categories / 517 items (adds crypto ecosystem, digital assets, business,
  trusts, foreign, etc.).
- **Security:** File Lock (whole-file encryption, family binding), session auto-lock,
  secure clipboard, panic/privacy toggle, tamper evidence, password health audit.
- **Ontario intelligence (moat):** EAT (probate) exposure calculator, deemed-disposition
  death-tax estimator, registered-account rules engine (TFSA/RRSP/RRIF/RESP/FHSA),
  Estate Readiness Score 0–100, advanced audit (beneficiary %/minors/stale designations).
- **Planning:** annual review generator, subscription & recurring-cost radar, net worth trend.
- **Output:** in-dashboard Export MD/CSV/JSON, generator Markdown + Excel artifacts,
  professional PDF estate binder, iCal export, QR emergency card.
- **Support:** email support (48h), annual update pack (policy figures), backup guidance.

### 🔴 Pro ($149/yr per seat; white-label $299/yr; Estate-pro $499/yr)
- **Everything in Plus, plus:**
- **Advisor workflows:** redacted sharing profiles (SEC-7), advisor handoff pack (IO-6),
  bulk client generation, CSV import from Canadian institutions + merge (IO-1).
- **Family & scenarios:** family profiles (PL-1), death simulator (PL-2), scenario sandbox
  (PL-3), Executor Mode (PL-7), POA Mode (PL-8), estate equalization (PL-9).
- **Net-worth core:** liabilities & true net worth (NW-1), computed-field engine (NW-2),
  ownership/tenancy model (NW-3), asset relationships (NW-4), multi-currency (NW-5),
  attachment vault (NW-6).
- **Deep analytics:** risk dashboard (PA-1), income streams (PA-2), tax-loss harvesting (PA-3),
  asset-location optimizer (PA-4), rebalancing alerts (PA-5), dividend tracker (PA-6),
  mortgage/rental/property-tax/HELOC/renovation (PA-7…11).
- **Compliance:** T1135 (ON-5), CRA audit-readiness (UX-16), compliance deadlines calendar
  (UX-17), legal registry (UX-15).
- **Platform:** white-label/logo, API/CLI automation, SLA, multi-client workspace.
- **Support:** priority support (24h), onboarding, client template customization, annual
  compliance update.

---

## 3. Copy-protection architecture

| Layer | Mechanism |
|-------|-----------|
| Closed generator | Users cannot regenerate paid files themselves. |
| Signed license | license = RSA/HMAC-signed JSON `{tier, order_id, buyer, issued}`; public key embedded in dashboard; validated on load → anti-tamper / anti-forgery. |
| Family binding | Paid modules require *valid license + family-word session* (reuses File Lock PBKDF2/AES-GCM). A copied file without the family word is an unusable shell. |
| Watermark | Purchaser name/email written into footer, print, and exports → traceability. |
| Estate continuity | Family/executor opening a paid file (with the family word) never pays again — paid capability travels with the file. |

**Honest boundary:** code-level bypass cannot be 100 % prevented on an offline artifact; the
goal is "copies are unusable and traceable", not "cannot be copied".

---

## 4. Engineering implementation

- Generator: `--tier free|plus|pro --license <token> --buyer "Name <email>"`; `FREE_CATEGORIES`
  constant filters the 517-item catalog to 15/256.
- Dashboard: `APP_TIER` constant + feature-gate table; paid modules gated by license check +
  family-word session.
- Export buttons hidden per tier with upgrade prompt; Save HTML / Print always available.
- Generator artifacts: Free = HTML only; Plus/Pro = HTML + Markdown + Excel.
- E2E parametrized for both tiers: free/paid counts, license valid/invalid/expired, watermark,
  export-button visibility.
- **108-field schema is identical across tiers** → upgrading Free→Plus is "open the paid file",
  no migration; JSON import interoperable.
- Docs fully updated with timestamps (incl. rewriting promotion_plan's "open-source marketing
  engine" premise).

---

## 5. Go-to-market

| Tier | Channel | Core action |
|------|---------|-------------|
| Free | Landing page, Reddit, Xiaohongshu, YouTube, SEO | 3 checklist lead magnets, comparison page, `--demo` demo file, email list |
| Plus | In-dashboard upgrade prompts, referrals | "Unlock full catalog / Export / Readiness Score" prompts; gift-to-parents; broker/lawyer referrals |
| Pro | B2B direct, partners | 20 lawyers + 20 planners free pilots, white-label co-branding, 20–30 % affiliate, CPA tax-season partnership, case studies |

---

## 6. Post-sales service

| Tier | Support | Updates |
|------|---------|---------|
| Free | FAQ / in-app help / community form | Generator updates (internal) |
| Plus | Email 48h | Optional $19/yr update pack (policy figures); backup guidance |
| Pro | Priority 24h, SLA, onboarding | Annual compliance update, white-label assets, client template customization |

---

## 7. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| License bypassed by skilled user | Accepted boundary; family binding + watermark raise cost; Pro revenue rests on service/white-label |
| Free too complete → nobody pays | Catalog size + Export + intelligence modules stay clearly paid |
| Family blocked by paywall | Iron rule: paid capability travels with the file; family never pays |
| Offline expiry unenforceable | Plus is perpetual by design; Pro annual fee is a service/subscription (updates + support), not a feature lock |
| Closed generator reduces marketing surface | Replace GitHub-star funnel with landing-page downloads + content + B2B |

---

## 8. Execution order

1. Write this plan + rewrite promotion_plan.md premise (closed source, 3 tiers).
2. Implement generator `--tier` + license/watermark + catalog filter.
3. Implement dashboard tier gating + Export visibility + family-binding on paid modules.
4. E2E dual-tier parametrization.
5. Docs + timestamps; commit & push (docs-update-before-commit enforced).
