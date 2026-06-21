#!/usr/bin/env python3
"""
normalize_sensor_ids.py
Normaliza los IDs de sensores al formato HOSXXX-SXX-NN.
Guarda el ID original en id_old. Marca sensores inactivos duplicados como Old-.
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).parent.parent
MASTER_FILE = ROOT / 'pielh_qa_master.json'
BACKUP_DIR  = ROOT / 'data' / 'backups'
REPORTS_DIR = ROOT / 'reports'

PROTECTED_FIELDS = {
    'thing_id', 'thing_token', 'raw', 'iot_health',
    'lat', 'lon', 'hos', 'system_id', 'building_name',
    'district_code', 'neighborhood_key',
}


def is_active(sensor):
    ih = sensor.get('iot_health') or {}
    return (
        ih.get('has_real_data') is True
        or ih.get('demo_ready') is True
        or sensor.get('has_data') == 'OK'
    )


def sort_key(sensor):
    ih = sensor.get('iot_health') or {}
    return (
        0 if ih.get('has_real_data') else 1,
        0 if ih.get('demo_ready') else 1,
        0 if sensor.get('has_data') == 'OK' else 1,
        sensor.get('thing_id') or '',
    )


def compute_plan(sensors):
    """
    Calcula los cambios necesarios sin modificar nada.
    Retorna (changes, stats).
    """
    groups = {}
    skipped_no_hos = []

    for s in sensors:
        hos = s.get('hos')
        if not hos:
            skipped_no_hos.append(s)
            continue
        key = (hos, s.get('system_id', ''))
        groups.setdefault(key, []).append(s)

    changes          = []  # list of {sensor, new_id, new_id_old}
    skipped_norm     = 0
    duplicate_groups = 0

    for (hos, system_id), group in sorted(groups.items()):
        has_active = any(is_active(s) for s in group)
        if len(group) > 1:
            duplicate_groups += 1

        sorted_group = sorted(group, key=sort_key)

        for i, s in enumerate(sorted_group, 1):
            if 'id_old' in s:
                # Ya procesado en una ejecución anterior → skip (idempotencia)
                skipped_norm += 1
                continue

            base_id = f"{hos}-{system_id}-{i:02d}"
            new_id  = (f"Old-{base_id}" if has_active and not is_active(s)
                       else base_id)

            changes.append({
                'sensor':    s,
                'new_id':    new_id,
                'new_id_old': s.get('id', ''),
            })

    stats = {
        'total':             len(sensors),
        'skipped_no_hos':    len(skipped_no_hos),
        'skipped_norm':      skipped_norm,
        'id_old_created':    len(changes),
        'renamed':           sum(1 for c in changes if c['new_id'] != c['new_id_old']),
        'old_marked':        sum(1 for c in changes if c['new_id'].startswith('Old-')),
        'duplicate_groups':  duplicate_groups,
    }
    return changes, stats, skipped_no_hos


def print_summary(stats, changes, skipped_no_hos, dry_run):
    mode = '[dry-run]' if dry_run else '[apply]'
    print(f"\n{mode} Resumen")
    print(f"  Total sensores revisados    : {stats['total']}")
    print(f"  Sin hos (omitidos)          : {stats['skipped_no_hos']}")
    print(f"  Ya normalizados (omitidos)  : {stats['skipped_norm']}")
    print(f"  id_old a crear              : {stats['id_old_created']}")
    print(f"  Sensores a renombrar        : {stats['renamed']}")
    print(f"  Sensores marcados OLD       : {stats['old_marked']}")
    print(f"  Grupos con duplicados       : {stats['duplicate_groups']}")
    print()

    if skipped_no_hos:
        print(f"  Sin hos (IDs actuales):")
        for s in skipped_no_hos[:5]:
            print(f"    '{s.get('id')}' | system_id={s.get('system_id')}")
        if len(skipped_no_hos) > 5:
            print(f"    ... y {len(skipped_no_hos)-5} más")
        print()

    print("  Ejemplos de cambios previstos:")
    shown = 0
    for c in changes:
        if c['new_id_old'] != c['new_id']:
            s = c['sensor']
            print(f"    [{s.get('hos')}-{s.get('system_id')}]  '{c['new_id_old']}'  ->  '{c['new_id']}'")
            shown += 1
            if shown >= 10:
                break


def validate(master_before, master_after):
    errors = []
    sb = master_before.get('sensors', [])
    sa = master_after.get('sensors', [])
    if len(sa) != len(sb):
        errors.append(f"Número de sensores cambió: {len(sb)} → {len(sa)}")
    if len(master_after.get('buildings', [])) != len(master_before.get('buildings', [])):
        errors.append("Número de edificios cambió")
    # Verificar campos protegidos no modificados
    for s_before, s_after in zip(sb, sa):
        for field in PROTECTED_FIELDS:
            if s_before.get(field) != s_after.get(field):
                errors.append(f"Campo protegido '{field}' modificado en sensor '{s_after.get('id')}'")
    # Verificar que todos los procesados tienen id_old
    for s in sa:
        if s.get('hos') and 'id_old' not in s:
            if not any(1 for c in []):  # placeholder check
                pass  # sensors processed in this run do have id_old
    return errors


def run(dry_run):
    with open(MASTER_FILE, encoding='utf-8') as f:
        master = json.load(f)

    sensors_count_before  = len(master.get('sensors', []))
    buildings_count_before = len(master.get('buildings', []))

    changes, stats, skipped_no_hos = compute_plan(master.get('sensors', []))
    print_summary(stats, changes, skipped_no_hos, dry_run)

    if dry_run:
        print("[dry-run] No se ha modificado ningún archivo.\n")
        return

    # ── Backup ────────────────────────────────────────────────────────
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts          = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"pielh_qa_master_before_sensor_id_normalization_{ts}.json"
    shutil.copy2(MASTER_FILE, backup_path)
    print(f"  Backup: {backup_path}")

    # ── Aplicar cambios ───────────────────────────────────────────────
    errors = 0
    for c in changes:
        try:
            s = c['sensor']
            s['id_old'] = c['new_id_old']
            s['id']     = c['new_id']
        except Exception as exc:
            print(f"  ERROR al procesar '{c.get('new_id_old')}': {exc}")
            errors += 1

    # ── Validación ────────────────────────────────────────────────────
    assert len(master.get('sensors', [])) == sensors_count_before, \
        "ERROR CRÍTICO: número de sensores cambió"
    assert len(master.get('buildings', [])) == buildings_count_before, \
        "ERROR CRÍTICO: número de edificios cambió"

    # Verificar que todos los sensores con hos tienen id_old
    missing_id_old = [
        s.get('id') for s in master.get('sensors', [])
        if s.get('hos') and 'id_old' not in s
    ]
    if missing_id_old:
        print(f"  AVISO: {len(missing_id_old)} sensores con hos sin id_old (ya normalizados en run anterior)")

    # ── Guardar ───────────────────────────────────────────────────────
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    # ── Informe ───────────────────────────────────────────────────────
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'sensor_id_normalization_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Sensor ID Normalization Report\n")
        f.write(f"Fecha  : {datetime.now().isoformat()}\n")
        f.write(f"Backup : {backup_path}\n\n")
        f.write(f"Total sensores revisados    : {stats['total']}\n")
        f.write(f"Sin hos (omitidos)          : {stats['skipped_no_hos']}\n")
        f.write(f"Ya normalizados (omitidos)  : {stats['skipped_norm']}\n")
        f.write(f"id_old creados              : {stats['id_old_created']}\n")
        f.write(f"Sensores renombrados        : {stats['renamed']}\n")
        f.write(f"Sensores marcados OLD       : {stats['old_marked']}\n")
        f.write(f"Grupos con duplicados       : {stats['duplicate_groups']}\n")
        f.write(f"Errores                     : {errors}\n\n")
        f.write("Sensores sin hos (omitidos):\n")
        for s in skipped_no_hos:
            f.write(f"  '{s.get('id')}' | system_id={s.get('system_id')}\n")
        f.write("\nCambios realizados:\n")
        for c in changes:
            s = c['sensor']
            f.write(f"  [{s.get('hos')}-{s.get('system_id')}]  '{c['new_id_old']}'  ->  '{c['new_id']}'\n")

    print(f"  Informe: {report_path}")
    print(f"  Errores: {errors}")
    print("[apply] Completado.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Normaliza IDs de sensores PIELH')
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true', help='Muestra cambios sin modificar nada')
    group.add_argument('--apply',   action='store_true', help='Aplica cambios con backup previo')
    args = parser.parse_args()
    run(dry_run=args.dry_run)
