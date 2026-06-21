#!/usr/bin/env python3
"""
audit_duplicate_sensors.py
Auditoria de sensores duplicados, sustituidos y con conflictos en pielh_qa_master.json.
Solo lectura. No modifica ningun archivo JSON.

Detecciones:
  - Mismo sensor ID en multiples registros
  - Mismo thing_id en multiples registros
  - Mismo thing_token en multiples registros
  - Mismo HOS + mismo system_id (posibles duplicados fisicos)
  - Distancia geografica < 5 m dentro del mismo grupo HOS+system_id
  - Similitud de nombre > 80%

Clasificacion por grupo:
  SYNC_CONFLICT      mismo id de texto, things distintos
  DUPLICATE_ACTIVE   dos o mas activos en el mismo HOS+system_id
  REPLACE_CANDIDATE  activo + inactivo con things distintos (sustitucion probable)
  LIKELY_REPLACED    activo + inactivo con mismo thing (datos duplicados)
  DUPLICATE_INACTIVE todos inactivos, HOS+system_id compartido
  OK                 sin incidencias detectadas

Riesgo:
  CRITICAL  SYNC_CONFLICT o DUPLICATE_ACTIVE
  HIGH      REPLACE_CANDIDATE
  MEDIUM    LIKELY_REPLACED o geo < 5m o similitud > 80%
  LOW       DUPLICATE_INACTIVE
"""

import csv
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

ROOT        = Path(__file__).parent.parent
MASTER_FILE = ROOT / 'pielh_qa_master.json'
REPORTS_DIR = ROOT / 'reports'

GEO_THRESHOLD_M   = 5.0
NAME_SIM_THRESHOLD = 0.80


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_active(s):
    ih = s.get('iot_health') or {}
    return (
        ih.get('has_real_data') is True
        or ih.get('demo_ready') is True
        or s.get('has_data') == 'OK'
    )


def days_since(ts_str):
    if not ts_str:
        return None
    try:
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return None


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6_371_000
    f1, f2 = math.radians(lat1), math.radians(lat2)
    df = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def name_sim(a, b):
    return SequenceMatcher(None, a or '', b or '').ratio()


def sensor_last_seen(s):
    ih = s.get('iot_health') or {}
    return ih.get('last_seen') or ''


def classify_group(group, detection_method):
    """Devuelve (classification, risk)."""
    actives   = [s for s in group if is_active(s)]
    inactives = [s for s in group if not is_active(s)]
    thing_ids = {s.get('thing_id', '') for s in group if s.get('thing_id')}
    tokens    = {s.get('thing_token', '') for s in group if s.get('thing_token')}

    # Mismo texto de ID pero things distintos -> conflicto de sincronizacion
    if detection_method == 'same_id' and len(thing_ids) > 1:
        return 'SYNC_CONFLICT', 'CRITICAL'

    if len(actives) >= 2:
        return 'DUPLICATE_ACTIVE', 'CRITICAL'

    if actives and inactives:
        if len(thing_ids) > 1:
            return 'REPLACE_CANDIDATE', 'HIGH'
        return 'LIKELY_REPLACED', 'MEDIUM'

    return 'DUPLICATE_INACTIVE', 'LOW'


def geo_min_dist(group):
    """Distancia minima en metros entre cualquier par con lat/lon. None si no hay pares."""
    pts = [(s, s['lat'], s['lon'])
           for s in group
           if s.get('lat') is not None and s.get('lon') is not None]
    min_d = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = haversine_m(pts[i][1], pts[i][2], pts[j][1], pts[j][2])
            if min_d is None or d < min_d:
                min_d = d
    return min_d


def max_name_sim(group):
    """Similitud maxima de nombre (campo id) entre cualquier par."""
    ids = [s.get('id', '') for s in group]
    max_s = 0.0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            s = name_sim(ids[i], ids[j])
            if s > max_s:
                max_s = s
    return max_s


def sensor_brief(s):
    ih   = s.get('iot_health') or {}
    last = ih.get('last_seen', '')
    age  = days_since(last)
    return {
        'id':          s.get('id', ''),
        'thing_id':    s.get('thing_id', ''),
        'thing_token': s.get('thing_token', ''),
        'hos':         s.get('hos', ''),
        'system_id':   s.get('system_id', ''),
        'active':      is_active(s),
        'last_seen':   last,
        'days_since':  age,
        'lat':         s.get('lat'),
        'lon':         s.get('lon'),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def audit():
    with open(MASTER_FILE, encoding='utf-8') as f:
        master = json.load(f)

    sensors = master.get('sensors', [])
    total   = len(sensors)

    # ── Indices ──────────────────────────────────────────────────────────
    by_id       = defaultdict(list)
    by_thing_id = defaultdict(list)
    by_token    = defaultdict(list)
    by_hos_sys  = defaultdict(list)

    for s in sensors:
        if s.get('id'):
            by_id[s['id']].append(s)
        if s.get('thing_id'):
            by_thing_id[s['thing_id']].append(s)
        if s.get('thing_token'):
            by_token[s['thing_token']].append(s)
        hos = s.get('hos') or ''
        sys = s.get('system_id') or ''
        if hos and sys:
            by_hos_sys[f"{hos}|{sys}"].append(s)

    dup_id_groups  = {k: v for k, v in by_id.items()       if len(v) > 1}
    dup_thing_id   = {k: v for k, v in by_thing_id.items() if len(v) > 1}
    dup_token_grps = {k: v for k, v in by_token.items()    if len(v) > 1}
    dup_hos_sys    = {k: v for k, v in by_hos_sys.items()  if len(v) > 1}

    # ── Construir incidencias ─────────────────────────────────────────────
    incidents = []
    seen_pairs = set()  # evitar duplicar incidencias para el mismo conjunto de sensors

    def add_incident(group, method, key):
        key_frozen = frozenset(id(s) for s in group)
        if key_frozen in seen_pairs:
            return
        seen_pairs.add(key_frozen)

        classification, risk = classify_group(group, method)

        min_dist  = geo_min_dist(group)
        max_sim   = max_name_sim(group)
        geo_close = min_dist is not None and min_dist < GEO_THRESHOLD_M
        name_close = max_sim >= NAME_SIM_THRESHOLD

        # Escalar riesgo por indicadores adicionales
        if risk == 'MEDIUM' and (geo_close or name_close):
            risk = 'HIGH'
        if risk == 'LOW' and geo_close:
            risk = 'MEDIUM'

        incidents.append({
            'group_key':      key,
            'detection':      method,
            'classification': classification,
            'risk':           risk,
            'count':          len(group),
            'actives':        sum(1 for s in group if is_active(s)),
            'inactives':      sum(1 for s in group if not is_active(s)),
            'geo_min_m':      round(min_dist, 2) if min_dist is not None else None,
            'name_sim_max':   round(max_sim, 3),
            'geo_close':      geo_close,
            'name_close':     name_close,
            'sensors':        [sensor_brief(s) for s in group],
        })

    for k, g in dup_id_groups.items():
        add_incident(g, 'same_id', k)
    for k, g in dup_thing_id.items():
        add_incident(g, 'same_thing_id', k)
    for k, g in dup_token_grps.items():
        add_incident(g, 'same_token', k)
    for k, g in dup_hos_sys.items():
        add_incident(g, 'same_hos_system_id', k)

    # Ordenar por riesgo
    _risk_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    incidents.sort(key=lambda i: (_risk_order[i['risk']], -i['count']))

    # ── Estadisticas ─────────────────────────────────────────────────────
    by_risk  = defaultdict(int)
    by_class = defaultdict(int)
    for inc in incidents:
        by_risk[inc['risk']] += 1
        by_class[inc['classification']] += 1

    n_critical    = by_risk['CRITICAL']
    n_high        = by_risk['HIGH']
    n_conflicts   = by_class['SYNC_CONFLICT']
    n_dup_active  = by_class['DUPLICATE_ACTIVE']
    n_replace     = by_class['REPLACE_CANDIDATE']
    n_likely_rep  = by_class['LIKELY_REPLACED']

    # Sensores implicados en algun incidente
    sensor_ids_flagged = set()
    for inc in incidents:
        for sb in inc['sensors']:
            sensor_ids_flagged.add(sb['id'])

    top50 = incidents[:50]

    # ── CSV (backward compat con mark_old_duplicate_sensors.py) ──────────
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_rows = []
    for s in sensors:
        sid   = s.get('id', '')
        tid   = s.get('thing_id', '')
        token = s.get('thing_token', '')
        ih    = s.get('iot_health') or {}
        last  = ih.get('last_seen', '')
        age   = days_since(last)
        group = by_id.get(sid, [s])

        has_active   = any(is_active(x) for x in group)
        has_inactive = any(not is_active(x) for x in group)
        sync_conflict = len(group) > 1 and has_active and has_inactive
        possible_old  = (
            (sync_conflict and not is_active(s))
            or (age is not None and age > 365)
        )

        dup_id  = len(group) > 1
        dup_tok = len(by_token.get(token, [])) > 1 if token else False
        dup_tid = len(by_thing_id.get(tid, [])) > 1 if tid else False

        # risk compatible con el formato original
        if len({x.get('thing_id') for x in group}) > 1 and has_active and has_inactive:
            risk = 'CRITICAL'
        elif dup_tok or dup_tid:
            risk = 'HIGH'
        elif dup_id:
            risk = 'MEDIUM'
        else:
            risk = 'LOW'

        csv_rows.append({
            'id': sid, 'thing_id': tid, 'thing_token': token,
            'hos': s.get('hos', ''), 'system_id': s.get('system_id', ''),
            'building_name': s.get('building_name', ''),
            'has_data': s.get('has_data', ''),
            'has_real_data': ih.get('has_real_data', ''),
            'demo_ready': ih.get('demo_ready', ''),
            'last_seen': last,
            'days_since_seen': age if age is not None else '',
            'duplicate_id': dup_id, 'duplicate_token': dup_tok,
            'duplicate_thing_id': dup_tid,
            'sync_conflict': sync_conflict,
            'possible_old': possible_old,
            'risk': risk,
        })

    csv_path = REPORTS_DIR / 'duplicate_sensors_audit.csv'
    fieldnames = [
        'id', 'thing_id', 'thing_token', 'hos', 'system_id', 'building_name',
        'has_data', 'has_real_data', 'demo_ready', 'last_seen', 'days_since_seen',
        'duplicate_id', 'duplicate_token', 'duplicate_thing_id',
        'sync_conflict', 'possible_old', 'risk',
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(csv_rows)

    # ── JSON ─────────────────────────────────────────────────────────────
    now = datetime.now().isoformat()
    result = {
        '_meta': {
            'generated_at':    now,
            'master_file':     str(MASTER_FILE),
            'master_modified': False,
            'total_sensors':   total,
        },
        'summary': {
            'total_sensors':          total,
            'total_incidents':        len(incidents),
            'sensors_flagged':        len(sensor_ids_flagged),
            'by_risk': {
                'CRITICAL': n_critical,
                'HIGH':     n_high,
                'MEDIUM':   by_risk['MEDIUM'],
                'LOW':      by_risk['LOW'],
            },
            'by_classification': {
                'SYNC_CONFLICT':      n_conflicts,
                'DUPLICATE_ACTIVE':   n_dup_active,
                'REPLACE_CANDIDATE':  n_replace,
                'LIKELY_REPLACED':    n_likely_rep,
                'DUPLICATE_INACTIVE': by_class['DUPLICATE_INACTIVE'],
            },
            'detection_counts': {
                'by_same_id':           len(dup_id_groups),
                'by_same_thing_id':     len(dup_thing_id),
                'by_same_token':        len(dup_token_grps),
                'by_same_hos_system_id': len(dup_hos_sys),
            },
        },
        'top50_incidents': top50,
        'all_incidents':   incidents,
    }

    json_path = REPORTS_DIR / 'audit_duplicate_sensors.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ── MD ───────────────────────────────────────────────────────────────
    def risk_badge(r):
        return {'CRITICAL': '🔴 CRITICAL', 'HIGH': '🟠 HIGH',
                'MEDIUM': '🟡 MEDIUM', 'LOW': '🟢 LOW'}.get(r, r)

    lines = [
        '# Auditoria de Sensores Duplicados y Sustituciones',
        '',
        f'- Generado: {now}',
        f'- Master: `{MASTER_FILE.name}`  |  master_modified: **false**',
        '',
        '## Resumen ejecutivo',
        '',
        '| Concepto | Valor |',
        '|---|---|',
        f'| Total sensores analizados | {total} |',
        f'| Total incidencias detectadas | {len(incidents)} |',
        f'| Sensores implicados en alguna incidencia | {len(sensor_ids_flagged)} |',
        f'| CRITICAL | {n_critical} |',
        f'| HIGH | {n_high} |',
        f'| MEDIUM | {by_risk["MEDIUM"]} |',
        f'| LOW | {by_risk["LOW"]} |',
        '',
        '## Tabla de incidencias por categoria',
        '',
        '| Clasificacion | Descripcion | Total |',
        '|---|---|---|',
        f'| SYNC_CONFLICT | Mismo ID de texto, things distintos | {n_conflicts} |',
        f'| DUPLICATE_ACTIVE | 2+ activos en mismo HOS+sistema | {n_dup_active} |',
        f'| REPLACE_CANDIDATE | Activo + inactivo, things distintos (sustitucion) | {n_replace} |',
        f'| LIKELY_REPLACED | Activo + inactivo, mismo thing (datos duplicados) | {n_likely_rep} |',
        f'| DUPLICATE_INACTIVE | Todos inactivos, HOS+sistema compartido | {by_class["DUPLICATE_INACTIVE"]} |',
        '',
        '## Deteccion por metodo',
        '',
        '| Metodo | Grupos | Descripcion |',
        '|---|---|---|',
        f'| same_id | {len(dup_id_groups)} | Mismo texto de sensor ID |',
        f'| same_thing_id | {len(dup_thing_id)} | Mismo thing_id de TheThings |',
        f'| same_token | {len(dup_token_grps)} | Mismo thing_token de TheThings |',
        f'| same_hos_system_id | {len(dup_hos_sys)} | Mismo edificio HOS y sistema |',
        '',
        f'## Top 50 incidencias criticas / de mayor riesgo',
        '',
        '| # | Riesgo | Clasificacion | Grupo | Sensores | Activos | Geo (m) | Sim nombre |',
        '|---|---|---|---|---|---|---|---|',
    ]

    for i, inc in enumerate(top50, 1):
        geo_str  = f"{inc['geo_min_m']:.1f}" if inc['geo_min_m'] is not None else '—'
        sim_str  = f"{inc['name_sim_max']:.2f}"
        lines.append(
            f"| {i} | {risk_badge(inc['risk'])} | {inc['classification']} | "
            f"`{inc['group_key']}` | {inc['count']} | {inc['actives']} | "
            f"{geo_str} | {sim_str} |"
        )

    # Detalle de los 20 primeros grupos CRITICAL/HIGH
    critical_high = [inc for inc in incidents if inc['risk'] in ('CRITICAL', 'HIGH')][:20]
    if critical_high:
        lines += ['', '## Detalle ejemplos CRITICAL / HIGH (max 20)', '']
        for inc in critical_high:
            lines.append(f"### [{inc['risk']}] `{inc['group_key']}` — {inc['classification']}")
            lines.append(f"- Deteccion: `{inc['detection']}` | Sensores: {inc['count']} "
                         f"| Activos: {inc['actives']} | Inactivos: {inc['inactives']}")
            if inc['geo_min_m'] is not None:
                lines.append(f"- Distancia minima: {inc['geo_min_m']} m")
            lines.append(f"- Similitud nombre: {inc['name_sim_max']:.2f}")
            lines.append('')
            lines.append('| sensor id | thing_id | activo | last_seen | dias |')
            lines.append('|---|---|---|---|---|')
            for sb in inc['sensors']:
                tid_short = (sb['thing_id'] or '')[:30]
                lines.append(
                    f"| {sb['id']} | {tid_short} | {'SI' if sb['active'] else 'NO'} "
                    f"| {sb['last_seen'][:19] if sb['last_seen'] else '—'} "
                    f"| {sb['days_since'] if sb['days_since'] is not None else '?'} |"
                )
            lines.append('')

    # Recomendacion
    lines += ['## Recomendacion de limpieza', '']
    if n_critical > 0:
        lines += [
            f'**PRECAUCION**: {n_critical} incidencias CRITICAL detectadas.',
            '',
            '- `SYNC_CONFLICT`: Mismo ID de texto asignado a things distintos. '
            'Puede causar errores 404 en sincronizacion con TheThings. '
            'Revisar manualmente y renombrar el registro incorrecto.',
            '',
            '- `DUPLICATE_ACTIVE`: Dos sensores activos para el mismo HOS+sistema. '
            'Determinar cual es el dispositivo real y marcar el otro como OLD.',
        ]
    if n_high > 0:
        lines += [
            '',
            f'**AVISO**: {n_high} incidencias HIGH (`REPLACE_CANDIDATE`).',
            'Probable sustitucion de dispositivo. El sensor inactivo puede marcarse como OLD '
            'usando `scripts/mark_old_duplicate_sensors.py` tras verificacion manual.',
        ]
    if n_critical == 0 and n_high == 0:
        lines += ['Sin riesgos CRITICAL ni HIGH. Estado del inventario aceptable.']

    lines += [
        '',
        '---',
        f'CSV compatibilidad: `reports/duplicate_sensors_audit.csv`',
        f'JSON completo     : `reports/audit_duplicate_sensors.json`',
    ]

    md_path = REPORTS_DIR / 'audit_duplicate_sensors.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # ── Consola ──────────────────────────────────────────────────────────
    print('=' * 65)
    print('PIELH - Auditoria de Sensores Duplicados')
    print(f'Fecha : {now}')
    print('=' * 65)
    print(f'  Total sensores         : {total}')
    print(f'  Total incidencias      : {len(incidents)}')
    print(f'  Sensores implicados    : {len(sensor_ids_flagged)}')
    print()
    print(f'  CRITICAL               : {n_critical}')
    print(f'  HIGH                   : {n_high}')
    print(f'  MEDIUM                 : {by_risk["MEDIUM"]}')
    print(f'  LOW                    : {by_risk["LOW"]}')
    print()
    print(f'  SYNC_CONFLICT          : {n_conflicts}')
    print(f'  DUPLICATE_ACTIVE       : {n_dup_active}')
    print(f'  REPLACE_CANDIDATE      : {n_replace}')
    print(f'  LIKELY_REPLACED        : {n_likely_rep}')
    print(f'  DUPLICATE_INACTIVE     : {by_class["DUPLICATE_INACTIVE"]}')
    print()
    print(f'  Grupos por same_id           : {len(dup_id_groups)}')
    print(f'  Grupos por same_thing_id     : {len(dup_thing_id)}')
    print(f'  Grupos por same_token        : {len(dup_token_grps)}')
    print(f'  Grupos por same_hos_system_id: {len(dup_hos_sys)}')
    print()
    print(f'[OK] {csv_path}')
    print(f'[OK] {json_path}')
    print(f'[OK] {md_path}')
    print()
    print('TOP 10 INCIDENCIAS')
    for i, inc in enumerate(incidents[:10], 1):
        geo = f" geo={inc['geo_min_m']}m" if inc['geo_min_m'] is not None else ''
        print(f"  {i:2}. [{inc['risk']:8}] {inc['classification']:20} | {inc['group_key']}{geo}")

    return result


if __name__ == '__main__':
    audit()
