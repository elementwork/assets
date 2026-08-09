# Asset Inventory Generator — Administrator Guide

> **Last updated:** 2026-08-09 16:46:21
> **Audience:** Administrators / maintainers who install, generate, customize, or
> troubleshoot the tool. End users should read the in-dashboard help (the **?** button)
> instead — it covers everyday usage in English and Chinese.

---

## 1. Overview

A self-contained, offline-first asset inventory tool for Canadian families in Ontario.
The Python generator produces three artifact types (Markdown, multi-sheet Excel, and a
single-file HTML dashboard) in English and Chinese. No server, no external runtime for the
dashboard, and no data leaves the user's device.

### Components

| Path | Purpose |
|------|---------|
| `src/generate_asset_inventory.py` | Generator: asset catalog, field schema, Markdown/Excel/HTML output, CLI |
| `src/translations.py` | UI / Excel / category / field translations (en, zh) |
| `templates/dashboard.html` | Single-file dashboard template with `{{TR_*}}` / `{{*_JSON}}` placeholders |
| `tests/e2e_visual_test.py` | End-to-end test: regenerates outputs + drives both dashboards in headless Chromium |
| `docs/dev/ASSET_FIELDS.md` | 108-field schema documentation |
| `docs/dev/feature_list.md` | Shipped feature catalog (implementation status) |
| `docs/dev/future_plan.md` | Roadmap (planned work, tracked by ID) |
| `output/` | Generated artifacts (regenerated on every run) |

---

## 2. Installation

Requires Python 3.9+.

```bash
# Generator only (Excel output needs openpyxl)
pip3 install openpyxl

# Full test suite (browser E2E)
pip3 install --user playwright==1.49.1 openpyxl
python3 -m playwright install chromium
```

Verify:

```bash
python3 -m py_compile src/*.py tests/*.py
python3 src/generate_asset_inventory.py --help
```

---

## 3. Generation (CLI)

Run from the project root:

```bash
python3 src/generate_asset_inventory.py
```

This regenerates all six artifacts in `output/` (en + zh: Markdown, Excel, HTML dashboard).

### Options

| Flag | Description |
|------|-------------|
| `--output, -o {md,excel,html,all}` | Formats to write (default `all`) |
| `--output-dir, -d DIR` | Output directory (default `./output`) |
| `--owner NAME` | Filter to assets whose owner contains NAME (case-insensitive) |
| `--category NAME` | Filter to assets whose category contains NAME |
| `--status {active,dormant,all}` | Filter by status (default `all`) |
| `--lang, -l {en,zh}` | Output language (default `en`; zh adds a `-zh` filename suffix) |
| `--demo` | Overlay a realistic Ontario family fixture (James & Mei Chen, 27 populated assets) |

### Examples

```bash
# Chinese Markdown only
python3 src/generate_asset_inventory.py --lang zh -o md

# English dashboard with demo data (for screenshots / first-run)
python3 src/generate_asset_inventory.py --demo -o html

# Filtered output
python3 src/generate_asset_inventory.py --owner "Chen" --category "Real Estate"
```

### Output naming

| Language | Markdown | Excel | HTML |
|----------|----------|-------|------|
| en | `asset-inventory.md` | `asset-inventory.xlsx` | `asset-inventory-dashboard.html` |
| zh | `asset-inventory-zh.md` | `asset-inventory-zh.xlsx` | `asset-inventory-dashboard-zh.html` |

### Filter semantics

- Filters apply **before** translation, so they match the source (English) data.
- The `--demo` fixture overlays sample data on the 517-asset template; only 27 assets are
  populated (flagged `source = "demo"`).

---

## 4. Data model

### Asset catalog

- **517 asset types** across **32 categories** (`ASSET_CATEGORIES` in `generate_asset_inventory.py`).
- Each asset has a **108-field schema** (`FIELD_DEFINITIONS`), grouped into 13 sections:
  Core Identity, Ownership, Institution & Access, Financial Value, Dates,
  Registration & Tax, Location & Access, Insurance & Protection, Status & Control,
  Beneficiary Designation, Estate Planning, Documentation, Notes.
- Field types: `text`, `textarea`, `select` (with options), `currency`, `percent`,
  `date`, `url`, `password`. The dashboard renders schema-appropriate inputs automatically.

> **Note:** `beneficiary` (Ownership) and `primary_beneficiary` (Beneficiary Designation)
> are separate fields. The Excel Beneficiaries sheet and the audit view use
> `primary_beneficiary`, falling back to `beneficiary` when the former is empty.

### "File = database" model

The HTML dashboard embeds the full asset set as `ASSETS_DATA`. Users edit in the browser;
**Save HTML** rewrites the embedded data so the downloaded file carries every edit.
localStorage is a convenience cache — opening a different copy of the file still shows that
file's embedded data (unless the browser serves all copies from the same origin/key).

---

## 5. Localization

- Two locales: `en`, `zh` (Simplified Chinese). `src/translations.py` holds:
  - `UI_TRANSLATIONS` — UI strings, Excel headers/sheets, export filenames, help text.
  - `CATEGORY_TRANSLATIONS` — 32 category names (zh only; en is identity).
  - `translate_field_definitions()` — maps field labels/groups to Excel column keys.
- The template references `{{TR_<key>}}` and `{{ASSETS_JSON}}` / `{{CATEGORIES_JSON}}` /
  `{{FIELDS_JSON}}`. The generator substitutes translations first, then the JSON blocks, so
  JSON content cannot clobber translations.
- The dashboard also reads `{{TR_locale}}` and `{{TR_currency_symbol}}` for number/date
  formatting and currency display.

### Adding a locale

1. Add a `"<code>": { ... }` block to `UI_TRANSLATIONS` and (if needed) to
   `CATEGORY_TRANSLATIONS`.
2. `translate_field_definitions()` group mapping must include the new language keys, and
   `col_*` keys must exist for every field.
3. Add the locale to the `--lang` choices in `main()` and to the filename suffix logic.
4. Run the E2E test to confirm no `{{TR_*}}` placeholders survive.

---

## 6. Testing & release workflow

### E2E visual test

```bash
python3 tests/e2e_visual_test.py
```

Covers: regeneration (en/zh), static artifact checks (placeholders, sheet structure,
asset counts), `--demo` fixture validation, and headless-Chromium interaction on both
dashboards (search, filters, themes, 5 templates, 8 layouts, editing, validation,
undo/redo, duplicate, delete, file lock, charts, exports, import, print,
quick-add, bulk edit, inline edit, kanban, columns, markdown, auto-save, plus regression
coverage for CSV injection, numeric-id import, audit filters, compact collapse).
**125 checks**; exit code 0 = pass. Screenshots land in
`tests/screenshots/` (gitignored).

### Pre-push checklist (see `docs/agents/pre-push.md`)

1. `python3 -m py_compile src/*.py tests/*.py`
2. `python3 -m pyflakes src/*.py` (if available; pre-existing warnings acceptable)
3. `python3 tests/e2e_visual_test.py` — must end with `0 failed`
4. Review `git status` / `git diff --stat`
5. Commit/push only with explicit user approval

> **Doc convention:** when updating any doc, set its timestamp to
> `YYYY-MM-DD HH:MM:SS` (date + time).

---

## 7. Security model

- **File Lock (whole-file encryption, default off):** the entire dashboard HTML is
  encrypted with AES-256-GCM via Web Crypto; the key is derived with PBKDF2
  (100,000 iterations, random 16-byte salt + 12-byte IV per file). The passphrase is
  derived from the owner's birth date (YYYYMMDD) plus a family word and is never stored —
  **no passphrase = no recovery**.
- Enabling the lock downloads a **bootloader copy**: a small plaintext gate that holds the
  ciphertext. Opening it in a browser shows an unlock prompt; a text editor only sees
  ciphertext. After a few wrong attempts, an exponential waiting period is enforced.
- **Save HTML in a locked session** re-encrypts the whole file with the in-memory
  passphrase, so the downloaded file stays encrypted. Disabling the lock downloads a plain
  copy.
- **XSS hardening:** user-supplied values (names, categories, dates) are HTML-escaped;
  `status` is validated against a whitelist before use in CSS class names.
- **CSV export:** RFC-4180 escaping plus a formula-injection guard
  (`=` `+` `-` `@`, including leading whitespace) prefixes a quote.
- Exports: Markdown/Excel omit `login_password` / `security_questions`; `account_number`
  is masked in the Excel-style export.

### Security limitations to document for users

- The file lock protects the file at rest (text editor / scanning / casual viewing). It is
  not a substitute for strong-key protection: the passphrase space is small
  (birth date + family word), so someone who knows the birth date — or can guess the word —
  can attempt an offline brute force. The in-browser backoff only slows repeated attempts
  through the UI; it cannot stop offline cracking of a copied file.
- Exported **JSON** contains the full asset array in **plaintext** when the file is not
  locked (the lock only guards the HTML artifact).
- localStorage persistence is per browser origin; clearing browser storage loses edits
  unless the user exported via Save HTML.

---

## 8. Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| `[SKIP] openpyxl not installed` | `pip3 install openpyxl` |
| Excel generation silent skip | Same as above; only Excel is affected, MD/HTML still emit |
| E2E fails at browser launch | `python3 -m playwright install chromium` |
| `{{TR_*}}` visible in dashboard | Template placeholder not translated — add key to `UI_TRANSLATIONS` and rerun |
| Wrong field count (e.g. 109 vs 108) | `FIELD_DEFINITIONS` and `ASSET_FIELDS.md` must match; the E2E does not yet assert this |
| Filtered output looks empty | Filters apply to source (English) data before translation; check `--owner`/`--category` spelling |
| Downloaded HTML shows old data | Another copy of the file shares the same localStorage key; use a fresh profile or open via USB/different browser |
| Locked file data unrecoverable | Passphrase is never stored; there is no recovery path — this is by design |
| Locked file won't open in a text editor | Expected — the file is a bootloader + ciphertext; open it in a browser and enter birth date + family word |

---

## 9. Maintenance notes

- **Schema edits** (adding/removing fields): update `FIELD_DEFINITIONS`,
  `generate_all_assets()` defaults, `ASSET_FIELDS.md`, `col_*` translations, and the
  dashboard's detail/modal rendering (schema-driven, so mostly automatic). No
  `schema_version` migration exists yet — see `future_plan.md` (SEC-2 / EN-1).
- **New asset types** are added under `ASSET_CATEGORIES`; ids are assigned sequentially
  (`A-0001` …).
- **Roadmap / status:** completed features live in `docs/dev/feature_list.md`; planned
  work is tracked in `docs/dev/future_plan.md` by ID (SEC-/ON-/PL-/NW-/PA-/IO-/UX-/EN-).
