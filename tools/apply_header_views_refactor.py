#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates' / 'dashboard.html'
TEST = ROOT / 'tests' / 'e2e_visual_test.py'
FEATURE = ROOT / 'docs' / 'dev' / 'feature_list.md'


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'{label}: anchor not found')
    return text.replace(old, new, 1)


html = TPL.read_text(encoding='utf-8')

old_header = '''<header class="header tier-header">
    <div class="header-left">
        <div class="logo">
            <button class="logo-icon logo-menu-toggle" id="featureMenuToggle" type="button"
                    aria-expanded="false" aria-controls="featureMenu" aria-label="{{TR_menu}}" title="{{TR_menu}}">📊</button>
            <div class="logo-text">
                <span><span class="logo-brand">{{TR_brand}}</span><span class="tier-badge" id="editionBadge"></span></span>
                <span class="logo-sub">{{TR_subtitle}}</span>
            </div>
        </div>
    </div>
    <div class="header-right">
        <button class="btn header-primary-action" id="addAssetBtn">＋ <span>{{TR_add_asset}}</span></button>
        <span class="save-state-wrap"><span class="unsaved-dot" id="unsavedIndicator" title="{{TR_unsaved_changes}}">●</span></span>
        <button class="btn btn-primary header-primary-action" id="saveHTML">💾 <span>{{TR_save}}</span></button>
        <span class="header-last-updated"><span>{{TR_last_updated}}</span><strong id="lastUpdated">-</strong></span>
    </div>
</header>'''

header_views = '''<header class="header tier-header">
    <div class="header-left">
        <div class="logo">
            <button class="logo-icon logo-menu-toggle" id="featureMenuToggle" type="button"
                    aria-expanded="false" aria-controls="featureMenu" aria-label="{{TR_menu}}" title="{{TR_menu}}">📊</button>
            <div class="logo-text">
                <span><span class="logo-brand">{{TR_brand}}</span><span class="tier-badge" id="editionBadge"></span></span>
                <span class="logo-sub">{{TR_subtitle}}</span>
            </div>
        </div>
    </div>

    <nav class="header-view-switcher" id="headerViewSwitcher" aria-label="{{TR_menu_views}}">
        <button class="layout-btn header-layout-btn active" data-layout="dashboard" title="{{TR_layout_dashboard}}" aria-label="{{TR_layout_dashboard}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="6" height="6" rx="1"/><rect x="9" y="1" width="6" height="6" rx="1"/><rect x="1" y="9" width="6" height="6" rx="1"/><rect x="9" y="9" width="6" height="6" rx="1"/></svg>
        </button>
        <!--__TIER_GE:family-->
        <button class="layout-btn header-layout-btn" data-layout="table" title="{{TR_layout_table}}" aria-label="{{TR_layout_table}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="14" height="14" rx="1"/><path d="M1 5h14M1 9h14M5 1v14M9 1v14"/></svg>
        </button>
        <!--__/TIER_GE:family-->
        <button class="layout-btn header-layout-btn" data-layout="kanban" title="{{TR_layout_kanban}}" aria-label="{{TR_layout_kanban}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="4" height="14" rx="1"/><rect x="6" y="1" width="4" height="14" rx="1"/><rect x="11" y="1" width="4" height="10" rx="1"/></svg>
        </button>
        <!--__TIER_GE:family-->
        <button class="layout-btn header-layout-btn" data-layout="timeline" title="{{TR_layout_timeline}}" aria-label="{{TR_layout_timeline}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="2" fill="currentColor" stroke="none"/><path d="M2 8h4M10 8h4"/><circle cx="4" cy="8" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="8" r="1" fill="currentColor" stroke="none"/></svg>
        </button>
        <!--__/TIER_GE:family-->
        <button class="layout-btn header-layout-btn" data-layout="detail" title="{{TR_layout_detail}}" aria-label="{{TR_layout_detail}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="5" height="14" rx="1"/><rect x="7" y="1" width="8" height="8" rx="1"/><rect x="7" y="11" width="8" height="4" rx="1"/></svg>
        </button>
        <button class="layout-btn header-layout-btn" data-layout="compact" title="{{TR_layout_compact}}" aria-label="{{TR_layout_compact}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h10M3 8h10M3 12h10"/></svg>
        </button>
        <!--__TIER_GE:planning-->
        <button class="layout-btn header-layout-btn" data-layout="audit" title="{{TR_professional_audit}}" aria-label="{{TR_professional_audit}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h7v12H3V4z"/><path d="M5.5 8l2 2 3.5-4"/></svg>
        </button>
        <button class="layout-btn header-layout-btn" data-layout="review" title="{{TR_professional_review}}" aria-label="{{TR_professional_review}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 3h10v10H3z"/><path d="M5 6h6M5 9h4"/></svg>
        </button>
        <!--__/TIER_GE:planning-->
        <!--__TIER_GE:family-->
        <button class="layout-btn header-layout-btn" data-layout="charts" title="{{TR_layout_charts}}" aria-label="{{TR_layout_charts}}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 14h12"/><path d="M4 14V9M8 14V5M12 14V8"/></svg>
        </button>
        <!--__/TIER_GE:family-->
    </nav>

    <div class="header-right">
        <span class="header-last-updated"><span>{{TR_last_updated}}</span><strong id="lastUpdated">-</strong></span>
        <span class="save-state-wrap"><span class="unsaved-dot" id="unsavedIndicator" title="{{TR_unsaved_changes}}">●</span></span>
        <button class="btn btn-primary header-primary-action" id="saveHTML">💾 <span>{{TR_save}}</span></button>
    </div>
</header>'''
html = replace_once(html, old_header, header_views, 'header replacement')

# Views now have a dedicated, always-visible central header surface. Remove the duplicate menu section.
menu_start = html.find('    <div class="menu-section menu-views-section">')
menu_end_marker = '    <!--__TIER_GE:family-->\n    <div class="menu-section" data-min-tier="family">'
menu_end = html.find(menu_end_marker, menu_start)
if menu_start < 0 or menu_end < 0:
    raise SystemExit('menu views anchors not found')
html = html[:menu_start] + html[menu_end:]

# Assets card: Add first, With Value subline beneath it; both right aligned.
old_assets_controls = '''                    <div class="stat-subline"><span><strong id="withValueCount">0</strong> {{TR_with_value}}</span></div>
                    <button class="stat-add-btn" id="statAddAssetBtn" type="button">＋ {{TR_add_asset}}</button>'''
new_assets_controls = '''                    <button class="stat-add-btn" id="statAddAssetBtn" type="button">＋ {{TR_add_asset}}</button>
                    <div class="stat-subline"><span><strong id="withValueCount">0</strong> {{TR_with_value}}</span></div>'''
html = replace_once(html, old_assets_controls, new_assets_controls, 'Assets card action order')

# The only Add Asset entry point is now the Assets summary card.
html = replace_once(html,
    "function initWizard() {\n    document.getElementById('addAssetBtn').addEventListener('click', openWizard);\n    const statAdd = document.getElementById('statAddAssetBtn');",
    "function initWizard() {\n    const statAdd = document.getElementById('statAddAssetBtn');",
    'remove header add listener')

# Latest chrome/filter rules intentionally override the earlier responsive rules.
css = r'''

/* ===== CENTERED HEADER VIEWS + SINGLE-LINE FILTER BAR ===== */
.tier-header { position: sticky; }
.header-view-switcher {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    max-width: calc(100% - 430px);
    padding: 3px;
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-width: none;
    white-space: nowrap;
}
.header-view-switcher::-webkit-scrollbar { display: none; }
.header-layout-btn {
    width: 34px;
    height: 34px;
    flex: 0 0 34px;
    padding: 0;
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
}
.header-layout-btn svg { width: 17px; height: 17px; display: block; }
.header-layout-btn:hover { color: var(--text); background: var(--surface); border-color: var(--border); }
.header-layout-btn.active { color: var(--accent); background: var(--accent-light); border-color: var(--accent); }
.header-right { margin-left: auto; }
.stat-card-assets .stat-content { align-items: stretch; }
.stat-card-assets .stat-add-btn,
.stat-card-assets .stat-subline { align-self: flex-end; text-align: right; }
.stat-card-assets .stat-add-btn { margin-top: 8px; }
.stat-card-assets .stat-subline { width: 100%; margin-top: 4px; }

.filter-bar {
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 8px;
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-width: thin;
}
.filter-search { flex: 1 1 220px; min-width: 180px; max-width: 300px; }
.quick-scope-filters { flex: 0 0 auto; width: auto !important; flex-wrap: nowrap !important; }
.filter-group { flex: 0 0 auto; }
.filter-select { min-width: 118px; max-width: 150px; }
.filter-result-count { flex: 0 0 auto; }
.filter-status-toggles {
    flex: 0 0 auto;
    width: auto !important;
    margin-left: auto !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    justify-content: flex-end;
}
.filter-status-toggles .status-toggle-btn { flex: 0 0 auto; white-space: nowrap; min-height: 0; }

@media (max-width: 980px) {
    .tier-header { padding-left: 16px; padding-right: 16px; flex-wrap: nowrap; }
    .header-view-switcher { max-width: calc(100% - 330px); }
}
@media (max-width: 680px) {
    .tier-header { height: 64px; padding: 0 10px; flex-wrap: nowrap; }
    .tier-header .logo-text { display: none; }
    .tier-header .header-right { width: auto; display: flex; grid-template-columns: none; gap: 5px; }
    .tier-header .header-right .btn { width: auto; min-height: 40px; flex: 0 0 auto; padding: 7px 9px; }
    .header-last-updated { grid-column: auto; justify-self: auto; font-size: 9px; }
    .header-last-updated > span { display: none; }
    .header-view-switcher { max-width: calc(100% - 185px); gap: 2px; }
    .header-layout-btn { width: 30px; height: 30px; flex-basis: 30px; }
    .header-layout-btn svg { width: 15px; height: 15px; }
    .filter-search { flex-basis: 220px; min-width: 180px; }
    .filter-status-toggles { display: flex !important; grid-template-columns: none !important; }
}
'''
html = replace_once(html, '</style>\n</head>', css + '\n</style>\n</head>', 'append centered header CSS')
TPL.write_text(html, encoding='utf-8')

# Tests now treat the centered header as the canonical view switcher.
test = TEST.read_text(encoding='utf-8')
test = test.replace(
    "                    available = page.locator(f'.menu-layout-item[data-layout=\"{feat}\"]').count() > 0",
    "                    available = page.locator(f'.header-layout-btn[data-layout=\"{feat}\"]').count() > 0",
    1,
)
test = test.replace(
    '    check("simplified chrome compiled", all(t in en_html for t in ["logo-menu-toggle", "statAddAssetBtn", "filter-status-toggles", "menu-layout-grid"]))',
    '    check("simplified chrome compiled", all(t in en_html for t in ["logo-menu-toggle", "statAddAssetBtn", "filter-status-toggles", "header-view-switcher"]))',
    1,
)
test = test.replace(
    '    check("professional terminology retained", all(t in en_html for t in [">Audit<", ">Annual Review<", "Export MD", "Export JSON"]))',
    '    check("professional terminology retained", all(t in en_html for t in [\'aria-label="Audit"\', \'aria-label="Annual Review"\', "Export MD", "Export JSON"]))',
    1,
)

start = test.find('def responsive_ui_check():')
end = test.find('\n\ndef browser_e2e():', start)
if start < 0 or end < 0:
    raise SystemExit('responsive function anchors not found')
new_responsive = '''def responsive_ui_check():
    print("\\n== Step 2c: responsive centered header + single-line filters ==")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in ((390, 844), (768, 900), (1440, 1000)):
            ctx = browser.new_context(viewport={"width": width, "height": height})
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(EN_HTML.as_uri(), wait_until="load")
            page.wait_for_timeout(500)
            check(f"responsive {width}: header Add removed",
                  page.locator(".tier-header #addAssetBtn").count() == 0)
            check(f"responsive {width}: right side is Last Updated + Save",
                  page.locator(".tier-header #lastUpdated").count() == 1
                  and page.locator(".tier-header #saveHTML").count() == 1)
            check(f"responsive {width}: centered SVG view switcher present",
                  page.locator("#headerViewSwitcher .header-layout-btn svg").count() == 9)
            box = page.locator("#headerViewSwitcher").bounding_box()
            check(f"responsive {width}: view switcher centered in viewport",
                  bool(box and abs((box['x'] + box['width'] / 2) - width / 2) <= 3), str(box))
            check(f"responsive {width}: all filters use one nowrap bar",
                  page.locator(".filter-bar").evaluate("el => getComputedStyle(el).flexWrap") == "nowrap")
            status_boxes = page.locator(".filter-bar .status-toggle-btn").evaluate_all(
                "els => els.map(el => { const r=el.getBoundingClientRect(); return [r.top,r.bottom]; })")
            check(f"responsive {width}: status buttons do not wrap",
                  len(status_boxes) == 4 and max(b[0] for b in status_boxes) - min(b[0] for b in status_boxes) <= 2,
                  str(status_boxes))
            check(f"responsive {width}: search/category/owner/status all in filter bar",
                  page.locator(".filter-bar #searchInput").count() == 1
                  and page.locator(".filter-bar #categoryFilter").count() == 1
                  and page.locator(".filter-bar #ownerFilter").count() == 1
                  and page.locator(".filter-bar .status-toggle-btn").count() == 4)
            page.click("#featureMenuToggle")
            check(f"responsive {width}: logo menu opens", page.locator("#featureMenu.open").count() == 1)
            check(f"responsive {width}: Views removed from menu",
                  page.locator("#featureMenu .menu-layout-item").count() == 0)
            page.click("#featureMenuClose")
            check(f"responsive {width}: no JS errors", not errors, str(errors[:3]))
            ctx.close()
        browser.close()
'''
test = test[:start] + new_responsive + test[end:]

test = test.replace(
    '    page.click("#addAssetBtn")\n    page.wait_for_selector("#wizardOverlay.active", timeout=5000)',
    '    check("en: header Add Asset removed", page.locator("#addAssetBtn").count() == 0)\n    page.click("#statAddAssetBtn")\n    page.wait_for_selector("#wizardOverlay.active", timeout=5000)',
    1,
)
old_zh = '''    _open_feature_menu(page)
    menu_text = page.locator("#featureMenu").text_content()
    check("zh: Professional logo menu uses bilingual terminology",
          "Audit 财产审计" in menu_text and "Annual Review 年度复核" in menu_text)
    check("zh: Professional export section localized", "Export 导出" in menu_text)'''
new_zh = '''    header_labels = page.locator("#headerViewSwitcher .header-layout-btn").evaluate_all(
        "els => els.map(el => el.getAttribute('aria-label'))")
    check("zh: Professional header views use bilingual terminology",
          "Audit 财产审计" in header_labels and "Annual Review 年度复核" in header_labels)
    _open_feature_menu(page)
    menu_text = page.locator("#featureMenu").text_content()
    check("zh: Professional export section localized", "Export 导出" in menu_text)'''
if old_zh not in test:
    raise SystemExit('zh navigation test anchor not found')
test = test.replace(old_zh, new_zh, 1)
TEST.write_text(test, encoding='utf-8')

feature = FEATURE.read_text(encoding='utf-8')
feature = feature.replace(
    '| 2a.2 | Primary header reduced to clickable logo-menu + Add + Save + Last Updated; all other actions live in the logo menu and all search/filter controls live in one filter bar | ✅ |',
    '| 2a.2 | Header uses clickable logo-menu on the left, centered SVG View buttons, and Last Updated + Save on the right; Add Asset lives only in the Assets card | ✅ |'
)
feature = feature.replace(
    '| 2a.5 | Active / Dormant / Pending / Closed controls are directly visible and right-aligned in the unified filter bar; standalone workspace/layout-switcher chrome is removed | ✅ |',
    '| 2a.5 | Search, scope, category, owner and Active / Dormant / Pending / Closed controls stay in one non-wrapping filter-bar row; status buttons remain directly visible and right-aligned | ✅ |'
)
feature = feature.replace(
    '| 2a.7 | Clicking the top-left EstateON logo icon opens the Features menu; layout choices retain the original SVG icon set, with explicit close/focus-return behavior and bilingual Professional terminology | ✅ |',
    '| 2a.7 | Clicking the top-left EstateON logo icon opens the Features menu; all Views use the original SVG icon set centered in the Header, with bilingual Professional labels exposed through title/ARIA | ✅ |'
)
FEATURE.write_text(feature, encoding='utf-8')

print('Applied centered header Views, Assets-card-only Add, and single-line filter bar')
