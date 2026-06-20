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

**Cos de la petició:**
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

| Camp | Req. | Notes |
|---|---|---|
| `entityType` | SI | `"building"` o `"sensor"` |
| `ids` | SI | Llista no buida d'IDs |
| `updates` | SI | Camps a aplicar a tots |

**Notes:**
- `OWN_FIELDS` (`thing_id`, `thing_token`) s'ignoren en batch (no hi ha `selector`)
- Un únic backup per a tota l'operació
- Si algun ID no existeix → error 404 per a tots

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

`records_updated` pot ser > `count` si hi ha sensors/edificis amb germans (mateixa ID, múltiples registres).

---

## POST /api/import

**Funció:** Inicia la importació asíncrona de tots els things des de la API thethings.

**Mètode:** POST  
**Cos:** cap (buit)

**Comportament:**
- Si ja hi ha una importació en curs → retorna `{"ok": true, "message": "already running"}`
- Si no → llança thread `_run_import()` i retorna `{"ok": true, "message": "started"}`

**El thread `_run_import()`:**
1. Reinicia `buildings = []` i `sensors = []` al master
2. Per cada model de `MODELS` (21 models):
   - `GET {thethings_api}/v2/models/{id}/things?lib=panel` amb SSL no verificat
   - Converteix cada thing a building o sensor
   - Guarda incrementalment el JSON
3. Escriu `_meta.last_sync`
4. Actualitza `_import_state`

**Nota:** L'import substitueix completament buildings i sensors. Catàlegs i QA no es toquen.

---

## GET /api/import-status

**Funció:** Retorna l'estat de la importació en curs (polling).

**Sortida:**
```json
{
  "running": true,
  "done": false,
  "error": null,
  "models_total": 21,
  "models_done": 5,
  "things_done": 143,
  "current_model": "S04 - Calidad Aire Interior",
  "buildings": 0,
  "sensors": 143,
  "started_at": "2026-06-18T10:00:00",
  "finished_at": null
}
```

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
- **No** s'executa durant l'import (l'import substitueix directament)
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
