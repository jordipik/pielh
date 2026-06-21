"""
PIELH - Informe de depuracion de sensores (Fase 4)
Solo lectura. No modifica pielh_qa_master.json.

Cruza:
  - pielh_qa_master.json       -> building_name por hos
  - thethings_resources_probe.json -> has_real_data, last_seen, recursos
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def main():
    base_dir = Path(__file__).resolve().parent.parent
    cfg_path = base_dir / "config.json"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    master_path = base_dir / cfg.get("json_file", "pielh_qa_master.json")
    probe_path  = base_dir / "data" / "thethings_snapshots" / "latest" / "thethings_resources_probe.json"

    if not master_path.exists():
        print(f"[ERROR] No encontrado: {master_path}")
        return 1
    if not probe_path.exists():
        print(f"[ERROR] No encontrado: {probe_path}")
        print("        Ejecuta primero: python scripts/discover_thethings_resources.py --no-ssl-verify")
        return 1

    master = json.loads(master_path.read_text(encoding="utf-8"))
    probe  = json.loads(probe_path.read_text(encoding="utf-8"))

    # Indice buildings: hos -> name
    buildings_idx = {
        b["id"]: b.get("name", b["id"])
        for b in master.get("buildings", [])
        if b.get("id")
    }

    # Indice master sensors: id -> building_name resuelto
    master_sensor_idx = {}
    for s in master.get("sensors", []):
        sid = s.get("id")
        if not sid:
            continue
        bn = s.get("building_name") or buildings_idx.get(s.get("hos", ""), "")
        master_sensor_idx[sid] = bn

    probe_sensors = probe.get("sensors", [])
    probe_meta    = probe.get("_meta", {})

    # Clasificar sensores
    with_data      = []
    without_data   = []
    resource_no_sample = []

    for s in probe_sensors:
        sid     = s.get("id", "")
        hos     = s.get("hos") or ""
        sys_id  = s.get("system_id", "")
        sys_name = s.get("system_name", "")
        last_seen = s.get("last_seen") or s.get("platform_last_seen") or ""
        bn      = master_sensor_idx.get(sid) or buildings_idx.get(hos, "")
        resources = s.get("resources", [])

        if s.get("has_real_data"):
            detected = next(
                (r["resource"] for r in resources if r.get("has_data")),
                ""
            )
            with_data.append({
                "id":            sid,
                "hos":           hos,
                "building_name": bn,
                "system_id":     sys_id,
                "last_seen":     last_seen,
                "resource":      detected,
            })
        else:
            # Determinar motivo
            has_any  = s.get("has_any_resource")
            err_cnt  = s.get("errors_count", 0)
            exists_any = any(r.get("exists") for r in resources)

            if err_cnt > 0 and not exists_any:
                motivo = "ERROR"
            elif not exists_any:
                motivo = "NO_RESOURCE"
            else:
                motivo = "NO_DATA"

            without_data.append({
                "id":            sid,
                "hos":           hos,
                "building_name": bn,
                "system_id":     sys_id,
                "motivo":        motivo,
            })

            # Sub-caso: recurso existe pero sin muestras
            exists_list = [r["resource"] for r in resources if r.get("exists")]
            if exists_list:
                resource_no_sample.append({
                    "id":              sid,
                    "hos":             hos,
                    "system_id":       sys_id,
                    "recursos_existentes": exists_list,
                })

    # Resumen por sistema
    by_system = defaultdict(lambda: {"total": 0, "con_datos": 0, "sin_datos": 0, "system_name": ""})
    for s in probe_sensors:
        sid = s.get("system_id", "?")
        by_system[sid]["total"] += 1
        by_system[sid]["system_name"] = s.get("system_name", "")
        if s.get("has_real_data"):
            by_system[sid]["con_datos"] += 1
        else:
            by_system[sid]["sin_datos"] += 1

    by_system_out = {}
    for sid, info in sorted(by_system.items()):
        total = info["total"]
        cd    = info["con_datos"]
        by_system_out[sid] = {
            "system_name": info["system_name"],
            "total":       total,
            "con_datos":   cd,
            "sin_datos":   info["sin_datos"],
            "pct_util":    f"{cd/total*100:.1f}%" if total else "—",
        }

    # Resumen por edificio
    by_hos = defaultdict(lambda: {"building_name": "", "total": 0, "con_datos": 0, "sin_datos": 0})
    for s in with_data:
        h = s["hos"] or "SIN_HOS"
        by_hos[h]["building_name"] = s["building_name"]
        by_hos[h]["total"]    += 1
        by_hos[h]["con_datos"] += 1
    for s in without_data:
        h = s["hos"] or "SIN_HOS"
        by_hos[h]["building_name"] = s["building_name"]
        by_hos[h]["total"]    += 1
        by_hos[h]["sin_datos"] += 1

    by_hos_out = {
        h: info for h, info in sorted(by_hos.items())
    }

    # Resultado JSON
    now = datetime.now().isoformat()
    result = {
        "_meta": {
            "generated_at":   now,
            "probe_created":  probe_meta.get("created_at", "?"),
            "master_path":    str(master_path),
            "master_modified": False,
        },
        "summary": {
            "total_sensors":        len(probe_sensors),
            "with_data":            len(with_data),
            "without_data":         len(without_data),
            "resource_exists_no_sample": len(resource_no_sample),
        },
        "sensors_with_data":            with_data,
        "sensors_without_data":         without_data,
        "sensors_resource_no_sample":   resource_no_sample,
        "by_system":                    by_system_out,
        "by_hos":                       by_hos_out,
    }

    # Generar MD
    def pct_str(n, t):
        return f"{n/t*100:.1f}%" if t else "—"

    total = len(probe_sensors)
    lines = [
        "# Informe de depuracion de sensores IoT",
        "",
        f"- Generado: {now}",
        f"- Probe base: `{probe_meta.get('created_at', '?')}`",
        f"- Sensores procesados: {total}",
        "",
        "## Resumen",
        "",
        "| Concepto | Valor |",
        "|---|---|",
        f"| Total sensores | {total} |",
        f"| Con datos reales | {len(with_data)} ({pct_str(len(with_data), total)}) |",
        f"| Sin datos | {len(without_data)} ({pct_str(len(without_data), total)}) |",
        f"| Recurso existe pero sin muestras | {len(resource_no_sample)} |",
        "",
        "## Resumen por sistema",
        "",
        "| Sistema | Nombre | Total | Con datos | Sin datos | % util |",
        "|---|---|---|---|---|---|",
    ]
    for sid, info in sorted(by_system_out.items()):
        lines.append(
            f"| {sid} | {info['system_name']} | {info['total']} | "
            f"{info['con_datos']} | {info['sin_datos']} | {info['pct_util']} |"
        )

    lines += [
        "",
        "## Resumen por edificio (HOS con al menos 1 sensor)",
        "",
        "| HOS | Nombre edificio | Total | Con datos | Sin datos |",
        "|---|---|---|---|---|",
    ]
    for h, info in sorted(by_hos_out.items()):
        bn = (info["building_name"] or "")[:50]
        lines.append(
            f"| {h} | {bn} | {info['total']} | {info['con_datos']} | {info['sin_datos']} |"
        )

    lines += [
        "",
        f"## Sensores con datos reales ({len(with_data)})",
        "",
        "| id | HOS | Edificio | Sistema | Ultimo dato | Recurso |",
        "|---|---|---|---|---|---|",
    ]
    for s in sorted(with_data, key=lambda x: (x["system_id"], x["hos"] or "", x["id"])):
        bn = (s["building_name"] or "")[:40]
        lines.append(
            f"| {s['id']} | {s['hos'] or '—'} | {bn} | "
            f"{s['system_id']} | {s['last_seen'] or '—'} | {s['resource']} |"
        )

    lines += [
        "",
        f"## Sensores sin datos ({len(without_data)})",
        "",
        "| id | HOS | Sistema | Motivo |",
        "|---|---|---|---|",
    ]
    for s in sorted(without_data, key=lambda x: (x["motivo"], x["system_id"], x["id"])):
        lines.append(
            f"| {s['id']} | {s['hos'] or '—'} | {s['system_id']} | {s['motivo']} |"
        )

    if resource_no_sample:
        lines += [
            "",
            f"## Recurso existe pero sin muestras ({len(resource_no_sample)})",
            "",
            "| id | HOS | Sistema | Recursos existentes |",
            "|---|---|---|---|",
        ]
        for s in sorted(resource_no_sample, key=lambda x: (x["system_id"], x["id"])):
            lines.append(
                f"| {s['id']} | {s['hos'] or '—'} | {s['system_id']} | "
                f"{', '.join(s['recursos_existentes'])} |"
            )

    # Guardar
    out_dir  = base_dir / "data" / "thethings_snapshots" / "latest"
    out_json = out_dir / "sensors_data_cleanup.json"
    out_md   = out_dir / "sensors_data_cleanup.md"

    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"[PIELH] Informe generado: {now}")
    print(f"        Total sensores  : {total}")
    print(f"        Con datos       : {len(with_data)} ({pct_str(len(with_data), total)})")
    print(f"        Sin datos       : {len(without_data)} ({pct_str(len(without_data), total)})")
    print(f"        Recurso/sin muestras: {len(resource_no_sample)}")
    print()
    print("        Por sistema:")
    for sid, info in sorted(by_system_out.items()):
        print(f"          {sid:5} {info['system_name']:30} {info['con_datos']:3}/{info['total']:3} ({info['pct_util']})")
    print()
    print(f"[OK] {out_json}")
    print(f"[OK] {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
