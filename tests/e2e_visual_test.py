#!/usr/bin/env python3
"""
End-to-end visual test for the Asset Inventory Generator.

Pipeline under test:
    1. Regenerate all outputs (en + zh): Markdown, Excel, self-contained HTML dashboard
    2. Static validation of the generated artifacts (no leftover template placeholders,
       Excel workbook structure, Markdown content)
    3. Headless-Chromium interaction on the generated dashboards (en + zh):
       stats, search, filters, themes, templates, layouts, table sorting, edit modal,
       validation, undo/redo, duplicate, delete, vault, charts, exports, import, print
    4. Screenshots captured to tests/screenshots/ for visual review

Exit code 0 = all checks pass, 1 = one or more failures.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
SHOTS = ROOT / "tests" / "screenshots"

EN_HTML = OUT / "asset-inventory-dashboard.html"
ZH_HTML = OUT / "asset-inventory-dashboard-zh.html"
EN_MD = OUT / "asset-inventory.md"
ZH_MD = OUT / "asset-inventory-zh.md"
EN_XLSX = OUT / "asset-inventory.xlsx"
ZH_XLSX = OUT / "asset-inventory-zh.xlsx"

PASSED = []
FAILED = []


def check(name, cond, detail=""):
    if cond:
        PASSED.append(name)
        print(f"  PASS  {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL  {name}  {detail}")
    return cond


# =============================================================================
# STEP 1 — Regenerate outputs
# =============================================================================

def run_generation():
    print("\n== Step 1: regenerate outputs (en + zh) ==")
    for lang in ("en", "zh"):
        cmd = [sys.executable, str(ROOT / "src" / "generate_asset_inventory.py")]
        if lang == "zh":
            cmd += ["--lang", "zh"]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
        check(
            f"generator ({lang}) exits 0",
            r.returncode == 0,
            f"exit={r.returncode}\nstdout={r.stdout[-800:]}\nstderr={r.stderr[-800:]}",
        )
    for p in (EN_MD, ZH_MD, EN_XLSX, ZH_XLSX, EN_HTML, ZH_HTML):
        check(f"output exists: {p.name}", p.exists() and p.stat().st_size > 0)


# =============================================================================
# STEP 2 — Static validation of generated artifacts
# =============================================================================

def static_checks():
    print("\n== Step 2: static artifact checks ==")

    # Markdown
    en_md = EN_MD.read_text(encoding="utf-8")
    zh_md = ZH_MD.read_text(encoding="utf-8")
    check("en md: title header", "# Asset Inventory" in en_md)
    check("en md: 517 assets reported", "Total Assets:** 517" in en_md)
    check("en md: category sections", en_md.count("\n## ") >= 32)
    check("zh md: Chinese title", "资产清单" in zh_md)
    check("zh md: 517 assets reported", "资产总数:** 517" in zh_md)

    # Excel
    try:
        import openpyxl
    except ImportError:
        check("openpyxl importable", False, "pip install openpyxl")
        return
    wb = openpyxl.load_workbook(EN_XLSX)
    en_sheets = [ws.title for ws in wb.worksheets]
    check(
        "en xlsx: expected sheets",
        en_sheets == ["All Assets", "By Category", "Summary", "Access",
                      "Financial Summary", "Insurance", "Beneficiaries", "Estate"],
        f"got {en_sheets}",
    )
    check("en xlsx: All Assets has 518 rows", wb["All Assets"].max_row == 518)
    wb_zh = openpyxl.load_workbook(ZH_XLSX)
    zh_sheets = [ws.title for ws in wb_zh.worksheets]
    check(
        "zh xlsx: expected sheets",
        zh_sheets == ["全部资产", "按类别", "摘要", "访问信息",
                      "财务摘要", "保险", "受益人", "遗产"],
        f"got {zh_sheets}",
    )
    check("zh xlsx: 全部资产 has 518 rows", wb_zh["全部资产"].max_row == 518)

    # HTML: no leftover placeholders, data blocks present
    for label, path in (("en", EN_HTML), ("zh", ZH_HTML)):
        html = path.read_text(encoding="utf-8")
        leftovers = re.findall(r"\{\{(?:TR_|ASSETS_JSON|CATEGORIES_JSON|FIELDS_JSON)", html)
        check(f"{label} html: no leftover placeholders", not leftovers, f"found {leftovers[:5]}")
        check(f"{label} html: ASSETS_DATA embedded", "const ASSETS_DATA = [" in html)
        check(f"{label} html: CATEGORIES_DATA embedded", "const CATEGORIES_DATA =" in html)
        check(f"{label} html: FIELDS_DATA embedded", "const FIELDS_DATA =" in html)
        check(f"{label} html: 517 assets in JSON", html.count('"id": "A-') == 517)
        check(f"{label} html: file-size sanity (>200KB)", len(html) > 200_000)


# =============================================================================
# STEP 2b — Demo fixture (1.7)
# =============================================================================

def demo_fixture_check():
    print("\n== Step 2b: --demo fixture (1.7) ==")
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [sys.executable, str(ROOT / "src" / "generate_asset_inventory.py"),
               "--demo", "-d", tmp]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
        check("demo: generator --demo exits 0", r.returncode == 0, r.stderr[-500:])
        html = (Path(tmp) / "asset-inventory-dashboard.html").read_text(encoding="utf-8")
        i = html.find("const ASSETS_DATA = ")
        j = html.find(";\nconst CATEGORIES_DATA", i)
        data = json.loads(html[i + len("const ASSETS_DATA = "):j])
        demo = [a for a in data if a.get("source") == "demo"]
        check("demo: 27 populated assets", len(demo) == 27, f"n={len(demo)}")
        total_fmv = sum(float(a.get("fmv") or 0) for a in demo)
        check("demo: FMV populated", total_fmv > 2_000_000, f"${total_fmv:,.0f}")
        owners = {a.get("owner") for a in demo if a.get("owner")}
        check("demo: James & Mei Chen owners",
              {"James Chen", "Mei Chen"} <= owners, str(owners))
        dormant = [a for a in demo if a.get("status") == "Dormant"]
        check("demo: dormant crypto wallet",
              any("Bitcoin" in (a.get("asset_name") or "") for a in dormant))
        check("demo: markdown notes in fixture",
              any("**" in (a.get("notes") or "") for a in demo))


# =============================================================================
# STEP 3 — Browser E2E
# =============================================================================

def browser_e2e():
    print("\n== Step 3: browser E2E (en + zh) ==")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ok = e2e_en(browser)
        ok = e2e_zh(browser) and ok
        browser.close()
        return ok


def _new_page(browser, html_path, viewport=(1440, 1000)):
    context = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                                  accept_downloads=True)
    page = context.new_page()
    js_errors = []
    page.on("pageerror", lambda exc: js_errors.append(str(exc)))
    page.on("console", lambda msg: js_errors.append(msg.text) if msg.type == "error" else None)
    page.goto(html_path.as_uri(), wait_until="load")
    return context, page, js_errors


def _layout(page, name):
    page.click(f'.layout-btn[data-layout="{name}"]')
    page.wait_for_timeout(150)


def _open_modal(page, asset_id):
    page.click(f'[data-asset-id="{asset_id}"]')
    page.wait_for_selector("#modalOverlay.active", timeout=5000)


def _save_modal(page):
    page.click("#modalSave")
    page.wait_for_selector("#modalOverlay:not(.active)", timeout=8000)


def e2e_en(browser):
    print("  -- en dashboard --")
    context, page, js_errors = _new_page(browser, EN_HTML)
    ok = True

    # Core rendering
    check("en: page title", "Asset Inventory" in page.title(), page.title())
    check("en: stat totalAssets = 517", page.text_content("#totalAssets") == "517",
          page.text_content("#totalAssets"))
    check("en: stat totalCategories = 32", page.text_content("#totalCategories") == "32",
          page.text_content("#totalCategories"))
    check("en: dashboard view renders 517 items",
          page.locator("#dashboardView .asset-item").count() == 517)

    # Search (input is debounced 300ms in the template)
    page.fill("#searchInput", "Chequing")
    page.wait_for_timeout(600)
    n = page.locator("#dashboardView .asset-item").count()
    check("en: search 'Chequing' narrows results", 0 < n < 517, f"n={n}")
    page.fill("#searchInput", "")
    page.wait_for_timeout(600)
    check("en: clearing search restores 517",
          page.locator("#dashboardView .asset-item").count() == 517)

    # Category filter
    first_cat = page.locator("#categoryFilter option").nth(1).text_content()
    expected = page.evaluate(
        "assets.filter(a => a.category === document.querySelector('#categoryFilter').value).length"
    ) if False else None
    page.select_option("#categoryFilter", index=1)
    page.wait_for_timeout(150)
    actual = page.locator("#dashboardView .asset-item").count()
    # Compare with the JS-side filtered length for correctness, not just a drop.
    expected = page.evaluate(
        "getFilteredAssets().length"
    )
    check(f"en: category filter '{first_cat}' matches", actual == expected,
          f"dom={actual} js={expected}")
    page.select_option("#categoryFilter", index=0)
    page.wait_for_timeout(150)

    # Theme toggle
    theme_before = page.evaluate("document.documentElement.getAttribute('data-theme')")
    page.click("#themeToggle")
    theme_after = page.evaluate("document.documentElement.getAttribute('data-theme')")
    check("en: theme toggle flips light/dark", theme_before != theme_after,
          f"{theme_before} -> {theme_after}")
    page.click("#themeToggle")  # back to light

    # Template select (5 templates)
    templates = page.locator("#templateSelect option").count()
    check("en: 5 template options", templates == 5, f"n={templates}")
    for i in range(1, 5):  # indexes 1..4 cover all 5 templates (0..4)
        page.select_option("#templateSelect", index=i)
        attr = page.evaluate("document.documentElement.getAttribute('data-template')")
        if i == 1:
            check("en: template select updates data-template", bool(attr), attr)
    page.screenshot(path=str(SHOTS / "en-dashboard.png"))

    # Layouts
    _layout(page, "table")
    check("en: table layout rows (50/page)", page.locator("#tableBody tr").count() == 50,
          page.locator("#tableBody tr").count())
    first_id_before = page.locator("#tableBody tr").first.text_content()
    page.click('th[data-sort="asset_name"]')  # sort ascending by name
    page.wait_for_timeout(150)
    page.click('th[data-sort="asset_name"]')  # sort descending
    page.wait_for_timeout(150)
    first_id_after = page.locator("#tableBody tr").first.text_content()
    check("en: table sort reorders rows", first_id_before != first_id_after,
          f"\nbefore={first_id_before[:60]!r}\nafter={first_id_after[:60]!r}")
    page.screenshot(path=str(SHOTS / "en-table.png"))

    _layout(page, "kanban")
    check("en: kanban cards", page.locator(".kanban-card").count() == 517)
    page.screenshot(path=str(SHOTS / "en-kanban.png"))

    _layout(page, "timeline")
    tl = page.locator(".timeline-item").count()
    check("en: timeline renders (items or empty state)", tl >= 0)
    check("en: timeline empty-state shown for undated template",
          page.locator(".empty-state").count() >= 1 or tl > 0)

    _layout(page, "detail")
    check("en: detail list items", page.locator("#detailAssetList .detail-asset-item").count() == 517)
    check("en: detail content grid", page.locator("#detailContent .detail-grid").count() == 1)

    _layout(page, "compact")
    check("en: compact view items", page.locator(".compact-asset").count() == 517)

    _layout(page, "audit")
    check("en: audit summary pills", page.locator(".audit-summary .audit-pill").count() == 3)
    n_audit = page.locator(".audit-item").count()
    check("en: audit flags all 517 template assets", n_audit == 517, f"n={n_audit}")
    page.screenshot(path=str(SHOTS / "en-audit.png"))

    # Charts: template has no FMV -> empty charts; after an FMV edit they populate.
    _layout(page, "charts")
    check("en: charts cards render", page.locator(".chart-card").count() == 4)
    check("en: charts empty without FMV data", page.locator(".chart-empty").count() >= 1)

    # Edit modal: schema-driven inputs
    _layout(page, "dashboard")
    _open_modal(page, "A-0001")
    fields = page.locator("#modalContent [data-field]").count()
    check("en: modal renders fields", fields > 50, f"n={fields}")
    check("en: currency input is type=number",
          page.locator('#modalContent [data-field="fmv"]').get_attribute("type") == "number")
    check("en: percent input is type=number",
          page.locator('#modalContent [data-field="yield_pct"]').get_attribute("type") == "number")
    date_field = page.locator('#modalContent [data-field="acquisition_date"]')
    check("en: date input is type=date",
          date_field.count() == 1 and date_field.get_attribute("type") == "date")
    check("en: select input rendered",
          page.locator('#modalContent select[data-field="status"]').count() == 1)

    # Validation: required asset_name blocks save
    page.fill('#modalContent [data-field="asset_name"]', "")
    page.click("#modalSave")
    page.wait_for_timeout(200)
    check("en: validation blocks save on missing name",
          page.locator("#modalOverlay.active").count() == 1 and
          page.locator("#modalContent .form-error").count() >= 1)
    page.fill('#modalContent [data-field="asset_name"]', "Test Chequing Account")

    # Edit + save: FMV so charts populate; name so we can verify persistence
    page.fill('#modalContent [data-field="fmv"]', "25000")
    _save_modal(page)
    check("en: unsaved-changes indicator appears",
          page.locator("#unsavedIndicator.visible").count() == 1)
    check("en: edited name in dashboard",
          page.locator("#dashboardView .asset-item").first.text_content().__contains__("Test Chequing Account") or
          page.locator("#dashboardView").text_content().__contains__("Test Chequing Account"))

    # Undo / redo via keyboard shortcuts
    page.keyboard.press("Control+z")
    page.wait_for_timeout(200)
    check("en: undo reverts edit",
          "Test Chequing Account" not in page.locator("#dashboardView").text_content())
    page.keyboard.press("Control+Shift+z")
    page.wait_for_timeout(200)
    check("en: redo re-applies edit",
          "Test Chequing Account" in page.locator("#dashboardView").text_content())

    # Charts now show the edited FMV
    _layout(page, "charts")
    check("en: charts populate after FMV edit",
          page.locator("#chartsView svg").count() >= 1)
    page.screenshot(path=str(SHOTS / "en-charts.png"))
    _layout(page, "dashboard")

    # Duplicate
    _open_modal(page, "A-0001")
    page.click("#modalDuplicate")
    page.wait_for_timeout(300)
    dup_id = page.evaluate("currentAsset ? (currentAsset.id || '') : ''")
    check("en: duplicate opens copy in modal", "copy" in dup_id, f"id={dup_id}")
    _save_modal(page)
    check("en: duplicated asset added (518)",
          page.locator("#dashboardView .asset-item").count() == 518)

    # Delete (confirm dialog)
    _open_modal(page, "A-0001-copy")
    page.once("dialog", lambda d: d.accept())
    page.click("#modalDelete")
    page.wait_for_timeout(300)
    check("en: deleted asset removed (517)",
          page.locator("#dashboardView .asset-item").count() == 517)

    # Vault: give the vault a real credential to encrypt first (blank template
    # data has no plaintext credentials, so set/encrypt/lock would be no-ops).
    _open_modal(page, "A-0001")
    page.fill('#modalContent [data-field="login_password"]', "s3cret-pw!")
    _save_modal(page)
    page.click("#vaultToggle")
    page.wait_for_selector("#vaultOverlay.active", timeout=5000)
    page.fill("#vaultPass1", "test-passphrase-123")
    page.fill("#vaultPass2", "test-passphrase-123")
    page.click("#vaultSetBtn")
    page.wait_for_timeout(2500)  # PBKDF2 derivation
    status = page.text_content("#vaultStatusText")
    check("en: vault set -> unlocked", "unlocked" in status.lower(), status)
    enc = page.evaluate("assets.find(a => a.id === 'A-0001').login_password")
    check("en: credential encrypted at rest",
          isinstance(enc, dict) and enc.get("enc") is True, str(enc)[:60])
    check("en: vault set cleared undo/redo history",
          page.evaluate("undoStack.length === 0 && redoStack.length === 0"))
    page.click("#vaultLockBtn")
    page.wait_for_timeout(200)
    status = page.text_content("#vaultStatusText")
    check("en: vault lock", "locked" in status.lower(), status)
    page.fill("#vaultPass1", "wrong-passphrase")
    page.click("#vaultUnlockBtn")
    page.wait_for_timeout(2500)
    toast = page.locator(".toast-notification").text_content() if page.locator(".toast-notification").count() else ""
    status = page.text_content("#vaultStatusText")
    check("en: vault rejects wrong passphrase",
          "incorrect" in toast.lower() and "locked" in status.lower(),
          f"toast={toast!r} status={status!r}")
    page.fill("#vaultPass1", "test-passphrase-123")
    page.click("#vaultUnlockBtn")
    page.wait_for_timeout(2500)
    status = page.text_content("#vaultStatusText")
    check("en: vault unlocks with correct passphrase", "unlocked" in status.lower(), status)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    # Exports (downloads)
    with page.expect_download() as dl:
        page.click("#exportMD")
    md_dl = dl.value
    md_content = Path(md_dl.path()).read_text(encoding="utf-8") if md_dl.path() else ""
    check("en: export Markdown downloads", "# Asset Inventory" in md_content)
    check("en: exported MD carries edits", "Test Chequing Account" in md_content)

    with page.expect_download() as dl:
        page.click("#exportExcel")
    csv_dl = dl.value
    csv_content = Path(csv_dl.path()).read_text(encoding="utf-8") if csv_dl.path() else ""
    check("en: export CSV downloads", "ID,Category" in csv_content)

    with page.expect_download() as dl:
        page.click("#exportJSON")
    json_dl = dl.value
    json_content = Path(json_dl.path()).read_text(encoding="utf-8") if json_dl.path() else ""
    try:
        exported = json.loads(json_content)
        json_ok = isinstance(exported, list) and len(exported) == 517 and \
            any(a.get("asset_name") == "Test Chequing Account" for a in exported)
    except Exception as e:
        json_ok = False
        json_content = str(e)
    check("en: export JSON round-trips 517 assets with edits", json_ok)

    with page.expect_download() as dl:
        page.click("#saveHTML")
    html_dl = dl.value
    html_path = html_dl.path()
    saved_html = Path(html_path).read_text(encoding="utf-8") if html_path else ""
    check("en: save-HTML carries edits",
          "const ASSETS_DATA = [" in saved_html and "Test Chequing Account" in saved_html)

    # Import JSON (replaces assets)
    page.set_input_files("#importJSONFile", str(json_dl.path()))
    page.wait_for_timeout(500)
    check("en: import JSON restores asset set",
          page.locator("#dashboardView .asset-item").count() == 517)

    # Print
    page.click("#printBtn")
    page.wait_for_timeout(400)
    print_html = page.text_content("#printView")
    check("en: print view populated", print_html is not None and len(print_html) > 500)

    # ---- Quick-add wizard (3.7) ----
    page.click("#addAssetBtn")
    page.wait_for_selector("#wizardOverlay.active", timeout=5000)
    types = page.locator(".wizard-type-item").count()
    check("en: wizard type list renders", types > 400, f"n={types}")
    page.fill("#wizardSearch", "Chequing")
    page.wait_for_timeout(250)
    narrowed = page.locator(".wizard-type-item").count()
    check("en: wizard search narrows types", 0 < narrowed < types, f"n={narrowed}")
    page.click('.wizard-type-item[data-type="Chequing Account"]')
    page.click("#wizardNext")
    page.wait_for_timeout(250)
    check("en: wizard step 2 institution pre-filled",
          page.locator("#wizardInstitution").input_value() != "")
    page.click("#wizardNext")
    page.wait_for_timeout(250)
    page.fill("#wizardOwner", "James Chen")
    page.click("#wizardNext")
    page.wait_for_timeout(250)
    page.fill("#wizardFmv", "5000")
    page.click("#wizardFinish")
    page.wait_for_selector("#wizardOverlay:not(.active)", timeout=8000)
    check("en: wizard creates asset",
          page.evaluate("assets.some(a => a.source === 'quick-add')"))

    # ---- Bulk edit (3.8) ----
    _layout(page, "table")
    # Earlier sort tests left the table sorted by asset_name desc; restore
    # id-ascending order so A-0001/A-0002 are on page 1 for selection.
    page.click('th[data-sort="id"]')
    page.wait_for_timeout(250)
    page.check('.row-check[data-check-id="A-0001"]')
    page.check('.row-check[data-check-id="A-0002"]')
    check("en: bulk selection bar visible", page.locator("#bulkBar").is_visible())
    page.click("#bulkEditBtn")
    page.wait_for_selector("#bulkOverlay.active", timeout=5000)
    page.select_option("#bulkFieldSelect", "owner")
    page.fill("#bulkValueInput", "Bulk Owner")
    page.click("#bulkApplyBtn")
    page.wait_for_selector("#bulkOverlay:not(.active)", timeout=8000)
    check("en: bulk edit updates both assets",
          page.evaluate("['A-0001', 'A-0002'].every(id => (assets.find(a => a.id === id) || {}).owner === 'Bulk Owner')"))

    # ---- Inline table editing (3.9) ----
    cell = page.locator('#tableBody tr[data-asset-id="A-0001"] td[data-edit-field="asset_name"]')
    cell.dblclick()
    page.wait_for_timeout(250)
    page.fill('#tableBody tr[data-asset-id="A-0001"] .inline-edit-input', "Inline Edited")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    check("en: inline cell edit saved",
          page.evaluate("(assets.find(a => a.id === 'A-0001') || {}).asset_name") == "Inline Edited")

    # ---- Kanban drag-and-drop (3.10) ----
    _layout(page, "kanban")
    check("en: kanban cards draggable",
          page.locator('.kanban-card[data-asset-id="A-0001"]').get_attribute("draggable") == "true")
    page.evaluate("""() => {
        const src = document.querySelector('.kanban-card[data-asset-id="A-0001"]');
        const dst = document.querySelector('.kanban-column[data-kanban-status="Dormant"] .kanban-body');
        const dt = new DataTransfer();
        src.dispatchEvent(new DragEvent('dragstart', { bubbles: true, dataTransfer: dt }));
        dst.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer: dt }));
        dst.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer: dt }));
        src.dispatchEvent(new DragEvent('dragend', { bubbles: true, dataTransfer: dt }));
    }""")
    page.wait_for_timeout(300)
    check("en: kanban drag moves asset to Dormant",
          page.evaluate("(assets.find(a => a.id === 'A-0001') || {}).status") == "Dormant")

    # ---- Column configuration (3.11) ----
    _layout(page, "table")
    page.click("#columnConfigBtn")
    page.wait_for_timeout(250)
    check("en: column menu renders 8 toggles",
          page.locator("#columnConfigMenu label").count() == 8)
    page.uncheck('input[data-col-check="owner"]')
    page.wait_for_timeout(250)
    check("en: owner column hidden",
          page.locator('.data-table th[data-col="owner"]').evaluate("el => el.style.display === 'none'"))
    page.check('input[data-col-check="owner"]')
    page.wait_for_timeout(250)
    check("en: owner column restored",
          page.locator('.data-table th[data-col="owner"]').evaluate("el => el.style.display !== 'none'"))
    page.click("#searchInput")  # close the menu (document click handler)

    # ---- Markdown notes (3.12) ----
    _layout(page, "dashboard")
    _open_modal(page, "A-0001")
    check("en: markdown hint shown for notes field",
          page.locator("#modalContent .markdown-hint").count() >= 3)
    page.fill('#modalContent [data-field="notes"]',
              "**Bold** and *italic* and [link](https://example.com)\n- item1\n- item2")
    _save_modal(page)
    _layout(page, "detail")
    page.click('.detail-asset-item[data-detail-id="A-0001"]')
    page.wait_for_timeout(300)
    detail_html = page.locator("#detailContent").inner_html()
    check("en: markdown bold rendered", "<strong>Bold</strong>" in detail_html)
    check("en: markdown link rendered", '<a href="https://example.com"' in detail_html)

    # ---- Auto-save (extends unsaved-changes indicator) ----
    _layout(page, "dashboard")
    _open_modal(page, "A-0002")
    page.fill('#modalContent [data-field="asset_name"]', "AutoSaved Name")
    _save_modal(page)
    check("en: autosave: dirty dot appears after edit",
          page.locator("#unsavedIndicator.visible").count() == 1)
    page.wait_for_timeout(2500)  # 1.5s debounce + margin
    check("en: autosave: dirty dot clears automatically",
          page.locator("#unsavedIndicator.visible").count() == 0)
    page.click("#autoSaveToggle")  # toggle off
    page.wait_for_timeout(250)
    check("en: autosave: toggle-off persisted",
          page.evaluate("localStorage.getItem('autoSaveEnabled')") == "0")
    _open_modal(page, "A-0003")
    page.fill('#modalContent [data-field="asset_name"]', "NoAutosave Name")
    _save_modal(page)
    page.wait_for_timeout(2500)
    check("en: autosave: off keeps dirty dot",
          page.locator("#unsavedIndicator.visible").count() == 1)
    page.click("#autoSaveToggle")  # toggle back on
    page.wait_for_timeout(2000)
    check("en: autosave: on clears dot",
          page.locator("#unsavedIndicator.visible").count() == 0)

    # ---- Regression checks (code-review fixes) ----
    # CSV formula-injection guard rejects leading-whitespace formulas
    guard_ok = page.evaluate("""(() => {
        const bad = [' =cmd|xyz', '+SUM(1,2)', '@link', '-123'];
        return bad.every(v => !/^[=+\-@]/.test(csvEscape(v).replace(/^"/, ''))) &&
               !/^[=+\-@]/.test(csvEscape('normal'));
    })()""")
    check("en: csvEscape guards leading-space formula", guard_ok,
          page.evaluate("csvEscape(' =cmd|xyz')"))

    # saveHTML must not bake decrypted plaintext from an open edit modal
    _open_modal(page, "A-0001")
    page.wait_for_timeout(300)
    with page.expect_download() as dl:
        page.evaluate("saveHTML()")  # modal is open, so trigger via JS
    leak_html = Path(dl.value.path()).read_text(encoding="utf-8") if dl.value.path() else ""
    check("en: saveHTML excludes modal plaintext password",
          "s3cret-pw!" not in leak_html)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    # Audit view follows the active search/filter
    _layout(page, "audit")
    n_all_audit = page.locator(".audit-item").count()
    page.fill("#searchInput", "Chequing")
    page.wait_for_timeout(600)
    n_filt_audit = page.locator(".audit-item").count()
    check("en: audit follows search filter", 0 < n_filt_audit < n_all_audit,
          f"n={n_filt_audit}/{n_all_audit}")
    page.fill("#searchInput", "")
    page.wait_for_timeout(600)

    # Compact category collapse hides its assets
    _layout(page, "compact")
    page.locator(".compact-category-header").first.click()
    page.wait_for_timeout(250)
    check("en: compact category collapse toggles body",
          page.locator(".compact-category-body.collapsed").count() >= 1)
    page.locator(".compact-category-header").first.click()  # restore
    page.wait_for_timeout(250)

    # Numeric-id JSON import is normalized to strings and rendered safely
    with tempfile.TemporaryDirectory() as tmp2:
        num_assets = json.loads(json_content)
        for i, a in enumerate(num_assets):
            a["id"] = i + 1  # numeric ids, as some exports/imports may produce
        num_path = Path(tmp2) / "numeric-ids.json"
        num_path.write_text(json.dumps(num_assets), encoding="utf-8")
        page.set_input_files("#importJSONFile", str(num_path))
        page.wait_for_timeout(500)
        ok_types = page.evaluate("assets.every(a => typeof a.id === 'string')")
        check("en: numeric-id import normalized to strings", ok_types,
              page.evaluate("assets.slice(0,3).map(a => a.id).join(',')"))
        _layout(page, "dashboard")
        check("en: numeric-id import renders without crash",
              page.locator("#dashboardView .asset-item").count() == len(num_assets))
        # duplicate ids are rejected, keeping the previous set
        errs_before_dup = list(js_errors)  # the reject logs an expected console.error
        dup_assets = json.loads(json_content)
        dup_assets[1]["id"] = dup_assets[0]["id"]
        dup_path = Path(tmp2) / "duplicate-ids.json"
        dup_path.write_text(json.dumps(dup_assets), encoding="utf-8")
        page.set_input_files("#importJSONFile", str(dup_path))
        page.wait_for_timeout(500)
        check("en: duplicate-id import rejected (state preserved)",
              page.evaluate("assets.length") == len(num_assets),
              page.evaluate("String(assets.length)"))
        # drop the expected duplicate-rejection console.error from the list
        js_errors[:] = errs_before_dup
        restore_path = Path(tmp2) / "restore.json"
        restore_path.write_text(json_content, encoding="utf-8")
        page.set_input_files("#importJSONFile", str(restore_path))
        page.wait_for_timeout(500)
        check("en: original export re-imported to restore state",
              page.locator("#dashboardView .asset-item").count() == 517)

    # No JS errors across the whole session
    check("en: zero JS errors on page", not js_errors, f"{js_errors[:5]}")

    context.close()
    return ok


def e2e_zh(browser):
    print("  -- zh dashboard --")
    context, page, js_errors = _new_page(browser, ZH_HTML)
    ok = True

    check("zh: title is Chinese", "资产清单" in page.title(), page.title())
    check("zh: stat totalAssets = 517", page.text_content("#totalAssets") == "517")
    check("zh: search placeholder translated",
          "搜索" in page.get_attribute("#searchInput", "placeholder"))
    check("zh: dashboard view renders 517 items",
          page.locator("#dashboardView .asset-item").count() == 517)
    check("zh: no leftover TR_ placeholders in body",
          "{{TR_" not in page.locator("body").inner_text())
    # Interact: search + theme + a layout. asset_name stays English in zh
    # builds; search by a translated category (加密货币 = Crypto) instead.
    page.fill("#searchInput", "加密货币")
    page.wait_for_timeout(600)
    n = page.locator("#dashboardView .asset-item").count()
    check("zh: Chinese search works", 0 < n < 517, f"n={n}")
    page.fill("#searchInput", "")
    page.click("#themeToggle")
    theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    check("zh: theme toggle works", theme == "dark", theme)
    _layout(page, "audit")
    check("zh: audit renders in Chinese", page.locator(".audit-item").count() == 517)
    page.screenshot(path=str(SHOTS / "zh-dashboard.png"))
    check("zh: zero JS errors on page", not js_errors, f"{js_errors[:5]}")

    context.close()
    return ok


# =============================================================================

def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    run_generation()
    static_checks()
    demo_fixture_check()
    browser_e2e()

    print("\n" + "=" * 60)
    print(f"RESULT: {len(PASSED)} passed, {len(FAILED)} failed")
    if FAILED:
        print("Failures:")
        for f in FAILED:
            print(f"  - {f}")
    print("=" * 60)
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
