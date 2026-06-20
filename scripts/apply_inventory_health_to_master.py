"""
PIELH FASE 0 - Enriquecimiento IoT del inventario master
Lee pielh_qa_master.json + ultimo CSV de auditoria + inventory_health_report.json.
Anade iot_health a cada sensor y agrega contadores IoT por edificio.
Hace backup antes de modificar.
"""

import json
import csv
import shutil
import argparse
from datetime import datetime
from pathlib import Path


DEMO_READY_STATUSES = {"ACTIVE_24H", "ACTIVE_7D"}


def find_latest_audit_csv(audit_dir: Path) -> Path:
    files = sorted(audit_dir.glob("thethings_activity_[0-9]*.csv"), reverse=True)
    if not files:
        raise FileNotFoundError(f"No se encontro CSV de auditoria en {audit_dir}")
    return files[0]


def load_config(base_dir: Path) -> dict:
    with open(base_dir / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_master(json_path: Path) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_audit_csv(csv_path: Path) -> dict:
    """Devuelve dict keyed by thing_token."""
    result = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            tt = row.get("thing_token", "").strip()
            if tt:
                result[tt] = row
    return result


def load_sys_class(report_path: Path) -> dict:
    """Devuelve dict: system_id -> class (A/B/C)."""
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    return {
        sid: info.get("class", "?")
        for sid, info in report.get("systems_detail", {}).items()
    }


def make_backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"pielh_qa_master_{ts}.json"
    shutil.copy2(master_path, dst)
    return dst


def build_iot_health(row: dict, sys_class: dict, health_source: str) -> dict:
    status     = (row.get("active_status") or "").strip() or "NO_DATA"
    has_real   = (row.get("has_real_value") or "").strip().lower() in ("true", "1", "yes")
    demo_ready = status in DEMO_READY_STATUSES
    last_seen  = (row.get("last_timestamp") or "").strip() or None
    resource   = (row.get("resource_detected") or "").strip() or None
    s_class    = sys_class.get((row.get("system_id") or "").strip(), "?")
    return {
        "status":        status,
        "has_real_data": has_real,
        "demo_ready":    demo_ready,
        "last_seen":     last_seen,
        "resource":      resource,
        "system_class":  s_class,
        "health_source": health_source,
    }


def main():
    parser = argparse.ArgumentParser(
        description="PIELH - Enriquecimiento IoT del inventario master"
    )
    parser.add_argument("--csv",      type=str, default=None,
                        help="Ruta al CSV de auditoria (por defecto: ultimo generado)")
    parser.add_argument("--report",   type=str, default=None,
                        help="Ruta a inventory_health_report.json")
    parser.add_argument("--dry-run",  action="store_true",
                        help="No modificar ficheros, solo mostrar resumen")
    args = parser.parse_args()

    base_dir  = Path(__file__).resolve().parent.parent
    audit_dir = base_dir / "data" / "audits"
    cfg       = load_config(base_dir)

    master_path = base_dir / cfg["json_file"]
    backup_dir  = base_dir / cfg.get("backup_dir", "data/backups")

    csv_path    = Path(args.csv)    if args.csv    else find_latest_audit_csv(audit_dir)
    report_path = Path(args.report) if args.report else audit_dir / "inventory_health_report.json"

    print(f"[IoT] Master:        {master_path.name}")
    print(f"[IoT] CSV auditoria: {csv_path.name}")
    print(f"[IoT] Health report: {report_path.name}")

    audit_by_token = load_audit_csv(csv_path)
    sys_class      = load_sys_class(report_path)
    master         = load_master(master_path)

    health_source = csv_path.name
    sensors   = master.get("sensors", [])
    buildings = master.get("buildings", [])

    # --- Enriquecer sensores ---
    matched   = 0
    unmatched = 0
    for s in sensors:
        tt  = s.get("thing_token", "")
        row = audit_by_token.get(tt)
        if row:
            s["iot_health"] = build_iot_health(row, sys_class, health_source)
            matched += 1
        else:
            s["iot_health"] = {
                "status":        "NOT_AUDITED",
                "has_real_data": False,
                "demo_ready":    False,
                "last_seen":     None,
                "resource":      None,
                "system_class":  sys_class.get(s.get("system_id", ""), "?"),
                "health_source": health_source,
            }
            unmatched += 1

    # --- Agregar por edificio (via campo 'hos') ---
    sensors_by_hos: dict = {}
    for s in sensors:
        hos = s.get("hos", "")
        if hos:
            sensors_by_hos.setdefault(hos, []).append(s)

    bld_updated    = 0
    bld_active     = 0
    for b in buildings:
        bld_sensors = sensors_by_hos.get(b.get("id", ""), [])
        total  = len(bld_sensors)
        active = sum(1 for s in bld_sensors
                     if s.get("iot_health", {}).get("demo_ready", False))

        if total == 0:
            iot_status = "NO_SENSORS"
        elif active > 0:
            iot_status = "ACTIVE"
        else:
            iot_status = "NO_DATA"

        b["iot_total_sensors"]  = total
        b["iot_active_sensors"] = active
        b["iot_demo_ready"]     = active
        b["iot_health_status"]  = iot_status
        bld_updated += 1
        if iot_status == "ACTIVE":
            bld_active += 1

    # --- Resumen ---
    demo_sensors = sum(1 for s in sensors
                       if s.get("iot_health", {}).get("demo_ready", False))

    print(f"[IoT] Sensores totales:       {len(sensors)}")
    print(f"[IoT]   con match CSV:        {matched}")
    print(f"[IoT]   sin match:            {unmatched}")
    print(f"[IoT]   demo_ready:           {demo_sensors}")
    print(f"[IoT] Edificios actualizados: {bld_updated}")
    print(f"[IoT]   con sensores activos: {bld_active}")

    if args.dry_run:
        print("[IoT] --dry-run: no se modifican ficheros.")
        return

    backup_path = make_backup(master_path, backup_dir)
    print(f"[IoT] Backup:   {backup_path.name}")

    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"[IoT] Guardado: {master_path.name}")


if __name__ == "__main__":
    main()
