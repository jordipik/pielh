# PIELH QA — Sistema GIS / Mapa

## Dashboard principal (app.js)

### Inicialització de Leaflet

```javascript
// app.js: initMap()
map = L.map('map').setView([41.365, 2.105], 13);
// Basemap: CartoDB Positron (light_all)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd', maxZoom: 19
}).addTo(map);
```

| Paràmetre | Valor |
|---|---|
| Biblioteca | Leaflet 1.9.4 (CDN) |
| Centre inicial | [41.365, 2.105] (L'Hospitalet de Llobregat) |
| Zoom inicial | 13 |
| Basemap | CartoDB Positron (`light_all`) |
| Zoom màxim | 19 |

### Panes (Z-index)

Les capes es renditzen en ordre de Z-index:

| Pane | Z-index | Contingut |
|---|---|---|
| `districtsPane` | 200 | Polígons GeoJSON de districtes o marcadors punt |
| `neighborhoodsPane` | 250 | Polígons GeoJSON de barris o marcadors punt |
| `streetsPane` | 275 | Marcadors de carrers (OTROS-CALLES) |
| `buildingsPane` | 300 | Marcadors d'edificis (quadrats divIcon) |
| `sensorsPane` | 420 | Marcadors de sensors (circleMarker) + highlight |

### Capes del mapa

| Capa (layers.X) | Per defecte | Contingut |
|---|---|---|
| `layers.basemap` | Visible | Tiles CartoDB Positron |
| `layers.cityBoundary` | Ocult | Contorn de la ciutat (GeoJSON) |
| `layers.districts` | Visible | Polígons GeoJSON districtes o cercles punt |
| `layers.neighborhoods` | Visible | Polígons GeoJSON barris o cercles punt |
| `layers.streets` | Ocult | Punts OTROS-CALLES |
| `layers.buildings` | Visible | Marcadors edificis |
| `layers.sensors` | Visible | Marcadors sensors |

L'usuari pot activar/desactivar capes via el control `L.control.layers` (posició: `topright`).

### GeoJSON de límits administratius

Es carreguen de forma asíncrona. Si el fitxer retorna 404, cau en fallback de marcadors punt sense error visible.

**`hospitalet_districtes.geojson`** → `layers.districts`
- Color: `#1e40af` (blau fosc), dashArray: `8 5`
- Camps d'etiqueta: `NOM_DIS`, `NOM`, `DISTRICTE`, `NOMBRE_DIS`, `name`
- Si es carrega correctament: `geoJsonLoaded.districts = true`

**`hospitalet_barris.geojson`** → `layers.neighborhoods`
- Color: `#15803d` (verd fosc)
- Camps d'etiqueta: `NOM_BAR`, `NOM`, `BARRI`, `NOMBRE_BAR`, `name`
- Si es carrega correctament: `geoJsonLoaded.neighborhoods = true`

**`hospitalet_boundary.geojson`** → `layers.cityBoundary`
- Color: `#1e3a5f`, sense farcit
- Usa `getBounds()` per calcular `_cityBounds` → usa'd per `zoomToCity()`

### Marcadors d'edificis (divIcon)

Funció: `renderBuildingMarker(b)` — `app.js:560`

```html
<!-- Estructura del divIcon -->
<div class="bm-wrap">
  <div class="building-marker [statusCls]"></div>
  <div class="building-label">HOS001</div>
</div>
```

| Classe CSS | Condició | Color |
|---|---|---|
| `bm-ok` | `has_data === "OK"` | Verd `#4ade80` |
| `bm-nodata` | `has_data === "SIN DATOS"` | Gris `#94a3b8` |
| `bm-unknown` | `has_data` desconegut | Blau `#93c5fd` |
| `bm-fuera` | `state === "Fuera Proyecto"` | (sobreescriu) |

- Mida del icona: `[18, 18]`, ancla `[9, 9]`
- Pane: `buildingsPane` (z-index 300)
- Click: `selectRecord(b.id, {source: 'map'})`

### Marcadors de sensors (circleMarker)

Funció: `renderSensorMarker(s, offsets)` — `app.js:589`

- Radi: 6px
- Color: `SYSTEM_COLORS[system_id]` (25+ colors per sistema)
- Vora: blanc `#fff`, pes 1.5px
- `fillOpacity`: 0.9
- Pane: `sensorsPane` (z-index 420)
- Click: `selectRecord(s.id, {source: 'map'})`

**Sensors solapats:** `offsetOverlappingSensors()` distribueix sensors amb les mateixes coordenades en un cercle de radi `0.000040°` (~4m). — `app.js:137`

### Marcadors de barris (fallback sense GeoJSON)

Funció: `renderNeighborhoodMarkers()` — `app.js:611`  
Font: `data._otherByType['OTROS-BARRIOS']`

- Cercle gran transparent (`radius: 32`), `interactive: false`
- Etiqueta divIcon clicable (obri popup)

### Marcadors de districtes (fallback sense GeoJSON)

Funció: `renderDistrictMarkers()` — `app.js:646`  
Font: `data._otherByType['OTROS-DISTRITOS']`

- Cercle gran puntejat (`radius: 60`, `dashArray: '8 5'`), `interactive: false`
- Etiqueta divIcon clicable

### Marcadors de carrers

Funció: `renderStreetMarkers()` — `app.js:682`  
Font: `data._otherByType['OTROS-CALLES']`

- CircleMarker violeta (`#8b5cf6`), radi 5px
- Tooltip (no permanent) amb el nom del carrer
- Popup amb dades de l'objecte

### Highlight de selecció

Funció: `highlightMapRecord(id, type)` — `app.js:948`

- Crea un `L.circleMarker` groc al damunt del marcador seleccionat
- Color: `#f59e0b`, radi 18 (edifici) o 14 (sensor)
- Pane: `sensorsPane`
- `interactive: false`
- Es guarda a `_hlLayer`; es neteja amb `clearMapHighlight()`

### Control de zoom a la ciutat

Botó personalitzat `⌂` (posició: `topleft`):
- Usa `_cityBounds` (del GeoJSON del contorn) si és vàlid
- Fallback: intenta calcular bounds des dels polígons de districte
- Fallback final: `map.setView([41.365, 2.105], 13)`

### Zoom a un element seleccionat

- Edifici: `focusBuilding(id)` → `map.setView([lat, lon], 17)`
- Sensor: `focusSensor(id, thingId)` → `map.setView([lat, lon], 17)`
- Activa la capa corresponent si estava desactivada

### Sincronització mapa-taula

`map.on('moveend zoomend', ...)`:
- Si `state.onlyVisibleBld` → `renderBuildingsList()` (filtra per bounds del mapa)
- Si `state.onlyVisibleSns` → `renderSensorsList()`

Funció `getMapVisible(records)` → `map.getBounds().contains([lat, lon])`

---

## QA Explorer (modules/map.js)

Aplicació separada `qa_explorer.html`. Basemap diferent (OpenStreetMap).

| Paràmetre | Valor |
|---|---|
| Centre inicial | [41.362, 2.110] |
| Zoom inicial | 14 |
| Basemap | OpenStreetMap (`tile.openstreetmap.org`) |

### Capes

- `buildings`: L.layerGroup (actiu per defecte)
- `sensors`: L.layerGroup (s'afegeix al mapa quan cal)
- `neighborhoods`: L.layerGroup
- `districts`: L.layerGroup

### Marcadors edificis (Explorer)

- `L.divIcon` amb classe `map-bld`, mida 12×12
- Click: crida `_fireSelect('buildings', b)` → `Details.render` + `TableView.highlightRow`

### Marcadors sensors (Explorer)

- `L.divIcon` amb `sensor-dot` coloreig per sistema
- Offset espiral per sensors solapats: `_spiralOffset(i, total)`, radi `0.00005`

### Marcadors barris/districtes (Explorer)

- CircleMarker + etiqueta divIcon no interactiva
- Click en cercle: `_fireSelect('neighborhoods', n)`
- Districtes: centroide calculat com a mitjana de les coords dels barris del districte

### Selecció al mapa (Explorer)

- `highlightById(type, id)`: afegeix/treu classe `marker-selected` als icons
- `zoomToSelected()`: `map.setView(marker.getLatLng(), max(zoom, 17))`
