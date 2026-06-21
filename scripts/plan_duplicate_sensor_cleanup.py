#!/usr/bin/env python3
"""
plan_duplicate_sensor_cleanup.py
Plan de limpieza dry-run para sensores duplicados/conflictivos.
Solo lectura. No modifica pielh_qa_master.json ni ningun otro dato.
"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT        = Path(__file__).parent.parent
AUDIT_JSON  = ROOT / 'reports' / 'audit_duplicate_sensors.json'
PROBE_JSON  = ROOT / 'data' / 'thethings_snapshots' / 'latest' / 'thethings_resources_probe.json'
MASTER_FILE = ROOT / 'pielh_qa_master.json'
REPORTS_DIR = ROOT / 'reports'

RECENT_DATA_DAYS = 30   # diferencia minima para decidir por last_seen


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_dt(ts_str):
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except Exception:
        return None


def days_between(ts_a, ts_b):
    da, db = parse_dt(ts_a), parse_dt(ts_b)
    if da and db:
        return abs((da - db).days)
    return None


def score_sensor(item):
    """Puntuacion para desempatar cuando no hay datos claros."""
    s = 0
    if item.get('has_real_data'):
        s += 100
    if item.get('thing_token_present'):
        s += 20
    if item.get('hos'):
        s += 10
    if item.get('lat') is not None:
        s += 5
    return s


# ---------------------------------------------------------------------------
# Construir indice de datos del probe por thing_id
# ---------------------------------------------------------------------------

def load_probe_index(probe_path):
    """thing_id -> {has_real_data, last_seen, thing_token_present}"""
    if not probe_path.exists():
        return {}
    data  = json.loads(probe_path.read_text(encoding='utf-8'))
    index = {}
    for s in data.get('sensors', []):
        tid = s.get('thing_id', '')
        if tid:
            index[tid] = {
                'has_real_data':      s.get('has_real_data', False),
                'last_seen':          s.get('last_seen') or '',
                'thing_token_present': s.get('thing_token_present', False),
            }
    return index


# ---------------------------------------------------------------------------
# Enriquecer sensor del incidente con datos del probe
# ---------------------------------------------------------------------------

def enrich(sensor_brief, probe_index):
    tid  = sensor_brief.get('thing_id', '')
    prob = probe_index.get(tid, {})
    return {
        'id':                sensor_brief.get('id', ''),
        'thing_id':          tid,
        'thing_token':       sensor_brief.get('thing_token', ''),
        'thing_token_present': bool(sensor_brief.get('thing_token') or prob.get('thing_token_present')),
        'hos':               sensor_brief.get('hos', ''),
        'system_id':         sensor_brief.get('system_id', ''),
        'active':            sensor_brief.get('active', False),
        'has_real_data':     prob.get('has_real_data', sensor_brief.get('active', False)),
        'last_seen':         prob.get('last_seen') or sensor_brief.get('last_seen', ''),
        'days_since':        sensor_brief.get('days_since'),
        'lat':               sensor_brief.get('lat'),
        'lon':               sensor_brief.get('lon'),
    }


# ---------------------------------------------------------------------------
# Reglas de decision
# ---------------------------------------------------------------------------

def decide_sync_conflict(items):
    """SYNC_CONFLICT: mismo id visible, things distintos."""
    with_data    = [it for it in items if it['has_real_data']]
    without_data = [it for it in items if not it['has_real_data']]

    if len(with_data) == 1:
        winner = with_data[0]
        for it in items:
            it['decision'] = 'KEEP'      if it is winner else 'MARK_LEGACY'
            it['reason']   = ('unico sensor con datos reales'
                              if it is winner else 'sin datos reales, sustituido')
        return 'HIGH', f"KEEP {winner['id'][:30]} (unico con datos)"

    if len(with_data) > 1:
        # Ordenar por last_seen descendente
        with_data_sorted = sorted(
            with_data,
            key=lambda x: x['last_seen'] or '',
            reverse=True,
        )
        newest = with_data_sorted[0]
        oldest = with_data_sorted[-1]
        diff   = days_between(newest['last_seen'], oldest['last_seen'])

        if diff is not None and diff > RECENT_DATA_DAYS:
            # Ganador claro: el mas reciente
            for it in items:
                if it is newest:
                    it['decision'] = 'KEEP'
                    it['reason']   = f"datos mas recientes (diff {diff}d)"
                elif it['has_real_data']:
                    it['decision'] = 'MARK_LEGACY'
                    it['reason']   = f"datos mas antiguos (diff {diff}d vs winner)"
                else:
                    it['decision'] = 'MARK_LEGACY'
                    it['reason']   = 'sin datos reales'
            return 'MEDIUM', f"KEEP mas reciente (diff {diff}d), {len(with_data)-1} MARK_LEGACY"

        # Diferencia < 30 dias: no decidir
        for it in items:
            it['decision'] = 'MANUAL_REVIEW'
            it['reason']   = f"varios activos con datos recientes (diff {diff}d si disponible)"
        return 'LOW', f"MANUAL_REVIEW — {len(with_data)} sensores activos con datos recientes"

    # Ninguno con datos: desempatar por puntuacion
    ranked = sorted(items, key=score_sensor, reverse=True)
    best   = ranked[0]
    rest   = ranked[1:]
    scores = [score_sensor(it) for it in items]

    if len(set(scores)) == 1:
        # Empate total
        for it in items:
            it['decision'] = 'MANUAL_REVIEW'
            it['reason']   = 'ninguno tiene datos y puntuacion identica'
        return 'LOW', 'MANUAL_REVIEW — empate sin datos'

    for it in items:
        if it is best:
            it['decision'] = 'MARK_LEGACY'   # No podemos KEEP sin certeza
            it['reason']   = f"candidato preferido por puntuacion ({score_sensor(it)}), sin datos verificados"
        else:
            it['decision'] = 'MARK_LEGACY'
            it['reason']   = f"puntuacion inferior ({score_sensor(it)}), sin datos"
    # En caso sin datos reales no hacemos KEEP automatico: todo MANUAL_REVIEW
    for it in items:
        it['decision'] = 'MANUAL_REVIEW'
        it['reason']   = 'ninguno tiene datos reales verificados'
    return 'LOW', 'MANUAL_REVIEW — ninguno con datos verificados'


def decide_replace_candidate(items):
    """REPLACE_CANDIDATE: activo + inactivo, things distintos."""
    actives   = [it for it in items if it['has_real_data'] or it['active']]
    inactives = [it for it in items if not it['has_real_data'] and not it['active']]

    if len(actives) == 1:
        winner = actives[0]
        for it in items:
            it['decision'] = 'KEEP'        if it is winner else 'MARK_LEGACY'
            it['reason']   = ('sensor activo con datos' if it is winner
                              else 'sensor inactivo/sustituido')
        return 'HIGH', f"KEEP activo {winner['id'][:30]}, MARK_LEGACY {len(inactives)} inactivos"

    if len(actives) > 1:
        # Multiples activos: ya deberia ser DUPLICATE_ACTIVE, pero por si acaso
        for it in items:
            it['decision'] = 'MANUAL_REVIEW'
            it['reason']   = 'multiples activos, no se decide automaticamente'
        return 'LOW', 'MANUAL_REVIEW — multiples activos'

    # Ninguno activo
    for it in items:
        it['decision'] = 'MANUAL_REVIEW'
        it['reason']   = 'ninguno activo, posible inventario historico'
    return 'LOW', 'MANUAL_REVIEW — ninguno activo'


def decide_duplicate_active(items):
    """DUPLICATE_ACTIVE: 2+ activos mismo HOS+sistema. No decidir."""
    for it in items:
        it['decision'] = 'MANUAL_REVIEW'
        it['reason']   = 'mas de un sensor activo en mismo HOS+sistema'
    return 'LOW', f"MANUAL_REVIEW — {len(items)} activos en mismo HOS+sistema"


def decide_duplicate_inactive(items):
    """DUPLICATE_INACTIVE: todos inactivos."""
    for it in items:
        it['decision'] = 'MANUAL_REVIEW'
        it['reason']   = 'todos inactivos, posible inventario historico'
    return 'LOW', 'MANUAL_REVIEW — todos inactivos'


DECISION_FN = {
    'SYNC_CONFLICT':      decide_sync_conflict,
    'REPLACE_CANDIDATE':  decide_replace_candidate,
    'DUPLICATE_ACTIVE':   decide_duplicate_active,
    'DUPLICATE_INACTIVE': decide_duplicate_inactive,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not AUDIT_JSON.exists():
        print(f"[ERROR] No encontrado: {AUDIT_JSON}")
        print("        Ejecuta primero: python scripts/audit_duplicate_sensors.py")
        return 1

    print("[PIELH] Cargando auditoria...")
    audit = json.loads(AUDIT_JSON.read_text(encoding='utf-8'))

    print("[PIELH] Cargando probe de recursos...")
    probe_index = load_probe_index(PROBE_JSON)
    print(f"        Things indexados en probe: {len(probe_index)}")

    incidents = audit.get('all_incidents', [])
    print(f"[PIELH] Incidencias a procesar: {len(incidents)}")
    print()

    groups_out = []
    csv_rows   = []

    n_keep   = n_legacy = n_manual = 0
    n_high   = n_medium = n_low = 0

    for inc in incidents:
        classification = inc['classification']
        risk_orig      = inc['risk']
        group_key      = inc['group_key']
        detection      = inc['detection']

        # Extraer HOS y system_id del grupo
        sensors_brief = inc.get('sensors', [])
        items = [enrich(sb, probe_index) for sb in sensors_brief]

        # HOS y system_id del grupo (del primero que lo tenga)
        hos_group = next((it['hos'] for it in items if it['hos']), '')
        sys_group = next((it['system_id'] for it in items if it['system_id']), '')

        # Aplicar regla segun clasificacion
        fn = DECISION_FN.get(classification)
        if fn:
            confidence, decision_summary = fn(items)
        else:
            for it in items:
                it['decision'] = 'MANUAL_REVIEW'
                it['reason']   = f"clasificacion desconocida: {classification}"
            confidence, decision_summary = 'LOW', 'MANUAL_REVIEW — clasificacion desconocida'

        # Contadores
        for it in items:
            d = it.get('decision', 'MANUAL_REVIEW')
            if d == 'KEEP':
                n_keep += 1
            elif d == 'MARK_LEGACY':
                n_legacy += 1
            else:
                n_manual += 1

        if confidence == 'HIGH':
            n_high += 1
        elif confidence == 'MEDIUM':
            n_medium += 1
        else:
            n_low += 1

        # Preparar items de salida (sin thing_token completo)
        items_out = []
        for it in items:
            items_out.append({
                'id':                  it['id'],
                'thing_id':            it['thing_id'],
                'thing_token_present': it['thing_token_present'],
                'hos':                 it['hos'],
                'system_id':           it['system_id'],
                'has_real_data':       it['has_real_data'],
                'active':              it['active'],
                'last_seen':           it['last_seen'],
                'days_since':          it['days_since'],
                'decision':            it.get('decision', 'MANUAL_REVIEW'),
                'reason':              it.get('reason', ''),
            })

            csv_rows.append({
                'group_id':            group_key,
                'classification':      classification,
                'risk':                risk_orig,
                'id':                  it['id'],
                'hos':                 it['hos'],
                'system_id':           it['system_id'],
                'thing_id':            it['thing_id'],
                'thing_token_present': it['thing_token_present'],
                'has_real_data':       it['has_real_data'],
                'last_seen':           it['last_seen'],
                'decision':            it.get('decision', 'MANUAL_REVIEW'),
                'confidence':          confidence,
                'reason':              it.get('reason', ''),
            })

        groups_out.append({
            'group_id':        group_key,
            'classification':  classification,
            'risk':            risk_orig,
            'detection':       detection,
            'hos':             hos_group,
            'system_id':       sys_group,
            'decision_summary': decision_summary,
            'confidence':      confidence,
            'geo_min_m':       inc.get('geo_min_m'),
            'name_sim_max':    inc.get('name_sim_max'),
            'items':           items_out,
        })

    # ── JSON ──────────────────────────────────────────────────────────────
    now = datetime.now().isoformat()
    result = {
        '_meta': {
            'created_at':    now,
            'source_audit':  str(AUDIT_JSON),
            'source_probe':  str(PROBE_JSON),
            'master_modified': False,
        },
        'summary': {
            'groups_total':           len(groups_out),
            'sensors_keep':           n_keep,
            'sensors_mark_legacy':    n_legacy,
            'sensors_manual_review':  n_manual,
            'high_confidence':        n_high,
            'medium_confidence':      n_medium,
            'low_confidence':         n_low,
        },
        'groups': groups_out,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS_DIR / 'duplicate_sensor_cleanup_plan.json'
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    # ── CSV ───────────────────────────────────────────────────────────────
    csv_path = REPORTS_DIR / 'duplicate_sensor_cleanup_plan.csv'
    fieldnames = [
        'group_id', 'classification', 'risk', 'id', 'hos', 'system_id',
        'thing_id', 'thing_token_present', 'has_real_data', 'last_seen',
        'decision', 'confidence', 'reason',
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(csv_rows)

    # ── MD ────────────────────────────────────────────────────────────────
    high_conf   = [g for g in groups_out if g['confidence'] == 'HIGH']
    manual_grps = [g for g in groups_out
                   if any(it['decision'] == 'MANUAL_REVIEW' for it in g['items'])]

    lines = [
        '# Plan de Limpieza de Sensores Duplicados (Dry-Run)',
        '',
        f'- Generado: {now}',
        f'- Auditoria base: `{AUDIT_JSON.name}`',
        f'- **master_modified: false** — solo lectura, ningun dato modificado',
        '',
        '## Resumen ejecutivo',
        '',
        '| Concepto | Valor |',
        '|---|---|',
        f'| Grupos analizados | {len(groups_out)} |',
        f'| Sensores propuestos KEEP | {n_keep} |',
        f'| Sensores propuestos MARK_LEGACY | {n_legacy} |',
        f'| Sensores enviados a MANUAL_REVIEW | {n_manual} |',
        f'| Decisiones HIGH confidence | {n_high} |',
        f'| Decisiones MEDIUM confidence | {n_medium} |',
        f'| Decisiones LOW confidence | {n_low} |',
        '',
        '## Conteos por clasificacion',
        '',
        '| Clasificacion | Grupos | Sensores KEEP | MARK_LEGACY | MANUAL_REVIEW |',
        '|---|---|---|---|---|',
    ]
    by_class_counts = {}
    for g in groups_out:
        cl = g['classification']
        bc = by_class_counts.setdefault(cl, {'groups': 0, 'keep': 0, 'legacy': 0, 'manual': 0})
        bc['groups'] += 1
        for it in g['items']:
            d = it['decision']
            if d == 'KEEP':
                bc['keep'] += 1
            elif d == 'MARK_LEGACY':
                bc['legacy'] += 1
            else:
                bc['manual'] += 1

    for cl, bc in sorted(by_class_counts.items()):
        lines.append(f"| {cl} | {bc['groups']} | {bc['keep']} | {bc['legacy']} | {bc['manual']} |")

    lines += [
        '',
        f'## Casos HIGH confidence con decision automatica (max 20)',
        '',
        '| Grupo | Clase | HOS | Sistema | Decision |',
        '|---|---|---|---|---|',
    ]
    for g in high_conf[:20]:
        lines.append(
            f"| `{g['group_id']}` | {g['classification']} | "
            f"{g['hos']} | {g['system_id']} | {g['decision_summary']} |"
        )

    lines += [
        '',
        '### Detalle ejemplos HIGH confidence (5 primeros)',
        '',
    ]
    for g in high_conf[:5]:
        lines.append(f"**`{g['group_id']}`** — {g['classification']} — {g['confidence']}")
        lines.append(f"_{g['decision_summary']}_")
        lines.append('')
        lines.append('| id | thing_id | has_data | last_seen | decision | razon |')
        lines.append('|---|---|---|---|---|---|')
        for it in g['items']:
            tid_s = (it['thing_id'] or '')[:28]
            lines.append(
                f"| {it['id']} | {tid_s} | {'SI' if it['has_real_data'] else 'NO'} "
                f"| {it['last_seen'][:10] if it['last_seen'] else '—'} "
                f"| **{it['decision']}** | {it['reason']} |"
            )
        lines.append('')

    lines += [
        f'## Casos MANUAL_REVIEW (max 10 ejemplos)',
        '',
        '| Grupo | Clase | HOS | Sistema | Sensores | Razon |',
        '|---|---|---|---|---|---|',
    ]
    for g in manual_grps[:10]:
        reason = g['items'][0].get('reason', '') if g['items'] else ''
        lines.append(
            f"| `{g['group_id']}` | {g['classification']} | "
            f"{g['hos']} | {g['system_id']} | {len(g['items'])} | {reason} |"
        )

    lines += [
        '',
        '## Advertencias',
        '',
        f'- {by_class_counts.get("SYNC_CONFLICT", {}).get("groups", 0)} grupos SYNC_CONFLICT: '
        'mismo ID visible asignado a things distintos. Riesgo de escritura contra thing incorrecto en sync.',
        f'- {by_class_counts.get("DUPLICATE_ACTIVE", {}).get("groups", 0)} grupos DUPLICATE_ACTIVE: '
        'dos o mas sensores activos para mismo HOS+sistema. Revisar manualmente cual es el dispositivo real.',
        '- Los sensores MARK_LEGACY propuestos NO han sido modificados. Este es un plan dry-run.',
        '',
        '## Siguiente paso recomendado',
        '',
        '1. Revisar los `MANUAL_REVIEW` manualmente usando el CSV generado.',
        '2. Para los HIGH confidence, ejecutar `scripts/mark_old_duplicate_sensors.py` '
        '   tras verificacion visual de una muestra.',
        '3. Para DUPLICATE_ACTIVE, identificar el thing_id correcto en TheThings antes de actuar.',
        '',
        '---',
        f'JSON: `reports/duplicate_sensor_cleanup_plan.json`',
        f'CSV:  `reports/duplicate_sensor_cleanup_plan.csv`',
    ]

    md_path = REPORTS_DIR / 'duplicate_sensor_cleanup_plan.md'
    md_path.write_text('\n'.join(lines), encoding='utf-8')

    # ── Consola ───────────────────────────────────────────────────────────
    print(f'[PIELH] Plan generado: {now}')
    print(f'        Grupos analizados       : {len(groups_out)}')
    print(f'        Sensores KEEP           : {n_keep}')
    print(f'        Sensores MARK_LEGACY    : {n_legacy}')
    print(f'        Sensores MANUAL_REVIEW  : {n_manual}')
    print(f'        HIGH confidence         : {n_high}')
    print(f'        MEDIUM confidence       : {n_medium}')
    print(f'        LOW confidence          : {n_low}')
    print()
    print('        Por clasificacion:')
    for cl, bc in sorted(by_class_counts.items()):
        print(f"          {cl:25} grupos={bc['groups']:3}  KEEP={bc['keep']:3}  "
              f"LEGACY={bc['legacy']:3}  MANUAL={bc['manual']:3}")
    print()
    print(f'[OK] {json_path}')
    print(f'[OK] {csv_path}')
    print(f'[OK] {md_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
