# PIELH QA — Procés de Guardada de Dades

## Flux seqüencial complet — Edició individual

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. ACCIÓ DE L'USUARI                                               │
│                                                                     │
│  L'usuari fa click en un edifici o sensor (taula o mapa)           │
│  → selectRecord(id, {source})                                       │
│  → apareix selection-bar amb botó "Editar"                         │
│  → click "Editar" → editSelectedRecord() → openDetailPanel(id)     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. RENDERITZAT DEL FORMULARI                                       │
│                                                                     │
│  openDetailPanel(id, thingId)                                       │
│  ├── detecta entityType ('building' o 'sensor')                     │
│  ├── troba el registre a data._buildingsMap o findSensor()          │
│  ├── editState = {entityType, ids:[id], bulk:false, selector}       │
│  └── renderDetailForm(record, entityType)                           │
│      → genera formulari HTML amb camps editable (text/select/num)  │
│      → camps readonly: id, type (per sensor)                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. EDICIÓ DELS CAMPS                                               │
│                                                                     │
│  L'usuari modifica valors al formulari                              │
│  Opció (sensor): "Copiar datos edificio" → showCopyFromBuilding()  │
│  → mostra previsualització de diferències                           │
│  → "Aplicar" omple els camps (no guarda encara)                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. VALIDACIÓ AL FRONTEND (mínima)                                  │
│                                                                     │
│  saveDetailPanel()                                                  │
│  ├── getSingleFormValues(): recull tots els [data-field]            │
│  │   camps buits → null; camps amb valor → string                  │
│  └── si updates buit → showToast("No hay campos") i avorta         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. PETICIÓ A L'API                                                 │
│                                                                     │
│  POST /api/save-record                                              │
│  Body: {entityType, id, selector:{thing_id}, updates:{...}}        │
│  fetchJson() → await resposta                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼ (al servidor — server.py)
┌─────────────────────────────────────────────────────────────────────┐
│  6. PROCESSAMENT AL SERVIDOR                                        │
│                                                                     │
│  _handle_save_single()                                              │
│  ├── _read_json()             llegeix body                          │
│  ├── validació bàsica de camps obligatoris                          │
│  ├── _load()                  llegeix pielh_qa_master.json          │
│  ├── _validate(updates, master)                                     │
│  │   ├── district_code en catàleg?                                  │
│  │   ├── neighborhood_key en catàleg?                               │
│  │   ├── system_id existeix?                                        │
│  │   └── lat/lon → float (si no buits)                             │
│  │   → si error: retorna HTTP 400                                   │
│  ├── _siblings(master, entityType, id)                              │
│  │   → llista de registres amb el mateix 'id'                      │
│  │   → si buida: retorna HTTP 404                                   │
│  ├── selecciona target per selector.thing_id                        │
│  └── _expand_updates(updates, master)                               │
│      → district_code → + district_name des de catàleg              │
│      → neighborhood_key → + neighborhood des de catàleg            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  7. BACKUP AUTOMÀTIC                                                │
│                                                                     │
│  _backup()                                                          │
│  ├── BACKUP_DIR.mkdir(parents=True, exist_ok=True)                 │
│  ├── shutil.copy2(DATA_FILE, backup_path)                          │
│  │   Format: pielh_qa_master_YYYYMMDD_HHMMSS.json                 │
│  └── rotació: elimina backups antics si > MAX_BACKUPS (20)         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  8. APLICACIÓ DE CANVIS                                             │
│                                                                     │
│  Per a cada germà (registre amb el mateix id):                     │
│  ├── _apply_updates(r, shared_updates)  → r.update(updates)        │
│  │   + actualitza raw['Distrito'] / raw['Barrio'] si cal           │
│  └── Si OWN_FIELDS: _apply_updates(target, own_updates)            │
│                                                                     │
│  _complete_empty_fields(siblings)                                   │
│  → per cada clau: si un germà té valor i l'altre no, propaga      │
│  (excepcions: thing_id, thing_token, id, raw)                      │
│                                                                     │
│  Si entityType === 'building':                                      │
│  → _propagate_to_sensors(master, record_id, shared_updates)        │
│    → aplica BUILDING_TO_SENSOR_FIELDS a sensors amb hos == id      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  9. PERSISTÈNCIA JSON                                               │
│                                                                     │
│  _save(master)                                                      │
│  → DATA_FILE.write_text(json.dumps(master, ensure_ascii=False,     │
│                          indent=2), encoding='utf-8')              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  10. REGISTRE AL LOG                                                │
│                                                                     │
│  Per cada camp modificat (before vs after):                        │
│  _log_change(entity_type, record_id, field, old_val, new_val)      │
│  → logs/pielh.log: "TIMESTAMP | type | id | field | old -> new"   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼ (de tornada al navegador)
┌─────────────────────────────────────────────────────────────────────┐
│  11. RESPOSTA I ACTUALITZACIÓ DE LA UI                              │
│                                                                     │
│  Resposta: {ok: true, id, updates, records, sensors_updated}       │
│                                                                     │
│  saveDetailPanel() [continuació]                                    │
│  ├── reloadData()                                                   │
│  │   ├── fetch('pielh_qa_master.json', {cache:'no-store'})         │
│  │   ├── normalizeData()         → re-indexa en memòria            │
│  │   ├── applyFilters()          → re-filtra + re-renderitza       │
│  │   │   ├── renderMarkers()     → actualitza mapa                 │
│  │   │   ├── renderBuildingsList()                                  │
│  │   │   └── renderSensorsList()                                   │
│  │   └── _applyMetaSync()        → actualitza text del sync        │
│  ├── showToast("Guardado correctamente.")                           │
│  ├── closeDetailPanel()                                             │
│  └── clearMultiSelect()                                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Flux de guardada batch (format actual — targets)

```
saveDetailPanel() [bulk=true]
  ├── getBulkFormValues()           → NOMÉS camps amb valor
  ├── POST /api/save-batch {entityType, targets:[{id, selector}], updates}
  │   servidor:
  │   ├── valida tots els targets ABANS de fer backup
  │   ├── UN ÚNIC _backup() al principi
  │   ├── per cada target {id, selector:{thing_id}}:
  │   │   ├── _siblings(id)                      → tots els germanos
  │   │   ├── si selector.thing_id:
  │   │   │   └── aplica updates NOMÉS al registre amb thing_id indicat
  │   │   │       (sense _complete_empty_fields)
  │   │   └── si sense selector (legacy):
  │   │       ├── aplica updates a TOTS els germanos
  │   │       └── _complete_empty_fields(germanos)
  │   ├── _propagate_to_sensors() (si building)
  │   └── UNA ÚNICA _save() al final
  └── reloadData() + showToast(N registres guardats)
```

### Retrocompatibilitat: format `ids` (legacy)

Si el client envia `ids` en comptes de `targets`, el servidor fa la conversió automàtica:

```
POST /api/save-batch { entityType, ids: ["HOS001","HOS002"], updates }
  ↓ conversió interna
targets = [{ id: "HOS001", selector: null }, { id: "HOS002", selector: null }]
  ↓ comportament: aplica a tots els germanos de cada id (igual que abans)
```

### Exemple: bulk edit de sensors germanos per thing_id

```json
POST /api/save-batch
{
  "entityType": "sensor",
  "targets": [
    { "id": "HOS136-S01-01", "selector": { "thing_id": "abc123" } },
    { "id": "HOS136-S01-01", "selector": { "thing_id": "def456" } }
  ],
  "updates": { "qa_notes": "revisat" }
}
```

Resultat: `abc123` i `def456` s'actualitzen per separat, cadascun amb la seva edició independent.

Veure [PIELH_IDENTITY_MODEL.md](PIELH_IDENTITY_MODEL.md) per al model d'identitat complet.

## Gestió d'errors

| Escenari | Comportament |
|---|---|
| Xarxa caiguda | `fetchJson` llança Error; `showToast('Error: ...')` |
| Validació fallida (400) | `showToast('Error: ...')` amb el missatge del servidor |
| Registre no trobat (404) | `showToast('Error: ...')` |
| Error intern servidor (500) | `showToast('Error: ...')` |
| Fitxer JSON corrupte | `_load()` llança excepció → error 500 |

En cap cas s'escriu el JSON si la validació falla (el backup tampoc es crea).

## Diagrama de seqüència simplificat

```
Usuari    Frontend (app.js)         Backend (server.py)        Fitxers
  │           │                           │                       │
  │─click─────▶                           │                       │
  │           │─openDetailPanel()          │                       │
  │           │─[formulari]               │                       │
  │─guardar──▶│                           │                       │
  │           │─POST /api/save-record────▶│                       │
  │           │                           │─llegeix JSON──────────▶│
  │           │                           │─valida                │
  │           │                           │─backup────────────────▶│
  │           │                           │─aplica canvis         │
  │           │                           │─escriu JSON───────────▶│
  │           │                           │─escriu log────────────▶│
  │           │◀─{ok:true, ...}───────────│                       │
  │           │─reloadData()              │                       │
  │           │─GET pielh_qa_master.json─▶│                       │
  │           │◀─JSON actualitzat─────────│◀──────────────────────│
  │           │─normalizeData()           │                       │
  │           │─applyFilters()            │                       │
  │           │─renderMarkers()           │                       │
  │◀─toast────│                           │                       │
```
