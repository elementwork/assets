---
name: bilingual-content-audit
description: Systematic audit of bilingual (EN/ZH) website content for correctness, accuracy, precision, consistency, terminology alignment, and currency across all content sources.
last_updated: 2026-08-09 16:46:21
---

# Bilingual Content Audit

Systematic audit of bilingual website content. Scans all content sources and produces a structured findings report with prioritized fixes.

## When to use

- User asks to audit content, verify accuracy, check translations, or review consistency
- Before major releases or after bulk content changes
- When bilingual terminology drift is suspected

## Phase 1 — Discover content sources

Before scanning, identify all content-bearing files in the project:

1. **Locale/translation files** — JSON/YAML/i18n files with translation keys (e.g. `en.json`, `zh.json`, `translations.py`)
2. **Data files** — Structured content arrays/objects (blog articles, resources, case studies, product listings)
3. **Page components** — Route-level views with hardcoded text, CTAs, credentials
4. **Shared components** — Footer, Navigation, headers, modals with repeated text
5. **Email/API templates** — Server-rendered content, compliance disclaimers
6. **Static files** — `robots.txt`, `llms.txt`, `sitemap.xml`, meta tags in HTML entry point
7. **Legal/regulatory references** — Tax thresholds, designation titles, regulatory body names

Use `glob` and `grep` to find these. Don't assume file locations — discover them.

## Phase 2 — Audit criteria

| # | Criterion | What to check |
|---|-----------|---------------|
| 1 | Clarity & Readability | Sentence length, jargon, passive voice, reading level |
| 2 | Brand Voice Consistency | Tone uniformity across pages, persona alignment |
| 3 | SEO & Structure | Meta tags, heading hierarchy, canonical URLs, structured data |
| 4 | Persuasion & CTAs | Clear calls to action, value propositions, conversion flow |
| 5 | Accuracy & Recency | Tax rates, thresholds, dates, statistical claims — verify against sources |
| 6 | Content Gaps | Missing translations, incomplete sections, stale references |

## Phase 3 — Bilingual-specific checks

- Every content entry must exist in both languages with matching structure
- Language identifier field must be explicit on each entry
- Terminology must be consistent across all files (standardize terms, pick one translation per concept)
- Category/tag translations must be 1:1 mappings
- Interpolation syntax must match the i18n framework's requirements
- Filtering logic must handle both language variants

## Phase 4 — Produce findings report

Output a structured report with findings grouped by file, each tagged with:

- **Severity**: Critical (wrong facts) / High (inconsistency) / Medium (quality) / Low (style)
- **Location**: File path + line number
- **Current**: What exists now
- **Fix**: What to change
- **Rationale**: Why (regulatory, accuracy, consistency)

## Common fixes

- Standardize terminology across all files (pick one term, apply everywhere)
- Fix untranslated words in localized content
- Add missing language identifier fields to bilingual entries
- Update stale tax thresholds, regulatory references, designation titles
- Reconcile contradictory claims across pages
- Fix WCAG contrast issues (minimum 4.5:1 for normal text)

## Stopping condition

Report is complete when all discovered content source categories have been scanned and all findings are documented with severity, location, and fix.
