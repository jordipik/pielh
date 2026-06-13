#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descarga calles de L'Hospitalet desde OpenStreetMap/Overpass,
las recorta con hospitalet_barris.geojson y genera data/hospitalet_streets.geojson.

Uso desde la raíz del proyecto:
    python scripts/download_hospitalet_streets.py

Dependencias:
    pip install requests shapely
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests
from shapely.geometry import LineString, MultiLineString, shape, mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BARRIS_PATH = DATA_DIR / "hospitalet_barris.geojson"
OUT_PATH = DATA_DIR / "hospitalet_streets.geojson"

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

HIGHWAYS = [
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "service",
    "pedestrian",
    "living_street",
    "unclassified",
]


def load_boundary() -> Any:
    if not BARRIS_PATH.exists():
        raise FileNotFoundError(f"No existe {BARRIS_PATH}")

    data = json.loads(BARRIS_PATH.read_text(encoding="utf-8"))
    polygons = [shape(f["geometry"]) for f in data.get("features", [])]
    if not polygons:
        raise ValueError("hospitalet_barris.geojson no contiene geometrías")
    return unary_union(polygons)


def bbox_from_geom(geom: Any) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = geom.bounds
    return miny, minx, maxy, maxx  # south, west, north, east para Overpass


def build_query(south: float, west: float, north: float, east: float) -> str:
    highway_regex = "|".join(HIGHWAYS)
    return f"""
[out:json][timeout:120];
(
  way["highway"~"^({highway_regex})$"]({south},{west},{north},{east});
);
out tags geom;
""".strip()


def fetch_overpass(query: str) -> Dict[str, Any]:
    last_error = None
    for url in OVERPASS_URLS:
        try:
            print(f"Consultando Overpass: {url}")
            r = requests.post(url, data={"data": query}, timeout=180)
            r.raise_for_status()
            return r.json()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(f"  Falló {url}: {exc}")
            time.sleep(3)
    raise RuntimeError(f"No se pudo consultar Overpass. Último error: {last_error}")


def geom_to_lines(geom: Any) -> List[Any]:
    if geom.is_empty:
        return []
    if isinstance(geom, LineString):
        return [geom]
    if isinstance(geom, MultiLineString):
        return list(geom.geoms)
    # GeometryCollection u otros derivados del clip
    if hasattr(geom, "geoms"):
        lines = []
        for g in geom.geoms:
            lines.extend(geom_to_lines(g))
        return lines
    return []


def convert_to_geojson(osm: Dict[str, Any], boundary: Any) -> Dict[str, Any]:
    features = []
    seen = set()

    for el in osm.get("elements", []):
        if el.get("type") != "way" or "geometry" not in el:
            continue

        coords = [(p["lon"], p["lat"]) for p in el["geometry"]]
        if len(coords) < 2:
            continue

        raw_line = LineString(coords)
        clipped = raw_line.intersection(boundary)
        clipped = clipped.simplify(0.00001, preserve_topology=True)

        tags = el.get("tags", {}) or {}
        props = {
            "osm_id": el.get("id"),
            "name": tags.get("name", ""),
            "highway": tags.get("highway", ""),
        }

        for line in geom_to_lines(clipped):
            if line.is_empty or line.length == 0:
                continue
            key = (props["osm_id"], tuple(line.coords))
            if key in seen:
                continue
            seen.add(key)
            features.append({
                "type": "Feature",
                "properties": props,
                "geometry": mapping(line),
            })

    features.sort(key=lambda f: (f["properties"].get("name") or "", str(f["properties"].get("osm_id") or "")))
    return {
        "type": "FeatureCollection",
        "name": "hospitalet_streets_osm_clipped",
        "features": features,
    }


def main() -> int:
    boundary = load_boundary()
    south, west, north, east = bbox_from_geom(boundary)
    print(f"BBox L'Hospitalet: {south},{west},{north},{east}")

    query = build_query(south, west, north, east)
    osm = fetch_overpass(query)
    geojson = convert_to_geojson(osm, boundary)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(geojson, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(geojson['features'])} tramos guardados en {OUT_PATH}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
