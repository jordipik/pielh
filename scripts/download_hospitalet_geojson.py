#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descarga los limites oficiales de L'Hospitalet de Llobregat desde
OpenStreetMap (Overpass API) y los convierte a GeoJSON para Leaflet.

Fuente: OSM relation 345401 (l'Hospitalet de Llobregat)
  - Districtes: admin_level=9  (6 distritos)
  - Barris:     admin_level=10 (13 barrios)

Prerrequisitos:
    pip install requests geopandas pyogrio shapely osm2geojson

Uso:
    python scripts/download_hospitalet_geojson.py

Salida:
    data/geojson/hospitalet_districtes.geojson
    data/geojson/hospitalet_barris.geojson

Modo manual (si tienes SHP del Geoportal):
    python scripts/download_hospitalet_geojson.py ruta.shp salida.geojson
"""

import sys
import json
import time
from pathlib import Path

import requests
import geopandas as gpd

# Forzar salida UTF-8 en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Configuracion ────────────────────────────────────────────

OSM_RELATION_LH = 345401   # l'Hospitalet de Llobregat

# Mirror principal (kumi) + fallback
OVERPASS_URLS = [
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass-api.de/api/interpreter',
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
]
OVERPASS_HEADERS = {
    'User-Agent': 'PIELH-QA-Dashboard/1.0 (geographic-data-download)',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
}

OUT_DIR = Path(__file__).parent.parent / 'data' / 'geojson'
TIMEOUT = 70

# ── Overpass helper ──────────────────────────────────────────

def overpass_query(query):
    for url in OVERPASS_URLS:
        try:
            r = requests.post(url, data={'data': query}, headers=OVERPASS_HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            print(f"    [{r.status_code}] {url}")
        except Exception as e:
            print(f"    [ERR] {url}: {e}")
    raise RuntimeError("Todos los mirrors de Overpass fallaron")


def flatten_osm_props(props):
    """Mueve props['tags'] al nivel superior para simplificar acceso en Leaflet."""
    tags = props.pop('tags', {}) or {}
    props.update(tags)
    return props


def relations_to_geojson(admin_level):
    """
    Descarga relaciones de un admin_level dentro de L'Hospitalet con geometria
    completa y devuelve una lista de features GeoJSON con propiedades aplanadas.
    """
    print(f"  Consultando admin_level={admin_level}...")

    query = f"""[out:json][timeout:60];
area(3600{OSM_RELATION_LH})->.city;
relation(area.city)["admin_level"="{admin_level}"]["boundary"="administrative"];
(._; >>;);
out body;"""

    data = overpass_query(query)

    try:
        import osm2geojson
        geojson = osm2geojson.json2geojson(data)
    except ImportError:
        print("  osm2geojson no instalado; usando conversion manual")
        geojson = osm_to_geojson_manual(data, admin_level)

    # Filtrar solo poligonos con el admin_level correcto
    features = []
    for f in geojson.get('features', []):
        if f['geometry']['type'] not in ('Polygon', 'MultiPolygon'):
            continue
        props = f.get('properties', {}) or {}
        tags = props.get('tags', props)  # osm2geojson anida en 'tags'
        if str(tags.get('admin_level', '')).strip() != str(admin_level):
            continue
        f['properties'] = flatten_osm_props(dict(props))
        features.append(f)

    print(f"  {len(features)} poligonos encontrados")
    for f in features:
        print(f"    {f['properties'].get('name','?')}")

    return {'type': 'FeatureCollection', 'features': features}


def osm_to_geojson_manual(osm_data, admin_level):
    """Conversion manual OSM -> GeoJSON sin osm2geojson."""
    nodes = {e['id']: (e['lon'], e['lat'])
             for e in osm_data['elements'] if e['type'] == 'node'}
    ways = {e['id']: e.get('nodes', [])
            for e in osm_data['elements'] if e['type'] == 'way'}

    features = []
    for rel in [e for e in osm_data['elements'] if e['type'] == 'relation']:
        tags = rel.get('tags', {})
        if str(tags.get('admin_level', '')) != str(admin_level):
            continue
        rings = []
        for member in rel.get('members', []):
            if member['type'] == 'way' and member['ref'] in ways:
                coords = [nodes[n] for n in ways[member['ref']] if n in nodes]
                if len(coords) >= 4:
                    rings.append(coords)
        if not rings:
            continue
        features.append({
            'type': 'Feature',
            'properties': dict(tags),
            'geometry': {'type': 'Polygon', 'coordinates': rings[:1]},
        })
    return {'type': 'FeatureCollection', 'features': features}


def save_geojson(geojson, out_path):
    features = geojson.get('features', [])
    if not features:
        print("  Sin features para guardar.")
        return False
    gdf = gpd.GeoDataFrame.from_features(features, crs='EPSG:4326')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(out_path, driver='GeoJSON')
    size = out_path.stat().st_size
    cols = [c for c in gdf.columns if c != 'geometry']
    print(f"  OK  {out_path.name}  ({size:,} bytes, {len(gdf)} features)")
    print(f"      Campos: {cols[:8]}")
    return True


# ── Modo manual: convertir SHP local ────────────────────────

def convert_manual(shp_path, out_name):
    print(f"Convirtiendo {shp_path} -> {out_name}...")
    gdf = gpd.read_file(shp_path, engine='pyogrio')
    gdf.to_file(OUT_DIR / out_name, driver='GeoJSON')
    print(f"  OK  {out_name}")


# ── Main ─────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) == 3:
        convert_manual(sys.argv[1], sys.argv[2])
        sys.exit(0)

    print("=== Descarga limites L'Hospitalet (OpenStreetMap) ===")
    print(f"    Relacion OSM: {OSM_RELATION_LH}")

    try:
        import osm2geojson
        print("    osm2geojson: OK")
    except ImportError:
        print("    AVISO: osm2geojson no instalado (pip install osm2geojson)")
        print("    Se usara conversion manual (menos precisa)")

    print()

    # Districtes (admin_level=9)
    print("--- Districtes ---")
    try:
        gj_dis = relations_to_geojson(9)
        ok_dis = save_geojson(gj_dis, OUT_DIR / 'hospitalet_districtes.geojson')
    except Exception as e:
        print(f"  ERROR: {e}")
        ok_dis = False

    time.sleep(3)

    # Barris (admin_level=10)
    print()
    print("--- Barris ---")
    try:
        gj_bar = relations_to_geojson(10)
        ok_bar = save_geojson(gj_bar, OUT_DIR / 'hospitalet_barris.geojson')
    except Exception as e:
        print(f"  ERROR: {e}")
        ok_bar = False

    print()
    print("=" * 50)
    if ok_dis and ok_bar:
        print(f"OK  Archivos en: {OUT_DIR.resolve()}")
        print("    Abre index.html con Live Server para verlos en el mapa.")
    else:
        print("AVISO: algunos archivos fallaron.")
        if not ok_dis:
            print("  Fallo: hospitalet_districtes.geojson")
        if not ok_bar:
            print("  Fallo: hospitalet_barris.geojson")
