#!/usr/bin/env python3
"""PIELH QA — servidor con guardado, health check y logging."""

import http.server
import json
import logging
import shutil
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent

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
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/save-record':
            self._handle_save_single()
        elif self.path == '/api/save-batch':
            self._handle_save_batch()
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

            rec = self._find(master, entity_type, record_id, selector)
            if rec is None:
                return self._err(404, f"{entity_type} '{record_id}' no encontrado")

            updates = self._expand_updates(updates, master)
            old_values = {k: rec.get(k) for k in updates}
            self._backup()
            self._apply_updates(rec, updates)
            self._save(master)
            for field, new_val in updates.items():
                _log_change(entity_type, record_id, field, old_values.get(field), new_val)

            self._ok({'ok': True, 'id': record_id, 'updates': updates})

        except Exception as e:
            self._err(500, str(e))

    # ── Batch ─────────────────────────────────────────────────────────

    def _handle_save_batch(self):
        try:
            body        = self._read_json()
            entity_type = body.get('entityType', '')
            ids         = body.get('ids', [])
            updates     = body.get('updates', {})

            if entity_type not in ('sensor', 'building'):
                return self._err(400, 'entityType must be sensor or building')
            if not ids or not isinstance(ids, list):
                return self._err(400, 'ids must be a non-empty list')
            if not isinstance(updates, dict) or not updates:
                return self._err(400, 'updates must be a non-empty dict')

            master = self._load()
            err = self._validate(updates, master)
            if err:
                return self._err(400, err)
            updates = self._expand_updates(updates, master)

            not_found = [rid for rid in ids if self._find(master, entity_type, rid) is None]
            if not_found:
                return self._err(404, f"No encontrados: {', '.join(not_found)}")

            self._backup()
            for rid in ids:
                rec = self._find(master, entity_type, rid)
                if rec is not None:
                    old_values = {k: rec.get(k) for k in updates}
                    self._apply_updates(rec, updates)
                    for field, new_val in updates.items():
                        _log_change(entity_type, rid, field, old_values.get(field), new_val)
            self._save(master)
            self._ok({'ok': True, 'count': len(ids), 'updates': updates})

        except Exception as e:
            self._err(500, str(e))

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

    def _find(self, master, entity_type, record_id, selector=None):
        collection = 'sensors' if entity_type == 'sensor' else 'buildings'
        matches = [r for r in master.get(collection, []) if r.get('id') == record_id]
        selector = selector if isinstance(selector, dict) else {}
        if selector.get('thing_id'):
            return next((r for r in matches if r.get('thing_id') == selector['thing_id']), None)
        return matches[0] if matches else None

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
    print(f'PIELH QA  →  http://localhost:{PORT}')
    try:
        threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
    except Exception:
        pass
    srv.serve_forever()
