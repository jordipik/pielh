"""
PIELH — Herencia edificio → sensor
Propaga campos administrativos y de localización del edificio padre a sus sensores.
Regla: si el edificio tiene valor útil → copiar al sensor (incluso si ya tiene valor).
       si el edificio no tiene valor útil → no tocar el sensor.
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ADMIN_FIELDS = [
    'district_code',
    'district_name',
    'neighborhood_key',
    'neighborhood',
    'type',
    'zone',
    'street_etra',
    'street_mti',
    'lat',
    'lon',
]

PROTECTED_FIELDS = {
    'id', 'thing_id', 'thing_token', 'system_id', 'system_name',
    'iot_health', 'has_data', 'status', 'raw', 'tags',
    'sensor_order', 'cu_old', 'ref_etra',
}


def _is_useful(value) -> bool:
    """Valor útil: no None, no cadena vacía ni solo espacios."""
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    return True


def _backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime('%Y%m%d_%H%M%S')
    dst = backup_dir / f'pielh_qa_master_before_sensor_building_inheritance_{ts}.json'
    shutil.copy2(master_path, dst)
    # Conservar solo los 20 backups más recientes
    backups = sorted(backup_dir.glob('pielh_qa_master_before_sensor_building_inheritance_*.json'))
    for old in backups[:-20]:
        old.unlink(missing_ok=True)
    return dst


def apply_inheritance(master: dict, dry_run: bool = True) -> dict:
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])

    buildings_by_id = {b['id']: b for b in buildings if b.get('id')}

    stats = {
        'total_sensors':                   len(sensors),
        'sensors_with_hos':                0,
        'sensors_without_hos':             0,
        'sensors_without_matching_building': 0,
        'sensors_checked':                 0,
        'sensors_modified':                0,
        'total_fields_modified':           0,
        'fields_modified_count':           Counter(),
    }
    examples = []

    for sensor in sensors:
        hos = sensor.get('hos')

        if not hos:
            stats['sensors_without_hos'] += 1
            continue

        stats['sensors_with_hos'] += 1
        building = buildings_by_id.get(hos)

        if building is None:
            stats['sensors_without_matching_building'] += 1
            continue

        stats['sensors_checked'] += 1
        changes = {}

        for field in ADMIN_FIELDS:
            b_val = building.get(field)
            if not _is_useful(b_val):
                continue  # edificio sin valor útil → no tocar sensor
            s_val = sensor.get(field)
            if s_val == b_val:
                continue  # ya coinciden
            if not dry_run:
                sensor[field] = b_val
            changes[field] = {'old': s_val, 'new': b_val}
            stats['fields_modified_count'][field] += 1
            stats['total_fields_modified'] += 1

        if changes:
            stats['sensors_modified'] += 1
            if len(examples) < 30:
                examples.append({
                    'sensor_id': sensor.get('id'),
                    'thing_id':  sensor.get('thing_id'),
                    'hos':       hos,
                    'changes':   changes,
                })

    stats['fields_modified_count'] = dict(stats['fields_modified_count'])
    return {**stats, 'examples': examples}


def fill_building_coords_from_sensors(master: dict, dry_run: bool = True) -> dict:
    """
    Rellena lat/lon del edificio desde sus sensores cuando el edificio no tiene coordenadas.
    No sobrescribe edificios que ya tienen lat/lon válidos.
    """
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])

    # Agrupar sensores con coords válidas por HOS
    sensors_by_hos: dict[str, list] = {}
    for s in sensors:
        hos = s.get('hos')
        if not hos:
            continue
        if _is_useful(s.get('lat')) and _is_useful(s.get('lon')):
            sensors_by_hos.setdefault(hos, []).append(s)

    stats = {
        'total_buildings':                    len(buildings),
        'buildings_without_coordinates':      0,
        'buildings_filled_from_sensors':      0,
        'buildings_with_multiple_sensor_coords': 0,
        'buildings_without_sensor_coords':    0,
    }
    examples = []

    for building in buildings:
        bid = building.get('id')
        if _is_useful(building.get('lat')) and _is_useful(building.get('lon')):
            continue  # ya tiene coords → no tocar

        stats['buildings_without_coordinates'] += 1

        candidates = sensors_by_hos.get(bid, [])
        if not candidates:
            stats['buildings_without_sensor_coords'] += 1
            continue

        if len(candidates) == 1:
            new_lat = candidates[0]['lat']
            new_lon = candidates[0]['lon']
            n_sensors = 1
        else:
            new_lat = sum(float(s['lat']) for s in candidates) / len(candidates)
            new_lon = sum(float(s['lon']) for s in candidates) / len(candidates)
            n_sensors = len(candidates)
            stats['buildings_with_multiple_sensor_coords'] += 1

        if not dry_run:
            building['lat'] = new_lat
            building['lon'] = new_lon

        stats['buildings_filled_from_sensors'] += 1
        if len(examples) < 30:
            examples.append({
                'building_id':  bid,
                'lat':          new_lat,
                'lon':          new_lon,
                'from_sensors': n_sensors,
            })

    return {**stats, 'examples_buildings_filled': examples}


# Esquina SE fuera de L'Hospitalet — zona claramente fuera del mapa real
_PLACEHOLDER_BASE_LAT = 41.322
_PLACEHOLDER_BASE_LON = 2.175
_PLACEHOLDER_LON_STEP = 0.004   # ~350m entre placeholders


def fill_building_placeholder_coords(master: dict, dry_run: bool = True) -> dict:
    """
    Asigna coordenadas placeholder a edificios que siguen sin lat/lon.
    Posición: esquina SE fuera de los límites de L'Hospitalet.
    Marca los edificios modificados con coords_source='placeholder'.
    No toca edificios que ya tienen lat/lon válidos.
    """
    buildings = master.get('buildings', [])

    missing = [b for b in buildings if not _is_useful(b.get('lat')) or not _is_useful(b.get('lon'))]
    assigned = []

    for i, building in enumerate(missing):
        bid     = building.get('id', f'idx_{i}')
        new_lat = _PLACEHOLDER_BASE_LAT
        new_lon = round(_PLACEHOLDER_BASE_LON + i * _PLACEHOLDER_LON_STEP, 7)

        if not dry_run:
            building['lat']          = new_lat
            building['lon']          = new_lon
            building['coords_source'] = 'placeholder'

        assigned.append({
            'building_id': bid,
            'lat':         new_lat,
            'lon':         new_lon,
        })

    return {
        'buildings_assigned_placeholder': len(assigned),
        'examples_placeholder':           assigned,
    }


def validate_result(master_orig: dict, master_mod: dict, dry_run: bool) -> dict:
    """Validación post-apply: comprueba integridad básica."""
    sensors_orig   = master_orig.get('sensors', [])
    buildings_orig = master_orig.get('buildings', [])
    sensors_mod    = master_mod.get('sensors', [])
    buildings_mod  = master_mod.get('buildings', [])

    issues = []

    # Conteos
    if len(sensors_mod) != len(sensors_orig):
        issues.append(f'SENSORES: {len(sensors_orig)} → {len(sensors_mod)} (CAMBIO NO ESPERADO)')
    if len(buildings_mod) != len(buildings_orig):
        issues.append(f'EDIFICIOS: {len(buildings_orig)} → {len(buildings_mod)} (CAMBIO NO ESPERADO)')

    if not dry_run:
        # Sensores: verificar campos protegidos por índice (IDs no son únicos)
        for i, (orig, mod) in enumerate(zip(sensors_orig, sensors_mod)):
            sid = orig.get('id', f'idx_{i}')
            for pf in ('id', 'thing_id', 'thing_token', 'system_id', 'system_name', 'iot_health'):
                if mod.get(pf) != orig.get(pf):
                    issues.append(f'PROTEGIDO MODIFICADO: sensor {sid} (idx {i}) campo {pf}')

        # Edificios: los que tenían lat/lon no deben haber cambiado
        for i, (orig, mod) in enumerate(zip(buildings_orig, buildings_mod)):
            bid = orig.get('id', f'idx_{i}')
            had_coords = _is_useful(orig.get('lat')) and _is_useful(orig.get('lon'))
            if had_coords:
                if mod.get('lat') != orig.get('lat') or mod.get('lon') != orig.get('lon'):
                    issues.append(f'COORDS SOBREESCRITAS: edificio {bid} (idx {i}) tenía lat/lon previas')
            # Solo lat/lon pueden cambiar en edificios — nada más
            for pf in ('id', 'name', 'short_name', 'district_code', 'district_name',
                       'neighborhood_key', 'neighborhood', 'type', 'zone',
                       'street_etra', 'street_mti'):
                if mod.get(pf) != orig.get(pf):
                    issues.append(f'CAMPO NO ESPERADO MODIFICADO: edificio {bid} campo {pf}')

    return {
        'total_sensors_orig':   len(sensors_orig),
        'total_sensors_mod':    len(sensors_mod),
        'total_buildings_orig': len(buildings_orig),
        'total_buildings_mod':  len(buildings_mod),
        'issues':               issues,
        'passed':               len(issues) == 0,
    }


def build_report(result: dict, bld_result: dict, ph_result: dict,
                 backup_path: Path, val: dict, dry_run: bool) -> dict:
    return {
        'generated_at':                   datetime.now(timezone.utc).isoformat(),
        'mode':                           'dry-run' if dry_run else 'apply',
        'backup':                         str(backup_path),
        # sensor inheritance
        'total_sensors':                  result['total_sensors'],
        'sensors_with_hos':               result['sensors_with_hos'],
        'sensors_without_hos':            result['sensors_without_hos'],
        'sensors_without_matching_building': result['sensors_without_matching_building'],
        'sensors_checked':                result['sensors_checked'],
        'sensors_modified':               result['sensors_modified'],
        'total_fields_modified':          result['total_fields_modified'],
        'fields_modified_count':          result['fields_modified_count'],
        'examples':                       result['examples'],
        # building coord fill from sensors
        'total_buildings':                bld_result['total_buildings'],
        'buildings_without_coordinates':  bld_result['buildings_without_coordinates'],
        'buildings_filled_from_sensors':  bld_result['buildings_filled_from_sensors'],
        'buildings_with_multiple_sensor_coords': bld_result['buildings_with_multiple_sensor_coords'],
        'buildings_without_sensor_coords': bld_result['buildings_without_sensor_coords'],
        'examples_buildings_filled':      bld_result['examples_buildings_filled'],
        # placeholder coords
        'buildings_assigned_placeholder': ph_result['buildings_assigned_placeholder'],
        'examples_placeholder':           ph_result['examples_placeholder'],
        # validation
        'validation':                     val,
    }


def build_markdown(report: dict) -> str:
    r   = report
    val = r['validation']
    fmc = r['fields_modified_count']

    lines = []
    lines.append('# PIELH — Herencia Edificio → Sensor')
    lines.append(f'\n_Generado: {r["generated_at"]}_')
    lines.append(f'_Modo: `{r["mode"]}`_')
    lines.append(f'_Backup: `{Path(r["backup"]).name}`_\n')

    lines.append('---\n## Resumen\n')
    lines.append('| Métrica | Valor |')
    lines.append('|---|---|')
    lines.append(f'| Total sensores | {r["total_sensors"]} |')
    lines.append(f'| Sensores con HOS | {r["sensors_with_hos"]} |')
    lines.append(f'| Sensores sin HOS (excluidos) | {r["sensors_without_hos"]} |')
    lines.append(f'| Sensores con HOS inválido | {r["sensors_without_matching_building"]} |')
    lines.append(f'| Sensores revisados | {r["sensors_checked"]} |')
    lines.append(f'| **Sensores modificados** | **{r["sensors_modified"]}** |')
    lines.append(f'| **Total campos modificados** | **{r["total_fields_modified"]}** |')
    lines.append('')

    if fmc:
        lines.append('---\n## Campos modificados\n')
        lines.append('| Campo | Sensores afectados |')
        lines.append('|---|---|')
        for f, cnt in sorted(fmc.items(), key=lambda x: -x[1]):
            lines.append(f'| {f} | {cnt} |')
        lines.append('')

    lines.append('---\n## Validación\n')
    status = 'PASADA' if val['passed'] else 'FALLIDA'
    lines.append(f'**Estado: {status}**\n')
    lines.append(f'- Sensores antes/después: {val["total_sensors_orig"]} / {val["total_sensors_mod"]}')
    lines.append(f'- Edificios antes/después: {val["total_buildings_orig"]} / {val["total_buildings_mod"]}')
    if val['issues']:
        lines.append('\n**Problemas detectados:**')
        for issue in val['issues']:
            lines.append(f'- {issue}')
    lines.append('')

    if r['examples']:
        lines.append(f'---\n## Muestra de cambios (máx. 30)\n')
        lines.append('| Sensor ID | HOS | Campos |')
        lines.append('|---|---|---|')
        for ex in r['examples']:
            fields = ', '.join(ex['changes'].keys())
            lines.append(f'| {ex["sensor_id"]} | {ex["hos"]} | {fields} |')
        lines.append('')

    lines.append('---\n## Coordenadas edificios desde sensores\n')
    lines.append('| Métrica | Valor |')
    lines.append('|---|---|')
    lines.append(f'| Total edificios | {r["total_buildings"]} |')
    lines.append(f'| Sin coordenadas propias | {r["buildings_without_coordinates"]} |')
    lines.append(f'| **Rellenados desde sensores** | **{r["buildings_filled_from_sensors"]}** |')
    lines.append(f'| &nbsp;&nbsp;→ Con múltiples sensores (media) | {r["buildings_with_multiple_sensor_coords"]} |')
    lines.append(f'| Sin sensores con coords (no rellenados) | {r["buildings_without_sensor_coords"]} |')
    lines.append('')

    if r['examples_buildings_filled']:
        lines.append('---\n## Muestra edificios rellenados desde sensores (máx. 30)\n')
        lines.append('| Edificio ID | lat | lon | Sensores usados |')
        lines.append('|---|---|---|---|')
        for ex in r['examples_buildings_filled']:
            lines.append(f'| {ex["building_id"]} | {ex["lat"]:.6f} | {ex["lon"]:.6f} | {ex["from_sensors"]} |')
        lines.append('')

    lines.append('---\n## Coordenadas placeholder\n')
    lines.append(f'| Edificios con placeholder | {r["buildings_assigned_placeholder"]} |')
    lines.append(f'| Base: lat={_PLACEHOLDER_BASE_LAT}, lon={_PLACEHOLDER_BASE_LON} (SE fuera de L\'Hospitalet) |  |')
    if r['examples_placeholder']:
        lines.append('\n| Edificio ID | lat | lon |')
        lines.append('|---|---|---|')
        for ex in r['examples_placeholder']:
            lines.append(f'| {ex["building_id"]} | {ex["lat"]} | {ex["lon"]} |')
    lines.append('')

    lines.append('---')
    lines.append(f'_PIELH Smart City — Herencia edificio→sensor — {r["mode"]}._')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='PIELH — Herencia edificio→sensor')
    parser.add_argument('--master',    default=None)
    parser.add_argument('--dry-run',   action='store_true', help='Simular sin guardar (por defecto)')
    parser.add_argument('--apply',     action='store_true', help='Aplicar y guardar cambios')
    args = parser.parse_args()

    dry_run = not args.apply  # sin --apply siempre es dry-run

    base_dir    = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    backup_dir  = base_dir / 'data' / 'backups'
    reports_dir = base_dir / 'reports'

    print(f'[PIELH] Master: {master_path.name}')
    if dry_run:
        print('[PIELH] Modo: DRY-RUN — no se guardarán cambios')
    else:
        print('[PIELH] Modo: APPLY — se escribirán cambios')

    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)

    # Snapshot original para validación
    import copy
    master_orig = copy.deepcopy(master)

    backup_path = _backup(master_path, backup_dir)
    print(f'[PIELH] Backup: {backup_path.name}')

    result     = apply_inheritance(master, dry_run=dry_run)
    bld_result = fill_building_coords_from_sensors(master, dry_run=dry_run)
    ph_result  = fill_building_placeholder_coords(master, dry_run=dry_run)

    if not dry_run:
        with open(master_path, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        print('[PIELH] Master guardado.')

    val = validate_result(master_orig, master, dry_run=dry_run)

    report = build_report(result, bld_result, ph_result, backup_path, val, dry_run=dry_run)
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_out = reports_dir / 'sensor_building_inheritance_report.json'
    md_out   = reports_dir / 'sensor_building_inheritance_report.md'
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(build_markdown(report))

    sep = '-' * 52
    mode = 'DRY-RUN' if dry_run else 'APPLY'
    print(f'\n[PIELH] RESULTADO [{mode}] {sep}')
    print(f'  Total sensores:            {report["total_sensors"]}')
    print(f'  Con HOS:                   {report["sensors_with_hos"]}')
    print(f'  Sin HOS:                   {report["sensors_without_hos"]}')
    print(f'  HOS inválido:              {report["sensors_without_matching_building"]}')
    print(f'  Revisados:                 {report["sensors_checked"]}')
    print(f'  Modificados:               {report["sensors_modified"]}')
    print(f'  Total campos modificados:  {report["total_fields_modified"]}')
    if report['fields_modified_count']:
        print('  Campos más modificados:')
        for f, cnt in sorted(report['fields_modified_count'].items(), key=lambda x: -x[1])[:5]:
            print(f'    {f}: {cnt}')
    print(f'\n  --- Coordenadas edificios desde sensores ---')
    print(f'  Sin coords:                {report["buildings_without_coordinates"]}')
    print(f'  Rellenados:                {report["buildings_filled_from_sensors"]}')
    print(f'  Sin sensores con coords:   {report["buildings_without_sensor_coords"]}')
    print(f'  Placeholder asignados:     {report["buildings_assigned_placeholder"]}')
    if report['examples_placeholder']:
        for ex in report['examples_placeholder']:
            print(f'    {ex["building_id"]}: {ex["lat"]}, {ex["lon"]}')
    val_status = 'PASADA' if val['passed'] else 'FALLIDA'
    print(f'\n  Validación:                {val_status}')
    if val['issues']:
        for issue in val['issues']:
            print(f'    AVISO: {issue}')
    print(sep)
    print(f'  JSON: {json_out}')
    print(f'  MD:   {md_out}')


if __name__ == '__main__':
    main()
