"""
PIELH FASE 0 — Auditoría herencia edificio → sensor
Comprueba que los sensores vinculados a un HOS heredan correctamente
los campos administrativos y geográficos del edificio.
Solo lectura. No modifica pielh_qa_master.json.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict

# Campos administrativos a comparar edificio → sensor
# (campo_edificio, campo_sensor)
ADMIN_FIELD_PAIRS = [
    ('district_code',    'district_code'),
    ('district_name',    'district_name'),
    ('neighborhood_key', 'neighborhood_key'),
    ('neighborhood',     'neighborhood'),
    ('zone',             'zone'),
    ('type',             'type'),
    ('street_etra',      'street_etra'),
]

# Campo de nombre del edificio: se comprueba building.short_name || building.name vs sensor.building_name
COORD_TOLERANCE = 0.000001   # ~0.1m — diferencias por debajo son ruido de redondeo
COORD_REVIEW_THRESHOLD = 0.001  # ~100m — por encima, revisar antes de sobrescribir


# ---------------------------------------------------------------------------
# Comparadores
# ---------------------------------------------------------------------------

def _coord_diff(building: dict, sensor: dict) -> dict:
    """Analiza diferencias de coordenadas. Devuelve dict con flags."""
    bl, bln = building.get('lat'), building.get('lon')
    sl, sln = sensor.get('lat'),   sensor.get('lon')

    b_has = bl is not None and bln is not None
    s_has = sl is not None and sln is not None

    if not b_has and not s_has:
        return {'status': 'both_null'}
    if not b_has:
        return {'status': 'building_null', 'sensor_lat': sl, 'sensor_lon': sln}
    if not s_has:
        return {'status': 'sensor_null', 'building_lat': bl, 'building_lon': bln}

    dlat = abs(float(bl) - float(sl))
    dlon = abs(float(bln) - float(sln))
    max_diff = max(dlat, dlon)

    if max_diff <= COORD_TOLERANCE:
        return {'status': 'ok'}

    return {
        'status':       'mismatch',
        'dlat':         round(dlat, 7),
        'dlon':         round(dlon, 7),
        'max_diff':     round(max_diff, 7),
        'needs_review': max_diff > COORD_REVIEW_THRESHOLD,
        'building_lat': bl,   'building_lon': bln,
        'sensor_lat':   sl,   'sensor_lon':   sln,
    }


def _check_sensor(sensor: dict, building: dict) -> dict:
    """
    Compara un sensor contra su edificio.
    Devuelve:
      category: OK | MISSING_BUILDING | MISSING_FIELDS | MISMATCH_FIELDS | COORDINATE_MISMATCH
      differences: dict con detalles
      recommended_action: str
    """
    differences = {}
    missing_fields  = []
    mismatch_fields = []

    # Nombre del edificio
    b_name = building.get('short_name') or building.get('name') or ''
    s_name = sensor.get('building_name') or ''
    if b_name and not s_name:
        missing_fields.append('building_name')
    elif b_name and s_name and b_name != s_name:
        mismatch_fields.append({
            'field': 'building_name', 'building': b_name, 'sensor': s_name
        })

    # Campos administrativos
    for bf, sf in ADMIN_FIELD_PAIRS:
        bv = building.get(bf) or ''
        sv = sensor.get(sf) or ''
        if bv and not sv:
            missing_fields.append(sf)
        elif bv and sv and bv != sv:
            mismatch_fields.append({'field': sf, 'building': bv, 'sensor': sv})

    # ref_etra legacy: si sensor tiene ref_etra pero no street_etra, anotar
    if sensor.get('ref_etra') and not sensor.get('street_etra') and building.get('street_etra'):
        differences['street_field_model'] = {
            'note': 'sensor usa ref_etra (legacy), edificio usa street_etra',
            'ref_etra': sensor.get('ref_etra'),
            'building_street_etra': building.get('street_etra'),
        }

    # Coordenadas
    coord_result = _coord_diff(building, sensor)

    if missing_fields:
        differences['missing_fields'] = missing_fields
    if mismatch_fields:
        differences['mismatch_fields'] = mismatch_fields
    if coord_result['status'] not in ('ok', 'both_null'):
        differences['coords'] = coord_result

    # Determinar categoría (prioridad)
    if mismatch_fields:
        category = 'MISMATCH_FIELDS'
        action   = 'revision_manual — conflicto de datos entre sensor y edificio'
    elif coord_result['status'] == 'mismatch' and coord_result.get('needs_review'):
        category = 'COORDINATE_MISMATCH'
        action   = 'revision_manual — sensor a >100m del edificio (posicion fisica propia?)'
    elif coord_result['status'] == 'mismatch' and not coord_result.get('needs_review'):
        category = 'COORDINATE_MISMATCH'
        action   = 'auto_corregible — diferencia de redondeo (<100m)'
    elif missing_fields or coord_result['status'] in ('sensor_null',):
        category = 'MISSING_FIELDS'
        action   = 'auto_rellenable — campos vacios que el edificio tiene'
    elif not differences:
        category = 'OK'
        action   = 'ninguna'
    else:
        category = 'OK'
        action   = 'ninguna'

    return {
        'category':            category,
        'differences':         differences,
        'recommended_action':  action,
    }


# ---------------------------------------------------------------------------
# Build audit
# ---------------------------------------------------------------------------

def build_audit(master: dict) -> dict:
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])
    catalogs  = master.get('catalogs', {})
    systems_cat = {s['id']: s.get('name', s['id']) for s in catalogs.get('systems', []) if 'id' in s}

    buildings_by_id  = {b['id']: b for b in buildings if b.get('id')}
    sensors_with_hos = [s for s in sensors if s.get('hos')]
    sensors_no_hos   = [s for s in sensors if not s.get('hos')]

    rows = []
    for s in sensors_with_hos:
        hos = s['hos']
        building = buildings_by_id.get(hos)

        if building is None:
            rows.append({
                'sensor_id':          s.get('id'),
                'thing_id':           s.get('thing_id'),
                'system_id':          s.get('system_id'),
                'hos':                hos,
                'category':           'MISSING_BUILDING',
                'differences':        {'error': f'HOS {hos!r} no existe en buildings'},
                'recommended_action': 'revision_manual — HOS invalido',
            })
            continue

        result = _check_sensor(s, building)
        rows.append({
            'sensor_id':          s.get('id'),
            'thing_id':           s.get('thing_id'),
            'system_id':          s.get('system_id'),
            'hos':                hos,
            'category':           result['category'],
            'differences':        result['differences'],
            'recommended_action': result['recommended_action'],
        })

    # --- Estadísticas ---
    by_cat = Counter(r['category'] for r in rows)

    # Resumen por campo
    field_missing  = Counter()
    field_mismatch = Counter()
    for r in rows:
        for f in r['differences'].get('missing_fields', []):
            field_missing[f] += 1
        for item in r['differences'].get('mismatch_fields', []):
            field_mismatch[item['field']] += 1

    # Coord stats
    coord_sensor_null   = sum(1 for r in rows if r['differences'].get('coords', {}).get('status') == 'sensor_null')
    coord_building_null = sum(1 for r in rows if r['differences'].get('coords', {}).get('status') == 'building_null')
    coord_mismatch      = sum(1 for r in rows if r['differences'].get('coords', {}).get('status') == 'mismatch')
    coord_needs_review  = sum(1 for r in rows if r['differences'].get('coords', {}).get('needs_review'))
    coord_auto_fix      = coord_mismatch - coord_needs_review

    # Auto-corregibles vs revisión manual
    auto_fixable = sum(1 for r in rows if 'auto' in r['recommended_action'])
    manual_review = sum(1 for r in rows if 'manual' in r['recommended_action'])

    # Top HOS con diferencias
    hos_issues = Counter(r['hos'] for r in rows if r['category'] != 'OK')
    top_hos = hos_issues.most_common(20)

    # Por sistema
    by_sys = defaultdict(Counter)
    for r in rows:
        sys_id = r.get('system_id', '?')
        by_sys[sys_id][r['category']] += 1

    return {
        'generated_at':        datetime.now(timezone.utc).isoformat(),
        'total_sensors':       len(sensors),
        'sensors_with_hos':    len(sensors_with_hos),
        'sensors_without_hos': len(sensors_no_hos),
        'summary': {
            'ok':                        by_cat.get('OK', 0),
            'missing_building':          by_cat.get('MISSING_BUILDING', 0),
            'missing_fields':            by_cat.get('MISSING_FIELDS', 0),
            'mismatch_fields':           by_cat.get('MISMATCH_FIELDS', 0),
            'coordinate_mismatch':       by_cat.get('COORDINATE_MISMATCH', 0),
        },
        'coordinate_detail': {
            'sensor_null_building_has':  coord_sensor_null,
            'building_null_sensor_has':  coord_building_null,
            'both_differ':               coord_mismatch,
            'needs_review_gt100m':       coord_needs_review,
            'auto_fixable_lt100m':       coord_auto_fix,
        },
        'field_missing':       dict(field_missing.most_common()),
        'field_mismatch':      dict(field_mismatch.most_common()),
        'auto_fixable':        auto_fixable,
        'manual_review':       manual_review,
        'top_hos_with_issues': [{'hos': k, 'count': v} for k, v in top_hos],
        'by_system': {
            sys_id: dict(cats)
            for sys_id, cats in sorted(by_sys.items(), key=lambda kv: -sum(kv[1].values()))
        },
        'sensors': rows,
    }


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def build_markdown(audit: dict) -> str:
    s   = audit['summary']
    cd  = audit['coordinate_detail']
    gen = audit['generated_at']

    lines = []
    lines.append('# PIELH — Auditoría Herencia Edificio → Sensor')
    lines.append(f'\n_Generado: {gen}_\n')
    lines.append('> **Solo lectura.** No se ha modificado ningún dato.\n')

    lines.append('---\n## Resumen general\n')
    lines.append('| Métrica | Valor |')
    lines.append('|---|---|')
    lines.append(f'| Total sensores | {audit["total_sensors"]} |')
    lines.append(f'| Sensores con HOS | {audit["sensors_with_hos"]} |')
    lines.append(f'| Sensores sin HOS (excluidos) | {audit["sensors_without_hos"]} |')
    lines.append('')

    lines.append('---\n## Clasificación\n')
    lines.append('| Categoría | Sensores | Descripción |')
    lines.append('|---|---|---|')
    lines.append(f'| OK | {s["ok"]} | Todos los campos heredados correctamente |')
    lines.append(f'| MISSING_FIELDS | {s["missing_fields"]} | Campos vacíos en sensor que el edificio sí tiene |')
    lines.append(f'| COORDINATE_MISMATCH | {s["coordinate_mismatch"]} | Coordenadas distintas al edificio |')
    lines.append(f'| MISMATCH_FIELDS | {s["mismatch_fields"]} | Campos administrativos en conflicto |')
    lines.append(f'| MISSING_BUILDING | {s["missing_building"]} | HOS apunta a edificio inexistente |')
    lines.append(f'| **Auto-corregibles** | **{audit["auto_fixable"]}** | Se pueden rellenar/corregir automáticamente |')
    lines.append(f'| **Revisión manual** | **{audit["manual_review"]}** | Requieren decisión humana |')
    lines.append('')

    lines.append('---\n## Coordenadas\n')
    lines.append('| Situación | Sensores |')
    lines.append('|---|---|')
    lines.append(f'| Sensor sin lat/lon (edificio sí tiene) | {cd["sensor_null_building_has"]} |')
    lines.append(f'| Edificio sin lat/lon (sensor sí tiene) | {cd["building_null_sensor_has"]} |')
    lines.append(f'| Ambos tienen coords pero difieren | {cd["both_differ"]} |')
    lines.append(f'| &nbsp;&nbsp;→ Diferencia >100m (revisar antes de sobrescribir) | {cd["needs_review_gt100m"]} |')
    lines.append(f'| &nbsp;&nbsp;→ Diferencia <100m (auto-corregible, ruido de redondeo) | {cd["auto_fixable_lt100m"]} |')
    lines.append('')

    if audit['field_missing']:
        lines.append('---\n## Campos vacíos en sensor (edificio los tiene)\n')
        lines.append('| Campo | Sensores afectados |')
        lines.append('|---|---|')
        for f, cnt in audit['field_missing'].items():
            lines.append(f'| {f} | {cnt} |')
        lines.append('')

    if audit['field_mismatch']:
        lines.append('---\n## Campos en conflicto (valores distintos)\n')
        lines.append('| Campo | Sensores afectados |')
        lines.append('|---|---|')
        for f, cnt in audit['field_mismatch'].items():
            lines.append(f'| {f} | {cnt} |')
        lines.append('')

    if audit['top_hos_with_issues']:
        lines.append('---\n## Top edificios con más sensores afectados\n')
        lines.append('| HOS | Sensores con diferencias |')
        lines.append('|---|---|')
        for item in audit['top_hos_with_issues']:
            lines.append(f'| {item["hos"]} | {item["count"]} |')
        lines.append('')

    lines.append('---\n## Por sistema\n')
    lines.append('| Sistema | OK | MISSING_FIELDS | COORD_MISMATCH | MISMATCH | MISSING_BLDG |')
    lines.append('|---|---|---|---|---|---|')
    for sys_id, cats in audit['by_system'].items():
        lines.append(
            f'| {sys_id} | {cats.get("OK",0)} | {cats.get("MISSING_FIELDS",0)} '
            f'| {cats.get("COORDINATE_MISMATCH",0)} | {cats.get("MISMATCH_FIELDS",0)} '
            f'| {cats.get("MISSING_BUILDING",0)} |'
        )
    lines.append('')

    # Muestra de casos representativos
    for cat in ('MISSING_BUILDING', 'MISMATCH_FIELDS', 'COORDINATE_MISMATCH', 'MISSING_FIELDS'):
        sample = [r for r in audit['sensors'] if r['category'] == cat][:3]
        if not sample:
            continue
        lines.append(f'---\n## Muestra: {cat}\n')
        for r in sample:
            lines.append(f'- **{r["sensor_id"]}** (HOS `{r["hos"]}`, sys `{r["system_id"]}`)')
            lines.append(f'  - Acción: _{r["recommended_action"]}_')
            for k, v in r['differences'].items():
                lines.append(f'  - {k}: {v}')
        lines.append('')

    lines.append('---')
    lines.append('_PIELH Smart City — Auditoría FASE 0 — Solo lectura._')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='PIELH — Auditoría herencia edificio→sensor')
    parser.add_argument('--master', default=None)
    args = parser.parse_args()

    base_dir    = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    audit_dir   = base_dir / 'data' / 'audits'

    print(f'[PIELH] Leyendo: {master_path.name}')
    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)

    audit = build_audit(master)
    s     = audit['summary']
    cd    = audit['coordinate_detail']

    audit_dir.mkdir(parents=True, exist_ok=True)
    json_out = audit_dir / 'sensor_building_inheritance_audit.json'
    md_out   = audit_dir / 'sensor_building_inheritance_report.md'
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(build_markdown(audit))

    sep = '-' * 52
    print(f'\n[PIELH] HERENCIA EDIFICIO->SENSOR {sep}')
    print(f'  Sensores con HOS:          {audit["sensors_with_hos"]}')
    print(f'  OK (herencia correcta):    {s["ok"]}')
    print(f'  MISSING_FIELDS:            {s["missing_fields"]}')
    print(f'  COORDINATE_MISMATCH:       {s["coordinate_mismatch"]}')
    print(f'    > 100m (revisar):        {cd["needs_review_gt100m"]}')
    print(f'    < 100m (auto):           {cd["auto_fixable_lt100m"]}')
    print(f'  MISMATCH_FIELDS:           {s["mismatch_fields"]}')
    print(f'  MISSING_BUILDING:          {s["missing_building"]}')
    print(f'')
    print(f'  Auto-corregibles:          {audit["auto_fixable"]}')
    print(f'  Revision manual:           {audit["manual_review"]}')
    print(sep)
    if audit['field_missing']:
        print(f'  Campos vacios mas comunes:')
        for f, cnt in list(audit['field_missing'].items())[:5]:
            print(f'    {f}: {cnt}')
    print(f'  JSON: {json_out}')
    print(f'  MD:   {md_out}')


if __name__ == '__main__':
    main()
