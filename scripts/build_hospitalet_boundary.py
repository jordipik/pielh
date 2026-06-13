#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el límite municipal de L'Hospitalet uniendo los polígonos de distritos.

Uso:
    python scripts/build_hospitalet_boundary.py

Entrada:  data/geojson/hospitalet_districtes.geojson
Salida:   data/geojson/hospitalet_boundary.geojson
"""

import json
import sys
from pathlib import Path

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT      = Path(__file__).resolve().parent.parent
SRC_PATH  = ROOT / "data" / "geojson" / "hospitalet_districtes.geojson"
DEST_PATH = ROOT / "data" / "geojson" / "hospitalet_boundary.geojson"

SIMPLIFY_TOLERANCE = 0.000025   # ~2.5 m — suaviza microvértices sin perder forma


def main() -> int:
    if not SRC_PATH.exists():
        print(f"ERROR: no existe {SRC_PATH}", file=sys.stderr)
        return 1

    data = json.loads(SRC_PATH.read_text(encoding="utf-8"))
    features = data.get("features", [])
    if not features:
        print("ERROR: el archivo no contiene features", file=sys.stderr)
        return 1

    geoms = []
    for f in features:
        g = shape(f["geometry"])
        if not g.is_valid:
            g = g.buffer(0)
        geoms.append(g)

    union = unary_union(geoms)
    if not union.is_valid:
        union = union.buffer(0)

    union = union.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)

    result = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name":            "L'Hospitalet de Llobregat",
                    "source":          "derived_from_districts",
                    "districts_count": len(features),
                },
                "geometry": mapping(union),
            }
        ],
    }

    DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEST_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: límite guardado en {DEST_PATH}")
    print(f"    Distritos usados: {len(features)}")
    print(f"    Tipo geometría:   {union.geom_type}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
