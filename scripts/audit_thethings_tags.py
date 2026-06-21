"""
PIELH - Audit TheThings Tags (Fase 2)
Compara los tags de pielh_qa_master.json con un snapshot de TheThings (tags_only).
Solo lectura. No modifica ningún archivo de datos.

Prerequisito: ejecutar primero scripts/fetch_thethings_tags.py
"""

import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

KNOWN_PREFIXES = ['BARRIO', 'CALLE', 'CONFIG', 'CU', 'DISTRITO', 'HOS', 'INSTALADO', 'TIPO', 'ZONA']


def parse_tags_csv(tags_field):
    """Convierte un campo tags del master (string CSV) en un conjunto de strings."""
    if not tags_field:
        return set()
    return {t.strip() for t in str(tags_field).split(",") if t.strip()}


def get_prefix(tag_name):
    t = tag_name.upper()
    for p in KNOWN_PREFIXES:
        if t.startswith(p):
            return p
    return None


def build_prefix_summary(tags_flat):
    by_prefix = defaultdict(int)
    unknown   = []
    for tag in tags_flat:
        p = get_prefix(tag)
        if p:
            by_prefix[p] += 1
        else:
            unknown.append(tag)
    return {k: v for k, v in sorted(by_prefix.items())}, list(set(unknown))


def main():
    parser = argparse.ArgumentParser(description="PIELH - Audit TheThings Tags (Fase 2)")
    parser.add_argument(
        "--snapshot",
        default=None,
        help="Ruta al thethings_tags_only.json (default: data/thethings_snapshots/latest/thethings_tags_only.json)"
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
        snap_path = base_dir / "data" / "thethings_snapshots" / "latest" / "thethings_tags_only.json"

    if not snap_path.exists():
        print(f"[ERROR] No encontrado snapshot: {snap_path}")
        print("        Ejecuta primero: python scripts/fetch_thethings_tags.py")
        return 1

    master   = json.loads(master_path.read_text(encoding="utf-8"))
    snapshot = json.loads(snap_path.read_text(encoding="utf-8"))
    snap_meta = snapshot.get("_meta", {})

    m_buildings = master.get("buildings", [])
    m_sensors   = master.get("sensors",   [])
    s_buildings = snapshot.get("buildings", [])
    s_sensors   = snapshot.get("sensors",   [])

    # Índices por id
    m_b_idx = {b["id"]: b for b in m_buildings if b.get("id")}
    m_s_idx = {s["id"]: s for s in m_sensors   if s.get("id")}
    s_b_idx = {b["id"]: b for b in s_buildings if b.get("id")}
    s_s_idx = {s["id"]: s for s in s_sensors   if s.get("id")}

    # --- Comparación buildings ---
    b_diffs      = []
    b_identical  = 0
    b_only_m     = 0
    b_only_t     = 0
    b_with_m_tags = 0
    b_with_t_tags = 0

    all_ids_b = set(m_b_idx) | set(s_b_idx)
    for bid in sorted(all_ids_b):
        m_entry = m_b_idx.get(bid)
        s_entry = s_b_idx.get(bid)

        if not m_entry:
            b_only_t += 1
            continue
        if not s_entry:
            b_only_m += 1
            continue

        m_tags = parse_tags_csv(m_entry.get("tags", ""))
        s_tags = set(s_entry.get("tags", []))

        if m_tags:
            b_with_m_tags += 1
        if s_tags:
            b_with_t_tags += 1

        tags_only_m = sorted(m_tags - s_tags)
        tags_only_t = sorted(s_tags - m_tags)

        if tags_only_m or tags_only_t:
            b_diffs.append({
                "entity_type":      "building",
                "id":               bid,
                "thing_id":         s_entry.get("thing_id", ""),
                "master_tags":      sorted(m_tags),
                "thethings_tags":   sorted(s_tags),
                "tags_only_master": tags_only_m,
                "tags_only_thethings": tags_only_t,
            })
        else:
            b_identical += 1

    # --- Comparación sensors ---
    s_diffs      = []
    s_identical  = 0
    s_only_m     = 0
    s_only_t     = 0
    s_with_m_tags = 0
    s_with_t_tags = 0

    all_ids_s = set(m_s_idx) | set(s_s_idx)
    for sid in sorted(all_ids_s):
        m_entry = m_s_idx.get(sid)
        s_entry = s_s_idx.get(sid)

        if not m_entry:
            s_only_t += 1
            continue
        if not s_entry:
            s_only_m += 1
            continue

        m_tags = parse_tags_csv(m_entry.get("tags", ""))
        s_tags = set(s_entry.get("tags", []))

        if m_tags:
            s_with_m_tags += 1
        if s_tags:
            s_with_t_tags += 1

        tags_only_m = sorted(m_tags - s_tags)
        tags_only_t = sorted(s_tags - m_tags)

        if tags_only_m or tags_only_t:
            s_diffs.append({
                "entity_type":      "sensor",
                "id":               sid,
                "thing_id":         s_entry.get("thing_id", ""),
                "hos":              s_entry.get("hos"),
                "system_id":        s_entry.get("system_id"),
                "master_tags":      sorted(m_tags),
                "thethings_tags":   sorted(s_tags),
                "tags_only_master": tags_only_m,
                "tags_only_thethings": tags_only_t,
            })
        else:
            s_identical += 1

    # --- Resumen de prefijos (sobre tags de TheThings) ---
    all_t_tags = [t for b in s_buildings for t in b.get("tags", [])] + \
                 [t for s in s_sensors   for t in s.get("tags", [])]
    by_prefix, unknown_tags = build_prefix_summary(all_t_tags)

    # --- Resultado JSON ---
    now = datetime.now().isoformat()
    result = {
        "_meta": {
            "audit_at":          now,
            "master_path":       str(master_path),
            "snapshot_path":     str(snap_path),
            "snapshot_created":  snap_meta.get("created_at", "desconocido"),
        },
        "summary": {
            "buildings_compared":    len(all_ids_b),
            "buildings_only_master": b_only_m,
            "buildings_only_thethings": b_only_t,
            "buildings_with_master_tags":    b_with_m_tags,
            "buildings_with_thethings_tags": b_with_t_tags,
            "buildings_identical": b_identical,
            "buildings_with_diffs": len(b_diffs),
            "sensors_compared":    len(all_ids_s),
            "sensors_only_master": s_only_m,
            "sensors_only_thethings": s_only_t,
            "sensors_with_master_tags":    s_with_m_tags,
            "sensors_with_thethings_tags": s_with_t_tags,
            "sensors_identical": s_identical,
            "sensors_with_diffs": len(s_diffs),
        },
        "buildings_diff": b_diffs,
        "sensors_diff":   s_diffs,
        "tags_format_summary": {
            "by_prefix":     by_prefix,
            "unknown_format": unknown_tags,
            "total_thethings_tags_seen": len(all_t_tags),
        },
    }

    # --- Guardar en carpeta con timestamp ---
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = base_dir / "data" / "thethings_snapshots" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    out_json = out_dir / "audit_tags.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- Generar MD ---
    lines = [
        "# Auditoría Tags TheThings vs Master",
        "",
        f"- Fecha: {now}",
        f"- Master: `{master_path.name}`",
        f"- Snapshot tags: `{snap_meta.get('created_at', '?')}`",
        "",
        "## Resumen general",
        "",
        f"| Concepto | Valor |",
        "|---|---|",
        f"| Buildings comparados | {len(all_ids_b)} |",
        f"| Buildings solo en master | {b_only_m} |",
        f"| Buildings solo en TheThings | {b_only_t} |",
        f"| Buildings con tags en master | {b_with_m_tags} |",
        f"| Buildings con tags en TheThings | {b_with_t_tags} |",
        f"| Buildings con tags idénticos | {b_identical} |",
        f"| Buildings con diferencias | {len(b_diffs)} |",
        f"| Sensors comparados | {len(all_ids_s)} |",
        f"| Sensors solo en master | {s_only_m} |",
        f"| Sensors solo en TheThings | {s_only_t} |",
        f"| Sensors con tags en master | {s_with_m_tags} |",
        f"| Sensors con tags en TheThings | {s_with_t_tags} |",
        f"| Sensors con tags idénticos | {s_identical} |",
        f"| Sensors con diferencias | {len(s_diffs)} |",
        "",
        "## Tags en TheThings por prefijo",
        "",
        "| Prefijo | Apariciones |",
        "|---|---|",
    ]
    for prefix, cnt in sorted(by_prefix.items()):
        lines.append(f"| {prefix} | {cnt} |")
    if unknown_tags:
        lines.append(f"| (formato desconocido) | {len(unknown_tags)} |")

    if b_diffs:
        lines += [
            "",
            f"## Buildings con diferencias ({len(b_diffs)})",
            "",
            "| HOS | Solo en master | Solo en TheThings |",
            "|---|---|---|",
        ]
        for d in b_diffs:
            om = ", ".join(d["tags_only_master"])    or "—"
            ot = ", ".join(d["tags_only_thethings"]) or "—"
            lines.append(f"| {d['id']} | {om} | {ot} |")
    else:
        lines += ["", "## Buildings con diferencias", "", "Ninguna diferencia detectada."]

    if s_diffs:
        lines += [
            "",
            f"## Sensors con diferencias ({len(s_diffs)}) — muestra, max 50",
            "",
            "| Sensor | HOS | Sistema | Solo en master | Solo en TheThings |",
            "|---|---|---|---|---|",
        ]
        for d in s_diffs[:50]:
            om = ", ".join(d["tags_only_master"])    or "—"
            ot = ", ".join(d["tags_only_thethings"]) or "—"
            lines.append(f"| {d['id']} | {d.get('hos','?')} | {d.get('system_id','?')} | {om} | {ot} |")
        if len(s_diffs) > 50:
            lines.append(f"\n_... y {len(s_diffs)-50} más — ver audit_tags.json_")
    else:
        lines += ["", "## Sensors con diferencias", "", "Ninguna diferencia detectada."]

    if unknown_tags:
        lines += ["", "## Tags con formato desconocido (en TheThings)", ""]
        for t in sorted(unknown_tags)[:50]:
            lines.append(f"- {t}")

    out_md = out_dir / "audit_tags.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")

    # --- Copiar a latest ---
    latest_dir = base_dir / "data" / "thethings_snapshots" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_json, latest_dir / "audit_tags.json")
    shutil.copy2(out_md,   latest_dir / "audit_tags.md")

    # --- Consola ---
    print(f"[PIELH] Auditoría completada: {now}")
    print(f"        Buildings: comparados={len(all_ids_b)}, diffs={len(b_diffs)}, idénticos={b_identical}")
    print(f"        Sensors  : comparados={len(all_ids_s)}, diffs={len(s_diffs)}, idénticos={s_identical}")
    print(f"        Tags TheThings por prefijo: {dict(by_prefix)}")
    print(f"        Tags formato desconocido: {len(unknown_tags)}")
    print(f"[OK] {out_json}")
    print(f"[OK] {out_md}")
    print(f"[OK] {latest_dir / 'audit_tags.json'}")
    print(f"[OK] {latest_dir / 'audit_tags.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
