# Promotion & Sales Plan: Asset Inventory Generator

> **Status:** Living document · Last updated 2026-08-10 01:10:36
> **Product:** Self-contained, offline-first asset inventory for Canadian families in Ontario
> (single-file HTML dashboard, en/zh, optional whole-file encryption)
> **Pricing model:** 3 tiers — Free / Plus ($49) / Pro ($149/yr) — see `versioning_plan.md`
> **Generator:** closed-source; free files download from the landing page, paid files are
> delivered by email with an embedded license.
> **Companion docs:** `feature_list.md` (what to sell), `future_plan.md` (what's next),
> `versioning_plan.md` (feature→tier map).

---

## 1. Positioning

**One-liner:** *"The estate binder your family can actually open — even without an app, an
internet connection, or you."*

**The wedge problem (why people buy):**
1. **Death is a paperwork disaster** — spouses/executors inherit scattered accounts, unknown
   subscriptions, unmapped crypto, no beneficiary list. This tool is the single file that
   fixes it.
2. **Generic apps are online and US-centric** — most inventory/net-worth tools store data in
   the cloud and ignore Ontario-specific rules (probate/EAT, TFSA/RRSP/RESP/FHSA, T1135,
   Ontario land transfer tax, OTPP/HOOPP).
3. **Existing estate binders are static PDFs** — lawyers hand out forms; this is a living,
   editable, self-contained dashboard that carries its own edits.

**Positioning statement:**
> For Ontario families (and their advisors) who want one offline, self-contained file that
> catalogs every asset, flags estate gaps, and survives the user — the Asset Inventory
> Generator is the only tool that generates a fully portable Markdown/Excel/HTML package
> with a built-in file lock, audit, and estate-readiness view, without any cloud
> dependency.

**Brand pillars:** Private by design · Ontario-smart · Zero-dependency · Family-ready.

---

## 2. Target audience (segmented)

| Segment | Who | Pain | Angle | Willingness to pay |
|---------|-----|------|-------|--------------------|
| **S1 — Estate planning lawyers & paralegals** | Ontario estates/elder-law firms | Clients arrive with no inventory; discovery is weeks of back-and-forth | Client-engagement tool: send the file, client fills it, advisor gets a clean binder | High (B2B seat/white-label) |
| **S2 — Financial advisors & planners** | Fee-for-service planners, insurance brokers | No standardized inventory; compliance wants documented client facts | "Redacted Advisor Profile" export, readiness score, annual review generator | High (B2B) |
| **S3 — DIY families (40–70)** | Ontario homeowners with TFSAs/RRSPs/RESPs, aging parents | Wants a binder but won't pay $2–5k for a lawyer consultation just to organize | $49 one-time Plus; giftable to aging parents | Medium |
| **S4 — Executors & caregivers** | Recently bereaved, POA attorneys | Needs a crisis-mode runbook now | Executor Mode: first 72 hours checklist, institution contacts, subscription kill-list | High urgency, one-off |
| **S5 — Crypto & digital-heavy households** | HNW individuals with wallets, business owners | Value dies with the owner; no offline protocol | Crypto inheritance protocol, digital executor, seed-location cards | Medium–High |
| **S6 — Mandarin-speaking families (Canada)** | Chinese-Canadian households (GTA/GVRD) | Same pain, underserved by English-only tools; estate topics discussed within family in Chinese | Full zh localization is a differentiator, not a translation afterthought | Medium |

**Primary go-to-market: S1 + S2 (advisors) first** — they are distribution multipliers
(each advisor reaches dozens of families) and they buy tools; S3/S6 come via their
recommendation and organic content.

---

## 3. What we're actually selling

**Not a "net worth tracker" — a "family financial continuity system":**

- **The artifact:** one self-contained `.html` file that is the inventory *and* the app.
  Email it, USB it, reopen anywhere — edits persist in the file itself (Save-HTML carries edits).
- **The guarantees:** offline forever, no account required, no data leaves the device,
  optional whole-file encryption with a birth-date + family-word passphrase (default off),
  no-passphrase = no recovery (clear trade-off UX).
- **The outputs:** Markdown reference, 8-sheet Excel, print-ready estate binder, CSV/JSON exports.
- **The intelligence (roadmap):** EAT/probate exposure, death-tax estimate, estate readiness
  score, audit flags, executor/POA modes.

**Value props to lead with in copy:**
1. *One file. No account. No cloud.*
2. *Your executor doesn't need a subscription to read your estate plan.*
3. *Ontario rules built in — probate, TFSA/RRSP/RESP/FHSA, T1135, land transfer tax.*
4. *Optional whole-file encryption — lock the file with a passphrase only your family knows.*
5. *Chinese and English in the same product.*

---

## 4. Product-marketing artifacts to build (before launch)

| Artifact | Purpose | Notes |
|----------|---------|-------|
| Demo file with `--demo` fixture | Screenshot tours, press, first-run | Realistic Ontario family (2 adults, 2 kids, house+mortgage, TFSAs/RRSPs/RESP, dormant crypto) |
| 90-second explainer video | Landing page hero | Screen-capture: open file → fill → lock file → audit → print binder |
| 6 screenshot set | Every layout + audit + charts + zh | Light/dark, mobile viewport |
| Live interactive demo (hosted copy of the dashboard) | Try-before-download | Static hosting only; no backend, no PII |
| One-page "What executors need" PDF | Lead magnet for S4 | Generated by the tool itself — dogfooding |
| "Ontario Estate Checklist" PDF | Lead magnet | 20-point checklist; CTA to the tool |
| Compare page: vs spreadsheets, vs Notion, vs cloud net-worth apps, vs lawyer binder | Conversion | Honest table — offline/self-contained/encrypted/Ontario are our columns |

---

## 5. Pricing & packaging (3 tiers)

| Tier | Price | Contents |
|------|-------|----------|
| **Free** | $0 | Landing-page HTML download: 15 categories / 256 assets, all core dashboard features, Save HTML + Print. No Export, no File Lock, no Ontario modules |
| **Plus** | $49 one-time (optional $19/yr update pack) | Full 32-category catalog, Export (MD/CSV/JSON + generator MD/Excel), File Lock + security suite, Ontario calculators (EAT/death tax/registered rules), readiness score, PDF/iCal/QR, email support |
| **Pro** | $149/yr per advisor (white-label $299/yr, Estate-pro $499/yr) | Plus for N clients + advisor workflows (redacted profiles, handoff pack, CSV import, bulk clients) + family/scenario/estate modules + net-worth analytics + compliance + API/CLI + SLA + white-label |

**Principles:**
- Generator is closed-source: paid capability cannot be regenerated by users; paid files carry
  a signed license + family binding + watermark (see `versioning_plan.md`).
- Plus is a perpetual buy-out — always usable, never forced to expire. Policy figures
  (CPP/OAS/TFSA limits, rates) change yearly and are refreshed via the optional $19/yr update
  pack; recurring revenue must come from Pro (service/subscription) and updates, not from
  locking the file.
- Advisors are the revenue floor (B2B); families are the volume.
- Free is the trust funnel: complete enough to be genuinely useful, minus Export and the
  intelligence modules that justify upgrading.

---

## 6. Channels & campaigns

### 6.1 Organic (primary, zero budget)
- **Landing page + free download** — the funnel hub: Free tier HTML download, `--demo` demo file,
  screenshots, comparison page, email-capture. Generator is closed-source; the downloadable
  Free artifact IS the marketing engine.
- **r/PersonalFinanceCanada, r/CanadianInvestor, r/EstatePlanning, r/FatFIRE, r/PersonalFinanceCanadaCrypto** —
  launch post: "I built a free offline estate binder for Ontario families — here's what
  happens to your accounts when you die." (Follow subreddit self-promo rules: contribute, then share.)
- **Lawyer/advisor directories** — content contributions, not ads: offer a free
  "client inventory intake" template lawyers can rebrand.
- **Mandarin community** — WeChat/RED (小红书) posts in Chinese for the zh build; GTA
  Chinese media (加国无忧/51.ca, 超级生活) — very underserved niche.
- **YouTube** — "I organized my parents' entire estate in one offline file" walkthrough;
  "What your executor needs from you today" (great for S4/S3).

### 6.2 Paid (after PMF signals)
- **Google Ads:** keywords — "estate inventory template Canada", "what is probate Ontario",
  "TFSA over-contribution penalty", "online estate binder Canada".
- **Meta/Reddit ads:** 45–65 demo targeting; interest stack: estate planning, personal
  finance Canada, retirement planning.
- **LinkedIn:** advisors/paralegals — "give clients a 5-minute inventory that fills itself."

### 6.3 Partnerships (force multiplier)
- **Estate lawyers (S1):** free Pro seats for a pilot; they hand the file to every new
  client; we co-brand ("prepared with X Law's Estate Binder").
- **Fee-for-service planners (S2):** affiliate 20–30% recurring; they use it as their
  annual-review instrument.
- **Insurance brokers:** binder surfaces coverage gaps → natural upsell conversation.
- **Chartered Professional Accountants (CPAs)** for tax season + T1135 angle.
- **Funeral homes / memorial planners** (S4) — a dark but real channel for the executor runbook.

### 6.4 Launch sequence (90 days)
| Week | Action |
|------|--------|
| 1–2 | Generate Free demo file + `--demo` fixture; record video; write 3 lead magnets; set up landing page + download |
| 3 | Landing-page launch + Reddit launch post (timed weekday, EST); open Plus early-bird sales |
| 4 | Mandarin launch (zh demo + WeChat/RED content) |
| 5–8 | Pilot 5–10 advisors/lawyers free; collect testimonials + referral mechanics |
| 9–12 | Paid ads on top 10 keywords; publish 4 comparison/checklist articles; iterate on pricing |

---

## 7. Content strategy (sales enablement)

| Asset | For whom | CTA |
|-------|----------|-----|
| "What your executor needs from you today" checklist | S3/S4 | Download the binder |
| "Ontario probate 101: what goes through EAT and how to reduce it" | S1/S2/S3 | Try the EAT calculator (roadmap) |
| "TFSA/RRSP/RESP/FHSA room cheat-sheet 2026" | S3/S6 | Generate your inventory |
| "T1135 explained: foreign property over $100K" | S2/S6 | Audit your foreign assets |
| "The case for an offline estate file (privacy in estate planning)" | S2/S5 | Switch to self-contained |
| Case study: "How a GTA family organized 300+ assets in one weekend" | S3/S6 | Start free |

**Dogfood rule:** every lead magnet is *produced by the tool* — it demonstrates the output
and seeds the "why" of the product simultaneously.

---

## 8. Metrics & success criteria

| Metric | Target (3 months) | Target (12 months) |
|--------|-------------------|--------------------|
| Free downloads (landing page) | 2,000 | 25,000 |
| Plus purchases (free→paid) | 100 | 2,000 |
| Advisor pilots → paying | 10 pilots, 3 paying | 150 paying advisors |
| zh share of users | 15% | 25% |
| NPS (survey in-app) | 40 | 55 |
| Trial→activation (created ≥20 assets) | 40% | 50% |
| Revenue | — | $50k ARR |

**North-star metric:** *number of families with a current (≤12-month-reviewed) inventory
file.* Everything (checklists, templates, renewals) should push toward "open the file, update
it, re-save."

---

## 9. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| "It's just a spreadsheet" perception | Lead with estate-readiness/audit/file-lock/print binder; comparison page vs spreadsheets |
| Legal liability (giving tax/legal advice) | Clear disclaimers: "educational estimates, not advice"; position as organizer, calculators labeled estimates |
| Open-source → nobody pays | Keep intelligence (file-lock/audit/Ontario modules) in paid tiers; free is the marketing engine |
| Chinese market regulatory/content concerns | No financial advice claims; zh marketing stays descriptive of features, not guarantees |
| Advisor adoption is slow | Free pilots, white-label, "intake template" give-away; win one firm, clone the playbook |
| Data-loss fear ("what if I lose the passphrase?") | Turn it into trust: explicit no-recovery UX, export/backup prompts, clear documentation |
| Single-file file grows huge with attachments | Size meter + `documents/` folder on generator side (roadmap) — plan before attachments ship |

---

## 10. Immediate next steps (no code)

1. Write the 3 lead-magnet checklists using the current tool output as the template.
2. Record the 90-second demo video (screenshots already exist in `tests/screenshots/`).
3. Draft the Reddit launch post + landing page copy (feature-first, screenshots, zh).
4. Set up the Free/Plus build pipeline (generator `--tier` + license/watermark; see `versioning_plan.md` §4) and the landing-page download flow.
5. List 20 Ontario estate lawyers + 20 fee-only planners as pilot prospects; draft outreach email.
6. Prepare the Mandarin landing page copy for the zh build.
7. Open a pricing feedback thread with the first 50 free users.
