# PIELH QA — Interfície d'Usuari

## Layout general

```
┌──────────────────────────────────────────────────────────────────┐
│ HEADER: PIELH QA · Sincronizar · QA Explorer · Cards resum      │
├────────────┬─────────────────────┬────────────────────────────────┤
│  SIDEBAR   │      MAPA           │     PANELL DRET                │
│  Filtres   │   (Leaflet)         │ [selected-building-card]       │
│  Llegenda  │                     │ [selected-sensor-card]         │
│            │    [resizer]        │ Tabs: Edificis | Sensores | QA │
│            │                     │ [selection-bar]                │
│            │                     │ [taula filtrada + ordenable]   │
└────────────┴─────────────────────┴────────────────────────────────┘
             [detail-panel] (overlay dret, s'obre sobre el layout)
             [toast] (notificació temporal, cantonada inferior)
             [resolve-modal] (modal central per a tags)
```

---

## Header

**Fitxer:** `index.html:14-44`

| Element | ID/Class | Funció |
|---|---|---|
| Títol | `.header-brand` | "PIELH QA" + "L'Hospitalet de Llobregat" |
| Botó sincronitzar | `#btn-sync` | `importFromAPI()` — importa des de thethings |
| Estat sync | `#sync-status` | Text dinàmic: última sync o progrés |
| Enllaç Explorer | `.btn-explorer` | Obre `qa_explorer.html` en nova pestanya |
| Cards resum | `#count-buildings` etc. | Comptadors dinàmics (edificis, sensors, barrios, sistemes, QA) |

La card QA té estil d'alerta (`card-alert`, fons taronja).

---

## Sidebar (Filtres)

**Fitxer:** `index.html:54-130` | `app.js:402-451`

| Filtre | ID | Tipus | Camps filtrats |
|---|---|---|---|
| Cerca lliure | `#filter-search` | text input | id, name, short_name, street_etra, neighborhood, thing_id, thing_token, state (edificis); id, hos, building_name, system_name, ref_etra, thing_id, cu_old, neighborhood (sensors) |
| Districte | `#filter-district` | select | `district_code` |
| Barri | `#filter-neighborhood` | select | `neighborhood_key` (normalitzat) |
| Sistema | `#filter-system` | select | `system_id` (normalitzat, inclou sensors de l'edifici) |
| Tipus edifici | `#filter-type` | select | `type` |
| Zona | `#filter-zone` | select | `zone` |

- Botó "Limpiar filtros": `resetFilters()` — buida tots els filtres i crida `applyFilters()`
- Botó "Resolver Tags": `resolveTagsFromAPI()` — obre el modal i llança el procés al servidor

**Llegenda:** Mostra tipus de capes (districte, barri, carrer, edifici, sensor) i colors dels sistemes (16 sistemes principals renderitzats via `renderSystemsLegend()`).

---

## Panell dret — Cards de selecció

### selected-building-card (`#selected-building-card`)

Apareix quan es selecciona un edifici. Conté:
- Icona edifici (o imatge si `b.image` existeix — camp NO habitual a les dades)
- Kicker "Edificio seleccionado"
- Títol: `HOS_ID · short_name`
- Meta: type · neighborhood · district · state
- Badges de sistema + comptador de sensors
- Botons: Editar (✏), Zoom (📍), Netejar (✕)

### selected-sensor-card (`#selected-sensor-card`)

Apareix quan es selecciona un sensor. Conté:
- Icona cercle amb color del sistema
- Kicker "Sensor seleccionado"
- Títol: ID sensor
- Meta: system_name · type · ref_etra · neighborhood
- Badges sistema + has_data + district
- Botons: Editar, Zoom, Netejar

---

## Pestanyes (Tabs)

**Fitxer:** `index.html:143-147` | `app.js:1235`

| Pestanya | ID | Contingut |
|---|---|---|
| Edificios | `tab-buildings` | Taula d'edificis filtrats |
| Sensores | `tab-sensors` | Taula de sensors filtrats |
| QA | `tab-qa` | Avisos QA amb filtres per severitat i tipus |

`showTab(btn, tabId)`: commuta classes `active` en `.tab-btn` i `.tab-pane`.

Auto-switch: en clicar un edifici al mapa → va a pestanya Edificios; sensor → Sensores.

---

## Barra de selecció (`#selection-bar`)

**Fitxer:** `app.js:1474`

Apareix quan hi ha elements seleccionats (`n >= 1`):
- `n > 1`: Mode multi-selecció → "N edificios/sensores seleccionados" + "Editar N" + "Limpiar"
- `n = 1` o selecció simple: Mostra les cards de building/sensor (la barra s'amaga)

---

## Taula d'Edificis (`#buildings-table`)

**Fitxer:** `index.html:165-180` | `app.js:802`

| Columna | `data-sort` | Notes |
|---|---|---|
| HOS | `id` | Codi identificador |
| Nombre | `name` | Truncat a 30 caràcters |
| Tipo | `type` | |
| Barrio | `neighborhood` | Abreujat (`shortNeighborhood`) |
| Dist. | `district_name` | |
| Calle | `street_etra` | Truncat a 20 caràcters |
| S | `_sCount` | Nombre de sensors (calculat des de `_sensorsByBuilding`) |
| Datos | `has_data` | Color: verd (OK) o gris |

**Funcionalitats:**
- Ordenació: click en capçalera alterna asc/desc (`sortRecords`)
- Multi-selecció: Ctrl+click (toggle), Shift+click (rang), click simple (exclusiu)
- Fila ressaltada: `row-selected` (CSS)
- Fila especial: `row-fuera` per `state === "Fuera Proyecto"`
- Filtre "Solo visibles": mostra només els visibles al mapa actual
- Columnes redimensionables (`initResizableColumns`), amplada persistida a `localStorage`
- Toolbar: info text + botó "Editar N" (si multi-selecció > 1)

---

## Taula de Sensors (`#sensors-table`)

**Fitxer:** `index.html:184-210` | `app.js:854`

| Columna | `data-sort` | Notes |
|---|---|---|
| ID | `id` | Truncat a 18 caràcters |
| HOS | `hos` | Edifici pare |
| Sistema | `system_id` | Amb punt de color del sistema |
| Barrio | `neighborhood` | Abreujat |
| Dist. | `district_name` | |
| Calle | `ref_etra` | Truncat a 18 caràcters |
| Datos | `has_data` | Color: verd (OK) o gris |

**Funcionalitats:**
- Límit de 500 sensors mostrats (`SENSOR_LIMIT`)
- Si hi ha un edifici seleccionat, filtra per `s.hos === selectedId`
- Mateixa multi-selecció que edificis
- Filtre "Solo visibles" per bounds del mapa

---

## Pestanya QA

**Fitxer:** `index.html:213-240` | `app.js:1146`

| Element | Funció |
|---|---|
| `#qa-severity-badges` | Badges amb comptadors per severitat |
| `#qa-filter-severity` | Select filtre per severitat |
| `#qa-filter-type` | Select filtre per tipus de problema |
| Taula `#qa-tbody` | Files amb: severitat (badge), tipus, detalls (tots els camps del finding) |

`filterQA()`: amaga/mostra files via `tr.style.display`.

---

## Panell de detall/edició (`#detail-panel`)

**Fitxer:** `index.html:250-266` | `app.js:1258`

Overlay lateral dret amb classe `open` quan s'obre.

**Components:**
- Capçalera `#dp-title`: "Edificio HOS001" o "Sensor HOS136-S01-01" o "Editar N edificios"
- Botó tancar (`dp-close`): `closeDetailPanel()`
- Cos `#dp-body`: formulari generat dinàmicament (`renderDetailForm` o `renderBulkForm`)
- Footer:
  - `#dp-copy-preview`: previsualització de còpia de dades d'edifici (sensor únicament)
  - Botó "Copiar datos edificio" (`#dp-copy-btn`): `showCopyFromBuilding()` (sensors)
  - Botó "Guardar": `saveDetailPanel()`
  - Botó "Cancelar": `closeDetailPanel()`

### Formulari d'edifici (`renderDetailForm` — building)

Camps: ID (readonly), Nombre corto (text), Descripción (text), Tipo (text), Zona (text), Barrio (select → catàleg), Distrito (select → catàleg), Calle (text), Latitud (number), Longitud (number), ThingID (text), ThingToken (text), Tags (text), Observaciones (textarea).

### Formulari de sensor (`renderDetailForm` — sensor)

Camps: ID (readonly), Tipo (readonly), Sistema (select → catàleg+extra), Barrio (select), Distrito (select), Edificio HOS (select → buildings), Calle (text), Latitud (number), Longitud (number), ThingID (text), ThingToken (text), Tags (text), Observaciones (textarea).

### Formulari bulk (`renderBulkForm`)

Nota: "Los campos en blanco no se modificarán."

- Edificis: Barrio (select), Distrito (select), Tipo (text), Zona (text)
- Sensors: Sistema (select), Barrio (select), Distrito (select), Edificio HOS (select)

---

## Redimensionador del panell dret (`#panel-resizer`)

**Fitxer:** `app.js:1042`

- Drag horitzontal per canviar l'amplada del panell dret
- Rang: 280px – 900px
- Amplada persistida a `localStorage` (clau: `pielh_panelW`)

---

## Modal de resolució de tags (`#resolve-modal`)

**Fitxer:** `index.html:272-286` | `app.js:1888`

Overlay centrat que apareix durant `resolveTagsFromAPI()`:
- Barra de progrés (`#resolve-progress-bar`)
- Log de missatges (`#resolve-log`) — s'omple via polling `/api/resolve-status`
- Resum final (`#resolve-summary`) amb estadístiques detallades
- Botó tancar (desactivat fins que acaba)

---

## Toast de notificació (`#toast`)

**Fitxer:** `app.js:2032`

- Apareix 3.5 segons
- Classe `toast-ok` (verd) o `toast-err` (vermell)
- `showToast(msg, ok)` — crida des de tota la lògica de guardada

---

## QA Explorer — UI diferent

**Fitxer:** `qa_explorer.html`

Layout: topbar (filtres) + main (taula Tabulator + mapa side-by-side) + detail-panel inferior.

Diferències principals respecte al dashboard:
- Taula: Tabulator 6.2.1 (paginació, columnes mòbils, export CSV)
- Filtres de tipus: botons "Edificios / Sensores / Barrios / Distritos"
- Sense capacitat d'edició (read-only)
- Botó "CSV ↓" per exportar
- Botó "Zoom" per centrar al seleccionat
