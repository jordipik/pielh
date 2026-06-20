"""
PIELH FASE 0 - Auditoría IoT TheThings
Solo lectura. No modifica pielh_qa_master.json.
"""

import json
import csv
import ssl
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# ---------------------------------------------------------------------------
# Recursos candidatos por sistema
# ---------------------------------------------------------------------------
# Recursos reales descubiertos via discover_thethings_resources.py (2026-06-20)
RESOURCE_CANDIDATES = {
    "S01":  ["noise", "noise_avg_d", "noise_avg_h", "noise_avg_w"],
    "S02":  ["temperature", "co2", "no2", "o3", "pm1", "pm10", "pm25", "pressure", "co"],
    "S04":  ["temperature", "humidity", "co2"],
    "S05":  ["energy", "watts", "amps", "volts", "pf", "var"],
    "S07":  ["gas", "m3_a", "m3_b", "ch_a", "ch_b"],
    "S14A": ["temperature_ext", "humidity_ext", "rainfall", "wind_speed", "solar_rad",
             "uv_index", "pressure"],
    "S21":  ["alert_fire", "temperature", "keepalive", "battery"],
    "S22":  ["next_time_ferrocarril", "destination_ferrocarril",
             "code_line_ferrocarril", "name_ferrocarril"],
    "S24":  ["all", "Car", "Bus", "Truck", "Bicycle", "plate"],
    "SIP":  ["connected"],
}
RESOURCE_DEFAULT = ["temperature", "humidity", "co2", "energy", "value", "noise"]

CSV_COLUMNS = [
    "sensor_id", "thing_id", "thing_token", "hos", "building_found",
    "building_name", "system_id", "system_name", "district_name",
    "neighborhood", "lat", "lon", "thing_status", "resource_detected",
    "last_timestamp", "last_value", "has_real_value", "timestamp_status",
    "days_since_last_data", "active_status", "issues", "api_error",
]

# Códigos de retorno internos de fetch_resource
_FR_OK      = "OK"
_FR_SKIP    = "NOT_FOUND"       # 404 — recurso no existe, probar siguiente
_FR_INVALID = "TOKEN_OR_THING_INVALID"   # 400/401/403 — token/thing inválido
_FR_ERROR   = "API_ERROR"       # 500+, timeout, red

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config(base_dir: Path) -> dict:
    cfg_path = base_dir / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_master(cfg: dict, base_dir: Path) -> dict:
    json_path = base_dir / cfg["json_file"]
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_ssl_ctx(verify: bool) -> ssl.SSLContext:
    if not verify:
        return ssl._create_unverified_context()
    return ssl.create_default_context()


def fetch_resource(api_base: str, token: str, thing_token: str, resource: str,
                   ssl_ctx: ssl.SSLContext, timeout: int = 15) -> Tuple:
    """Returns (data_or_none, fetch_status) — nunca lanza excepciones."""
    url = f"{api_base}/v2/things/{thing_token}/resources/{resource}?limit=1&lib=panel"
    req = urllib.request.Request(url, headers={"authorization": token})
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data, _FR_OK
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, _FR_SKIP
        if e.code in (400, 401, 403):
            return None, _FR_INVALID
        return None, _FR_ERROR   # 500+
    except Exception as e:
        return None, _FR_ERROR


def parse_timestamp(ts_raw) -> Optional[datetime]:
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


def classify_status(days: Optional[float]) -> str:
    if days is None:
        return "NO_DATA"
    if days <= 1:
        return "ACTIVE_24H"
    if days <= 7:
        return "ACTIVE_7D"
    if days <= 30:
        return "STALE_30D"
    if days <= 90:
        return "STALE_90D"
    return "INACTIVE_90D"


_TS_KEYS  = ("timestamp", "ts", "at", "datetime", "date", "created_at",
             "created", "time", "recv", "recvTime")
_VAL_KEYS = ("value", "v", "data", "result", "val")


def _pick_value(obj: dict):
    for k in _VAL_KEYS:
        if k in obj and obj[k] is not None:
            return obj[k]
    return None


def _pick_ts(obj: dict):
    for k in _TS_KEYS:
        if k in obj and obj[k] is not None:
            return obj[k]
    return None


def extract_last_reading(api_response) -> Tuple:
    """Returns (last_value, last_timestamp_str, last_dt).

    last_timestamp_str is the raw value as string (even if unparseable),
    so callers can distinguish MISSING (None) from INVALID (str but dt=None).
    """
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
            val = _pick_value(api_response)
            ts  = _pick_ts(api_response)
            dt  = parse_timestamp(ts)
            return val, str(ts) if ts is not None else None, dt

    if not items:
        return None, None, None

    last = items[0]
    val = _pick_value(last)
    ts  = _pick_ts(last)
    dt  = parse_timestamp(ts)
    return val, str(ts) if ts is not None else None, dt


# ---------------------------------------------------------------------------
# Auditoría de un sensor
# ---------------------------------------------------------------------------

def audit_sensor(sensor: dict, api_base: str, token: str, ssl_ctx: ssl.SSLContext,
                 buildings_by_hos: dict) -> dict:
    now_utc = datetime.now(timezone.utc)

    sid        = sensor.get("id", "")
    thing_id   = sensor.get("thing_id", "")
    thing_tok  = sensor.get("thing_token", "")
    hos        = sensor.get("hos", "")
    system_id  = sensor.get("system_id", "")
    system_name = sensor.get("system_name", "")
    lat        = sensor.get("lat")
    lon        = sensor.get("lon")
    building_name  = sensor.get("building_name") or ""
    district_name  = sensor.get("district_name") or ""
    neighborhood   = sensor.get("neighborhood") or ""

    issues = []

    # Quality checks
    if not thing_tok:
        issues.append("MISSING_THING_TOKEN")
    if not thing_id:
        issues.append("MISSING_THING_ID")
    if not hos:
        issues.append("MISSING_HOS")
    if lat is None or lon is None:
        issues.append("MISSING_COORDS")

    # Building lookup
    building_found = False
    if hos and hos in buildings_by_hos:
        building_found = True
        b = buildings_by_hos[hos]
        if not building_name:
            building_name = b.get("name", "")
        if not district_name:
            district_name = b.get("district_name") or ""
        if not neighborhood:
            neighborhood  = b.get("neighborhood") or ""
        if lat is None:
            lat = b.get("lat")
        if lon is None:
            lon = b.get("lon")
    else:
        issues.append("BUILDING_NOT_FOUND")

    if not district_name:
        issues.append("MISSING_DISTRICT")
    if not neighborhood:
        issues.append("MISSING_NEIGHBORHOOD")

    result = {
        "sensor_id":            sid,
        "thing_id":             thing_id,
        "thing_token":          thing_tok,
        "hos":                  hos,
        "building_found":       building_found,
        "building_name":        building_name,
        "system_id":            system_id,
        "system_name":          system_name,
        "district_name":        district_name,
        "neighborhood":         neighborhood,
        "lat":                  lat,
        "lon":                  lon,
        "thing_status":         "UNKNOWN",
        "resource_detected":    "",
        "last_timestamp":       None,
        "last_value":           None,
        "has_real_value":       False,
        "timestamp_status":     "NOT_APPLICABLE",
        "days_since_last_data": None,
        "active_status":        "NO_DATA",
        "issues":               [],
        "api_error":            "",
        "raw_sample":           None,
    }

    if "MISSING_THING_TOKEN" in issues:
        result["issues"] = issues
        return result

    # Probar recursos candidatos
    candidates = RESOURCE_CANDIDATES.get(system_id, RESOURCE_DEFAULT)
    found_data  = False
    last_error  = ""

    for resource in candidates:
        api_data, fetch_status = fetch_resource(
            api_base, token, thing_tok, resource, ssl_ctx
        )

        if fetch_status == _FR_INVALID:
            result["thing_status"]  = "TOKEN_OR_THING_INVALID"
            result["active_status"] = "TOKEN_OR_THING_INVALID"
            issues.append("TOKEN_OR_THING_INVALID")
            break

        if fetch_status == _FR_ERROR:
            result["thing_status"] = "API_ERROR"
            issues.append("API_ERROR")
            result["api_error"] = last_error or "timeout_or_server_error"
            break

        if fetch_status == _FR_SKIP:
            # 404 — recurso no existe en este thing; marcar válido y probar siguiente
            result["thing_status"] = "VALID"
            continue

        # _FR_OK — respuesta recibida
        result["thing_status"] = "VALID"
        val, ts_str, ts_dt = extract_last_reading(api_data)
        if val is None and ts_str is None:
            continue  # respuesta vacía, probar siguiente

        result["resource_detected"] = resource
        result["last_value"]        = val
        result["last_timestamp"]    = ts_str
        result["has_real_value"]    = val is not None
        result["raw_sample"]        = api_data if not isinstance(api_data, list) else api_data[:1]

        if ts_dt is not None:
            result["timestamp_status"] = "OK"
        elif ts_str is not None:
            result["timestamp_status"] = "INVALID"
        else:
            result["timestamp_status"] = "MISSING"

        if ts_dt is not None:
            delta = now_utc - ts_dt
            result["days_since_last_data"] = round(delta.total_seconds() / 86400, 2)
            result["active_status"] = classify_status(result["days_since_last_data"])
        elif val is not None:
            result["active_status"] = "DATA_NO_TIMESTAMP"

        found_data = True
        break

    if (not found_data
            and result["thing_status"] not in ("TOKEN_OR_THING_INVALID", "API_ERROR")):
        if "NO_DATA" not in issues:
            issues.append("NO_DATA")

    result["issues"] = issues
    return result


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------

def save_outputs(results: list, summary: dict, out_dir: Path, ts_str: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON completo
    json_path = out_dir / f"thethings_activity_{ts_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    # CSV
    csv_path = out_dir / f"thethings_activity_{ts_str}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = dict(r)
            row["issues"] = "; ".join(r.get("issues", []))
            writer.writerow(row)

    # Summary JSON
    summary_path = out_dir / f"thethings_activity_summary_{ts_str}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return json_path, csv_path, summary_path


def _sys_zero(system_name: str = "") -> dict:
    return {
        "system_name": system_name,
        "total": 0, "valid": 0, "invalid": 0,
        "active_24h": 0, "active_7d": 0, "stale_30d": 0,
        "stale_90d": 0, "inactive_90d": 0,
        "data_no_timestamp": 0, "no_data": 0, "has_real_value": 0,
    }


def build_summary(results: list) -> dict:
    summary = {
        "total_sensors":           len(results),
        "valid_things":            0,
        "invalid_things":          0,
        "active_24h":              0,
        "active_7d":               0,
        "stale_30d":               0,
        "stale_90d":               0,
        "inactive_90d":            0,
        "data_no_timestamp":       0,
        "no_data":                 0,
        "token_or_thing_invalid":  0,
        "has_real_value":          0,
        "missing_thing_token":     0,
        "missing_hos":             0,
        "building_not_found":      0,
        "missing_coords":          0,
        "api_errors":              0,
        "by_system":               {},
        "by_district":             {},
        "by_neighborhood":         {},
    }
    status_map = {
        "ACTIVE_24H":              "active_24h",
        "ACTIVE_7D":               "active_7d",
        "STALE_30D":               "stale_30d",
        "STALE_90D":               "stale_90d",
        "INACTIVE_90D":            "inactive_90d",
        "DATA_NO_TIMESTAMP":       "data_no_timestamp",
        "NO_DATA":                 "no_data",
        "TOKEN_OR_THING_INVALID":  "token_or_thing_invalid",
    }

    for r in results:
        status     = r.get("active_status", "NO_DATA")
        thing_st   = r.get("thing_status", "UNKNOWN")

        summary[status_map.get(status, "no_data")] += 1

        if thing_st == "VALID":
            summary["valid_things"] += 1
        elif thing_st == "TOKEN_OR_THING_INVALID":
            summary["invalid_things"] += 1

        if r.get("has_real_value"):
            summary["has_real_value"] += 1

        issues = r.get("issues", [])
        if "MISSING_THING_TOKEN"      in issues: summary["missing_thing_token"] += 1
        if "MISSING_HOS"              in issues: summary["missing_hos"]         += 1
        if "BUILDING_NOT_FOUND"       in issues: summary["building_not_found"]  += 1
        if "MISSING_COORDS"           in issues: summary["missing_coords"]      += 1
        if "API_ERROR"                in issues: summary["api_errors"]          += 1

        sys_id = r.get("system_id") or "UNKNOWN"
        if sys_id not in summary["by_system"]:
            summary["by_system"][sys_id] = _sys_zero(r.get("system_name", ""))
        s = summary["by_system"][sys_id]
        s["total"] += 1
        if thing_st == "VALID":
            s["valid"] += 1
        elif thing_st == "TOKEN_OR_THING_INVALID":
            s["invalid"] += 1
        if status in status_map:
            key = status_map[status]
            if key in s:
                s[key] += 1
        if r.get("has_real_value"):
            s["has_real_value"] += 1

        dist = r.get("district_name") or "UNKNOWN"
        summary["by_district"].setdefault(dist, 0)
        summary["by_district"][dist] += 1

        neigh = r.get("neighborhood") or "UNKNOWN"
        summary["by_neighborhood"].setdefault(neigh, 0)
        summary["by_neighborhood"][neigh] += 1

    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PIELH FASE 0 - Auditoría IoT TheThings")
    parser.add_argument("--limit",          type=int,   default=None, help="Auditar solo N sensores")
    parser.add_argument("--system",         type=str,   default=None, help="Filtrar por system_id (ej: S01)")
    parser.add_argument("--hos",            type=str,   default=None, help="Filtrar por HOS (ej: HOS001)")
    parser.add_argument("--no-ssl-verify",  action="store_true",      help="Deshabilitar verificación SSL")
    parser.add_argument("--sleep",          type=float, default=0.2,  help="Pausa entre peticiones (s)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent

    print("[PIELH] Cargando configuración...")
    cfg = load_config(base_dir)

    api_base = cfg.get("thethings_api", "").rstrip("/")
    token    = cfg.get("thethings_token", "")

    if not token:
        print("[ERROR] thethings_token no encontrado en config.json")
        return

    print(f"[PIELH] API: {api_base}")
    print("[PIELH] Cargando master JSON...")
    master = load_master(cfg, base_dir)

    sensors   = master.get("sensors", [])
    buildings = master.get("buildings", [])

    # Índice de edificios por HOS
    buildings_by_hos = {b["id"]: b for b in buildings if b.get("id")}

    # Filtros
    if args.system:
        sensors = [s for s in sensors if s.get("system_id") == args.system]
        print(f"[PIELH] Filtro sistema: {args.system} ({len(sensors)} sensores)")
    if args.hos:
        sensors = [s for s in sensors if s.get("hos") == args.hos]
        print(f"[PIELH] Filtro HOS: {args.hos} ({len(sensors)} sensores)")
    if args.limit:
        sensors = sensors[: args.limit]
        print(f"[PIELH] Límite: {args.limit} sensores")

    total = len(sensors)
    print(f"[PIELH] Total sensores a auditar: {total}")

    ssl_ctx = make_ssl_ctx(verify=not args.no_ssl_verify)

    results  = []
    ts_start = datetime.now(timezone.utc)

    for i, sensor in enumerate(sensors, 1):
        sid = sensor.get("id", f"sensor_{i}")
        print(f"  [{i}/{total}] {sid} ...", end=" ", flush=True)

        result = audit_sensor(sensor, api_base, token, ssl_ctx, buildings_by_hos)
        results.append(result)

        status = result["active_status"]
        resource = result.get("resource_detected") or "-"
        days = result.get("days_since_last_data")
        days_str = f"{days:.1f}d" if days is not None else "n/a"
        issues_str = ",".join(result.get("issues", [])) or "ok"
        print(f"{status} | {resource} | {days_str} | {issues_str}")

        if args.sleep > 0:
            time.sleep(args.sleep)

    summary = build_summary(results)

    ts_str   = ts_start.strftime("%Y%m%d_%H%M%S")
    out_dir  = base_dir / "data" / "audits"
    jp, cp, sp = save_outputs(results, summary, out_dir, ts_str)

    sep = "-" * 52
    print(f"\n[PIELH] RESUMEN {sep}")
    print(f"  Total:                   {summary['total_sensors']}")
    print(f"  Things validos:          {summary['valid_things']}")
    print(f"  Things invalidos:        {summary['invalid_things']}")
    print(f"  ACTIVE_24H:              {summary['active_24h']}")
    print(f"  ACTIVE_7D:               {summary['active_7d']}")
    print(f"  STALE_30D:               {summary['stale_30d']}")
    print(f"  STALE_90D:               {summary['stale_90d']}")
    print(f"  INACTIVE_90D:            {summary['inactive_90d']}")
    print(f"  DATA_NO_TIMESTAMP:       {summary['data_no_timestamp']}")
    print(f"  NO_DATA:                 {summary['no_data']}")
    print(f"  TOKEN_OR_THING_INVALID:  {summary['token_or_thing_invalid']}")
    print(f"  Con valor real:          {summary['has_real_value']}")
    print(f"  API_ERRORS:              {summary['api_errors']}")
    print(sep)
    print(f"  JSON:    {jp}")
    print(f"  CSV:     {cp}")
    print(f"  Summary: {sp}")


# ---------------------------------------------------------------------------
# Función reutilizable (importada desde server.py)
# ---------------------------------------------------------------------------

def run_audit(master: dict, api_base: str, token: str, audit_dir: Path,
              sleep: float = 0.1, progress_cb=None):
    """Audita todos los sensores del master contra TheThings.
    Guarda CSV + JSON en audit_dir. Devuelve (results, summary, csv_path).
    progress_cb(done, total, last_result) se llama tras cada sensor."""
    sensors   = master.get("sensors", [])
    buildings = master.get("buildings", [])
    buildings_by_hos = {b["id"]: b for b in buildings if b.get("id")}

    ssl_ctx  = make_ssl_ctx(verify=False)
    results  = []
    ts_start = datetime.now(timezone.utc)
    total    = len(sensors)

    for i, sensor in enumerate(sensors, 1):
        result = audit_sensor(sensor, api_base, token, ssl_ctx, buildings_by_hos)
        results.append(result)
        if progress_cb:
            progress_cb(i, total, result)
        if sleep > 0:
            time.sleep(sleep)

    summary  = build_summary(results)
    ts_str   = ts_start.strftime("%Y%m%d_%H%M%S")
    _, csv_path, _ = save_outputs(results, summary, audit_dir, ts_str)

    return results, summary, csv_path


if __name__ == "__main__":
    main()
