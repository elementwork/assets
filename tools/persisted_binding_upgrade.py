#!/usr/bin/env python3
"""Add persistent File System Access binding via IndexedDB and test/docs coverage."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch(rel, old, new):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    if old not in s:
        raise SystemExit(f"anchor missing in {rel}: {old[:120]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")


# ---- dashboard: persisted file handle ----
patch(
    "templates/dashboard.html",
    """let saveFileHandle = null;\nconst SOURCE_INVENTORY_ID = INVENTORY_DATA.inventory_id || '';\n\nfunction ensureInventoryId() {""",
    """let saveFileHandle = null;\nconst SOURCE_INVENTORY_ID = INVENTORY_DATA.inventory_id || '';\nconst SAVE_HANDLE_DB = 'estateon-asset-inventory';\nconst SAVE_HANDLE_STORE = 'file-handles';\n\nfunction openSaveHandleDB() {\n    if (!('indexedDB' in window)) return Promise.resolve(null);\n    return new Promise((resolve, reject) => {\n        const req = indexedDB.open(SAVE_HANDLE_DB, 1);\n        req.onupgradeneeded = () => {\n            const db = req.result;\n            if (!db.objectStoreNames.contains(SAVE_HANDLE_STORE)) db.createObjectStore(SAVE_HANDLE_STORE);\n        };\n        req.onsuccess = () => resolve(req.result);\n        req.onerror = () => reject(req.error);\n    });\n}\n\nasync function persistSaveFileHandle(handle) {\n    if (!handle) return;\n    let db = null;\n    try {\n        db = await openSaveHandleDB();\n        if (!db) return;\n        await new Promise((resolve, reject) => {\n            const tx = db.transaction(SAVE_HANDLE_STORE, 'readwrite');\n            tx.objectStore(SAVE_HANDLE_STORE).put(handle, INVENTORY_DATA.inventory_id || 'default');\n            tx.oncomplete = resolve;\n            tx.onerror = () => reject(tx.error);\n            tx.onabort = () => reject(tx.error);\n        });\n    } catch (e) {\n        console.warn('Could not persist file handle; session binding remains available', e);\n    } finally {\n        if (db) db.close();\n    }\n}\n\nasync function loadPersistedSaveFileHandle() {\n    let db = null;\n    try {\n        db = await openSaveHandleDB();\n        if (!db) return null;\n        return await new Promise((resolve, reject) => {\n            const tx = db.transaction(SAVE_HANDLE_STORE, 'readonly');\n            const req = tx.objectStore(SAVE_HANDLE_STORE).get(INVENTORY_DATA.inventory_id || 'default');\n            req.onsuccess = () => resolve(req.result || null);\n            req.onerror = () => reject(req.error);\n        });\n    } catch (e) {\n        console.warn('Could not restore persisted file handle', e);\n        return null;\n    } finally {\n        if (db) db.close();\n    }\n}\n\nasync function restoreSaveFileHandle() {\n    if (!supportsDirectFileSave()) return null;\n    const handle = await loadPersistedSaveFileHandle();\n    if (!handle) return null;\n    saveFileHandle = handle;\n    const chip = document.getElementById('inventoryIdChip');\n    if (chip && handle.name) chip.title = `{{TR_inventory_id_label}}: ${INVENTORY_DATA.inventory_id || ''} • ${handle.name}`;\n    return handle;\n}\n\nasync function ensureWritePermission(handle) {\n    if (!handle) return false;\n    if (typeof handle.queryPermission !== 'function' || typeof handle.requestPermission !== 'function') return true;\n    const opts = { mode: 'readwrite' };\n    if (await handle.queryPermission(opts) === 'granted') return true;\n    return (await handle.requestPermission(opts)) === 'granted';\n}\n\nfunction ensureInventoryId() {""",
)

patch(
    "templates/dashboard.html",
    """async function directSaveCurrentFile(forcePicker = false) {\n    const html = await buildSavedHTML();\n    let handle = saveFileHandle;\n    if (!handle || forcePicker) {\n        handle = await window.showSaveFilePicker({""",
    """async function directSaveCurrentFile(forcePicker = false) {\n    let handle = saveFileHandle;\n    if (handle && !forcePicker) {\n        const permitted = await ensureWritePermission(handle);\n        if (!permitted) handle = null;\n    }\n    if (!handle || forcePicker) {\n        handle = await window.showSaveFilePicker({""",
)

patch(
    "templates/dashboard.html",
    """        saveFileHandle = handle;\n    }\n    const writable = await handle.createWritable();""",
    """        saveFileHandle = handle;\n        await persistSaveFileHandle(handle);\n    }\n    const html = await buildSavedHTML();\n    const writable = await handle.createWritable();""",
)

patch(
    "templates/dashboard.html",
    """    const invChip = document.getElementById('inventoryIdChip');\n    if (invChip) invChip.textContent = (INVENTORY_DATA.inventory_id || '').replace('INV-', '#');\n    // Save guide overlay actions""",
    """    const invChip = document.getElementById('inventoryIdChip');\n    if (invChip) invChip.textContent = (INVENTORY_DATA.inventory_id || '').replace('INV-', '#');\n    restoreSaveFileHandle().catch(e => console.warn('Persisted binding restore failed', e));\n    // Save guide overlay actions""",
)

# ---- E2E: compile/runtime coverage for persistent binding ----
patch(
    "tests/e2e_visual_test.py",
    """    check(\"direct-save API path compiled\", \"showSaveFilePicker\" in en_html and \"directSaveCurrentFile\" in en_html)\n""",
    """    check(\"direct-save API path compiled\", \"showSaveFilePicker\" in en_html and \"directSaveCurrentFile\" in en_html)\n    check(\"persistent file-handle binding compiled\",\n          all(t in en_html for t in [\"indexedDB.open\", \"persistSaveFileHandle\", \"loadPersistedSaveFileHandle\", \"restoreSaveFileHandle\", \"ensureWritePermission\"]))\n""",
)

patch(
    "tests/e2e_visual_test.py",
    """    check(\"en: save-as control present\", page.locator(\"#saveAsHTML\").count() == 1)\n""",
    """    check(\"en: save-as control present\", page.locator(\"#saveAsHTML\").count() == 1)\n    check(\"en: persistent binding helpers available\",\n          page.evaluate(\"typeof persistSaveFileHandle === 'function' && typeof loadPersistedSaveFileHandle === 'function' && typeof restoreSaveFileHandle === 'function' && typeof ensureWritePermission === 'function'\"))\n""",
)

# ---- docs ----
for rel in ["README.md", "docs/dev/versioning_plan.md", "docs/user/ADMIN_GUIDE.md", "docs/dev/feature_list.md"]:
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    if rel == "README.md":
        s = s.replace(
            "Chromium Direct Save uses the File System Access API; **Inventory ID binding blocks accidental overwrite of another family's inventory**.",
            "Chromium Direct Save uses the File System Access API and persists the authorized file handle in IndexedDB; **Inventory ID binding blocks accidental overwrite of another family's inventory**.",
            1,
        )
    elif rel == "docs/dev/versioning_plan.md":
        s = s.replace(
            "- Chrome/Edge: Save opens a File System Access picker on first use, then reuses that in-session handle for direct writes. **Save As** always asks for a target.",
            "- Chrome/Edge: Save opens a File System Access picker on first use, stores the authorized `FileSystemFileHandle` in IndexedDB under the Inventory ID, and restores that binding on later opens. The browser may request write permission again. **Save As** always asks for a target and replaces the stored binding.",
            1,
        )
    elif rel == "docs/user/ADMIN_GUIDE.md":
        s = s.replace(
            "subsequent saves in that browser session write directly to the same bound file.",
            "subsequent saves write directly to the same bound file; Chrome/Edge stores the authorized file handle in IndexedDB so the binding can be restored after reopening the inventory. The browser may ask you to approve write access again.",
            1,
        )
    elif rel == "docs/dev/feature_list.md":
        s = s.replace(
            "Direct Save: Chromium File System Access API writes back to a user-selected bound file; Inventory ID prevents cross-inventory overwrite; staged Ctrl+S/download remains the fallback",
            "Direct Save: Chromium File System Access API writes back to a bound file; authorized handle persists in IndexedDB across reopen; Inventory ID prevents cross-inventory overwrite; staged Ctrl+S/download remains the fallback",
            1,
        )
    p.write_text(s, encoding="utf-8")

print("persistent binding upgrade applied")
