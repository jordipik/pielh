"""
PIELH FASE 0 — Aplicación de asignaciones HOS a sensores sin edificio
Lee data/audits/sensors_without_hos_audit.json y aplica los 81 candidatos HIGH.
Genera backup + informe de cambios.
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Campos del edificio que se propagan al sensor
BUILDING_TO_SENSOR_FIELDS = [
    'district_code', 'district_name',
    'neighborhood_key', 'neighborhood',
    'type', 'zone', 'street_etra',
]

# Campos del sensor que NUNCA se tocan
PROTECTED_FIELDS = {
    'thing_id', 'thing_token', 'iot_health', 'raw',
    'system_id', 'system_name', 'id',
}


# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def _backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime('%Y%m%d_%H%M%S')
    dst = backup_dir / f'pielh_qa_master_{ts}.json'
    shutil.copy2(master_path, dst)
    # Rotación: mantener solo los últimos 20
    backups = sorted(backup_dir.glob('pielh_qa_master_*.json'))
    for old in backups[:-20]:
        old.unlink(missing_ok=True)
    return dst


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def apply_assignments(master: dict, candidates: list) -> dict:
    """
    Aplica hos + propagación de campos a los sensores del master.
    Devuelve dict con resultados.
    """
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])

    # Índices
    buildings_by_id    = {b['id']: b for b in buildings if b.get('id')}
    sensors_by_thing   = {s['thing_id']: s for s in sensors if s.get('thing_id')}

    applied   = []
    skipped   = []

    for row in candidates:
        thing_id      = row.get('thing_id')
        candidate_hos = row.get('candidate_hos')
        category      = row.get('category')

        # Guardia: identificador único
        if not thing_id:
            skipped.append({'row': row, 'reason': 'sin thing_id'})
            continue

        # Guardia: HOS existe en buildings
        if not candidate_hos or candidate_hos not in buildings_by_id:
            skipped.append({'row': row, 'reason': f'candidate_hos {candidate_hos!r} no existe en buildings'})
            continue

        # Localizar sensor
        sensor = sensors_by_thing.get(thing_id)
        if not sensor:
            skipped.append({'row': row, 'reason': f'thing_id {thing_id!r} no encontrado en master'})
            continue

        # Guardia: ya tiene HOS (no debería pasar, pero seguro)
        if sensor.get('hos'):
            skipped.append({'row': row, 'reason': f'sensor ya tiene hos={sensor["hos"]}'})
            continue

        building = buildings_by_id[candidate_hos]
        changes  = {}

        # Asignar HOS
        sensor['hos'] = candidate_hos
        changes['hos'] = candidate_hos

        # building_name desde edificio si el sensor lo tiene vacío
        if not sensor.get('building_name') and building.get('name'):
            sensor['building_name'] = building['name']
            changes['building_name'] = building['name']

        # Propagar campos del edificio (solo si el campo está vacío en el sensor)
        for field in BUILDING_TO_SENSOR_FIELDS:
            val = building.get(field)
            if val and not sensor.get(field):
                sensor[field] = val
                changes[field] = val

        applied.append({
            'thing_id':      thing_id,
            'sensor_id':     row.get('sensor_id'),
            'category':      category,
            'hos':           candidate_hos,
            'building_name': building.get('name', ''),
            'changes':       changes,
        })

    return {
        'total_candidates': len(candidates),
        'applied':          len(applied),
        'skipped':          len(skipped),
        'applied_list':     applied,
        'skipped_list':     skipped,
    }


# ---------------------------------------------------------------------------
# Informe
# ---------------------------------------------------------------------------

def build_report(result: dict, backup_path: Path) -> dict:
    from collections import Counter
    applied = result['applied_list']
    skipped = result['skipped_list']

    by_cat = Counter(r['category'] for r in applied)
    by_hos = Counter(r['hos'] for r in applied)
    skip_reasons = Counter(r['reason'] for r in skipped)

    return {
        'generated_at':     datetime.now(timezone.utc).isoformat(),
        'backup':           str(backup_path),
        'total_candidates': result['total_candidates'],
        'applied':          result['applied'],
        'skipped':          result['skipped'],
        'applied_by_category': dict(by_cat),
        'applied_by_hos':      dict(by_hos.most_common(30)),
        'skipped_reasons':     dict(skip_reasons),
        'applied_sample':      applied[:10],
        'skipped_detail':      skipped,
    }


def build_markdown(report: dict) -> str:
    lines = []
    lines.append('# PIELH — Aplicación HOS: Informe de cambios')
    lines.append(f'\n_Generado: {report["generated_at"]}_\n')
    lines.append(f'_Backup: `{Path(report["backup"]).name}`_\n')

    lines.append('---\n## Resumen\n')
    lines.append('| Métrica | Valor |')
    lines.append('|---|---|')
    lines.append(f'| Candidatos HIGH | {report["total_candidates"]} |')
    lines.append(f'| **Aplicados** | **{report["applied"]}** |')
    lines.append(f'| Saltados | {report["skipped"]} |')
    lines.append('')

    lines.append('---\n## Por categoría\n')
    lines.append('| Categoría | Aplicados |')
    lines.append('|---|---|')
    for cat, cnt in report['applied_by_category'].items():
        lines.append(f'| {cat} | {cnt} |')
    lines.append('')

    lines.append('---\n## Por edificio (HOS)\n')
    lines.append('| HOS | Sensores asignados |')
    lines.append('|---|---|')
    for hos, cnt in report['applied_by_hos'].items():
        lines.append(f'| {hos} | {cnt} |')
    lines.append('')

    if report['skipped_reasons']:
        lines.append('---\n## Saltados por motivo\n')
        lines.append('| Motivo | Cantidad |')
        lines.append('|---|---|')
        for reason, cnt in report['skipped_reasons'].items():
            lines.append(f'| {reason} | {cnt} |')
        lines.append('')

    lines.append('---\n## Muestra de cambios aplicados\n')
    lines.append('| thing_id (corto) | sensor_id | Categoría | HOS | Campos propagados |')
    lines.append('|---|---|---|---|---|')
    for r in report['applied_sample']:
        tid_short = (r['thing_id'] or '')[:12]
        fields = ', '.join(k for k in r['changes'] if k not in ('hos', 'building_name'))
        lines.append(f'| {tid_short} | {r["sensor_id"]} | {r["category"]} | {r["hos"]} | {fields or "-"} |')
    lines.append('')
    lines.append('---')
    lines.append('_PIELH Smart City — Asignación automática HOS — Solo HIGH confidence._')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='PIELH — Aplicar asignaciones HOS (HIGH confidence)')
    parser.add_argument('--master',    default=None, help='Ruta a pielh_qa_master.json')
    parser.add_argument('--audit',     default=None, help='Ruta a sensors_without_hos_audit.json')
    parser.add_argument('--dry-run',   action='store_true', help='Simular sin guardar cambios')
    args = parser.parse_args()

    base_dir    = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    audit_path  = Path(args.audit)  if args.audit  else base_dir / 'data' / 'audits' / 'sensors_without_hos_audit.json'
    backup_dir  = base_dir / 'data' / 'backups'
    audit_dir   = base_dir / 'data' / 'audits'

    print(f'[PIELH] Master:  {master_path.name}')
    print(f'[PIELH] Audit:   {audit_path.name}')

    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)
    with open(audit_path, encoding='utf-8') as f:
        audit_data = json.load(f)

    # Seleccionar solo candidatos HIGH con candidate_hos
    candidates = [
        r for r in audit_data.get('sensors', [])
        if r.get('confidence') == 'HIGH'
        and r.get('category') in ('BUILDING_MATCH_BY_ID', 'DUPLICATE_OR_SIBLING')
        and r.get('candidate_hos')
    ]
    print(f'[PIELH] Candidatos HIGH: {len(candidates)}')

    if args.dry_run:
        print('[PIELH] DRY RUN — no se guardarán cambios')

    # Backup
    backup_path = _backup(master_path, backup_dir)
    print(f'[PIELH] Backup:  {backup_path.name}')

    # Aplicar
    result = apply_assignments(master, candidates)

    # Guardar master (salvo dry-run)
    if not args.dry_run:
        with open(master_path, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        print(f'[PIELH] Master guardado.')

    # Informe
    report = build_report(result, backup_path)
    json_out = audit_dir / 'hos_assignments_applied.json'
    md_out   = audit_dir / 'hos_assignments_applied.md'
    audit_dir.mkdir(parents=True, exist_ok=True)
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(build_markdown(report))

    sep = '-' * 52
    print(f'\n[PIELH] RESULTADO {sep}')
    print(f'  Candidatos:  {report["total_candidates"]}')
    print(f'  Aplicados:   {report["applied"]}')
    print(f'  Saltados:    {report["skipped"]}')
    if report['skipped_reasons']:
        for reason, cnt in report['skipped_reasons'].items():
            print(f'    - {reason}: {cnt}')
    print(f'  Por categoria:')
    for cat, cnt in report['applied_by_category'].items():
        print(f'    {cat}: {cnt}')
    print(sep)
    print(f'  JSON: {json_out}')
    print(f'  MD:   {md_out}')


if __name__ == '__main__':
    main()
