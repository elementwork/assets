#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "templates" / "dashboard.html"
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

p.write_text(s, encoding="utf-8")
print('Kept recorded-asset metadata within existing schema constraints')
