"""
PIELH - Fase 3: Descubrimiento de recursos y salud de datos IoT
Solo lectura. No modifica pielh_qa_master.json.

Fuente: data/thethings_snapshots/latest/thethings_structure_only.json

Prerequisito: ejecutar primero scripts/fetch_thethings_structure.py --no-ssl-verify

API utilizada:
  GET /v2/things/{thing_token}/resources/{resource}?limit=N&lib=panel
"""

import json
import ssl
import time
import argparse
import shutil
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Recursos conocidos por sistema (sincronizado con audit_thethings_activity.py)
# ---------------------------------------------------------------------------
RESOURCE_CANDIDATES = {
    "S01":  ["noise", "noise_avg_d", "noise_avg_h", "noise_avg_w"],
    "S02":  ["temperature", "co2", "no2", "o3", "pm1", "pm10", "pm25", "pressure", "co"],
    "S03":  ["radon", "temperature"],
    "S04":  ["temperature", "humidity", "co2"],
    "S05":  ["energy", "watts", "amps", "volts", "pf", "var"],
    "S06":  ["flow", "volume", "liters", "m3", "water"],
    "S07":  ["gas", "m3_a", "m3_b", "ch_a", "ch_b"],
    "S08":  ["temperature", "pressure", "status", "alarm", "description"],
    "S09":  ["temperature", "humidity", "status", "alarm"],
    "S13A": ["temperature", "humidity", "co2", "energy"],
    "S14A": ["temperature_ext", "humidity_ext", "rainfall", "wind_speed", "solar_rad", "uv_index", "pressure"],
    "S14B": ["temperature_ext", "solar_rad", "uv_index"],
    "S15":  ["presence", "occupancy", "motion", "count"],
    "S17":  ["count", "occupancy", "passengers"],
    "S19":  ["alarm", "gas", "status"],
    "S20":  ["flood", "leak", "alarm", "status"],
    "S21":  ["alert_fire", "temperature", "keepalive", "battery"],
    "S22":  ["next_time_ferrocarril", "destination_ferrocarril",
             "code_line_ferrocarril", "name_ferrocarril"],
    "S23":  ["occupancy", "count", "status"],
    "S24":  ["all", "Car", "Bus", "Truck", "Bicycle", "plate"],
    "SIP":  ["connected", "keepalive"],
}
RESOURCE_DEFAULT = [
    "temperature", "humidity", "co2", "energy", "value",
    "noise", "status", "keepalive", "battery", "alarm",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_TS_KEYS  = ("timestamp", "ts", "at", "datetime", "date",
             "created_at", "created", "time", "recv", "recvTime")
_VAL_KEYS = ("value", "v", "data", "result", "val")


def infer_value_type(val) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, (int, float)):
        return "number"
    if isinstance(val, str):
        return "string"
    return "unknown"


def parse_timestamp(ts_raw):
    if not ts_raw:
        return None
    if isinstance(ts_raw, (int, float)):
        try:
            return datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
        except Exception:
            return None
    if isinstance(ts_raw, str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(ts_raw, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    return None


def extract_last_reading(api_response):
    """Returns (value, timestamp_str, timestamp_dt)."""
    if not api_response:
        return None, None, None
    items = None
    if isinstance(api_response, list):
        items = api_response
    elif isinstance(api_response, dict):
        for key in ("data", "values", "resources", "items"):
            if key in api_response and isinstance(api_response[key], list):
                items = api_response[key]
                break
        if items is None:
            val = next((api_response[k] for k in _VAL_KEYS
                        if k in api_response and api_response[k] is not None), None)
            ts  = next((api_response[k] for k in _TS_KEYS
                        if k in api_response and api_response[k] is not None), None)
            return val, str(ts) if ts is not None else None, parse_timestamp(ts)
    if not items:
        return None, None, None
    last = items[0]
    val = next((last[k] for k in _VAL_KEYS if k in last and last[k] is not None), None)
    ts  = next((last[k] for k in _TS_KEYS  if k in last and last[k] is not None), None)
    return val, str(ts) if ts is not None else None, parse_timestamp(ts)


def build_last_seen_index(raw_dir: Path) -> dict:
    """Construye thing_id → lastSeen desde los raw de Fase 1 (sin llamadas API)."""
    index = {}
    for f in sorted(raw_dir.glob("model_*.json")):
        try:
            things = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(things, dict):
                things = things.get("things", things.get("data", []))
            for t in things:
                tid = t.get("_id", "")
                ls  = t.get("lastSeen")
                if tid and ls:
                    index[tid] = ls
        except Exception:
            pass
    return index


def fetch_resource(api_base, token, thing_token, resource, limit, ssl_ctx):
    url = f"{api_base}/v2/things/{thing_token}/resources/{resource}?limit={limit}&lib=panel"
    req = urllib.request.Request(url, headers={"authorization": token})
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8")), 200, None
    except urllib.error.HTTPError as e:
        return None, e.code, f"HTTP {e.code}"
    except Exception as e:
        return None, 0, str(e)[:120]


def probe_sensor(sensor, api_base, token, ssl_ctx, resources_to_probe,
                 limit_samples, include_preview, sleep_secs):
    thing_token = sensor.get("thing_token", "")
    resource_results = []
    errors_count = 0
    has_real_data = False
    best_last_seen     = None
    best_last_seen_dt  = None

    for i, resource in enumerate(resources_to_probe):
        if i > 0 and sleep_secs > 0:
            time.sleep(sleep_secs)

        if not thing_token:
            resource_results.append({
                "resource": resource, "exists": False, "has_data": False,
                "samples_count": 0, "last_seen": None,
                "last_value_type": None, "http_status": None,
                "error": "no_thing_token",
            })
            errors_count += 1
            continue

        data, status, err = fetch_resource(api_base, token, thing_token, resource,
                                           limit_samples, ssl_ctx)

        if status == 404:
            resource_results.append({
                "resource": resource, "exists": False, "has_data": False,
                "samples_count": 0, "last_seen": None,
                "last_value_type": None, "http_status": 404, "error": None,
            })
        elif status != 200:
            errors_count += 1
            resource_results.append({
                "resource": resource, "exists": None, "has_data": False,
                "samples_count": 0, "last_seen": None,
                "last_value_type": None,
                "http_status": status if status else None,
                "error": err,
            })
        else:
            val, ts_str, ts_dt = extract_last_reading(data)
            has_data = val is not None or ts_str is not None
            if has_data:
                has_real_data = True
                if ts_dt and (best_last_seen_dt is None or ts_dt > best_last_seen_dt):
                    best_last_seen_dt = ts_dt
                    best_last_seen = ts_str
            entry = {
                "resource":        resource,
                "exists":          True,
                "has_data":        has_data,
                "samples_count":   1 if has_data else 0,
                "last_seen":       ts_str,
                "last_value_type": infer_value_type(val) if val is not None
                                   else ("unknown" if has_data else None),
                "http_status":     200,
                "error":           None,
            }
            if include_preview and val is not None:
                entry["sample_value"] = val
            resource_results.append(entry)

    has_any = any(r["exists"] is True for r in resource_results)
    return {
        "resources":       resource_results,
        "has_any_resource": has_any,
        "has_real_data":    has_real_data,
        "last_seen":        best_last_seen,
        "errors_count":     errors_count,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PIELH - Fase 3: Descubrimiento de recursos y salud de datos IoT"
    )
    parser.add_argument("--limit-sensors",       type=int,   default=None,
                        help="Procesar solo N sensores (útil para pruebas)")
    parser.add_argument("--system",              type=str,   default=None,
                        help="Filtrar por system_id (ej: S01)")
    parser.add_argument("--limit-samples",       type=int,   default=1,
                        help="Muestras a pedir por recurso — ?limit=N (default: 1)")
    parser.add_argument("--no-ssl-verify",       action="store_true",
                        help="Deshabilitar verificación SSL")
    parser.add_argument("--resources",           type=str,   default=None,
                        help="Recursos a probar (separados por coma). Ej: temperature,co2")
    parser.add_argument("--probe-common",        action="store_true",
                        help="Usar RESOURCE_DEFAULT para sistemas sin candidatos conocidos")
    parser.add_argument("--include-sample-preview", action="store_true",
                        help="Incluir muestra del valor en el output (desactivado por defecto)")
    parser.add_argument("--sleep",               type=float, default=0.15,
                        help="Pausa entre peticiones en segundos (default: 0.15)")
    args = parser.parse_args()

    base_dir   = Path(__file__).resolve().parent.parent
    cfg_path   = base_dir / "config.json"

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

    latest_dir  = base_dir / "data" / "thethings_snapshots" / "latest"
    raw_dir     = latest_dir / "raw"
    struct_path = latest_dir / "thethings_structure_only.json"

    if not struct_path.exists():
        print("[ERROR] No existe thethings_structure_only.json en latest/")
        print("        Ejecuta primero: python scripts/fetch_thethings_structure.py --no-ssl-verify")
        return 1

    struct = json.loads(struct_path.read_text(encoding="utf-8"))
    sensors = struct.get("sensors", [])

    # Índice lastSeen desde raw
    last_seen_index = {}
    if raw_dir.exists():
        print("[PIELH] Leyendo lastSeen desde raw/...")
        last_seen_index = build_last_seen_index(raw_dir)
        print(f"        Things con lastSeen: {len(last_seen_index)}")

    # Filtros
    if args.system:
        sensors = [s for s in sensors if s.get("system_id") == args.system]
        print(f"[PIELH] Filtro sistema: {args.system} -> {len(sensors)} sensores")

    if args.limit_sensors:
        sensors = sensors[:args.limit_sensors]
        print(f"[PIELH] Límite sensores: {args.limit_sensors}")

    # Recursos a probar
    fixed_resources = None
    if args.resources:
        fixed_resources = [r.strip() for r in args.resources.split(",") if r.strip()]
        print(f"[PIELH] Recursos fijos: {fixed_resources}")

    ssl_ctx = (ssl._create_unverified_context() if args.no_ssl_verify
               else ssl.create_default_context())
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"[PIELH] API: {api_base}")
    print(f"[PIELH] Sensores a procesar: {len(sensors)}")
    print(f"[PIELH] Muestras por recurso: {args.limit_samples}")
    print()

    sensors_out   = []
    summary_sys   = defaultdict(lambda: {
        "sensors_processed": 0, "sensors_with_data": 0,
        "resources_found": set(), "errors": 0,
        "last_seen": None, "last_seen_dt": None,
    })
    global_errors = []

    for i, sensor in enumerate(sensors, 1):
        sid       = sensor.get("id", "?")
        sys_id    = sensor.get("system_id", "UNKNOWN")
        sys_name  = sensor.get("system_name", "")
        thing_id  = sensor.get("thing_id", "")

        # Recursos a probar para este sensor
        if fixed_resources:
            resources_to_probe = fixed_resources
        elif sys_id in RESOURCE_CANDIDATES:
            resources_to_probe = RESOURCE_CANDIDATES[sys_id]
        elif args.probe_common:
            resources_to_probe = RESOURCE_DEFAULT
        else:
            resources_to_probe = RESOURCE_CANDIDATES.get(sys_id, RESOURCE_DEFAULT)

        platform_last_seen = last_seen_index.get(thing_id)

        print(f"  [{i:4}/{len(sensors)}] {sid[:45]:45} {sys_id:5} "
              f"{len(resources_to_probe)} recursos ... ", end="", flush=True)

        probe = probe_sensor(
            sensor, api_base, token, ssl_ctx,
            resources_to_probe, args.limit_samples,
            args.include_sample_preview, args.sleep,
        )

        # Actualizar summary de sistema
        ss = summary_sys[sys_id]
        ss["sensors_processed"] += 1
        ss.setdefault("system_name", sys_name)
        if probe["has_real_data"]:
            ss["sensors_with_data"] += 1
            ls_dt = parse_timestamp(probe["last_seen"])
            if ls_dt and (ss["last_seen_dt"] is None or ls_dt > ss["last_seen_dt"]):
                ss["last_seen_dt"] = ls_dt
                ss["last_seen"]    = probe["last_seen"]
        if probe["errors_count"]:
            ss["errors"] += probe["errors_count"]
        for r in probe["resources"]:
            if r["exists"]:
                ss["resources_found"].add(r["resource"])

        tag_status = ("DATA" if probe["has_real_data"]
                      else ("ERR" if probe["errors_count"] else "NO_DATA"))
        print(tag_status)

        sensors_out.append({
            "id":                  sid,
            "hos":                 sensor.get("hos"),
            "system_id":           sys_id,
            "system_name":         sys_name,
            "thing_id":            thing_id,
            "thing_token_present": bool(sensor.get("thing_token")),
            "platform_last_seen":  platform_last_seen,
            **probe,
        })

    # Serializar summary (convertir sets a listas)
    summary_final = {}
    for sys_id, info in sorted(summary_sys.items()):
        summary_final[sys_id] = {
            "sensors_processed": info["sensors_processed"],
            "sensors_with_data": info["sensors_with_data"],
            "system_name":       info.get("system_name", ""),
            "resources_found":   sorted(info["resources_found"]),
            "errors":            info["errors"],
            "last_seen":         info["last_seen"],
        }
        # No guardar last_seen_dt en output

    output = {
        "_meta": {
            "created_at":           datetime.now().isoformat(),
            "source":               "thethings",
            "phase":                "resources_probe",
            "base_structure_snapshot": str(struct_path),
            "sensors_total":        len(struct.get("sensors", [])),
            "sensors_processed":    len(sensors_out),
            "limit_samples":        args.limit_samples,
            "mode":                 "probe_candidates",
            "master_modified":      False,
        },
        "sensors":           sensors_out,
        "summary_by_system": summary_final,
        "errors":            global_errors,
    }

    # Guardar snapshot timestamped
    snap_dir = base_dir / "data" / "thethings_snapshots" / ts
    snap_dir.mkdir(parents=True, exist_ok=True)
    out_file = snap_dir / "thethings_resources_probe.json"
    out_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # Copiar a latest
    latest_out = latest_dir / "thethings_resources_probe.json"
    shutil.copy2(out_file, latest_out)

    # Resumen final
    with_data  = sum(1 for s in sensors_out if s["has_real_data"])
    with_any   = sum(1 for s in sensors_out if s["has_any_resource"])
    no_data    = sum(1 for s in sensors_out if not s["has_real_data"])
    with_err   = sum(1 for s in sensors_out if s["errors_count"] > 0)

    print()
    print("[OK] Probe completado:")
    print(f"     Sensores procesados    : {len(sensors_out)}")
    print(f"     Con recursos válidos   : {with_any}")
    print(f"     Con datos reales       : {with_data}")
    print(f"     Sin datos              : {no_data}")
    print(f"     Con errores API        : {with_err}")
    print()
    print("     Por sistema:")
    for sys_id, info in sorted(summary_final.items()):
        pct = f"{info['sensors_with_data']/info['sensors_processed']*100:.0f}%" \
              if info["sensors_processed"] else "—"
        print(f"       {sys_id:5} {info['system_name']:30} "
              f"{info['sensors_with_data']}/{info['sensors_processed']} ({pct})")
    print()
    print(f"     Snapshot : {out_file}")
    print(f"     Latest   : {latest_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
