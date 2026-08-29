# EstateON Product Strategy & North Star

> **Status:** Canonical product-strategy document · Living document
> **Last updated:** 2026-08-19
> **Scope:** Product philosophy, positioning, target users, packaging, working pricing, growth model, UX principles, trust model, roadmap guardrails, and feature-decision framework.
> **Product:** EstateON — private, offline-first family asset inventory and estate continuity system.
>
> **Strategic precedence:** When this document conflicts with older tactical documents on product positioning, user-facing edition names, packaging philosophy, or working pricing, this document is the strategic source of truth until the tactical document is explicitly refreshed.
>
> Companion documents:
> - `feature_list.md` — what exists now.
> - `future_plan.md` — implementation roadmap / future capability backlog.
> - `versioning_plan.md` — build-time tier implementation and delivery mechanics.
> - `promotion_plan.md` — channel, campaign, launch, and sales tactics.
> - `ASSET_FIELDS.md` — field/schema reference.
> - `ASSET_SAMPLE_LIST.md` — catalog/taxonomy reference.

---

## 1. Executive product thesis

EstateON is **not primarily a net-worth tracker, budgeting app, password manager, document vault, or will-writing product**.

EstateON is a **family asset inventory and estate continuity system** designed to answer four questions reliably:

1. **What exists?**
2. **Where is it?**
3. **How can the right person find or access the next step?**
4. **What must happen if the owner is incapacitated or dies?**

The product exists because financial and estate information is usually fragmented across bank apps, investment portals, email, filing cabinets, insurance policies, corporate records, property documents, password managers, family memory, and devices. A will may explain who receives property, but it does not guarantee that an executor, spouse, child, or attorney for property can discover everything efficiently.

EstateON therefore focuses on the chain:

> **Asset exists → asset is documented → asset is discoverable → access path is understood → handoff is prepared → family/executor can act.**

The durable product idea is **continuity**, not merely inventory.

### One-line positioning

> **EstateON is a private, offline family asset inventory and estate continuity system that helps people document what they own, where it is, and how their family can find and handle it when it matters.**

Chinese positioning:

> **EstateON 是一套离线、私密的家庭财产清单与遗产交接系统，帮助你把“有什么、在哪里、怎么找、谁来处理”一次整理清楚，让家人在真正需要的时候接得上。**

### Emotional promise

The product should create **clarity, preparedness, and relief** rather than fear.

Preferred emotional territory:

- organized for life;
- ready for family;
- private by design;
- practical in an emergency;
- understandable to non-experts.

Avoid building the brand around death anxiety, legal intimidation, wealth-showing, or fintech novelty.

---

## 2. The problem EstateON is solving

### 2.1 The fragmentation problem

A typical established household may have:

- multiple bank accounts;
- TFSA/RRSP/RRIF/FHSA/RESP and non-registered investments;
- pensions;
- multiple life, disability, critical illness, health, home and auto policies;
- one or more homes, rentals, recreational properties or foreign real estate;
- mortgages and private debts;
- corporations, partnerships or professional corporations;
- shareholder loans and business interests;
- safe-deposit boxes;
- jewelry, collectibles and valuable personal property;
- crypto wallets and exchanges;
- domain names, online businesses and digital accounts;
- intellectual property;
- foreign assets;
- important documents stored across physical and digital locations.

The problem is rarely that no record exists anywhere. The problem is that **no one has the map**.

### 2.2 The continuity problem

The system must work through three states:

| State | Primary user need |
|---|---|
| Normal life | Maintain an understandable inventory and know what needs attention. |
| Incapacity | POA/spouse/family can identify institutions, documents, contacts and authorized access routes. |
| Death | Executor/family can discover assets, locate records, contact institutions/advisors and execute the estate plan. |

A feature that improves ordinary organization but becomes useless during incapacity or death is lower strategic value than a feature that improves continuity.

### 2.3 The estate-plan discovery gap

Traditional estate planning answers important legal questions, but often leaves an operational gap:

- A will may say who inherits an asset, but not where the account is.
- A POA may grant authority, but the attorney may not know which institutions exist.
- A beneficiary designation may be valid, but the family may not know the policy exists.
- A crypto estate plan may name a beneficiary, but recovery instructions may be unusable.
- A family may know there is a corporation, but not where minute books, shareholder records, accountant details, banking or insurance are kept.

EstateON is intended to be the **operational index beneath the estate plan**.

---

## 3. Product category and competitive frame

EstateON should be positioned as:

> **Family Asset Inventory + Estate Continuity Binder**

not simply “asset tracker.”

### 3.1 What adjacent tools do

| Category | Primary job | EstateON distinction |
|---|---|---|
| Spreadsheet | Flexible manual record | EstateON provides a purpose-built asset taxonomy, structured handoff fields, views, audit/readiness and binder output. |
| Budget/net-worth app | Daily financial tracking | EstateON optimizes for discovery and continuity, not transaction syncing or spending analysis. |
| Password manager | Credential storage | EstateON is primarily an access-path map and continuity index, not a vault for every transactional secret. |
| Will | Legal distribution | A will answers legal disposition; EstateON helps survivors discover and operationalize the estate. |
| Document vault | Store files | EstateON tells users what exists and where source documents are kept. |
| Static estate binder/PDF | Paper checklist | EstateON is editable, searchable, structured, auditable and re-printable. |
| Advisor CRM | Manage client relationships | EstateON is family-owned continuity infrastructure; advisor workflows may be layered on later. |

### 3.2 Strategic category language

Preferred terms:

- Family Asset Inventory
- Estate Continuity
- Estate Binder
- Emergency Access Guide
- Master Asset Index
- Access Readiness
- Annual Review
- Executor / POA preparedness

Use “net worth” only when needed as a secondary analytic output, not as the core product category.

---

## 4. Product principles

These principles are durable constraints for product decisions.

### 4.1 Offline first

The core deliverable should continue to work without EstateON servers, subscriptions, cloud authentication, or an internet connection.

The long-term promise is stronger than “we support offline mode.” It is:

> **The family owns a durable artifact that remains readable and usable independently of EstateON.**

### 4.2 File ownership

The user owns the file.

The file can be:

- stored on a computer;
- duplicated to encrypted USB media;
- placed in secure cloud storage chosen by the user;
- backed up to NAS;
- delivered to an executor/advisor where appropriate;
- printed as an estate binder.

EstateON should not create artificial captivity around access to the user’s own data.

### 4.3 File = application + database

The self-contained HTML model is a strategic differentiator, not an incidental technical implementation.

Benefits:

- understandable mental model;
- no server dependency;
- portable;
- easy archival;
- easy backup;
- family-readable;
- supports a “buy once, keep forever” promise.

Future architecture may add companion services, but the core artifact should remain usable independently.

### 4.4 Comprehensive inventory

A broad catalog has product value beyond convenience.

The catalog communicates:

> **“We already thought about assets you may have forgotten.”**

Therefore the catalog should be maintained as a curated taxonomy, not treated as filler rows.

### 4.5 Locator, not indiscriminate secret vault

The inventory should contain enough information to enable authorized discovery and continuity, while avoiding casual concentration of high-risk transactional secrets.

Generally appropriate:

- institution;
- branch/contact;
- account/policy reference;
- document location;
- password-manager location;
- access-location description;
- recovery contact;
- advisor contact;
- incapacity/death access state;
- handoff instructions.

Generally not encouraged as default inventory content:

- debit card PIN;
- CVV;
- full transaction credentials;
- crypto seed phrase/private key;
- secrets whose presence turns the inventory into a single catastrophic compromise point.

For crypto and similar assets, EstateON should identify the **exact recovery path/location**, while the seed/private key remains separately protected.

### 4.6 Print is a first-class continuity output

Print is not merely “export to paper.”

The binder should be designed for a stressed family member, POA or executor who may not understand the original owner’s systems.

Critical print outputs include:

1. Emergency Access Guide
2. Master Asset Index
3. cover / identity / date / inventory ID
4. category sections
5. beneficiary and insurance summaries where appropriate

### 4.7 Bilingual is a product capability

English/Chinese support is not a cosmetic translation layer.

For Chinese-Canadian families, the product may be used across generations with different language preferences. Important professional terms can remain bilingual where that improves clarity, for example:

- Audit 财产审计
- Annual Review 年度复核
- Access Readiness 交接准备度

### 4.8 Progressive sophistication

Free should feel useful and understandable.

Family should feel like a meaningful transformation from “inventory” into “family-ready binder.”

Professional should introduce deeper professional terminology and continuity intelligence.

Do not make every tier look like the same UI with arbitrary buttons disabled.

---

## 5. Explicit non-goals

These non-goals prevent strategic drift.

EstateON is not currently trying to become:

- a bank-aggregation platform;
- a real-time trading portfolio tracker;
- a budgeting application;
- a full accounting system;
- a tax-filing application;
- a legal-document drafting substitute for a lawyer;
- a universal password manager;
- a cloud document-management platform;
- a CRM-first advisor SaaS;
- a social network;
- an AI system that autonomously moves money or changes beneficiary designations.

A future feature can touch these domains only when it directly strengthens estate inventory, continuity, preparedness, review, or professional workflow.

---

## 6. Core user segments and Jobs-to-be-Done

### 6.1 Established household / aging household

Typical profile:

- age roughly 45–75;
- homeowner;
- multiple financial institutions;
- registered and non-registered investments;
- insurance;
- adult children;
- possibly business/foreign/digital assets.

Job:

> “Help me organize everything so I understand it now and my family can find it later.”

### 6.2 Adult child organizing parents

This is a particularly strong buyer and referral use case.

Job:

> “Help me sit down with my parents and document what exists without forcing them into a complex cloud app.”

Potential messaging:

> **Help your parents leave a map, not a mystery.**

Chinese:

> **帮父母把财产整理成一份以后家人找得到的清单。**

### 6.3 Executor / POA preparedness

Job:

> “If I have to step in unexpectedly, show me what exists, who to contact, where documents are, and what the authorized next step is.”

### 6.4 Complex / HNW household

Typical complexity:

- several properties;
- corporate holdings;
- professional corporation;
- trusts;
- cross-border or foreign assets;
- multiple policies;
- crypto/digital assets;
- collectibles/IP/business interests.

Job:

> “Help me identify gaps and test whether my estate is actually operationally ready, not merely documented.”

### 6.5 Professional intermediary

Examples:

- estate lawyer;
- life insurance advisor;
- financial planner;
- accountant;
- estate administrator;
- family office.

Job:

> “Give clients a structured preparation artifact that improves discovery and makes planning/review conversations more complete.”

This is a future B2B2C distribution layer, not necessarily the first architecture of the product.

---

## 7. Product lifecycle: Discover → Organize → Prepare → Maintain → Handoff

This should become the core product model.

### Stage 1 — Discover

The user learns the breadth of what should be considered.

Value mechanisms:

- broad asset catalog;
- categories/subcategories;
- search;
- guided quick add;
- examples;
- locked preview of deeper capabilities.

### Stage 2 — Organize

The user converts the catalog into their household’s usable inventory.

Value mechanisms:

- edit/detail/table/timeline views;
- owner/institution/category structure;
- current value;
- document paths;
- contacts;
- status;
- local save/direct save.

### Stage 3 — Prepare

The user makes the inventory continuity-ready.

Value mechanisms:

- access location;
- recovery contact;
- incapacity access;
- death access;
- handoff instructions;
- Emergency Access Guide;
- Master Asset Index;
- Access Readiness;
- Audit.

### Stage 4 — Maintain

The inventory remains current.

Value mechanisms:

- review date;
- last access test;
- next access review;
- Annual Review;
- stale-data flags;
- “what changed since last review” in future versions.

### Stage 5 — Handoff

The file and binder become actionable for another authorized person.

Value mechanisms:

- clearly structured print output;
- executor/POA-oriented navigation;
- masked sensitive references;
- contact and document maps;
- future crisis/executor modes.

This model is more important than any individual layout.

---

## 8. Edition strategy

Canonical user-facing editions:

1. **Free / 免费版**
2. **Family / 家庭版**
3. **Professional / 专业版**

Internal implementation may continue to use `planning` for Professional compatibility.

### 8.1 Free — Discover your estate

Strategic job:

- acquisition;
- trust;
- demonstrate catalog breadth;
- make the user recognize missing/forgotten asset categories;
- begin real inventory work.

Free should be genuinely useful. It should not feel like a broken demo.

The upgrade strategy should be **visible capability depth**, not aggressive interruption.

Desired user reaction:

> “I didn’t realize there were this many things I should organize — and this already feels useful.”

Free can show static locked previews of Family and Professional capabilities, while higher-tier implementation code remains build-time stripped.

### 8.2 Family — Organize it for your family

Family should be the likely consumer volume product.

Its value is not “more layouts.”

Its core transformation is:

> **Inventory → usable family estate binder.**

Strong Family value anchors:

- expanded catalog;
- Table / Timeline / Charts where useful;
- Print Estate Binder;
- Emergency Access Guide;
- Master Asset Index;
- broader appearance/templates;
- continuity-oriented fields/workflows.

Family should feel complete enough that a typical household does not need Professional.

### 8.3 Professional — Make it continuity-ready

Professional should not merely be “Family with more categories.”

Its durable value is intelligence and review:

- comprehensive catalog;
- Audit;
- Access Readiness;
- Annual Review;
- professional exports;
- deeper estate-continuity analysis;
- future scenario / executor / advisor capabilities.

Desired user reaction:

> “This is telling me what is still operationally weak, not just what I own.”

The long-term Professional moat should become a **continuity rules engine**.

---

## 9. Working pricing strategy

> **Important:** The prices below are a recommended working baseline for product design and testing, not an irreversible legal/commercial commitment. Pricing should be validated with real conversion data. Any public launch pricing must be deliberately confirmed before launch.

### 9.1 Recommended consumer baseline

| Edition | Working price | Commercial role |
|---|---:|---|
| Free | **CAD $0** | Acquisition / trust / discovery |
| Family | **CAD $29 one-time** | Primary household conversion product |
| Professional | **CAD $99 one-time** | Complex household / advanced planning product |
| Optional Updates | **CAD $19/year** | Updated taxonomy, policy figures, templates, rules and new version access; not required to keep the purchased file working |

### 9.2 Why one-time pricing fits the product

The product promise is:

> **Buy once. Keep your file. Your family can still open it later.**

A mandatory recurring subscription would undermine the offline/private/ownership story.

Therefore:

- purchased artifacts should remain usable indefinitely;
- expiration should not make the customer’s family file unusable;
- recurring revenue should come from optional updates, professional services, advisor tooling, or other ongoing value—not hostage access to the user’s own estate inventory.

### 9.3 Why Family should be inexpensive

Family is expected to be a low-friction upgrade after the user has already invested effort.

The strongest conversion moment is likely:

> **“I have organized this; now I want a proper binder for my spouse/children/executor.”**

Therefore the Family paywall should focus on the **result** (family-ready continuity output), not arbitrary caps such as “only 20 assets.”

### 9.4 Why Professional can command more

Professional should earn the price by answering questions such as:

- Which important assets have weak handoff readiness?
- Which accounts lack recovery contacts?
- Which assets are blocked for incapacity/death access?
- Which data has not been reviewed recently?
- Which policies/registered accounts have beneficiary gaps?
- Which critical assets are under-documented?

This is decision-support value rather than mere storage.

### 9.5 Pricing experiments worth testing

Do not change packaging based on intuition alone. Test:

- Family CAD $29 vs $39;
- Professional CAD $79 vs $99 vs $129;
- launch discount vs permanent lower list price;
- family bundle/gift purchase;
- free Family upgrade with advisor referral sponsorship;
- Professional + 1 year Updates bundle;
- household license vs individual license language.

Measure conversion, refund rate, activation, review completion and willingness to recommend—not revenue alone.

---

## 10. Product-led growth model

The ideal funnel is:

> **Content / referral → Free download → user starts inventory → user realizes breadth/gaps → Family binder conversion → Professional readiness conversion where complexity exists.**

### 10.1 Free as the marketing engine

Free should communicate product depth naturally through use.

Good upgrade mechanisms:

- “256 asset types covered” or current actual catalog count;
- visible but tasteful locked Family capability previews;
- visible Professional readiness/audit preview;
- clear “what Family adds” comparison;
- contextual upgrade at the moment the user wants Print Estate Binder;
- contextual upgrade when the user wants advanced audit/readiness.

Avoid:

- repeated modal nags;
- fake urgency;
- artificially blocking ordinary data entry;
- excessive upgrade banners;
- hiding the product’s real usefulness until payment.

### 10.2 The catalog as acquisition psychology

A large catalog has two marketing functions:

1. **Completeness signal** — EstateON appears more comprehensive than a blank spreadsheet.
2. **Discovery trigger** — users remember forgotten asset classes.

The UI should distinguish **catalog coverage** from **assets actually owned** so users are not misled.

Preferred metric language:

- Asset Catalog: 517 covered
- Showing: 8
- With Value: 23

rather than implying the user owns 517 assets.

---

## 11. Promotion and go-to-market

### 11.1 Core acquisition message

The strongest general question is:

> **If you couldn’t explain your finances tomorrow, would your family know what exists and where to start?**

Chinese:

> **如果明天你无法亲自说明，家人知道你有哪些财产、在哪里、该找谁吗？**

This problem is understandable without explaining software features first.

### 11.2 Lead magnet

Primary CTA:

> **Download the Free Family Asset Inventory**

Chinese:

> **免费领取家庭财产清单**

Trust copy:

- No account required.
- No bank connection.
- No cloud dependency.
- Your file stays with you.

### 11.3 Content pillars

Build content around user problems rather than product features.

#### Pillar A — Executor preparedness

Examples:

- What does your executor need to know?
- What documents should an executor be able to find?
- What happens when the family cannot identify all accounts?

#### Pillar B — Aging parents

Examples:

- How to organize your parents’ financial information respectfully.
- A checklist for adult children helping aging parents.
- How to prepare before a hospitalization or cognitive decline.

#### Pillar C — Ontario/Canadian estate organization

Examples:

- What assets may bypass the estate and why the executor still needs a record.
- Beneficiary-designated assets vs estate assets.
- TFSA/RRSP/RRIF/FHSA/RESP information an estate inventory should include.

Content must clearly separate organization/education from legal or tax advice.

#### Pillar D — Digital and crypto continuity

Examples:

- Why putting a seed phrase in a general spreadsheet is dangerous.
- How to document a crypto recovery path without exposing the key.
- Digital accounts your family may need to find.

#### Pillar E — Privacy/offline ownership

Examples:

- Why an estate inventory should survive a vendor shutdown.
- Cloud vault vs offline family asset index.
- How to store and back up an estate inventory safely.

#### Pillar F — Chinese-Canadian families

Examples:

- 加拿大华人家庭财产清单怎么整理？
- 父母的加拿大和海外资产，子女应该知道哪些信息？
- 怎样给家人留一份“找得到”的财产地图？

### 11.4 Channel priorities

Potential channels:

- SEO / educational blog;
- YouTube walkthroughs;
- Reddit where self-promotion rules permit;
- Chinese-language WeChat / RED / community media;
- advisor/lawyer/accountant referrals;
- workshops/webinars on family financial organization;
- downloadable executor/aging-parent checklists;
- comparison pages vs spreadsheet, cloud apps and static binders.

Paid acquisition should follow evidence of organic conversion rather than precede product-market fit.

---

## 12. B2B2C and professional distribution

Professional distribution can become a major growth engine without turning the core household artifact into a CRM.

Potential professional use cases:

### Estate lawyers

- pre-meeting client inventory;
- estate-plan discovery checklist;
- executor-preparedness artifact;
- branded client binder.

### Life insurance advisors / financial planners

- needs-analysis preparation;
- beneficiary and policy discovery;
- annual client review;
- continuity gap conversation;
- family handoff planning.

### Accountants

- corporate/foreign asset organization;
- tax-document locator;
- estate administration preparation.

### Family office / HNW

- complex ownership map;
- private continuity review;
- multi-entity handoff.

### B2B2C strategic rule

The professional should help the client create and maintain the artifact, but **the family should retain ownership and long-term readability of the file**.

Future advisor software should therefore be layered around EstateON rather than replacing the offline artifact.

---

## 13. Messaging architecture

### Master message

> **One private file that tells your family what exists, where it is, and where to start.**

### Supporting messages

**Privacy**
> No account. No forced cloud. Your file stays with you.

**Continuity**
> A will says who receives assets. EstateON helps your family find them.

**Completeness**
> A structured catalog helps you remember assets a blank spreadsheet does not.

**Family readiness**
> Turn your inventory into an Emergency Access Guide and Estate Binder.

**Professional readiness**
> Audit gaps, measure access readiness, and review the estate regularly.

### Brand tone

Prefer:

- calm;
- precise;
- trustworthy;
- practical;
- family-oriented;
- non-judgmental;
- professional without unnecessary jargon.

Avoid:

- “death panic” marketing;
- exaggerated guarantees;
- “AI will solve your estate” claims;
- implying legal/tax advice where the product is only organizing information;
- shaming users for incomplete planning.

---

## 14. UX and information-architecture principles

### 14.1 Action hierarchy

Primary high-frequency actions should remain obvious:

- Search
- Add Asset
- Save
- Print where the tier supports it

Low-frequency actions belong in Features or contextual menus.

### 14.2 Workspace hierarchy

The UI should distinguish:

- **actions** — save/add/print;
- **workspace modes** — dashboard/table/charts/audit/review;
- **secondary utilities** — import/export/theme/security/help.

Do not collapse these concepts into a single toolbar with 15 icons.

### 14.3 Mobile principle

Mobile is likely to be used during family conversations, walkthroughs, or quick reviews.

Prioritize:

- large touch targets;
- readable labels;
- clear Save state;
- horizontal workspace navigation when needed;
- avoid multiple competing sticky bars;
- Features as a sheet/menu with an explicit close action.

### 14.4 Elder-friendly principle

Because many users may be older adults:

- avoid unexplained icon-only controls;
- use plain language;
- maintain adequate type size and contrast;
- avoid hidden gestures;
- show save state clearly;
- provide forgiving navigation;
- avoid requiring account creation for basic use.

### 14.5 Professional terminology

Professional can retain terms such as:

- Audit
- Access Readiness
- Annual Review
- Export Markdown / Excel / JSON

Chinese Professional may intentionally use bilingual terminology to preserve professional meaning.

---

## 15. Trust, privacy and security model

Trust is part of the product, not a settings page.

### 15.1 Trust promises

EstateON should be able to explain plainly:

- where data lives;
- what leaves the device;
- whether a server is involved;
- how a file is locked;
- what happens if a passphrase is lost;
- what is and is not appropriate to store inside the inventory;
- how to maintain backups.

### 15.2 Backup philosophy

A continuity file that exists in only one place is itself a continuity risk.

Future UX should encourage a sensible backup pattern, for example:

- working copy;
- protected backup;
- executor/family access arrangement where appropriate.

The app should educate without assuming one universal storage strategy.

### 15.3 Encryption philosophy

Whole-file encryption can be useful but increases recovery risk.

The UX should clearly explain the trade-off:

> Strong privacy can also make the estate inaccessible if the family cannot recover the passphrase.

Future improvements may include stronger key derivation, recovery-design guidance, key-file options, or split-secret workflows, but complexity must be justified by real users.

### 15.4 License security is separate from data security

Commercial license enforcement and protection of user data are different security domains.

The current pre-existing HMAC license approach embeds client-side verification material and should not be treated as tamper-resistant commercial licensing. Before relying on the license boundary commercially, move toward asymmetric signing (for example Ed25519) where build infrastructure holds the private signing key and distributed files contain only a public verification key.

This change should not weaken the user’s permanent ability to read their purchased file.

---

## 16. Continuity intelligence: the long-term Professional moat

Professional’s strategic destination is a rules/assessment layer that can identify operational weaknesses.

Potential dimensions:

### Identity completeness

- asset has meaningful name/category;
- owner is known;
- institution/location is known;
- reference number is available where appropriate.

### Access discoverability

- access location documented;
- document path known;
- recovery contact known;
- advisor/support contact available.

### Incapacity readiness

- authorized party identified;
- POA path understood;
- institution requirements noted;
- physical/digital documents discoverable.

### Death readiness

- executor can identify asset;
- beneficiary/estate path understood;
- policy/account contact route known;
- instructions are available without embedding unsafe secrets.

### Currency of information

- last reviewed;
- last access test;
- next review date;
- stale-value warning;
- missing confirmation.

### Materiality

Not every catalog row should receive the same urgency.

Future rules should distinguish:

- critical assets;
- meaningful owned assets;
- template/catalog rows;
- dormant/closed assets;
- informational/non-financial items.

The goal is to produce **actionable priorities**, not a wall of warnings.

---

## 17. Future product expansion framework

Expansion should follow the continuity lifecycle rather than feature novelty.

### Horizon A — deepen the current core

Examples:

- explicit “owned / confirmed / not owned / needs review” state;
- better material-asset filtering;
- improved Master Asset Index based on actual/material assets;
- richer Annual Review workflow;
- review completion metadata;
- access-tested/verified state;
- backup guidance;
- better first-run onboarding;
- household profile;
- executor/POA identity and contact section;
- better print hierarchy;
- stronger security architecture.

### Horizon B — family continuity workflows

Examples:

- guided aging-parent setup;
- “family meeting” workflow;
- emergency mode;
- executor mode;
- incapacity mode;
- household roles;
- review checklist;
- change log / what changed since last review;
- archive historical versions;
- secure handoff checklist;
- QR/pointer cards to the protected inventory location.

### Horizon C — professional intelligence

Examples:

- continuity risk scoring;
- beneficiary/designation review;
- stale/duplicate asset detection;
- corporate ownership relationships;
- estate-readiness report;
- advisor review notes;
- scenario views;
- redacted professional export;
- white-label binder;
- client preparation workflow.

### Horizon D — optional companion services

Possible—but only if they do not compromise the core offline promise:

- update delivery;
- signed taxonomy/rules packages;
- optional encrypted sync chosen by the user;
- family notification/reminder service;
- advisor portal that generates or reviews client-owned artifacts;
- secure backup verification.

The offline artifact should remain independently usable.

### Horizon E — AI assistance

AI may eventually help with:

- guided classification;
- “what might I be missing?” interviews;
- explanation of fields;
- summarization for family/executor;
- anomaly detection;
- review prioritization;
- document-to-inventory extraction where privacy permits.

AI should **not** become a requirement for opening or understanding the core inventory.

---

## 18. Feature-decision framework

Before implementing a substantial feature, score it against these questions.

### 18.1 Strategic-fit test

1. Does it improve **Discover, Organize, Prepare, Maintain, or Handoff**?
2. Does it improve family/executor/POA usability?
3. Does it strengthen offline ownership or unnecessarily create server dependence?
4. Does it make the product easier for normal families or only more impressive in a demo?
5. Does it create a natural Free → Family → Professional value progression?
6. Does it increase data risk or encourage storing dangerous secrets?
7. Is it understandable in both English and Chinese?
8. Does it print/handoff well where relevant?
9. Can the user still understand their data years later?
10. Does it create legal/tax advice liability that should instead be framed as organization/education?

### 18.2 Simple prioritization score

Score 0–3 on each:

| Dimension | 0 | 3 |
|---|---|---|
| Continuity value | cosmetic | materially improves incapacity/death handoff |
| Household usefulness | niche | useful to broad target users |
| Trust/privacy fit | weakens | strongly reinforces |
| Differentiation | commodity | distinctive EstateON capability |
| Tier economics | no value ladder | clear paid-value contribution |
| Complexity | high risk/cost | low implementation/support burden |
| Maintainability | brittle | durable/simple |

High total score = strong roadmap candidate.

Do not prioritize features solely because competitors have them.

---

## 19. Metrics and product health

### 19.1 North-star metric

Recommended conceptual north star:

> **Number of households with a materially complete inventory reviewed within the last 12 months.**

This measures continuity, not downloads.

### 19.2 Funnel metrics

Track where technically and ethically possible:

- Free downloads;
- file opened/activated (if measurable without violating privacy);
- assets confirmed/owned;
- Family conversion;
- Print Estate Binder usage;
- Professional conversion;
- Annual Review completion;
- percentage of material assets with adequate access readiness;
- 12-month review rate;
- referral/share intent;
- refund rate;
- support burden.

Because the product is offline-first, do not add invasive telemetry merely to satisfy SaaS-style analytics. Use voluntary, privacy-respecting measurement and public-site funnel data where possible.

### 19.3 Better success question

The ultimate product question is:

> **If a household emergency occurred today, would this EstateON file materially reduce confusion and discovery time?**

---

## 20. Product moat

EstateON’s moat should become the combination of several elements, not any single feature.

### 20.1 Curated asset taxonomy

A comprehensive Canada/Ontario-aware taxonomy that reflects real household complexity.

### 20.2 Continuity-oriented schema

Fields designed around discovery, documents, recovery contacts, incapacity, death and handoff—not just financial value.

### 20.3 Self-contained artifact architecture

A durable offline file is meaningfully different from a cloud dashboard.

### 20.4 Family-ready print output

A binder designed for continuity and crisis use.

### 20.5 Continuity rules engine

The eventual ability to identify actionable gaps in preparedness.

### 20.6 Bilingual Canadian specialization

Strong English/Chinese support plus Canadian/Ontario relevance can create a defensible niche before broader geographic expansion.

### 20.7 Professional distribution

Lawyers, advisors and accountants can become trusted distribution channels if the tool saves preparation time and improves client completeness.

---

## 21. Geographic strategy

### 21.1 Initial depth: Ontario / Canada

Depth is preferable to superficial global coverage.

Canadian concepts may include, as appropriate and carefully framed:

- TFSA;
- RRSP/RRIF;
- FHSA;
- RESP/RDSP;
- registered pensions;
- corporate interests;
- beneficiary designations;
- probate/estate administration terminology;
- Canadian insurance structures;
- foreign-property organization.

### 21.2 Expansion pattern

Do not simply replace currency symbols and call it international.

A geographic edition should evaluate:

- account types;
- estate terminology;
- beneficiary structures;
- tax/document fields;
- local professional expectations;
- language;
- legal disclaimers;
- print outputs.

Potential future expansion could proceed province-by-province or country-by-country only after the Canadian core is strong.

---

## 22. Legal/compliance positioning guardrails

EstateON is primarily an organizer and continuity-preparation tool.

When adding rules/calculators/flags:

- distinguish facts entered by the user from estimates;
- identify assumptions;
- timestamp rules/figures where relevant;
- avoid guaranteeing tax/legal outcomes;
- include appropriate educational disclaimers;
- encourage professional advice when an issue depends on legal/tax facts.

Preferred framing:

> “Potential review item”

rather than:

> “Your estate plan is legally wrong.”

Professional intelligence should prioritize questions and gaps, not impersonate legal counsel.

---

## 23. Packaging rules for future features

### Free feature rule

Put a feature in Free when it:

- builds trust;
- improves activation;
- demonstrates breadth;
- helps a real household begin useful work;
- increases awareness of a paid outcome without giving away the full paid transformation.

### Family feature rule

Put a feature in Family when it primarily helps a household:

- organize more completely;
- communicate with spouse/children;
- print/share a family-ready binder;
- maintain continuity information.

### Professional feature rule

Put a feature in Professional when it primarily provides:

- audit/intelligence;
- complexity handling;
- advanced review;
- professional export;
- scenario analysis;
- estate-readiness prioritization;
- professional workflow value.

### Anti-pattern

Do not move an ordinary usability feature into Professional merely to manufacture differentiation.

Professional should be better because it is **smarter and deeper**, not because Family was intentionally made inconvenient.

---

## 24. Conversion moments by edition

### Free → Family

Natural triggers:

- “I want to print this for my family.”
- “I want Table/Timeline/Charts to organize a larger household.”
- “I want the Emergency Access Guide.”
- “I want the Master Asset Index.”

### Family → Professional

Natural triggers:

- “How complete is this?”
- “What am I missing?”
- “Which access paths are weak?”
- “What should I review this year?”
- “I have companies/foreign assets/complex ownership.”
- “I need professional exports or deeper audit.”

The upgrade UI should appear at these moments rather than interrupting unrelated workflows.

---

## 25. Gift and family-network opportunity

EstateON has unusual gift potential because the buyer and user may differ.

Possible offers:

- Buy Family for Parents;
- Couple/household license;
- Parents + adult child setup kit;
- annual “family estate review” checklist;
- advisor-sponsored client copy.

The positioning should avoid sounding like a morbid gift. Frame it as organization and care:

> **A practical way to help your family stay organized.**

---

## 26. Recommended future onboarding

A blank catalog can be overwhelming. Future onboarding should preserve breadth while reducing cognitive load.

Potential flow:

1. Household basics
2. Home/real estate
3. Bank accounts
4. Investments/pensions
5. Insurance
6. Business interests
7. Digital/crypto
8. Other valuables/foreign assets
9. Access & documents
10. Family handoff review

Users should be able to skip freely.

The system should eventually distinguish:

- catalog item;
- confirmed owned;
- not owned;
- needs review;
- closed/historical.

This explicit state is preferable to inferring “recorded” from pre-populated template fields.

---

## 27. Recommended future Annual Review model

Annual Review should evolve from a summary into a workflow.

Potential inventory-level review metadata:

- review_started_at;
- review_completed_at;
- reviewed_by;
- household_confirmed;
- access_verified;
- binder_printed;
- backup_verified;
- executor/POA contact_confirmed;
- next_review_date.

Potential asset-level review metadata:

- ownership_confirmed;
- institution_confirmed;
- value_updated;
- beneficiary_checked;
- document_path_checked;
- access_path_checked;
- handoff_instructions_checked;
- closed/resolved.

The review should focus on material assets first, not force the user to inspect every catalog row equally.

---

## 28. Recommended future Executor / Incapacity modes

These should be designed as **read-oriented operational modes**, not just another layout.

### Incapacity Mode

Prioritize:

- POA/authorized person;
- financial institutions;
- bills/ongoing obligations;
- income sources;
- insurance;
- property management;
- advisor contacts;
- document locations;
- access instructions.

### Executor Mode

Prioritize:

- identity and legal-document locations;
- asset discovery;
- institution contacts;
- insurance/beneficiary assets;
- debts/liabilities;
- corporate/business interests;
- digital assets;
- property;
- tax/accountant contacts;
- actions requiring professional advice.

These modes should never imply unauthorized access rights.

---

## 29. AI-agent implementation guidance

When an AI coding agent modifies EstateON, it should use this decision order:

1. Read `product_strategy.md` for intent and product boundaries.
2. Read `feature_list.md` for current shipped behavior.
3. Read `versioning_plan.md` for tier/build rules.
4. Read `future_plan.md` for roadmap context.
5. Read schema/catalog docs for data-model constraints.
6. Inspect generated outputs and E2E tests before changing behavior.
7. Preserve build-time code stripping for lower tiers.
8. Preserve internal `planning` tier compatibility unless an explicit migration is approved.
9. Preserve self-contained/offline operation for the core artifact.
10. Treat print, EN/ZH localization, mobile, license downgrade and local persistence as regression surfaces.
11. Add tests for strategic edge cases, not only happy-path visual checks.
12. Do not silently redefine pricing, edition names or product positioning from an older tactical document.

If a proposed feature conflicts with this document, the agent should flag the conflict rather than silently choosing a direction.

---

## 30. Canonical terminology

| Concept | Canonical term |
|---|---|
| Brand | EstateON |
| Product category | Family Asset Inventory & Estate Continuity System |
| Free edition | Free / 免费版 |
| Family edition | Family / 家庭版 |
| Professional edition | Professional / 专业版 |
| Internal Professional key | `planning` (compatibility) |
| Family print package | Estate Binder |
| First critical print page | Emergency Access Guide |
| Asset locator print index | Master Asset Index |
| Continuity score | Access Readiness |
| Advanced review | Annual Review |
| Advanced diagnostic | Audit |
| Catalog breadth metric | Asset Catalog / assets covered |
| Filtered count | Showing |
| Current-economic-value signal | With Value |

Avoid reintroducing **Plus** as a user-facing edition name unless there is an explicit product decision to change the three-edition strategy.

---

## 31. Working strategic decisions vs open hypotheses

### Current strategic decisions

- Core artifact remains offline/self-contained.
- User-facing editions are Free / Family / Professional.
- Professional retains internal `planning` key for compatibility.
- Free should create strong perceived product breadth, not behave like a crippled demo.
- Family is the primary household paid edition.
- Professional differentiates through intelligence/review/complexity.
- Print is Family+ under the current packaging.
- Lower-tier paid feature implementations remain build-time stripped.
- The inventory is primarily a locator/continuity map, not a casual transactional-secret vault.
- English and Chinese remain first-class product languages.

### Working hypotheses requiring market validation

- CAD $29 Family is the optimal consumer conversion price.
- CAD $99 Professional is the optimal advanced-household price.
- CAD $19/year optional Updates creates acceptable recurring revenue without harming trust.
- Adult children organizing parents may convert better than self-directed older users.
- Print Estate Binder is the strongest Free→Family conversion moment.
- Access Readiness/Audit is the strongest Family→Professional conversion moment.
- Ontario/Chinese-Canadian specialization produces a strong early-market wedge.
- Advisor/lawyer/accountant distribution can outperform paid direct-to-consumer acquisition.

These hypotheses should be measured and revised deliberately.

---

## 32. Product North Star summary

EstateON should become the most practical answer to this household question:

> **“If I could not explain my affairs myself, would the people I trust know what exists, where it is, and what to do next?”**

Every major feature should make that answer more confidently **yes**.

The product progression is:

> **Discover → Organize → Prepare → Maintain → Handoff**

The commercial progression is:

> **Free → Family → Professional**

The value progression is:

> **Breadth → Family usability → Continuity intelligence**

The trust promise is:

> **Private. Portable. Understandable. Family-ready.**

And the architectural promise is:

> **The user owns a durable artifact that can outlive the software company that created it.**
