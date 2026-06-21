"""
PIELH - Fase 3: Auditoría de salud de datos IoT
Solo lectura. No modifica pielh_qa_master.json.

Prerequisito: ejecutar primero scripts/discover_thethings_resources.py --no-ssl-verify
"""

import json
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict


def parse_timestamp(ts_str):
    if not ts_str:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def classify_days(days):
    if days is None:
        return "NO_DATA"
    if days <= 1:
        return "ACTIVE_24H"
    if days <= 7:
        return "ACTIVE_7D"
    if days <= 30:
        return "ACTIVE_30D"
    return "STALE_30D"


def pct(n, total):
    return f"{n/total*100:.1f}%" if total else "—"


def main():
    parser = argparse.ArgumentParser(description="PIELH - Fase 3: Auditoría de salud de datos IoT")
    parser.add_argument(
        "--snapshot", default=None,
        help="Ruta al thethings_resources_probe.json "
             "(default: data/thethings_snapshots/latest/thethings_resources_probe.json)"
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    cfg_path = base_dir / "config.json"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    if args.snapshot:
        snap_path = Path(args.snapshot)
    else:
        snap_path = (base_dir / "data" / "thethings_snapshots"
                     / "latest" / "thethings_resources_probe.json")

    if not snap_path.exists():
        print(f"[ERROR] No encontrado: {snap_path}")
        print("        Ejecuta primero: python scripts/discover_thethings_resources.py --no-ssl-verify")
        return 1

    probe = json.loads(snap_path.read_text(encoding="utf-8"))
    meta  = probe.get("_meta", {})
    sensors = probe.get("sensors", [])

    now_utc = datetime.now(timezone.utc)

    # ---------- Enriquecer sensores con cálculo de días ----------
    enriched = []
    for s in sensors:
        # Mejor timestamp disponible: primero last_seen del probe, luego platform_last_seen
        best_ts_str = s.get("last_seen") or s.get("platform_last_seen")
        best_dt     = parse_timestamp(best_ts_str)
        days        = round((now_utc - best_dt).total_seconds() / 86400, 2) if best_dt else None
        enriched.append({
            **s,
            "_days_since_data": days,
            "_status":          classify_days(days),
        })

    # ---------- Estadísticas globales ----------
    total_processed = len(enriched)
    with_any        = sum(1 for s in enriched if s.get("has_any_resource"))
    with_data       = sum(1 for s in enriched if s.get("has_real_data"))
    no_data         = sum(1 for s in enriched if not s.get("has_real_data"))
    with_error      = sum(1 for s in enriched if s.get("errors_count", 0) > 0)
    active_24h      = sum(1 for s in enriched if s["_status"] == "ACTIVE_24H")
    active_7d       = sum(1 for s in enriched if s["_status"] in ("ACTIVE_24H", "ACTIVE_7D"))
    active_30d      = sum(1 for s in enriched if s["_status"] in ("ACTIVE_24H", "ACTIVE_7D", "ACTIVE_30D"))
    stale_30d       = sum(1 for s in enriched if s["_status"] == "STALE_30D")
    no_last_seen    = sum(1 for s in enriched if not s.get("last_seen") and not s.get("platform_last_seen"))

    # Recursos únicos encontrados
    all_resources = set()
    for s in enriched:
        for r in s.get("resources", []):
            if r.get("exists"):
                all_resources.add(r["resource"])

    # Última lectura global
    global_last_seen_dt = None
    global_last_seen    = None
    for s in enriched:
        dt = parse_timestamp(s.get("last_seen"))
        if dt and (global_last_seen_dt is None or dt > global_last_seen_dt):
            global_last_seen_dt = dt
            global_last_seen    = s.get("last_seen")

    # ---------- Por sistema ----------
    by_system = defaultdict(lambda: {
        "sensors_processed": 0, "sensors_with_data": 0,
        "sensors_no_data": 0, "sensors_error": 0,
        "active_24h": 0, "active_7d": 0, "active_30d": 0, "stale_30d": 0,
        "resources_found": set(),
        "last_seen": None, "last_seen_dt": None,
        "system_name": "",
        "sensors_no_last_seen": 0,
    })

    for s in enriched:
        sid    = s.get("system_id", "UNKNOWN")
        ss     = by_system[sid]
        ss["sensors_processed"] += 1
        ss["system_name"] = s.get("system_name", ss["system_name"])

        if s.get("has_real_data"):
            ss["sensors_with_data"] += 1
            dt = parse_timestamp(s.get("last_seen"))
            if dt and (ss["last_seen_dt"] is None or dt > ss["last_seen_dt"]):
                ss["last_seen_dt"] = dt
                ss["last_seen"]    = s.get("last_seen")
        else:
            ss["sensors_no_data"] += 1

        if s.get("errors_count", 0) > 0:
            ss["sensors_error"] += 1

        status = s["_status"]
        if status == "ACTIVE_24H":
            ss["active_24h"] += 1
            ss["active_7d"]  += 1
            ss["active_30d"] += 1
        elif status == "ACTIVE_7D":
            ss["active_7d"]  += 1
            ss["active_30d"] += 1
        elif status == "ACTIVE_30D":
            ss["active_30d"] += 1
        elif status == "STALE_30D":
            ss["stale_30d"]  += 1

        if not s.get("last_seen") and not s.get("platform_last_seen"):
            ss["sensors_no_last_seen"] += 1

        for r in s.get("resources", []):
            if r.get("exists"):
                ss["resources_found"].add(r["resource"])

    # Serializar (sets → listas, eliminar last_seen_dt)
    by_system_out = {}
    for sid, info in sorted(by_system.items()):
        resources = sorted(info["resources_found"])
        primary   = resources[0] if resources else None
        by_system_out[sid] = {
            "system_name":       info["system_name"],
            "sensors_processed": info["sensors_processed"],
            "sensors_with_data": info["sensors_with_data"],
            "sensors_no_data":   info["sensors_no_data"],
            "sensors_error":     info["sensors_error"],
            "pct_with_data":     pct(info["sensors_with_data"], info["sensors_processed"]),
            "active_24h":        info["active_24h"],
            "active_7d":         info["active_7d"],
            "active_30d":        info["active_30d"],
            "stale_30d":         info["stale_30d"],
            "sensors_no_last_seen": info["sensors_no_last_seen"],
            "resources_found":   resources,
            "primary_resource":  primary,
            "last_seen":         info["last_seen"],
        }

    # ---------- Listas adicionales ----------
    top_active = sorted(
        [s for s in enriched if s.get("has_real_data") and s.get("last_seen")],
        key=lambda s: s.get("last_seen", ""),
        reverse=True,
    )[:20]

    sensors_no_data_by_sys = defaultdict(list)
    for s in enriched:
        if not s.get("has_real_data"):
            sensors_no_data_by_sys[s.get("system_id", "?")].append(s.get("id", "?"))

    sensors_errors_by_sys = defaultdict(list)
    for s in enriched:
        if s.get("errors_count", 0) > 0:
            sensors_errors_by_sys[s.get("system_id", "?")].append(s.get("id", "?"))

    # ---------- Resultado JSON ----------
    now = datetime.now().isoformat()
    result = {
        "_meta": {
            "audit_at":         now,
            "snapshot_path":    str(snap_path),
            "probe_created_at": meta.get("created_at", "?"),
            "sensors_in_probe": meta.get("sensors_processed", len(sensors)),
        },
        "summary": {
            "sensors_processed":    total_processed,
            "sensors_with_resource": with_any,
            "sensors_with_data":    with_data,
            "sensors_no_data":      no_data,
            "sensors_with_error":   with_error,
            "unique_resources":     sorted(all_resources),
            "unique_resources_count": len(all_resources),
            "global_last_seen":     global_last_seen,
            "active_24h":           active_24h,
            "active_7d":            active_7d,
            "active_30d":           active_30d,
            "stale_30d":            stale_30d,
            "no_last_seen":         no_last_seen,
        },
        "by_system": by_system_out,
        "top_active_sensors": [
            {"id": s["id"], "system_id": s.get("system_id"), "last_seen": s.get("last_seen")}
            for s in top_active
        ],
        "sensors_no_data_by_system": {k: v for k, v in sensors_no_data_by_sys.items()},
        "sensors_errors_by_system":  {k: v for k, v in sensors_errors_by_sys.items()},
    }

    # ---------- Guardar JSON timestamped ----------
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = base_dir / "data" / "thethings_snapshots" / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "audit_data_health.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- Generar MD ----------
    summ = result["summary"]
    lines = [
        "# Auditoría Salud de Datos IoT — Fase 3",
        "",
        f"- Fecha: {now}",
        f"- Snapshot probe: `{meta.get('created_at', '?')}`",
        "",
        "## Resumen general",
        "",
        "| Concepto | Valor |",
        "|---|---|",
        f"| Sensores procesados | {summ['sensors_processed']} |",
        f"| Con al menos 1 recurso válido | {summ['sensors_with_resource']} ({pct(summ['sensors_with_resource'], summ['sensors_processed'])}) |",
        f"| Con datos reales | {summ['sensors_with_data']} ({pct(summ['sensors_with_data'], summ['sensors_processed'])}) |",
        f"| Sin datos | {summ['sensors_no_data']} |",
        f"| Con error API | {summ['sensors_with_error']} |",
        f"| Recursos únicos encontrados | {summ['unique_resources_count']} |",
        f"| Última lectura global | {summ['global_last_seen'] or '—'} |",
        f"| Activos últimas 24h | {summ['active_24h']} |",
        f"| Activos últimos 7 días | {summ['active_7d']} |",
        f"| Activos últimos 30 días | {summ['active_30d']} |",
        f"| Inactivos >30 días | {summ['stale_30d']} |",
        f"| Sin ningún timestamp | {summ['no_last_seen']} |",
        "",
        "## Recursos únicos detectados",
        "",
        ", ".join(sorted(all_resources)) if all_resources else "—",
        "",
        "## Resumen por sistema",
        "",
        "| Sistema | Nombre | Procesados | Con datos | % | 24h | 7d | 30d | Recursos | Último dato |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, info in sorted(by_system_out.items()):
        resources_str = ", ".join(info["resources_found"][:4])
        if len(info["resources_found"]) > 4:
            resources_str += f" (+{len(info['resources_found'])-4})"
        lines.append(
            f"| {sid} | {info['system_name']} | {info['sensors_processed']} | "
            f"{info['sensors_with_data']} | {info['pct_with_data']} | "
            f"{info['active_24h']} | {info['active_7d']} | {info['active_30d']} | "
            f"{resources_str or '—'} | {info['last_seen'] or '—'} |"
        )

    lines += [
        "",
        "## Top sensores activos recientes (máx. 20)",
        "",
        "| Sensor | Sistema | Última lectura |",
        "|---|---|---|",
    ]
    for s in result["top_active_sensors"]:
        lines.append(f"| {s['id']} | {s['system_id']} | {s['last_seen']} |")

    lines += ["", "## Sensores sin datos por sistema", ""]
    for sid in sorted(sensors_no_data_by_sys):
        lst = sensors_no_data_by_sys[sid]
        lines.append(f"**{sid}** ({len(lst)} sensores):")
        for sid_item in lst[:10]:
            lines.append(f"- {sid_item}")
        if len(lst) > 10:
            lines.append(f"  _(y {len(lst)-10} más — ver audit_data_health.json)_")

    if sensors_errors_by_sys:
        lines += ["", "## Sensores con errores API", ""]
        for sid in sorted(sensors_errors_by_sys):
            lst = sensors_errors_by_sys[sid]
            lines.append(f"**{sid}** ({len(lst)} sensores):")
            for sid_item in lst[:10]:
                lines.append(f"- {sid_item}")

    out_md = out_dir / "audit_data_health.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")

    # Copiar a latest
    latest_dir = base_dir / "data" / "thethings_snapshots" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_json, latest_dir / "audit_data_health.json")
    shutil.copy2(out_md,   latest_dir / "audit_data_health.md")

    # Consola
    print(f"[PIELH] Auditoría completada: {now}")
    print(f"        Procesados  : {total_processed}")
    print(f"        Con datos   : {with_data} ({pct(with_data, total_processed)})")
    print(f"        Sin datos   : {no_data}")
    print(f"        Con errores : {with_error}")
    print(f"        Activos 24h : {active_24h}")
    print(f"        Activos 7d  : {active_7d}")
    print(f"        Activos 30d : {active_30d}")
    print(f"        Stale >30d  : {stale_30d}")
    print(f"        Recursos    : {len(all_resources)} únicos")
    print(f"[OK] {out_json}")
    print(f"[OK] {out_md}")
    print(f"[OK] {latest_dir / 'audit_data_health.json'}")
    print(f"[OK] {latest_dir / 'audit_data_health.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
