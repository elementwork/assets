#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates' / 'dashboard.html'
TR = ROOT / 'src' / 'translations.py'
TEST = ROOT / 'tests' / 'e2e_visual_test.py'
FEATURE = ROOT / 'docs' / 'dev' / 'feature_list.md'
GEN = ROOT / 'src' / 'generate_asset_inventory.py'


def replace1(text, old, new, label):
    if old not in text:
        raise SystemExit(f'{label}: anchor not found')
    return text.replace(old, new, 1)


s = TPL.read_text(encoding='utf-8')

s = replace1(s,
'''                    <div class="stat-subline">
                        <button class="stat-link" data-stat-scope="recorded"><strong id="recordedCount">0</strong> {{TR_recorded}}</button>
                        <button class="stat-link" data-stat-scope="value"><strong id="withValueCount">0</strong> {{TR_with_value}}</button>
                    </div>''',
'''                    <div class="stat-subline">
                        <button class="stat-link" data-stat-scope="value"><strong id="withValueCount">0</strong> {{TR_with_value}}</button>
                    </div>''', 'asset stat subline')

s = replace1(s,
'''            <button class="scope-filter-btn active" data-asset-scope="all" aria-pressed="true">{{TR_filter_all}} <span class="scope-filter-count" id="scopeAllCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="recorded" aria-pressed="false">{{TR_filter_recorded}} <span class="scope-filter-count" id="scopeRecordedCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="value" aria-pressed="false">{{TR_filter_with_value}} <span class="scope-filter-count" id="scopeValueCount">0</span></button>''',
'''            <button class="scope-filter-btn active" data-asset-scope="all" aria-pressed="true">{{TR_filter_all}} <span class="scope-filter-count" id="scopeAllCount">0</span></button>
            <button class="scope-filter-btn" data-asset-scope="value" aria-pressed="false">{{TR_filter_with_value}} <span class="scope-filter-count" id="scopeValueCount">0</span></button>''', 'quick scope controls')

start = s.index("// ===== TIER-AWARE UI / ASSET SCOPE =====")
end = s.index("function editionDisplayName()", start)
new_scope = '''// ===== TIER-AWARE UI / ASSET SCOPE =====
let assetScopeFilter = 'all';
const VALUE_FIELDS = ['fmv','market_value','current_balance','equity'];

function hasFinancialValue(asset) {
    return VALUE_FIELDS.some(k => Number(asset && asset[k]) > 0);
}

function setAssetScope(scope) {
    assetScopeFilter = ['all','value'].includes(scope) ? scope : 'all';
    document.querySelectorAll('.scope-filter-btn').forEach(btn => {
        const active = btn.dataset.assetScope === assetScopeFilter;
        btn.classList.toggle('active', active);
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    renderCurrentLayout();
}

'''
s = s[:start] + new_scope + s[end:]

s = replace1(s,
'''        const matchesScope = assetScopeFilter === 'all' ||
            (assetScopeFilter === 'recorded' && isRecordedAsset(asset)) ||
            (assetScopeFilter === 'value' && hasFinancialValue(asset));''',
'''        const matchesScope = assetScopeFilter === 'all' ||
            (assetScopeFilter === 'value' && hasFinancialValue(asset));''', 'scope predicate')

s = replace1(s,
'''    const recorded = assets.filter(isRecordedAsset).length;
    const withValue = assets.filter(hasFinancialValue).length;''',
'''    const withValue = assets.filter(hasFinancialValue).length;''', 'stats variables')

s = replace1(s,
'''    const recEl = document.getElementById('recordedCount');
    const valEl = document.getElementById('withValueCount');
    const allChip = document.getElementById('scopeAllCount');
    const recChip = document.getElementById('scopeRecordedCount');
    const valChip = document.getElementById('scopeValueCount');
    if (recEl) recEl.textContent = recorded.toLocaleString(LOCALE);
    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);
    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);
    if (recChip) recChip.textContent = recorded.toLocaleString(LOCALE);
    if (valChip) valChip.textContent = withValue.toLocaleString(LOCALE);''',
'''    const valEl = document.getElementById('withValueCount');
    const allChip = document.getElementById('scopeAllCount');
    const valChip = document.getElementById('scopeValueCount');
    if (valEl) valEl.textContent = withValue.toLocaleString(LOCALE);
    if (allChip) allChip.textContent = assets.length.toLocaleString(LOCALE);
    if (valChip) valChip.textContent = withValue.toLocaleString(LOCALE);''', 'stats elements')
TPL.write_text(s, encoding='utf-8')

# Remove the experimental Recorded wording entirely. A future Recorded metric should
# use explicit persisted user-confirmation metadata rather than infer from template defaults.
t = TR.read_text(encoding='utf-8')
for line in [
    '        "recorded": "Recorded",\n',
    '        "filter_recorded": "Recorded",\n',
    '        "recorded": "已登记",\n',
    '        "filter_recorded": "已登记",\n',
]:
    t = t.replace(line, '')
TR.write_text(t, encoding='utf-8')

# E2E now asserts the requested value signal only.
e = TEST.read_text(encoding='utf-8')
e = e.replace('''    check("en: blank catalog has zero recorded assets", page.text_content("#recordedCount") == "0", page.text_content("#recordedCount"))
''', '')
e = e.replace('''    check("en: quick scope filters render", page.locator(".scope-filter-btn").count() == 3)
''', '''    check("en: quick scope filters render", page.locator(".scope-filter-btn").count() == 2)
''')
e = e.replace('''    check("en: recorded count updates after edit", int(page.text_content("#recordedCount")) >= 1)
''', '')
TEST.write_text(e, encoding='utf-8')

f = FEATURE.read_text(encoding='utf-8')
f = f.replace('Total Assets card includes Recorded and With Value counts; one-click All / Recorded / With Value scope filters apply across layouts',
              'Total Assets card includes a With Value count; one-click All / With Value scope filters apply across layouts')
FEATURE.write_text(f, encoding='utf-8')

# Tier-marker stripping can leave indentation-only lines in generated artifacts.
# Normalize trailing whitespace in the generator itself so checked-in outputs remain
# byte-stable after future regeneration rather than cleaning artifacts post hoc.
g = GEN.read_text(encoding='utf-8')
g = replace1(g,
'''    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
''',
'''    # Normalize generated whitespace so tier-marker stripping never leaves
    # indentation-only lines that produce noisy diffs on regeneration.
    had_final_newline = html.endswith("\\n")
    html = "\\n".join(line.rstrip() for line in html.splitlines())
    if had_final_newline:
        html += "\\n"

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
''', 'generated HTML whitespace normalization')
GEN.write_text(g, encoding='utf-8')

print('value scope refined and generated HTML normalized')
