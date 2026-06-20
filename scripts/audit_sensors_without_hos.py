"""
PIELH FASE 0 — Auditoría de sensores sin HOS asignado
Solo lectura. No modifica pielh_qa_master.json.

Categorías:
  DUPLICATE_OR_SIBLING  — id existe en otro sensor que ya tiene hos
  BUILDING_MATCH_BY_ID  — id contiene HOS\d+ que existe en buildings
  STREET_SENSOR         — id es EUI/serial/numérico de hardware sin referencia a edificio
  UNKNOWN               — no se puede determinar
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Patrón HOS en el id del sensor
_HOS_PAT = re.compile(r'HOS\d+', re.IGNORECASE)

# Patrones de IDs de hardware (EUI LoRa, seriales, numéricos largos)
# Se clasifica como STREET_SENSOR si encaja uno de estos
_HARDWARE_PATTERNS = [
    re.compile(r'^[0-9a-fA-F]{16}$'),              # EUI LoRa 16 hex: 70B3D5CEC0000380
    re.compile(r'^[0-9a-fA-F]{8}[0-9a-fA-F]+$', re.I),  # hex largo variante
    re.compile(r'^[A-Z]\d{2}[A-Z]{2}\d+[A-Z]$'),   # serial alfanum S06: I17BE085778O
    re.compile(r'^[A-Z]\d{2}[A-Z]{2}\d+$'),         # variante sin sufijo
    re.compile(r'^[A-Z]\d{2}[A-Z]{2}\d+[A-Z]\d+$'),# variante larga: D8683450...
    re.compile(r'^\d{14,}$'),                       # numérico muy largo (S05): 22323387990187
    re.compile(r'^ID[A-Z0-9]{10,}$'),               # SIP NodoIoT: ID0200J23007500262
    re.compile(r'^\d{1,4}$'),                       # numérico corto S08: 1112, 1113
]

# Prefijos de ID compuesto: "S06-01 SERIAL" → el prefijo indica sistema, no edificio
_COMPOUND_PREFIX_PAT = re.compile(r'^[A-Z]\d{2}-\d{2}\s+\S+$')  # ej: S06-01 I17BC095962D

# IDs explícitamente marcados como duplicados o genéricos
_GENERIC_NAMES = {'SISTEMA_4', 'SISTEMA_5', 'SISTEMA_6', 'ZZ-DUPLICADO'}


def _is_hardware_id(sid: str) -> bool:
    if not sid:
        return False
    if any(p.match(sid) for p in _HARDWARE_PATTERNS):
        return True
    # Compuesto: prefijo_sistema ESPACIO serial
    if _COMPOUND_PREFIX_PAT.match(sid):
        return True
    # Empieza con prefijo sistema y contiene serial tras espacio
    parts = sid.split()
    if len(parts) == 2 and any(p.match(parts[1]) for p in _HARDWARE_PATTERNS):
        return True
    return False


# ---------------------------------------------------------------------------
# Clasificación
# ---------------------------------------------------------------------------

def classify_sensor(sensor: dict, hos_ids: set, ids_with_hos: set) -> dict:
    """
    Devuelve {'category': ..., 'candidate_hos': ..., 'confidence': ..., 'reason': ...}
    """
    sid = sensor.get('id', '') or ''

    # 1. Hermano
    if sid in ids_with_hos:
        return {
            'category': 'DUPLICATE_OR_SIBLING',
            'candidate_hos': None,   # se resuelve en post-proceso con el hermano
            'confidence': 'HIGH',
            'reason': 'id existe en otro sensor con hos asignado',
        }

    # 2. HOS en el ID
    hos_matches = _HOS_PAT.findall(sid)
    if hos_matches:
        candidate = hos_matches[0].upper()
        if candidate in hos_ids:
            return {
                'category': 'BUILDING_MATCH_BY_ID',
                'candidate_hos': candidate,
                'confidence': 'HIGH',
                'reason': f'patron {candidate} encontrado en id del sensor',
            }
        else:
            return {
                'category': 'UNKNOWN',
                'candidate_hos': candidate,
                'confidence': 'LOW',
                'reason': f'patron {candidate} en id pero no existe en buildings',
            }

    # 3. Hardware ID
    if _is_hardware_id(sid):
        return {
            'category': 'STREET_SENSOR',
            'candidate_hos': None,
            'confidence': 'MEDIUM',
            'reason': 'id con formato EUI/serial/numerico de hardware sin referencia a edificio',
        }

    # 4. Desconocido
    return {
        'category': 'UNKNOWN',
        'candidate_hos': None,
        'confidence': 'LOW',
        'reason': 'no coincide con ningun patron conocido',
    }


# ---------------------------------------------------------------------------
# Resolución de hermanos
# ---------------------------------------------------------------------------

def _resolve_sibling_hos(sensor: dict, with_hos_list: list):
    """Devuelve el hos del hermano con hos asignado, si existe."""
    sid = sensor.get('id')
    if not sid:
        return None
    match = next((s for s in with_hos_list if s.get('id') == sid and s.get('hos')), None)
    return match['hos'] if match else None


# ---------------------------------------------------------------------------
# Build audit
# ---------------------------------------------------------------------------

def build_audit(master: dict) -> dict:
    sensors   = master.get('sensors', [])
    buildings = master.get('buildings', [])
    catalogs  = master.get('catalogs', {})
    systems_cat = {s['id']: s.get('name', s['id']) for s in catalogs.get('systems', []) if 'id' in s}

    hos_ids      = {b['id'] for b in buildings if b.get('id')}
    with_hos     = [s for s in sensors if s.get('hos')]
    ids_with_hos = {s['id'] for s in with_hos if s.get('id')}
    no_hos       = [s for s in sensors if not s.get('hos')]

    # Broken HOS: tiene hos pero no existe en buildings
    broken_hos = [s for s in sensors if s.get('hos') and s['hos'] not in hos_ids]

    rows = []
    for s in no_hos:
        clf = classify_sensor(s, hos_ids, ids_with_hos)
        candidate_hos = clf['candidate_hos']

        # Para hermanos: buscar el HOS del hermano
        if clf['category'] == 'DUPLICATE_OR_SIBLING':
            candidate_hos = _resolve_sibling_hos(s, with_hos)

        sys_id   = s.get('system_id', '')
        sys_name = systems_cat.get(sys_id, sys_id)

        rows.append({
            'sensor_id':     s.get('id'),
            'thing_id':      s.get('thing_id'),
            'thing_token':   s.get('thing_token'),
            'system_id':     sys_id,
            'system_name':   sys_name,
            'building_name': s.get('building_name', ''),
            'ref_etra':      s.get('ref_etra'),
            'lat':           s.get('lat'),
            'lon':           s.get('lon'),
            'tags':          s.get('tags', ''),
            'iot_status':    (s.get('iot_health') or {}).get('status'),
            'category':      clf['category'],
            'candidate_hos': candidate_hos,
            'confidence':    clf['confidence'],
            'reason':        clf['reason'],
        })

    # --- Estadísticas ---
    by_cat = Counter(r['category'] for r in rows)
    by_sys = Counter(r['system_id'] for r in rows)
    by_sys_cat = defaultdict(Counter)
    for r in rows:
        by_sys_cat[r['system_id']][r['category']] += 1

    # Candidatos automáticos con alta confianza
    auto_candidates = [r for r in rows if r['confidence'] == 'HIGH' and r['candidate_hos']]

    # Top edificios candidatos
    from collections import Counter as _C
    top_buildings = _C(r['candidate_hos'] for r in rows if r.get('candidate_hos')).most_common(20)

    return {
        'generated_at':          datetime.now(timezone.utc).isoformat(),
        'total_sensors':         len(sensors),
        'total_buildings':       len(buildings),
        'total_sin_hos':         len(no_hos),
        'total_broken_hos':      len(broken_hos),
        'summary': {
            'BUILDING_MATCH_BY_ID':   by_cat.get('BUILDING_MATCH_BY_ID', 0),
            'DUPLICATE_OR_SIBLING':   by_cat.get('DUPLICATE_OR_SIBLING', 0),
            'STREET_SENSOR':          by_cat.get('STREET_SENSOR', 0),
            'UNKNOWN':                by_cat.get('UNKNOWN', 0),
        },
        'auto_assignable':       len(auto_candidates),
        'top_candidate_buildings': [{'hos': k, 'count': v} for k, v in top_buildings],
        'by_system': {
            sys_id: {
                'total':    by_sys[sys_id],
                'by_cat':   dict(by_sys_cat[sys_id]),
            }
            for sys_id in sorted(by_sys, key=lambda k: -by_sys[k])
        },
        'broken_hos': [
            {'id': s.get('id'), 'hos': s.get('hos'), 'system_id': s.get('system_id')}
            for s in broken_hos
        ],
        'sensors': rows,
    }


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def build_markdown(audit: dict) -> str:
    s   = audit['summary']
    gen = audit['generated_at']
    lines = []
    lines.append('# PIELH — Auditoría Sensores sin HOS')
    lines.append(f'\n_Generado: {gen}_\n')
    lines.append('> **Solo lectura.** No se ha modificado ningún dato.\n')

    lines.append('---\n## Resumen\n')
    lines.append(f'| Métrica | Valor |')
    lines.append(f'|---|---|')
    lines.append(f'| Total sensores | {audit["total_sensors"]} |')
    lines.append(f'| Total edificios | {audit["total_buildings"]} |')
    lines.append(f'| **Sensores sin HOS** | **{audit["total_sin_hos"]}** |')
    lines.append(f'| HOS roto (no existe en buildings) | {audit["total_broken_hos"]} |')
    lines.append('')

    lines.append('---\n## Clasificación\n')
    lines.append('| Categoría | Sensores | Descripción |')
    lines.append('|---|---|---|')
    lines.append(f'| BUILDING_MATCH_BY_ID | {s["BUILDING_MATCH_BY_ID"]} | `id` contiene `HOSxxx` que existe en buildings — asignable automáticamente |')
    lines.append(f'| DUPLICATE_OR_SIBLING | {s["DUPLICATE_OR_SIBLING"]} | Hermano de un sensor con HOS ya asignado — asignable automáticamente |')
    lines.append(f'| STREET_SENSOR | {s["STREET_SENSOR"]} | ID de hardware (EUI/serial) sin referencia a edificio — sensor urbano independiente |')
    lines.append(f'| UNKNOWN | {s["UNKNOWN"]} | No se puede determinar automáticamente — revisión manual |')
    lines.append(f'| **Total asignables automáticamente** | **{audit["auto_assignable"]}** | BUILDING_MATCH_BY_ID + DUPLICATE_OR_SIBLING con HOS resuelto |')
    lines.append('')

    lines.append('---\n## Por sistema\n')
    lines.append('| Sistema | Total sin HOS | MATCH_BY_ID | SIBLING | STREET | UNKNOWN |')
    lines.append('|---|---|---|---|---|---|')
    for sys_id, d in audit['by_system'].items():
        bc = d['by_cat']
        lines.append(
            f'| {sys_id} | {d["total"]} '
            f'| {bc.get("BUILDING_MATCH_BY_ID",0)} '
            f'| {bc.get("DUPLICATE_OR_SIBLING",0)} '
            f'| {bc.get("STREET_SENSOR",0)} '
            f'| {bc.get("UNKNOWN",0)} |'
        )
    lines.append('')

    if audit['top_candidate_buildings']:
        lines.append('---\n## Top edificios candidatos (asignación automática)\n')
        lines.append('| HOS | Sensores candidatos |')
        lines.append('|---|---|')
        for item in audit['top_candidate_buildings']:
            lines.append(f'| {item["hos"]} | {item["count"]} |')
        lines.append('')

    if audit['broken_hos']:
        lines.append('---\n## HOS rotos (apuntan a edificio inexistente)\n')
        lines.append('| Sensor ID | HOS (roto) | Sistema |')
        lines.append('|---|---|---|')
        for b in audit['broken_hos']:
            lines.append(f'| {b["id"]} | {b["hos"]} | {b["system_id"]} |')
        lines.append('')

    lines.append('---\n## Detalle sensores sin HOS\n')
    lines.append('| Sensor ID | Sistema | Categoría | Candidato HOS | Confianza | Motivo |')
    lines.append('|---|---|---|---|---|---|')
    for r in audit['sensors']:
        lines.append(
            f'| {r["sensor_id"]} | {r["system_id"]} | {r["category"]} '
            f'| {r["candidate_hos"] or "-"} | {r["confidence"]} | {r["reason"]} |'
        )
    lines.append('')
    lines.append('---')
    lines.append('_PIELH Smart City — Auditoría FASE 0 — Solo lectura._')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main / run_audit_hos (reutilizable)
# ---------------------------------------------------------------------------

def run_audit_hos(master: dict, audit_dir: Path) -> dict:
    """Genera auditoría de sensores sin HOS. Devuelve el dict del audit."""
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit = build_audit(master)
    json_out = audit_dir / 'sensors_without_hos_audit.json'
    md_out   = audit_dir / 'sensors_without_hos_report.md'
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(build_markdown(audit))
    return audit


def main():
    parser = argparse.ArgumentParser(description='PIELH — Auditoría sensores sin HOS')
    parser.add_argument('--master', default=None, help='Ruta a pielh_qa_master.json')
    args = parser.parse_args()

    base_dir  = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    audit_dir   = base_dir / 'data' / 'audits'

    print(f'[PIELH] Leyendo: {master_path.name}')
    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)

    audit = run_audit_hos(master, audit_dir)
    s = audit['summary']

    sep = '-' * 52
    print(f'\n[PIELH] SENSORES SIN HOS {sep}')
    print(f'  Total sin HOS:              {audit["total_sin_hos"]}')
    print(f'  BUILDING_MATCH_BY_ID:       {s["BUILDING_MATCH_BY_ID"]}')
    print(f'  DUPLICATE_OR_SIBLING:       {s["DUPLICATE_OR_SIBLING"]}')
    print(f'  STREET_SENSOR:              {s["STREET_SENSOR"]}')
    print(f'  UNKNOWN:                    {s["UNKNOWN"]}')
    print(f'')
    print(f'  Asignables automaticamente: {audit["auto_assignable"]}')
    print(f'  Probablemente urbanos:      {s["STREET_SENSOR"]}')
    print(f'  Revision manual:            {s["UNKNOWN"]}')
    print(sep)
    json_out = audit_dir / 'sensors_without_hos_audit.json'
    md_out   = audit_dir / 'sensors_without_hos_report.md'
    print(f'  JSON: {json_out}')
    print(f'  MD:   {md_out}')


if __name__ == '__main__':
    main()
