# PIELH - Descarga de calles de L'Hospitalet

Este paquete usa los barrios ya descargados como máscara territorial:

- `data/hospitalet_barris.geojson`
- `data/hospitalet_districtes.geojson`

## Ejecutar en Windows

Doble clic en:

```txt
Ejecutar_descarga_calles.bat
```

O desde terminal:

```bash
pip install requests shapely
python scripts/download_hospitalet_streets.py
```

## Salida

Genera:

```txt
data/hospitalet_streets.geojson
```

## Capa Leaflet sugerida

```js
let streetLayer = null;

fetch('data/hospitalet_streets.geojson')
  .then(r => r.json())
  .then(data => {
    streetLayer = L.geoJSON(data, {
      style: {
        color: '#9ca3af',
        weight: 1,
        opacity: 0.65
      },
      onEachFeature: (feature, layer) => {
        const name = feature.properties?.name || '';
        const highway = feature.properties?.highway || '';
        if (name) layer.bindTooltip(name, { sticky: true });
        layer.bindPopup(`<strong>${name || 'Calle sin nombre'}</strong><br>${highway}`);
      }
    });

    // Añadirla al control de capas existente:
    // overlays['Calles'] = streetLayer;
    // streetLayer.addTo(map);
  })
  .catch(err => console.warn('No se pudo cargar hospitalet_streets.geojson', err));
```
