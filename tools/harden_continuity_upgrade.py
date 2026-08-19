#!/usr/bin/env python3
"""Post-migration hardening for per-family binding and bilingual print text."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch(rel, old, new):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    if old not in s:
        raise SystemExit(f"hardening anchor missing in {rel}: {old[:120]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")


# Generic distributed templates receive a template identity in source; the browser
# adopts a random per-family identity on first open. Paid buyer-bound builds keep a
# deterministic buyer-specific identity.
patch(
    "src/generate_asset_inventory.py",
    '''    inventory_id = "INV-" + hashlib.sha256(\n        f"{tier}|{lang}|{buyer or 'unbound-family'}".encode("utf-8")\n    ).hexdigest()[:12].upper()\n''',
    '''    identity_prefix = "INV-" if buyer else "INV-TEMPLATE-"\n    identity_seed = f"{tier}|{lang}|{buyer or 'distribution-template'}"\n    inventory_id = identity_prefix + hashlib.sha256(\n        identity_seed.encode("utf-8")\n    ).hexdigest()[:12].upper()\n''',
)

# Fully bilingual emergency-page procedures.
patch(
    "src/translations.py",
    '        "print_death_path": "If the owner has died",\n',
    '''        "print_death_path": "If the owner has died",\n        "print_incapacity_step1": "Locate the POA / authority documents referenced in this inventory.",\n        "print_incapacity_step2": "Use each critical asset's recovery location and recovery contact.",\n        "print_incapacity_step3": "Contact the institution directly and follow its incapacity process.",\n        "print_death_step1": "Locate the will / executor authority and death certificate.",\n        "print_death_step2": "Use the Master Asset Index to identify institutions, policies and account references.",\n        "print_death_step3": "Follow each institution's estate process and preserve records for tax and probate work.",\n''',
)
patch(
    "src/translations.py",
    '        "print_death_path": "所有者身故时",\n',
    '''        "print_death_path": "所有者身故时",\n        "print_incapacity_step1": "找到本清单所引用的授权委托书（POA）及其他授权文件。",\n        "print_incapacity_step2": "按关键资产记录的恢复资料位置和恢复联系人取得协助。",\n        "print_incapacity_step3": "直接联系相关机构并遵循其失能处理流程。",\n        "print_death_step1": "找到遗嘱、遗嘱执行人授权文件及死亡证明。",\n        "print_death_step2": "使用资产总索引确认机构、保单及账户参考信息。",\n        "print_death_step3": "遵循各机构的遗产处理流程，并保留税务及遗嘱认证所需记录。",\n''',
)

patch(
    "templates/dashboard.html",
    '''            <h3>{{TR_print_incapacity_path}}</h3>\n            <ol><li>Locate the POA / authority documents referenced in this inventory.</li><li>Use the recovery location and recovery contact below for each critical asset.</li><li>Contact the institution directly and follow its incapacity process.</li></ol>\n            <h3>{{TR_print_death_path}}</h3>\n            <ol><li>Locate the will / executor authority and death certificate.</li><li>Use the Master Asset Index to identify institutions, policies and account references.</li><li>Follow each institution's estate process; preserve records for tax and probate work.</li></ol>\n''',
    '''            <h3>{{TR_print_incapacity_path}}</h3>\n            <ol><li>{{TR_print_incapacity_step1}}</li><li>{{TR_print_incapacity_step2}}</li><li>{{TR_print_incapacity_step3}}</li></ol>\n            <h3>{{TR_print_death_path}}</h3>\n            <ol><li>{{TR_print_death_step1}}</li><li>{{TR_print_death_step2}}</li><li>{{TR_print_death_step3}}</li></ol>\n''',
)

# Adopt a unique family ID on first open of an unbound distribution template.
patch(
    "templates/dashboard.html",
    '''let saveFileHandle = null;\n\nfunction supportsDirectFileSave() {''',
    '''let saveFileHandle = null;\nconst SOURCE_INVENTORY_ID = INVENTORY_DATA.inventory_id || '';\n\nfunction ensureInventoryId() {\n    const current = INVENTORY_DATA.inventory_id || '';\n    if (current && !current.startsWith('INV-TEMPLATE-')) return current;\n    const bytes = new Uint8Array(6);\n    if (globalThis.crypto && crypto.getRandomValues) crypto.getRandomValues(bytes);\n    else for (let i = 0; i < bytes.length; i++) bytes[i] = Math.floor(Math.random() * 256);\n    const next = 'INV-' + [...bytes].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();\n    INVENTORY_DATA.inventory_id = next;\n    const scriptEl = [...document.scripts].find(s => s.textContent.includes('const INVENTORY_DATA ='));\n    if (scriptEl && current) {\n        scriptEl.textContent = scriptEl.textContent.replace(`"inventory_id": "${current}"`, `"inventory_id": "${next}"`);\n    }\n    return next;\n}\n\nfunction supportsDirectFileSave() {''',
)

patch(
    "templates/dashboard.html",
    '''            if (!targetId || !currentId || targetId !== currentId) {\n                showToast('{{TR_direct_save_mismatch}}');\n                return false;\n            }\n''',
    '''            const adoptingSourceTemplate = SOURCE_INVENTORY_ID.startsWith('INV-TEMPLATE-') && targetId === SOURCE_INVENTORY_ID;\n            if (!targetId || !currentId || (targetId !== currentId && !adoptingSourceTemplate)) {\n                showToast('{{TR_direct_save_mismatch}}');\n                return false;\n            }\n''',
)

patch(
    "templates/dashboard.html",
    '''    document.getElementById('saveHTML').addEventListener('click', () => saveCurrentData(false));\n    document.getElementById('saveAsHTML').addEventListener('click', () => saveCurrentData(true));\n    const invChip = document.getElementById('inventoryIdChip');\n''',
    '''    ensureInventoryId();\n    document.getElementById('saveHTML').addEventListener('click', () => saveCurrentData(false));\n    document.getElementById('saveAsHTML').addEventListener('click', () => saveCurrentData(true));\n    const invChip = document.getElementById('inventoryIdChip');\n''',
)

# E2E explicitly verifies template adoption happened on load.
patch(
    "tests/e2e_visual_test.py",
    '''    check("en: inventory id format", bool(re.match(r"^INV-[A-F0-9]{12}$", current_inv_id or "")), current_inv_id)\n''',
    '''    check("en: inventory id format", bool(re.match(r"^INV-[A-F0-9]{12}$", current_inv_id or "")), current_inv_id)\n    check("en: distributed template adopts per-family inventory id",\n          not str(current_inv_id).startswith("INV-TEMPLATE-"))\n''',
)

print("continuity hardening applied")
