#!/usr/bin/env python3
"""Adjust the legacy file-lock save regression to exercise fallback mode explicitly."""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "tests" / "e2e_visual_test.py"
s = p.read_text(encoding="utf-8")
old = '''    _save_modal(page)\n    page.click("#lockToggle")\n'''
new = '''    _save_modal(page)\n    # This legacy File Lock regression validates the universal staged/download\n    # fallback. Direct Save has separate Inventory ID/API assertions below.\n    page.evaluate("Object.defineProperty(window, 'showSaveFilePicker', {value: undefined, configurable: true})")\n    page.click("#lockToggle")\n'''
if old not in s:
    raise SystemExit("file-lock fallback E2E anchor missing")
s = s.replace(old, new, 1)
# Clean an existing pyflakes warning while touching this test.
s = s.replace("check(f\"tier {tier}: asset count embedded\", f'\\\"id\\\": \\\"A-' in html)",
              "check(f\"tier {tier}: asset count embedded\", '\\\"id\\\": \\\"A-' in html)", 1)
p.write_text(s, encoding="utf-8")
print("fallback-mode E2E adjusted")
