"""
PIELH - Fetch TheThings Tags (Fase 2)
Extrae tags desde los raw descargados en Fase 1 (sin nuevas llamadas a la API).
Solo lectura. No modifica pielh_qa_master.json.

Prerequisito: ejecutar primero scripts/fetch_thethings_structure.py --no-ssl-verify
"""

import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

KNOWN_PREFIXES = ['BARRIO', 'CALLE', 'CONFIG', 'CU', 'DISTRITO', 'HOS', 'INSTALADO', 'TIPO', 'ZONA']

# Cada prefix en minúsculas también, para normalizar
KNOWN_PREFIXES_UPPER = [p.upper() for p in KNOWN_PREFIXES]


def get_prefix(tag_name):
    t = tag_name.upper()
    for p in KNOWN_PREFIXES_UPPER:
        if t.startswith(p):
            return p
    return None


def build_thing_tags_index(raw_dir):
    """Lee todos los raw/*.json y devuelve dict thing_id → raw_tags_list."""
    index = {}
    for raw_file in sorted(raw_dir.glob("model_*.json")):
        data = json.loads(raw_file.read_text(encoding="utf-8"))
        things = data if isinstance(data, list) else data.get('things', data.get('data', []))
        for thing in things:
            thing_id = thing.get('_id', '')
            if thing_id:
                index[thing_id] = thing.get('tags') or []
    return index


def normalize_tags(raw_tags):
    """raw_tags: lista de objetos {'_id': ..., 'name': ..., ...}. Devuelve lista de strings."""
    return [t['name'] for t in raw_tags if t.get('name')]


def build_tags_summary(all_tags_flat):
    """all_tags_flat: lista plana de todos los nombres de tags vistos."""
    unique = sorted(set(all_tags_flat))
    by_prefix = defaultdict(list)
    unknown = []
    for tag in unique:
        p = get_prefix(tag)
        if p:
            by_prefix[p].append(tag)
        else:
            unknown.append(tag)
    return {
        "all_tags":      unique,
        "by_prefix":     {k: sorted(v) for k, v in sorted(by_prefix.items())},
        "unknown_format": unknown,
    }


def main():
    parser = argparse.ArgumentParser(description="PIELH - Fetch TheThings Tags (Fase 2)")
    parser.add_argument("--no-ssl-verify", action="store_true",
                        help="Ignorado (no se hacen llamadas API en Fase 2, incluido por consistencia)")
    args = parser.parse_args()

    base_dir  = Path(__file__).resolve().parent.parent
    cfg_path  = base_dir / "config.json"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    latest_dir    = base_dir / "data" / "thethings_snapshots" / "latest"
    raw_dir       = latest_dir / "raw"
    struct_path   = latest_dir / "thethings_structure_only.json"

    if not raw_dir.exists():
        print("[ERROR] No existe data/thethings_snapshots/latest/raw/")
        print("        Ejecuta primero:")
        print("        python scripts/fetch_thethings_structure.py --no-ssl-verify")
        return 1

    if not struct_path.exists():
        print("[ERROR] No existe data/thethings_snapshots/latest/thethings_structure_only.json")
        print("        Ejecuta primero:")
        print("        python scripts/fetch_thethings_structure.py --no-ssl-verify")
        return 1

    print("[PIELH] Leyendo snapshot estructural de Fase 1...")
    struct = json.loads(struct_path.read_text(encoding="utf-8"))
    snap_meta = struct.get("_meta", {})

    print("[PIELH] Construyendo índice de tags desde raw/...")
    tag_index = build_thing_tags_index(raw_dir)
    print(f"        Things indexados: {len(tag_index)}")

    all_tags_flat = []
    buildings_out = []
    sensors_out   = []

    for b in struct.get("buildings", []):
        thing_id = b.get("thing_id", "")
        raw_tags = tag_index.get(thing_id, [])
        tags     = normalize_tags(raw_tags)
        all_tags_flat.extend(tags)
        buildings_out.append({
            "id":          b.get("id"),
            "thing_id":    thing_id,
            "thing_token": b.get("thing_token", ""),
            "tags":        tags,
            "tags_csv":    ", ".join(tags),
            "raw_tags":    raw_tags,
        })

    for s in struct.get("sensors", []):
        thing_id = s.get("thing_id", "")
        raw_tags = tag_index.get(thing_id, [])
        tags     = normalize_tags(raw_tags)
        all_tags_flat.extend(tags)
        sensors_out.append({
            "id":          s.get("id"),
            "hos":         s.get("hos"),
            "system_id":   s.get("system_id"),
            "thing_id":    thing_id,
            "thing_token": s.get("thing_token", ""),
            "tags":        tags,
            "tags_csv":    ", ".join(tags),
            "raw_tags":    raw_tags,
        })

    things_with_tags    = sum(1 for b in buildings_out if b["tags"]) + \
                          sum(1 for s in sensors_out   if s["tags"])
    things_without_tags = (len(buildings_out) + len(sensors_out)) - things_with_tags

    output = {
        "_meta": {
            "created_at":            datetime.now().isoformat(),
            "source":                "thethings",
            "phase":                 "tags_only",
            "base_structure_snapshot": snap_meta.get("created_at", str(struct_path)),
            "buildings_total":       len(buildings_out),
            "sensors_total":         len(sensors_out),
            "things_with_tags":      things_with_tags,
            "things_without_tags":   things_without_tags,
        },
        "buildings":    buildings_out,
        "sensors":      sensors_out,
        "tags_summary": build_tags_summary(all_tags_flat),
    }

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_dir = base_dir / "data" / "thethings_snapshots" / ts
    snap_dir.mkdir(parents=True, exist_ok=True)

    out_file = snap_dir / "thethings_tags_only.json"
    out_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # Copiar solo el archivo a latest (preservando raw/ y structure del latest actual)
    latest_tags = latest_dir / "thethings_tags_only.json"
    shutil.copy2(out_file, latest_tags)

    tags_summary = output["tags_summary"]
    print()
    print("[OK] Tags extraídos:")
    print(f"     Buildings procesados   : {len(buildings_out)}")
    print(f"     Sensors procesados     : {len(sensors_out)}")
    print(f"     Things con tags        : {things_with_tags}")
    print(f"     Things sin tags        : {things_without_tags}")
    print(f"     Tags únicos            : {len(tags_summary['all_tags'])}")
    print(f"     Tags formato desconocido: {len(tags_summary['unknown_format'])}")
    print()
    print("     Por prefijo:")
    for prefix, tags in tags_summary["by_prefix"].items():
        print(f"       {prefix:12}: {len(tags)} únicos")
    print()
    print(f"     Snapshot : {out_file}")
    print(f"     Latest   : {latest_tags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
