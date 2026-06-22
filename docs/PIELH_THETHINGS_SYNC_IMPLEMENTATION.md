# PIELH — TheThings Sync Implementation

Data: 2026-06-18 / Actualitzat: 2026-06-20

## Resum

Aquest document cobreix **dues operacions de sincronització amb TheThings** que operen en sentits oposats:

| Operació | Direcció | Botó UI | Endpoint |
|---|---|---|---|
| **Sync de baixada** (import complet) | TheThings → PIELH | "⟳ Sincronizar tot" | `POST /api/import` |
| **Sync de pujada** (push canvis locals) | PIELH → TheThings | "↑ Pujar canvis" | `POST /api/sync-all` |

---

## Identitat vs Sincronització

Els identificadors de registre i els mecanismes de comunicació amb TheThings serveixen finalitats completament diferents. **No s'han de confondre.**

| Identificador | Àmbit | Funció |
|---|---|---|
| `thing_id` | PIELH intern + TheThings | Identifica el registre **dins de PIELH**: selecció, edició, multi-selecció, desambiguació de germanos |
| `thing_token` | TheThings API únicament | Identifica el recurs remot a la plataforma TheThings: push de valors, lectura d'activitat |

### Regles clau

- `thing_id` és la **clau operativa de PIELH**: es desa a `state.multiSelect`, a `editState.selector`, a `editState.targets[].selector.thing_id`.
- `thing_token` **mai s'usa com a clau interna**: no apareix a la UI, no es passa com a selector d'edició, no s'envia al frontend en cap operació de selecció o formulari.
- Tots dos camps formen `OWN_FIELDS` al servidor: no es sobreescriuen en operacions shared (ni en batch, ni via `_complete_empty_fields`).
- La fase 3 del pipeline d'import (auditoria d'activitat) usa `thing_token` per consultar TheThings; el resultat (`iot_health`) s'indexa per `thing_id`.

### Resum gràfic

```
PIELH intern                    TheThings API
─────────────────────────────   ──────────────────────────────
recordKey = thing_id || id      push:  POST /things/{thing_token}
editState.selector.thing_id     audit: GET  /things/{thing_token}/last
state.multiSelect.add(thing_id)
findSensor(id, thingId)
```

**Referència:** [PIELH_IDENTITY_MODEL.md](PIELH_IDENTITY_MODEL.md)

---

## Sync de baixada — Pipeline `import_tags_inventory_v1`

Implementat a `server.py:_run_import()`. Executa 3 fases automàtiques en seqüència.

### Flux

```
POST /api/import
  ↓
_run_import() [thread]
  │
  ├── [FASE 1 — importing]
  │   ├── _backup() preventiu → data/backups/pielh_qa_master_YYYYMMDD_HHMMSS.json
  │   ├── buildings = [], sensors = []
  │   └── per cada model MODELS[22]:
  │       GET {API}/v2/models/{id}/things?lib=panel → _thing_to_building() / _thing_to_sensor()
  │       _save() incremental
  │
  ├── [FASE 2 — resolving_tags]
  │   └── _resolve_tags_in_master(master)
  │       per cada edifici: _resolve_tags_to_fields() → _propagate_to_sensors()
  │
  ├── [FASE 3 — updating_inventory]
  │   ├── run_audit() [scripts/audit_thethings_activity.py]
  │   │   └── per cada sensor: GET {API}/v2/things/{token}/last → status, last_seen
  │   │       guarda data/audits/thethings_activity_YYYYMMDD_HHMMSS.csv + .json
  │   ├── run_build_report() [scripts/build_inventory_health_report.py]
  │   │   └── guarda data/audits/inventory_health_report.json + .md
  │   └── _apply_iot_health_to_master(master, audit_data)
  │       per cada sensor: iot_health = {status, has_real_data, demo_ready, last_seen, ...}
  │       per cada edifici: iot_total_sensors, iot_active_sensors, iot_demo_ready, iot_health_status
  │
  ├── _validate_iot_health(master) → warnings[]
  └── escriu _meta: {last_sync, buildings, sensors, tags_resolved_at,
                     inventory_health_updated_at, inventory_health_skipped,
                     sync_pipeline_version, validation}
```

### Resultat prova real (2026-06-20)

| Mètrica | Valor |
|---|---|
| Durada total | ~16 min (1564 sensors × API TheThings) |
| Buildings baixats | 192 |
| Sensors baixats | 1564 |
| Things processats | 1756 (22 models) |
| Tags resolts (edificis) | 166 / 192 |
| Tags resolts (sensors) | 1135 / 1564 |
| Sensors amb `iot_health` | 1564 / 1564 |
| Edificis actius IoT | 98 / 192 |
| `inventory_health_skipped` | false |
| Avís generat | "382 sensores sin HOS asignado" |
| Backup generat | `pielh_qa_master_20260620_172332.json` |

### Degradació graceful

Si la fase 3 falla (API no disponible, token invàlid, timeout):
- `_apply_inventory_health_full()` retorna `{'skipped': True, 'reason': '...'}`
- L'import continua i guarda buildings + tags resolts
- `_meta.inventory_health_skipped = true`
- UI mostra toast d'avís amb el motiu

### Seguretat

- `THETHINGS_TOKEN` viu a `config.json` → `server.py`. Mai al frontend.
- L'auditoria de la fase 3 usa el mateix token per llegir l'activitat dels sensors.

---

---

## Fitxers modificats

| Fitxer | Canvis |
|---|---|
| `server.py` | +`SYNC_ALLOWED_FIELDS`, +routing 4 endpoints, +6 mètodes, mod. `_handle_save_single` i `_handle_save_batch` |
| `index.html` | +botó `#btn-push` + indicador `#push-status` al header; +botó `#dp-sync-btn` al detail panel |
| `app.js` | +4 funcions sync, mod. `openDetailPanel`, `saveDetailPanel`, `loadData`, `reloadData` |
| `styles.css` | +`.btn-push`, `.push-status` variants, `.btn-sync-record` |

---

## Endpoints nous

### `GET /api/sync-status`

Retorna resum de registres per estat.

```json
{
  "ok": true,
  "pending": 3,
  "synced": 12,
  "errors": 1,
  "last_sync": "2026-06-18T02:30:00.000Z"
}
```

### `GET /api/sync-pending`

Retorna tots els registres amb `_sync.status === "pending"` o `"error"`.

```json
{
  "ok": true,
  "count": 4,
  "records": [
    { "id": "HOS001", "_entity_type": "building", "_sync": {...}, ... }
  ]
}
```

### `POST /api/sync-record`

Sincronitza un registre individual.

**Input:**
```json
{
  "entityType": "building",
  "id": "HOS001",
  "selector": { "thing_id": "..." }
}
```

**Output:**
```json
{
  "ok": true,
  "id": "HOS001",
  "result": { "values_sent": 3 }
}
```

**Errors:**
- `400` — sense `thing_token` o `entityType` invàlid
- `404` — registre no trobat
- `500` — error de xarxa o API TheThings

### `POST /api/sync-all`

Sincronitza tots els registres pendents o amb error.

**Output:**
```json
{
  "ok": true,
  "total": 5,
  "synced": 4,
  "errors": 1,
  "results": [
    { "id": "HOS001", "ok": true,  "values_sent": 2 },
    { "id": "HOS002", "ok": false, "error": "sin thing_token" }
  ]
}
```

---

## Estructura `_sync` al JSON

Cada registre editat rep el camp `_sync`:

```json
{
  "_sync": {
    "status":     "pending",
    "updated_at": "2026-06-18T02:30:00.000Z",
    "fields":     ["district_code", "district_name", "lat"],
    "error":      null,
    "synced_at":  null
  }
}
```

**Estats possibles:** `pending` → `synced` | `error`

---

## Allowlist de camps sincronitzables

```
SYNC_ALLOWED_FIELDS = {
    lat, lon,
    district_code, district_name,
    neighborhood_key, neighborhood,
    street_etra,
    type, zone,
    has_data, status, qa_notes
}
```

Camps fora d'aquesta llista (p.ex. `name`, `thing_id`, `raw`) mai s'envien a TheThings.

---

## Format payload TheThings

```
POST https://api.smartpielh.l-h.cat/v2/things/{thing_token}?store=true&broadcast=true
Authorization: {THETHINGS_TOKEN}
Content-Type: application/json

{
  "values": [
    {"key": "lat", "value": 41.35},
    {"key": "district_code", "value": "D01"}
  ]
}
```

El token **no s'exposa al frontend**. Viu únicament a `config.json` i `server.py`.

---

## Flux de sincronització

```
Usuari edita camp
     ↓
saveDetailPanel() → POST /api/save-record
     ↓
_handle_save_single():
  _apply_updates() → _mark_sync_pending() → _save()
  [camps a SYNC_ALLOWED_FIELDS → _sync.status = "pending"]
     ↓
Frontend: loadPushStatus() → GET /api/sync-status
  → renderPushStatus() → indicador "N pendents de pujar"
     ↓
Usuari prem "↑ Pujar canvis"
     ↓
syncAllPending() → POST /api/sync-all
     ↓
_handle_sync_all():
  per cada registre pending/error:
    _sync_thing() → POST TheThings API
    _sync.status = "synced" | "error"
  _save(master)
     ↓
Frontend: loadPushStatus() → indicador actualitzat
```

---

## Propagació a sensors

Quan s'edita un building amb camps de `BUILDING_TO_SENSOR_FIELDS`:
- Els sensors del mateix HOS també queden marcats com `pending`
- Cada sensor té el seu propi `thing_token` i es sincronitza independentment

---

## Seguretat

- Token THETHINGS_TOKEN: `config.json` → `server.py`. Mai al frontend.
- Si falta token → error `"sin token configurado en config.json"`
- SSL no verificat (comportament existent conservat, igual que `_fetch_model_things`)
- Backup automàtic abans de cada `sync-record` i `sync-all`

---

## Notes importants

- L'import complet (`POST /api/import`) **sobreescriu** buildings i sensors → perd tots els `_sync` markers. Comportament esperat: l'import és un reset.
- Si un registre no té `thing_token` → error de sync (no bloqueja els altres en sync-all)
- `_sync` és visible al frontend (el JSON es llegeix directament) → no conté dades sensibles

---

## Proves manuals

### 1. Verificar marca pending

```
1. Obrir dashboard → editar un building → guardar
2. Verificar: GET http://localhost:8080/api/sync-status
   → "pending": 1 (o més)
3. Verificar: el botó "↑ Pujar canvis" mostra "N pendents de pujar"
```

### 2. Sync individual

```
1. Obrir el registre editat al detail panel
2. El botó "↑ Sincronitzar" hauria de ser visible
3. Premer-lo → toast "Sincronitzat (N camps)"
4. El botó desapareix del panel
```

### 3. Sync-all

```
1. Premer "↑ Pujar canvis" al header
2. Toast: "Pujat: N ok, 0 errors de N"
3. Indicador canvia a "Tot sincronitzat"
```

### 4. Verificar a TheThings

```bash
curl -sk \
  -H "authorization: VF_EF98t-LOviEi0ugeu63Lj6t8" \
  "https://api.smartpielh.l-h.cat/v2/things/{thing_token}?lib=panel"
```

---

## Errors pendents / deute tècnic

- `_sync` és visible als registres exportats a WordPress → filtrar si cal
- El botó `#dp-sync-btn` al bulk-edit no es gestiona (no apareix en bulk)
- No hi ha retry automàtic d'errors
- SSL no verificat (heretat del codi existent)
