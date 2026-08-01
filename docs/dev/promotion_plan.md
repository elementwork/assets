# Promotion & Sales Plan: Asset Inventory Generator

> **Status:** Living document · Last updated 2026-07-31 23:08:58
> **Product:** Self-contained, offline-first asset inventory for Canadian families in Ontario
> (Markdown + Excel + single-file HTML dashboard, en/zh, AES-256-GCM credential vault)
> **Companion docs:** `feature_list.md` (what to sell), `future_plan.md` (what's next)

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
> with a built-in encrypted vault, audit, and estate-readiness view, without any cloud
> dependency.

**Brand pillars:** Private by design · Ontario-smart · Zero-dependency · Family-ready.

---

## 2. Target audience (segmented)

| Segment | Who | Pain | Angle | Willingness to pay |
|---------|-----|------|-------|--------------------|
| **S1 — Estate planning lawyers & paralegals** | Ontario estates/elder-law firms | Clients arrive with no inventory; discovery is weeks of back-and-forth | Client-engagement tool: send the file, client fills it, advisor gets a clean binder | High (B2B seat/white-label) |
| **S2 — Financial advisors & planners** | Fee-for-service planners, insurance brokers | No standardized inventory; compliance wants documented client facts | "Redacted Advisor Profile" export, readiness score, annual review generator | High (B2B) |
| **S3 — DIY families (40–70)** | Ontario homeowners with TFSAs/RRSPs/RESPs, aging parents | Wants a binder but won't pay $2–5k for a lawyer consultation just to organize | $19–39 one-time or $5/mo; giftable to aging parents | Medium |
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
  AES-256-GCM encrypted credentials, no-passphrase = no recovery (clear trade-off UX).
- **The outputs:** Markdown reference, 8-sheet Excel, print-ready estate binder, CSV/JSON exports.
- **The intelligence (roadmap):** EAT/probate exposure, death-tax estimate, estate readiness
  score, audit flags, executor/POA modes.

**Value props to lead with in copy:**
1. *One file. No account. No cloud.*
2. *Your executor doesn't need a subscription to read your estate plan.*
3. *Ontario rules built in — probate, TFSA/RRSP/RESP/FHSA, T1135, land transfer tax.*
4. *Encrypted credentials that even the file's author can't recover without the passphrase.*
5. *Chinese and English in the same product.*

---

## 4. Product-marketing artifacts to build (before launch)

| Artifact | Purpose | Notes |
|----------|---------|-------|
| Demo file with `--demo` fixture | Screenshot tours, press, first-run | Realistic Ontario family (2 adults, 2 kids, house+mortgage, TFSAs/RRSPs/RESP, dormant crypto) |
| 90-second explainer video | Landing page hero | Screen-capture: open file → fill → vault → audit → print binder |
| 6 screenshot set | Every layout + audit + charts + zh | Light/dark, mobile viewport |
| Live interactive demo (hosted copy of the dashboard) | Try-before-download | Static hosting only; no backend, no PII |
| One-page "What executors need" PDF | Lead magnet for S4 | Generated by the tool itself — dogfooding |
| "Ontario Estate Checklist" PDF | Lead magnet | 20-point checklist; CTA to the tool |
| Compare page: vs spreadsheets, vs Notion, vs cloud net-worth apps, vs lawyer binder | Conversion | Honest table — offline/self-contained/encrypted/Ontario are our columns |

---

## 5. Pricing & packaging

| Tier | Price | Contents |
|------|-------|----------|
| **Free** | $0 | Generator (open source CLI), en/zh outputs, all core dashboard features, community support |
| **Family** | $39 one-time (or $5/mo) | Everything free + credential vault + audit + print binder + future Ontario intelligence (EAT, readiness score) + email support |
| **Advisor** | $149/yr per advisor (or $299/yr white-label) | Family tier for N clients + redacted client profiles + bulk client generation + CSV import + priority support + logo/white-label option |
| **Estate-pro** | $499/yr | Advisor + API/CLI automation, handoff packs, multi-user practice dashboard, SLA |

**Principles:**
- CLI/generator stays free and open — it is the marketing engine (devs/advisors find it on GitHub).
- Monetize the *dashboard intelligence* (vault, audit, Ontario calculators), not the file format.
- One-time Family price because the artifact is a file, not a service — recurring value must
  come from new intelligence modules and updates (roadmap items).
- Advisors are the revenue floor (B2B); families are the volume.

---

## 6. Channels & campaigns

### 6.1 Organic (primary, zero budget)
- **GitHub** — open-source the generator; README demo GIF; good first-issue labels;
  topics: `estate-planning`, `canada`, `tax`, `finance`, `self-hosted`.
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
| 1–2 | Ship `--demo` fixture; record video; write 3 lead magnets; set up landing page + download |
| 3 | GitHub launch + Show HN + Reddit launch post (timed weekday, EST) |
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
| Downloads / generator stars | 2,000 downloads, 300 GitHub stars | 25,000 downloads, 2,500 stars |
| Advisor pilots → paying | 10 pilots, 3 paying | 150 paying advisors |
| Family conversions (free→paid) | 5% | 8–10% |
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
| "It's just a spreadsheet" perception | Lead with estate-readiness/audit/vault/print binder; comparison page vs spreadsheets |
| Legal liability (giving tax/legal advice) | Clear disclaimers: "educational estimates, not advice"; position as organizer, calculators labeled estimates |
| Open-source → nobody pays | Keep intelligence (vault/audit/Ontario modules) in paid tiers; free is the marketing engine |
| Chinese market regulatory/content concerns | No financial advice claims; zh marketing stays descriptive of features, not guarantees |
| Advisor adoption is slow | Free pilots, white-label, "intake template" give-away; win one firm, clone the playbook |
| Data-loss fear ("what if I lose the passphrase?") | Turn it into trust: explicit no-recovery UX, export/backup prompts, clear documentation |
| Single-file file grows huge with attachments | Size meter + `documents/` folder on generator side (roadmap) — plan before attachments ship |

---

## 10. Immediate next steps (no code)

1. Write the 3 lead-magnet checklists using the current tool output as the template.
2. Record the 90-second demo video (screenshots already exist in `tests/screenshots/`).
3. Draft the Reddit launch post + GitHub README rewrite (feature-first, screenshots, zh).
4. List 20 Ontario estate lawyers + 20 fee-only planners as pilot prospects; draft outreach email.
5. Prepare the Mandarin landing page copy for the zh build.
6. Open a pricing feedback thread with the first 50 free users.
