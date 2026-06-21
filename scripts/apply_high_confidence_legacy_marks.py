#!/usr/bin/env python3
"""
apply_high_confidence_legacy_marks.py
Aplica marcas LEGACY a sensores con decision=MARK_LEGACY + confidence=HIGH
del plan de limpieza de duplicados.

SOLO LECTURA hasta que se use --apply.

Uso:
    python scripts/apply_high_confidence_legacy_marks.py --dry-run
    python scripts/apply_high_confidence_legacy_marks.py --apply
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT        = Path(__file__).parent.parent
PLAN_FILE   = ROOT / 'reports' / 'duplicate_sensor_cleanup_plan.json'
MASTER_FILE = ROOT / 'pielh_qa_master.json'
BACKUP_DIR  = ROOT / 'data' / 'backups'
REPORTS_DIR = ROOT / 'reports'

KNOWN_SHA256 = '9E4BD2EA87F76541C45F42C71C3D69DBB10747544B871C49A527339AC0E031E6'
LEGACY_SOURCE = 'duplicate_sensor_cleanup_plan'

# Campos que nunca deben modificarse
PROTECTED_FIELDS = {'id', 'thing_id', 'thing_token', 'hos', 'system_id', 'raw'}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Cargar plan: solo HIGH confidence + MARK_LEGACY
# ---------------------------------------------------------------------------

def load_targets(plan_path: Path):
    """
    Devuelve lista de {thing_id, id, hos, system_id, reason, group_id}
    para sensores con decision=MARK_LEGACY y confidence=HIGH.
    Aborta si hay thing_id vacíos.
    """
    data = json.loads(plan_path.read_text(encoding='utf-8'))
    targets = []
    no_thing_id = []

    for g in data.get('groups', []):
        if g.get('confidence') != 'HIGH':
            continue
        for item in g.get('items', []):
            if item.get('decision') != 'MARK_LEGACY':
                continue
            tid = item.get('thing_id', '').strip()
            if not tid:
                no_thing_id.append({
                    'group_id': g['group_id'],
                    'id': item.get('id', ''),
                    'reason': item.get('reason', ''),
                })
                continue
            targets.append({
                'thing_id':  tid,
                'id':        item.get('id', ''),
                'hos':       item.get('hos', ''),
                'system_id': item.get('system_id', ''),
                'reason':    item.get('reason', ''),
                'group_id':  g['group_id'],
                'classification': g.get('classification', ''),
            })

    return targets, no_thing_id


# ---------------------------------------------------------------------------
# Construir indice master: thing_id -> posicion en lista sensors
# ---------------------------------------------------------------------------

def build_master_index(sensors: list) -> dict:
    idx = {}
    for i, s in enumerate(sensors):
        tid = (s.get('thing_id') or '').strip()
        if tid:
            if tid in idx:
                print(f"[WARN] thing_id duplicado en master: {tid} (posicion {idx[tid]} y {i})")
            idx[tid] = i
    return idx


# ---------------------------------------------------------------------------
# Validar que un sensor no tiene ya campos legacy
# ---------------------------------------------------------------------------

def already_legacy(sensor: dict) -> bool:
    return sensor.get('inventory_status') == 'LEGACY'


# ---------------------------------------------------------------------------
# Preview / result report
# ---------------------------------------------------------------------------

def write_preview(path: Path, targets, master_idx, sensors, sha_before,
                  no_thing_id, timestamp_str, dry_run: bool):
    found   = [t for t in targets if t['thing_id'] in master_idx]
    missing = [t for t in targets if t['thing_id'] not in master_idx]
    skip_already = [t for t in found if already_legacy(sensors[master_idx[t['thing_id']]])]
    to_apply = [t for t in found if not already_legacy(sensors[master_idx[t['thing_id']]])]

    mode_label = 'DRY-RUN (sin cambios)' if dry_run else 'APLICADO'

    lines = [
        f'# Alta Confianza — Marcas LEGACY {mode_label}',
        '',
        f'- Modo: **{mode_label}**',
        f'- Timestamp: {timestamp_str}',
        f'- SHA256 master (antes): `{sha_before}`',
    ]
    if not dry_run:
        sha_after = sha256_of(MASTER_FILE)
        lines += [
            f'- SHA256 master (despues): `{sha_after}`',
            f'- SHA256 modificado: {"SI" if sha_before != sha_after else "NO — sin cambios"}',
        ]
    lines += [
        '',
        '## Resumen',
        '',
        '| Concepto | Valor |',
        '|---|---|',
        f'| Targets HIGH + MARK_LEGACY en plan | {len(targets)} |',
        f'| Encontrados en master (por thing_id) | {len(found)} |',
        f'| Ya marcados LEGACY (omitidos) | {len(skip_already)} |',
        f'| Sin thing_id en plan (omitidos) | {len(no_thing_id)} |',
        f'| No encontrados en master | {len(missing)} |',
        f'| **A aplicar / aplicados** | **{len(to_apply)}** |',
        '',
        '## Sensores a marcar LEGACY',
        '',
        '| thing_id (primeros 32) | id | hos | sistema | clasificacion | razon |',
        '|---|---|---|---|---|---|',
    ]
    for t in to_apply:
        tid_s = t['thing_id'][:32]
        lines.append(
            f"| `{tid_s}` | {t['id']} | {t['hos']} | "
            f"{t['system_id']} | {t['classification']} | {t['reason']} |"
        )

    if missing:
        lines += [
            '',
            f'## Targets no encontrados en master ({len(missing)})',
            '',
            '| thing_id | id | hos |',
            '|---|---|---|',
        ]
        for t in missing:
            lines.append(f"| `{t['thing_id'][:40]}` | {t['id']} | {t['hos']} |")

    if skip_already:
        lines += [
            '',
            f'## Ya marcados LEGACY previamente ({len(skip_already)})',
            '',
        ]
        for t in skip_already:
            lines.append(f"- `{t['thing_id'][:40]}` ({t['id']})")

    if no_thing_id:
        lines += [
            '',
            f'## Sin thing_id en plan ({len(no_thing_id)}) — omitidos',
            '',
        ]
        for t in no_thing_id:
            lines.append(f"- grupo `{t['group_id']}` id=`{t['id']}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines), encoding='utf-8')
    return to_apply, found, missing, skip_already


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true',
                       help='Solo mostrar que se haria, sin modificar nada')
    group.add_argument('--apply',   action='store_true',
                       help='Aplicar cambios reales al master')
    args = parser.parse_args()

    dry_run = args.dry_run

    # ── Verificar archivos ─────────────────────────────────────────────────
    for p in [PLAN_FILE, MASTER_FILE]:
        if not p.exists():
            print(f'[ERROR] No encontrado: {p}')
            return 1

    # ── SHA256 antes ───────────────────────────────────────────────────────
    sha_before = sha256_of(MASTER_FILE)
    print(f'[PIELH] SHA256 master (antes): {sha_before}')
    if sha_before.upper() != KNOWN_SHA256.upper():
        print('[WARN]  El SHA256 no coincide con el valor de referencia.')
        print(f'        Esperado:  {KNOWN_SHA256}')
        print(f'        Actual:    {sha_before}')
        if not dry_run:
            print('[ABORT] No se aplicaran cambios sobre un master no verificado.')
            print('        Usa --dry-run para inspeccionar de todas formas.')
            return 2

    # ── Cargar plan ────────────────────────────────────────────────────────
    print(f'[PIELH] Cargando plan: {PLAN_FILE.name}')
    targets, no_thing_id = load_targets(PLAN_FILE)
    print(f'        Targets HIGH + MARK_LEGACY: {len(targets)}')
    if no_thing_id:
        print(f'        Sin thing_id (omitidos):   {len(no_thing_id)}')

    # ── Cargar master ──────────────────────────────────────────────────────
    print(f'[PIELH] Cargando master...')
    master = json.loads(MASTER_FILE.read_text(encoding='utf-8'))
    sensors = master.get('sensors', [])
    print(f'        Sensores en master: {len(sensors)}')

    # ── Indice master ──────────────────────────────────────────────────────
    master_idx = build_master_index(sensors)

    timestamp_str = now_iso()

    # ── DRY-RUN ────────────────────────────────────────────────────────────
    if dry_run:
        preview_path = REPORTS_DIR / 'high_confidence_legacy_apply_preview.md'
        to_apply, found, missing, skip_already = write_preview(
            preview_path, targets, master_idx, sensors,
            sha_before, no_thing_id, timestamp_str, dry_run=True
        )
        print()
        print(f'[PIELH] DRY-RUN completado: {timestamp_str}')
        print(f'        Encontrados en master   : {len(found)}')
        print(f'        A marcar LEGACY         : {len(to_apply)}')
        print(f'        Ya LEGACY (omitidos)    : {len(skip_already)}')
        print(f'        No encontrados          : {len(missing)}')
        print(f'        Sin thing_id (omitidos) : {len(no_thing_id)}')
        print()
        print(f'[OK] Preview: {preview_path}')
        print()
        if to_apply:
            print('Para aplicar cambios:')
            print('    python scripts/apply_high_confidence_legacy_marks.py --apply')
        return 0

    # ── APPLY ──────────────────────────────────────────────────────────────
    # 1. Backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts_file = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f'pielh_qa_master_before_high_confidence_legacy_{ts_file}.json'
    shutil.copy2(MASTER_FILE, backup_path)
    sha_backup = sha256_of(backup_path)
    print(f'[PIELH] Backup creado: {backup_path.name}')
    print(f'        SHA256 backup: {sha_backup}')

    # 2. Aplicar cambios
    applied  = []
    skipped  = []
    missing_list = []

    for t in targets:
        tid = t['thing_id']
        if tid not in master_idx:
            missing_list.append(t)
            continue

        idx_s = master_idx[tid]
        sensor = sensors[idx_s]

        if already_legacy(sensor):
            skipped.append(t)
            continue

        # Verificar que los campos protegidos no cambian (doble seguro)
        for field in PROTECTED_FIELDS:
            if field in sensor and sensor[field] != t.get(field, sensor[field]):
                # Solo advertir si el campo es id/thing_id/thing_token
                if field in {'id', 'thing_id', 'thing_token'}:
                    print(f'[WARN] Campo {field} discrepante para {tid}: '
                          f'master={sensor[field]!r} vs plan={t.get(field)!r}')

        # Aplicar marcas
        sensor['inventory_status'] = 'LEGACY'
        sensor['legacy_reason']    = t['reason']
        sensor['legacy_marked_at'] = timestamp_str
        sensor['legacy_source']    = LEGACY_SOURCE
        sensor['include']          = False

        applied.append({
            'thing_id':       tid,
            'id':             sensor.get('id', ''),
            'hos':            sensor.get('hos', ''),
            'system_id':      sensor.get('system_id', ''),
            'classification': t['classification'],
            'reason':         t['reason'],
        })

    if not applied:
        print('[WARN] No hay cambios que aplicar. Master no modificado.')
        # Eliminar backup vacío
        backup_path.unlink(missing_ok=True)
        return 0

    # 3. Escribir master
    master_text = json.dumps(master, ensure_ascii=False, indent=2)
    MASTER_FILE.write_text(master_text, encoding='utf-8')

    sha_after = sha256_of(MASTER_FILE)
    print(f'[PIELH] SHA256 master (despues): {sha_after}')
    print(f'        SHA256 modificado: {"SI" if sha_before != sha_after else "NO — algo fue mal"}')

    # 4. Verificar integridad: contar sensores
    master_verify = json.loads(MASTER_FILE.read_text(encoding='utf-8'))
    n_sensors_after = len(master_verify.get('sensors', []))
    n_buildings_after = len(master_verify.get('buildings', []))

    if n_sensors_after != len(sensors):
        print(f'[ABORT-CHECK] Numero de sensores cambio: {len(sensors)} -> {n_sensors_after}')
        print('              Restaurando desde backup...')
        shutil.copy2(backup_path, MASTER_FILE)
        return 3

    # 5. Verificar que IDs/thing_id/thing_token no se tocaron
    original = json.loads(backup_path.read_text(encoding='utf-8'))
    orig_sensors = {s['thing_id']: s for s in original['sensors'] if s.get('thing_id')}
    for s in master_verify['sensors']:
        tid = s.get('thing_id', '')
        if not tid or tid not in orig_sensors:
            continue
        orig = orig_sensors[tid]
        for pf in ('id', 'thing_id', 'thing_token', 'hos', 'system_id'):
            if s.get(pf) != orig.get(pf):
                print(f'[ABORT-CHECK] Campo protegido cambiado: {pf} en {tid}')
                print('              Restaurando desde backup...')
                shutil.copy2(backup_path, MASTER_FILE)
                return 4

    # 6. Informe de resultado
    result_path = REPORTS_DIR / 'high_confidence_legacy_apply_result.md'
    write_preview(
        result_path, targets, master_idx,
        # Usamos los sensores modificados (en memoria) para el reporte
        master_verify['sensors'], sha_before,
        no_thing_id, timestamp_str, dry_run=False
    )

    # Sobreescribir con datos reales post-apply
    lines_extra = [
        '',
        f'## Verificacion post-apply',
        '',
        f'| Campo | Valor |',
        f'|---|---|',
        f'| SHA256 antes | `{sha_before}` |',
        f'| SHA256 despues | `{sha_after}` |',
        f'| Backup | `{backup_path.name}` |',
        f'| Sensores antes | {len(sensors)} |',
        f'| Sensores despues | {n_sensors_after} |',
        f'| Sensores marcados LEGACY | {len(applied)} |',
        f'| Sensores omitidos (ya LEGACY) | {len(skipped)} |',
        f'| Targets no encontrados | {len(missing_list)} |',
        f'| IDs modificados | NO |',
        f'| thing_id modificados | NO |',
        f'| thing_token modificados | NO |',
        f'| Sensores borrados | NO |',
    ]
    existing = result_path.read_text(encoding='utf-8')
    result_path.write_text(existing + '\n' + '\n'.join(lines_extra), encoding='utf-8')

    # 7. Consola
    print()
    print(f'[PIELH] APPLY completado: {timestamp_str}')
    print(f'        Sensores marcados LEGACY : {len(applied)}')
    print(f'        Omitidos (ya LEGACY)     : {len(skipped)}')
    print(f'        No encontrados           : {len(missing_list)}')
    print(f'        Sensores en master antes : {len(sensors)}')
    print(f'        Sensores en master despues: {n_sensors_after}')
    print(f'        Sensores borrados        : 0')
    print()
    print(f'[OK] Backup:   {backup_path}')
    print(f'[OK] Resultado: {result_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
