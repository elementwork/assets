#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parent.parent
p = root / "templates" / "dashboard.html"
s = p.read_text(encoding="utf-8")

old = "const RECORDED_SOURCES = new Set(['quick-add', 'manual-add', 'duplicate', 'user-edit', 'demo', 'import']);"
new = "const RECORDED_SOURCES = new Set(['quick-add', 'demo', 'import']);"
if old not in s:
    raise SystemExit('RECORDED_SOURCES anchor not found')
s = s.replace(old, new, 1)

old = """function touchAsset(asset, source = 'user-edit') {
    if (!asset) return;
    asset.last_modified_by = 'user';
    asset.last_update = new Date().toISOString().slice(0, 10);
    if (!asset.source) asset.source = source;
}"""
new = """function touchAsset(asset) {
    if (!asset) return;
    asset.last_modified_by = 'user';
    asset.last_update = new Date().toISOString().slice(0, 10);
}"""
if old not in s:
    raise SystemExit('touchAsset anchor not found')
s = s.replace(old, new, 1)

old = """    copy.security_questions = '';
    copy.source = 'duplicate';
    copy.last_modified_by = 'user';
    showAssetModal(copy);"""
new = """    copy.security_questions = '';
    showAssetModal(copy);"""
if old not in s:
    raise SystemExit('duplicate source anchor not found')
s = s.replace(old, new, 1)

old = "    document.getElementById('totalAssets').textContent = ASSETS_DATA.length.toLocaleString(LOCALE);"
new = "    const assetTypeCount = Array.isArray(ASSETS_DATA) ? ASSETS_DATA.length : 0;\n    document.getElementById('totalAssets').textContent = assetTypeCount.toLocaleString(LOCALE);"
if old not in s:
    raise SystemExit('locked-safe asset type count anchor not found')
s = s.replace(old, new, 1)

old = """    menu.addEventListener('click', e => {
        if (e.target.closest('.menu-layout-item')) setFeatureMenuOpen(false);
    });"""
new = """    menu.addEventListener('click', e => {
        if (e.target.closest('.menu-layout-item, .menu-action, #themeToggle')) setFeatureMenuOpen(false);
    });"""
if old not in s:
    raise SystemExit('menu action close anchor not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")

# The standalone workspace is intentionally gone. Professional zh terminology now lives
# in the logo-triggered Features menu, so assert against that canonical navigation surface.
test_path = root / "tests" / "e2e_visual_test.py"
t = test_path.read_text(encoding="utf-8")
old = '''    check("zh: Professional workspace uses bilingual terminology",
          "Audit 财产审计" in page.locator('[data-workspace-tier="planning"]').text_content() and
          "Annual Review 年度复核" in page.locator('[data-workspace-tier="planning"]').text_content())
    _open_feature_menu(page)
    check("zh: Professional export section localized", "Export 导出" in page.locator("#featureMenu").text_content())'''
new = '''    _open_feature_menu(page)
    menu_text = page.locator("#featureMenu").text_content()
    check("zh: Professional logo menu uses bilingual terminology",
          "Audit 财产审计" in menu_text and "Annual Review 年度复核" in menu_text)
    check("zh: Professional export section localized", "Export 导出" in menu_text)'''
if old not in t:
    raise SystemExit('zh workspace test anchor not found')
t = t.replace(old, new, 1)
test_path.write_text(t, encoding="utf-8")

print('Applied schema-safe recording, locked startup, menu action-close, and zh logo-menu test')
