# PIELH QA — Arquitectura Global

## Visió general

```
┌─────────────────────────────────────────────────────────────┐
│  NAVEGADOR                                                  │
│                                                             │
│  index.html + app.js + styles.css                          │
│  ├── Mapa Leaflet (CartoDB Positron basemap)               │
│  ├── Taula edificis (HTML table, sort natiu)               │
│  ├── Taula sensors (HTML table, sort natiu)                │
│  ├── Taula QA findings                                     │
│  ├── Panell lateral d'edició (detail-panel)               │
│  ├── Barra de selecció (selection-bar)                     │
│  └── Modal Resolve Tags                                    │
│                                                             │
│  qa_explorer.html + qa_explorer_app.js + modules/*.js      │
│  ├── Mapa Leaflet (OpenStreetMap basemap)                  │
│  ├── Taula Tabulator (paginació, CSV export)               │
│  └── Panell de fitxa inferior                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP (fetch API)
                   │ GET / (fitxers estàtics)
                   │ GET /api/health
                   │ GET /api/import-status
                   │ GET /api/resolve-status
                   │ POST /api/import
                   │ POST /api/save-record
                   │ POST /api/save-batch
                   │ POST /api/resolve-tags
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  server.py (Python http.server, port 8080)                 │
│  ├── SimpleHTTPRequestHandler (fitxers estàtics)           │
│  ├── Handler._handle_health()                              │
│  ├── Handler._handle_save_single()                         │
│  ├── Handler._handle_save_batch()                          │
│  ├── Handler._handle_import() → thread _run_import()       │
│  ├── Handler._handle_resolve_tags() → thread _run_resolve()│
│  ├── _import_lock / _resolve_lock (threading.Lock)         │
│  └── logging → logs/pielh.log                             │
└──────────────────┬──────────────────────────────────────────┘
                   │ read/write JSON
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  PERSISTÈNCIA                                               │
│                                                             │
│  pielh_qa_master.json  ← font de veritat única             │
│  data/backups/         ← còpies automàtiques (màx. 20)    │
│  logs/pielh.log        ← registre de canvis de camps      │
│  config.json           ← configuració servidor            │
└──────────────────┬──────────────────────────────────────────┘
                   │ urllib.request (HTTPS amb SSL no verificat)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  API EXTERNA                                               │
│  https://api.smartpielh.l-h.cat                           │
│  GET /v2/models/{model_id}/things?lib=panel               │
│  Header: authorization: {token}                            │
└─────────────────────────────────────────────────────────────┘
```

## Flux principal d'ús

```
Usuari → Obre index.html
       → fetch('pielh_qa_master.json')   [sense cache]
       → normalizeData()                  [indexació en memòria]
       → initMap()                        [Leaflet init]
       → loadBoundaryLayers()             [GeoJSON async]
       → buildFilters()                   [omple selects]
       → applyFilters()                   [filtra + renderitza]
       → renderQA()                       [pestanya QA]
       → initTables()                     [sort + resize]
```

## Flux de selecció d'un element

```
Click taula/mapa → selectRecord(id, {source})
                 → row.classList.add('row-selected')
                 → highlightMapRecord(id, type)     [cercle groc]
                 → renderSelectionBar()              [barra accions]
                 → renderSensorsList()               [si edifici]
```

## Flux d'edició i guardada

```
Usuari → editSelectedRecord() / openDetailPanel(id)
       → renderDetailForm(record, entityType)
       → [edita camps]
       → saveDetailPanel()
       → POST /api/save-record o /api/save-batch
       → server: _backup() + _apply_updates() + _save()
       → reloadData()           [actualitza UI sense reload complet]
       → showToast()
```

## Flux d'importació de l'API externa

```
Usuari → importFromAPI()
       → POST /api/import
       → server: thread _run_import()
         → per cada model MODELS[]:
           → _fetch_model_things(model_id)  [HTTPS extern]
           → _thing_to_building() o _thing_to_sensor()
           → _save(master)
       → _pollSyncStatus() [cada 1.5s, fetch /api/import-status]
       → reloadData()
```

## Flux de resolució de tags

```
Usuari → resolveTagsFromAPI()
       → POST /api/resolve-tags
       → server: thread _run_resolve_tags()
         → per cada building:
           → _resolve_tags_to_fields()  [mapeja tags → camps]
           → _apply_updates()
           → _propagate_to_sensors()
         → _save(master)
       → _pollResolveStatus() [cada 1s]
       → reloadData()
```

## Components principals

### Frontend (app.js)

| Component | Funció |
|---|---|
| `state` (objecte global) | Estat de la UI: selecció, ordenació, multi-selecció, filtres visibles |
| `data` (objecte global) | Dades carregades + índexs (`_buildingsMap`, `_sensorsByBuilding`, etc.) |
| `layers` (objecte global) | Grups de capes Leaflet |
| `markerIndex` | Diccionari id → L.marker per accés ràpid |
| `filtered` | Subconjunt de dades filtrades (buildings, sensors, otherObjects) |
| `editState` | Estat del panell d'edició (entityType, ids, bulk, selector) |

### Backend (server.py)

| Component | Funció |
|---|---|
| `Handler` | Subclasse de `SimpleHTTPRequestHandler` |
| `_import_state` | Estat de l'import (running, done, progress) — protegit per `_import_lock` |
| `_resolve_state` | Estat del resolve-tags — protegit per `_resolve_lock` |
| `MODELS` | Llista de 21 models IoT amb els seus system_id |
| `BUILDING_TO_SENSOR_FIELDS` | Camps que es propaguen d'edifici a sensors |
| `OWN_FIELDS` | Camps que NO es propaguen entre germans (`thing_id`, `thing_token`) |

## Dues aplicacions, un JSON

```
pielh_qa_master.json
       │
       ├── index.html / app.js          (Dashboard QA — app principal)
       │   - Lectura directa via fetch
       │   - Escriptura via API /api/save-*
       │   - Importació via API /api/import
       │
       └── qa_explorer.html / modules   (Explorador — app de consulta)
           - Lectura directa via fetch
           - SENSE capacitat d'edició (read-only)
```
