# PIELH QA — API del Servidor

**Servidor:** `server.py` — Python `http.server.SimpleHTTPRequestHandler`  
**Host/Port:** Configurable via `config.json` (per defecte: `127.0.0.1:8080`)

---

## GET /api/health

**Funció:** Comprova l'estat del sistema.  
**Mètode:** GET  
**Entrada:** cap  

**Sortida (200 OK):**
```json
{
  "status": "ok",
  "json_file": "ok",
  "backup_dir": "ok",
  "log_file": "ok"
}
```

**Sortida (error parcial):**
```json
{
  "status": "error",
  "json_file": "error: not found",
  "backup_dir": "warning: not created yet",
  "log_file": "ok"
}
```

**Notes:** `backup_dir` retorna `warning` (no `error`) si no existeix. El directori es crea automàticament en el primer backup.

---

## POST /api/save-record

**Funció:** Guarda un únic registre (edifici o sensor) amb gestió de germans, propagació a sensors i backup automàtic.

**Mètode:** POST  
**Content-Type:** `application/json`

**Cos de la petició:**
```json
{
  "entityType": "building" | "sensor",
  "id": "HOS001",
  "selector": { "thing_id": "kEl-nX4_..." },
  "updates": {
    "neighborhood_key": "CENTRE",
    "district_code": "DISTRITO-1"
  }
}
```

| Camp | Req. | Notes |
|---|---|---|
| `entityType` | SI | `"building"` o `"sensor"` |
| `id` | SI | ID del registre |
| `selector` | No | `{thing_id: "..."}` per disambiguar sensors germans |
| `updates` | SI | Objecte no buit de camps a actualitzar |

**Validació de `updates`:**
- `district_code`: ha d'existir al catàleg de districtes
- `neighborhood_key`: ha d'existir al catàleg de barris
- `system_id`: ha d'existir al catàleg de sistemes o en algun sensor
- `lat`/`lon`: han de ser números vàlids (es converteixen a float)

**Processament al servidor:**
1. `_siblings()` — troba tots els registres amb el mateix `id`
2. `_backup()` — còpia de seguretat del JSON
3. `_apply_updates()` — aplica `shared_updates` a tots els germans
4. Si `selector.thing_id` → aplica `OWN_FIELDS` (`thing_id`, `thing_token`) només al registre específic
5. `_complete_empty_fields()` — propaga valors entre germans
6. Si `entityType === 'building'` → `_propagate_to_sensors()` — aplica `BUILDING_TO_SENSOR_FIELDS` als sensors del HOS
7. `_save()` — escriu el JSON
8. Registre a `logs/pielh.log`

**`_expand_updates()`:** Si s'envia `district_code`, el servidor afegeix automàticament `district_name` des del catàleg. Idem per `neighborhood_key` → `neighborhood`.

**Sortida (200 OK):**
```json
{
  "ok": true,
  "id": "HOS001",
  "updates": { ... },
  "records": [ ... ],
  "sensors_updated": 3
}
```

**Errors:**
| Codi | Motiu |
|---|---|
| 400 | `entityType` invàlid, `id` buit, `updates` buit, validació fallida |
| 404 | Registre no trobat |
| 500 | Excepció intern |

---

## POST /api/save-batch

**Funció:** Guarda múltiples registres en una sola operació (un backup, una escriptura).

**Mètode:** POST  
**Content-Type:** `application/json`

### Format recomanat: `targets` (des de 2026-06)

Permet especificar `selector.thing_id` per a cada registre, essencial per a sensors germanos.

```json
{
  "entityType": "sensor",
  "targets": [
    { "id": "HOS136-S01-01", "selector": { "thing_id": "abc123" } },
    { "id": "HOS136-S01-01", "selector": { "thing_id": "def456" } },
    { "id": "HOS002-S02-01", "selector": null }
  ],
  "updates": {
    "qa_notes": "revisat",
    "status": "OK"
  }
}
```

| Camp | Req. | Notes |
|---|---|---|
| `entityType` | SI | `"building"` o `"sensor"` |
| `targets` | SI* | Llista de `{id, selector}`. *Si no s'envia, cal `ids` (legacy) |
| `targets[].id` | SI | ID lògic del registre |
| `targets[].selector` | No | `{thing_id: "..."}` per a edició precisa; `null` → afecta tots els germanos del `id` |
| `updates` | SI | Camps a aplicar |

**Comportament per target:**
- Amb `selector.thing_id` → aplica updates **únicament** al registre amb aquell `thing_id`. No executa `_complete_empty_fields` (evita contaminació entre germanos).
- Sense `selector` (`null`) → aplica updates a **tots** els germanos del `id` (comportament legacy). Executa `_complete_empty_fields`.
- Deduplicació: cada registre (per `object id` Python) s'actualitza com a màxim una vegada, fins i tot si apareix a diversos targets.

### Format legacy: `ids`

Mantingut per retrocompatibilitat. El servidor el converteix internament a targets sense selector.

```json
{
  "entityType": "building",
  "ids": ["HOS001", "HOS002", "HOS003"],
  "updates": {
    "neighborhood_key": "CENTRE",
    "type": "ADMINISTRATIVO"
  }
}
```

Equivalent a: `targets = [{ id: rid, selector: null } for rid in ids]`

**Efecte:** aplica updates a tots els germanos de cada id. Adequat per a edificis (no tenen el problema de germanos). Per a sensors amb germanos, usar format `targets` per precisió.

**Notes comunes:**
- `OWN_FIELDS` (`thing_id`, `thing_token`) sempre s'exclouen de `shared_updates` (mai es modifiquen en batch)
- Un únic backup per a tota l'operació (abans de qualsevol modificació)
- Validació completa de tots els targets **abans** del backup; si algun no existeix → error 404 sense modificar res

**Sortida (200 OK):**
```json
{
  "ok": true,
  "count": 3,
  "records_updated": 5,
  "updates": { ... },
  "sensors_updated": 12
}
```

- `count`: nombre de targets enviats
- `records_updated`: nombre de registres JSON realment modificats (pot ser > `count` si hi ha germanos sense selector)

---

## POST /api/import

**Funció:** Inicia la importació asíncrona completa (pipeline `import_tags_inventory_v1`): descàrrega TheThings + resolució de tags + inventari IoT.

**Mètode:** POST  
**Cos:** cap (buit)

**Comportament:**
- Si ja hi ha una importació en curs → retorna `{"ok": true, "message": "already running"}`
- Si no → llança thread `_run_import()` i retorna `{"ok": true, "message": "started"}`

**El thread `_run_import()` — 3 fases:**

**Fase 1 — importing:**
1. `_backup()` preventiu
2. Reinicia `buildings = []` i `sensors = []` al master
3. Per cada model de `MODELS` (22 models):
   - `GET {thethings_api}/v2/models/{id}/things?lib=panel` amb SSL no verificat
   - Converteix cada thing a building o sensor via `_thing_to_building()` / `_thing_to_sensor()`
   - Guarda incrementalment el JSON

**Fase 2 — resolving_tags:**
4. `_resolve_tags_in_master(master)` — llegeix tags de cada edifici i omple camps de catàleg
5. `_propagate_to_sensors()` per cada edifici actualitzat
6. Guarda `tags_stats` a `_import_state`

**Fase 3 — updating_inventory:**
7. `_apply_inventory_health_full(master)` — crida live a l'API TheThings per auditar activitat de cada sensor
8. Genera CSV + JSON d'auditoria a `data/audits/`
9. Aplica `iot_health` a cada sensor i comptadors IoT a cada edifici
10. Validació final via `_validate_iot_health(master)`
11. Escriu `_meta` complet amb estadístiques i validació

**`_meta` resultant:**
```json
{
  "last_sync": "2026-06-20T17:37:24.986673",
  "buildings": 192,
  "sensors": 1564,
  "tags_resolved_at": "...",
  "inventory_health_updated_at": "...",
  "inventory_health_skipped": false,
  "inventory_health_error": null,
  "sync_pipeline_version": "import_tags_inventory_v1",
  "validation": {
    "total_sensors": 1564,
    "sensors_with_iot_health": 1564,
    "buildings_with_iot_counts": 192,
    "buildings_missing_iot_counts": 0,
    "total_buildings": 192,
    "warnings": ["382 sensores sin HOS asignado"]
  }
}
```

**Nota:** L'import substitueix completament buildings i sensors. Catàlegs i QA no es toquen. Si la fase 3 falla (API no disponible), l'import continua i `inventory_health_skipped = true`.

---

## GET /api/import-status

**Funció:** Retorna l'estat de la importació en curs (polling).

**Sortida (exemple real — prova 2026-06-20):**
```json
{
  "running": false,
  "done": true,
  "error": null,
  "phase": "done",
  "sub_status": "",
  "models_total": 22,
  "models_done": 22,
  "things_done": 1756,
  "current_model": "SIP - NodoIoT",
  "buildings": 192,
  "sensors": 1564,
  "tags_stats": {
    "buildings_updated": 166,
    "sensors_updated": 1135,
    "no_tags": 2,
    "skipped": 24,
    "tags_unknown": ["CONFIG", "CU02", "CU08", ...]
  },
  "inventory_stats": {
    "skipped": false,
    "matched": 1564,
    "unmatched": 0,
    "buildings_updated": 192,
    "buildings_active": 98,
    "health_source": "thethings_activity_20260620_152144.csv",
    "sensors_audited": 1564
  },
  "inventory_health_skipped": false,
  "warnings": ["382 sensores sin HOS asignado"],
  "sync_pipeline_version": "import_tags_inventory_v1",
  "started_at": "2026-06-20T17:21:33.019758",
  "finished_at": "2026-06-20T17:37:24.986673"
}
```

**Camp `phase`:** `importing` | `resolving_tags` | `updating_inventory` | `done` | `error`

**Camp `sub_status`:** Detall dins la fase actual (ex: `"Auditando sensor 832/1564…"`). Buit quan no hi ha import en curs.

**Camp `inventory_health_skipped`:** `true` si la fase d'inventari IoT es va ometre (API no disponible). En aquest cas `inventory_stats.reason` conté el motiu.

---

## POST /api/resolve-tags

**Funció:** Inicia la resolució asíncrona de tags de cada edifici per omplir camps de catàleg.

**Mètode:** POST  
**Cos:** cap

**El thread `_run_resolve_tags()`:**
1. Llegeix `buildings` i catàlegs del master
2. Per cada edifici:
   - Llegeix `b.tags` (CSV)
   - `_resolve_tags_to_fields()` → mapeja tags a camps
   - `_apply_updates()` a l'edifici
   - `_propagate_to_sensors()` als sensors del HOS
3. Guarda el master

**Format de tags reconeguts:**
```
DISTRITO-DISTRITO-1  → district_code, district_name
BARRIO-CENTRE        → neighborhood_key, neighborhood
TIPO-ADMINISTRATIVO  → type
ZONA-RESIDENCIAL     → zone
CALLE-C. Digoine     → street_etra
```

Tags no reconeguts es recopilen a `_resolve_state.tags_unknown`.

---

## GET /api/resolve-status

**Funció:** Polling de l'estat de la resolució de tags.

**Sortida:**
```json
{
  "running": false,
  "done": true,
  "total": 150,
  "done_count": 150,
  "buildings_updated": 120,
  "sensors_updated": 450,
  "no_tags": 10,
  "skipped": 20,
  "fields_count": {"district_code": 118, "neighborhood_key": 115, "type": 100, ...},
  "tags_unknown": ["TAG1", "TAG2"],
  "sensors_no_building": 5,
  "log": ["HOS001: district_code=DISTRITO-1, ..."],
  "started_at": "...",
  "finished_at": "..."
}
```

---

## GET / (fitxers estàtics)

`SimpleHTTPRequestHandler` serveix tots els fitxers del directori arrel (`ROOT = Path(__file__).parent`).

Inclou: `index.html`, `app.js`, `styles.css`, `pielh_qa_master.json`, `data/geojson/*.geojson`, `modules/*.js`, `qa_explorer.html`, etc.

**No hi ha autenticació.** El servidor es dissenyat per a ús intern (localhost o intranet).

---

## Sistema de backup

**Funció:** `_backup()` — `server.py:720`

- S'executa automàticament en cada crida a `save-record` i `save-batch` (un cop per crida)
- S'executa **automàticament al inici de cada import** (backup preventiu) i en cada `save-record` / `save-batch`
- Format: `data/backups/pielh_qa_master_YYYYMMDD_HHMMSS.json`
- Rotació: manté els últims `MAX_BACKUPS` (defecte: 20) fitxers. Elimina els més antics.

---

## Sistema de logs

**Fitxer:** `logs/pielh.log`  
**Format:** `YYYY-MM-DD HH:MM:SS | entity_type | record_id | field | old_val -> new_val`

**S'enregistra:** qualsevol camp que canvia de valor en `save-record`, `save-batch` i `resolve-tags`.

**Exemple:**
```
2026-06-12 10:20:59 | building | HOS001 | short_name | Aj. Casa Consistorial -> Aj. Casa Consistorial
2026-06-13 09:29:27 | sensor | HOS136-S01-01 | lat | 41.35299999999999 -> 41.3625896728415
```

**Nota:** El logger registra fins i tot canvis on `old_val == new_val` (confirmació de valor). Comportament confirmat als logs reals.

---

## Validació de coordenades

Si `updates` conté `lat` o `lon`:
- Si el valor és `null` o `""` → s'accepta (neteja la coordenada)
- Si no és buit → es converteix a `float`; si falla → error 400

Les coordenades es validen al servidor i es converteixen a number en el JSON final.
