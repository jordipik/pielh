# PIELH QA — Funcionalitats Detallades

## 1. Selecció d'edifici

**Punt d'entrada:** Click a la taula o al marcador del mapa.

| Via | Funció cridada | Paràmetres |
|---|---|---|
| Click fila taula | `selectRecord(b.id, {source: 'table'})` | |
| Click marcador mapa | `selectRecord(b.id, {source: 'map'})` | |

**Flux complet:**

```
selectRecord(id, {source})
  ├── treu row-selected de totes les files
  ├── clearMapHighlight()
  ├── state.selectedId = id
  ├── marca fila com row-selected + scrollIntoView
  ├── highlightMapRecord(id, 'building')  → cercle groc al mapa
  ├── si source === 'map' → showTab() a pestanya Edificios
  ├── renderSelectionBar()               → mostra card de l'edifici
  └── renderSensorsList()               → filtra sensors per este edifici
```

**Fitxers:** `app.js:965-1004`

---

## 2. Selecció de sensor

**Punt d'entrada:** Click a la taula de sensors o marcador sensor al mapa.

```
selectRecord(id, {source, thingId})
  ├── state.selectedId = id, state.selectedThingId = thingId
  ├── findSensor(id, thingId)           → desambigua sensors germans
  ├── highlightMapRecord(id, 'sensor')
  ├── si source === 'map' → showTab() a pestanya Sensores
  └── renderSelectionBar()
        ├── renderSelectedBuildingCard(building pare)  [si s.hos existeix]
        └── renderSelectedSensorCard(sensor)
```

**Fitxers:** `app.js:965-1004`

**Nota sobre sensors germans:** Sensors amb el mateix `id` però diferent `thing_id` es seleccionen per `thingId`. `findSensor(id, thingId)` busca primer per `thing_id`, cau en el primer `id` coincident si no troba.

---

## 3. Multi-selecció

**Activació:**
- `Ctrl+Click` (o `Meta+Click`) a una fila → `toggleMultiSelect(id, type)`
- `Shift+Click` → `rangeMultiSelect(id, type, records)` (selecció per rang)

**Regles:**
- Només es pot tenir selecció d'un tipus (`building` o `sensor`) a la vegada
- Canviar de tipus neteja la selecció anterior

**Estat:**
- `state.multiSelect`: `Set` d'IDs
- `state.multiSelectType`: `'building'` | `'sensor'` | `null`
- `state.lastSelectedId`: última ID seleccionada (per al rang)

**UI actualitzada per `updateMultiSelectUI()`:**
- Botó "Editar N edificios" (`#btn-bulk-bld`) apareix si ≥ 2 edificis seleccionats
- Botó "Editar N sensores" (`#btn-bulk-sns`) apareix si ≥ 2 sensors seleccionats
- Files amb classe `row-multi-selected`
- `renderSelectionBar()` → mostra barra d'accions si n > 1

**Fitxers:** `app.js:1773-1834`

---

## 4. Filtres

**Funció principal:** `applyFilters()` — `app.js:455`

**Filtres disponibles:**

| Filtre | Lògica edificis | Lògica sensors |
|---|---|---|
| Districte | `b.district_code === value` | `s.district_code === value` |
| Barri | `sameKey(b.neighborhood_key, value)` (normalitzat) | `sameKey(s.neighborhood_key, value)` |
| Sistema | Comprova si algun sensor de l'edifici té el sistema | `normalizeSystemId(s.system_id) === normalizeSystemId(value)` |
| Tipus | `b.type === value` | `s.type === value` |
| Zona | `b.zone === value` | `s.zone === value` |
| Cerca lliure | Concatena camps i `includes(search)` | Idem |

`normalizeKey()`: trim + uppercase + NFC → NFD + treu accents + underscore→espai + espais múltiples.

`normalizeSystemId()`: idem + treu espais + S08 → S08A.

**Resultat:** Omple `filtered.buildings`, `filtered.sensors`, `filtered.otherObjects`.

**Efecte:** `pruneStaleSelection()` + `renderMarkers()` + `renderSummary()` + `renderBuildingsList()` + `renderSensorsList()`.

**Fitxers:** `app.js:402-510`

---

## 5. Ordenació de taules

**Funció:** `sortRecords(records, sortState)` — `app.js:1018`

- Cambia `state.sort.buildings` o `state.sort.sensors` amb `{key, dir}`
- Click a la capçalera: alterna `asc`/`desc`; diferent columna: comença per `asc`
- Columna especial `_sCount`: calcula longitud de `data._sensorsByBuilding[a.id]`
- Comparació: numèrica si ambdós valors són `number`, sino `localeCompare('ca', {sensitivity:'base'})`
- Icones de sort: `▲` (asc) o `▼` (desc) a la capçalera activa

**Fitxers:** `app.js:1103-1141`

---

## 6. Filtre "Solo visibles"

Checkboxes `#chk-visible-bld` i `#chk-visible-sns`.

- `state.onlyVisibleBld` / `state.onlyVisibleSns`
- `getMapVisible(records)`: filtra per `map.getBounds().contains([lat, lon])`
- Es re-aplica cada vegada que el mapa es mou (`map.on('moveend zoomend', ...)`)

**Fitxers:** `app.js:1006-1013`

---

## 7. Edició individual (Detail Panel)

**Activació:** `editSelectedRecord()` → `openDetailPanel(id, thingId)`

**Flux:**
```
openDetailPanel(id)
  ├── detecta si building o sensor
  ├── editState = {entityType, ids:[id], bulk:false, selector:{thing_id}}
  └── renderDetailForm(record, entityType)
        └── genera formulari HTML amb camps editable/readonly

[Usuari edita camps]

saveDetailPanel()
  ├── getSingleFormValues()              → recull valors del formulari
  ├── POST /api/save-record {entityType, id, selector, updates}
  ├── server: _backup() + _apply_updates() + _complete_empty_fields()
  │           + _propagate_to_sensors() (si building)
  │           + _save()
  ├── reloadData()                       → actualitza data + UI
  └── showToast() + closeDetailPanel()
```

**Camps always-null en formulari:** `null` → string buit al formulari; `''` → `null` al servidor.

**Fitxers:** `app.js:1413-1470`, `app.js:1627-1707`

---

## 8. Edició massiva (Bulk Edit)

**Activació:** `openBulkEdit(type)` des del botó "Editar N" o `editSelectedRecord()` si multi-selecció.

```
openBulkEdit(type)
  ├── editState = {entityType, ids:[...multiSelect], bulk:true}
  └── renderBulkForm(type)              → formulari reduït, camps en blanc = no modificar

saveDetailPanel()  [bulk]
  ├── getBulkFormValues()               → només camps amb valor
  ├── POST /api/save-batch {entityType, ids, updates}
  ├── server: per cada id → _siblings() + _apply_updates() + ...
  └── reloadData() + showToast()
```

**Diferència clau:** En bulk, només els camps amb valor al formulari s'envien. El servidor aplica els camps a tots els germans de cada ID.

**Fitxers:** `app.js:1440-1470`, `app.js:1648-1707`

---

## 9. Copiar dades d'edifici a sensor

**Activació:** Botó "Copiar datos edificio" (visible en edició individual de sensor).

```
showCopyFromBuilding()
  ├── llegeix dp-hos.value (edifici seleccionat al formulari)
  ├── compara camps: neighborhood_key, district_code, street_etra, lat, lon
  └── mostra dp-copy-preview amb diferències (valor actual → valor nou)

applyCopyFromBuilding()
  ├── omple els camps del formulari amb els valors de l'edifici
  └── showToast("Pulsa Guardar para persistir")
```

**No guarda automàticament** — l'usuari ha de clicar "Guardar" per persistir.

**Fitxers:** `app.js:1709-1771`

---

## 10. Zoom a element seleccionat

**Activació:** Botó 📍 a la card de selecció, o `zoomSelectedRecord()`.

```
zoomSelectedRecord()
  ├── si multiSelect.size === 1 → usa el primer de multiSelect
  ├── si no → usa state.selectedId
  ├── si building → focusBuilding(id) → map.setView([lat, lon], 17)
  └── si sensor  → focusSensor(id, thingId) → map.setView([lat, lon], 17)
```

Activa la capa del mapa corresponent si estava desactivada.

**Fitxers:** `app.js:1618-1625`, `app.js:910-928`

---

## 11. Ressaltat al mapa

**Funció:** `highlightMapRecord(id, type)` — `app.js:948`

- Neteja el highlight anterior (`_hlLayer`)
- Busca el marcador a `markerIndex.buildings[id]` o `markerIndex.sensors[id]`
- Crea un `L.circleMarker` groc al damunt (`color: #f59e0b`)
- Guarda a `_hlLayer` (es neteja automàticament en la pròxima selecció)

---

## 12. Sincronització des de l'API thethings

**Activació:** Botó "⟳ Sincronizar" → `importFromAPI()`

```
importFromAPI()
  ├── POST /api/import
  ├── servidor: thread _run_import()
  │     ├── per cada model MODELS[21]:
  │     │   ├── GET {API}/v2/models/{id}/things?lib=panel
  │     │   ├── _thing_to_building() o _thing_to_sensor()
  │     │   └── _save(master) incremental
  │     └── escriu _meta: {last_sync, buildings, sensors}
  └── _pollSyncStatus() [polling /api/import-status cada 1.5s]
        └── quan done: reloadData() + showToast()
```

**Comportament de l'import:** Substitueix `buildings` i `sensors` completament (no és incremental). Els catàlegs (`catalogs`) no es modifiquen.

**Fitxers:** `server.py:297-374`, `app.js:1836-1886`

---

## 13. Resolució de tags

**Activació:** Botó "⚙ Resolver Tags" → `resolveTagsFromAPI()`

El servidor llegeix els tags de cada edifici (format CSV) i els mapeja a camps:

| Format del tag | Camp resultant |
|---|---|
| `DISTRITO-X` | `district_code`, `district_name` |
| `BARRIO-X` | `neighborhood_key`, `neighborhood` |
| `TIPO-X` | `type` |
| `ZONA-X` | `zone` |
| `CALLE-X` | `street_etra` |

Els camps resolts es propaguen als sensors de l'edifici (`BUILDING_TO_SENSOR_FIELDS`).

**Polling:** `/api/resolve-status` cada 1s. El log es va omplint en temps real al modal.

**Fitxers:** `server.py:376-509`, `app.js:1888-2006`

---

## 14. Propagació de camps edifici → sensors

Quan es guarda un edifici (individual o batch), el servidor aplica automàticament aquests camps a tots els sensors del mateix HOS:

`BUILDING_TO_SENSOR_FIELDS = {district_code, district_name, neighborhood_key, neighborhood, type, zone, street_etra}`

**Fitxers:** `server.py:26-30`, `server.py:623-639`

---

## 15. Completat de camps entre sensors germans

Sensors amb el mateix `id` (duplicats lògics) es consideren "germans". Quan se'n guarda un, el servidor omple els camps buits dels altres amb el primer valor no buit trobat (`_complete_empty_fields`). Excepcions: `thing_id`, `thing_token` (cada registre té els seus propis).

**Fitxers:** `server.py:641-664`

---

## 16. Filtre QA

**Funció:** `filterQA()` — `app.js:1200`

- Filtre per `severity` i/o `type` via selects
- Amaga/mostra files via `tr.style.display`
- No re-renderitza (operació DOM pura)

---

## 17. Neteja de selecció

**Funció:** `clearSelection()` — `app.js:1597`

- `state.selectedId = null`
- Treu `row-selected` de totes les files
- `clearMapHighlight()`
- `closeDetailPanel()`
- `clearMultiSelect()` → `updateMultiSelectUI()` → `renderSelectionBar()`
- `renderSensorsList()` (elimina el filtre per edifici)
