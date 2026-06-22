# PIELH QA — Estat de Funcionalitats

## Llegenda d'estats

- **FUNCIONAL** — Implementat i funcionant tal com s'espera
- **PARCIAL** — Implementat però amb limitacions o problemes detectats
- **NO IMPLEMENTAT** — Intenció detectada al codi però no realitzada
- **LEGACY** — Existent però no actiu o substituït

---

## Funcionalitats de la UI principal (app.js / index.html)

| Funcionalitat | Estat | Notes |
|---|---|---|
| Càrrega inicial de dades | FUNCIONAL | `loadData()` + `normalizeData()` |
| Mapa Leaflet (basemap, panes) | FUNCIONAL | CartoDB Positron, 6 panes |
| Capes GeoJSON barris/districtes | FUNCIONAL | Fallback automàtic si no existeixen |
| Marcadors d'edificis (divIcon) | FUNCIONAL | 3 estats visuals + Fuera Proyecto |
| Marcadors de sensors (circleMarker) | FUNCIONAL | Colors per sistema, offset solapament |
| Marcadors de carrers (OTROS-CALLES) | FUNCIONAL | Capa desactivada per defecte |
| Marcadors de barris (punt fallback) | FUNCIONAL | Només si GeoJSON no carregat |
| Marcadors de districtes (punt fallback) | FUNCIONAL | Idem |
| Control de capes (topright) | FUNCIONAL | 7 capes commutables |
| Botó zoom a la ciutat (⌂) | FUNCIONAL | Usa bounds del contorn GeoJSON |
| Filtres (districte, barri, sistema, tipus, zona) | FUNCIONAL | Normalització d'accents/underscore |
| Cerca lliure (text) | FUNCIONAL | Busca en múltiples camps |
| Botó limpiar filtres | FUNCIONAL | |
| Filtre "Solo visibles" | FUNCIONAL | Binds a `moveend`/`zoomend` del mapa |
| Taula d'edificis | FUNCIONAL | 8 columnes, ordenació, multi-selecció |
| Taula de sensors | FUNCIONAL | 9 columnes (ID, Nombre Corto, ThingID, HOS, Sistema, Barrio, Dist., Calle, Datos), límit 500, `data-key` i `data-thing-id` per fila |
| Pestanya QA | FUNCIONAL | Filtres per severitat i tipus |
| Cards de resum (header) | FUNCIONAL | Edificis, sensors, barrios, sistemes, QA |
| Selecció simple (taula o mapa) | FUNCIONAL | Sincronització bidireccional. Sensors germanos desambiguats per `thing_id` |
| Selecció multi (Ctrl+click, Shift+click) | FUNCIONAL | Clau `thing_id \|\| id` — dos germanos compten com 2 entrades separades |
| Highlight al mapa | FUNCIONAL | Cercle groc. Sensors per `markerIndex.sensors[thing_id\|\|id]` |
| Zoom a element seleccionat | FUNCIONAL | `map.setView(..., 17)` |
| Panell de detall/edició | FUNCIONAL | Edifici i sensor |
| Edició individual | FUNCIONAL | Tots els camps del formulari |
| Edició massiva (bulk) | FUNCIONAL | Camps reduïts |
| Copiar dades d'edifici a sensor | FUNCIONAL | Previsualització + confirmació |
| Barra de selecció (accions) | FUNCIONAL | Editar, Zoom, Netejar |
| Redimensionador del panell dret | FUNCIONAL | Persistit a localStorage |
| Redimensionament de columnes | FUNCIONAL | Persistit a localStorage |
| Toast de notificació | FUNCIONAL | |
| Sincronització des de thethings API (pipeline complet) | FUNCIONAL | 3 fases: import → tags → inventari IoT. Pipeline `import_tags_inventory_v1`. Prova real: 192 edif., 1564 sens. |
| Resolució de tags (automàtica dins sync) | FUNCIONAL | S'executa automàticament al sincronitzar. Prova real: 166 edif., 1135 sens. resolts |
| Resolució de tags (manual, secundari) | FUNCIONAL | Botó "⚙ Resolver Tags" secundari per a reparació manual |
| Inventari IoT (audit + health) | FUNCIONAL | Auditoria live TheThings API + `iot_health` per sensor. Prova real: 1564/1564 sens. amb iot_health, 98 edif. actius |
| Propagació edifici → sensors | FUNCIONAL | `BUILDING_TO_SENSOR_FIELDS` |
| Completat entre sensors germans | FUNCIONAL | `_complete_empty_fields` |
| Tab auto-switch (mapa → taula) | FUNCIONAL | Edifici→Edificios, Sensor→Sensores |
| Llegenda de sistemes (sidebar) | FUNCIONAL | 16 sistemes mostrats |
| Llegenda de capes (sidebar) | FUNCIONAL | Descripció visual |

---

## Funcionalitats del backend (server.py)

| Funcionalitat | Estat | Notes |
|---|---|---|
| Servir fitxers estàtics | FUNCIONAL | SimpleHTTPRequestHandler |
| GET /api/health | FUNCIONAL | |
| POST /api/save-record | FUNCIONAL | Validació, backup, log, propagació |
| POST /api/save-batch | FUNCIONAL | Idem, múltiples IDs |
| POST /api/import | FUNCIONAL | Thread asíncron, 3 fases: importing → resolving_tags → updating_inventory |
| GET /api/import-status | FUNCIONAL | Inclou `phase`, `sub_status`, `tags_stats`, `inventory_stats`, `warnings`, `inventory_health_skipped` |
| POST /api/resolve-tags | FUNCIONAL | Thread asíncron, polling, log en temps real (manual/reparació) |
| GET /api/resolve-status | FUNCIONAL | |
| Sistema de backup automàtic | FUNCIONAL | Rotació a màx. 20. Backup preventiu al inici de cada import |
| Logging de canvis de camps | FUNCIONAL | |
| Validació de coordenades | FUNCIONAL | Conversió a float |
| Validació de catàlegs | FUNCIONAL | district_code, neighborhood_key, system_id |
| Expand de claus (district_code → district_name) | FUNCIONAL | `_expand_updates` |
| SSL no verificat per a l'API externa | PARCIAL | `ssl._create_unverified_context()` — risc de seguretat acceptable en entorn intern |
| Autenticació del servidor | NO IMPLEMENTAT | No hi ha autenticació a l'API local |

---

## Explorador QA (qa_explorer.html + modules/)

| Funcionalitat | Estat | Notes |
|---|---|---|
| Càrrega de dades (Data.load) | FUNCIONAL | |
| Taula Tabulator | FUNCIONAL | Paginació, CSV export, columnes mòbils |
| Filtres per tipus (buildings/sensors/neighborhoods/districts) | FUNCIONAL | |
| Filtres per sistema, barri, districte | FUNCIONAL | |
| Cerca lliure | FUNCIONAL | JSON.stringify complet |
| Mapa Leaflet (OSM) | FUNCIONAL | |
| Renderitzat de buildings, sensors, barris, districtes | FUNCIONAL | |
| Selecció bidireccional (taula ↔ mapa) | FUNCIONAL | |
| Zoom a seleccionat | FUNCIONAL | |
| Export CSV | FUNCIONAL | |
| Panell de fitxa inferior | FUNCIONAL | Edifici, sensor, barri, districte |
| Edició de dades | NO IMPLEMENTAT | Explorer és read-only |
| Offset espiral sensors solapats | FUNCIONAL | `_spiralOffset` |

---

## Problemes resolts (2026-06)

| Problema | Solució | Commit |
|---|---|---|
| `markerIndex.sensors[id]` — germanos sobreescrivien la clau | Indexat per `getRecordKey(s) = thing_id\|\|id` | `fix(identity)` 2026-06-22 |
| `highlightMapRecord(id, 'sensor')` sense thingId — marcador equivocat | Nou paràmetre `thingId`, lookup per `thingId\|\|id` | `fix(identity)` 2026-06-22 |
| `querySelector('[data-rid="${id}"]')` — fila equivocada per a germanos | Ressaltat per `data-key` (únic) en comptes de `data-rid` (compartit) | `fix(identity)` 2026-06-22 |
| ThingID de tarjeta poc visible (opacity 0.65) | Elimada opacity, `<strong>`, truncat augmentat a 20 | `fix(identity)` 2026-06-22 |

---

## Problemes tècnics i deute detectats

| Problema | Fitxer | Línia aprox. | Risc | Proposta |
|---|---|---|---|---|
| Log registra canvis on `old == new` | `server.py:_log_change` | 123 | Baix | Afegir condició `if old_val != new_val` |
| SSL no verificat per a API externa | `server.py:_fetch_model_things` | 514 | Mig | Afegir certificat CA o verificació |
| Sense autenticació local | `server.py` | — | Alt (si exposat) | Afegir auth bàsica o limitar a localhost |
| `sensor_count` al building pot quedar obsolet | `pielh_qa_master.json` | — | Baix | Calcular dinàmicament (ja es fa a la UI) |
| `details.js` / `modules/*.js` no usats pel dashboard | `modules/` | — | Baix | Afegir nota al codi; no esborrar (qa_explorer en depèn) |
| Import substitueix completament buildings/sensors | `server.py:_run_import` | 325-327 | Alt | No preserva edicions manuals; documentar com a disseny |
| `image` camp a Building no poblat per API | `server.py:_thing_to_building` | 525-555 | Baix | Camp reservat, no operatiu |
| Sensors del carrer (OTROS-CALLES) no editables | `app.js` | — | Baix | No hi ha formulari d'edició per a OtherObjects |
| `pielh_qa_master_legacy.json` sense ús | `/` | — | Cap | Arxivar o esborrar |
| `qa_explorer` no inclòs en `build_deploy_ftp.py` | `build_deploy_ftp.py` | 21-29 | Mig | Afegir si es vol desplegar l'explorador |

---

## Funcionalitats NO IMPLEMENTADES

| Funcionalitat | Evidència al codi | Notes |
|---|---|---|
| Autenticació d'usuari | Cap | No hi ha login, sessions ni tokens al servidor local |
| Edició d'OtherObjects (carrers, barris, districtes) | Cap formulari | Només buildings i sensors al panell d'edició |
| Mapes de calor | Cap | |
| Exportació CSV des del dashboard principal | Cap botó | Sí disponible a l'Explorer |
| Importació CSV | Cap | |
| Historial de canvis a la UI | Cap | Sí al log de text |
| Notifications push | Cap | Polling manual |
| Mode offline / PWA | Cap | Depèn de CDN |
| Multiusuari concurrent | Cap mecanisme de locks a nivell d'usuari | Risc si múltiples usuaris editen simultàniament |
| Validació de formulari al frontend | Mínima | Delega al servidor |
| Confirmació abans de guardar | Cap diàleg de confirmació | Guarda directe |
