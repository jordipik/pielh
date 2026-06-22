#!/usr/bin/env python3
"""PIELH QA — servidor con guardado, health check y logging."""

import copy
import csv
import http.server
import json
import logging
import shutil
import ssl
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent

import sys as _sys
_scripts_dir = str(ROOT / 'scripts')
if _scripts_dir not in _sys.path:
    _sys.path.insert(0, _scripts_dir)
try:
    from audit_thethings_activity import run_audit as _run_audit_fn
    from build_inventory_health_report import run_build_report as _run_report_fn
    _HAS_AUDIT_MODULES = True
except ImportError:
    _HAS_AUDIT_MODULES = False

# Fields that are never propagated/completed across sensors that share the same id
# (each duplicate is treated as the same logical sensor, but ID/token belong to a
# specific physical device/registration).
OWN_FIELDS = {'thing_id', 'thing_token'}
EMPTY_VALUES = (None, '', [])

# Building fields that propagate to all sensors of that building (same hos)
# when edited. Conflicts overwrite, like sibling propagation.
BUILDING_TO_SENSOR_FIELDS = {
    'district_code', 'district_name',
    'neighborhood_key', 'neighborhood',
    'type', 'zone', 'street_etra', 'street_mti',
    'lat', 'lon',
}

# Fields that can be pushed back to TheThings API
SYNC_ALLOWED_FIELDS = {
    'lat', 'lon',
    'district_code', 'district_name',
    'neighborhood_key', 'neighborhood',
    'street_etra',
    'type', 'zone',
    'has_data', 'status', 'qa_notes',
}

# ── Config ────────────────────────────────────────────────────────────
_DEFAULTS = {
    "json_file":   "pielh_qa_master.json",
    "backup_dir":  "data/backups",
    "log_file":    "logs/pielh.log",
    "max_backups": 20,
    "host":        "127.0.0.1",
    "port":        8080,
}

def _load_config():
    cfg_path = ROOT / 'config.json'
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
            return {**_DEFAULTS, **cfg}
        except Exception:
            pass
    return dict(_DEFAULTS)

CFG         = _load_config()
DATA_FILE   = ROOT / CFG['json_file']
BACKUP_DIR  = ROOT / CFG['backup_dir']
LOG_FILE    = ROOT / CFG['log_file']
MAX_BACKUPS = int(CFG['max_backups'])
HOST        = CFG['host']
PORT        = int(CFG['port'])
THETHINGS_API   = CFG.get('thethings_api',   'https://api.smartpielh.l-h.cat')
THETHINGS_TOKEN = CFG.get('thethings_token', '')

# model_id → {type, system_id, system_name, label}
# type 'building' → ASSETS; type 'sensor' → sensor systems
MODELS = [
    {'id': 34738, 'label': 'ASSETS',                       'type': 'building'},
    {'id': 33814, 'label': 'S01 - Ruido',                  'type': 'sensor', 'system_id': 'S01',  'system_name': 'RUIDO'},
    {'id': 34132, 'label': 'S02 - Contaminantes',          'type': 'sensor', 'system_id': 'S02',  'system_name': 'CONTAMINACIÓN EXTERIOR'},
    {'id': 34923, 'label': 'S03 - Gas Radón',              'type': 'sensor', 'system_id': 'S03',  'system_name': 'GAS RADON'},
    {'id': 34164, 'label': 'S04 - Calidad Aire Interior',  'type': 'sensor', 'system_id': 'S04',  'system_name': 'AMBIENTE INTERIOR'},
    {'id': 34563, 'label': 'S05 - Energía Circutor',       'type': 'sensor', 'system_id': 'S05',  'system_name': 'ELECTRICIDAD'},
    {'id': 34149, 'label': 'S06 - Contador Agua',          'type': 'sensor', 'system_id': 'S06',  'system_name': 'AGUA'},
    {'id': 34148, 'label': 'S07 - Contador Gas',           'type': 'sensor', 'system_id': 'S07',  'system_name': 'GAS'},
    {'id': 34565, 'label': 'S08 - Calderas',               'type': 'sensor', 'system_id': 'S08',  'system_name': 'CALDERAS'},
    {'id': 34924, 'label': 'S09 - Climatización',          'type': 'sensor', 'system_id': 'S09',  'system_name': 'CLIMATIZACIÓN'},
    {'id': 34927, 'label': 'S13A - Sostenibilidad',        'type': 'sensor', 'system_id': 'S13A', 'system_name': 'SOSTENIBILIDAD EDIFICIOS'},
    {'id': 34682, 'label': 'S14A - Meteorología',          'type': 'sensor', 'system_id': 'S14A', 'system_name': 'METEO'},
    {'id': 36935, 'label': 'S14B - Sensor Pira',           'type': 'sensor', 'system_id': 'S14B', 'system_name': 'METEO SENSOR'},
    {'id': 34928, 'label': 'S15 - Presencia',              'type': 'sensor', 'system_id': 'S15',  'system_name': 'PRESENCIA'},
    {'id': 34116, 'label': 'S17 - Aforos',                 'type': 'sensor', 'system_id': 'S17',  'system_name': 'AFORO'},
    {'id': 34930, 'label': 'S19 - Fuga Gas',               'type': 'sensor', 'system_id': 'S19',  'system_name': 'GAS'},
    {'id': 34931, 'label': 'S20 - Inundación',             'type': 'sensor', 'system_id': 'S20',  'system_name': 'INUNDACION'},
    {'id': 34932, 'label': 'S21 - Det. Humos',             'type': 'sensor', 'system_id': 'S21',  'system_name': 'DETECCION HUMOS'},
    {'id': 36331, 'label': 'S22 - Transporte Público',     'type': 'sensor', 'system_id': 'S22',  'system_name': 'TRANSPORTE PUBLICO'},
    {'id': 34235, 'label': 'S23 - Parking',                'type': 'sensor', 'system_id': 'S23',  'system_name': 'PARKING'},
    {'id': 34933, 'label': 'S24 - Tráfico',                'type': 'sensor', 'system_id': 'S24',  'system_name': 'TRAFICO'},
    {'id': 34099, 'label': 'SIP - NodoIoT',                'type': 'sensor', 'system_id': 'SIP',  'system_name': 'IPS'},
]

_import_lock  = threading.Lock()
_import_state = {
    'running': False, 'done': False, 'error': None,
    'phase': '',       # importing | resolving_tags | updating_inventory | done | error
    'sub_status': '',  # detalle dentro de la fase actual
    'models_total': len(MODELS), 'models_done': 0,
    'things_done': 0, 'current_model': '',
    'buildings': 0, 'sensors': 0,
    'tags_stats': None,        # stats de resolve_tags
    'inventory_stats': None,   # stats de iot_health
    'inventory_health_skipped': None,
    'warnings': [],
    'tags_resolved_at': None, 'inventory_health_updated_at': None,
    'sync_pipeline_version': 'import_tags_inventory_v1',
    'started_at': None, 'finished_at': None,
}

_resolve_lock  = threading.Lock()
_resolve_state = {
    'running': False, 'done': False, 'error': None,
    'total': 0, 'done_count': 0,
    'buildings_updated': 0, 'sensors_updated': 0,
    'no_tags': 0, 'skipped': 0,
    'fields_count': {}, 'tags_unknown': [],
    'sensors_no_building': 0,
    'log': [],
    'started_at': None, 'finished_at': None,
}

_system_sync_lock  = threading.Lock()
_system_sync_state = {
    'running': False, 'done': False, 'error': None,
    'systems': [],
    'current_system': '', 'current_idx': 0, 'total': 0,
    'things_done': 0,
    'started_at': None, 'finished_at': None,
}
_last_system_sync = {}  # system_id → {at, sensors, ok, error?}

# ── File logger ───────────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
_log = logging.getLogger('pielh')
_log.setLevel(logging.INFO)
_fh = logging.FileHandler(str(LOG_FILE), encoding='utf-8')
_fh.setFormatter(logging.Formatter('%(message)s'))
_log.addHandler(_fh)


def _log_change(entity_type, record_id, field, old_val, new_val):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _log.info(f"{ts} | {entity_type} | {record_id} | {field} | {old_val} -> {new_val}")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == '/api/health':
            self._handle_health()
        elif self.path == '/api/import-status':
            self._handle_import_status()
        elif self.path == '/api/resolve-status':
            self._handle_resolve_status()
        elif self.path == '/api/sync-pending':
            self._handle_sync_pending()
        elif self.path == '/api/sync-status':
            self._handle_sync_status()
        elif self.path == '/api/systems-status':
            self._handle_systems_status()
        elif self.path == '/api/system-sync-status':
            self._handle_system_sync_status()
        elif self.path == '/api/models':
            self._handle_models()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/save-record':
            self._handle_save_single()
        elif self.path == '/api/save-batch':
            self._handle_save_batch()
        elif self.path == '/api/import':
            self._handle_import()
        elif self.path == '/api/resolve-tags':
            self._handle_resolve_tags()
        elif self.path == '/api/sync-record':
            self._handle_sync_record()
        elif self.path == '/api/sync-all':
            self._handle_sync_all()
        elif self.path == '/api/import-system':
            self._handle_import_system()
        elif self.path == '/api/import-selected':
            self._handle_import_selected()
        else:
            self.send_error(404)

    # ── Health ────────────────────────────────────────────────────────

    def _handle_health(self):
        result = {'status': 'ok'}
        issues = []

        if DATA_FILE.exists():
            result['json_file'] = 'ok'
        else:
            result['json_file'] = 'error: not found'
            issues.append('json_file')

        if BACKUP_DIR.exists():
            result['backup_dir'] = 'ok'
        else:
            result['backup_dir'] = 'warning: not created yet'

        try:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            result['log_file'] = 'ok'
        except Exception as e:
            result['log_file'] = f'error: {e}'
            issues.append('log_file')

        if issues:
            result['status'] = 'error'

        self._ok(result)

    # ── Single record ─────────────────────────────────────────────────

    def _handle_save_single(self):
        try:
            body        = self._read_json()
            entity_type = body.get('entityType', '')
            record_id   = body.get('id', '')
            selector    = body.get('selector', {})
            updates     = body.get('updates', {})

            if entity_type not in ('sensor', 'building'):
                return self._err(400, 'entityType must be sensor or building')
            if not record_id:
                return self._err(400, 'id is required')
            if not isinstance(updates, dict) or not updates:
                return self._err(400, 'updates must be a non-empty dict')

            master = self._load()
            err = self._validate(updates, master)
            if err:
                return self._err(400, err)

            siblings = self._siblings(master, entity_type, record_id)
            if not siblings:
                return self._err(404, f"{entity_type} '{record_id}' no encontrado")

            selector = selector if isinstance(selector, dict) else {}
            target = siblings[0]
            if selector.get('thing_id'):
                target = next((r for r in siblings if r.get('thing_id') == selector['thing_id']), siblings[0])

            updates = self._expand_updates(updates, master)
            shared_updates = {k: v for k, v in updates.items() if k not in OWN_FIELDS}
            own_updates    = {k: v for k, v in updates.items() if k in OWN_FIELDS}

            before = {id(r): copy.deepcopy(r) for r in siblings}
            self._backup()
            for r in siblings:
                self._apply_updates(r, shared_updates)
            if own_updates:
                self._apply_updates(target, own_updates)
            self._complete_empty_fields(siblings)

            sensors_updated = 0
            if entity_type == 'building':
                sensors_updated = self._propagate_to_sensors(master, record_id, shared_updates)

            self._mark_sync_pending(siblings, list(updates.keys()))
            if entity_type == 'building' and sensors_updated > 0:
                affected_sns = [s for s in master.get('sensors', []) if s.get('hos') == record_id]
                propagated   = [k for k in shared_updates if k in BUILDING_TO_SENSOR_FIELDS]
                self._mark_sync_pending(affected_sns, propagated)

            self._save(master)

            for r in siblings:
                old = before[id(r)]
                for field, new_val in r.items():
                    if field == 'raw':
                        continue
                    if old.get(field) != new_val:
                        _log_change(entity_type, r.get('id'), field, old.get(field), new_val)

            self._ok({'ok': True, 'id': record_id, 'updates': updates, 'records': siblings,
                      'sensors_updated': sensors_updated})

        except Exception as e:
            self._err(500, str(e))

    # ── Batch ─────────────────────────────────────────────────────────

    def _handle_save_batch(self):
        try:
            body        = self._read_json()
            entity_type = body.get('entityType', '')
            targets_raw = body.get('targets')      # new: [{id, selector}]
            ids_raw     = body.get('ids', [])      # legacy: [id, ...]
            updates     = body.get('updates', {})

            if entity_type not in ('sensor', 'building'):
                return self._err(400, 'entityType must be sensor or building')
            if not isinstance(updates, dict) or not updates:
                return self._err(400, 'updates must be a non-empty dict')

            # Normalize to targets list
            if targets_raw is not None:
                if not isinstance(targets_raw, list) or not targets_raw:
                    return self._err(400, 'targets must be a non-empty list')
                targets = targets_raw
            else:
                if not ids_raw or not isinstance(ids_raw, list):
                    return self._err(400, 'ids must be a non-empty list')
                targets = [{'id': rid, 'selector': None} for rid in ids_raw]

            master = self._load()
            err = self._validate(updates, master)
            if err:
                return self._err(400, err)
            updates = self._expand_updates(updates, master)
            shared_updates = {k: v for k, v in updates.items() if k not in OWN_FIELDS}

            # Validate all targets exist before any write
            not_found = []
            for t in targets:
                tid      = t.get('id', '')
                selector = t.get('selector') or {}
                thing_id = selector.get('thing_id') if isinstance(selector, dict) else None
                siblings = self._siblings(master, entity_type, tid)
                if not siblings:
                    not_found.append(tid)
                elif thing_id:
                    if not any(r.get('thing_id') == thing_id for r in siblings):
                        not_found.append(f"{tid}/{thing_id}")
            if not_found:
                return self._err(404, f"No encontrados: {', '.join(not_found)}")

            self._backup()
            total_records   = 0
            sensors_updated = 0
            seen = set()  # object ids of already-processed records

            for t in targets:
                tid      = t.get('id', '')
                selector = t.get('selector') or {}
                thing_id = selector.get('thing_id') if isinstance(selector, dict) else None
                siblings = self._siblings(master, entity_type, tid)

                if thing_id:
                    # Targeted: apply only to the record matching thing_id
                    specific = next((r for r in siblings if r.get('thing_id') == thing_id), None)
                    if not specific or id(specific) in seen:
                        continue
                    seen.add(id(specific))
                    records_to_update = [specific]
                else:
                    # Legacy/fallback: apply to all siblings not yet processed
                    records_to_update = [r for r in siblings if id(r) not in seen]
                    for r in records_to_update:
                        seen.add(id(r))

                before = {id(r): copy.deepcopy(r) for r in records_to_update}
                for r in records_to_update:
                    self._apply_updates(r, shared_updates)
                # _complete_empty_fields only makes sense when editing all siblings together;
                # skip it when targeting a specific thing_id to avoid cross-contamination.
                if not thing_id:
                    self._complete_empty_fields(records_to_update)

                if entity_type == 'building':
                    sensors_updated += self._propagate_to_sensors(master, tid, shared_updates)
                self._mark_sync_pending(records_to_update, list(shared_updates.keys()))
                if entity_type == 'building':
                    affected_sns = [s for s in master.get('sensors', []) if s.get('hos') == tid]
                    propagated   = [k for k in shared_updates if k in BUILDING_TO_SENSOR_FIELDS]
                    self._mark_sync_pending(affected_sns, propagated)

                for r in records_to_update:
                    old = before[id(r)]
                    for field, new_val in r.items():
                        if field == 'raw':
                            continue
                        if old.get(field) != new_val:
                            _log_change(entity_type, r.get('id'), field, old.get(field), new_val)
                total_records += len(records_to_update)

            self._save(master)
            self._ok({'ok': True, 'count': len(targets), 'records_updated': total_records,
                      'updates': shared_updates, 'sensors_updated': sensors_updated})

        except Exception as e:
            self._err(500, str(e))

    # ── Import ────────────────────────────────────────────────

    def _handle_import_status(self):
        with _import_lock:
            self._ok(dict(_import_state))

    def _handle_import(self):
        try:
            with _import_lock:
                already = _import_state['running']
                if not already:
                    _import_state.update({
                        'running': True, 'done': False, 'error': None,
                        'phase': '', 'sub_status': '',
                        'models_done': 0, 'things_done': 0,
                        'buildings': 0, 'sensors': 0,
                        'current_model': '',
                        'tags_stats': None, 'inventory_stats': None,
                        'inventory_health_skipped': None,
                        'warnings': [],
                        'tags_resolved_at': None, 'inventory_health_updated_at': None,
                        'started_at': datetime.now().isoformat(),
                        'finished_at': None,
                    })
            self._ok({'ok': True, 'message': 'already running' if already else 'started'})
            if not already:
                threading.Thread(target=self._run_import, daemon=True).start()
        except Exception as e:
            self._err(500, str(e))

    def _run_import(self):
        try:
            # ── Backup preventivo ─────────────────────────────────────
            self._backup()
            _log.info('import: inicio sincronización completa (pipeline import_tags_inventory_v1)')

            # ── Fase 1: importing ─────────────────────────────────────
            with _import_lock:
                _import_state['phase'] = 'importing'

            master = self._load()
            master['buildings'] = []
            master['sensors']   = []

            for m in MODELS:
                with _import_lock:
                    if not _import_state['running']:
                        break
                    _import_state['current_model'] = m['label']

                try:
                    things = self._fetch_model_things(m['id'])
                except Exception as exc:
                    _log.warning(f"import: modelo {m['id']} fallido — {exc}")
                    things = []

                if isinstance(things, list):
                    for thing in things:
                        if m['type'] == 'building':
                            master['buildings'].append(self._thing_to_building(thing))
                        else:
                            master['sensors'].append(self._thing_to_sensor(thing, m))
                        with _import_lock:
                            _import_state['things_done'] += 1

                self._save(master)
                with _import_lock:
                    _import_state['models_done'] += 1
                    _import_state['buildings'] = len(master['buildings'])
                    _import_state['sensors']   = len(master['sensors'])

                time.sleep(0.3)

            # ── Fase 2: resolving_tags ────────────────────────────────
            with _import_lock:
                _import_state['phase'] = 'resolving_tags'

            _log.info('import: resolviendo tags…')
            resolve_stats = self._resolve_tags_in_master(master)
            _log.info(
                f"import: tags — {resolve_stats['buildings_updated']} edif., "
                f"{resolve_stats['sensors_updated']} sens."
            )
            with _import_lock:
                _import_state['tags_stats'] = {
                    'buildings_updated': resolve_stats['buildings_updated'],
                    'sensors_updated':   resolve_stats['sensors_updated'],
                    'no_tags':           resolve_stats['no_tags'],
                    'skipped':           resolve_stats['skipped'],
                    'tags_unknown':      resolve_stats['tags_unknown'][:10],
                }

            # ── Fase 3: updating_inventory ────────────────────────────
            with _import_lock:
                _import_state['phase']      = 'updating_inventory'
                _import_state['sub_status'] = 'Iniciando auditoría IoT…'

            inv_stats = self._apply_inventory_health_full(master)
            inv_skipped = bool(inv_stats.get('skipped'))
            if inv_skipped:
                _log.info(f"import: inventario omitido — {inv_stats.get('reason')}")
            else:
                _log.info(
                    f"import: inventario — {inv_stats.get('sensors_audited')} auditados, "
                    f"{inv_stats.get('matched')} matched, "
                    f"{inv_stats.get('buildings_updated')} edif."
                )
            with _import_lock:
                _import_state['inventory_stats']          = inv_stats
                _import_state['inventory_health_skipped'] = inv_skipped

            # ── Validación final ──────────────────────────────────────
            validation = self._validate_iot_health(master)
            with _import_lock:
                _import_state['warnings'] = validation['warnings']

            # ── Guardar y finalizar ───────────────────────────────────
            finished = datetime.now().isoformat()
            master['_meta'] = {
                'last_sync':                     finished,
                'buildings':                     len(master['buildings']),
                'sensors':                       len(master['sensors']),
                'tags_resolved_at':              finished,
                'inventory_health_updated_at':   finished if not inv_skipped else None,
                'inventory_health_skipped':      inv_skipped,
                'inventory_health_error':        inv_stats.get('reason') if inv_skipped else None,
                'sync_pipeline_version':         'import_tags_inventory_v1',
                'validation':                    validation,
            }
            self._save(master)

            with _import_lock:
                _import_state['running']                     = False
                _import_state['done']                        = True
                _import_state['phase']                       = 'done'
                _import_state['sub_status']                  = ''
                _import_state['finished_at']                 = finished
                _import_state['tags_resolved_at']            = finished
                _import_state['inventory_health_updated_at'] = finished if not inv_skipped else None

            _log.info(
                f"import done: {_import_state['buildings']} edif., "
                f"{_import_state['sensors']} sens. "
                f"warnings={validation['warnings']}"
            )

        except Exception as exc:
            with _import_lock:
                _import_state['running']    = False
                _import_state['error']      = str(exc)
                _import_state['phase']      = 'error'
                _import_state['sub_status'] = ''
            _log.error(f"import failed: {exc}")

    # ── Resolve Tags ──────────────────────────────────────────────

    def _handle_resolve_status(self):
        with _resolve_lock:
            self._ok(dict(_resolve_state))

    def _handle_resolve_tags(self):
        try:
            with _import_lock:
                if _import_state.get('running'):
                    return self._err(409, 'Import en curso — espera a que termine antes de resolver tags')
            with _resolve_lock:
                already = _resolve_state['running']
                if not already:
                    _resolve_state.update({
                        'running': True, 'done': False, 'error': None,
                        'total': 0, 'done_count': 0,
                        'buildings_updated': 0, 'sensors_updated': 0,
                        'no_tags': 0, 'skipped': 0,
                        'fields_count': {}, 'tags_unknown': [],
                        'sensors_no_building': 0,
                        'log': [],
                        'started_at': datetime.now().isoformat(),
                        'finished_at': None,
                    })
            self._ok({'ok': True, 'message': 'already running' if already else 'started'})
            if not already:
                threading.Thread(target=self._run_resolve_tags, daemon=True).start()
        except Exception as e:
            self._err(500, str(e))

    def _run_resolve_tags(self):
        def log(msg):
            with _resolve_lock:
                _resolve_state['log'].append(msg)

        try:
            master    = self._load()
            buildings = master.get('buildings', [])

            with _resolve_lock:
                _resolve_state['total'] = len(buildings)
            log(f'Cargados {len(buildings)} edificios')

            def on_progress(done, total, stats):
                with _resolve_lock:
                    _resolve_state['done_count']       = done
                    _resolve_state['buildings_updated'] = stats['buildings_updated']
                    _resolve_state['sensors_updated']   = stats['sensors_updated']
                    _resolve_state['no_tags']           = stats['no_tags']
                    _resolve_state['skipped']           = stats['skipped']
                    _resolve_state['fields_count']      = stats['fields_count']
                    _resolve_state['tags_unknown']      = stats['tags_unknown']
                    if stats.get('last_log'):
                        _resolve_state['log'].append(stats['last_log'])

            stats = self._resolve_tags_in_master(master, on_progress=on_progress)

            self._save(master)
            finished = datetime.now().isoformat()
            log(
                f'✓ Completado: {stats["buildings_updated"]} resueltos · '
                f'{stats["skipped"]} sin coincidencia · {stats["no_tags"]} sin tags · '
                f'{stats["sensors_updated"]} sensores'
            )

            with _resolve_lock:
                _resolve_state['sensors_no_building'] = stats['sensors_no_building']
                _resolve_state['running']             = False
                _resolve_state['done']                = True
                _resolve_state['finished_at']         = finished

        except Exception as exc:
            with _resolve_lock:
                _resolve_state['running'] = False
                _resolve_state['error']   = str(exc)
                _resolve_state['log'].append(f'Error: {exc}')
            _log.error(f'resolve-tags failed: {exc}')

    def _validate_iot_health(self, master):
        """Comprueba integridad del inventario IoT en master. No modifica nada."""
        sensors   = master.get('sensors', [])
        buildings = master.get('buildings', [])
        total_sensors   = len(sensors)
        total_buildings = len(buildings)

        sensors_with_iot       = sum(1 for s in sensors if 'iot_health' in s)
        buildings_with_counts  = sum(1 for b in buildings if 'iot_total_sensors' in b)
        buildings_missing      = total_buildings - buildings_with_counts
        missing_token          = sum(1 for s in sensors if not s.get('thing_token'))
        no_hos                 = sum(1 for s in sensors if not s.get('hos'))

        warnings = []
        if sensors_with_iot < total_sensors:
            warnings.append(
                f'{total_sensors - sensors_with_iot}/{total_sensors} sensores sin iot_health'
            )
        if buildings_missing > 0:
            warnings.append(
                f'{buildings_missing}/{total_buildings} edificios sin contadores IoT'
            )
        if missing_token > 0:
            warnings.append(f'{missing_token} sensores sin thing_token')
        if no_hos > 0:
            warnings.append(f'{no_hos} sensores sin HOS asignado')

        return {
            'total_sensors':              total_sensors,
            'sensors_with_iot_health':    sensors_with_iot,
            'buildings_with_iot_counts':  buildings_with_counts,
            'buildings_missing_iot_counts': buildings_missing,
            'total_buildings':            total_buildings,
            'warnings':                   warnings,
        }

    def _resolve_tags_in_master(self, master, on_progress=None):
        """Resuelve tags de todos los edificios en master (in-place). Devuelve stats."""
        cats      = master.get('catalogs', {})
        buildings = master.get('buildings', [])
        sensors   = master.get('sensors', [])

        district_map = {d['code'].upper(): d for d in cats.get('districts', [])}
        neighborhood_map = {}
        for nb in cats.get('neighborhoods', []):
            key_norm = nb['key'].upper().replace(' ', '_')
            neighborhood_map[key_norm] = nb

        building_ids = {b['id'] for b in buildings}
        sns_no_bld   = sum(1 for s in sensors if s.get('hos', '') and s['hos'] not in building_ids)

        bld_updated = sns_updated = no_tags_cnt = skipped_cnt = 0
        fields_count = {'district_code': 0, 'neighborhood_key': 0, 'type': 0, 'zone': 0, 'street_etra': 0}
        unknown_tags = set()
        log_entries  = []

        for i, b in enumerate(buildings):
            tags_str = b.get('tags', '')
            if not tags_str:
                no_tags_cnt += 1
            else:
                tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                fields, unknowns = self._resolve_tags_to_fields(tags_list, district_map, neighborhood_map)
                unknown_tags.update(unknowns)
                if fields:
                    for fk in fields_count:
                        if fk in fields:
                            fields_count[fk] += 1
                    self._apply_updates(b, fields)
                    n = self._propagate_to_sensors(master, b['id'], fields)
                    bld_updated += 1
                    sns_updated += n
                    msg = f'{b["id"]}: ' + ', '.join(f'{k}={v}' for k, v in list(fields.items())[:3])
                    log_entries.append(msg)
                else:
                    skipped_cnt += 1

            if on_progress:
                on_progress(i + 1, len(buildings), {
                    'buildings_updated': bld_updated,
                    'sensors_updated':   sns_updated,
                    'no_tags':           no_tags_cnt,
                    'skipped':           skipped_cnt,
                    'fields_count':      dict(fields_count),
                    'tags_unknown':      sorted(unknown_tags)[:50],
                    'last_log':          log_entries[-1] if log_entries else None,
                })

        return {
            'buildings_updated': bld_updated,
            'sensors_updated':   sns_updated,
            'no_tags':           no_tags_cnt,
            'skipped':           skipped_cnt,
            'fields_count':      dict(fields_count),
            'tags_unknown':      sorted(unknown_tags)[:50],
            'sensors_no_building': sns_no_bld,
            'log':               log_entries,
        }

    _DEMO_READY_STATUSES = {'ACTIVE_24H', 'ACTIVE_7D'}

    def _apply_iot_health_to_master(self, master, audit_by_token, sys_class, health_source):
        """Core in-memory: aplica iot_health a sensores y contadores IoT a edificios (in-place).
        audit_by_token: dict {thing_token → row_dict} con campos del audit.
        sys_class:      dict {system_id → class_letter}.
        Devuelve stats dict."""
        sensors   = master.get('sensors', [])
        buildings = master.get('buildings', [])
        matched   = unmatched = 0

        for s in sensors:
            tt  = s.get('thing_token', '')
            row = audit_by_token.get(tt)
            if row:
                status   = (row.get('active_status') or 'NO_DATA')
                if isinstance(status, str):
                    status = status.strip() or 'NO_DATA'
                has_real_raw = row.get('has_real_value')
                if isinstance(has_real_raw, bool):
                    has_real = has_real_raw
                else:
                    has_real = str(has_real_raw or '').strip().lower() in ('true', '1', 'yes')
                demo_ready = status in self._DEMO_READY_STATUSES
                last_seen  = row.get('last_timestamp') or None
                if isinstance(last_seen, str):
                    last_seen = last_seen.strip() or None
                resource   = row.get('resource_detected') or None
                if isinstance(resource, str):
                    resource = resource.strip() or None
                sys_id = (row.get('system_id') or '')
                if isinstance(sys_id, str):
                    sys_id = sys_id.strip()
                s_class = sys_class.get(sys_id, '?')
                s['iot_health'] = {
                    'status':        status,
                    'has_real_data': has_real,
                    'demo_ready':    demo_ready,
                    'last_seen':     last_seen,
                    'resource':      resource,
                    'system_class':  s_class,
                    'health_source': health_source,
                }
                matched += 1
            else:
                s['iot_health'] = {
                    'status':        'NOT_AUDITED',
                    'has_real_data': False,
                    'demo_ready':    False,
                    'last_seen':     None,
                    'resource':      None,
                    'system_class':  sys_class.get(s.get('system_id', ''), '?'),
                    'health_source': health_source,
                }
                unmatched += 1

        sensors_by_hos: dict = {}
        for s in sensors:
            hos = s.get('hos', '')
            if hos:
                sensors_by_hos.setdefault(hos, []).append(s)

        bld_updated = bld_active = 0
        for b in buildings:
            bld_sensors = sensors_by_hos.get(b.get('id', ''), [])
            total  = len(bld_sensors)
            active = sum(1 for s in bld_sensors if s.get('iot_health', {}).get('demo_ready', False))

            if total == 0:
                iot_status = 'NO_SENSORS'
            elif active > 0:
                iot_status = 'ACTIVE'
            else:
                iot_status = 'NO_DATA'

            b['iot_total_sensors']  = total
            b['iot_active_sensors'] = active
            b['iot_demo_ready']     = active
            b['iot_health_status']  = iot_status
            bld_updated += 1
            if iot_status == 'ACTIVE':
                bld_active += 1

        return {
            'skipped':           False,
            'matched':           matched,
            'unmatched':         unmatched,
            'buildings_updated': bld_updated,
            'buildings_active':  bld_active,
            'health_source':     health_source,
        }

    def _apply_inventory_health(self, master):
        """Fallback file-based: carga CSV + report de data/audits/ y aplica al master.
        Solo funciona si existen archivos previos de auditoría."""
        audit_dir = ROOT / 'data' / 'audits'

        csvs = sorted(audit_dir.glob('thethings_activity_[0-9]*.csv'), reverse=True)
        if not csvs:
            return {'skipped': True, 'reason': 'no audit CSV in data/audits/'}

        report_path = audit_dir / 'inventory_health_report.json'
        if not report_path.exists():
            return {'skipped': True, 'reason': 'inventory_health_report.json not found'}

        csv_path = csvs[0]
        audit_by_token = {}
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                tt = row.get('thing_token', '').strip()
                if tt:
                    audit_by_token[tt] = row

        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        sys_class = {
            sid: info.get('class', '?')
            for sid, info in report.get('systems_detail', {}).items()
        }

        return self._apply_iot_health_to_master(master, audit_by_token, sys_class, csv_path.name)

    def _apply_inventory_health_full(self, master):
        """Pipeline completo: llama a TheThings API → CSV/report en data/audits/ → aplica al master.
        Requiere thethings_token en config.json.
        En caso de error devuelve {'skipped': True, 'reason': ...} sin romper el import."""
        if not _HAS_AUDIT_MODULES:
            return {'skipped': True, 'reason': 'módulos de auditoría no disponibles (ImportError)'}
        if not THETHINGS_TOKEN:
            return {'skipped': True, 'reason': 'thethings_token no configurado'}

        audit_dir = ROOT / 'data' / 'audits'
        audit_dir.mkdir(parents=True, exist_ok=True)

        sensors_total = len(master.get('sensors', []))

        def _progress(done, total, _result):
            with _import_lock:
                _import_state['sub_status'] = f'Auditando sensor {done}/{total}…'

        try:
            with _import_lock:
                _import_state['sub_status'] = 'Auditando actividad real de sensores…'

            results, summary, csv_path = _run_audit_fn(
                master, THETHINGS_API, THETHINGS_TOKEN, audit_dir,
                sleep=0.1, progress_cb=_progress,
            )

            with _import_lock:
                _import_state['sub_status'] = 'Generando informe de salud IoT…'

            report = _run_report_fn(summary, audit_dir, summary_source=str(csv_path))

            with _import_lock:
                _import_state['sub_status'] = 'Aplicando inventario IoT al master…'

            # Construir lookup dicts desde datos en memoria
            audit_by_token = {
                r['thing_token']: r
                for r in results
                if r.get('thing_token')
            }
            sys_class = {
                sid: info.get('class', '?')
                for sid, info in report.get('systems_detail', {}).items()
            }

            stats = self._apply_iot_health_to_master(
                master, audit_by_token, sys_class, csv_path.name
            )
            stats['sensors_audited'] = len(results)
            return stats

        except Exception as exc:
            _log.error(f'inventory_health_full failed: {exc}')
            with _import_lock:
                _import_state['sub_status'] = f'Inventario IoT omitido: {exc}'
            return {'skipped': True, 'reason': str(exc)}

    def _resolve_tags_to_fields(self, tags_list, district_map, neighborhood_map):
        result   = {}
        unknowns = []
        for raw_tag in tags_list:
            tag = raw_tag.strip().upper()
            if tag.startswith('DISTRITO-'):
                d = district_map.get(tag)
                if d:
                    result['district_code'] = d['code']
                    result['district_name'] = d['name']
            elif tag.startswith('BARRIO-'):
                nb = neighborhood_map.get(tag[7:])
                if nb:
                    result['neighborhood_key'] = nb['key']
                    result['neighborhood']     = nb['name']
            elif tag.startswith('TIPO-'):
                result['type'] = tag[5:]
            elif tag.startswith('ZONA-'):
                result['zone'] = tag[5:]
            elif tag.startswith('CALLE-'):
                val = raw_tag.strip()[6:]
                if val:
                    result['street_etra'] = val
            else:
                unknowns.append(raw_tag.strip())
        return result, unknowns

    def _fetch_model_things(self, model_id):
        url = f'{THETHINGS_API}/v2/models/{model_id}/things?lib=panel'
        req = urllib.request.Request(url, headers={'authorization': THETHINGS_TOKEN})
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))

    @staticmethod
    def _extract_hos(text):
        """Extrae el código HOS### de un nombre de thing. Devuelve el original si no hay."""
        import re
        m = re.search(r'HOS(\d+)', text, re.IGNORECASE)
        return f'HOS{m.group(1)}' if m else text

    def _thing_to_building(self, thing):
        desc = thing.get('description') or {}
        geo  = desc.get('geo') or {}
        full_name = (desc.get('name') or '').strip()
        hos_id    = self._extract_hos(full_name)
        api_tags = thing.get('tags') or []
        tag_names = [t.get('name') for t in api_tags if t.get('name')]
        return {
            'id':               hos_id,
            'name':             full_name,
            'short_name':       '',
            'description':      '',
            'observaciones':    '',
            'pielh_id':         '',
            'district_code':    None,
            'district_name':    None,
            'neighborhood_key': None,
            'neighborhood':     None,
            'type':             None,
            'zone':             None,
            'street_etra':      '',
            'street_mti':       '',
            'lat':              geo.get('lat'),
            'lon':              geo.get('long'),
            'thing_id':         thing.get('_id', ''),
            'thing_token':      thing.get('thingToken', ''),
            'tags':             ', '.join(tag_names),
            'state':            None,
            'has_data':         None,
            'sensor_count':     0,
            'raw':              {'tags': tag_names},
        }

    def _thing_to_sensor(self, thing, model_info):
        desc = thing.get('description') or {}
        geo  = desc.get('geo') or {}
        name = (desc.get('name') or '').strip()
        tags = thing.get('tags') or []

        # HOS desde tags; fallback: primer token del nombre
        hos = None
        for tag in tags:
            tname = (tag.get('name') or '').upper()
            if tname.startswith('HOS'):
                hos = tname
                break
        if not hos:
            part = name.split('-')[0].split(' ')[0].upper()
            if part.startswith('HOS'):
                hos = part

        return {
            'id':               name,
            'thing_id':         thing.get('_id', ''),
            'thing_token':      thing.get('thingToken', ''),
            'hos':              hos,
            'system_id':        model_info['system_id'],
            'system_name':      model_info['system_name'],
            'lat':              geo.get('lat'),
            'lon':              geo.get('long'),
            'building_name':    None,
            'district_code':    None,
            'district_name':    None,
            'neighborhood_key': None,
            'neighborhood':     None,
            'type':             None,
            'zone':             None,
            'ref_etra':         None,
            'has_data':         None,
            'include':          True,
            'status':           None,
            'sensor_code_old':  None,
            'sensor_order':     None,
            'cu_old':           None,
            'qa_notes':         None,
            'tags':             '',
            'raw':              {},
        }

    # ── Centro de Sincronización IoT ─────────────────────────────────

    def _handle_models(self):
        sensor_models = [m for m in MODELS if m.get('type') == 'sensor']
        self._ok({'ok': True, 'models': sensor_models})

    def _handle_systems_status(self):
        try:
            master = self._load()
            sensors = master.get('sensors', [])
            by_system = {}
            for m in MODELS:
                if m.get('type') != 'sensor':
                    continue
                sid = m['system_id']
                by_system[sid] = {
                    'system_id':   sid,
                    'system_name': m['system_name'],
                    'label':       m['label'],
                    'count':       0,
                    'with_data':   0,
                    'without_data': 0,
                    'last_seen':   None,
                }
            for s in sensors:
                sid = s.get('system_id', '')
                if sid not in by_system:
                    continue
                row = by_system[sid]
                row['count'] += 1
                ih = s.get('iot_health') or {}
                if ih.get('demo_ready') or ih.get('has_real_data'):
                    row['with_data'] += 1
                    ls = ih.get('last_seen')
                    if ls and (not row['last_seen'] or ls > row['last_seen']):
                        row['last_seen'] = ls
                else:
                    row['without_data'] += 1
            for sid, row in by_system.items():
                if row['count'] == 0:
                    row['status'] = 'NO_DATA'
                elif row['with_data'] == 0:
                    row['status'] = 'NO_DATA'
                elif row['without_data'] == 0:
                    row['status'] = 'ACTIVE'
                else:
                    row['status'] = 'PARTIAL'
                lss = _last_system_sync.get(sid)
                if lss:
                    row['last_sync'] = lss
            total_sensors = len(sensors)
            total_with    = sum(1 for s in sensors if (s.get('iot_health') or {}).get('demo_ready'))
            self._ok({
                'ok': True,
                'systems': list(by_system.values()),
                'total_sensors': total_sensors,
                'total_with_data': total_with,
            })
        except Exception as e:
            self._err(500, str(e))

    def _handle_system_sync_status(self):
        with _system_sync_lock:
            self._ok(dict(_system_sync_state))

    def _handle_import_system(self):
        try:
            body      = self._read_json()
            system_id = (body.get('system_id') or '').strip()
            if not system_id:
                return self._err(400, 'system_id requerido')
            model = next((m for m in MODELS if m.get('system_id') == system_id), None)
            if not model:
                return self._err(404, f'Sistema {system_id} no encontrado')
            with _system_sync_lock:
                if _system_sync_state['running']:
                    return self._ok({'ok': False, 'message': 'already running'})
                _system_sync_state.update({
                    'running': True, 'done': False, 'error': None,
                    'systems': [system_id], 'current_system': system_id,
                    'current_idx': 0, 'total': 1, 'things_done': 0,
                    'started_at': datetime.now().isoformat(), 'finished_at': None,
                })
            self._ok({'ok': True, 'message': 'started'})
            threading.Thread(target=self._run_import_systems, args=([system_id],), daemon=True).start()
        except Exception as e:
            self._err(500, str(e))

    def _handle_import_selected(self):
        try:
            body    = self._read_json()
            systems = body.get('systems') or []
            systems = [s.strip() for s in systems if s.strip()]
            valid   = [m['system_id'] for m in MODELS if m.get('system_id') in systems and m.get('type') == 'sensor']
            if not valid:
                return self._err(400, 'Ningún sistema válido')
            with _system_sync_lock:
                if _system_sync_state['running']:
                    return self._ok({'ok': False, 'message': 'already running'})
                _system_sync_state.update({
                    'running': True, 'done': False, 'error': None,
                    'systems': valid, 'current_system': valid[0],
                    'current_idx': 0, 'total': len(valid), 'things_done': 0,
                    'started_at': datetime.now().isoformat(), 'finished_at': None,
                })
            self._ok({'ok': True, 'message': 'started', 'count': len(valid)})
            threading.Thread(target=self._run_import_systems, args=(valid,), daemon=True).start()
        except Exception as e:
            self._err(500, str(e))

    def _run_import_systems(self, system_ids):
        global _last_system_sync
        try:
            master = self._load()
            for idx, system_id in enumerate(system_ids):
                model = next((m for m in MODELS if m.get('system_id') == system_id), None)
                if not model:
                    continue
                with _system_sync_lock:
                    _system_sync_state['current_system'] = system_id
                    _system_sync_state['current_idx']    = idx
                    _system_sync_state['things_done']    = 0
                ts = datetime.now().isoformat()
                try:
                    things = self._fetch_model_things(model['id'])
                except Exception as exc:
                    _log.warning(f"import-system: {system_id} fallido — {exc}")
                    _last_system_sync[system_id] = {'at': ts, 'sensors': 0, 'ok': False, 'error': str(exc)}
                    continue
                master['sensors'] = [s for s in master['sensors'] if s.get('system_id') != system_id]
                new_sensors = []
                if isinstance(things, list):
                    for thing in things:
                        new_sensors.append(self._thing_to_sensor(thing, model))
                        with _system_sync_lock:
                            _system_sync_state['things_done'] += 1
                master['sensors'].extend(new_sensors)
                _last_system_sync[system_id] = {'at': ts, 'sensors': len(new_sensors), 'ok': True}
                _log.info(f"import-system: {system_id} — {len(new_sensors)} sensores")
                time.sleep(0.2)
            self._resolve_tags_in_master(master)
            self._save(master)
            finished = datetime.now().isoformat()
            with _system_sync_lock:
                _system_sync_state.update({
                    'running': False, 'done': True, 'finished_at': finished,
                })
            _log.info(f"import-system: completado {system_ids}")
        except Exception as exc:
            _log.error(f"import-system: error — {exc}")
            with _system_sync_lock:
                _system_sync_state.update({
                    'running': False, 'done': True, 'error': str(exc),
                    'finished_at': datetime.now().isoformat(),
                })

    # ── Sync to TheThings ─────────────────────────────────────────────

    def _handle_sync_pending(self):
        try:
            master = self._load()
            records = []
            for coll, et in (('buildings', 'building'), ('sensors', 'sensor')):
                for r in master.get(coll, []):
                    if r.get('_sync', {}).get('status') in ('pending', 'error'):
                        records.append({**r, '_entity_type': et})
            self._ok({'ok': True, 'count': len(records), 'records': records})
        except Exception as e:
            self._err(500, str(e))

    def _handle_sync_status(self):
        try:
            master = self._load()
            pending = synced = errors = 0
            last_sync = None
            for coll in ('buildings', 'sensors'):
                for r in master.get(coll, []):
                    st   = r.get('_sync', {}).get('status')
                    s_at = r.get('_sync', {}).get('synced_at')
                    if st == 'pending':  pending += 1
                    elif st == 'synced': synced  += 1
                    elif st == 'error':  errors  += 1
                    if s_at and (not last_sync or s_at > last_sync):
                        last_sync = s_at
            self._ok({'ok': True, 'pending': pending, 'synced': synced, 'errors': errors, 'last_sync': last_sync})
        except Exception as e:
            self._err(500, str(e))

    def _handle_sync_record(self):
        try:
            body        = self._read_json()
            entity_type = body.get('entityType', '')
            record_id   = body.get('id', '')
            selector    = body.get('selector') or {}
            if entity_type not in ('sensor', 'building'):
                return self._err(400, 'entityType must be sensor or building')
            if not record_id:
                return self._err(400, 'id is required')
            master   = self._load()
            siblings = self._siblings(master, entity_type, record_id)
            if not siblings:
                return self._err(404, f"{entity_type} '{record_id}' no encontrado")
            target = siblings[0]
            if selector.get('thing_id'):
                target = next((r for r in siblings if r.get('thing_id') == selector['thing_id']), siblings[0])
            if not target.get('thing_token'):
                return self._err(400, 'Registro sin thing_token')
            self._backup()
            ts = datetime.now().isoformat()
            try:
                result = self._sync_thing(target)
                target['_sync'] = {**(target.get('_sync') or {}), 'status': 'synced', 'synced_at': ts, 'error': None}
                self._save(master)
                _log.info(f"sync: {entity_type} {record_id} ok ({result.get('values_sent', 0)} fields)")
                self._ok({'ok': True, 'id': record_id, 'result': result})
            except Exception as exc:
                target['_sync'] = {**(target.get('_sync') or {}), 'status': 'error', 'error': str(exc)}
                self._save(master)
                _log.error(f"sync: {entity_type} {record_id} error: {exc}")
                self._err(500, str(exc))
        except Exception as e:
            self._err(500, str(e))

    def _handle_sync_all(self):
        try:
            master  = self._load()
            pending = []
            for coll, et in (('buildings', 'building'), ('sensors', 'sensor')):
                for r in master.get(coll, []):
                    if r.get('_sync', {}).get('status') in ('pending', 'error'):
                        pending.append((et, r))
            if not pending:
                return self._ok({'ok': True, 'total': 0, 'synced': 0, 'errors': 0, 'results': []})
            self._backup()
            ts = datetime.now().isoformat()
            synced_n = errors_n = 0
            results  = []
            for et, record in pending:
                rid = record.get('id', '')
                if not record.get('thing_token'):
                    record['_sync'] = {**(record.get('_sync') or {}), 'status': 'error', 'error': 'sin thing_token'}
                    errors_n += 1
                    results.append({'id': rid, 'ok': False, 'error': 'sin thing_token'})
                    continue
                try:
                    r = self._sync_thing(record)
                    record['_sync'] = {**(record.get('_sync') or {}), 'status': 'synced', 'synced_at': ts, 'error': None}
                    synced_n += 1
                    results.append({'id': rid, 'ok': True, 'values_sent': r.get('values_sent', 0)})
                    _log.info(f"sync-all: {et} {rid} ok")
                except Exception as exc:
                    record['_sync'] = {**(record.get('_sync') or {}), 'status': 'error', 'error': str(exc)}
                    errors_n += 1
                    results.append({'id': rid, 'ok': False, 'error': str(exc)})
                    _log.error(f"sync-all: {et} {rid} error: {exc}")
            self._save(master)
            self._ok({'ok': True, 'total': len(pending), 'synced': synced_n, 'errors': errors_n, 'results': results})
        except Exception as e:
            self._err(500, str(e))

    def _sync_thing(self, record):
        thing_token = record.get('thing_token', '')
        if not thing_token:
            raise ValueError('sin thing_token')
        if not THETHINGS_TOKEN:
            raise ValueError('sin token configurado en config.json')
        sync_fields = record.get('_sync', {}).get('fields', [])
        values = [
            {'key': f, 'value': record[f]}
            for f in sync_fields
            if f in record and record[f] is not None and f in SYNC_ALLOWED_FIELDS
        ]
        if not values:
            return {'skipped': True, 'reason': 'no values to sync', 'values_sent': 0}
        url     = f'{THETHINGS_API}/v2/things/{thing_token}?store=true&broadcast=true'
        payload = json.dumps({'values': values}).encode('utf-8')
        req     = urllib.request.Request(
            url, data=payload,
            headers={'authorization': THETHINGS_TOKEN, 'Content-Type': 'application/json'},
            method='POST',
        )
        ctx = ssl._create_unverified_context()
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                resp.read()
        except urllib.error.HTTPError as e:
            body = ''
            try:
                body = e.read().decode('utf-8', errors='replace')
            except Exception:
                pass
            _log.error(f"sync: POST {url} → {e.code} {e.reason} | body: {body}")
            raise ValueError(f"HTTP {e.code} {e.reason}: {body}")
        return {'values_sent': len(values)}

    def _mark_sync_pending(self, records, updated_fields):
        sync_fields = sorted(f for f in updated_fields if f in SYNC_ALLOWED_FIELDS)
        if not sync_fields:
            return
        ts = datetime.now().isoformat()
        for r in records:
            prev   = r.get('_sync') or {}
            merged = sorted(set(prev.get('fields', [])) | set(sync_fields))
            r['_sync'] = {
                'status':     'pending',
                'updated_at': ts,
                'fields':     merged,
                'error':      None,
                'synced_at':  prev.get('synced_at'),
            }

    # ── Helpers ───────────────────────────────────────────────────────

    def _read_json(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n).decode('utf-8'))

    def _load(self):
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))

    def _save(self, master):
        DATA_FILE.write_text(
            json.dumps(master, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    def _siblings(self, master, entity_type, record_id):
        collection = 'sensors' if entity_type == 'sensor' else 'buildings'
        return [r for r in master.get(collection, []) if r.get('id') == record_id]

    def _propagate_to_sensors(self, master, building_id, shared_updates):
        """Aplica a todos los sensores de un edificio (mismo `hos`) los campos
        de BUILDING_TO_SENSOR_FIELDS editados en el edificio. La edición
        explícita gana (sobreescribe)."""
        sensor_updates = {k: v for k, v in shared_updates.items() if k in BUILDING_TO_SENSOR_FIELDS}
        if not sensor_updates:
            return 0
        sensors = [s for s in master.get('sensors', []) if s.get('hos') == building_id]
        for s in sensors:
            before = copy.deepcopy(s)
            self._apply_updates(s, sensor_updates)
            for field, new_val in s.items():
                if field == 'raw':
                    continue
                if before.get(field) != new_val:
                    _log_change('sensor', s.get('id'), field, before.get(field), new_val)
        return len(sensors)

    def _complete_empty_fields(self, records):
        """Rellena campos vacíos de cada registro con el primer valor no vacío
        entre sus hermanos (mismo id). Nunca sobreescribe valores existentes."""
        if len(records) < 2:
            return
        keys = set()
        for r in records:
            keys.update(r.keys())
        keys -= OWN_FIELDS
        keys -= {'id', 'raw'}

        for key in keys:
            donor_value = None
            for r in records:
                v = r.get(key)
                if v not in EMPTY_VALUES:
                    donor_value = v
                    break
            if donor_value is None:
                continue
            for r in records:
                if r.get(key) in EMPTY_VALUES:
                    r[key] = donor_value

    def _expand_updates(self, updates, master):
        expanded = dict(updates)
        cats = master.get('catalogs', {})

        if 'district_code' in expanded:
            district = next(
                (d for d in cats.get('districts', []) if d.get('code') == expanded['district_code']),
                None
            )
            expanded['district_name'] = district.get('name') if district else None

        if 'neighborhood_key' in expanded:
            neighborhood = next(
                (n for n in cats.get('neighborhoods', []) if n.get('key') == expanded['neighborhood_key']),
                None
            )
            expanded['neighborhood'] = neighborhood.get('name') if neighborhood else None

        return expanded

    def _apply_updates(self, rec, updates):
        rec.update(updates)
        raw = rec.get('raw')
        if not isinstance(raw, dict):
            return
        if 'district_code' in updates:
            raw['Distrito'] = updates['district_code']
        if 'neighborhood' in updates:
            raw['Barrio'] = updates['neighborhood']

    def _validate(self, updates, master):
        cats = master.get('catalogs', {})
        valid_districts     = {d['code'] for d in cats.get('districts', [])}
        valid_neighborhoods = {n['key']  for n in cats.get('neighborhoods', [])}
        valid_systems       = {s['id']   for s in cats.get('systems', [])}
        valid_systems      |= {s.get('system_id') for s in master.get('sensors', []) if s.get('system_id')}

        errors = []
        if updates.get('district_code'):
            if updates['district_code'] not in valid_districts:
                errors.append(f"district_code '{updates['district_code']}' no existe en catálogo")
        if updates.get('neighborhood_key'):
            if updates['neighborhood_key'] not in valid_neighborhoods:
                errors.append(f"neighborhood_key '{updates['neighborhood_key']}' no existe en catálogo")
        if updates.get('system_id'):
            if updates['system_id'] not in valid_systems:
                errors.append(f"system_id '{updates['system_id']}' no existe")
        for coord in ('lat', 'lon'):
            if coord in updates and updates[coord] is not None and updates[coord] != '':
                try:
                    updates[coord] = float(updates[coord])
                except (TypeError, ValueError):
                    errors.append(f"'{coord}' debe ser un número válido")
        return ' | '.join(errors) if errors else None

    def _backup(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
        dest = BACKUP_DIR / f'pielh_qa_master_{ts}.json'
        shutil.copy2(DATA_FILE, dest)
        backups = sorted(BACKUP_DIR.glob('pielh_qa_master_*.json'))
        for old in backups[:-MAX_BACKUPS]:
            old.unlink()

    def _ok(self, obj):
        self._send(200, obj)

    def _err(self, code, msg):
        self._send(code, {'ok': False, 'error': msg})

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[{datetime.now():%H:%M:%S}] {fmt % args}')


if __name__ == '__main__':
    srv = http.server.HTTPServer((HOST, PORT), Handler)
    print(f'PIELH QA  ->  http://localhost:{PORT}')
    try:
        threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
    except Exception:
        pass
    srv.serve_forever()
