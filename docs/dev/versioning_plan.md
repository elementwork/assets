# Versioning Plan: Free / Family / Planning / Advisor

> **Status:** Living document · Last updated 2026-08-19 12:59:00
> **Product:** Self-contained, offline-first asset inventory for Canadian families in Ontario
> (single-file HTML dashboard, en/zh). Generator is **closed-source**; artifacts are the product.
> **Companion docs:** `feature_list.md` (what exists), `future_plan.md` (what's next),
> `promotion_plan.md` (go-to-market). This document defines tiers, data storage, save model,
> copy protection, and engineering.

---

## 1. Decisions (locked)

1. **Buy-out = perpetual, no forced expiry.** A one-time purchase stays usable forever; only
   policy figures (CPP/OAS/TFSA limits, tax rates, etc.) change yearly and are refreshed via an
   **optional annual update pack ($19/yr, Planning tier)**. Update-pack licenses carry an
   expiry; expiry stops updates only, never disables features.
2. **Generator is closed-source.** Users cannot produce paid files themselves. Free files are
   downloaded from a landing page; paid files are delivered by email with an embedded license.
3. **Pricing:** Free $0 · Family $29 one-time · Planning $99 one-time (optional $19/yr update
   pack) · Advisor $149/yr (white-label $299, Estate-pro $499).
4. **Four tiers; Advisor deferred.** Advisor ($149/yr) + insurance-broker lead-gen is a
   **next-round topic**, not implemented now.
5. **Export is Planning-tier only** (in-dashboard MD/CSV/JSON buttons + generator Markdown/Excel
   artifacts). **Save (data persistence) and Print stay in all tiers.**
6. **Catalog size differentiates tiers** by cutting whole categories:
   Free 15/256 → Family 20/324 → Planning 32/517.
7. **Save model:** Chrome/Edge use the File System Access API for explicit user-selected Direct Save when available. Every selected existing target is verified against the embedded `inventory_id` before overwrite. Firefox/Safari and denied API contexts retain the staged Ctrl+S / direct-download fallback.
8. **Data-block encryption (not whole-file):** only the `assets` payload inside the embedded
   `INVENTORY_DATA` is AES-GCM encrypted (key = family word). Templates/catalog stay plaintext.
   Replaces the whole-file bootloader approach.
9. **Copy protection = family binding + signed license + watermark.** Honest boundary: an
   offline HTML cannot be made truly uncopyable; goal is "copies are unusable and traceable".

---

## 2. Feature → tier map

### 🟢 Free ($0)
- **Catalog:** 15 categories / 256 items — Cash (10), Fixed Income (15), Equities (15),
  Registered Accounts (15), Pension (17), Insurance (28), Real Estate (15), Vehicles (13),
  Valuables (15), Household (15), Loyalty (31), Deposits (14), Joint (9), Gov Benefits (25),
  Gov Programs (19).
- **Layouts:** Dashboard, Compact, Detail, Kanban.
- **Features:** full editing, undo/redo, quick-add, search/filters, stats, markdown notes,
  **Save** (stage + Ctrl+S; Safari download fallback), **File Lock** (family-word encryption),
  localStorage, en/zh, beforeunload flush.
- **Excluded:** Table/Timeline layouts, Print/PDF binder, charts, Export buttons, generator
  MD/Excel, Ontario modules, advisor features.
- **Distribution:** free HTML download from landing page.

### 🟡 Family ($29 one-time)
- **Catalog:** 20 categories / ~324 items (Free 15 + Employment (11) + Digital Online (17) +
  Digital Business (14) + Digital Content (13) + Digital Accounts (13)).
- **Adds:** Table (big grid) + Timeline layouts, 5 templates + dark mode (UI enhancement),
  **Print/PDF estate binder** (code-generated print view), **basic 2 charts**
  (category donut + top-institutions h-bar).
- **Still excluded:** Export buttons, generator MD/Excel, full charts, Ontario modules.
- **Support:** email 48h.

### 🟠 Planning ($99 one-time; optional $19/yr update pack)
- **Catalog:** 32 categories / 517 items (adds crypto ecosystem, IP, business, trusts,
  foreign, etc.).
- **Adds:** Charts + Audit layouts, all 4 charts + audit + net-worth trend, **Export**
  (in-dashboard MD/CSV/JSON + generator MD/Excel), **Ontario intelligence**
  (EAT, death-tax estimator, registered-account rules, readiness score, advanced audit),
  **deep analysis framework** (net worth/liabilities, computed fields, subscription radar,
  annual review).
- **Support:** email support, annual update pack (policy figures), backup guidance.

### 🔴 Advisor ($149/yr) — **deferred to next round**
- Advisor workflows, family/scenario modules, net-worth core, compliance, white-label/API/SLA,
  insurance-broker lead-gen. Not implemented now; research framework in `future_plan.md`.

---

## 3. Data storage (`INVENTORY_DATA`)

Single authoritative data block embedded in the file:

```js
const INVENTORY_DATA = {
  "format": "asset-inventory",
  "version": 2,            // data-format version
  "schema_version": 2,     // 116-field schema incl. Emergency & Handoff
  "inventory_id": "INV-…", // stable file/family binding identity
  "tier": "free",          // free | family | planning | advisor
  "key_version": 1,        // decryption key chain version
  "generated": "2026-08-09",
  "assets": <encrypted or plaintext asset array>
};
```

- File is the single source of truth; localStorage is a session cache only (defaults to
  file-first to avoid origin-overwrite bugs).
- **Data-block encryption:** when a family word is set, `assets` is AES-GCM encrypted with the
  family-word-derived key (PBKDF2 100k). Template/catalog stay plaintext. Real encryption
  (key never in file), not hardcoded obfuscation.
- **Key chain:** `KEY_REGISTRY = {1: <v1>, 2: <v2>, ...}` — new files use the latest key;
  historical keys stay read-only so any version can import older files. Upgrade-safe.
- **Upgrade = swap renderer file, reuse data:** a Family/Planning file opens with the same
  `INVENTORY_DATA` (import by reading the old HTML's data block). Zero migration.

---

## 4. Save model (the core UX)

**Principle:** use the strongest browser-supported persistence path while keeping a complete offline fallback. Chromium Direct Save is preferred; staged native save/download remains universal.

1. Every edit / auto-save updates the DOM data script to the latest payload
   (plaintext or ciphertext depending on family word) — data is always "staged" in the file.
2. The **Save button is always visible**, with per-browser behavior:
   | Browser | Click "Save" → |
   |---------|----------------|
   | Chrome / Edge / Firefox | Stage data → show guidance: **"✅ 已暂存 — 按 Ctrl+S / Cmd+S 选择位置保存"** with a secondary "直接下载到下载文件夹" button |
   | Safari | Stage data → direct download + toast "已保存到下载文件夹" (Safari can't native-save HTML) |
3. Auto-save: debounced 1.5s → localStorage (fallback) + update DOM data script. `beforeunload`
   flushes pending edits to localStorage.
4. **File Lock (Free):** family-word encryption of the `assets` block. Unlock = in-page overlay
   (birth date + family word), not a bootloader file. Enabling encryption requires one save
   action to produce the encrypted file (accepted).

---

## 5. Copy-protection architecture

| Layer | Mechanism |
|-------|-----------|
| Closed generator | Users cannot regenerate paid files themselves. |
| Signed license | license = RSA/HMAC-signed JSON `{tier, order_id, buyer, issued, expires?}`; public key embedded; validated on load. Buy-out licenses have no expiry; update-pack licenses expire (updates only). |
| Family binding | Paid modules require *valid license + family-word session*. A copied file without the family word is unusable. |
| Watermark | Purchaser name/email written into footer, print, exports. |
| Estate continuity | Family/executor opening a paid file (with family word) never pays again. |

**Honest boundary:** code-level bypass cannot be 100 % prevented on an offline artifact; goal
is "copies are unusable and traceable".

---

## 6. Engineering implementation

- **Generator:** `--tier free|family|planning --license <token> --buyer "Name <email>"`;
  `FREE_CATEGORIES` / `FAMILY_CATEGORIES` constants filter the 517 catalog; build-time tier
  stripping so lower tiers contain **no** higher-tier code/content (conditional-compile style).
  Artifacts: Free/Family = HTML only; Planning = HTML + Markdown + Excel.
- **Dashboard:** `APP_TIER` + feature-gate table; page-internal unlock overlay (family word);
  Save button with browser detection (native-save guidance vs Safari download); data-script
  sync on every edit/auto-save; `INVENTORY_DATA` + key chain + data-block encryption.
- **E2E parametrized per tier:** catalog counts (15/20/32), layout/export/chart/print
  visibility, license valid/invalid/expired, watermark, ciphertext-block present + decrypted
  count, browser-branch save logic.
- **116-field schema identical across tiers** → upgrading is "open the paid file", no migration.
- Docs fully updated with timestamps.

---

## 7. Go-to-market

| Tier | Channel | Core action |
|------|---------|-------------|
| Free | Landing page, Reddit, Xiaohongshu, YouTube, SEO | 3 checklist lead magnets, comparison page, demo file, email list |
| Family | In-dashboard upgrade prompts, referrals | "Unlock Table/Print/Charts" prompts; gift-to-parents; broker/lawyer referrals |
| Planning | Upsell from Family; organic | "Unlock full catalog / Export / Ontario intelligence"; annual update pack |
| Advisor | B2B direct (deferred) | Next round |

---

## 8. Post-sales service

| Tier | Support | Updates |
|------|---------|---------|
| Free | FAQ / in-app help / community form | — |
| Family | Email 48h | — |
| Planning | Email 48h | Optional $19/yr update pack (policy figures); backup guidance |

---

## 9. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| License bypassed by skilled user | Accepted boundary; family binding + watermark raise cost |
| Free too complete → nobody pays | Catalog + Table/Print/Charts (Family) + Export/Ontario (Planning) stay clearly paid |
| Family blocked by paywall | Paid capability travels with the file; family never pays |
| Ctrl+S not understood by users | Save button guidance text + "直接下载" fallback button |
| Safari can't native-save HTML | Auto-detect Safari → direct download fallback |
| Offline expiry unenforceable | Buy-out perpetual; update-pack expiry = updates only |
| Data split between file & localStorage | localStorage is session cache only; data script is source of truth |

---

## 10. Execution order

1. Generator `--tier` + catalog filter + `INVENTORY_DATA` + data-block encryption + key chain.
2. Dashboard: tier gating, in-page unlock overlay, Save button (stage + Ctrl+S guidance /
   Safari download), data-script sync, beforeunload flush.
3. License + watermark (paid tiers).
4. E2E per-tier parametrization.
5. Docs + timestamps + commit & push (docs-update-before-commit enforced).


## 4a. Direct Save + inventory binding (shipped 2026-08-19 12:59:00)

- Chrome/Edge: Save opens a File System Access picker on first use, then reuses that in-session handle for direct writes. **Save As** always asks for a target.
- Before overwriting an existing target, the dashboard extracts its `inventory_id`; a mismatch or missing ID is blocked. This prevents accidentally saving Family A into Family B's inventory file.
- Firefox/Safari/API-denied contexts retain stage-to-DOM + Ctrl/Cmd+S and direct-download fallbacks.
- `inventory_id` is embedded in the versioned data block and printed on the Emergency Access Guide / Master Asset Index.
- Schema v2 adds eight Emergency & Handoff fields while remaining identical across Free/Family/Planning tiers.
