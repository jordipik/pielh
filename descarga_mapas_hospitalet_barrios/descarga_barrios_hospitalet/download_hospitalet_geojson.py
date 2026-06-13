#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_hospitalet_geojson.py

Descarga los límites oficiales de L'Hospitalet:
- Distritos: DIV_DIS_OD
- Barrios:   DIV_BAR_OD

Genera:
- data/geojson/hospitalet_districtes.geojson
- data/geojson/hospitalet_barris.geojson

Uso:
    python scripts/download_hospitalet_geojson.py

Requisitos recomendados:
    pip install requests geopandas pyogrio shapely

Fallback:
    Si geopandas no está disponible, el script deja descargados los ZIP/SHP
    en data/raw/hospitalet_geo/ para convertir manualmente con QGIS.
"""

from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("ERROR: falta requests. Instala con: pip install requests")
    sys.exit(1)


BASE_URL = "https://geoportal.l-h.cat//CartoAPI.ashx"

LAYERS = {
    "districtes": {
        "layer": "DIV_DIS_OD",
        "output": "hospitalet_districtes.geojson",
    },
    "barris": {
        "layer": "DIV_BAR_OD",
        "output": "hospitalet_barris.geojson",
    },
}


ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == "scripts" else Path.cwd()
RAW_DIR = ROOT / "data" / "raw" / "hospitalet_geo"
OUT_DIR = ROOT / "data" / "geojson"


def build_url(layer: str) -> str:
    return f"{BASE_URL}?format=SHP&layer={quote(layer)}&request=getlayer&srid=4326"


def download_file(url: str, dest: Path) -> None:
    print(f"Descargando: {url}")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"OK: {dest} ({dest.stat().st_size:,} bytes)")


def unzip_file(zip_path: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)

    print(f"Descomprimido en: {target_dir}")


def find_shp(folder: Path) -> Path:
    shp_files = list(folder.rglob("*.shp"))
    if not shp_files:
        raise FileNotFoundError(f"No se ha encontrado ningún .shp en {folder}")
    return shp_files[0]


def convert_to_geojson(shp_path: Path, output_path: Path) -> bool:
    try:
        import geopandas as gpd
    except ImportError:
        print("AVISO: geopandas no está instalado. No puedo convertir automáticamente a GeoJSON.")
        print("Instala con: pip install geopandas pyogrio shapely")
        return False

    print(f"Convirtiendo a GeoJSON: {shp_path.name} -> {output_path.name}")

    gdf = gpd.read_file(shp_path)

    # Asegurar WGS84 para Leaflet.
    if gdf.crs is None:
        print("AVISO: el SHP no declara CRS. Asumo EPSG:4326 porque la descarga usa srid=4326.")
        gdf = gdf.set_crs(epsg=4326)
    else:
        gdf = gdf.to_crs(epsg=4326)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")

    # Limpieza mínima: confirmar que es JSON válido.
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    features = len(parsed.get("features", []))
    print(f"GeoJSON generado: {output_path} ({features} features)")
    return True


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    converted_all = True

    for name, cfg in LAYERS.items():
        layer = cfg["layer"]
        url = build_url(layer)

        zip_path = RAW_DIR / f"{name}.zip"
        extract_dir = RAW_DIR / name
        output_path = OUT_DIR / cfg["output"]

        try:
            download_file(url, zip_path)
            unzip_file(zip_path, extract_dir)
            shp_path = find_shp(extract_dir)
            ok = convert_to_geojson(shp_path, output_path)
            converted_all = converted_all and ok
        except Exception as e:
            converted_all = False
            print(f"ERROR procesando {name}: {e}")

    print("\nResumen:")
    print(f"- Descargas RAW: {RAW_DIR}")
    print(f"- GeoJSON salida: {OUT_DIR}")

    if converted_all:
        print("\nListo. Ya puedes cargar estos ficheros desde Leaflet:")
        print("- data/geojson/hospitalet_districtes.geojson")
        print("- data/geojson/hospitalet_barris.geojson")
    else:
        print("\nDescarga completada parcial o sin conversión automática.")
        print("Puedes abrir los SHP en QGIS y exportarlos manualmente como GeoJSON EPSG:4326.")


if __name__ == "__main__":
    main()
