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
| `thing_id` | string | `"kEl-nX4_..."` | No | ID a la plataforma thethings |
| `thing_token` | string | `"1OdhHyb..."` | No | Token a la plataforma thethings |
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
| `id` | string | `"HOS136-S01-01"` | SI | Pot repetir-se (sensors germans amb el mateix ID lògic) |
| `thing_id` | string | `"0vgUY6Uk..."` | No | ID únic a thethings (disambigua germans) |
| `thing_token` | string | `"8n5lCA8..."` | No | Token a thethings |
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

**Nota important:** Sensors amb el mateix `id` però diferent `thing_id` es consideren "germans" (duplicats lògics). El servidor propaga camps compartits a tots els germans i reserva `thing_id`/`thing_token` al registre específic (`OWN_FIELDS`).

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
| `data._buildingsMap` | `{ building_id → Building }` | Lookup ràpid d'edificis |
| `data._sensorsByBuilding` | `{ hos → [Sensor] }` | Sensors per edifici |
| `data._otherByType` | `{ object_type → [OtherObject] }` | Altres objectes per tipus |
