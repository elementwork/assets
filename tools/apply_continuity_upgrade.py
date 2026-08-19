#!/usr/bin/env python3
"""One-shot repository migration for Direct Save + estate continuity features.

This script is intentionally removed by the release workflow after it applies the
upgrade.  It edits the existing generator/template/tests in-place so the final
squash commit contains only product changes.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAMP = "2026-08-19 12:59:00"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_once(rel: str, old: str, new: str) -> None:
    text = read(rel)
    if old not in text:
        raise SystemExit(f"anchor missing in {rel}: {old[:100]!r}")
    write(rel, text.replace(old, new, 1))


def regex_once(rel: str, pattern: str, repl: str, flags: int = 0) -> None:
    text = read(rel)
    out, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"regex anchor count={count} in {rel}: {pattern[:100]!r}")
    write(rel, out)


# ---------------------------------------------------------------------------
# 1) Generator schema + stable per-inventory identity
# ---------------------------------------------------------------------------
GEN = "src/generate_asset_inventory.py"

replace_once(
    GEN,
    '    "annual_report": {"group": "Documentation", "type": "select", "label": "Annual Report", "options": ["Yes", "No", "N/A"]},\n    \n    # Notes\n',
    '''    "annual_report": {"group": "Documentation", "type": "select", "label": "Annual Report", "options": ["Yes", "No", "N/A"]},\n\n    # Emergency & Handoff\n    "emergency_priority": {"group": "Emergency & Handoff", "type": "select", "label": "Emergency Priority", "options": ["", "Critical", "Important", "Routine"]},\n    "access_location": {"group": "Emergency & Handoff", "type": "text", "label": "Access / Recovery Location"},\n    "access_recovery_contact": {"group": "Emergency & Handoff", "type": "text", "label": "Recovery Contact"},\n    "incapacity_access": {"group": "Emergency & Handoff", "type": "select", "label": "Incapacity Access", "options": ["", "Ready", "Partial", "Blocked", "Not applicable"]},\n    "death_access": {"group": "Emergency & Handoff", "type": "select", "label": "Death Access", "options": ["", "Ready", "Partial", "Blocked", "Not applicable"]},\n    "handoff_instructions": {"group": "Emergency & Handoff", "type": "textarea", "label": "Handoff Instructions"},\n    "last_access_test": {"group": "Emergency & Handoff", "type": "date", "label": "Last Access Test"},\n    "next_access_review": {"group": "Emergency & Handoff", "type": "date", "label": "Next Access Review"},\n    \n    # Notes\n''',
)

replace_once(
    GEN,
    '                "annual_report": "",\n                "notes": "",\n',
    '''                "annual_report": "",\n                "emergency_priority": "",\n                "access_location": "",\n                "access_recovery_contact": "",\n                "incapacity_access": "",\n                "death_access": "",\n                "handoff_instructions": "",\n                "last_access_test": "",\n                "next_access_review": "",\n                "notes": "",\n''',
)

replace_once(
    GEN,
    '    inventory = {\n        "format": "asset-inventory",\n        "version": 2,\n        "schema_version": 1,\n',
    '''    inventory_id = "INV-" + hashlib.sha256(\n        f"{tier}|{lang}|{buyer or 'unbound-family'}".encode("utf-8")\n    ).hexdigest()[:12].upper()\n    inventory = {\n        "format": "asset-inventory",\n        "version": 2,\n        "schema_version": 2,\n        "inventory_id": inventory_id,\n''',
)

# ---------------------------------------------------------------------------
# 2) Bilingual strings
# ---------------------------------------------------------------------------
TR = "src/translations.py"

replace_once(
    TR,
    '        "save_guide_direct": "Download copy to Downloads folder",\n',
    '''        "save_guide_direct": "Download copy to Downloads folder",\n        "save_as": "Save As",\n        "direct_save_success": "Saved directly to the bound inventory file",\n        "direct_save_mismatch": "Save blocked: the selected file belongs to a different inventory",\n        "inventory_id_label": "Inventory ID",\n        "layout_review": "Annual Review",\n        "review_title": "Annual Family Review",\n        "review_subtitle": "Continuity, access readiness and review-due items",\n        "review_overall_readiness": "Overall Access Readiness",\n        "review_due": "Review Due / Overdue",\n        "review_critical_assets": "Critical Handoff Assets",\n        "review_access_gaps": "Access Gaps",\n        "review_no_gaps": "No material access gaps found",\n        "review_incapacity": "Incapacity Path",\n        "review_death": "Death Path",\n        "review_access_test": "Access Test",\n        "review_score": "Readiness Score",\n        "emergency_handoff": "Emergency & Handoff",\n        "print_emergency_guide": "Emergency Access Guide",\n        "print_master_index": "Master Asset Index",\n        "print_inventory_id": "Inventory ID",\n        "print_access_score": "Access Score",\n        "print_incapacity_path": "If the owner is incapacitated",\n        "print_death_path": "If the owner has died",\n        "print_no_passwords": "This guide identifies where recovery information is kept. It intentionally does not print passwords or secret recovery phrases.",\n        "print_recovery_contact": "Recovery Contact",\n        "print_access_location": "Access / Recovery Location",\n        "audit_access_critical": "Access readiness is critically low",\n        "audit_access_attention": "Access readiness needs attention",\n        "audit_incapacity_missing": "Incapacity access path is not ready",\n        "audit_death_missing": "Death access path is not ready",\n        "audit_access_test_stale": "Access path has not been tested in the last 12 months",\n''',
)

replace_once(
    TR,
    '        "save_guide_direct": "下载副本到下载文件夹",\n',
    '''        "save_guide_direct": "下载副本到下载文件夹",\n        "save_as": "另存为",\n        "direct_save_success": "已直接保存到绑定的资产清单文件",\n        "direct_save_mismatch": "已阻止保存：所选文件属于另一份资产清单",\n        "inventory_id_label": "清单编号",\n        "layout_review": "年度复核",\n        "review_title": "家庭年度复核",\n        "review_subtitle": "接管连续性、访问准备度与到期复核项目",\n        "review_overall_readiness": "整体访问准备度",\n        "review_due": "到期 / 逾期复核",\n        "review_critical_assets": "关键接管资产",\n        "review_access_gaps": "访问缺口",\n        "review_no_gaps": "未发现重大访问缺口",\n        "review_incapacity": "失能接管路径",\n        "review_death": "身故接管路径",\n        "review_access_test": "访问测试",\n        "review_score": "准备度评分",\n        "emergency_handoff": "紧急接管与交接",\n        "print_emergency_guide": "紧急访问指南",\n        "print_master_index": "资产总索引",\n        "print_inventory_id": "清单编号",\n        "print_access_score": "访问评分",\n        "print_incapacity_path": "所有者失能时",\n        "print_death_path": "所有者身故时",\n        "print_no_passwords": "本指南仅说明恢复资料存放位置，不打印密码、助记词或其他秘密恢复信息。",\n        "print_recovery_contact": "恢复联系人",\n        "print_access_location": "访问 / 恢复资料位置",\n        "audit_access_critical": "访问准备度严重不足",\n        "audit_access_attention": "访问准备度需要完善",\n        "audit_incapacity_missing": "失能接管路径尚未就绪",\n        "audit_death_missing": "身故接管路径尚未就绪",\n        "audit_access_test_stale": "访问路径超过 12 个月未测试",\n''',
)

replace_once(
    TR,
    '        "documentation": "Documentation",\n        "notes": "Notes",\n',
    '        "documentation": "Documentation",\n        "emergency_handoff": "Emergency & Handoff",\n        "notes": "Notes",\n',
)
replace_once(
    TR,
    '        "documentation": "文件",\n        "notes": "备注",\n',
    '        "documentation": "文件",\n        "emergency_handoff": "紧急接管与交接",\n        "notes": "备注",\n',
)

replace_once(
    TR,
    '        "col_annual_report": "Annual Report",\n        "col_notes": "Notes",\n',
    '''        "col_annual_report": "Annual Report",\n        "col_emergency_priority": "Emergency Priority",\n        "col_access_location": "Access / Recovery Location",\n        "col_access_recovery_contact": "Recovery Contact",\n        "col_incapacity_access": "Incapacity Access",\n        "col_death_access": "Death Access",\n        "col_handoff_instructions": "Handoff Instructions",\n        "col_last_access_test": "Last Access Test",\n        "col_next_access_review": "Next Access Review",\n        "col_notes": "Notes",\n''',
)
replace_once(
    TR,
    '        "col_annual_report": "年度报告",\n        "col_notes": "备注",\n',
    '''        "col_annual_report": "年度报告",\n        "col_emergency_priority": "紧急优先级",\n        "col_access_location": "访问 / 恢复资料位置",\n        "col_access_recovery_contact": "恢复联系人",\n        "col_incapacity_access": "失能访问",\n        "col_death_access": "身故访问",\n        "col_handoff_instructions": "交接说明",\n        "col_last_access_test": "最近访问测试",\n        "col_next_access_review": "下次访问复核",\n        "col_notes": "备注",\n''',
)

replace_once(
    TR,
    '        "help_save_html": "Save HTML — download the current dashboard as a self-contained HTML file, including any edits you have made",\n',
    '        "help_save_html": "Save HTML — Chrome/Edge can save directly back to a bound inventory file; other browsers keep the staged Ctrl+S/download fallback",\n',
)
replace_once(
    TR,
    '        "help_save_html": "保存 HTML — 下载包含所有编辑内容的自包含 HTML 文件",\n',
    '        "help_save_html": "保存 HTML — Chrome/Edge 可直接保存回已绑定的资产清单文件；其他浏览器继续使用暂存 + Ctrl+S/下载回退",\n',
)

# Teach group translator about the new group.
replace_once(
    TR,
    '        "Documentation": _("documentation", lang),\n        "Notes": _("notes", lang),\n',
    '        "Documentation": _("documentation", lang),\n        "Emergency & Handoff": _("emergency_handoff", lang),\n        "Notes": _("notes", lang),\n',
)

# ---------------------------------------------------------------------------
# 3) Dashboard: Direct Save, binding, readiness, print handoff, annual review
# ---------------------------------------------------------------------------
TPL = "templates/dashboard.html"

# CSS
replace_once(
    TPL,
    '/* ===== HEADER ===== */\n',
    '''/* ===== CONTINUITY / REVIEW ===== */\n.review-view { display: none; }\n.review-view.active { display: block; }\n.review-hero { display:flex; gap:20px; align-items:center; padding:22px; background:var(--card); border:1px solid var(--border); border-radius:var(--radius-lg); margin-bottom:18px; }\n.readiness-score { width:92px; height:92px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-direction:column; border:8px solid var(--accent-light); font-weight:700; font-size:24px; }\n.readiness-score small { font-size:10px; color:var(--muted); font-weight:500; }\n.review-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-bottom:18px; }\n.review-card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:16px; }\n.review-card .metric { font-size:28px; font-weight:700; margin-top:6px; }\n.review-list { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; }\n.review-row { display:grid; grid-template-columns:minmax(180px,1.5fr) 90px 1fr 1fr; gap:12px; padding:11px 14px; border-top:1px solid var(--border-light); align-items:center; font-size:13px; }\n.review-row:first-child { border-top:0; }\n.review-pill { display:inline-flex; align-items:center; justify-content:center; padding:3px 8px; border-radius:999px; background:var(--surface); font-size:11px; font-weight:600; }\n.inventory-id-chip { font-size:10px; color:var(--muted); white-space:nowrap; }\n@media (max-width:760px) { .review-row { grid-template-columns:1fr 72px; } .review-row .review-path { grid-column:1 / -1; } .inventory-id-chip { display:none; } }\n\n/* ===== HEADER ===== */\n''',
)

# Save-As control and visible inventory identity.
replace_once(
    TPL,
    '        <button class="btn btn-primary" id="saveHTML">{{TR_save_html}}</button>\n',
    '''        <span class="inventory-id-chip" id="inventoryIdChip" title="{{TR_inventory_id_label}}"></span>\n        <button class="btn" id="saveAsHTML" title="{{TR_save_as}}">{{TR_save_as}}</button>\n        <button class="btn btn-primary" id="saveHTML">{{TR_save_html}}</button>\n''',
)

# Planning Annual Review layout button.
replace_once(
    TPL,
    '''            <!--__/TIER_GE:planning-->\n            <!--__TIER_GE:family-->\n            <button class="layout-btn" data-layout="charts"''',
    '''            <!--__/TIER_GE:planning-->\n            <!--__TIER_GE:planning-->\n            <button class="layout-btn" data-layout="review" title="{{TR_layout_review}}" aria-label="{{TR_layout_review}}">\n                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 3h10v10H3z"/><path d="M5 6h6M5 9h4"/></svg>\n            </button>\n            <!--__/TIER_GE:planning-->\n            <!--__TIER_GE:family-->\n            <button class="layout-btn" data-layout="charts"''',
)

# Planning review view container.
replace_once(
    TPL,
    '''        <!-- Audit View -->\n        <div class="audit-view" id="auditView"></div>\n        \n        <!-- Charts View -->''',
    '''        <!-- Audit View -->\n        <div class="audit-view" id="auditView"></div>\n\n        <!--__TIER_GE:planning-->\n        <!-- Annual Review View -->\n        <div class="review-view" id="reviewView"></div>\n        <!--__/TIER_GE:planning-->\n        \n        <!-- Charts View -->''',
)

# Field-group order.
replace_once(
    TPL,
    '    "{{TR_documentation}}": ["document_path", "document_reference", "last_statement", "statement_frequency", "tax_slip_type", "tax_slip_received", "annual_report"],\n    "{{TR_notes}}": ["notes", "alert", "todo", "last_modified_by", "source"]\n',
    '    "{{TR_documentation}}": ["document_path", "document_reference", "last_statement", "statement_frequency", "tax_slip_type", "tax_slip_received", "annual_report"],\n    "{{TR_emergency_handoff}}": ["emergency_priority", "access_location", "access_recovery_contact", "incapacity_access", "death_access", "handoff_instructions", "last_access_test", "next_access_review"],\n    "{{TR_notes}}": ["notes", "alert", "todo", "last_modified_by", "source"]\n',
)

# Tier feature map + runtime gating.
replace_once(
    TPL,
    "    free:    { table:false, timeline:false, charts:false, audit:false, print:false,\n               export:false, templates:1,  templatesList:['estateon'] },\n    family:  { table:true,  timeline:true,  charts:true,  audit:false, print:true,\n               export:false, templates:5,  templatesList:['estateon','lumina','cardinal','atlantic','monarch'] },\n    planning:{ table:true,  timeline:true,  charts:true,  audit:true,  print:true,\n               export:true,  templates:5,  templatesList:['estateon','lumina','cardinal','atlantic','monarch'] },",
    "    free:    { table:false, timeline:false, charts:false, audit:false, review:false, print:false,\n               export:false, templates:1,  templatesList:['estateon'] },\n    family:  { table:true,  timeline:true,  charts:true,  audit:false, review:false, print:true,\n               export:false, templates:5,  templatesList:['estateon','lumina','cardinal','atlantic','monarch'] },\n    planning:{ table:true,  timeline:true,  charts:true,  audit:true,  review:true, print:true,\n               export:true,  templates:5,  templatesList:['estateon','lumina','cardinal','atlantic','monarch'] },",
)
replace_once(
    TPL,
    "    const layoutGate = { table: tierHas('table'), timeline: tierHas('timeline'),\n                         audit: tierHas('audit'), charts: tierHas('charts') };",
    "    const layoutGate = { table: tierHas('table'), timeline: tierHas('timeline'),\n                         audit: tierHas('audit'), review: tierHas('review'), charts: tierHas('charts') };",
)

# Layout mapping / rendering. Marker comments are removed at build time.
replace_once(
    TPL,
    "        audit: 'auditView',\n        charts: 'chartsView'",
    "        audit: 'auditView',\n        <!--__TIER_GE:planning-->\n        review: 'reviewView',\n        <!--__/TIER_GE:planning-->\n        charts: 'chartsView'",
)
replace_once(
    TPL,
    "        case 'audit': if (tierHas('audit')) renderAudit(); else renderDashboard(); break;\n        case 'charts': if (tierHas('charts')) renderCharts(); else renderDashboard(); break;",
    "        case 'audit': if (tierHas('audit')) renderAudit(); else renderDashboard(); break;\n        <!--__TIER_GE:planning-->\n        case 'review': if (tierHas('review')) renderAnnualReview(); else renderDashboard(); break;\n        <!--__/TIER_GE:planning-->\n        case 'charts': if (tierHas('charts')) renderCharts(); else renderDashboard(); break;",
)

# Direct Save replaces the old save-button branch while retaining the old staged/download fallback.
regex_once(
    TPL,
    r'// Save button: stage data, then branch by browser\.\nasync function saveCurrentData\(\) \{.*?\n\}\n\nfunction showSaveGuide\(\) \{',
    r'''// Save button: prefer File System Access direct-save in Chromium; preserve\n// the staged Ctrl+S/download model as a complete fallback.  A selected existing\n// target must carry the same inventory_id, preventing accidental cross-family overwrite.\nlet saveFileHandle = null;\n\nfunction supportsDirectFileSave() {\n    return typeof window.showSaveFilePicker === 'function' && !isSafari();\n}\n\nfunction extractInventoryId(html) {\n    const m = String(html || '').match(/"inventory_id"\\s*:\\s*"([^"]+)"/);\n    return m ? m[1] : '';\n}\n\nasync function buildSavedHTML() {\n    await stageDataToScript();\n    return '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;\n}\n\nasync function directSaveCurrentFile(forcePicker = false) {\n    const html = await buildSavedHTML();\n    let handle = saveFileHandle;\n    if (!handle || forcePicker) {\n        handle = await window.showSaveFilePicker({\n            suggestedName: '{{TR_export_html_filename}}',\n            types: [{ description: 'HTML', accept: { 'text/html': ['.html', '.htm'] } }]\n        });\n        let existing = '';\n        try { existing = await (await handle.getFile()).text(); } catch (_) {}\n        if (existing.trim()) {\n            const targetId = extractInventoryId(existing);\n            const currentId = INVENTORY_DATA.inventory_id || '';\n            if (!targetId || !currentId || targetId !== currentId) {\n                showToast('{{TR_direct_save_mismatch}}');\n                return false;\n            }\n        }\n        saveFileHandle = handle;\n    }\n    const writable = await handle.createWritable();\n    await writable.write(html);\n    await writable.close();\n    saveToLocalStorage();\n    clearDirty();\n    showToast('{{TR_direct_save_success}}');\n    return true;\n}\n\nasync function saveCurrentData(forcePicker = false) {\n    await stageDataToScript();\n    saveToLocalStorage();\n    if (supportsDirectFileSave()) {\n        try {\n            await directSaveCurrentFile(forcePicker);\n            return;\n        } catch (e) {\n            if (e && e.name === 'AbortError') return;\n            console.warn('Direct Save unavailable; using staged fallback', e);\n        }\n    }\n    if (isSafari()) {\n        const html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;\n        downloadFile(html, '{{TR_export_html_filename}}', 'text/html');\n        clearDirty();\n        showToast('{{TR_html_saved}}');\n        return;\n    }\n    showSaveGuide();\n}\n\nfunction showSaveGuide() {''',
    flags=re.S,
)

# Bind Save As and surface inventory id.
replace_once(
    TPL,
    "    document.getElementById('saveHTML').addEventListener('click', saveCurrentData);\n",
    "    document.getElementById('saveHTML').addEventListener('click', () => saveCurrentData(false));\n    document.getElementById('saveAsHTML').addEventListener('click', () => saveCurrentData(true));\n    const invChip = document.getElementById('inventoryIdChip');\n    if (invChip) invChip.textContent = (INVENTORY_DATA.inventory_id || '').replace('INV-', '#');\n",
)

# Family+ access readiness engine: usable by print and Planning audit/review.
replace_once(
    TPL,
    '<!--__TIER_GE:family-->\n// ===== PRINT VIEW (ESTATE BINDER) =====\n',
    '''<!--__TIER_GE:family-->\n// ===== ACCESS READINESS (Family print + Planning intelligence) =====\nfunction accessReadiness(a) {\n    let score = 0;\n    const gaps = [];\n    const hasLocator = !!(a.access_location || a.login_url || a.online_access_url || a.physical_location ||\n        a.safe_deposit_box || a.digital_wallet || a.account_number);\n    const hasContact = !!(a.access_recovery_contact || a.support_contact || a.advisor_contact || a.poa);\n    const hasInstructions = !!(a.handoff_instructions || a.document_path || a.document_reference);\n    if (a.institution || a.physical_location || a.exchange) score += 15; else gaps.push('{{TR_audit_missing_institution}}');\n    if (hasLocator) score += 20; else gaps.push('{{TR_print_access_location}}');\n    if (hasContact) score += 15; else gaps.push('{{TR_print_recovery_contact}}');\n    if (hasInstructions) score += 15; else gaps.push('{{TR_col_handoff_instructions}}');\n    if (a.incapacity_access === 'Ready' || a.incapacity_access === 'Not applicable') score += 15; else gaps.push('{{TR_audit_incapacity_missing}}');\n    if (a.death_access === 'Ready' || a.death_access === 'Not applicable') score += 15; else gaps.push('{{TR_audit_death_missing}}');\n    if (a.last_access_test) {\n        const t = Date.parse(a.last_access_test);\n        if (!isNaN(t) && (Date.now() - t) <= 365 * 24 * 3600 * 1000) score += 5;\n        else gaps.push('{{TR_audit_access_test_stale}}');\n    } else {\n        gaps.push('{{TR_audit_access_test_stale}}');\n    }\n    return { score: Math.min(100, score), gaps };\n}\n\nfunction accessScoreClass(score) { return score < 40 ? 'red' : (score < 70 ? 'yellow' : 'green'); }\n\n// ===== PRINT VIEW (ESTATE BINDER) =====\n''',
)

# Planning audit consumes readiness.
replace_once(
    TPL,
    '''    }\n    return findings;\n}\n\nfunction renderAudit() {''',
    '''    }\n    const readiness = accessReadiness(a);\n    if (readiness.score < 40) findings.push({ level: 'red', message: '{{TR_audit_access_critical}}' + ` (${readiness.score}/100)` });\n    else if (readiness.score < 70) findings.push({ level: 'yellow', message: '{{TR_audit_access_attention}}' + ` (${readiness.score}/100)` });\n    if (a.incapacity_access === 'Blocked') findings.push({ level: 'red', message: '{{TR_audit_incapacity_missing}}' });\n    if (a.death_access === 'Blocked') findings.push({ level: 'red', message: '{{TR_audit_death_missing}}' });\n    return findings;\n}\n\nfunction renderAudit() {''',
)

# Annual Review is injected at the end of the Planning audit block.
replace_once(
    TPL,
    '''    container.innerHTML = html;\n}\n<!--__/TIER_GE:planning-->\n\n<!--__TIER_GE:family-->\n// ===== CHARTS VIEW (pure SVG, no library) =====''',
    '''    container.innerHTML = html;\n}\n\nfunction renderAnnualReview() {\n    const container = document.getElementById('reviewView');\n    if (!container) return;\n    const rows = assets.map(a => ({ asset: a, ready: accessReadiness(a) }));\n    const avg = rows.length ? Math.round(rows.reduce((s, r) => s + r.ready.score, 0) / rows.length) : 0;\n    const now = Date.now();\n    const due = rows.filter(r => {\n        const raw = r.asset.next_access_review || r.asset.next_review || r.asset.last_update;\n        const t = Date.parse(raw || '');\n        return !raw || (!isNaN(t) && t <= now);\n    });\n    const critical = rows.filter(r => r.asset.emergency_priority === 'Critical' || r.ready.score < 40);\n    const gaps = rows.filter(r => r.ready.gaps.length > 0);\n    const sorted = [...rows].sort((a,b) => a.ready.score - b.ready.score).slice(0, 30);\n    container.innerHTML = `\n        <div class="review-hero">\n            <div class="readiness-score"><span>${avg}</span><small>/ 100</small></div>\n            <div><h2>{{TR_review_title}}</h2><p class="text-muted">{{TR_review_subtitle}}</p>\n            <p class="text-muted">{{TR_inventory_id_label}}: ${escapeHtml(INVENTORY_DATA.inventory_id || '')}</p></div>\n        </div>\n        <div class="review-grid">\n            <div class="review-card"><div>{{TR_review_overall_readiness}}</div><div class="metric">${avg}/100</div></div>\n            <div class="review-card"><div>{{TR_review_due}}</div><div class="metric">${due.length}</div></div>\n            <div class="review-card"><div>{{TR_review_critical_assets}}</div><div class="metric">${critical.length}</div></div>\n            <div class="review-card"><div>{{TR_review_access_gaps}}</div><div class="metric">${gaps.length}</div></div>\n        </div>\n        <div class="review-list">\n            ${sorted.length ? sorted.map(r => `\n                <div class="review-row" data-review-id="${escapeHtml(r.asset.id)}">\n                    <div><strong>${escapeHtml(r.asset.asset_name || r.asset.id)}</strong><br><span class="text-muted">${escapeHtml(r.asset.owner || '')}</span></div>\n                    <div><span class="review-pill">${r.ready.score}/100</span></div>\n                    <div class="review-path">{{TR_review_incapacity}}: ${escapeHtml(r.asset.incapacity_access || '—')}</div>\n                    <div class="review-path">{{TR_review_death}}: ${escapeHtml(r.asset.death_access || '—')}</div>\n                </div>`).join('') : emptyStateHTML('{{TR_review_no_gaps}}', '')}\n        </div>`;\n}\n<!--__/TIER_GE:planning-->\n\n<!--__TIER_GE:family-->\n// ===== CHARTS VIEW (pure SVG, no library) =====''',
)

# Print: Emergency Access Guide first, Master Asset Index second, then existing binder.
replace_once(
    TPL,
    "    const dateStr = new Date().toLocaleDateString('{{TR_locale}}');\n    \n    const cover = `",
    "    const dateStr = new Date().toLocaleDateString('{{TR_locale}}');\n    const continuityRows = assets.map(a => ({ asset: a, ready: accessReadiness(a) }));\n    const criticalRows = continuityRows.filter(r => r.asset.emergency_priority === 'Critical' || r.ready.score < 40).slice(0, 20);\n    const recoveryContacts = [...new Set(assets.map(a => a.access_recovery_contact).filter(Boolean))].slice(0, 8);\n    const emergencyPage = `\n        <div class=\"print-cover print-emergency-guide\">\n            <h1>{{TR_print_emergency_guide}}</h1>\n            <div class=\"print-cover-meta\">{{TR_print_inventory_id}}: ${escapeHtml(INVENTORY_DATA.inventory_id || '')}<br>${dateStr}</div>\n            <h3>{{TR_print_incapacity_path}}</h3>\n            <ol><li>Locate the POA / authority documents referenced in this inventory.</li><li>Use the recovery location and recovery contact below for each critical asset.</li><li>Contact the institution directly and follow its incapacity process.</li></ol>\n            <h3>{{TR_print_death_path}}</h3>\n            <ol><li>Locate the will / executor authority and death certificate.</li><li>Use the Master Asset Index to identify institutions, policies and account references.</li><li>Follow each institution's estate process; preserve records for tax and probate work.</li></ol>\n            <p><strong>{{TR_print_recovery_contact}}:</strong> ${recoveryContacts.map(escapeHtml).join('; ') || '—'}</p>\n            <p class=\"print-warning\">{{TR_print_no_passwords}}</p>\n            ${criticalRows.length ? `<h3>{{TR_review_critical_assets}}</h3><ul>${criticalRows.map(r => `<li>${escapeHtml(r.asset.asset_name || '')} — ${r.ready.score}/100 — ${escapeHtml(r.asset.access_location || r.asset.document_path || '—')}</li>`).join('')}</ul>` : ''}\n        </div>`;\n    const masterIndex = `\n        <div class=\"print-section print-master-index\">\n            <h2>{{TR_print_master_index}}</h2>\n            <div>{{TR_print_inventory_id}}: ${escapeHtml(INVENTORY_DATA.inventory_id || '')}</div>\n            <table class=\"print-table\"><tr><th>{{TR_id}}</th><th>{{TR_asset_name}}</th><th>{{TR_owner}}</th><th>{{TR_institution}}</th><th>{{TR_col_account_number}}</th><th>{{TR_print_access_score}}</th></tr>\n            ${continuityRows.map(r => `<tr><td>${escapeHtml(r.asset.id || '')}</td><td>${escapeHtml(r.asset.asset_name || '')}</td><td>${escapeHtml(r.asset.owner || '')}</td><td>${escapeHtml(r.asset.institution || r.asset.physical_location || '')}</td><td>${escapeHtml(maskAccount(r.asset.account_number || r.asset.insurance_policy || ''))}</td><td>${r.ready.score}/100</td></tr>`).join('')}\n            </table>\n        </div>`;\n    \n    const cover = `",
)
replace_once(
    TPL,
    '    el.innerHTML = cover + toc + sections + beneficiarySection + insuranceSection;\n',
    '    el.innerHTML = emergencyPage + masterIndex + cover + toc + sections + beneficiarySection + insuranceSection;\n',
)

# ---------------------------------------------------------------------------
# 4) E2E coverage
# ---------------------------------------------------------------------------
TEST = "tests/e2e_visual_test.py"

replace_once(
    TEST,
    '        "free":    {"assets": 256, "tpl": 1, "table": False, "timeline": False,\n                    "charts": False, "audit": False, "print": False, "export": False},\n        "family":  {"assets": 324, "tpl": 5, "table": True, "timeline": True,\n                    "charts": True, "audit": False, "print": True, "export": False},\n        "planning": {"assets": 517, "tpl": 5, "table": True, "timeline": True,\n                     "charts": True, "audit": True, "print": True, "export": True},\n',
    '        "free":    {"assets": 256, "tpl": 1, "table": False, "timeline": False,\n                    "charts": False, "audit": False, "review": False, "print": False, "export": False},\n        "family":  {"assets": 324, "tpl": 5, "table": True, "timeline": True,\n                    "charts": True, "audit": False, "review": False, "print": True, "export": False},\n        "planning": {"assets": 517, "tpl": 5, "table": True, "timeline": True,\n                     "charts": True, "audit": True, "review": True, "print": True, "export": True},\n',
)

# Add static artifact assertions after template-marker check.
replace_once(
    TEST,
    '    check("template tier markers balanced & nested", marker_ok and not stack,\n          f"unclosed={stack}")\n\n    # Markdown\n',
    '    check("template tier markers balanced & nested", marker_ok and not stack,\n          f"unclosed={stack}")\n\n    en_html = EN_HTML.read_text(encoding="utf-8")\n    zh_html = ZH_HTML.read_text(encoding="utf-8")\n    check("inventory identity embedded", \'"inventory_id": "INV-\' in en_html)\n    check("direct-save API path compiled", "showSaveFilePicker" in en_html and "directSaveCurrentFile" in en_html)\n    check("planning annual-review layout compiled", \'data-layout="review"\' in en_html and "renderAnnualReview" in en_html)\n    check("handoff schema fields compiled", all(k in en_html for k in ["emergency_priority", "incapacity_access", "death_access", "last_access_test"]))\n    check("zh continuity strings compiled", "紧急访问指南" in zh_html and "家庭年度复核" in zh_html)\n\n    # Markdown\n',
)

# Existing print check: add continuity binder checks immediately after it.
replace_once(
    TEST,
    '    check("en: print view populated", print_html is not None and len(print_html) > 500)\n\n    # ---- Quick-add wizard (3.7) ----\n',
    '    check("en: print view populated", print_html is not None and len(print_html) > 500)\n    check("en: emergency access guide is first print section",\n          page.locator("#printView").inner_text().find("Emergency Access Guide") >= 0\n          and page.locator("#printView").inner_text().find("Emergency Access Guide") < page.locator("#printView").inner_text().find("Master Asset Index"))\n    check("en: master asset index printed", "Master Asset Index" in page.locator("#printView").inner_text())\n    check("en: print includes inventory id", "INV-" in page.locator("#printView").inner_text())\n\n    # ---- Continuity / access readiness ----\n    current_inv_id = page.evaluate("INVENTORY_DATA.inventory_id")\n    check("en: inventory id format", bool(re.match(r"^INV-[A-F0-9]{12}$", current_inv_id or "")), current_inv_id)\n    check("en: inventory binding extracts same id",\n          page.evaluate("extractInventoryId(document.documentElement.outerHTML)") == current_inv_id)\n    check("en: save-as control present", page.locator("#saveAsHTML").count() == 1)\n    ready_score = page.evaluate("accessReadiness({institution:\'TD\',access_location:\'vault\',access_recovery_contact:\'Jane\',handoff_instructions:\'call TD\',incapacity_access:\'Ready\',death_access:\'Ready\',last_access_test:new Date().toISOString().slice(0,10)}).score")\n    check("en: fully prepared access path scores 100", ready_score == 100, str(ready_score))\n    weak_score = page.evaluate("accessReadiness({}).score")\n    check("en: empty access path scores critically low", weak_score < 40, str(weak_score))\n    _layout(page, "review")\n    page.wait_for_timeout(300)\n    check("en: annual review renders", page.locator("#reviewView .review-hero").count() == 1)\n    check("en: annual review lists readiness rows", page.locator("#reviewView .review-row").count() > 0)\n    _layout(page, "dashboard")\n    _open_modal(page, "A-0001")\n    check("en: handoff fields available in editor",\n          all(page.locator(f\'#modalContent [data-field="{f}"]\').count() == 1 for f in ["emergency_priority", "incapacity_access", "death_access", "handoff_instructions", "last_access_test"]))\n    page.click("#modalClose")\n    page.wait_for_timeout(200)\n\n    # ---- Quick-add wizard (3.7) ----\n',
)

# ---------------------------------------------------------------------------
# 5) Documentation / versioning / admin guidance
# ---------------------------------------------------------------------------
FEATURE = "docs/dev/feature_list.md"
f = read(FEATURE)
f = re.sub(r'Last updated [0-9-]+ [0-9:]+', f'Last updated {STAMP}', f, count=1)
f = f.replace('108-field schema per asset', '116-field schema per asset')
f = f.replace('8 layouts: Dashboard, Table, Kanban, Timeline, Detail, Compact, Audit, Charts', '9 layouts: Dashboard, Table, Kanban, Timeline, Detail, Compact, Audit, Annual Review, Charts')
f = f.replace('all 108 fields', 'all 116 fields')
f = f.replace('cover, per-category sections, beneficiary/insurance summaries', 'Emergency Access Guide (page 1), Master Asset Index, cover, per-category sections, beneficiary/insurance summaries')
f = f.replace('Save model: stage data into DOM script → native Ctrl+S guidance (Chromium/Firefox) or direct-download fallback (Safari auto-detected)', 'Direct Save: Chromium File System Access API writes back to a user-selected bound file; Inventory ID prevents cross-inventory overwrite; staged Ctrl+S/download remains the fallback')
f = f.replace('| 7.1 | Audit view — traffic-light validation: missing beneficiary (red), missing FMV/ACB/institution/owner (yellow), bad selects, TFSA over-contribution, stale >12 months | ✅ |', '| 7.1 | Audit view — traffic-light validation incl. beneficiary/value/data quality plus Access Readiness and blocked incapacity/death paths | ✅ |\n| 7.2 | Access Readiness score (0–100) from locator, recovery contact, handoff instructions, incapacity/death readiness and annual access test | ✅ |\n| 7.3 | Annual Family Review layout — overall score, due/overdue reviews, critical handoff assets and access gaps | ✅ |\n| 7.4 | Emergency & Handoff schema — priority, recovery location/contact, incapacity/death paths, instructions, last test/next review | ✅ |')
f = re.sub(r'End-to-end visual test — \d+ checks:', 'End-to-end visual test — __E2E_CHECKS__ checks:', f, count=1)
write(FEATURE, f)

# Versioning plan: update schema and save-model decision.
VP = "docs/dev/versioning_plan.md"
v = read(VP)
v = re.sub(r'Last updated [0-9-]+ [0-9:]+', f'Last updated {STAMP}', v, count=1)
v = v.replace('**Data storage (`INVENTORY_DATA`)', '**Data storage (`INVENTORY_DATA`)') if False else v
v = v.replace('"schema_version": 1,     // 108-field schema version', '"schema_version": 2,     // 116-field schema incl. Emergency & Handoff')
v = v.replace('"tier": "free",          // free | family | planning | advisor', '"inventory_id": "INV-…", // stable file/family binding identity\n  "tier": "free",          // free | family | planning | advisor')
v = v.replace('**108-field schema identical across tiers**', '**116-field schema identical across tiers**')
v = v.replace('**Save model (the core UX fix):** the browser cannot write back to a `file://` document, so\n   "Save" = **stage data into the DOM data script, then let the user use native Ctrl+S** to\n   choose where to save. Safari gets a download fallback.', '**Save model:** Chrome/Edge use the File System Access API for explicit user-selected Direct Save when available. Every selected existing target is verified against the embedded `inventory_id` before overwrite. Firefox/Safari and denied API contexts retain the staged Ctrl+S / direct-download fallback.')
v = v.replace('**Principle:** browsers cannot write back to the open `file://` document. The user\'s most\nfamiliar save is native **Ctrl+S / Cmd+S** (dialog lets them choose location/name). So:', '**Principle:** use the strongest browser-supported persistence path while keeping a complete offline fallback. Chromium Direct Save is preferred; staged native save/download remains universal.')
v = v.replace('1. Every edit / auto-save updates the DOM data script to the latest payload', '1. Every edit / auto-save updates the DOM data script to the latest payload')
# Append authoritative direct-save/binding note instead of relying on old browser table alone.
v += f'''\n\n## 4a. Direct Save + inventory binding (shipped {STAMP})\n\n- Chrome/Edge: Save opens a File System Access picker on first use, then reuses that in-session handle for direct writes. **Save As** always asks for a target.\n- Before overwriting an existing target, the dashboard extracts its `inventory_id`; a mismatch or missing ID is blocked. This prevents accidentally saving Family A into Family B's inventory file.\n- Firefox/Safari/API-denied contexts retain stage-to-DOM + Ctrl/Cmd+S and direct-download fallbacks.\n- `inventory_id` is embedded in the versioned data block and printed on the Emergency Access Guide / Master Asset Index.\n- Schema v2 adds eight Emergency & Handoff fields while remaining identical across Free/Family/Planning tiers.\n'''
write(VP, v)

# README, roadmap, admin guide append concise shipped guidance.
for rel, block in {
    "README.md": f'''\n\n## Direct Save & Estate Continuity (2026-08-19)\n\n- Chromium Direct Save uses the File System Access API; **Inventory ID binding blocks accidental overwrite of another family's inventory**. Save As explicitly selects a new target. Firefox/Safari retain the staged Ctrl/Cmd+S/download fallback.\n- Schema v2 has 116 fields, adding Emergency Priority, recovery location/contact, incapacity/death readiness, handoff instructions, last access test, and next access review.\n- Family/Planning print binders start with an **Emergency Access Guide** and **Master Asset Index**. Passwords and secret recovery phrases are intentionally excluded from print.\n- Planning adds Access Readiness scoring and an Annual Family Review layout.\n''',
    "docs/dev/future_plan.md": f'''\n\n## Shipped continuity tranche — {STAMP}\n\n✅ Direct Save with File System Access API + Inventory ID binding and fallback save model.  \n✅ Emergency & Handoff schema and incapacity/death access paths.  \n✅ Family/Planning Emergency Access Guide + Master Asset Index print front matter.  \n✅ Planning Access Readiness scoring + audit integration + Annual Family Review.\n''',
    "docs/user/ADMIN_GUIDE.md": f'''\n\n## Direct Save, Emergency Access & Annual Review\n\n**Direct Save (Chrome/Edge).** Click **Save**. The first save asks you to select the HTML inventory file; subsequent saves in that browser session write directly to the same bound file. **Save As** selects a different file. An existing target with a different or missing Inventory ID is blocked to prevent cross-family overwrite. Firefox/Safari continue to use the staged Ctrl/Cmd+S or download fallback.\n\n**Emergency & Handoff fields.** For important assets, set Emergency Priority, Access/Recovery Location, Recovery Contact, Incapacity Access, Death Access, Handoff Instructions, Last Access Test and Next Access Review. Store only references to credential/recovery storage in these fields; keep passwords, seed phrases and secret recovery material in the designated secure system.\n\n**Print binder.** Family and Planning print output begins with the Emergency Access Guide, followed by the Master Asset Index. Confirm these pages are current before placing a copy with the executor/attorney/POA.\n\n**Planning Annual Review.** Use the Annual Review layout at least yearly. Resolve low Access Readiness scores, blocked incapacity/death paths, overdue reviews and stale access tests.\n''',
}.items():
    txt = read(rel)
    txt = re.sub(r'Last updated [0-9-]+ [0-9:]+', f'Last updated {STAMP}', txt, count=1)
    if 'Direct Save & Estate Continuity (2026-08-19)' not in txt and 'Shipped continuity tranche' not in txt and '## Direct Save, Emergency Access & Annual Review' not in txt:
        txt += block
    write(rel, txt)

# Update ASSET_FIELDS with schema delta and timestamp.
af = read("docs/dev/ASSET_FIELDS.md")
af = re.sub(r'Last updated [0-9-]+ [0-9:]+', f'Last updated {STAMP}', af, count=1)
if 'Emergency & Handoff (8 fields)' not in af:
    af += '''\n\n## Emergency & Handoff (8 fields) — schema v2\n\n| Field | Type | Purpose |\n|---|---|---|\n| `emergency_priority` | select | Critical / Important / Routine handoff priority |\n| `access_location` | text | Location/reference for credential or recovery instructions |\n| `access_recovery_contact` | text | Person/professional who can assist recovery |\n| `incapacity_access` | select | Ready / Partial / Blocked / Not applicable |\n| `death_access` | select | Ready / Partial / Blocked / Not applicable |\n| `handoff_instructions` | textarea | Operational handoff steps without embedding secrets |\n| `last_access_test` | date | Last verified recovery/access test |\n| `next_access_review` | date | Next scheduled continuity review |\n\nThese fields are present in every tier so data files upgrade without schema migration. The Planning tier uses them for Access Readiness and Annual Review; Family/Planning print uses them for emergency handoff front matter.\n'''
write("docs/dev/ASSET_FIELDS.md", af)

# Promotion plan needs only a timestamp + shipped benefit note.
pp = read("docs/dev/promotion_plan.md")
pp = re.sub(r'Last updated [0-9-]+ [0-9:]+', f'Last updated {STAMP}', pp, count=1)
if 'Inventory ID binding' not in pp:
    pp += '''\n\n### Continuity value proposition (shipped 2026-08-19)\nDirect Save + Inventory ID binding reduces file-loss/overwrite risk; Emergency Access Guide, Master Asset Index, Access Readiness and Annual Review make the product useful for POA/executor/family handoff rather than inventorying assets only.\n'''
write("docs/dev/promotion_plan.md", pp)

# Ensure source compiles before workflow spends time installing browsers.
print("continuity migration applied")
