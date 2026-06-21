"""
PIELH - Audit TheThings Structure
Compara pielh_qa_master.json con un snapshot de TheThings (structure_only).
Solo lectura. No modifica ningún archivo de datos.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_duplicates(items, field):
    vals = [item.get(field) for item in items if item.get(field)]
    return [v for v, c in Counter(vals).items() if c > 1]


def main():
    parser = argparse.ArgumentParser(description="PIELH - Audit TheThings Structure")
    parser.add_argument(
        "--snapshot",
        default=None,
        help="Ruta al thethings_structure_only.json (default: data/thethings_snapshots/latest/thethings_structure_only.json)"
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    cfg_path = base_dir / "config.json"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    master_path = base_dir / cfg.get("json_file", "pielh_qa_master.json")
    if not master_path.exists():
        print(f"[ERROR] No encontrado master: {master_path}")
        return 1

    if args.snapshot:
        snap_path = Path(args.snapshot)
    else:
        snap_path = base_dir / "data" / "thethings_snapshots" / "latest" / "thethings_structure_only.json"

    if not snap_path.exists():
        print(f"[ERROR] No encontrado snapshot: {snap_path}")
        print("        Ejecuta primero: python scripts/fetch_thethings_structure.py")
        return 1

    master   = load_json(master_path)
    snapshot = load_json(snap_path)

    m_buildings = master.get("buildings", [])
    m_sensors   = master.get("sensors", [])
    s_buildings = snapshot.get("buildings", [])
    s_sensors   = snapshot.get("sensors", [])
    snap_meta   = snapshot.get("_meta", {})

    m_hos_ids = {b.get("id") for b in m_buildings if b.get("id")}
    s_hos_ids = {b.get("id") for b in s_buildings if b.get("id")}

    m_sensor_ids = {s.get("id") for s in m_sensors if s.get("id")}
    s_sensor_ids = {s.get("id") for s in s_sensors if s.get("id")}

    m_thing_ids_b  = {b.get("thing_id") for b in m_buildings if b.get("thing_id")}
    s_thing_ids_b  = {b.get("thing_id") for b in s_buildings if b.get("thing_id")}
    m_thing_ids_s  = {s.get("thing_id") for s in m_sensors if s.get("thing_id")}
    s_thing_ids_s  = {s.get("thing_id") for s in s_sensors if s.get("thing_id")}

    m_tokens_b = {b.get("thing_token") for b in m_buildings if b.get("thing_token")}
    s_tokens_b = {b.get("thing_token") for b in s_buildings if b.get("thing_token")}
    m_tokens_s = {s.get("thing_token") for s in m_sensors if s.get("thing_token")}
    s_tokens_s = {s.get("thing_token") for s in s_sensors if s.get("thing_token")}

    hos_new        = sorted(s_hos_ids - m_hos_ids)
    hos_missing    = sorted(m_hos_ids - s_hos_ids)
    sensors_new    = sorted(s_sensor_ids - m_sensor_ids)
    sensors_missing = sorted(m_sensor_ids - s_sensor_ids)

    # Duplicados en master
    dup_m_hos        = check_duplicates(m_buildings, "id")
    dup_m_thing_id_b = check_duplicates(m_buildings, "thing_id")
    dup_m_token_b    = check_duplicates(m_buildings, "thing_token")
    dup_m_sensor_id  = check_duplicates(m_sensors, "id")
    dup_m_thing_id_s = check_duplicates(m_sensors, "thing_id")
    dup_m_token_s    = check_duplicates(m_sensors, "thing_token")

    # Duplicados en snapshot
    dup_s_hos        = check_duplicates(s_buildings, "id")
    dup_s_thing_id_b = check_duplicates(s_buildings, "thing_id")
    dup_s_sensor_id  = check_duplicates(s_sensors, "id")
    dup_s_thing_id_s = check_duplicates(s_sensors, "thing_id")

    # Sensores sin HOS
    s_no_hos_master   = [s.get("id") for s in m_sensors if not s.get("hos")]
    s_no_hos_snap     = [s.get("id") for s in s_sensors if not s.get("hos")]

    # Sensores con HOS inexistente en master
    m_hos_set = {b.get("id") for b in m_buildings}
    s_hos_invalido_master = [
        s.get("id") for s in m_sensors
        if s.get("hos") and s.get("hos") not in m_hos_set
    ]
    s_hos_invalido_snap = [
        s.get("id") for s in s_sensors
        if s.get("hos") and s.get("hos") not in s_hos_ids
    ]

    # Resumen por system_id (snapshot)
    by_system = {}
    for s in s_sensors:
        sid = s.get("system_id", "UNKNOWN")
        by_system.setdefault(sid, 0)
        by_system[sid] += 1

    # ---------- Construir resultado ----------
    now = datetime.now().isoformat()
    snap_created = snap_meta.get("created_at", "desconocido")

    result = {
        "_meta": {
            "audit_at":        now,
            "master_path":     str(master_path),
            "snapshot_path":   str(snap_path),
            "snapshot_created": snap_created,
        },
        "counts": {
            "master_buildings":  len(m_buildings),
            "snap_buildings":    len(s_buildings),
            "master_sensors":    len(m_sensors),
            "snap_sensors":      len(s_sensors),
        },
        "diff": {
            "hos_new":           hos_new,
            "hos_missing":       hos_missing,
            "sensors_new":       sensors_new,
            "sensors_missing":   sensors_missing,
        },
        "duplicates_master": {
            "buildings_by_id":        dup_m_hos,
            "buildings_by_thing_id":  dup_m_thing_id_b,
            "buildings_by_token":     dup_m_token_b,
            "sensors_by_id":          dup_m_sensor_id,
            "sensors_by_thing_id":    dup_m_thing_id_s,
            "sensors_by_token":       dup_m_token_s,
        },
        "duplicates_snapshot": {
            "buildings_by_id":        dup_s_hos,
            "buildings_by_thing_id":  dup_s_thing_id_b,
            "sensors_by_id":          dup_s_sensor_id,
            "sensors_by_thing_id":    dup_s_thing_id_s,
        },
        "sensors_without_hos": {
            "master": s_no_hos_master,
            "snapshot": s_no_hos_snap,
        },
        "sensors_with_invalid_hos": {
            "master":   s_hos_invalido_master,
            "snapshot": s_hos_invalido_snap,
        },
        "by_system_id_snapshot": by_system,
    }

    # ---------- Guardar JSON ----------
    snap_dir = snap_path.parent
    out_json = snap_dir / "audit_structure.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ---------- Generar MD ----------
    lines = [
        "# Auditoría estructura TheThings vs Master",
        "",
        f"- Fecha: {now}",
        f"- Master: `{master_path.name}`",
        f"- Snapshot: `{snap_created}`",
        "",
        "## Conteos",
        "",
        f"| Concepto | Master | TheThings |",
        f"|---|---|---|",
        f"| Buildings (HOS) | {len(m_buildings)} | {len(s_buildings)} |",
        f"| Sensors | {len(m_sensors)} | {len(s_sensors)} |",
        "",
        "## Diferencias",
        "",
        f"- HOS nuevos en TheThings (+{len(hos_new)}): " + (", ".join(hos_new) if hos_new else "ninguno"),
        f"- HOS desaparecidos de TheThings (-{len(hos_missing)}): " + (", ".join(hos_missing) if hos_missing else "ninguno"),
        f"- Sensores nuevos en TheThings (+{len(sensors_new)}): " + (f"{len(sensors_new)} sensores" if sensors_new else "ninguno"),
        f"- Sensores desaparecidos de TheThings (-{len(sensors_missing)}): " + (f"{len(sensors_missing)} sensores" if sensors_missing else "ninguno"),
        "",
        "## Duplicados en Master",
        "",
        f"- Buildings por id: {dup_m_hos or 'ninguno'}",
        f"- Buildings por thing_id: {dup_m_thing_id_b or 'ninguno'}",
        f"- Buildings por thing_token: {dup_m_token_b or 'ninguno'}",
        f"- Sensors por id: {len(dup_m_sensor_id)} duplicados",
        f"- Sensors por thing_id: {dup_m_thing_id_s or 'ninguno'}",
        f"- Sensors por thing_token: {dup_m_token_s or 'ninguno'}",
        "",
        "## Duplicados en Snapshot TheThings",
        "",
        f"- Buildings por id: {dup_s_hos or 'ninguno'}",
        f"- Buildings por thing_id: {dup_s_thing_id_b or 'ninguno'}",
        f"- Sensors por id: {len(dup_s_sensor_id)} duplicados",
        f"- Sensors por thing_id: {dup_s_thing_id_s or 'ninguno'}",
        "",
        "## Sensores sin HOS",
        "",
        f"- Master: {len(s_no_hos_master)}",
        f"- Snapshot: {len(s_no_hos_snap)}",
        "",
        "## Sensores con HOS inexistente",
        "",
        f"- Master: {len(s_hos_invalido_master)}",
        f"- Snapshot: {len(s_hos_invalido_snap)}",
        "",
        "## Por system_id (Snapshot)",
        "",
        "| System | Sensores |",
        "|---|---|",
    ]
    for sid, cnt in sorted(by_system.items()):
        lines.append(f"| {sid} | {cnt} |")

    if sensors_new:
        lines += ["", "## Sensores nuevos en TheThings (muestra, max 50)", ""]
        for s in sensors_new[:50]:
            lines.append(f"- {s}")

    if sensors_missing:
        lines += ["", "## Sensores desaparecidos de TheThings (muestra, max 50)", ""]
        for s in sensors_missing[:50]:
            lines.append(f"- {s}")

    out_md = snap_dir / "audit_structure.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")

    # ---------- Consola ----------
    print(f"[PIELH] Auditoría completada: {now}")
    print(f"        Master     : buildings={len(m_buildings)}, sensors={len(m_sensors)}")
    print(f"        TheThings  : buildings={len(s_buildings)}, sensors={len(s_sensors)}")
    print(f"        HOS nuevos : {len(hos_new)}")
    print(f"        HOS falta  : {len(hos_missing)}")
    print(f"        Sens nuevos: {len(sensors_new)}")
    print(f"        Sens falta : {len(sensors_missing)}")
    print(f"[OK] {out_json}")
    print(f"[OK] {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
