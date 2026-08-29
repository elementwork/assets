#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates" / "dashboard.html"
TR = ROOT / "src" / "translations.py"
TEST = ROOT / "tests" / "e2e_visual_test.py"
FEATURE = ROOT / "docs" / "dev" / "feature_list.md"


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"{label}: anchor not found")
    return text.replace(old, new, 1)


def replace_between(text, start_marker, end_marker, new, label):
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit(f"{label}: start marker not found")
    end = text.find(end_marker, start)
    if end < 0:
        raise SystemExit(f"{label}: end marker not found")
    return text[:start] + new + text[end:]


html = TPL.read_text(encoding="utf-8")

# Remove the old standalone layout-switcher styling. Layout icons now live only in the logo menu.
html = re.sub(
    r"/\* ===== LAYOUT SWITCHER ===== \*/.*?/\* ===== TEMPLATE SWITCHER ===== \*/",
    "/* ===== TEMPLATE SWITCHER ===== */",
    html,
    count=1,
    flags=re.S,
)

# Header: logo icon is the Features/menu trigger. Top chrome keeps only Add + Save actions.
header = '''<!-- HEADER -->
<header class="header tier-header">
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
</header>

'''
menu_marker = '<div class="feature-menu" id="featureMenu" aria-hidden="true" tabindex="-1">'
html = replace_between(html, '<!-- HEADER -->', menu_marker, header, 'header/workspace replacement')

# Views menu: preserve the original SVG icon language from the old layout switcher.
views_start = '    <div class="menu-section">\n        <div class="menu-section-title">{{TR_menu_views}}</div>'
views_end = '\n\n    <!--__TIER_GE:family-->'
views = '''    <div class="menu-section menu-views-section">
        <div class="menu-section-title">{{TR_menu_views}}</div>
        <div class="menu-grid menu-layout-grid">
            <button class="menu-layout-item" data-layout="dashboard" title="{{TR_layout_dashboard}}" aria-label="{{TR_layout_dashboard}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="6" height="6" rx="1"/><rect x="9" y="1" width="6" height="6" rx="1"/><rect x="1" y="9" width="6" height="6" rx="1"/><rect x="9" y="9" width="6" height="6" rx="1"/></svg>
                <span>{{TR_layout_dashboard}}</span>
            </button>
            <!--__TIER_GE:family-->
            <button class="menu-layout-item" data-layout="table" title="{{TR_layout_table}}" aria-label="{{TR_layout_table}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="14" height="14" rx="1"/><path d="M1 5h14M1 9h14M5 1v14M9 1v14"/></svg>
                <span>{{TR_layout_table}}</span>
            </button>
            <!--__/TIER_GE:family-->
            <button class="menu-layout-item" data-layout="kanban" title="{{TR_layout_kanban}}" aria-label="{{TR_layout_kanban}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="4" height="14" rx="1"/><rect x="6" y="1" width="4" height="14" rx="1"/><rect x="11" y="1" width="4" height="10" rx="1"/></svg>
                <span>{{TR_layout_kanban}}</span>
            </button>
            <!--__TIER_GE:family-->
            <button class="menu-layout-item" data-layout="timeline" title="{{TR_layout_timeline}}" aria-label="{{TR_layout_timeline}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="2" fill="currentColor" stroke="none"/><path d="M2 8h4M10 8h4"/><circle cx="4" cy="8" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="8" r="1" fill="currentColor" stroke="none"/></svg>
                <span>{{TR_layout_timeline}}</span>
            </button>
            <!--__/TIER_GE:family-->
            <button class="menu-layout-item" data-layout="detail" title="{{TR_layout_detail}}" aria-label="{{TR_layout_detail}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="5" height="14" rx="1"/><rect x="7" y="1" width="8" height="8" rx="1"/><rect x="7" y="11" width="8" height="4" rx="1"/></svg>
                <span>{{TR_layout_detail}}</span>
            </button>
            <button class="menu-layout-item" data-layout="compact" title="{{TR_layout_compact}}" aria-label="{{TR_layout_compact}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h10M3 8h10M3 12h10"/></svg>
                <span>{{TR_layout_compact}}</span>
            </button>
            <!--__TIER_GE:planning-->
            <button class="menu-layout-item" data-layout="audit" title="{{TR_professional_audit}}" aria-label="{{TR_professional_audit}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h7v12H3V4z"/><path d="M5.5 8l2 2 3.5-4"/></svg>
                <span>{{TR_professional_audit}}</span>
            </button>
            <button class="menu-layout-item" data-layout="review" title="{{TR_professional_review}}" aria-label="{{TR_professional_review}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 3h10v10H3z"/><path d="M5 6h6M5 9h4"/></svg>
                <span>{{TR_professional_review}}</span>
            </button>
            <!--__/TIER_GE:planning-->
            <!--__TIER_GE:family-->
            <button class="menu-layout-item" data-layout="charts" title="{{TR_layout_charts}}" aria-label="{{TR_layout_charts}}">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 14h12"/><path d="M4 14V9M8 14V5M12 14V8"/></svg>
                <span>{{TR_layout_charts}}</span>
            </button>
            <!--__/TIER_GE:family-->
        </div>
    </div>'''
start = html.find(views_start, html.find(menu_marker))
if start < 0:
    raise SystemExit('views menu start not found')
end = html.find(views_end, start)
if end < 0:
    raise SystemExit('views menu end not found')
html = html[:start] + views + html[end:]

# Print is an action and belongs in the menu (Family+), not the header.
old_family_tools = '''    <div class="menu-section" data-min-tier="family">
        <div class="menu-section-title">{{TR_menu_family_tools}}</div>
        <div class="menu-note">✓ {{TR_print_emergency_guide}} · {{TR_print_master_index}} · {{TR_print_cover_title}}</div>
    </div>'''
new_family_tools = '''    <div class="menu-section" data-min-tier="family">
        <div class="menu-section-title">{{TR_menu_family_tools}}</div>
        <button class="menu-action" id="printBtn">🖨 {{TR_print}}</button>
        <div class="menu-note">✓ {{TR_print_emergency_guide}} · {{TR_print_master_index}} · {{TR_print_cover_title}}</div>
    </div>'''
html = replace_once(html, old_family_tools, new_family_tools, 'move print into menu')

# Summary cards + a single canonical filter bar.
summary_start = '    <!-- SUMMARY STATS -->'
summary_end = '    <!-- MAIN CONTENT -->'
summary = '''    <!-- SUMMARY STATS -->
    <section class="summary-section">
        <div class="primary-stats">
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalAssets">0</div>
                    <div class="stat-label">{{TR_asset_types}}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏷️</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalCategories">0</div>
                    <div class="stat-label">{{TR_categories}}</div>
                </div>
            </div>
            <div class="stat-card stat-card-assets">
                <div class="stat-icon">🗂️</div>
                <div class="stat-content">
                    <div class="stat-value" id="assetCount">0</div>
                    <div class="stat-label">{{TR_assets}}</div>
                    <div class="stat-subline"><span><strong id="withValueCount">0</strong> {{TR_with_value}}</span></div>
                    <button class="stat-add-btn" id="statAddAssetBtn" type="button">＋ {{TR_add_asset}}</button>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalFMV">$0</div>
                    <div class="stat-label">{{TR_total_fmv}}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalIncome">$0</div>
                    <div class="stat-label">{{TR_annual_income}}</div>
                </div>
            </div>
        </div>
    </section>

    <!-- FILTER BAR: all search/filter controls live here -->
    <div class="filter-bar">
        <div class="filter-search">
            <input type="text" id="searchInput" placeholder="{{TR_search_placeholder}}" aria-label="{{TR_search_placeholder}}">
        </div>
        <div class="quick-scope-filters" aria-label="{{TR_quick_filters}}">
            <button class="scope-filter-btn active" data-asset-scope="all" aria-pressed="true">{{TR_filter_all}} <span class="scope-filter-count" id="scopeAllCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="value" aria-pressed="false">{{TR_filter_with_value}} <span class="scope-filter-count" id="scopeValueCount">0</span></button>
        </div>
        <div class="filter-group">
            <span class="filter-label">{{TR_category}}</span>
            <select class="filter-select" id="categoryFilter">
                <option value="">{{TR_all_categories}}</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">{{TR_owner}}</span>
            <select class="filter-select" id="ownerFilter">
                <option value="">{{TR_all_owners}}</option>
            </select>
        </div>
        <span class="filter-result-count"><strong id="showingCount">0</strong> {{TR_showing}}</span>
        <div class="status-toggles filter-status-toggles" aria-label="{{TR_status}}">
            <button class="status-toggle-btn active" data-status="Active" aria-pressed="true"><span class="status-dot active"></span> {{TR_active}} <span class="status-count" id="activeCount">0</span></button>
            <button class="status-toggle-btn active" data-status="Dormant" aria-pressed="true"><span class="status-dot dormant"></span> {{TR_dormant}} <span class="status-count" id="dormantCount">0</span></button>
            <button class="status-toggle-btn active" data-status="Pending" aria-pressed="true"><span class="status-dot pending"></span> {{TR_pending}} <span class="status-count" id="pendingCount">0</span></button>
            <button class="status-toggle-btn active" data-status="Closed" aria-pressed="true"><span class="status-dot closed"></span> {{TR_closed}} <span class="status-count" id="closedCount">0</span></button>
        </div>
    </div>

'''
html = replace_between(html, summary_start, summary_end, summary, 'summary/filter replacement')

# CSS overrides for the simplified chrome, left-anchored menu, five-card summary and unified filter bar.
css = r'''

/* ===== SIMPLIFIED PRODUCT CHROME / LOGO MENU ===== */
.logo-menu-toggle {
    border: 0;
    padding: 0;
    font: inherit;
    cursor: pointer;
    box-shadow: none;
}
.logo-menu-toggle:hover,
.logo-menu-toggle:focus-visible {
    background: var(--accent-hover);
    outline: none;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent);
}
.header-last-updated {
    display: inline-flex;
    align-items: baseline;
    gap: 5px;
    padding-left: 2px;
    color: var(--muted);
    font-size: 10px;
    white-space: nowrap;
}
.header-last-updated strong { color: var(--text-secondary); font-weight: 650; }
.feature-menu { left: 24px; right: auto; }
.menu-layout-grid { grid-template-columns: 1fr 1fr; }
.menu-layout-item svg { width: 16px; height: 16px; flex: 0 0 16px; }
.menu-layout-item span { min-width: 0; }
.primary-stats { grid-template-columns: repeat(5, minmax(0, 1fr)); }
.stat-card-assets .stat-content { display: flex; flex-direction: column; align-items: flex-start; }
.stat-add-btn {
    margin-top: 9px;
    padding: 5px 9px;
    border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--border));
    border-radius: var(--radius-sm);
    background: var(--accent-light);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
}
.stat-add-btn:hover { background: var(--accent); color: white; }
.filter-search { position: relative; flex: 1 1 250px; min-width: 210px; }
.filter-search input {
    width: 100%;
    padding: 8px 12px 8px 36px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--surface);
    color: var(--text);
    font-size: 13px;
}
.filter-search::before {
    content: "🔍";
    position: absolute;
    left: 11px;
    top: 50%;
    transform: translateY(-50%);
    opacity: .6;
    font-size: 12px;
    pointer-events: none;
}
.filter-search input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(13,148,136,.12); }
.filter-result-count { color: var(--muted); font-size: 11px; white-space: nowrap; }
.filter-result-count strong { color: var(--text-secondary); }
.filter-status-toggles { margin-left: auto; justify-content: flex-end; flex-wrap: wrap; }
.status-count { min-width: 1.25em; text-align: center; font-variant-numeric: tabular-nums; opacity: .72; }

@media (max-width: 1180px) {
    .primary-stats { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
    .primary-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .filter-search { flex-basis: 100%; min-width: 100%; }
    .filter-status-toggles { width: 100%; margin-left: 0; justify-content: flex-end; }
    .feature-menu { left: 8px; right: 8px; width: auto; }
}
@media (max-width: 680px) {
    .tier-header .header-right { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .tier-header .header-right .btn { width: 100%; min-height: 44px; justify-content: center; }
    .header-last-updated { grid-column: 1 / -1; justify-self: end; }
    .filter-status-toggles .status-toggle-btn { min-height: 40px; }
}
@media (max-width: 460px) {
    .primary-stats { grid-template-columns: 1fr; }
    .filter-status-toggles { display: grid; grid-template-columns: 1fr 1fr; }
    .filter-status-toggles .status-toggle-btn { justify-content: flex-start; }
}
'''
html = replace_once(html, '</style>\n</head>', css + '\n</style>\n</head>', 'append IA CSS')

# Durable distinction between the catalog/type library and user-recorded assets.
old_value_block = "const VALUE_FIELDS = ['fmv','fmv_usd','market_value','current_balance','equity'];\n\nfunction hasFinancialValue(asset) {\n    return VALUE_FIELDS.some(k => Number(asset && asset[k]) > 0);\n}\n"
new_value_block = "const VALUE_FIELDS = ['fmv','fmv_usd','market_value','current_balance','equity'];\nconst RECORDED_SOURCES = new Set(['quick-add', 'manual-add', 'duplicate', 'user-edit', 'demo', 'import']);\nconst RECORD_SIGNAL_FIELDS = ['account_number','owner','joint_owner','primary_beneficiary','insurance_policy','document_reference','access_location','access_recovery_contact'];\n\nfunction hasFinancialValue(asset) {\n    return VALUE_FIELDS.some(k => Number(asset && asset[k]) > 0);\n}\n\nfunction isRecordedAsset(asset) {\n    if (!asset) return false;\n    if (asset.last_modified_by === 'user' || RECORDED_SOURCES.has(asset.source || '')) return true;\n    if (hasFinancialValue(asset)) return true;\n    return RECORD_SIGNAL_FIELDS.some(k => String(asset[k] || '').trim() !== '');\n}\n\nfunction touchAsset(asset, source = 'user-edit') {\n    if (!asset) return;\n    asset.last_modified_by = 'user';\n    asset.last_update = new Date().toISOString().slice(0, 10);\n    if (!asset.source) asset.source = source;\n}\n"
html = replace_once(html, old_value_block, new_value_block, 'recorded asset helpers')

old_stats = '''function updateStats() {
    const filtered = getFilteredAssets();
    const withValue = assets.filter(hasFinancialValue).length;
    const totalFMV = filtered.reduce((sum, a) => sum + (parseFloat(a.fmv) || 0), 0);
    const totalIncome = filtered.reduce((sum, a) => sum + (parseFloat(a.annual_income) || 0), 0);
    const statusCounts = { Active: 0, Dormant: 0, Pending: 0, Closed: 0 };
    filtered.forEach(a => { statusCounts[a.status || 'Active'] = (statusCounts[a.status || 'Active'] || 0) + 1; });

    document.getElementById('totalAssets').textContent = assets.length.toLocaleString(LOCALE);
    const showingEl = document.getElementById('showingCount');
    const valEl = document.getElementById('withValueCount');
    const allChip = document.getElementById('scopeAllCount');
    const valChip = document.getElementById('scopeValueCount');
    if (showingEl) showingEl.textContent = filtered.length.toLocaleString(LOCALE);
    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);
    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);
    if (valChip) valChip.textContent = withValue.toLocaleString(LOCALE);

    document.getElementById('totalFMV').textContent = formatCurrency(totalFMV);
    document.getElementById('totalIncome').textContent = formatCurrency(totalIncome);
    document.getElementById('totalCategories').textContent = Object.keys(groupBy(filtered, 'category')).length;
    document.getElementById('activeCount').textContent = statusCounts.Active || 0;
    document.getElementById('dormantCount').textContent = statusCounts.Dormant || 0;
    document.getElementById('pendingCount').textContent = statusCounts.Pending || 0;
    document.getElementById('closedCount').textContent = statusCounts.Closed || 0;
    const dates = filtered.map(a => a.last_update).filter(Boolean).sort();
    document.getElementById('lastUpdated').textContent = dates.length ? dates[dates.length - 1] : '-';
}'''
new_stats = '''function updateStats() {
    const filtered = getFilteredAssets();
    const withValue = assets.filter(hasFinancialValue).length;
    const recordedAssets = assets.filter(isRecordedAsset).length;
    const totalFMV = filtered.reduce((sum, a) => sum + (parseFloat(a.fmv) || 0), 0);
    const totalIncome = filtered.reduce((sum, a) => sum + (parseFloat(a.annual_income) || 0), 0);
    const statusCounts = { Active: 0, Dormant: 0, Pending: 0, Closed: 0 };
    filtered.forEach(a => { statusCounts[a.status || 'Active'] = (statusCounts[a.status || 'Active'] || 0) + 1; });

    document.getElementById('totalAssets').textContent = ASSETS_DATA.length.toLocaleString(LOCALE);
    document.getElementById('totalCategories').textContent = Object.keys(CATEGORIES_DATA).length.toLocaleString(LOCALE);
    document.getElementById('assetCount').textContent = recordedAssets.toLocaleString(LOCALE);
    const showingEl = document.getElementById('showingCount');
    const valEl = document.getElementById('withValueCount');
    const allChip = document.getElementById('scopeAllCount');
    const valChip = document.getElementById('scopeValueCount');
    if (showingEl) showingEl.textContent = filtered.length.toLocaleString(LOCALE);
    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);
    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);
    if (valChip) valChip.textContent = withValue.toLocaleString(LOCALE);

    document.getElementById('totalFMV').textContent = formatCurrency(totalFMV);
    document.getElementById('totalIncome').textContent = formatCurrency(totalIncome);
    document.getElementById('activeCount').textContent = statusCounts.Active || 0;
    document.getElementById('dormantCount').textContent = statusCounts.Dormant || 0;
    document.getElementById('pendingCount').textContent = statusCounts.Pending || 0;
    document.getElementById('closedCount').textContent = statusCounts.Closed || 0;
    const dates = assets.map(a => a.last_update).filter(Boolean).sort();
    document.getElementById('lastUpdated').textContent = dates.length ? dates[dates.length - 1] : '-';
}'''
html = replace_once(html, old_stats, new_stats, 'updateStats')

# Both Add Asset entry points open the same wizard.
old_init_wizard = "function initWizard() {\n    document.getElementById('addAssetBtn').addEventListener('click', openWizard);"
new_init_wizard = "function initWizard() {\n    document.getElementById('addAssetBtn').addEventListener('click', openWizard);\n    const statAdd = document.getElementById('statAddAssetBtn');\n    if (statAdd) statAdd.addEventListener('click', openWizard);"
html = replace_once(html, old_init_wizard, new_init_wizard, 'stat Add Asset listener')

# Make user edits durable signals for the Assets card and Last Updated header value.
html = replace_once(html,
    "    if (isNew) assets.push(currentAsset);\n    saveToLocalStorage();",
    "    touchAsset(currentAsset, isNew ? 'manual-add' : 'user-edit');\n    if (isNew) assets.push(currentAsset);\n    saveToLocalStorage();",
    'modal edit touch')
html = replace_once(html,
    "        asset[field] = value;\n    }\n    saveToLocalStorage();",
    "        asset[field] = value;\n        touchAsset(asset, 'user-edit');\n    }\n    saveToLocalStorage();",
    'bulk edit touch')
html = replace_once(html,
    "            asset[field] = value;\n            saveToLocalStorage();",
    "            asset[field] = value;\n            touchAsset(asset, 'user-edit');\n            saveToLocalStorage();",
    'inline edit touch')
html = replace_once(html,
    "        asset.status = status;\n        saveToLocalStorage();",
    "        asset.status = status;\n        touchAsset(asset, 'user-edit');\n        saveToLocalStorage();",
    'kanban touch')
html = replace_once(html,
    "    copy.security_questions = '';\n    showAssetModal(copy);",
    "    copy.security_questions = '';\n    copy.source = 'duplicate';\n    copy.last_modified_by = 'user';\n    showAssetModal(copy);",
    'duplicate recorded source')

TPL.write_text(html, encoding="utf-8")

# Translation: Asset Types is a product-library concept distinct from Assets.
tr = TR.read_text(encoding="utf-8")
tr = replace_once(tr, '        "asset_catalog": "Asset Catalog",\n', '        "asset_catalog": "Asset Catalog",\n        "asset_types": "Asset Types",\n', 'en asset_types')
tr = replace_once(tr, '        "asset_catalog": "资产目录",\n', '        "asset_catalog": "资产目录",\n        "asset_types": "资产类型",\n', 'zh asset_types')
TR.write_text(tr, encoding="utf-8")

# Tests: replace old workspace geometry checks with the new single-menu IA checks.
test = TEST.read_text(encoding="utf-8")
start = test.find('def responsive_ui_check():')
end = test.find('\n\ndef browser_e2e():', start)
if start < 0 or end < 0:
    raise SystemExit('responsive_ui_check anchors not found')
new_responsive = '''def responsive_ui_check():
    print("\\n== Step 2c: responsive simplified chrome ==")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in ((390, 844), (768, 900), (1440, 1000)):
            ctx = browser.new_context(viewport={"width": width, "height": height})
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(EN_HTML.as_uri(), wait_until="load")
            page.wait_for_timeout(500)
            check(f"responsive {width}: no standalone workspace/layout switcher",
                  page.locator(".workspace-bar").count() == 0 and page.locator(".layout-switcher").count() == 0)
            check(f"responsive {width}: logo icon is menu trigger",
                  page.locator("#featureMenuToggle.logo-icon").count() == 1)
            check(f"responsive {width}: top actions are Add + Save only",
                  page.locator(".tier-header #addAssetBtn").count() == 1
                  and page.locator(".tier-header #saveHTML").count() == 1
                  and page.locator(".tier-header #printBtn").count() == 0)
            check(f"responsive {width}: Last Updated sits in header",
                  page.locator(".tier-header #lastUpdated").count() == 1)
            check(f"responsive {width}: search is in filter bar",
                  page.locator(".filter-bar #searchInput").count() == 1)
            check(f"responsive {width}: four status buttons are directly visible",
                  page.locator(".filter-bar .status-toggle-btn").count() == 4
                  and page.locator(".filter-bar .status-toggle-btn:visible").count() == 4)
            page.click("#featureMenuToggle")
            check(f"responsive {width}: logo menu opens", page.locator("#featureMenu.open").count() == 1)
            check(f"responsive {width}: legacy SVG layout icons retained",
                  page.locator("#featureMenu .menu-layout-item svg").count() >= 9)
            menu_box = page.locator("#featureMenu").bounding_box()
            check(f"responsive {width}: menu is left anchored",
                  bool(menu_box and menu_box['x'] <= (12 if width <= 760 else 32)), str(menu_box))
            page.click("#featureMenuClose")
            check(f"responsive {width}: no JS errors", not errors, str(errors[:3]))
            ctx.close()
        browser.close()
'''
test = test[:start] + new_responsive + test[end:]

test = test.replace(
    '    check("dynamic header geometry compiled", "ResizeObserver" in en_html and "--app-header-height" in en_html)\n',
    '    check("simplified chrome compiled", all(t in en_html for t in ["logo-menu-toggle", "statAddAssetBtn", "filter-status-toggles", "menu-layout-grid"]))\n    check("standalone workspace/layout switcher removed", \'<div class="workspace-bar"\' not in en_html and \'<div class="layout-switcher"\' not in en_html)\n'
)
test = test.replace(
    '    check("en: Asset Catalog label", "Asset Catalog" in page.locator(".stat-card").first.text_content())\n',
    '    check("en: Asset Types label", "Asset Types" in page.locator(".stat-card").first.text_content())\n    check("en: blank catalog starts with zero recorded Assets", page.text_content("#assetCount") == "0", page.text_content("#assetCount"))\n    check("en: stat card order is Asset Types / Categories / Assets", [x.strip() for x in page.locator(".primary-stats .stat-label").all_text_contents()[:3]] == ["Asset Types", "Categories", "Assets"])\n'
)
test = test.replace(
    '    page.click("#printBtn")\n    page.wait_for_timeout(400)\n',
    '    _menu_click(page, "#printBtn")\n    page.wait_for_timeout(400)\n',
    1,
)
test = test.replace(
    '    check("en: print media hides workspace chrome", page.evaluate("getComputedStyle(document.querySelector(\'.workspace-bar\')).display") == "none")\n',
    '    check("en: print media has no standalone workspace chrome", page.locator(".workspace-bar").count() == 0)\n'
)
# After quick-add, the Assets card must reflect a real recorded asset.
test = test.replace(
    '    check("en: wizard creates asset",\n          page.evaluate("assets.some(a => a.source === \'quick-add\')"))\n',
    '    check("en: wizard creates asset",\n          page.evaluate("assets.some(a => a.source === \'quick-add\')"))\n    check("en: Assets card increments after quick-add", int(page.text_content("#assetCount")) >= 1, page.text_content("#assetCount"))\n'
)
TEST.write_text(test, encoding="utf-8")

# Feature documentation follows the new information architecture.
feature = FEATURE.read_text(encoding="utf-8")
feature = feature.replace(
    '| 2a.2 | Primary header reduced to Search + Add + Print (paid) + Save + Features; secondary controls grouped in the Features menu | ✅ |',
    '| 2a.2 | Primary header reduced to clickable logo-menu + Add + Save + Last Updated; all other actions live in the logo menu and all search/filter controls live in one filter bar | ✅ |'
)
feature = feature.replace(
    '| 2a.4 | Asset Catalog card distinguishes global catalog size, current Showing count, and With Value count; one-click All / With Value scope filters apply across layouts | ✅ |',
    '| 2a.4 | Summary separates Asset Types, Categories and recorded Assets; Assets card includes Add Asset and With Value context; All / With Value remain quick filters | ✅ |'
)
feature = feature.replace(
    '| 2a.5 | Status controls collapsed into an accessible dropdown; workspace uses measured sticky geometry and becomes non-sticky on narrow mobile screens | ✅ |',
    '| 2a.5 | Active / Dormant / Pending / Closed controls are directly visible and right-aligned in the unified filter bar; standalone workspace/layout-switcher chrome is removed | ✅ |'
)
feature = feature.replace(
    '| 2a.7 | Feature menu has explicit close/focus-return behavior and Professional zh labels retain bilingual professional terminology | ✅ |',
    '| 2a.7 | Clicking the top-left EstateON logo icon opens the Features menu; layout choices retain the original SVG icon set, with explicit close/focus-return behavior and bilingual Professional terminology | ✅ |'
)
FEATURE.write_text(feature, encoding="utf-8")

print('Applied simplified logo-menu/header/filter refactor')
