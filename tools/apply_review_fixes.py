#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates' / 'dashboard.html'
TR = ROOT / 'src' / 'translations.py'
TEST = ROOT / 'tests' / 'e2e_visual_test.py'
FEATURE = ROOT / 'docs' / 'dev' / 'feature_list.md'


def replace1(text, old, new, label):
    if old not in text:
        raise SystemExit(f'{label}: anchor not found')
    return text.replace(old, new, 1)


s = TPL.read_text(encoding='utf-8')

# --- tier state must be based on the effective (licensed) tier ---
s = replace1(s,
"""// advisor (deferred) treated as planning for now.\nconst tierCfg = TIER_FEATURES[APP_TIER] || TIER_FEATURES.planning;\n\nfunction tierHas(feature) {\n    return !!tierCfg[feature];\n}\n""",
"""// advisor (deferred) treated as planning for now.\nconst TIER_RANK = { free: 0, family: 1, planning: 2, advisor: 3 };\nlet effectiveTier = APP_TIER;\n\nfunction cloneTierConfig(tier) {\n    const source = TIER_FEATURES[tier] || TIER_FEATURES.planning;\n    return { ...source, templatesList: [...source.templatesList] };\n}\n\nlet tierCfg = cloneTierConfig(APP_TIER);\n\nfunction tierHas(feature) {\n    return !!tierCfg[feature];\n}\n\nfunction tierAtLeast(minTier) {\n    return (TIER_RANK[effectiveTier] ?? 0) >= (TIER_RANK[minTier] ?? 0);\n}\n\nfunction downgradeToFree() {\n    licenseValid = false;\n    effectiveTier = 'free';\n    tierCfg = cloneTierConfig('free');\n}\n""", 'tier config')

s = replace1(s,
"""async function verifyLicense() {\n    if (!LICENSE_JSON) { licenseValid = true; return; } // free tier\n    if (!window.crypto || !crypto.subtle) { licenseValid = false; return; }\n""",
"""async function verifyLicense() {\n    if (!LICENSE_JSON) {\n        if (APP_TIER === 'free') {\n            licenseValid = true;\n            effectiveTier = 'free';\n            tierCfg = cloneTierConfig('free');\n        } else {\n            downgradeToFree();\n        }\n        return;\n    }\n    if (!window.crypto || !crypto.subtle) { downgradeToFree(); return; }\n""", 'verify license preamble')

s = replace1(s,
"""        licenseValid = true;\n    } catch (e) {\n        licenseValid = false;\n    }\n    if (!licenseValid) {\n        // Downgrade to free capability: hide paid features entirely.\n        Object.assign(tierCfg, TIER_FEATURES.free);\n    }\n}\n""",
"""        licenseValid = true;\n        effectiveTier = APP_TIER;\n        tierCfg = cloneTierConfig(APP_TIER);\n    } catch (e) {\n        downgradeToFree();\n    }\n}\n""", 'verify license completion')

# Hide tier sections after a paid build is downgraded.
s = replace1(s,
"""function applyTierGating() {\n    // Layout buttons\n""",
"""function applyTierGating() {\n    document.querySelectorAll('[data-min-tier]').forEach(el => {\n        el.hidden = !tierAtLeast(el.dataset.minTier);\n    });\n    // Layout buttons\n""", 'tier section gating')

# Normalize a persisted layout before rendering it under a downgraded/lower tier.
s = replace1(s,
"""let currentLayout = localStorage.getItem('assetLayout') || 'dashboard';\nlet currentAsset = null;\n""",
"""let currentLayout = localStorage.getItem('assetLayout') || 'dashboard';\n\nfunction layoutAllowedForTier(layout) {\n    if (['dashboard', 'kanban', 'detail', 'compact'].includes(layout)) return true;\n    if (layout === 'table') return tierHas('table');\n    if (layout === 'timeline') return tierHas('timeline');\n    if (layout === 'charts') return tierHas('charts');\n    if (layout === 'audit') return tierHas('audit');\n    if (layout === 'review') return tierHas('review');\n    return false;\n}\n\nfunction normalizeLayoutForTier() {\n    if (!layoutAllowedForTier(currentLayout)) {\n        currentLayout = 'dashboard';\n        localStorage.setItem('assetLayout', currentLayout);\n    }\n}\n\nlet currentAsset = null;\n""", 'layout normalization')

# Print must contain only the binder, never application navigation.
s = replace1(s,
"""    .header,\n    .summary-section,\n""",
"""    .header,\n    .workspace-bar,\n    .feature-menu,\n    .summary-section,\n""", 'print chrome hide')

# Dynamic sticky offset plus mobile non-sticky workspace.
s = replace1(s,
"""/* ===== TIER-AWARE PRODUCT NAVIGATION ===== */\n.tier-header {\n""",
"""/* ===== TIER-AWARE PRODUCT NAVIGATION ===== */\n:root { --app-header-height: 68px; }\n.tier-header {\n""", 'header css var')
s = replace1(s, "    top:68px;\n", "    top:var(--app-header-height);\n", 'workspace sticky top')
s = replace1(s, "    .workspace-bar { top:116px; padding:6px 16px; }\n    .workspace-upgrade { display:none; }\n",
"    .workspace-bar { padding:6px 16px; }\n    .workspace-upgrade { font-size:10px; padding:6px 9px; }\n    .upgrade-long { display:none; }\n    .upgrade-short { display:inline; }\n", 'tablet workspace')
s = replace1(s, "    .workspace-bar { top:126px; overflow-x:auto; }\n",
"    .workspace-bar { position:relative; top:auto; overflow-x:auto; }\n", 'mobile workspace')

# Better touch targets and explicit mobile menu affordance.
s = replace1(s,
"""    .feature-menu { top:8px; right:8px; width:calc(100vw - 16px); max-height:calc(100vh - 16px); }\n    .menu-grid { grid-template-columns:1fr; }\n""",
"""    .feature-menu { top:8px; right:8px; width:calc(100vw - 16px); max-height:calc(100vh - 16px); }\n    .menu-grid { grid-template-columns:1fr; }\n    .tier-header .header-right .btn,\n    .workspace-btn.layout-btn,\n    .menu-action, .menu-layout-item,\n    .scope-filter-btn,\n    .status-filter-details > summary { min-height:44px; font-size:13px; }\n    .feature-menu-close { width:44px; height:44px; }\n""", 'mobile touch targets')

# Upgrade teaser remains visible on tablet/mobile in compact form.
s = replace1(s,
""".workspace-upgrade:hover { border-style:solid; color:var(--accent); }\n\n.feature-menu {\n""",
""".workspace-upgrade:hover { border-style:solid; color:var(--accent); }\n.upgrade-short { display:none; }\n\n.feature-menu {\n""", 'upgrade compact css')

# Feature menu header + close button.
s = replace1(s,
""".feature-menu.open { display:block; }\n.menu-section { padding:8px 4px 12px; border-bottom:1px solid var(--border-light); }\n""",
""".feature-menu.open { display:block; }\n.feature-menu-header { display:flex; align-items:center; justify-content:space-between; gap:10px; padding:2px 4px 8px 7px; border-bottom:1px solid var(--border-light); }\n.feature-menu-header strong { font-size:13px; }\n.feature-menu-close { border:0; background:transparent; color:var(--text-secondary); border-radius:var(--radius-sm); font-size:22px; line-height:1; cursor:pointer; }\n.feature-menu-close:hover { background:var(--surface); color:var(--text); }\n.menu-section { padding:8px 4px 12px; border-bottom:1px solid var(--border-light); }\n""", 'feature menu header css')

# Professional navigation uses localized bilingual professional terminology in zh.
s = replace1(s,
"""        <button class=\"layout-btn workspace-btn\" data-layout=\"dashboard\">Dashboard</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"table\">Table</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"charts\">Charts</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"audit\">Audit</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"review\">Annual Review</button>\n""",
"""        <button class=\"layout-btn workspace-btn\" data-layout=\"dashboard\">{{TR_professional_dashboard}}</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"table\">{{TR_professional_table}}</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"charts\">{{TR_professional_charts}}</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"audit\">{{TR_professional_audit}}</button>\n        <button class=\"layout-btn workspace-btn\" data-layout=\"review\">{{TR_professional_review}}</button>\n""", 'professional workspace labels')

s = replace1(s,
"""    <button class=\"workspace-upgrade\" data-upgrade-trigger=\"free\">🔒 {{TR_family_teaser}}</button>\n    <button class=\"workspace-upgrade\" data-upgrade-trigger=\"family\">🔒 {{TR_professional_teaser}}</button>\n""",
"""    <button class=\"workspace-upgrade\" data-upgrade-trigger=\"free\">🔒 <span class=\"upgrade-long\">{{TR_family_teaser}}</span><span class=\"upgrade-short\">{{TR_edition_family}}</span></button>\n    <button class=\"workspace-upgrade\" data-upgrade-trigger=\"family\">🔒 <span class=\"upgrade-long\">{{TR_professional_teaser}}</span><span class=\"upgrade-short\">{{TR_edition_professional}}</span></button>\n""", 'workspace teaser compact labels')

s = replace1(s,
"""<div class=\"feature-menu\" id=\"featureMenu\" aria-hidden=\"true\">\n    <div class=\"menu-section\">\n""",
"""<div class=\"feature-menu\" id=\"featureMenu\" aria-hidden=\"true\" tabindex=\"-1\">\n    <div class=\"feature-menu-header\">\n        <strong>{{TR_menu}}</strong>\n        <button class=\"feature-menu-close\" id=\"featureMenuClose\" aria-label=\"{{TR_close}}\">×</button>\n    </div>\n    <div class=\"menu-section\">\n""", 'feature menu close markup')

s = replace1(s,
"""            <button class=\"menu-layout-item\" data-layout=\"audit\">Audit</button>\n            <button class=\"menu-layout-item\" data-layout=\"review\">Annual Review</button>\n""",
"""            <button class=\"menu-layout-item\" data-layout=\"audit\">{{TR_professional_audit}}</button>\n            <button class=\"menu-layout-item\" data-layout=\"review\">{{TR_professional_review}}</button>\n""", 'professional menu labels')

s = replace1(s,
"""    <div class=\"menu-section\">\n        <div class=\"menu-section-title\">{{TR_menu_family_tools}}</div>\n""",
"""    <div class=\"menu-section\" data-min-tier=\"family\">\n        <div class=\"menu-section-title\">{{TR_menu_family_tools}}</div>\n""", 'family tier section')

s = replace1(s,
"""    <div class=\"menu-section\">\n        <div class=\"menu-section-title\">Export</div>\n        <div class=\"menu-grid\">\n            <button class=\"menu-action\" id=\"exportMD\">{{TR_export_md}}</button>\n""",
"""    <div class=\"menu-section\" data-min-tier=\"planning\">\n        <div class=\"menu-section-title\">{{TR_professional_export}}</div>\n        <div class=\"menu-grid\">\n            <button class=\"menu-action\" id=\"exportMD\">{{TR_export_md}}</button>\n""", 'professional export section')

# Asset Catalog semantics: catalog size stays global while Showing tracks current filters.
s = replace1(s,
"""                    <div class=\"stat-label\">{{TR_total_assets}}</div>\n                    <div class=\"stat-subline\">\n                        <button class=\"stat-link\" data-stat-scope=\"value\"><strong id=\"withValueCount\">0</strong> {{TR_with_value}}</button>\n                    </div>\n""",
"""                    <div class=\"stat-label\">{{TR_asset_catalog}}</div>\n                    <div class=\"stat-subline\">\n                        <span><strong id=\"showingCount\">0</strong> {{TR_showing}}</span>\n                        <button class=\"stat-link\" data-stat-scope=\"value\"><strong id=\"withValueCount\">0</strong> {{TR_with_value}}</button>\n                    </div>\n""", 'asset catalog stat')

# Current USD FMV is also a real current value signal.
s = replace1(s,
"const VALUE_FIELDS = ['fmv','market_value','current_balance','equity'];\n",
"const VALUE_FIELDS = ['fmv','fmv_usd','market_value','current_balance','equity'];\n", 'value fields')

# Tier UI follows effective tier, not build tier.
s = replace1(s,
"""function editionDisplayName() {\n    if (APP_TIER === 'planning') return '{{TR_edition_professional}}';\n    if (APP_TIER === 'family') return '{{TR_edition_family}}';\n    return '{{TR_edition_free}}';\n}\n\nfunction initTierUI() {\n    document.documentElement.dataset.edition = APP_TIER;\n""",
"""function editionDisplayName() {\n    if (effectiveTier === 'planning') return '{{TR_edition_professional}}';\n    if (effectiveTier === 'family') return '{{TR_edition_family}}';\n    return '{{TR_edition_free}}';\n}\n\nfunction initTierUI() {\n    document.documentElement.dataset.edition = effectiveTier;\n""", 'edition effective tier')
s = s.replace("el.dataset.workspaceTier !== APP_TIER", "el.dataset.workspaceTier !== effectiveTier")
s = s.replace("el.dataset.upgradeTrigger !== APP_TIER || APP_TIER === 'planning'", "el.dataset.upgradeTrigger !== effectiveTier || effectiveTier === 'planning'")
s = s.replace("includes(APP_TIER);", "includes(effectiveTier);")
s = s.replace("const target = APP_TIER === 'free' ? 'family' : 'professional';", "const target = effectiveTier === 'free' ? 'family' : 'professional';")

# Dynamic header geometry.
s = replace1(s,
"""function setFeatureMenuOpen(open) {\n""",
"""let headerResizeObserver = null;\nfunction initHeaderGeometry() {\n    const header = document.querySelector('.tier-header');\n    if (!header) return;\n    const sync = () => {\n        document.documentElement.style.setProperty('--app-header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`);\n    };\n    sync();\n    if ('ResizeObserver' in window) {\n        headerResizeObserver = new ResizeObserver(sync);\n        headerResizeObserver.observe(header);\n    } else {\n        window.addEventListener('resize', sync);\n    }\n}\n\nfunction setFeatureMenuOpen(open) {\n""", 'header geometry js')

# Close button + focus return.
s = replace1(s,
"""    menu.classList.toggle('open', !!open);\n    menu.setAttribute('aria-hidden', open ? 'false' : 'true');\n    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');\n}\n\nfunction initFeatureMenu() {\n    const menu = document.getElementById('featureMenu');\n    const toggle = document.getElementById('featureMenuToggle');\n    if (!menu || !toggle) return;\n""",
"""    menu.classList.toggle('open', !!open);\n    menu.setAttribute('aria-hidden', open ? 'false' : 'true');\n    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');\n    if (!open && menu.contains(document.activeElement)) toggle.focus();\n}\n\nfunction initFeatureMenu() {\n    const menu = document.getElementById('featureMenu');\n    const toggle = document.getElementById('featureMenuToggle');\n    const close = document.getElementById('featureMenuClose');\n    if (!menu || !toggle) return;\n""", 'menu focus')
s = replace1(s,
"""    toggle.addEventListener('click', e => {\n        e.stopPropagation();\n        setFeatureMenuOpen(!menu.classList.contains('open'));\n    });\n""",
"""    toggle.addEventListener('click', e => {\n        e.stopPropagation();\n        setFeatureMenuOpen(!menu.classList.contains('open'));\n    });\n    if (close) close.addEventListener('click', () => setFeatureMenuOpen(false));\n""", 'menu close event')

# Verify license before initializing any tier-sensitive UI state.
s = replace1(s,
"""document.addEventListener('DOMContentLoaded', async () => {\n    loadFromLocalStorage();\n    initTemplate();\n    initTheme();\n    initTierUI();\n    initFeatureMenu();\n    initFilters();\n    initLayout();\n""",
"""document.addEventListener('DOMContentLoaded', async () => {\n    loadFromLocalStorage();\n    await verifyLicense();\n    initTemplate();\n    initTheme();\n    initTierUI();\n    initHeaderGeometry();\n    applyTierGating();\n    normalizeLayoutForTier();\n    initFeatureMenu();\n    initFilters();\n    initLayout();\n""", 'init order')
s = replace1(s,
"""    initKeyboardShortcuts();\n    await verifyLicense();\n    // Hide higher-tier UI when the effective tier is lower than the build\n    // tier (e.g. an invalid license downgraded a paid file to free).\n    applyTierGating();\n""",
"""    initKeyboardShortcuts();\n""", 'remove late license verify')

# Accessible status toggles.
s = s.replace('class="status-toggle-btn active" data-status="Active"', 'class="status-toggle-btn active" data-status="Active" aria-pressed="true"')
s = s.replace('class="status-toggle-btn active" data-status="Dormant"', 'class="status-toggle-btn active" data-status="Dormant" aria-pressed="true"')
s = s.replace('class="status-toggle-btn active" data-status="Pending"', 'class="status-toggle-btn active" data-status="Pending" aria-pressed="true"')
s = s.replace('class="status-toggle-btn active" data-status="Closed"', 'class="status-toggle-btn active" data-status="Closed" aria-pressed="true"')
s = replace1(s,
"""        btn.addEventListener('click', () => {\n            btn.classList.toggle('active');\n            renderCurrentLayout();\n        });\n""",
"""        btn.addEventListener('click', () => {\n            btn.classList.toggle('active');\n            btn.setAttribute('aria-pressed', btn.classList.contains('active') ? 'true' : 'false');\n            renderCurrentLayout();\n        });\n""", 'status aria state')

# Showing count tracks filters; catalog and with-value remain global.
s = replace1(s,
"""    const valEl = document.getElementById('withValueCount');\n    const allChip = document.getElementById('scopeAllCount');\n""",
"""    const showingEl = document.getElementById('showingCount');\n    const valEl = document.getElementById('withValueCount');\n    const allChip = document.getElementById('scopeAllCount');\n""", 'showing element')
s = replace1(s,
"""    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);\n    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);\n""",
"""    if (showingEl) showingEl.textContent = filtered.length.toLocaleString(LOCALE);\n    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);\n    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);\n""", 'showing update')

TPL.write_text(s, encoding='utf-8')

# --- translations ---
t = TR.read_text(encoding='utf-8')
t = replace1(t,
'        "edition_professional": "Professional",\n',
'        "edition_professional": "Professional",\n        "asset_catalog": "Asset Catalog",\n        "showing": "Showing",\n        "professional_dashboard": "Dashboard",\n        "professional_table": "Table",\n        "professional_charts": "Charts",\n        "professional_audit": "Audit",\n        "professional_review": "Annual Review",\n        "professional_export": "Export",\n', 'en professional translations')
t = replace1(t,
'        "edition_professional": "专业版",\n',
'        "edition_professional": "专业版",\n        "asset_catalog": "资产目录",\n        "showing": "当前显示",\n        "professional_dashboard": "Dashboard 仪表板",\n        "professional_table": "Table 表格",\n        "professional_charts": "Charts 图表",\n        "professional_audit": "Audit 财产审计",\n        "professional_review": "Annual Review 年度复核",\n        "professional_export": "Export 导出",\n', 'zh professional translations')
TR.write_text(t, encoding='utf-8')

# --- formal E2E coverage for the review findings ---
e = TEST.read_text(encoding='utf-8')

# Static checks for new code paths.
e = replace1(e,
'''    check("tier-aware feature menu compiled", all(t in en_html for t in ["featureMenuToggle", "editionBadge", "upgrade-preview", "scope-filter-btn"]))\n''',
'''    check("tier-aware feature menu compiled", all(t in en_html for t in ["featureMenuToggle", "featureMenuClose", "editionBadge", "upgrade-preview", "scope-filter-btn"]))\n    check("effective-tier normalization compiled", all(t in en_html for t in ["effectiveTier", "normalizeLayoutForTier", "cloneTierConfig", "downgradeToFree"]))\n    check("dynamic header geometry compiled", "ResizeObserver" in en_html and "--app-header-height" in en_html)\n''', 'static review checks')

# Add a dedicated license downgrade regression before static validation.
marker = '\n\n# =============================================================================\n# STEP 2 — Static validation of generated artifacts\n# =============================================================================\n'
if marker not in e:
    raise SystemExit('license test insertion marker missing')
license_test = r'''

def license_downgrade_ui_check():
    print("\n== Step 1c: invalid-license effective-tier UI ==")
    path = TMP / "asset-inventory-dashboard-planning.html"
    if not path.exists():
        check("invalid license fixture exists", False, str(path))
        return
    html = path.read_text(encoding="utf-8")
    tampered = re.sub(r"const LICENSE_JSON = '[^']*';",
                      "const LICENSE_JSON = 'invalid.invalid';", html, count=1)
    invalid = TMP / "asset-inventory-dashboard-planning-invalid-license.html"
    invalid.write_text(tampered, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        ctx.add_init_script("localStorage.setItem('assetLayout', 'audit')")
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(invalid.as_uri(), wait_until="load")
        page.wait_for_timeout(800)
        check("invalid license: effective edition is Free",
              page.get_attribute("html", "data-edition") == "free",
              page.get_attribute("html", "data-edition"))
        check("invalid license: Free badge shown", "Free" in page.text_content("#editionBadge"), page.text_content("#editionBadge"))
        check("invalid license: stale Audit layout normalized",
              page.evaluate("currentLayout") == "dashboard" and page.locator("#dashboardView.active").count() == 1,
              page.evaluate("currentLayout"))
        check("invalid license: print hidden", page.locator("#printBtn").count() == 1 and not page.locator("#printBtn").is_visible())
        check("invalid license: exports hidden", page.locator("#exportMD").count() == 1 and not page.locator("#exportMD").is_visible())
        check("invalid license: Family tools hidden", page.locator('[data-min-tier="family"]:visible').count() == 0)
        check("invalid license: template reduced to one", page.locator("#templateSelect option").count() == 1)
        check("invalid license: no JS errors", not errors, str(errors[:3]))
        ctx.close()
        browser.close()
'''
e = e.replace(marker, license_test + marker, 1)

# English dashboard semantics + fmv_usd.
e = replace1(e,
'''    check("en: blank catalog has zero assets with value", page.text_content("#withValueCount") == "0", page.text_content("#withValueCount"))\n    check("en: quick scope filters render", page.locator(".scope-filter-btn").count() == 2)\n''',
'''    check("en: blank catalog has zero assets with value", page.text_content("#withValueCount") == "0", page.text_content("#withValueCount"))\n    check("en: Asset Catalog label", "Asset Catalog" in page.locator(".stat-card").first.text_content())\n    check("en: Showing starts at 517", page.text_content("#showingCount") == "517", page.text_content("#showingCount"))\n    check("en: quick scope filters render", page.locator(".scope-filter-btn").count() == 2)\n    check("en: USD FMV counts as With Value", page.evaluate("hasFinancialValue({fmv_usd: 100})"))\n''', 'en asset catalog tests')

# Showing count after search.
e = replace1(e,
'''    check("en: search 'Chequing' narrows results", 0 < n < 517, f"n={n}")\n''',
'''    check("en: search 'Chequing' narrows results", 0 < n < 517, f"n={n}")\n    check("en: Showing count follows search", int(page.text_content("#showingCount")) == n, page.text_content("#showingCount"))\n''', 'showing search test')

# Feature menu close/focus and print-media chrome.
e = replace1(e,
'''    # Theme toggle\n    theme_before = page.evaluate("document.documentElement.getAttribute('data-theme')")\n''',
'''    # Feature menu close affordance + focus return\n    _open_feature_menu(page)\n    page.locator("#featureMenuClose").focus()\n    page.click("#featureMenuClose")\n    check("en: feature menu close button works", page.locator("#featureMenu.open").count() == 0)\n    check("en: feature menu returns focus to toggle", page.evaluate("document.activeElement && document.activeElement.id") == "featureMenuToggle")\n\n    # Theme toggle\n    theme_before = page.evaluate("document.documentElement.getAttribute('data-theme')")\n''', 'menu close tests')

# Insert print media assertions after print is rendered.
e = replace1(e,
'''    check("en: print includes inventory id", inventory_id in print_text, inventory_id)\n''',
'''    check("en: print includes inventory id", inventory_id in print_text, inventory_id)\n    page.emulate_media(media="print")\n    check("en: print media hides workspace chrome", page.evaluate("getComputedStyle(document.querySelector('.workspace-bar')).display") == "none")\n    check("en: print media hides feature menu", page.evaluate("getComputedStyle(document.querySelector('#featureMenu')).display") == "none")\n    check("en: print media shows binder", page.locator("#printView").is_visible())\n    page.emulate_media(media="screen")\n''', 'print media tests')

# Chinese professional terminology should intentionally be bilingual, not stray English.
e = replace1(e,
'''    check("zh: search placeholder translated", "搜索" in page.get_attribute("#searchInput", "placeholder"))\n''',
'''    check("zh: search placeholder translated", "搜索" in page.get_attribute("#searchInput", "placeholder"))\n    check("zh: Professional workspace uses bilingual terminology",\n          "Audit 财产审计" in page.locator('[data-workspace-tier="planning"]').text_content() and\n          "Annual Review 年度复核" in page.locator('[data-workspace-tier="planning"]').text_content())\n    _open_feature_menu(page)\n    check("zh: Professional export section localized", "Export 导出" in page.locator("#featureMenu").text_content())\n    page.click("#featureMenuClose")\n''', 'zh professional test')

# Formal responsive geometry test is committed, not a one-shot workflow smoke.
insert_before = '\n\ndef browser_e2e():\n'
if insert_before not in e:
    raise SystemExit('responsive test insertion marker missing')
responsive = r'''

def responsive_ui_check():
    print("\n== Step 2c: responsive tier UI geometry ==")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in ((390, 844), (768, 900)):
            ctx = browser.new_context(viewport={"width": width, "height": height})
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(EN_HTML.as_uri(), wait_until="load")
            page.wait_for_timeout(500)
            page.evaluate("window.scrollTo(0, 500)")
            page.wait_for_timeout(150)
            header_box = page.locator(".tier-header").bounding_box()
            workspace_box = page.locator(".workspace-bar").bounding_box()
            if width <= 680:
                check(f"responsive {width}: workspace is non-sticky on mobile",
                      page.evaluate("getComputedStyle(document.querySelector('.workspace-bar')).position") == "relative")
            else:
                check(f"responsive {width}: sticky workspace clears header",
                      bool(header_box and workspace_box and workspace_box['y'] + 1 >= header_box['y'] + header_box['height']),
                      f"header={header_box} workspace={workspace_box}")
            page.click("#featureMenuToggle")
            check(f"responsive {width}: feature menu opens", page.locator("#featureMenu.open").count() == 1)
            check(f"responsive {width}: close control visible", page.locator("#featureMenuClose").is_visible())
            if width <= 680:
                min_h = page.evaluate("parseFloat(getComputedStyle(document.querySelector('#featureMenuClose')).height)")
                check(f"responsive {width}: close touch target >=44", min_h >= 44, str(min_h))
            page.click("#featureMenuClose")
            check(f"responsive {width}: no JS errors", not errors, str(errors[:3]))
            ctx.close()
        browser.close()
'''
e = e.replace(insert_before, responsive + insert_before, 1)

# Ensure new suites execute.
e = replace1(e,
'''    tier_gating_check()\n    static_checks()\n    demo_fixture_check()\n''',
'''    tier_gating_check()\n    license_downgrade_ui_check()\n    static_checks()\n    demo_fixture_check()\n    responsive_ui_check()\n''', 'main test sequence')

TEST.write_text(e, encoding='utf-8')

# Feature docs: update semantics; E2E count will be refreshed by workflow.
f = FEATURE.read_text(encoding='utf-8')
f = f.replace('Total Assets card includes a With Value count; one-click All / With Value scope filters apply across layouts',
              'Asset Catalog card distinguishes global catalog size, current Showing count, and With Value count; one-click All / With Value scope filters apply across layouts')
f = f.replace('| 2a.5 | Status controls collapsed into a dropdown and workspace navigation is responsive/mobile-scrollable | ✅ |',
              '| 2a.5 | Status controls collapsed into an accessible dropdown; workspace uses measured sticky geometry and becomes non-sticky on narrow mobile screens | ✅ |\n| 2a.6 | Effective-tier UI follows verified license state; invalid paid licenses downgrade branding, workspace, templates and persisted layouts to Free | ✅ |\n| 2a.7 | Feature menu has explicit close/focus-return behavior and Professional zh labels retain bilingual professional terminology | ✅ |')
FEATURE.write_text(f, encoding='utf-8')

print('review fixes applied')
