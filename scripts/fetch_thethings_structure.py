"""
PIELH - Fetch TheThings Structure (Fase 1)
Descarga estructura de buildings y sensores desde TheThings API.
Solo lectura. No modifica pielh_qa_master.json. No resuelve tags ni recursos.
"""

import json
import ssl
import re
import time
import shutil
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# MODELS copiado de server.py (fuente: server.py:88-111)
# Mantener sincronizado si se añaden/eliminan modelos en server.py
# ---------------------------------------------------------------------------
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


def _extract_hos(text):
    m = re.search(r'HOS(\d+)', text, re.IGNORECASE)
    return f'HOS{m.group(1)}' if m else None


def _thing_to_building_minimal(thing):
    desc = thing.get('description') or {}
    geo  = desc.get('geo') or {}
    full_name = (desc.get('name') or '').strip()
    hos_id    = _extract_hos(full_name) or full_name
    return {
        'id':           hos_id,
        'name':         full_name,
        'thing_id':     thing.get('_id', ''),
        'thing_token':  thing.get('thingToken', ''),
        'model_id':     34738,
        'model_name':   'ASSETS',
        'system_id':    None,
        'system_name':  None,
        'hos':          hos_id,
        'lat':          geo.get('lat'),
        'lon':          geo.get('long'),
        'raw_minimal':  {'status': thing.get('status')},
    }


def _thing_to_sensor_minimal(thing, model_info):
    desc = thing.get('description') or {}
    geo  = desc.get('geo') or {}
    name = (desc.get('name') or '').strip()
    tags = thing.get('tags') or []

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
        'id':           name,
        'thing_id':     thing.get('_id', ''),
        'thing_token':  thing.get('thingToken', ''),
        'model_id':     model_info['id'],
        'model_name':   model_info['label'],
        'system_id':    model_info['system_id'],
        'system_name':  model_info['system_name'],
        'hos':          hos,
        'lat':          geo.get('lat'),
        'lon':          geo.get('long'),
        'raw_minimal':  {'status': thing.get('status')},
    }


def fetch_model(api_base, token, model_id, ssl_verify):
    url = f"{api_base}/v2/models/{model_id}/things?lib=panel"
    req = urllib.request.Request(url, headers={'authorization': token})
    ctx = ssl.create_default_context() if ssl_verify else ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description="PIELH - Fetch TheThings Structure (Fase 1)")
    parser.add_argument("--no-ssl-verify", action="store_true", help="Deshabilitar verificación SSL")
    parser.add_argument("--sleep",         type=float, default=0.3, help="Pausa entre peticiones (s)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    cfg_path = base_dir / "config.json"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    api_base = cfg.get("thethings_api", "").rstrip("/")
    token    = cfg.get("thethings_token", "")

    if not token:
        print("[ERROR] thethings_token no encontrado en config.json")
        return 1

    if not api_base:
        print("[ERROR] thethings_api no encontrado en config.json")
        return 1

    ssl_verify = not args.no_ssl_verify
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    snap_dir = base_dir / "data" / "thethings_snapshots" / ts
    raw_dir  = snap_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print(f"[PIELH] API: {api_base}")
    print(f"[PIELH] Snapshot: {snap_dir}")
    print(f"[PIELH] Modelos a procesar: {len(MODELS)}")
    print()

    buildings = []
    sensors   = []
    models_summary = []
    errors = []

    for model in MODELS:
        model_id   = model['id']
        model_type = model['type']
        label      = model['label']
        system_id  = model.get('system_id', 'ASSETS')

        print(f"  [{model_type.upper():8}] {label} (id={model_id}) ... ", end="", flush=True)

        try:
            data = fetch_model(api_base, token, model_id, ssl_verify)
        except urllib.error.HTTPError as e:
            msg = f"HTTP {e.code}"
            print(f"ERROR {msg}")
            errors.append({'model_id': model_id, 'label': label, 'error': msg})
            models_summary.append({'model_id': model_id, 'label': label, 'type': model_type,
                                   'system_id': system_id, 'count': 0, 'error': msg})
            time.sleep(args.sleep)
            continue
        except Exception as e:
            msg = str(e)
            print(f"ERROR {msg}")
            errors.append({'model_id': model_id, 'label': label, 'error': msg})
            models_summary.append({'model_id': model_id, 'label': label, 'type': model_type,
                                   'system_id': system_id, 'count': 0, 'error': msg})
            time.sleep(args.sleep)
            continue

        # Guardar raw
        raw_file = raw_dir / f"model_{model_id}_{system_id}.json"
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        things = data if isinstance(data, list) else data.get('things', data.get('data', []))
        count  = len(things)
        print(f"{count} things")

        models_summary.append({
            'model_id':   model_id,
            'label':      label,
            'type':       model_type,
            'system_id':  system_id,
            'count':      count,
            'error':      None,
        })

        if model_type == 'building':
            for thing in things:
                buildings.append(_thing_to_building_minimal(thing))
        else:
            for thing in things:
                sensors.append(_thing_to_sensor_minimal(thing, model))

        time.sleep(args.sleep)

    structure = {
        '_meta': {
            'created_at':    datetime.now().isoformat(),
            'source':        'thethings',
            'phase':         'structure_only',
            'models_total':  len(MODELS),
            'models_ok':     len([m for m in models_summary if not m['error']]),
            'models_error':  len(errors),
            'things_total':  len(buildings) + len(sensors),
            'buildings_total': len(buildings),
            'sensors_total':   len(sensors),
        },
        'buildings':       buildings,
        'sensors':         sensors,
        'models_summary':  models_summary,
    }

    struct_file = snap_dir / "thethings_structure_only.json"
    with open(struct_file, "w", encoding="utf-8") as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)

    # Alias latest (copia en Windows — sin symlinks)
    latest_dir = base_dir / "data" / "thethings_snapshots" / "latest"
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    shutil.copytree(snap_dir, latest_dir)

    print()
    print("[OK] Descarga completada:")
    print(f"     Modelos procesados : {len(MODELS)}")
    print(f"     Modelos con error  : {len(errors)}")
    print(f"     Buildings          : {len(buildings)}")
    print(f"     Sensors            : {len(sensors)}")
    print(f"     Snapshot           : {snap_dir}")
    print(f"     Latest             : {latest_dir}")

    if errors:
        print()
        print("[WARN] Errores por modelo:")
        for e in errors:
            print(f"       model_id={e['model_id']} ({e['label']}): {e['error']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
