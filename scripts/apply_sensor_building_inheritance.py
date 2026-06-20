"""
PIELH FASE 0 — Corrección herencia edificio → sensor
Rellena campos vacíos en sensores desde el edificio padre.
No sobrescribe datos existentes. No toca coordenadas propias del sensor.
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ADMIN_FIELDS = [
    'district_code', 'district_name',
    'neighborhood_key', 'neighborhood',
    'zone', 'type', 'street_etra',
]

PROTECTED_FIELDS = {
    'iot_health', 'thing_id', 'thing_token', 'raw',
    'system_id', 'system_name',
}


def _backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime('%Y%m%d_%H%M%S')
    dst = backup_dir / f'pielh_qa_master_{ts}.json'
    shutil.copy2(master_path, dst)
    backups = sorted(backup_dir.glob('pielh_qa_master_*.json'))
    for old in backups[:-20]:
        old.unlink(missing_ok=True)
    return dst


def apply_inheritance(master: dict, dry_run: bool = False) -> dict:
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])

    buildings_by_id = {b['id']: b for b in buildings if b.get('id')}

    stats = {
        'total_with_hos':             0,
        'skipped_no_hos':             0,
        'skipped_invalid_hos':        0,
        'updated_building_name':      0,
        'updated_coords_from_building': 0,
        'skipped_existing_coords':    0,
        'updated_admin_fields':       0,
        'admin_field_counts':         Counter(),
        'sensors_changed':            0,
    }
    examples = []

    for sensor in sensors:
        hos = sensor.get('hos')

        if not hos:
            stats['skipped_no_hos'] += 1
            continue

        building = buildings_by_id.get(hos)
        if building is None:
            stats['skipped_invalid_hos'] += 1
            continue

        stats['total_with_hos'] += 1
        changes = {}

        # A. building_name
        if not sensor.get('building_name'):
            b_name = building.get('short_name') or building.get('name') or ''
            if b_name:
                if not dry_run:
                    sensor['building_name'] = b_name
                changes['building_name'] = b_name
                stats['updated_building_name'] += 1

        # B. Coordenadas — solo si el sensor NO tiene lat/lon
        s_lat = sensor.get('lat')
        s_lon = sensor.get('lon')
        b_lat = building.get('lat')
        b_lon = building.get('lon')

        if s_lat is not None or s_lon is not None:
            # Sensor ya tiene coordenadas propias: no tocar
            stats['skipped_existing_coords'] += 1
        elif b_lat is not None and b_lon is not None:
            # Sensor sin coords, edificio tiene: copiar
            if not dry_run:
                sensor['lat']          = b_lat
                sensor['lon']          = b_lon
                sensor['coords_source'] = 'building'
            changes['lat']          = b_lat
            changes['lon']          = b_lon
            changes['coords_source'] = 'building'
            stats['updated_coords_from_building'] += 1

        # C. Campos administrativos — solo si vacíos
        admin_updated = False
        for field in ADMIN_FIELDS:
            if not sensor.get(field):
                bv = building.get(field)
                if bv:
                    if not dry_run:
                        sensor[field] = bv
                    changes[field] = bv
                    stats['admin_field_counts'][field] += 1
                    admin_updated = True
        if admin_updated:
            stats['updated_admin_fields'] += 1

        if changes:
            stats['sensors_changed'] += 1
            if len(examples) < 5:
                examples.append({
                    'sensor_id': sensor.get('id'),
                    'thing_id':  sensor.get('thing_id'),
                    'hos':       hos,
                    'changes':   changes,
                })

    return {**stats, 'admin_field_counts': dict(stats['admin_field_counts']), 'examples': examples}


def build_report(result: dict, backup_path: Path) -> dict:
    return {
        'generated_at':                   datetime.now(timezone.utc).isoformat(),
        'backup':                         str(backup_path),
        'total_sensors_with_hos':         result['total_with_hos'],
        'skipped_no_hos':                 result['skipped_no_hos'],
        'skipped_invalid_hos':            result['skipped_invalid_hos'],
        'updated_building_name':          result['updated_building_name'],
        'updated_coordinates_from_building': result['updated_coords_from_building'],
        'skipped_existing_coordinates':   result['skipped_existing_coords'],
        'updated_admin_fields':           result['updated_admin_fields'],
        'admin_field_detail':             result['admin_field_counts'],
        'sensors_changed':                result['sensors_changed'],
        'examples':                       result['examples'],
    }


def build_markdown(report: dict) -> str:
    lines = []
    lines.append('# PIELH — Herencia Edificio → Sensor: Correcciones aplicadas')
    lines.append(f'\n_Generado: {report["generated_at"]}_')
    lines.append(f'\n_Backup: `{Path(report["backup"]).name}`_\n')

    lines.append('---\n## Resumen\n')
    lines.append('| Métrica | Valor |')
    lines.append('|---|---|')
    lines.append(f'| Sensores con HOS revisados | {report["total_sensors_with_hos"]} |')
    lines.append(f'| `building_name` rellenados | {report["updated_building_name"]} |')
    lines.append(f'| `lat/lon` copiados desde edificio | {report["updated_coordinates_from_building"]} |')
    lines.append(f'| Coordenadas propias conservadas (sin tocar) | {report["skipped_existing_coordinates"]} |')
    lines.append(f'| Campos admin rellenados (sensores) | {report["updated_admin_fields"]} |')
    lines.append(f'| Saltados por HOS inválido | {report["skipped_invalid_hos"]} |')
    lines.append(f'| **Total sensores modificados** | **{report["sensors_changed"]}** |')
    lines.append('')

    if report['admin_field_detail']:
        lines.append('---\n## Campos administrativos rellenados\n')
        lines.append('| Campo | Sensores |')
        lines.append('|---|---|')
        for f, cnt in report['admin_field_detail'].items():
            lines.append(f'| {f} | {cnt} |')
        lines.append('')

    if report['examples']:
        lines.append('---\n## Muestra de cambios\n')
        lines.append('| Sensor ID | HOS | Campos modificados |')
        lines.append('|---|---|---|')
        for ex in report['examples']:
            fields = ', '.join(report['examples'][0]['changes'].keys()) if report['examples'] else '-'
            fields = ', '.join(ex['changes'].keys())
            lines.append(f'| {ex["sensor_id"]} | {ex["hos"]} | {fields} |')
        lines.append('')

    lines.append('---')
    lines.append('_PIELH Smart City — Corrección FASE 0 — Solo campos vacíos._')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='PIELH — Aplicar herencia edificio→sensor')
    parser.add_argument('--master',   default=None)
    parser.add_argument('--dry-run',  action='store_true', help='Simular sin guardar')
    args = parser.parse_args()

    base_dir    = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    backup_dir  = base_dir / 'data' / 'backups'
    audit_dir   = base_dir / 'data' / 'audits'

    print(f'[PIELH] Master: {master_path.name}')
    if args.dry_run:
        print('[PIELH] DRY RUN — no se guardarán cambios')

    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)

    backup_path = _backup(master_path, backup_dir)
    print(f'[PIELH] Backup: {backup_path.name}')

    result = apply_inheritance(master, dry_run=args.dry_run)

    if not args.dry_run:
        with open(master_path, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        print('[PIELH] Master guardado.')

    report = build_report(result, backup_path)
    audit_dir.mkdir(parents=True, exist_ok=True)
    json_out = audit_dir / 'sensor_building_inheritance_applied.json'
    md_out   = audit_dir / 'sensor_building_inheritance_applied.md'
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(build_markdown(report))

    sep = '-' * 52
    print(f'\n[PIELH] RESULTADO {sep}')
    print(f'  Sensores con HOS:          {report["total_sensors_with_hos"]}')
    print(f'  building_name rellenados:  {report["updated_building_name"]}')
    print(f'  lat/lon desde edificio:    {report["updated_coordinates_from_building"]}')
    print(f'  coords propias (no toc.):  {report["skipped_existing_coordinates"]}')
    print(f'  admin fields rellenados:   {report["updated_admin_fields"]}')
    print(f'  HOS invalido (saltados):   {report["skipped_invalid_hos"]}')
    print(f'  Sensores modificados:      {report["sensors_changed"]}')
    print(sep)
    print(f'  JSON: {json_out}')
    print(f'  MD:   {md_out}')


if __name__ == '__main__':
    main()
