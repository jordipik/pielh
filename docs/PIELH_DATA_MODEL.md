# PIELH QA — Model de Dades

Font de veritat: `pielh_qa_master.json`

## Estructura arrel del JSON

```json
{
  "buildings":     [ ...Building ],
  "sensors":       [ ...Sensor ],
  "other_objects": [ ...OtherObject ],
  "catalogs": {
    "systems":       [ ...System ],
    "neighborhoods": [ ...Neighborhood ],
    "districts":     [ ...District ]
  },
  "qa": {
    "findings": [ ...Finding ]
  },
  "_meta": {
    "last_sync":  "ISO8601",
    "buildings":  number,
    "sensors":    number
  }
}
```

## Entitat: Building

Representa un edifici municipal amb sensors IoT.

| Camp | Tipus | Exemple | Req. | Notes |
|---|---|---|---|---|
| `id` | string | `"HOS001"` | SI | Codi únic HOS### |
| `name` | string | `"HOS001 Aj. Casa Consistorial"` | SI | Nom complet |
| `short_name` | string | `"Aj. Casa Consistorial"` | No | Nom curt |
| `description` | string | `""` | No | Descripció lliure |
| `observaciones` | string | `""` | No | Observacions |
| `pielh_id` | string | `""` | No | ID alternatiu legacy |
| `district_code` | string\|null | `"DISTRITO-1"` | No | Clau del catàleg de districtes |
| `district_name` | string\|null | `"Districte I"` | No | Nom derivat de `district_code` |
| `neighborhood_key` | string\|null | `"CENTRE"` | No | Clau del catàleg de barris |
| `neighborhood` | string\|null | `"Centre"` | No | Nom derivat de `neighborhood_key` |
| `type` | string\|null | `"ADMINISTRATIVO"` | No | Tipus d'edifici (lliure) |
| `zone` | string\|null | `"RESIDENCIAL"` | No | Zona (lliure) |
| `street_etra` | string | `"C. Digoine"` | No | Adreça ETRA |
| `street_mti` | string | `""` | No | Adreça MTI (legacy) |
| `lat` | number\|null | `41.3610058832045` | No | Latitud WGS84 |
| `lon` | number\|null | `2.09613941249931` | No | Longitud WGS84 |
| `thing_id` | string | `"kEl-nX4_..."` | No | **Identificador operatiu** a TheThings i PIELH. Clau per a selecció, edició i sync |
| `thing_token` | string | `"1OdhHyb..."` | No | Token de comunicació TheThings. Únicament per a API remota. Camp protegit (`OWN_FIELDS`) |
| `tags` | string | `"DISTRITO-1, BARRIO-CENTRE"` | No | Tags CSV de la plataforma |
| `state` | string\|null | `"Fuera Proyecto"` | No | Estat operatiu |
| `has_data` | string\|null | `"OK"` \| `"SIN DATOS"` | No | Estat de dades |
| `sensor_count` | number | `3` | No | Nombre de sensors (pot quedar obsolet) |
| `raw` | object | `{"tags": [...]}` | No | Dades brutes de la API |
| `image` | string | `""` | No | URL imatge (NO IMPLEMENTAT en API) |

## Entitat: Sensor

Representa un sensor físic instal·lat en un edifici o al carrer.

| Camp | Tipus | Exemple | Req. | Notes |
|---|---|---|---|---|
| `id` | string | `"HOS136-S01-01"` | SI | **Identificador lògic/visual.** Pot repetir-se entre sensors germanos |
| `thing_id` | string | `"0vgUY6Uk..."` | No | **Identificador operatiu únic.** Selecció, edició, sync, multiselecció. Disambigua germanos |
| `thing_token` | string | `"8n5lCA8..."` | No | Token de comunicació TheThings. Camp protegit (`OWN_FIELDS`) |
| `hos` | string\|null | `"HOS136"` | No | HOS de l'edifici pare |
| `system_id` | string | `"S01"` | No | ID del sistema (clau de catàleg) |
| `system_name` | string | `"RUIDO"` | No | Nom del sistema |
| `lat` | number\|null | `41.3626` | No | Latitud WGS84 |
| `lon` | number\|null | `2.1146` | No | Longitud WGS84 |
| `building_name` | string\|null | `null` | No | Nom de l'edifici pare |
| `district_code` | string\|null | `"DISTRITO-1"` | No | Propagat des de l'edifici |
| `district_name` | string\|null | `"Districte I"` | No | Propagat des de l'edifici |
| `neighborhood_key` | string\|null | `"COLLBLANC"` | No | Propagat des de l'edifici |
| `neighborhood` | string\|null | `"Collblanc"` | No | Propagat des de l'edifici |
| `type` | string\|null | `null` | No | Tipus (propagat des de l'edifici) |
| `zone` | string\|null | `null` | No | Zona (propagada des de l'edifici) |
| `ref_etra` | string\|null | `"0"` | No | Referència ETRA |
| `has_data` | string\|null | `"OK"` | No | Estat de dades |
| `include` | boolean | `true` | No | Inclòs en l'anàlisi |
| `status` | string\|null | `null` | No | Estat operatiu del sensor |
| `sensor_code_old` | string\|null | `null` | No | Codi legacy |
| `sensor_order` | number\|null | `null` | No | Ordre dins l'edifici |
| `cu_old` | string\|null | `null` | No | Referència antiga CU |
| `qa_notes` | string\|null | `null` | No | Notes de QA |
| `tags` | string | `""` | No | Tags CSV |
| `raw` | object | `{}` | No | Dades brutes |
| `iot_health` | object\|null | `{status, has_real_data, demo_ready, last_seen, resource, system_class, health_source}` | No | Salut IoT calculada pel pipeline de sincronització TheThings. `status`: `ACTIVE_24H`, `ACTIVE_7D`, `STALE_30D`, `STALE_90D`, `INACTIVE_90D`, `DATA_NO_TIMESTAMP`, `NO_DATA`. `last_seen`: ISO 8601 UTC. **No modificar directament**; es recalcula a cada sincronització. |

**Nota important:** Sensors amb el mateix `id` però diferent `thing_id` es consideren "germanos" (duplicats lògics). El servidor propaga camps compartits a tots els germanos per defecte i reserva `thing_id`/`thing_token` al registre específic (`OWN_FIELDS`). Quan una operació especifica `selector.thing_id`, afecta **únicament** el germano indicat i no executa `_complete_empty_fields` entre germanos. Vegeu [PIELH_IDENTITY_MODEL.md](PIELH_IDENTITY_MODEL.md).

## Entitat: OtherObject

Elements del mapa que no són edificis ni sensors (barris, districtes, carrers).

| Camp | Tipus | Exemple | Notes |
|---|---|---|---|
| `id` | string | `"OTROS-BARRIOS-001"` | |
| `object_type` | string | `"OTROS-BARRIOS"` \| `"OTROS-DISTRITOS"` \| `"OTROS-CALLES"` | Determina la capa del mapa |
| `name` | string | `"Centre"` | |
| `group` | string\|null | | |
| `lat` | number\|null | | |
| `lon` | number\|null | | |
| `thing_id` | string | | |
| `thing_token` | string | | |
| `has_data` | string\|null | | |

## Entitat: System (catàleg)

| Camp | Tipus | Exemple |
|---|---|---|
| `id` | string | `"S01"` |
| `name` | string | `"RUIDO"` |

Sistemes definits: S01 a S25, S08A, S08B, S13A, S13B, S14A, S14B, SIP (25+ codis).

## Entitat: Neighborhood (catàleg)

| Camp | Tipus | Exemple | Notes |
|---|---|---|---|
| `key` | string | `"CENTRE"` | Clau de referència |
| `name` | string | `"Centre"` | Nom mostrat |
| `district_code` | string | `"DISTRITO-1"` | |
| `district_name` | string | `"Districte I"` | |
| `building_count` | number | | Estadística |
| `sensor_count` | number | | Estadística |
| `lat` | number | | Centroide |
| `lon` | number | | Centroide |
| `thing_id` | string | | |

## Entitat: District (catàleg)

| Camp | Tipus | Exemple | Notes |
|---|---|---|---|
| `code` | string | `"DISTRITO-1"` | Clau de referència |
| `name` | string | `"Districte I"` | |
| `description` | string | | |
| `building_count` | number | | |
| `sensor_count` | number | | |

## Entitat: QA Finding

| Camp | Tipus | Exemple | Notes |
|---|---|---|---|
| `severity` | string | `"ERROR"` \| `"WARN"` \| `"INFO"` | |
| `type` | string | `"SENSOR_NO_HOS"` | Tipus de problema |
| + camps addicionals variables | | | Depenen del tipus |

## Relacions

```
District (1) ──────── (N) Neighborhood
                              │
                              │ neighborhood_key
                              ▼
                        Building (1) ──── (N) Sensor
                              │                    │
                              │ hos                │
                              │         ┌──────────┘
                              │         │ (germans: mateix id, diferent thing_id)
                              ▼         ▼
                           System (catàleg)
                           ← system_id ─ Sensor.system_id

OtherObject (OTROS-BARRIOS/DISTRITOS/CALLES) → capes del mapa (no relacionats per FK)
```

## Diagrama ASCII de relacions

```
┌──────────┐        ┌──────────────┐        ┌──────────┐
│ District │ 1    N │ Neighborhood │ 1    N │ Building │
│ code     │───────▶│ key          │───────▶│ id(HOS)  │
│ name     │        │ district_code│        │ district_│
└──────────┘        └──────────────┘        │ code     │
                                            │ neighbor_│
                                            │ hood_key │
                                            └────┬─────┘
                                                 │ 1
                                                 │
                                            ┌────▼─────┐
                                            │ Sensor   │ N (germans)
                                            │ id       │◀─── (same id, diff thing_id)
                                            │ hos      │
                                            │ system_id│
                                            └────┬─────┘
                                                 │ N
                                            ┌────▼─────┐
                                            │ System   │
                                            │ id       │
                                            │ name     │
                                            └──────────┘
```

## Índexs en memòria (generats per `normalizeData()`)

| Índex | Estructura | Ús |
|---|---|---|
| `data._systemsMap` | `{ system_id → System }` | Lookup ràpid de sistemas |
| `data._buildingsMap` | `{ building_id → Building }` | Lookup ràpid d'edificis per `id` |
| `data._buildingsByThingId` | `{ thing_id → Building }` | Lookup ràpid d'edificis per `thing_id` (multiselecció) |
| `data._sensorsByBuilding` | `{ hos → [Sensor] }` | Sensors per edifici |
| `data._otherByType` | `{ object_type → [OtherObject] }` | Altres objectes per tipus |

---

## Relació sensor-edifici i resolució HOS

### Regles canòniques

| Regla | Descripció |
|---|---|
| `Building.id` és la referència HOS | `Building.id` = `"HOS001"`, `"HOS136"`, etc. És la clau principal de l'edifici. |
| `Sensor.hos` apunta a `Building.id` | La relació 1:N edifici-sensors es resol via `sensor.hos == building.id`. |
| `Sensor.id` pot inferir HOS | Si `sensor.id` conté el patró `HOS\d+` (ex: `"HOS136-S01-01"`), es pot inferir l'edifici pare. No és garantit per a tots els sensors. |
| `thing_id` no substitueix `hos` | `thing_id` és la clau operativa per a selecció/edició. No conté ni implica `hos`. |
| `thing_token` no relaciona sensors amb edificis | `thing_token` és únicament per a crides API TheThings. Protegit. No usar com a clau de relació. |

### Com es resol HOS

1. **Preferent:** `sensor.hos` ja té valor → relació directa.
2. **Inferència per id:** `sensor.id` conté `HOS\d+` → candidat `BUILDING_MATCH_BY_ID`.
3. **Inferència per tags/raw:** tags de TheThings poden contenir prefix `HOS` → extret per `fetch_thethings_tags.py`.
4. **Hermanos:** si un hermano (mateix `id`, diferent `thing_id`) ja té `hos`, és candidat `DUPLICATE_OR_SIBLING` — cal verificar per `thing_id` per no contaminar.
5. **Sense pista:** classifica com `STREET_SENSOR` (EUI/serial) o `UNKNOWN`.

### Camps propagats del edifici al sensor

Quan `sensor.hos` és vàlid, els scripts de propagació copien:

| Camp edifici | Camp sensor | Scripts |
|---|---|---|
| `district_code` | `district_code` | `apply_hos_assignments.py`, `apply_sensor_building_inheritance.py` |
| `district_name` | `district_name` | idem |
| `neighborhood_key` | `neighborhood_key` | idem |
| `neighborhood` | `neighborhood` | idem |
| `type` | `type` | idem |
| `zone` | `zone` | idem |
| `street_etra` | `street_etra` | idem |
| `street_mti` | `street_mti` | `apply_sensor_building_inheritance.py` (superset) |
| `lat` | `lat` | `apply_sensor_building_inheritance.py` (si sensor no té lat) |
| `lon` | `lon` | `apply_sensor_building_inheritance.py` (si sensor no té lon) |

Camps **mai** sobreescrits: `thing_id`, `thing_token`, `id`, `system_id`, `system_name`, `iot_health`, `raw`, `tags`, `has_data`, `status`, `sensor_order`, `cu_old`, `ref_etra`.

### Riscos de correccions massives

- Qualsevol script que modifiqui `pielh_qa_master.json` **ha de fer backup previ**.
- Scripts amb `--apply` han d'executar-se primer en **dry-run** i revisar l'informe.
- En sensors hermanos (mateix `id`, diferent `thing_id`), l'assignació s'ha de fer per `thing_id` per evitar contaminar el germano incorrecte.
- `sync_thethings_tags.py --push` modifica dades a TheThings (sistema extern). Risc alt.
- `normalize_sensor_ids.py` no té dry-run clar. Fer backup manual abans d'executar.

Vegeu [PIELH_SCRIPTS.md](PIELH_SCRIPTS.md) per al fluix complet de resolució HOS i tots els scripts implicats.
