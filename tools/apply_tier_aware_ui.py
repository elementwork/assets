#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates" / "dashboard.html"
TR = ROOT / "src" / "translations.py"
TEST = ROOT / "tests" / "e2e_visual_test.py"
FEATURE = ROOT / "docs" / "dev" / "feature_list.md"
VERSION = ROOT / "docs" / "dev" / "versioning_plan.md"


def sub1(text, pattern, repl, flags=0, label="replacement"):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {n}")
    return out


def replace1(text, old, new, label="replacement"):
    if old not in text:
        raise SystemExit(f"{label}: anchor not found")
    return text.replace(old, new, 1)


# -----------------------------------------------------------------------------
# Dashboard template
# -----------------------------------------------------------------------------
s = TPL.read_text(encoding="utf-8")

css = r'''

/* ===== TIER-AWARE PRODUCT NAVIGATION ===== */
.tier-header {
    min-height: 68px;
    height: auto;
    gap: 18px;
}
.tier-header .header-left { min-width: 190px; }
.tier-header .header-search { flex: 1 1 340px; max-width: 680px; }
.tier-header .header-right { gap: 8px; }
.tier-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-left: 8px;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 10px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: .06em;
    text-transform: uppercase;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--muted);
    vertical-align: middle;
}
html[data-edition="family"] .tier-badge {
    color: var(--accent);
    border-color: color-mix(in srgb, var(--accent) 35%, var(--border));
    background: var(--accent-light);
}
html[data-edition="planning"] .tier-badge {
    color: var(--card);
    background: var(--primary);
    border-color: var(--primary);
}
.save-state-wrap { display:flex; align-items:center; gap:5px; min-width:10px; }
.header-primary-action { white-space: nowrap; }
.menu-toggle { min-width: 86px; }

.workspace-bar {
    display:flex;
    align-items:center;
    gap:10px;
    min-height:48px;
    padding:7px 32px;
    background:var(--card);
    border-bottom:1px solid var(--border);
    position:sticky;
    top:68px;
    z-index:90;
}
.workspace-set {
    display:flex;
    align-items:center;
    gap:5px;
    min-width:0;
    overflow-x:auto;
    scrollbar-width:none;
}
.workspace-set::-webkit-scrollbar { display:none; }
.workspace-btn.layout-btn {
    width:auto;
    height:34px;
    padding:0 12px;
    border-radius:999px;
    gap:6px;
    font-size:12px;
    font-weight:650;
    white-space:nowrap;
}
.workspace-btn.layout-btn svg { width:14px; height:14px; }
.workspace-upgrade {
    margin-left:auto;
    border:1px dashed color-mix(in srgb, var(--accent) 48%, var(--border));
    color:var(--text-secondary);
    background:var(--accent-light);
    border-radius:999px;
    padding:7px 12px;
    font-size:11px;
    font-weight:650;
    white-space:nowrap;
    cursor:pointer;
}
.workspace-upgrade:hover { border-style:solid; color:var(--accent); }

.feature-menu {
    display:none;
    position:fixed;
    top:66px;
    right:24px;
    width:min(380px, calc(100vw - 28px));
    max-height:calc(100vh - 82px);
    overflow:auto;
    z-index:220;
    padding:12px;
    border:1px solid var(--border);
    border-radius:var(--radius-lg);
    background:var(--card);
    box-shadow:var(--shadow-lg);
}
.feature-menu.open { display:block; }
.menu-section { padding:8px 4px 12px; border-bottom:1px solid var(--border-light); }
.menu-section:last-child { border-bottom:0; }
.menu-section-title {
    padding:0 7px 6px;
    color:var(--muted);
    font-size:10px;
    font-weight:800;
    letter-spacing:.08em;
    text-transform:uppercase;
}
.menu-grid { display:grid; grid-template-columns:1fr 1fr; gap:5px; }
.menu-action, .menu-layout-item {
    width:100%;
    display:flex;
    align-items:center;
    gap:8px;
    min-height:36px;
    padding:7px 9px;
    text-align:left;
    border:1px solid transparent;
    border-radius:var(--radius-sm);
    background:transparent;
    color:var(--text);
    font:inherit;
    font-size:12px;
    cursor:pointer;
}
.menu-action:hover, .menu-layout-item:hover { background:var(--surface); border-color:var(--border-light); }
.menu-layout-item.active { background:var(--accent-light); color:var(--accent); }
.menu-inline { display:flex; align-items:center; gap:8px; padding:4px 8px; }
.menu-inline .template-select { flex:1; min-width:0; }
.menu-note {
    margin:4px 7px;
    padding:9px 10px;
    border-radius:var(--radius-sm);
    background:var(--surface);
    color:var(--text-secondary);
    font-size:11px;
    line-height:1.45;
}
.upgrade-preview {
    display:none;
    margin:8px 4px 0;
    padding:12px;
    border:1px solid color-mix(in srgb, var(--accent) 34%, var(--border));
    border-radius:var(--radius);
    background:linear-gradient(135deg, var(--accent-light), var(--card));
}
.upgrade-preview.visible { display:block; }
.upgrade-title { display:flex; align-items:center; justify-content:space-between; gap:8px; font-weight:750; font-size:13px; }
.upgrade-tier-tag { font-size:9px; border-radius:999px; padding:3px 7px; background:var(--card); border:1px solid var(--border); color:var(--muted); }
.upgrade-desc { margin-top:6px; color:var(--text-secondary); font-size:11px; line-height:1.45; }

.stat-card:first-child .stat-content { min-width:0; }
.stat-subline { display:flex; flex-wrap:wrap; gap:4px 10px; margin-top:5px; font-size:11px; color:var(--muted); }
.stat-link {
    border:0;
    padding:0;
    background:transparent;
    color:inherit;
    font:inherit;
    cursor:pointer;
}
.stat-link:hover { color:var(--accent); text-decoration:underline; }
.stat-link strong { color:var(--text-secondary); }
.quick-scope-filters { display:flex; align-items:center; gap:6px; flex-wrap:wrap; }
.scope-filter-btn {
    display:inline-flex;
    align-items:center;
    gap:5px;
    border:1px solid var(--border);
    background:var(--card);
    color:var(--text-secondary);
    border-radius:999px;
    padding:6px 10px;
    font-size:11px;
    font-weight:650;
    cursor:pointer;
}
.scope-filter-btn.active { background:var(--primary); color:var(--card); border-color:var(--primary); }
.scope-filter-count { opacity:.78; font-variant-numeric:tabular-nums; }
.filter-divider { width:1px; align-self:stretch; min-height:28px; background:var(--border); margin:0 2px; }
.status-filter-details { position:relative; }
.status-filter-details > summary {
    list-style:none;
    cursor:pointer;
    border:1px solid var(--border);
    border-radius:var(--radius-sm);
    background:var(--card);
    padding:7px 10px;
    font-size:12px;
    color:var(--text-secondary);
}
.status-filter-details > summary::-webkit-details-marker { display:none; }
.status-filter-popover {
    position:absolute;
    top:calc(100% + 5px);
    right:0;
    min-width:150px;
    padding:6px;
    border:1px solid var(--border);
    border-radius:var(--radius);
    background:var(--card);
    box-shadow:var(--shadow-md);
    z-index:80;
}
.status-filter-popover .status-toggle-btn { width:100%; justify-content:flex-start; margin:1px 0; }

@media (max-width: 980px) {
    .tier-header { padding:10px 16px; flex-wrap:wrap; }
    .tier-header .header-left { min-width:auto; }
    .tier-header .header-search { order:3; flex-basis:100%; max-width:none; }
    .tier-header .header-right { margin-left:auto; }
    .workspace-bar { top:116px; padding:6px 16px; }
    .workspace-upgrade { display:none; }
    .header-primary-action .btn-label-optional { display:none; }
}
@media (max-width: 680px) {
    .logo-sub { display:none; }
    .tier-header .header-right { width:100%; justify-content:space-between; }
    .tier-header .header-right .btn { flex:1; justify-content:center; padding-left:8px; padding-right:8px; }
    .workspace-bar { top:126px; overflow-x:auto; }
    .filter-bar { align-items:flex-start; }
    .quick-scope-filters { width:100%; overflow-x:auto; flex-wrap:nowrap; padding-bottom:2px; }
    .filter-divider { display:none; }
    .feature-menu { top:8px; right:8px; width:calc(100vw - 16px); max-height:calc(100vh - 16px); }
    .menu-grid { grid-template-columns:1fr; }
}
'''
if "/* ===== TIER-AWARE PRODUCT NAVIGATION ===== */" not in s:
    s = replace1(s, "</style>\n</head>", css + "\n</style>\n</head>", "append UI CSS")

header = r'''<!-- HEADER -->
<header class="header tier-header">
    <div class="header-left">
        <div class="logo">
            <div class="logo-icon">📊</div>
            <div class="logo-text">
                <span><span class="logo-brand">{{TR_brand}}</span><span class="tier-badge" id="editionBadge"></span></span>
                <span class="logo-sub">{{TR_subtitle}}</span>
            </div>
        </div>
    </div>
    <div class="header-search">
        <input type="text" id="searchInput" placeholder="{{TR_search_placeholder}}">
    </div>
    <div class="header-right">
        <button class="btn btn-primary header-primary-action" id="addAssetBtn">＋ <span class="btn-label-optional">{{TR_add_asset}}</span></button>
        <!--__TIER_GE:family-->
        <button class="btn header-primary-action" id="printBtn">🖨 <span>{{TR_print}}</span></button>
        <!--__/TIER_GE:family-->
        <span class="save-state-wrap"><span class="unsaved-dot" id="unsavedIndicator" title="{{TR_unsaved_changes}}">●</span></span>
        <button class="btn btn-primary header-primary-action" id="saveHTML">💾 <span>{{TR_save}}</span></button>
        <button class="btn menu-toggle" id="featureMenuToggle" aria-expanded="false" aria-controls="featureMenu">☰ {{TR_menu}}</button>
    </div>
</header>

<div class="workspace-bar" id="workspaceBar">
    <div class="workspace-set" data-workspace-tier="free">
        <button class="layout-btn workspace-btn active" data-layout="dashboard">{{TR_layout_dashboard}}</button>
        <button class="layout-btn workspace-btn" data-layout="compact">{{TR_layout_compact}}</button>
        <button class="layout-btn workspace-btn" data-layout="kanban">{{TR_layout_kanban}}</button>
        <button class="layout-btn workspace-btn" data-layout="detail">{{TR_layout_detail}}</button>
    </div>
    <!--__TIER_GE:family-->
    <div class="workspace-set" data-workspace-tier="family">
        <button class="layout-btn workspace-btn active" data-layout="dashboard">{{TR_layout_dashboard}}</button>
        <button class="layout-btn workspace-btn" data-layout="table">{{TR_layout_table}}</button>
        <button class="layout-btn workspace-btn" data-layout="timeline">{{TR_layout_timeline}}</button>
        <button class="layout-btn workspace-btn" data-layout="charts">{{TR_layout_charts}}</button>
    </div>
    <!--__/TIER_GE:family-->
    <!--__TIER_GE:planning-->
    <div class="workspace-set" data-workspace-tier="planning">
        <button class="layout-btn workspace-btn active" data-layout="dashboard">Dashboard</button>
        <button class="layout-btn workspace-btn" data-layout="table">Table</button>
        <button class="layout-btn workspace-btn" data-layout="charts">Charts</button>
        <button class="layout-btn workspace-btn" data-layout="audit">Audit</button>
        <button class="layout-btn workspace-btn" data-layout="review">Annual Review</button>
    </div>
    <!--__/TIER_GE:planning-->
    <button class="workspace-upgrade" data-upgrade-trigger="free">🔒 {{TR_family_teaser}}</button>
    <button class="workspace-upgrade" data-upgrade-trigger="family">🔒 {{TR_professional_teaser}}</button>
</div>

<div class="feature-menu" id="featureMenu" aria-hidden="true">
    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_views}}</div>
        <div class="menu-grid">
            <button class="menu-layout-item" data-layout="dashboard">{{TR_layout_dashboard}}</button>
            <button class="menu-layout-item" data-layout="compact">{{TR_layout_compact}}</button>
            <button class="menu-layout-item" data-layout="kanban">{{TR_layout_kanban}}</button>
            <button class="menu-layout-item" data-layout="detail">{{TR_layout_detail}}</button>
            <!--__TIER_GE:family-->
            <button class="menu-layout-item" data-layout="table">{{TR_layout_table}}</button>
            <button class="menu-layout-item" data-layout="timeline">{{TR_layout_timeline}}</button>
            <button class="menu-layout-item" data-layout="charts">{{TR_layout_charts}}</button>
            <!--__/TIER_GE:family-->
            <!--__TIER_GE:planning-->
            <button class="menu-layout-item" data-layout="audit">Audit</button>
            <button class="menu-layout-item" data-layout="review">Annual Review</button>
            <!--__/TIER_GE:planning-->
        </div>
    </div>

    <!--__TIER_GE:family-->
    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_family_tools}}</div>
        <div class="menu-note">✓ {{TR_print_emergency_guide}} · {{TR_print_master_index}} · {{TR_print_cover_title}}</div>
    </div>
    <!--__/TIER_GE:family-->

    <!--__TIER_GE:planning-->
    <div class="menu-section">
        <div class="menu-section-title">Export</div>
        <div class="menu-grid">
            <button class="menu-action" id="exportMD">{{TR_export_md}}</button>
            <button class="menu-action" id="exportExcel">{{TR_export_excel}}</button>
            <button class="menu-action" id="exportJSON">{{TR_export_json}}</button>
        </div>
    </div>
    <!--__/TIER_GE:planning-->

    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_data}}</div>
        <button class="menu-action" id="importJSON">{{TR_import_json}}</button>
        <input type="file" id="importJSONFile" accept=".json,application/json" style="display:none">
    </div>

    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_file_security}}</div>
        <div class="menu-grid">
            <button class="menu-action" id="saveAsHTML">{{TR_save_as}}</button>
            <button class="menu-action" id="lockToggle">🔒 {{TR_lock_title}}</button>
            <button class="menu-action" id="autoSaveToggle">💾 {{TR_autosave}}</button>
        </div>
        <span class="inventory-id-chip" id="inventoryIdChip" title="{{TR_inventory_id_label}}"></span>
    </div>

    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_appearance}}</div>
        <div class="menu-inline">
            <select class="template-select" id="templateSelect" aria-label="{{TR_choose_template}}">
                <option value="estateon">{{TR_template_estateon}}</option>
                <!--__TIER_GE:family-->
                <option value="lumina">{{TR_template_lumina}}</option>
                <option value="cardinal">{{TR_template_cardinal}}</option>
                <option value="atlantic">{{TR_template_atlantic}}</option>
                <option value="monarch">{{TR_template_monarch}}</option>
                <!--__/TIER_GE:family-->
            </select>
            <button class="btn btn-icon" id="themeToggle" title="{{TR_toggle_theme}}">☾</button>
        </div>
    </div>

    <div class="upgrade-preview" data-show-editions="free" data-upgrade-panel="family">
        <div class="upgrade-title"><span>🔒 {{TR_upgrade_family}}</span><span class="upgrade-tier-tag">FAMILY</span></div>
        <div class="upgrade-desc">{{TR_upgrade_family_desc}}</div>
    </div>
    <div class="upgrade-preview" data-show-editions="free family" data-upgrade-panel="professional">
        <div class="upgrade-title"><span>🔒 {{TR_upgrade_professional}}</span><span class="upgrade-tier-tag">PROFESSIONAL</span></div>
        <div class="upgrade-desc">{{TR_upgrade_professional_desc}}</div>
    </div>

    <div class="menu-section">
        <div class="menu-section-title">{{TR_menu_help}}</div>
        <button class="menu-action" id="helpToggle">? {{TR_help}}</button>
    </div>
</div>

<!-- MAIN CONTAINER -->'''
s = sub1(s, r'<!-- HEADER -->.*?<!-- MAIN CONTAINER -->', lambda m: header, flags=re.S, label="header IA")

old_stat = '''            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalAssets">0</div>
                    <div class="stat-label">{{TR_total_assets}}</div>
                </div>
            </div>'''
new_stat = '''            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-content">
                    <div class="stat-value" id="totalAssets">0</div>
                    <div class="stat-label">{{TR_total_assets}}</div>
                    <div class="stat-subline">
                        <button class="stat-link" data-stat-scope="recorded"><strong id="recordedCount">0</strong> {{TR_recorded}}</button>
                        <button class="stat-link" data-stat-scope="value"><strong id="withValueCount">0</strong> {{TR_with_value}}</button>
                    </div>
                </div>
            </div>'''
s = replace1(s, old_stat, new_stat, "summary asset card")

old_filter = '''    <!-- FILTER BAR -->
    <div class="filter-bar">
        <div class="filter-group">'''
new_filter = '''    <!-- FILTER BAR -->
    <div class="filter-bar">
        <div class="quick-scope-filters" aria-label="{{TR_quick_filters}}">
            <button class="scope-filter-btn active" data-asset-scope="all" aria-pressed="true">{{TR_filter_all}} <span class="scope-filter-count" id="scopeAllCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="recorded" aria-pressed="false">{{TR_filter_recorded}} <span class="scope-filter-count" id="scopeRecordedCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="value" aria-pressed="false">{{TR_filter_with_value}} <span class="scope-filter-count" id="scopeValueCount">0</span></button>
        </div>
        <div class="filter-divider"></div>
        <div class="filter-group">'''
s = replace1(s, old_filter, new_filter, "quick filter insertion")

old_status = '''        <div class="status-toggles">
            <button class="status-toggle-btn active" data-status="Active">
                <span class="status-dot active"></span> {{TR_active}}
            </button>
            <button class="status-toggle-btn active" data-status="Dormant">
                <span class="status-dot dormant"></span> {{TR_dormant}}
            </button>
            <button class="status-toggle-btn active" data-status="Pending">
                <span class="status-dot pending"></span> {{TR_pending}}
            </button>
            <button class="status-toggle-btn active" data-status="Closed">
                <span class="status-dot closed"></span> {{TR_closed}}
            </button>
        </div>'''
new_status = '''        <details class="status-filter-details">
            <summary>{{TR_status}} ▾</summary>
            <div class="status-toggles status-filter-popover">
                <button class="status-toggle-btn active" data-status="Active"><span class="status-dot active"></span> {{TR_active}}</button>
                <button class="status-toggle-btn active" data-status="Dormant"><span class="status-dot dormant"></span> {{TR_dormant}}</button>
                <button class="status-toggle-btn active" data-status="Pending"><span class="status-dot pending"></span> {{TR_pending}}</button>
                <button class="status-toggle-btn active" data-status="Closed"><span class="status-dot closed"></span> {{TR_closed}}</button>
            </div>
        </details>'''
s = replace1(s, old_status, new_status, "status dropdown")

helpers = r'''
// ===== TIER-AWARE UI / ASSET SCOPE =====
let assetScopeFilter = 'all';
const RECORDED_FIELDS = [
    'owner','joint_owner','institution','branch','account_number','login_username',
    'fmv','market_value','current_balance','equity','acb','annual_income','purchase_price',
    'physical_location','safe_deposit_box','digital_wallet','exchange','online_access_url',
    'support_contact','advisor_name','advisor_contact','insurance_policy','primary_beneficiary',
    'document_path','document_reference','notes','access_location','access_recovery_contact',
    'handoff_instructions','last_access_test','next_access_review'
];
const VALUE_FIELDS = ['fmv','market_value','current_balance','equity','cash_value','purchase_price'];

function hasFinancialValue(asset) {
    return VALUE_FIELDS.some(k => Number(asset && asset[k]) > 0);
}

function isRecordedAsset(asset) {
    if (!asset) return false;
    if (asset.source === 'quick-add' || asset.source === 'demo') return true;
    return RECORDED_FIELDS.some(k => {
        const v = asset[k];
        if (v == null || v === '') return false;
        if (typeof v === 'number') return v !== 0;
        if (typeof v === 'string' && /^\s*0(?:\.0+)?\s*$/.test(v)) return false;
        return String(v).trim() !== '';
    });
}

function setAssetScope(scope) {
    assetScopeFilter = ['all','recorded','value'].includes(scope) ? scope : 'all';
    document.querySelectorAll('.scope-filter-btn').forEach(btn => {
        const active = btn.dataset.assetScope === assetScopeFilter;
        btn.classList.toggle('active', active);
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    renderCurrentLayout();
}

function editionDisplayName() {
    if (APP_TIER === 'planning') return '{{TR_edition_professional}}';
    if (APP_TIER === 'family') return '{{TR_edition_family}}';
    return '{{TR_edition_free}}';
}

function initTierUI() {
    document.documentElement.dataset.edition = APP_TIER;
    const badge = document.getElementById('editionBadge');
    if (badge) badge.textContent = editionDisplayName();
    document.querySelectorAll('[data-workspace-tier]').forEach(el => {
        el.hidden = el.dataset.workspaceTier !== APP_TIER;
    });
    document.querySelectorAll('[data-upgrade-trigger]').forEach(el => {
        el.hidden = el.dataset.upgradeTrigger !== APP_TIER || APP_TIER === 'planning';
    });
    document.querySelectorAll('.upgrade-preview[data-show-editions]').forEach(el => {
        const visible = (el.dataset.showEditions || '').split(/\s+/).includes(APP_TIER);
        el.classList.toggle('visible', visible);
    });
}

function setFeatureMenuOpen(open) {
    const menu = document.getElementById('featureMenu');
    const toggle = document.getElementById('featureMenuToggle');
    if (!menu || !toggle) return;
    menu.classList.toggle('open', !!open);
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
}

function initFeatureMenu() {
    const menu = document.getElementById('featureMenu');
    const toggle = document.getElementById('featureMenuToggle');
    if (!menu || !toggle) return;
    toggle.addEventListener('click', e => {
        e.stopPropagation();
        setFeatureMenuOpen(!menu.classList.contains('open'));
    });
    document.querySelectorAll('[data-upgrade-trigger]').forEach(btn => {
        btn.addEventListener('click', () => {
            setFeatureMenuOpen(true);
            const target = APP_TIER === 'free' ? 'family' : 'professional';
            const panel = menu.querySelector(`[data-upgrade-panel="${target}"]`);
            if (panel) panel.scrollIntoView({ block:'nearest', behavior:'smooth' });
        });
    });
    menu.addEventListener('click', e => {
        if (e.target.closest('.menu-layout-item')) setFeatureMenuOpen(false);
    });
    document.addEventListener('click', e => {
        if (menu.classList.contains('open') && !menu.contains(e.target) && !toggle.contains(e.target)) setFeatureMenuOpen(false);
    });
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && menu.classList.contains('open')) setFeatureMenuOpen(false);
    });
}

'''
if "// ===== TIER-AWARE UI / ASSET SCOPE =====" not in s:
    s = replace1(s, "// ===== INITIALIZATION =====", helpers + "// ===== INITIALIZATION =====", "JS helpers")

s = replace1(s, "    initTheme();\n    initFilters();", "    initTheme();\n    initTierUI();\n    initFeatureMenu();\n    initFilters();", "init tier UI")

s = s.replace("document.querySelectorAll('.layout-btn').forEach(btn => {", "document.querySelectorAll('.layout-btn, .menu-layout-item').forEach(btn => {")
s = s.replace("document.querySelectorAll('.layout-btn[data-layout]').forEach(btn => {", "document.querySelectorAll('.layout-btn[data-layout], .menu-layout-item[data-layout]').forEach(btn => {")

filters = r'''// ===== FILTERS =====
function initFilters() {
    const categorySelect = document.getElementById('categoryFilter');
    const ownerSelect = document.getElementById('ownerFilter');

    Object.keys(CATEGORIES_DATA).sort().forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });

    const owners = [...new Set(assets.map(a => a.owner).filter(Boolean))].sort();
    owners.forEach(owner => {
        const option = document.createElement('option');
        option.value = owner;
        option.textContent = owner;
        ownerSelect.appendChild(option);
    });

    document.getElementById('searchInput').addEventListener('input', debounce(renderCurrentLayout, 300));
    categorySelect.addEventListener('change', renderCurrentLayout);
    ownerSelect.addEventListener('change', renderCurrentLayout);
    document.querySelectorAll('.scope-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => setAssetScope(btn.dataset.assetScope));
    });
    document.querySelectorAll('[data-stat-scope]').forEach(btn => {
        btn.addEventListener('click', () => setAssetScope(btn.dataset.statScope));
    });
    document.querySelectorAll('.status-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('active');
            renderCurrentLayout();
        });
    });
}

function getFilteredAssets() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    const owner = document.getElementById('ownerFilter').value;
    const activeStatuses = [...document.querySelectorAll('.status-toggle-btn.active')].map(b => b.dataset.status);

    return assets.filter(asset => {
        const matchesSearch = !search ||
            (asset.asset_name || '').toLowerCase().includes(search) ||
            (asset.institution || '').toLowerCase().includes(search) ||
            (asset.owner || '').toLowerCase().includes(search) ||
            (asset.category || '').toLowerCase().includes(search) ||
            String(asset.id == null ? '' : asset.id).toLowerCase().includes(search);
        const matchesCategory = !category || asset.category === category;
        const matchesOwner = !owner || asset.owner === owner;
        const matchesStatus = activeStatuses.includes(asset.status || 'Active');
        const matchesScope = assetScopeFilter === 'all' ||
            (assetScopeFilter === 'recorded' && isRecordedAsset(asset)) ||
            (assetScopeFilter === 'value' && hasFinancialValue(asset));
        return matchesSearch && matchesCategory && matchesOwner && matchesStatus && matchesScope;
    });
}

'''
s = sub1(s, r'// ===== FILTERS =====.*?(?=// ===== RENDER LAYOUTS =====)', lambda m: filters, flags=re.S, label="filters")

stats = r'''// ===== STATS =====
function updateStats() {
    const filtered = getFilteredAssets();
    const recorded = assets.filter(isRecordedAsset).length;
    const withValue = assets.filter(hasFinancialValue).length;
    const totalFMV = filtered.reduce((sum, a) => sum + (parseFloat(a.fmv) || 0), 0);
    const totalIncome = filtered.reduce((sum, a) => sum + (parseFloat(a.annual_income) || 0), 0);
    const statusCounts = { Active: 0, Dormant: 0, Pending: 0, Closed: 0 };
    filtered.forEach(a => { statusCounts[a.status || 'Active'] = (statusCounts[a.status || 'Active'] || 0) + 1; });

    document.getElementById('totalAssets').textContent = assets.length.toLocaleString(LOCALE);
    const recEl = document.getElementById('recordedCount');
    const valEl = document.getElementById('withValueCount');
    const allChip = document.getElementById('scopeAllCount');
    const recChip = document.getElementById('scopeRecordedCount');
    const valChip = document.getElementById('scopeValueCount');
    if (recEl) recEl.textContent = recorded.toLocaleString(LOCALE);
    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);
    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);
    if (recChip) recChip.textContent = recorded.toLocaleString(LOCALE);
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
}

'''
s = sub1(s, r'// ===== STATS =====.*?(?=// ===== [A-Z])', lambda m: stats, flags=re.S, label="stats")

TPL.write_text(s, encoding="utf-8")


# -----------------------------------------------------------------------------
# Translations
# -----------------------------------------------------------------------------
t = TR.read_text(encoding="utf-8")
en_anchor = '        "save_html": "Save HTML",\n'
en_new = en_anchor + '''        "save": "Save",
        "menu": "Features",
        "edition_free": "Free",
        "edition_family": "Family",
        "edition_professional": "Professional",
        "menu_views": "Views",
        "menu_family_tools": "Family Estate Tools",
        "menu_data": "Data",
        "menu_file_security": "File & Security",
        "menu_appearance": "Appearance",
        "menu_help": "Help",
        "recorded": "Recorded",
        "with_value": "With Value",
        "quick_filters": "Quick asset filters",
        "filter_all": "All",
        "filter_recorded": "Recorded",
        "filter_with_value": "With Value",
        "family_teaser": "Table · Charts · Print — Family",
        "professional_teaser": "Audit · Annual Review · Export — Professional",
        "upgrade_family": "Unlock Family",
        "upgrade_family_desc": "324-asset catalog, Table, Timeline, Charts, Print Estate Binder, Emergency Access Guide, Master Asset Index and five visual themes.",
        "upgrade_professional": "Unlock Professional",
        "upgrade_professional_desc": "517-asset catalog plus Audit, Access Readiness, Annual Review and professional Export Markdown / Excel / JSON workflows.",
'''
t = replace1(t, en_anchor, en_new, "English UI strings")
zh_anchor = '        "save_html": "保存 HTML",\n'
zh_new = zh_anchor + '''        "save": "保存",
        "menu": "功能",
        "edition_free": "免费版",
        "edition_family": "家庭版",
        "edition_professional": "专业版",
        "menu_views": "查看方式",
        "menu_family_tools": "家庭财产工具",
        "menu_data": "数据",
        "menu_file_security": "文件与安全",
        "menu_appearance": "外观",
        "menu_help": "帮助",
        "recorded": "已登记",
        "with_value": "有金额",
        "quick_filters": "快速资产筛选",
        "filter_all": "全部",
        "filter_recorded": "已登记",
        "filter_with_value": "有金额",
        "family_teaser": "表格 · 图表 · 打印 — 家庭版",
        "professional_teaser": "Audit · Annual Review · Export — 专业版",
        "upgrade_family": "解锁家庭版",
        "upgrade_family_desc": "324 项资产目录、表格、时间线、图表、可打印 Estate Binder、Emergency Access Guide、Master Asset Index 与 5 套视觉主题。",
        "upgrade_professional": "解锁专业版",
        "upgrade_professional_desc": "517 项完整资产目录，以及 Audit、Access Readiness、Annual Review、Export Markdown / Excel / JSON 等专业工作流。",
'''
t = replace1(t, zh_anchor, zh_new, "Chinese UI strings")

t = t.replace('"help_exporting_intro": "Use the action-bar buttons to export or save your work:"',
              '"help_exporting_intro": "Save and Print stay visible in the header; use the Features menu for professional exports, import, appearance and security settings:"')
t = t.replace('"help_productivity_text": "Kanban cards can be dragged between status columns. Use the ☰ Columns menu to show or hide table columns. Notes, alerts, and to-dos support Markdown (bold, italics, links, lists). The 💾 button toggles auto-save."',
              '"help_productivity_text": "Kanban cards can be dragged between status columns. Use the Features menu for secondary views, appearance, file security and auto-save. Notes, alerts, and to-dos support Markdown."')
t = t.replace('"help_exporting_intro": "使用操作栏按钮导出或保存您的工作："',
              '"help_exporting_intro": "保存和打印固定显示在顶部；专业导出、导入、外观与安全设置集中在“功能”菜单："')
TR.write_text(t, encoding="utf-8")


# -----------------------------------------------------------------------------
# E2E updates
# -----------------------------------------------------------------------------
e = TEST.read_text(encoding="utf-8")
e = replace1(e, '''def _layout(page, name):
    page.click(f'.layout-btn[data-layout="{name}"]')
    page.wait_for_timeout(150)
''', '''def _open_feature_menu(page):
    menu = page.locator("#featureMenu")
    if not menu.evaluate("el => el.classList.contains('open')"):
        page.click("#featureMenuToggle")
        page.wait_for_timeout(100)


def _menu_click(page, selector):
    _open_feature_menu(page)
    page.click(selector)
    page.wait_for_timeout(120)


def _layout(page, name):
    primary = page.locator(f'.layout-btn[data-layout="{name}"]:visible')
    if primary.count():
        primary.first.click()
    else:
        _open_feature_menu(page)
        page.locator(f'.menu-layout-item[data-layout="{name}"]:visible').first.click()
    page.wait_for_timeout(150)
''', "layout test helper")

e = replace1(e, '''                selector = {"print": "#printBtn", "export": "#exportMD"}.get(feat)
                if selector:
                    vis = page.locator(selector).count() > 0 and page.locator(selector).first.is_visible()
                    check(f"tier {tier}: {feat} visible={on}", vis == on, f"got {vis}")
                else:
                    vis = page.locator(f'.layout-btn[data-layout="{feat}"]').count() > 0 \\
                        and page.locator(f'.layout-btn[data-layout="{feat}"]').first.is_visible()
                    check(f"tier {tier}: layout {feat} visible={on}", vis == on, f"got {vis}")
''', '''                selector = {"print": "#printBtn", "export": "#exportMD"}.get(feat)
                if selector:
                    available = page.locator(selector).count() > 0
                    check(f"tier {tier}: {feat} available={on}", available == on, f"got {available}")
                else:
                    available = page.locator(f'.menu-layout-item[data-layout="{feat}"]').count() > 0
                    check(f"tier {tier}: layout {feat} available={on}", available == on, f"got {available}")
            check(f"tier {tier}: edition badge", bool(page.text_content("#editionBadge")))
            teaser_count = page.locator('.upgrade-preview.visible').count()
            expected_teasers = 2 if tier == 'free' else (1 if tier == 'family' else 0)
            check(f"tier {tier}: upgrade preview count={expected_teasers}", teaser_count == expected_teasers, f"got {teaser_count}")
''', "tier gating UI assertions")

core_anchor = '''    check("en: stat totalCategories = 32", page.text_content("#totalCategories") == "32",
          page.text_content("#totalCategories"))
'''
core_new = core_anchor + '''    check("en: professional edition badge", "Professional" in page.text_content("#editionBadge"))
    check("en: blank catalog has zero recorded assets", page.text_content("#recordedCount") == "0", page.text_content("#recordedCount"))
    check("en: blank catalog has zero assets with value", page.text_content("#withValueCount") == "0", page.text_content("#withValueCount"))
    check("en: quick scope filters render", page.locator(".scope-filter-btn").count() == 3)
'''
e = replace1(e, core_anchor, core_new, "core UI checks")

# Theme/template/security/export controls now live in the Features menu.
e = e.replace('page.click("#themeToggle")', '_menu_click(page, "#themeToggle")')
e = e.replace('page.click("#lockToggle")', '_menu_click(page, "#lockToggle")')
e = e.replace('page.click("#autoSaveToggle")', '_menu_click(page, "#autoSaveToggle")')
e = e.replace('page.click("#exportMD")', '_menu_click(page, "#exportMD")')
e = e.replace('page.click("#exportExcel")', '_menu_click(page, "#exportExcel")')
e = e.replace('page.click("#exportJSON")', '_menu_click(page, "#exportJSON")')

tpl_anchor = '''    # Template select (5 templates)
    templates = page.locator("#templateSelect option").count()
'''
tpl_new = '''    # Template select (5 templates) — now organized under Features > Appearance.
    _open_feature_menu(page)
    templates = page.locator("#templateSelect option").count()
'''
e = replace1(e, tpl_anchor, tpl_new, "template menu setup")

edit_anchor = '''    # Undo / redo via keyboard shortcuts
'''
edit_new = '''    check("en: recorded count updates after edit", int(page.text_content("#recordedCount")) >= 1)
    check("en: with-value count updates after FMV edit", int(page.text_content("#withValueCount")) >= 1)
    page.click('.scope-filter-btn[data-asset-scope="value"]')
    page.wait_for_timeout(200)
    check("en: With Value quick filter narrows to valued assets",
          page.locator("#dashboardView .asset-item").count() == page.evaluate("assets.filter(hasFinancialValue).length"))
    page.click('.scope-filter-btn[data-asset-scope="all"]')
    page.wait_for_timeout(150)

    # Undo / redo via keyboard shortcuts
'''
e = replace1(e, edit_anchor, edit_new, "value filter checks")

static_anchor = '''    check("planning annual-review layout compiled", 'data-layout="review"' in en_html and "renderAnnualReview" in en_html)
'''
static_new = static_anchor + '''    check("tier-aware feature menu compiled", all(t in en_html for t in ["featureMenuToggle", "editionBadge", "upgrade-preview", "scope-filter-btn"]))
    check("professional terminology retained", all(t in en_html for t in [">Audit<", ">Annual Review<", "Export MD", "Export JSON"]))
'''
e = replace1(e, static_anchor, static_new, "static tier UI checks")
TEST.write_text(e, encoding="utf-8")


# -----------------------------------------------------------------------------
# Docs
# -----------------------------------------------------------------------------
f = FEATURE.read_text(encoding="utf-8")
if "Tier-aware product navigation" not in f:
    marker = "## 3. Data entry & editing"
    block = '''## 2a. Tier-aware product navigation\n\n| # | Feature | Status |\n|---|---------|--------|\n| 2a.1 | Tier-aware product navigation — Free / Family / Professional display names while internal key remains `planning` | ✅ |\n| 2a.2 | Primary header reduced to Search + Add + Print (paid) + Save + Features; secondary controls grouped in the Features menu | ✅ |\n| 2a.3 | Free continuously previews locked Family + Professional capabilities; Family previews Professional; Professional has no upsell UI | ✅ |\n| 2a.4 | Total Assets card includes Recorded and With Value counts; one-click All / Recorded / With Value scope filters apply across layouts | ✅ |\n| 2a.5 | Status controls collapsed into a dropdown and workspace navigation is responsive/mobile-scrollable | ✅ |\n\n'''
    if marker not in f:
        raise SystemExit("feature-list insertion marker missing")
    f = f.replace(marker, block + marker, 1)
FEATURE.write_text(f, encoding="utf-8")

v = VERSION.read_text(encoding="utf-8")
if "User-facing edition names" not in v:
    insert = '''\n### User-facing edition names and UI hierarchy\n\n- User-facing editions are **Free / Family / Professional** (免费版 / 家庭版 / 专业版). The implementation key `planning` remains unchanged for backward compatibility with licenses, build markers and tests.\n- Free intentionally shows locked Family and Professional capability previews to communicate product depth without shipping paid implementation code.\n- Family removes the Family upsell and previews only Professional analysis/export capability.\n- Professional removes upsell UI entirely and retains professional terminology such as Audit, Access Readiness, Annual Review, Export Markdown and Export JSON.\n- Save and Print remain first-class actions when available; low-frequency file/security/export/appearance controls live in a grouped Features menu.\n\n'''
    v = v.replace("## 2. Feature → tier map\n", "## 2. Feature → tier map\n" + insert, 1)
VERSION.write_text(v, encoding="utf-8")

print("tier-aware UI migration applied")
