#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parent.parent
tpl = root / 'templates' / 'dashboard.html'
test = root / 'tests' / 'e2e_visual_test.py'
feature = root / 'docs' / 'dev' / 'feature_list.md'

s = tpl.read_text(encoding='utf-8')
anchor = '''    <div class="feature-menu-header">
        <strong>{{TR_menu}}</strong>
        <button class="feature-menu-close" id="featureMenuClose" aria-label="{{TR_close}}">×</button>
    </div>
'''
if anchor not in s:
    raise SystemExit('feature menu header anchor not found')
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
    </div>
'''
s = s.replace(anchor, anchor + views, 1)
tpl.write_text(s, encoding='utf-8')

# Tests: both surfaces must expose the same tier-appropriate Views and share active state.
t = test.read_text(encoding='utf-8')
old = '''            check(f"responsive {width}: Views removed from menu",
                  page.locator("#featureMenu .menu-layout-item").count() == 0)
            page.click("#featureMenuClose")'''
new = '''            check(f"responsive {width}: Views also present in menu",
                  page.locator("#featureMenu .menu-layout-item").count() == 9
                  and page.locator("#featureMenu .menu-layout-item svg").count() == 9)
            page.locator('#featureMenu .menu-layout-item[data-layout="kanban"]').click()
            page.wait_for_timeout(120)
            check(f"responsive {width}: menu View syncs header active state",
                  page.locator('#headerViewSwitcher .header-layout-btn[data-layout="kanban"].active').count() == 1)
            page.click("#featureMenuToggle")
            page.locator('#featureMenu .menu-layout-item[data-layout="dashboard"]').click()
            page.wait_for_timeout(120)'''
if old not in t:
    raise SystemExit('responsive menu test anchor not found')
t = t.replace(old, new, 1)
# Static check: explicitly require both Header and menu view surfaces.
old2 = 'check("simplified chrome compiled", all(t in en_html for t in ["logo-menu-toggle", "statAddAssetBtn", "filter-status-toggles", "menu-layout-grid"]))'
new2 = 'check("dual View navigation compiled", all(t in en_html for t in ["logo-menu-toggle", "statAddAssetBtn", "filter-status-toggles", "headerViewSwitcher", "menu-layout-grid", "menu-layout-item"]))'
if old2 in t:
    t = t.replace(old2, new2, 1)
test.write_text(t, encoding='utf-8')

f = feature.read_text(encoding='utf-8')
oldf = '| 2a.7 | Clicking the top-left EstateON logo icon opens the Features menu; all Views use the original SVG icon set centered in the Header, with bilingual Professional labels exposed through title/ARIA | ✅ |'
newf = '| 2a.7 | All Views use the original SVG icon set in two synchronized surfaces: centered Header shortcuts and a complete Views section inside the Features menu; tier gating and active state stay in sync | ✅ |'
if oldf not in f:
    raise SystemExit('feature_list 2a.7 anchor not found')
f = f.replace(oldf, newf, 1)
feature.write_text(f, encoding='utf-8')

print('Restored synchronized Views section to Features menu')
