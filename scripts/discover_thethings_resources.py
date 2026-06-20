"""
PIELH FASE 0 - Descubrimiento de recursos IoT TheThings
Solo lectura. No modifica pielh_qa_master.json.

Endpoint descubierto:
  GET /v2/things/{thing_token}/resources
  -> {"status": "success", "resources": ["co2", "temperature", ...]}
"""

import json
import csv
import ssl
import time
import random
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Tuple
from collections import defaultdict

# Heurística de tipo por nombre de recurso
_TYPE_PATTERNS = {
    "numeric":  [
        "temperature", "humidity", "co2", "co", "no", "no2", "o3", "pm",
        "pressure", "noise", "db", "laeq", "energy", "power", "kwh", "voltage",
        "current", "flow", "volume", "water", "battery", "level", "count",
        "occupancy", "passengers", "speed", "value", "val", "index", "num",
        "avg", "max", "min", "sum", "total", "m3", "liters", "consumption",
        "radon", "gas", "smoke", "flood", "rain", "wind", "solar", "uv",
        "luminosity", "lux", "radiation",
    ],
    "boolean":  ["alarm", "alert", "status", "on", "off", "open", "closed",
                 "motion", "presence", "occupied", "door", "window", "leak"],
    "string":   ["description", "payload", "error", "id", "name", "label",
                 "ctm_payload", "ctm_error"],
}


def infer_type(resource_name: str) -> str:
    name_lower = resource_name.lower()
    for rtype, patterns in _TYPE_PATTERNS.items():
        if any(p in name_lower for p in patterns):
            return rtype
    return "unknown"


# ---------------------------------------------------------------------------
# Config + master
# ---------------------------------------------------------------------------

def load_config(base_dir: Path) -> dict:
    with open(base_dir / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_master(cfg: dict, base_dir: Path) -> dict:
    with open(base_dir / cfg["json_file"], "r", encoding="utf-8") as f:
        return json.load(f)


def make_ssl_ctx(verify: bool) -> ssl.SSLContext:
    return ssl._create_unverified_context() if not verify else ssl.create_default_context()


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

def fetch_resources(api_base: str, token: str, thing_token: str,
                    ssl_ctx: ssl.SSLContext, timeout: int = 15) -> Tuple[Optional[List[str]], str]:
    """
    Returns (resource_list, error_msg).
    resource_list is None on error.
    """
    url = f"{api_base}/v2/things/{thing_token}/resources"
    req = urllib.request.Request(url, headers={"authorization": token})
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            resources = data.get("resources")
            if isinstance(resources, list):
                return resources, ""
            return None, f"unexpected format: {list(data.keys())}"
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        reason = str(e.reason) if hasattr(e, "reason") else str(e)
        return None, f"URLError: {reason}"
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def discover(sensors: list, api_base: str, token: str,
             ssl_ctx: ssl.SSLContext, sample_size: int,
             sleep_secs: float) -> Tuple[list, dict]:
    """
    Returns:
      rows     — list of dicts for CSV/JSON (one row per sensor×resource)
      summary  — dict per system_id with aggregate info
    """
    # Group by system
    by_system: dict = defaultdict(list)
    for s in sensors:
        sys_id = s.get("system_id") or "UNKNOWN"
        by_system[sys_id].append(s)

    rows: list = []
    summary: dict = {}

    systems_sorted = sorted(by_system.keys())
    total_systems  = len(systems_sorted)

    for idx, sys_id in enumerate(systems_sorted, 1):
        group     = by_system[sys_id]
        sys_name  = group[0].get("system_name", "")
        pool      = [s for s in group if s.get("thing_token")]
        sampled   = random.sample(pool, min(sample_size, len(pool))) if pool else []

        print(f"[{idx}/{total_systems}] {sys_id} {sys_name} — {len(group)} sensores, {len(sampled)} muestras")

        sys_resources: set = set()
        sensors_ok    = 0
        sensors_err   = 0

        for s in sampled:
            tt = s["thing_token"]
            resource_list, error = fetch_resources(api_base, token, tt, ssl_ctx)

            if resource_list is None:
                print(f"  ERROR {s.get('id', '?')[:40]} — {error}")
                sensors_err += 1
            else:
                sensors_ok += 1
                sys_resources.update(resource_list)
                for res in resource_list:
                    rows.append({
                        "system_id":     sys_id,
                        "system_name":   sys_name,
                        "thing_id":      s.get("thing_id", ""),
                        "thing_token":   tt,
                        "resource_name": res,
                        "resource_type": infer_type(res),
                        "resource_key":  res,
                    })

            if sleep_secs > 0:
                time.sleep(sleep_secs)

        resources_list = sorted(sys_resources)
        summary[sys_id] = {
            "system_id":         sys_id,
            "system_name":       sys_name,
            "total_sensors":     len(group),
            "sampled":           len(sampled),
            "sensors_ok":        sensors_ok,
            "sensors_err":       sensors_err,
            "resource_count":    len(resources_list),
            "resources_detected": resources_list,
        }

        if resources_list:
            print(f"  -> {len(resources_list)} recursos: {', '.join(resources_list[:8])}"
                  + (" ..." if len(resources_list) > 8 else ""))
        else:
            print("  -> sin recursos detectados")

    return rows, summary


def build_resource_candidates(summary: dict) -> dict:
    """Genera un diccionario RESOURCE_CANDIDATES listo para copiar al script de auditoría."""
    candidates: dict = {}
    for sys_id, info in sorted(summary.items()):
        res = info.get("resources_detected", [])
        if res:
            # Excluir recursos de metadatos internos / estadísticos medios
            primary = [r for r in res if not any(
                r.endswith(sfx) for sfx in ("_avg_d", "_avg_h", "_avg_w", "_max", "_min")
            )]
            candidates[sys_id] = primary or res
    return candidates


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

CSV_COLUMNS = ["system_id", "system_name", "thing_id", "thing_token",
               "resource_name", "resource_type", "resource_key"]

SUMMARY_CSV_COLUMNS = ["system_id", "system_name", "total_sensors",
                        "sampled", "sensors_ok", "sensors_err",
                        "resource_count", "resources_detected"]


def save_outputs(rows: list, summary: dict, candidates: dict,
                 out_dir: Path, ts_str: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON completo (rows + summary + candidates)
    json_path = out_dir / f"resource_discovery_{ts_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at":      ts_str,
            "total_rows":        len(rows),
            "resource_candidates": candidates,
            "summary":           list(summary.values()),
            "rows":              rows,
        }, f, ensure_ascii=False, indent=2)

    # CSV detalle (una fila por sensor x recurso)
    csv_path = out_dir / f"resource_discovery_{ts_str}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    # CSV summary (una fila por sistema)
    summary_csv_path = out_dir / f"resource_discovery_summary_{ts_str}.csv"
    with open(summary_csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for info in sorted(summary.values(), key=lambda x: x["system_id"]):
            row = dict(info)
            row["resources_detected"] = "; ".join(info.get("resources_detected", []))
            writer.writerow(row)

    return json_path, csv_path, summary_csv_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PIELH FASE 0 - Descubrimiento de recursos IoT TheThings"
    )
    parser.add_argument("--sample",        type=int,   default=10,
                        help="Sensores a muestrear por sistema (default: 10)")
    parser.add_argument("--system",        type=str,   default=None,
                        help="Auditar solo un sistema (ej: S06)")
    parser.add_argument("--no-ssl-verify", action="store_true",
                        help="Deshabilitar verificacion SSL")
    parser.add_argument("--sleep",         type=float, default=0.1,
                        help="Pausa entre peticiones en segundos (default: 0.1)")
    parser.add_argument("--seed",          type=int,   default=42,
                        help="Semilla para seleccion aleatoria reproducible (default: 42)")
    args = parser.parse_args()

    random.seed(args.seed)

    base_dir = Path(__file__).resolve().parent.parent
    cfg      = load_config(base_dir)
    api_base = cfg.get("thethings_api", "").rstrip("/")
    token    = cfg.get("thethings_token", "")

    if not token:
        print("[ERROR] thethings_token no encontrado en config.json")
        return

    print(f"[PIELH] API: {api_base}")
    master   = load_master(cfg, base_dir)
    sensors  = master.get("sensors", [])

    if args.system:
        sensors = [s for s in sensors if s.get("system_id") == args.system]
        print(f"[PIELH] Filtro sistema: {args.system} ({len(sensors)} sensores)")

    print(f"[PIELH] Total sensores: {len(sensors)} | muestra/sistema: {args.sample}")

    ssl_ctx  = make_ssl_ctx(verify=not args.no_ssl_verify)
    ts_start = datetime.now(timezone.utc)

    rows, summary = discover(
        sensors, api_base, token, ssl_ctx,
        sample_size=args.sample,
        sleep_secs=args.sleep,
    )

    candidates = build_resource_candidates(summary)

    ts_str  = ts_start.strftime("%Y%m%d_%H%M%S")
    out_dir = base_dir / "data" / "audits"
    jp, cp, sp = save_outputs(rows, summary, candidates, out_dir, ts_str)

    # Imprimir RESOURCE_CANDIDATES generado
    sep = "-" * 52
    print(f"\n[PIELH] RESOURCE_CANDIDATES SUGERIDO {sep}")
    print("RESOURCE_CANDIDATES = {")
    for sys_id, res_list in sorted(candidates.items()):
        print(f'    "{sys_id}": {json.dumps(res_list)},')
    print("}")
    print(sep)
    print(f"\n[PIELH] RESUMEN POR SISTEMA:")
    for sys_id, info in sorted(summary.items()):
        ok  = info["sensors_ok"]
        err = info["sensors_err"]
        n   = info["resource_count"]
        print(f"  {sys_id:6} {info['system_name']:30} {ok}/{info['sampled']} OK  {n} recursos")

    print(f"\n  JSON:    {jp}")
    print(f"  CSV:     {cp}")
    print(f"  Summary: {sp}")


if __name__ == "__main__":
    main()
