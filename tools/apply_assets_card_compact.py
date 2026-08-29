#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates' / 'dashboard.html'
TEST = ROOT / 'tests' / 'e2e_visual_test.py'
FEATURE = ROOT / 'docs' / 'dev' / 'feature_list.md'

s = TPL.read_text(encoding='utf-8')
old = '''            <div class="stat-card stat-card-assets">
                <div class="stat-icon">🗂️</div>
                <div class="stat-content">
                    <div class="stat-value" id="assetCount">0</div>
                    <div class="stat-label">{{TR_assets}}</div>
                    <button class="stat-add-btn" id="statAddAssetBtn" type="button">＋ {{TR_add_asset}}</button>
                    <div class="stat-subline"><span><strong id="withValueCount">0</strong> {{TR_with_value}}</span></div>
                </div>
            </div>'''
new = '''            <div class="stat-card stat-card-assets">
                <div class="stat-icon">🗂️</div>
                <div class="stat-content assets-stat-grid">
                    <div class="assets-stat-left">
                        <div class="stat-value" id="assetCount">0</div>
                        <div class="stat-label">{{TR_assets}}</div>
                    </div>
                    <div class="assets-stat-right">
                        <button class="stat-add-btn" id="statAddAssetBtn" type="button">＋ {{TR_add_asset}}</button>
                        <div class="stat-subline"><span><strong id="withValueCount">0</strong> {{TR_with_value}}</span></div>
                    </div>
                </div>
            </div>'''
if old not in s:
    raise SystemExit('Assets card anchor not found')
s = s.replace(old, new, 1)

old = '''        <span class="filter-result-count"><strong id="showingCount">0</strong> {{TR_showing}}</span>
'''
if old not in s:
    raise SystemExit('filter-result-count anchor not found')
s = s.replace(old, '', 1)

# Override prior vertical Assets-card rules with a compact two-column row.
css = '''\n/* ===== COMPACT ASSETS CARD ===== */
.stat-card-assets .assets-stat-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: center;
    gap: 10px;
    width: 100%;
}
.assets-stat-left,
.assets-stat-right {
    min-width: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.assets-stat-left { align-items: flex-start; text-align: left; }
.assets-stat-right { align-items: flex-end; text-align: right; }
.stat-card-assets .stat-add-btn {
    margin: 0;
    white-space: nowrap;
    align-self: auto;
}
.stat-card-assets .stat-subline {
    width: auto;
    margin-top: 4px;
    align-self: auto;
    text-align: right;
    white-space: nowrap;
}
'''
if '</style>' not in s:
    raise SystemExit('style close not found')
s = s.replace('</style>', css + '\n</style>', 1)
TPL.write_text(s, encoding='utf-8')

# Tests: Showing UI is intentionally removed; add compact card geometry assertions.
t = TEST.read_text(encoding='utf-8')
t = t.replace('''    check("en: Showing starts at 517", page.text_content("#showingCount") == "517", page.text_content("#showingCount"))
''', '''    check("en: filter result count removed", page.locator(".filter-result-count").count() == 0 and page.locator("#showingCount").count() == 0)
''')
t = t.replace('''    check("en: Showing count follows search", int(page.text_content("#showingCount")) == n, page.text_content("#showingCount"))
''', '')
anchor = '''            check(f"responsive {width}: search/category/owner/status all in filter bar",
                  page.locator(".filter-bar #searchInput").count() == 1
                  and page.locator(".filter-bar #categoryFilter").count() == 1
                  and page.locator(".filter-bar #ownerFilter").count() == 1
                  and page.locator(".filter-bar .status-toggle-btn").count() == 4)
'''
extra = anchor + '''            check(f"responsive {width}: filter result count absent",
                  page.locator(".filter-bar .filter-result-count").count() == 0)
            asset_card = page.locator(".stat-card-assets")
            left_box = asset_card.locator(".assets-stat-left").bounding_box()
            right_box = asset_card.locator(".assets-stat-right").bounding_box()
            check(f"responsive {width}: Assets card stays two-column on one row",
                  bool(left_box and right_box and abs((left_box['y'] + left_box['height']/2) - (right_box['y'] + right_box['height']/2)) <= 18
                       and left_box['x'] < right_box['x']),
                  f"left={left_box} right={right_box}")
            check(f"responsive {width}: Assets card right column order",
                  asset_card.locator(".assets-stat-right > *").count() == 2
                  and asset_card.locator(".assets-stat-right > *").nth(0).get_attribute("id") == "statAddAssetBtn"
                  and asset_card.locator(".assets-stat-right > *").nth(1).get_attribute("class").startswith("stat-subline"))
'''
if anchor not in t:
    raise SystemExit('responsive test anchor not found')
t = t.replace(anchor, extra, 1)
TEST.write_text(t, encoding='utf-8')

f = FEATURE.read_text(encoding='utf-8')
f = f.replace(
    '| 2a.4 | Summary separates Asset Types, Categories and recorded Assets; Assets card includes Add Asset and With Value context; All / With Value remain quick filters | ✅ |',
    '| 2a.4 | Summary separates Asset Types, Categories and recorded Assets; Assets card uses a compact two-column row (count/label left, Add Asset/With Value right); All / With Value remain quick filters | ✅ |'
)
f = f.replace(
    '| 2a.5 | Search, scope, category, owner and Active / Dormant / Pending / Closed controls stay in one non-wrapping filter-bar row; status buttons remain directly visible and right-aligned | ✅ |',
    '| 2a.5 | Search, scope, category, owner and Active / Dormant / Pending / Closed controls stay in one non-wrapping filter-bar row; the Showing/filter-result count is removed and status buttons remain directly visible/right-aligned | ✅ |'
)
FEATURE.write_text(f, encoding='utf-8')
print('Applied compact Assets card and removed filter result count')
