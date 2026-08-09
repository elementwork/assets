# Asset Inventory Generator

> **Last updated:** 2026-08-09 16:46:21

A generator for Canadian families in Ontario that produces a structured asset inventory in three formats:

- **Markdown** — human-readable reference document
- **Excel** — multi-sheet workbook for analysis
- **HTML Dashboard** — self-contained, interactive dashboard with inline editing, multiple layouts, and export options

## Project structure

```
.
├── docs/
│   ├── agents/
│   │   ├── SKILL.md             # Bilingual content audit skill
│   │   └── pre-push.md          # Pre-push validation workflow
│   └── dev/
│       ├── ASSET_FIELDS.md      # Data field definitions
│       ├── ASSET_SAMPLE_LIST.md # Sample asset categories
│       ├── feature_list.md      # Shipped + planned feature catalog
│       ├── future_plan.md       # Merged product roadmap
│       └── promotion_plan.md    # Go-to-market & sales plan
├── output/
│   ├── asset-inventory.md
│   ├── asset-inventory.xlsx
│   ├── asset-inventory-dashboard.html
│   ├── asset-inventory-zh.md
│   ├── asset-inventory-zh.xlsx
│   └── asset-inventory-dashboard-zh.html
├── src/
│   └── generate_asset_inventory.py
├── templates/
│   └── dashboard.html
├── tests/
│   ├── e2e_visual_test.py      # End-to-end visual test (generation + browser E2E)
│   └── screenshots/            # Test artifacts (gitignored)
├── .gitignore
└── README.md
```

## Requirements

- Python 3.9+
- `openpyxl` (for Excel output)

Install dependencies:

```bash
pip install openpyxl
```

## Usage

Run from the project root:

```bash
python src/generate_asset_inventory.py
```

This generates all three outputs in `output/`.

### Options

| Flag | Description |
|------|-------------|
| `-o md` | Markdown only |
| `-o excel` | Excel only |
| `-o html` | HTML dashboard only |
| `-o all` | All formats (default) |
| `-d ./output` | Output directory (default: `./output`) |
| `--owner "Name"` | Filter by owner |
| `--category "Category"` | Filter by category |
| `--status active\|dormant\|all` | Filter by status |
| `--lang en\|zh` (`-l`) | Output language (default: `en`; `zh` adds `-zh` filename suffix) |
| `--demo` | Overlay a realistic Ontario family demo fixture (owners, FMV values, registered accounts, dormant crypto, markdown notes) for screenshots and first-run exploration |

Examples:

```bash
python src/generate_asset_inventory.py --lang zh          # Chinese outputs
python src/generate_asset_inventory.py --demo -o html     # English dashboard with demo data
```

## HTML dashboard

`output/asset-inventory-dashboard.html` is a self-contained file — no server required. Open it in any modern browser.

Features:

- Five visual templates (EstateON, Lumina, Cardinal, Atlantic, Monarch) with light / dark mode
- Eight layout modes: Dashboard, Table, Kanban, Timeline, Detail, Compact, Audit, Charts
- Real-time search and filtering by category, owner, and status (applies to every layout)
- Schema-driven edit modal with validation, undo/redo, duplicate, and delete
- Quick-add wizard — search a 517-type catalog → institution → owner → value, auto-fills defaults
- Bulk edit — select table rows and set a shared field across them
- Inline table editing (double-click a cell) and sortable, configurable table columns
- Kanban drag-and-drop between status columns
- Markdown rendering for notes / alerts / to-dos
- File lock (optional, default off) — encrypts the whole file with AES-256-GCM using a birth-date + family-word passphrase; browser unlock gate, ciphertext to text editors
- Audit view (traffic-light validation) and pure-SVG charts (no libraries)
- Auto-save to browser storage plus Save-HTML that carries every edit into the downloaded file
- Export to Markdown, CSV, JSON, and self-contained HTML; print-ready estate binder
- Full English and Chinese (zh) localization

Click the **?** button in the header for a complete usage guide.

## Testing

Run the end-to-end visual test from the project root:

```bash
python3 tests/e2e_visual_test.py
```

This validates the whole pipeline and requires Python 3.9+ and `openpyxl`:

1. **Regenerates** all outputs (en + zh) with the real generator, plus a `--demo` fixture check
2. **Static checks** — Markdown headers/counts, Excel sheet structure, no leftover
   `{{TR_*}}` template placeholders in the generated HTML
3. **Browser E2E** (headless Chromium via Playwright) — renders both dashboards and
   exercises search, filters, themes, all 5 templates, all 8 layouts, table sorting,
   schema-driven edit modal, validation, undo/redo, duplicate, delete, file lock
   (encrypt/unlock/wrong-passphrase/backoff), charts, exports, JSON import, print,
   quick-add wizard, bulk edit, inline editing, kanban drag-and-drop, column
   configuration, markdown notes, and auto-save
4. **Screenshots** saved to `tests/screenshots/` for visual review

Setup (one-time):

```bash
pip3 install --user playwright==1.49.1 openpyxl
python3 -m playwright install chromium
```

Exit code `0` means all checks pass; any failure exits `1`.

## License

Proprietary — EstateON Advisors.
