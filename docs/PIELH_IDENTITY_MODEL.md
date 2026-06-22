# PIELH — Model d'Identitat de Registres

Data de creació: 2026-06-22

Document canònic sobre com s'identifiquen i operen els registres (edificis i sensors) al sistema PIELH.

---

## Identificadors

### `id` — Identificador lògic/visual

- Visible a taules, tarjetes i capçaleres.
- Pot repetir-se entre sensors germanos (duplicats lògics de la mateixa posició física).
- **No és suficient per a operacions unívocament precises quan existeixen germanos.**
- Format habitual: `HOS001`, `HOS136-S01-01`.

### `thing_id` — Identificador operatiu principal

- Identificador únic dins la plataforma TheThings i dins de PIELH.
- **Referència principal per a:**
  - Selecció a la UI (`state.selectedThingId`, `state.selectedSensorThingId`)
  - Multi-selecció (`state.multiSelect` emmagatzema `thing_id` quan existeix)
  - Edició individual (`openDetailPanel`, `editState.selector`)
  - Edició massiva (`/api/save-batch` format `targets`)
  - Sincronització individual (`/api/sync-record`, `editState.selector`)
  - Desambiguació de germanos (`findSensor(id, thingId)`)
- Existeix tant en edificis com en sensors.
- Quan no existeix, es fa fallback a `id`.

### `thing_token` — Identificador de comunicació TheThings

- Identificador del recurs remot a la plataforma TheThings.
- Utilitzat **únicament** per a operacions d'API contra TheThings (sync, push).
- Mai s'usa com a clau de selecció, edició o cerca interna.
- Camp protegit: `OWN_FIELDS = {'thing_id', 'thing_token'}` al servidor.

### `hos` — Relació sensor → edifici

- Codi HOS de l'edifici pare d'un sensor.
- Equivalent a `Building.id`.
- Clau de la relació 1:N edifici-sensors.

---

## Regla general: `recordKey`

Tant al frontend com al backend s'aplica la mateixa lògica:

```
recordKey = thing_id  (si existeix)
           || id      (fallback)
```

### Frontend (`app.js`)

```js
function getRecordKey(record) {
    return record.thing_id || record.id;
}
```

`state.multiSelect` emmagatzema `recordKey` (no `id`) des de la versió actual.  
`getRecordByKey(key)` resol `{ record, type }` des d'un key.

### Backend (`server.py`)

```python
# Edició individual: aplica al registre exacte via selector
selector = { "thing_id": "abc123" }  # o null → fallback a id

# Edició massiva: per cada target, localitza el registre específic
target = { "id": "HOS136-S01-01", "selector": { "thing_id": "abc123" } }
```

---

## Sensores germanos

Dos sensors es consideren "germanos" quan comparteixen el mateix `id` però tenen `thing_id` diferent.  
Representen la mateixa posició lògica però registres físics o d'instal·lació distincts.

**Regles:**

- Mai haurien de compartir `thing_id`.
- `_siblings(master, entity_type, id)` retorna tots els germanos d'un `id`.
- Les operacions per `selector.thing_id` afecten **només** el germano especificat.
- Les operacions sense selector afecten **tots** els germanos (comportament legacy).
- `_complete_empty_fields(siblings)` propaga camps buits entre germanos, però **no s'executa** quan l'operació és per `selector.thing_id` (evita contaminació creuada).

---

## Taula resum

| Identificador | Àmbit | Usat per | Pot repetir-se |
|---|---|---|---|
| `id` | PIELH intern | Visualització, lookup per edifici (`_buildingsMap[id]`) | Sí (sensors germanos) |
| `thing_id` | TheThings + PIELH | Selecció, edició, sync, multiselecció | No |
| `thing_token` | TheThings API | Push/pull TheThings | No |
| `hos` | PIELH intern | Relació sensor-edifici | Sí (N sensors per edifici) |

---

## Flux de selecció

```
Click fila / marcador
  → selectRecord(id, { thingId: thing_id })
      ├── state.selectedSensorThingId = thingId
      ├── state.selectedThingId = thingId || building.thing_id
      └── findSensor(id, thingId) → registre exacte

Ctrl+Click (multi)
  → toggleMultiSelect(getRecordKey(record), type)
      └── state.multiSelect.add(thing_id || id)

Shift+Click (rang)
  → rangeMultiSelect(getRecordKey(record), type, records)
      └── rang per keys (thing_id || id), no per ids
```

---

## Flux d'edició

```
openDetailPanel(id, thingId)
  ├── findSensor(id, thingId) → registre exacte
  └── editState.selector = { thing_id }  (si existeix)

saveDetailPanel()
  ├── [individual] POST /api/save-record { id, selector: { thing_id }, updates }
  └── [bulk]       POST /api/save-batch  { targets: [{ id, selector }], updates }
```

---

## Documents relacionats

- [PIELH_DATA_MODEL.md](PIELH_DATA_MODEL.md) — Estructura de dades de `pielh_qa_master.json`
- [PIELH_FUNCTIONALITY.md](PIELH_FUNCTIONALITY.md) — Selecció, multi-selecció, edició
- [PIELH_SAVE_PROCESS.md](PIELH_SAVE_PROCESS.md) — Flux complet de guardada
- [PIELH_API.md](PIELH_API.md) — Endpoints `/api/save-record` i `/api/save-batch`
- [PIELH_THETHINGS_SYNC_IMPLEMENTATION.md](PIELH_THETHINGS_SYNC_IMPLEMENTATION.md) — Sync TheThings
