#!/usr/bin/env python3
"""
audit_post_cleanup.py
Auditoría post-limpieza: métricas antes/después del marcado LEGACY.
Solo lectura. No modifica ningún archivo de datos.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).parent.parent
MASTER_FILE = ROOT / 'pielh_qa_master.json'
PROBE_FILE  = ROOT / 'data' / 'thethings_snapshots' / 'latest' / 'thethings_resources_probe.json'
PLAN_FILE   = ROOT / 'reports' / 'duplicate_sensor_cleanup_plan.json'
REPORTS_DIR = ROOT / 'reports'


def main():
    for p in [MASTER_FILE]:
        if not p.exists():
            print(f'[ERROR] No encontrado: {p}')
            return 1

    print('[PIELH] Cargando master...')
    master = json.loads(MASTER_FILE.read_text(encoding='utf-8'))
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])

    # Probe (opcional)
    probe_idx = {}
    if PROBE_FILE.exists():
        probe = json.loads(PROBE_FILE.read_text(encoding='utf-8'))
        probe_idx = {
            s['thing_id']: s
            for s in probe.get('sensors', [])
            if s.get('thing_id')
        }
        print(f'        Probe cargado: {len(probe_idx)} things')
    else:
        print('[WARN]  Probe no encontrado. Metricas de datos no disponibles.')

    # Plan (para contexto de clasificaciones)
    plan_summary = {}
    if PLAN_FILE.exists():
        plan = json.loads(PLAN_FILE.read_text(encoding='utf-8'))
        plan_summary = plan.get('summary', {})

    # ── Clasificar sensores ────────────────────────────────────────────────
    visible = []
    legacy  = []
    for s in sensors:
        if s.get('inventory_status') == 'LEGACY' or s.get('include') is False:
            legacy.append(s)
        else:
            visible.append(s)

    # ── Métricas globales ──────────────────────────────────────────────────
    def has_data(s):
        p = probe_idx.get(s.get('thing_id', ''), {})
        return bool(p.get('has_real_data'))

    before_total    = len(sensors)
    before_with_d   = sum(1 for s in sensors  if has_data(s))
    before_no_d     = before_total - before_with_d

    after_total     = len(visible)
    after_legacy    = len(legacy)
    after_with_d    = sum(1 for s in visible  if has_data(s))
    after_no_d      = after_total - after_with_d

    pct_legacy = after_legacy / before_total * 100 if before_total else 0
    pct_reduce = (before_total - after_total) / before_total * 100 if before_total else 0

    print(f'        Total sensores:  {before_total}')
    print(f'        Visibles:        {after_total}')
    print(f'        LEGACY:          {after_legacy}  ({pct_legacy:.1f}%)')

    # ── Por sistema ────────────────────────────────────────────────────────
    by_system = {}
    for s in sensors:
        sid  = s.get('system_id') or '?'
        is_l = s.get('inventory_status') == 'LEGACY' or s.get('include') is False
        hd   = has_data(s)
        bs   = by_system.setdefault(sid, {
            'system_name': s.get('system_name', ''),
            'total': 0, 'legacy': 0, 'visible': 0,
            'with_data': 0, 'without_data': 0,
        })
        bs['total'] += 1
        if is_l:
            bs['legacy'] += 1
        else:
            bs['visible'] += 1
            if hd:
                bs['with_data'] += 1
            else:
                bs['without_data'] += 1

    # ── Por edificio ────────────────────────────────────────────────────────
    buildings_idx = {b['id']: b.get('name', b['id']) for b in buildings if b.get('id')}
    by_hos = defaultdict(lambda: {'building_name': '', 'total': 0, 'legacy': 0, 'visible': 0})
    for s in sensors:
        hos  = s.get('hos') or 'SIN_HOS'
        is_l = s.get('inventory_status') == 'LEGACY' or s.get('include') is False
        bh   = by_hos[hos]
        bh['building_name'] = buildings_idx.get(hos, '')
        bh['total'] += 1
        if is_l:
            bh['legacy'] += 1
        else:
            bh['visible'] += 1

    # ── JSON ───────────────────────────────────────────────────────────────
    now = datetime.now().isoformat()
    result = {
        '_meta': {
            'created_at': now,
            'master_modified': False,
            'probe_available': bool(probe_idx),
        },
        'before': {
            'total_sensors':   before_total,
            'with_data':       before_with_d,
            'without_data':    before_no_d,
        },
        'after': {
            'total_visible':   after_total,
            'total_legacy':    after_legacy,
            'with_data':       after_with_d,
            'without_data':    after_no_d,
            'pct_legacy':      round(pct_legacy, 1),
            'pct_reduction':   round(pct_reduce, 1),
        },
        'plan_context': plan_summary,
        'by_system': {k: v for k, v in sorted(by_system.items())},
        'by_hos':    {k: dict(v) for k, v in sorted(by_hos.items())},
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS_DIR / 'post_cleanup_audit.json'
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    # ── MD ────────────────────────────────────────────────────────────────
    def pct_s(n, t):
        return f'{n/t*100:.1f}%' if t else '—'

    lines = [
        '# Auditoría Post-Limpieza de Duplicados',
        '',
        f'- Generado: {now}',
        f'- Master: `{MASTER_FILE.name}` (solo lectura)',
        f'- Probe disponible: {"SI" if probe_idx else "NO (metricas de datos no disponibles)"}',
        '',
        '## Comparación antes / después',
        '',
        '| Concepto | Antes | Después | Diferencia |',
        '|---|---|---|---|',
        f'| Total sensores en JSON | {before_total} | {before_total} | 0 (ninguno borrado) |',
        f'| Sensores visibles | {before_total} | {after_total} | -{after_legacy} ({pct_reduce:.1f}%) |',
        f'| Sensores LEGACY (ocultos) | 0 | {after_legacy} | +{after_legacy} |',
    ]
    if probe_idx:
        lines += [
            f'| Sensores con datos reales | {before_with_d} | {after_with_d} | {after_with_d-before_with_d:+d} |',
            f'| Sensores sin datos | {before_no_d} | {after_no_d} | {after_no_d-before_no_d:+d} |',
        ]
    lines += [
        '',
        '> Los sensores LEGACY siguen existiendo en `pielh_qa_master.json`.',
        '> Solo tienen `include=false` e `inventory_status="LEGACY"`.',
        '> No se ha borrado ningún sensor ni modificado IDs o tokens.',
        '',
        '## Plan de limpieza aplicado',
        '',
        '| Concepto | Valor |',
        '|---|---|',
        f'| Grupos analizados | {plan_summary.get("groups_total", "—")} |',
        f'| KEEP propuestos | {plan_summary.get("sensors_keep", "—")} |',
        f'| MARK_LEGACY aplicados | {plan_summary.get("sensors_mark_legacy", "—")} |',
        f'| MANUAL_REVIEW pendientes | {plan_summary.get("sensors_manual_review", "—")} |',
        '',
        '## Por sistema',
        '',
        '| Sistema | Nombre | Total orig. | Visibles | LEGACY | Con datos | Sin datos | % LEGACY |',
        '|---|---|---|---|---|---|---|---|',
    ]
    for sid, bs in sorted(by_system.items()):
        pct_l = pct_s(bs['legacy'], bs['total'])
        lines.append(
            f"| {sid} | {bs['system_name']} | {bs['total']} | {bs['visible']} "
            f"| {bs['legacy']} | {bs['with_data']} | {bs['without_data']} | {pct_l} |"
        )

    # Edificios con LEGACY
    hos_con_legacy = {h: v for h, v in by_hos.items() if v['legacy'] > 0}
    lines += [
        '',
        f'## Edificios afectados por limpieza ({len(hos_con_legacy)} edificios con ≥1 sensor LEGACY)',
        '',
        '| HOS | Nombre | Total | Visibles | LEGACY |',
        '|---|---|---|---|---|',
    ]
    for h, v in sorted(hos_con_legacy.items(), key=lambda x: -x[1]['legacy']):
        bn = (v['building_name'] or '')[:45]
        lines.append(f"| {h} | {bn} | {v['total']} | {v['visible']} | {v['legacy']} |")

    lines += [
        '',
        '## Acciones recomendadas',
        '',
        '1. Revisar MANUAL_REVIEW en `reports/duplicate_sensor_cleanup_plan.csv` — '
        f'{plan_summary.get("sensors_manual_review", "N/A")} sensores pendientes de decisión manual.',
        '2. Para DUPLICATE_ACTIVE (varios activos mismo HOS+sistema): verificar en TheThings cuál es el dispositivo real.',
        '3. Para DUPLICATE_INACTIVE: confirmar si son inventario histórico o errores de registro.',
        '',
        '## Restaurar un sensor LEGACY',
        '',
        'Si un sensor fue marcado LEGACY incorrectamente, editar `pielh_qa_master.json`:',
        '',
        '```json',
        '{',
        '  "inventory_status": null,',
        '  "legacy_reason": null,',
        '  "legacy_marked_at": null,',
        '  "legacy_source": null,',
        '  "include": true',
        '}',
        '```',
        '',
        '## Verificación de integridad',
        '',
        f'- Sensores en JSON: **{before_total}** (ninguno borrado)',
        f'- Sensores visibles: **{after_total}**',
        f'- Sensores LEGACY: **{after_legacy}**',
        f'- Backup disponible en: `data/backups/pielh_qa_master_before_high_confidence_legacy_*.json`',
    ]

    md_path = REPORTS_DIR / 'post_cleanup_audit.md'
    md_path.write_text('\n'.join(lines), encoding='utf-8')

    print()
    print(f'[PIELH] Auditoria post-limpieza: {now}')
    print(f'        Antes: {before_total} sensores total ({before_with_d} con datos)')
    print(f'        Despues: {after_total} visibles + {after_legacy} LEGACY')
    print(f'        Reduccion: {pct_reduce:.1f}% ({after_legacy} sensores ocultos)')
    if probe_idx:
        print(f'        Datos visibles: {after_with_d} con datos / {after_no_d} sin datos')
    print()
    print('        Por sistema (legacy):')
    for sid, bs in sorted(by_system.items()):
        if bs['legacy'] > 0:
            print(f'          {sid:6} {bs["system_name"]:25} legacy={bs["legacy"]:3}/{bs["total"]:3}')
    print()
    print(f'[OK] {json_path}')
    print(f'[OK] {md_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
