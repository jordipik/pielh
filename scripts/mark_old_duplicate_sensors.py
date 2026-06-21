#!/usr/bin/env python3
"""
mark_old_duplicate_sensors.py
Marca como OLD los sensores hermanos inactivos detectados como CRITICAL en la auditoría.
Identificación por thing_id (clave única). No modifica thing_id ni thing_token.
"""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).parent.parent
MASTER_FILE = ROOT / 'pielh_qa_master.json'
AUDIT_CSV   = ROOT / 'reports' / 'duplicate_sensors_audit.csv'
BACKUP_DIR  = ROOT / 'data' / 'backups'
REPORTS_DIR = ROOT / 'reports'

PROTECTED_FIELDS = {
    'thing_id', 'thing_token', 'raw', 'iot_health',
    'lat', 'lon', 'hos', 'system_id', 'building_name',
}


def load_old_candidates():
    """Lee el CSV de auditoría y devuelve los thing_id de sensores OLD (CRITICAL inactivos)."""
    candidates = []
    with open(AUDIT_CSV, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('possible_old') == 'True' and row.get('risk') == 'CRITICAL':
                candidates.append({
                    'thing_id':    row['thing_id'],
                    'thing_token': row['thing_token'],
                    'id_csv':      row['id'],
                })
    return candidates


def is_active(sensor):
    ih = sensor.get('iot_health') or {}
    return (
        ih.get('has_real_data') is True
        or ih.get('demo_ready') is True
        or sensor.get('has_data') == 'OK'
    )


def run():
    if not AUDIT_CSV.exists():
        print(f"ERROR: no se encuentra {AUDIT_CSV}")
        print("Ejecuta primero: python scripts/audit_duplicate_sensors.py")
        return

    candidates = load_old_candidates()
    if not candidates:
        print("No se encontraron candidatos OLD (CRITICAL) en el CSV de auditoría.")
        return

    print(f"Candidatos OLD encontrados en auditoría: {len(candidates)}")
    for c in candidates:
        print(f"  thing_id={c['thing_id'][:40]}  id_csv='{c['id_csv']}'")

    with open(MASTER_FILE, encoding='utf-8') as f:
        master = json.load(f)

    sensors_before = len(master.get('sensors', []))
    buildings_before = len(master.get('buildings', []))

    # Indexar por thing_id para lookup O(1)
    candidate_tids = {c['thing_id'] for c in candidates}

    # Capturar estado antes para validación
    snapshots_before = {}
    for s in master.get('sensors', []):
        tid = s.get('thing_id', '')
        if tid in candidate_tids:
            snapshots_before[tid] = {
                'thing_id':    s.get('thing_id'),
                'thing_token': s.get('thing_token'),
                'id':          s.get('id'),
            }

    # ── Backup ────────────────────────────────────────────────────────
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts          = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"pielh_qa_master_before_mark_old_{ts}.json"
    shutil.copy2(MASTER_FILE, backup_path)
    print(f"\nBackup: {backup_path}")

    # ── Aplicar marcas ────────────────────────────────────────────────
    marked   = []
    skipped  = []
    errors   = []
    now_iso  = datetime.now().isoformat()

    for s in master.get('sensors', []):
        tid = s.get('thing_id', '')
        if tid not in candidate_tids:
            continue

        # Doble verificación: no marcar si resulta activo en el JSON actual
        if is_active(s):
            skipped.append({'thing_id': tid, 'id': s.get('id'), 'reason': 'activo en JSON actual'})
            continue

        try:
            old_id = s.get('id', '')

            # id_old: solo si no existe
            if 'id_old' not in s or s.get('id_old') is None:
                s['id_old'] = old_id

            # Renombrar id si no empieza por Old-
            if not str(old_id).startswith('Old-'):
                s['id'] = f"Old-{old_id}"

            # Excluir de sincronización
            s['include']  = False
            s['status']   = 'OLD'
            s['qa_notes'] = 'Sensor hermano inactivo detectado por auditoria CRITICAL'

            # Marca de auditoría
            s['old_sensor'] = True
            s['old_reason'] = 'CRITICAL_DUPLICATE_INACTIVE'
            s['old_marked_at'] = now_iso

            marked.append({
                'thing_id':    tid,
                'thing_token': s.get('thing_token'),
                'id_before':   old_id,
                'id_after':    s['id'],
            })

        except Exception as exc:
            errors.append({'thing_id': tid, 'error': str(exc)})

    if errors:
        print(f"\nERROR: {len(errors)} fallos al marcar. Abortando sin guardar.")
        for e in errors:
            print(f"  {e}")
        return

    # ── Validación ────────────────────────────────────────────────────
    assert len(master.get('sensors', [])) == sensors_before, "ERROR: numero de sensores cambio"
    assert len(master.get('buildings', [])) == buildings_before, "ERROR: numero de edificios cambio"

    for s in master.get('sensors', []):
        tid = s.get('thing_id', '')
        if tid in snapshots_before:
            snap = snapshots_before[tid]
            assert s.get('thing_id')    == snap['thing_id'],    f"thing_id modificado: {tid}"
            assert s.get('thing_token') == snap['thing_token'], f"thing_token modificado: {tid}"

    # Verificar que los activos del mismo grupo no fueron tocados
    for s in master.get('sensors', []):
        if s.get('status') == 'OLD' and s.get('thing_id') not in candidate_tids:
            assert False, f"Sensor fuera de scope marcado: {s.get('id')}"

    # ── Guardar ───────────────────────────────────────────────────────
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    # ── Informe ───────────────────────────────────────────────────────
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'old_sensors_marked_report.txt'
    lines = []
    a = lines.append
    a("=" * 60)
    a("PIELH - Sensores OLD Marcados")
    a(f"Fecha  : {now_iso}")
    a(f"Backup : {backup_path}")
    a("=" * 60)
    a(f"\nSensores OLD marcados : {len(marked)}")
    a(f"Omitidos (activos)    : {len(skipped)}")
    a(f"Errores               : {len(errors)}")
    a("\nDetalle:")
    for m_entry in marked:
        a(f"\n  thing_id    : {m_entry['thing_id']}")
        a(f"  thing_token : {m_entry['thing_token']}")
        a(f"  id antes    : '{m_entry['id_before']}'")
        a(f"  id despues  : '{m_entry['id_after']}'")
        a(f"  include     : False")
        a(f"  status      : OLD")
    if skipped:
        a("\nOmitidos (activos en JSON actual):")
        for sk in skipped:
            a(f"  thing_id={sk['thing_id']}  id='{sk['id']}'")
    a("\nValidacion:")
    a(f"  Total sensores intacto     : {sensors_before}")
    a(f"  Total edificios intacto    : {buildings_before}")
    a(f"  thing_id/thing_token       : sin cambios (verificado)")
    a(f"  Sensores activos hermanos  : no modificados")

    txt = '\n'.join(lines)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    print(f"\n{txt}")
    print(f"\nInforme: {report_path}")


# ── Utilidad futura de exclusión de sync ──────────────────────────────
def is_sync_eligible(sensor: dict) -> bool:
    """
    Devuelve False si el sensor debe quedar excluido de sincronizaciones.
    Usar antes de cualquier operacion de push a TheThings.
    """
    if sensor.get('status') == 'OLD':
        return False
    if sensor.get('include') is False:
        return False
    return True


if __name__ == '__main__':
    run()
