# PIELH - Proceso de Snapshots TheThings

## Objetivo

Descargar y comparar información desde la plataforma IoT TheThings de forma segura, sin modificar pielh_qa_master.json en ninguna fase.

El proceso permite:
- Guardar un backup (legacy) del master actual antes de cualquier cambio.
- Descargar y auditar estructura de edificios HOS y sensores (Fase 1).
- Descargar y auditar tags (Fase 2).
- Descubrir recursos disponibles y verificar datos reales por sensor (Fase 3).
- Repetir el proceso cuantas veces sea necesario sin sobrescribir snapshots anteriores.

---

## Archivos que NO se modifican en este proceso

- `pielh_qa_master.json` — fuente de verdad del proyecto. Nunca se toca.
- `config.json` — configuración del servidor.
- `app.js`, `index.html`, `styles.css` — frontend.
- Ningún endpoint POST de escritura se invoca.

---

## Scripts disponibles

| Script | Fase | Descripción |
|---|---|---|
| `scripts/export_legacy_02.py` | Pre-proceso | Crea backup del master actual |
| `scripts/fetch_thethings_structure.py` | Fase 1 | Descarga estructura HOS y sensores desde TheThings |
| `scripts/audit_thethings_structure.py` | Fase 1 | Compara estructura master vs TheThings |
| `scripts/fetch_thethings_tags.py` | Fase 2 | Extrae tags desde los raw de Fase 1 (sin nuevas llamadas API) |
| `scripts/audit_thethings_tags.py` | Fase 2 | Compara tags master vs TheThings |
| `scripts/discover_thethings_resources.py` | Fase 3 | Prueba recursos y verifica si hay datos reales por sensor |
| `scripts/audit_thethings_data_health.py` | Fase 3 | Auditoría de cobertura real de datos IoT |
| `scripts/report_sensors_data_cleanup.py` | Fase 4 | Informe de depuración: sensores con/sin datos para revisión manual |
| `scripts/audit_duplicate_sensors.py` | Auditoría | Detecta sensores duplicados/conflictivos por ID, thing_id, HOS+sistema, geo, nombre |
| `scripts/plan_duplicate_sensor_cleanup.py` | Fase 5 | Plan dry-run de limpieza: KEEP / MARK_LEGACY / MANUAL_REVIEW por grupo |
| `scripts/apply_high_confidence_legacy_marks.py` | Fase 5 | Aplica marcas LEGACY HIGH confidence al master (--dry-run / --apply) |
| `scripts/audit_post_cleanup.py` | Fase 5 | Auditoría post-limpieza: métricas antes/después, por sistema y edificio |

---

## Estructura de directorios generada

```
data/
  legacy/
    pielh_qa_master_legacy_02.json
    pielh_qa_master_legacy_02_YYYYMMDD_HHMMSS.json

  thethings_snapshots/
    YYYYMMDD_HHMMSS/          <- snapshot con timestamp (nunca se borra)
      raw/                    <- raw de Fase 1 por modelo
        model_34738_ASSETS.json
        model_33814_S01.json
        ...
      thethings_structure_only.json
      thethings_tags_only.json
      thethings_resources_probe.json
      audit_structure.json / .md
      audit_tags.json / .md
      audit_data_health.json / .md

    latest/                   <- siempre el estado mas reciente (copia)
      raw/
      thethings_structure_only.json
      thethings_tags_only.json
      thethings_resources_probe.json
      audit_structure.json / .md
      audit_tags.json / .md
      audit_data_health.json / .md
```

---

## Proceso completo — cómo repetirlo

```bash
# 0. Backup del master actual
python scripts/export_legacy_02.py

# 1. Descargar estructura
python scripts/fetch_thethings_structure.py --no-ssl-verify

# 1b. Auditar estructura
python scripts/audit_thethings_structure.py --snapshot data/thethings_snapshots/latest/thethings_structure_only.json

# 2. Extraer tags
python scripts/fetch_thethings_tags.py

# 2b. Auditar tags
python scripts/audit_thethings_tags.py --snapshot data/thethings_snapshots/latest/thethings_tags_only.json

# 3. Descubrir recursos y datos (recomendado: prueba pequeña primero)
python scripts/discover_thethings_resources.py --no-ssl-verify --limit-sensors 20 --limit-samples 1
python scripts/discover_thethings_resources.py --no-ssl-verify --limit-samples 1

# 3b. Auditar salud de datos
python scripts/audit_thethings_data_health.py --snapshot data/thethings_snapshots/latest/thethings_resources_probe.json
```

---

## Fase 1 — Estructura HOS y sensores

**Script:** `scripts/fetch_thethings_structure.py`

Descarga desde `GET /v2/models/{model_id}/things?lib=panel` para los 22 modelos definidos en `MODELS`.

**Genera:**
- `raw/model_{id}_{system}.json` — respuesta bruta por modelo (incluye `lastSeen` por thing)
- `thethings_structure_only.json` — estructura normalizada:
  - buildings: id, name, thing_id, thing_token, model_id, hos, lat, lon
  - sensors: id, thing_id, thing_token, model_id, system_id, system_name, hos, lat, lon

**No incluye:** tags, recursos, has_data, datos de resolución.

**Script auditoría:** `scripts/audit_thethings_structure.py`

Compara master vs snapshot: HOS nuevos/desaparecidos, sensores nuevos/desaparecidos,
duplicados por id/thing_id/thing_token, sensores sin HOS, resumen por system_id.

---

## Fase 2 — Tags

**Script:** `scripts/fetch_thethings_tags.py`

Extrae tags desde los `raw/` de Fase 1 sin nuevas llamadas a la API.

**Prerequisito:** Fase 1 completada.

**Genera:** `thethings_tags_only.json` con:
- buildings: id, thing_id, thing_token, tags (array), tags_csv, raw_tags
- sensors: id, hos, system_id, thing_id, thing_token, tags (array), tags_csv, raw_tags
- tags_summary: all_tags, by_prefix, unknown_format

**Prefijos conocidos:** BARRIO, CALLE, CONFIG, CU, DISTRITO, HOS, INSTALADO, TIPO, ZONA

**Script auditoría:** `scripts/audit_thethings_tags.py`

Compara `tags` del master vs tags de TheThings.

**Resultado esperado:**
- Buildings: tags idénticos (master guarda principalmente tags `CU*`; diferencias son esperadas pues TheThings tiene además BARRIO, CALLE, DISTRITO, TIPO, ZONA).
- Sensors: diferencias esperadas — master no almacena tags; TheThings tiene tags `HOS*`.

---

## Fase 3 — Recursos y salud de datos

**Script:** `scripts/discover_thethings_resources.py`

**Prerequisito:** Fase 1 completada (necesita `latest/thethings_structure_only.json` y `latest/raw/`).

**API utilizada:**
```
GET /v2/things/{thing_token}/resources/{resource}?limit=N&lib=panel
```

**Estrategia de descubrimiento:**
1. Los raw de Fase 1 no contienen información de recursos (solo estructura).
2. Se usa `RESOURCE_CANDIDATES[system_id]` — lista controlada de recursos conocidos por sistema.
3. Si el sistema no está en la lista, se usa `RESOURCE_DEFAULT` (genérico).
4. Si un recurso responde 200 con datos → `exists=true`, `has_data=true`.
5. Si responde 404 → `exists=false`.
6. Si responde otro error → `exists=null`, `error` registrado.

**Recursos conocidos por sistema:**
- S01 RUIDO: noise, noise_avg_d, noise_avg_h, noise_avg_w
- S02 CONTAMINACIÓN: temperature, co2, no2, o3, pm1, pm10, pm25, pressure, co
- S04 INTERIOR: temperature, humidity, co2
- S05 ELECTRICIDAD: energy, watts, amps, volts, pf, var
- S07 GAS: gas, m3_a, m3_b, ch_a, ch_b
- S08 CALDERAS: temperature, pressure, status, alarm, description
- S14A METEO: temperature_ext, humidity_ext, rainfall, wind_speed, solar_rad, uv_index, pressure
- S21 HUMOS: alert_fire, temperature, keepalive, battery
- (resto de sistemas: ver RESOURCE_CANDIDATES en el script)

**Parámetros disponibles:**
```
--limit-sensors N      Procesar solo N sensores (para pruebas)
--system S01           Filtrar por system_id
--limit-samples N      Muestras a pedir por recurso — ?limit=N (default: 1)
--no-ssl-verify        Deshabilitar SSL (recomendado en local)
--resources R1,R2      Probar solo estos recursos en todos los sensores
--probe-common         Usar lista genérica para sistemas sin candidatos
--include-sample-preview  Incluir muestra del valor en output (default: no)
--sleep N              Pausa entre peticiones (default: 0.15s)
```

**Genera:** `thethings_resources_probe.json` con:
- `_meta.master_modified: false` — confirmación explícita
- Por sensor: id, hos, system_id, thing_id, `thing_token_present` (bool — no expone el token),
  `platform_last_seen` (de los raw de Fase 1), `resources` (lista de resultados por recurso),
  `has_any_resource`, `has_real_data`, `last_seen`, `errors_count`
- `summary_by_system`: conteos por sistema
- `errors`: lista de errores globales

**Lo que NO guarda:**
- El token de TheThings.
- Valores completos de lecturas (solo `last_value_type` y `last_seen`).
- Históricos masivos.

**Script auditoría:** `scripts/audit_thethings_data_health.py`

Lee `thethings_resources_probe.json` y calcula:
- Sensores activos 24h / 7d / 30d / stale >30d
- Recursos únicos detectados
- Top sensores activos
- Sensores sin datos por sistema
- Sensores con errores API

**Genera:**
- `audit_data_health.json` y `audit_data_health.md`
- Copia a `latest/`

---

## Cómo interpretar los informes

### `audit_structure.md`

- `HOS nuevos: 0`, `HOS falta: 0` → master y TheThings alineados estructuralmente.
- Si aparecen HOS nuevos → edificios en TheThings no en master (decidir si importar).
- Si aparecen sensores desaparecidos → master tiene sensores que ya no existen en TheThings.

### `audit_tags.md`

- `Buildings con diferencias: 0` → tags alineados (el master guarda un subconjunto de CU tags).
- `Sensors con diferencias` — esperado: master no almacena tags en sensores; TheThings tiene HOS tags.
- `Tags formato desconocido` — revisar si son nuevos tipos a catalogar.

### `audit_data_health.md`

- `active_24h` → sensores con dato en las últimas 24h.
- `active_7d` → sensores con dato en los últimos 7 días.
- `stale_30d` → sensores sin dato desde hace más de 30 días.
- `no_last_seen` → sensores sin ningún timestamp disponible (puede indicar que el recurso no existe o que nunca han tenido datos).
- La tabla por sistema muestra el porcentaje de cobertura real de datos.

### `sensors_data_cleanup.md`

Informe de depuración generado por `report_sensors_data_cleanup.py`. Cruza el probe de Fase 3 con el master para añadir `building_name`. Pensado para revisión manual: qué sensores mantener, revisar o descartar.

- **Sensores con datos** — lista completa con id, HOS, edificio, sistema, último dato y recurso detectado.
- **Sensores sin datos** — clasificados por motivo: `NO_RESOURCE` (recurso no existe en TheThings), `NO_DATA` (recurso existe pero sin muestras), `ERROR` (error de API).
- **Recurso existe pero sin muestras** — sensores donde el recurso responde 200 pero sin datos históricos.
- **Resumen por sistema** y **por edificio** — para ver cobertura de forma agregada.

```bash
python scripts/report_sensors_data_cleanup.py
```

Genera directamente en `data/thethings_snapshots/latest/` (no crea carpeta timestamped).

---

## Riesgos conocidos

- Si se modifica `MODELS` en `server.py`, actualizar también `RESOURCE_CANDIDATES` en `fetch_thethings_structure.py` y `discover_thethings_resources.py`.
- El alias `latest/` se sobrescribe en cada ejecución. Los snapshots con timestamp nunca se borran.
- El token de TheThings no aparece en ningún archivo generado (se usa `thing_token_present: true/false`).
- `pielh_qa_master.json` nunca se modifica. Verificar con hash SHA256 si hay duda.
- El probe de recursos puede ser lento con muchos sensores (~1564). Usar `--limit-sensors N` primero.
- Si un sistema tiene `RESOURCE_CANDIDATES` vacío, se usa `RESOURCE_DEFAULT` (lista genérica).

---

## Fase 5 — Plan de limpieza dry-run

**Script:** `scripts/plan_duplicate_sensor_cleanup.py`

**Prerequisito:** `reports/audit_duplicate_sensors.json` (salida de `audit_duplicate_sensors.py`)

**Prerequisito opcional:** `data/thethings_snapshots/latest/thethings_resources_probe.json` (para datos de `has_real_data` / `last_seen`). Si no existe, usa el campo `active` del audit.

**Lógica de decisión por clasificación:**

| Clasificación | Condición | Decision | Confianza |
|---|---|---|---|
| SYNC_CONFLICT | 1 sensor con datos reales | KEEP + MARK_LEGACY resto | HIGH |
| SYNC_CONFLICT | >1 con datos, diff >30d | KEEP más reciente + MARK_LEGACY resto | MEDIUM |
| SYNC_CONFLICT | >1 con datos recientes o sin datos | MANUAL_REVIEW todos | LOW |
| REPLACE_CANDIDATE | 1 activo, N inactivos | KEEP activo + MARK_LEGACY inactivos | HIGH |
| REPLACE_CANDIDATE | 0 o >1 activos | MANUAL_REVIEW todos | LOW |
| DUPLICATE_ACTIVE | cualquiera | MANUAL_REVIEW todos | LOW |
| DUPLICATE_INACTIVE | cualquiera | MANUAL_REVIEW todos | LOW |

**Genera:**
- `reports/duplicate_sensor_cleanup_plan.json` — estructura completa por grupo con `decision`, `confidence`, `reason` por sensor
- `reports/duplicate_sensor_cleanup_plan.csv` — tabla plana para revisión manual
- `reports/duplicate_sensor_cleanup_plan.md` — informe legible con resumen y ejemplos

**No modifica:** `pielh_qa_master.json` ni ningún otro archivo de datos.

```bash
python scripts/plan_duplicate_sensor_cleanup.py
```

**Resultado esperado (2026-06-21):**
- 415 grupos analizados
- KEEP: 235 sensores (REPLACE_CANDIDATE + SYNC_CONFLICT con dato único)
- MARK_LEGACY: 287 sensores (propuesta automática con HIGH confidence)
- MANUAL_REVIEW: 469 sensores (DUPLICATE_ACTIVE/INACTIVE + conflictos sin decisión clara)
- HIGH confidence: 235 grupos | LOW confidence: 180 grupos

**Siguiente paso:** Revisar CSV de MANUAL_REVIEW y, para los HIGH confidence, ejecutar `scripts/mark_old_duplicate_sensors.py` tras verificación visual.

---

## Limpieza de duplicados aplicada (2026-06-21)

### Qué se hizo

Se ejecutó `scripts/apply_high_confidence_legacy_marks.py --apply` aplicando las decisiones HIGH confidence del plan.

**Criterios de marcado LEGACY:**
- `decision = MARK_LEGACY` + `confidence = HIGH` en el plan de limpieza
- Aplicado a: REPLACE_CANDIDATE (inactivos sustituidos) + SYNC_CONFLICT con único sensor activo con datos

**Campos añadidos a cada sensor LEGACY:**
```json
{
  "inventory_status": "LEGACY",
  "legacy_reason": "sensor inactivo/sustituido",
  "legacy_marked_at": "2026-06-21T20:02:22.352005+00:00",
  "legacy_source": "duplicate_sensor_cleanup_plan",
  "include": false
}
```

**Campos NO modificados:** `id`, `thing_id`, `thing_token`, `hos`, `system_id`, `raw`

### Resultado

| Concepto | Valor |
|---|---|
| Sensores totales en JSON | 1564 (ninguno borrado) |
| Sensores visibles | 1278 |
| Sensores LEGACY (ocultos) | 286 (18.3%) |
| Sensores con datos reales visibles | 400 |
| Backup | `data/backups/pielh_qa_master_before_high_confidence_legacy_20260621_220222.json` |
| SHA256 antes | `9E4BD2EA87F76541C45F42C71C3D69DBB10747544B871C49A527339AC0E031E6` |
| SHA256 después | `7A5F173E8D305DE2088A77841CB8BE183A37D0293A234DE92FC5D614289E6BC2` |

### Sensores LEGACY por sistema

| Sistema | Total | Visibles | LEGACY |
|---|---|---|---|
| S22 TRANSPORTE PUBLICO | 325 | 238 | 87 |
| S06 AGUA | 257 | 171 | 86 |
| S04 AMBIENTE INTERIOR | 112 | 77 | 35 |
| S02 CONTAMINACIÓN EXTERIOR | 69 | 36 | 33 |
| S05 ELECTRICIDAD | 102 | 70 | 32 |
| S14A METEO | 19 | 13 | 6 |
| S07 GAS | 25 | 21 | 4 |
| S01 RUIDO | 3 | 2 | 1 |
| S24 TRAFICO | 6 | 5 | 1 |
| SIP IPS | 139 | 138 | 1 |

### Pendiente: MANUAL_REVIEW

469 sensores quedan sin decisión automática. Consultar:
- `reports/duplicate_sensor_cleanup_plan.csv` — tabla completa por grupo
- `reports/duplicate_sensor_cleanup_plan.md` — resumen con ejemplos

### Comportamiento en la UI

Por defecto los sensores LEGACY están **ocultos** en:
- mapa (no aparecen marcadores)
- listado de sensores
- contadores del header
- búsquedas

Para mostrarlos: activar **"Mostrar LEGACY"** en la pestaña Sensores.

Los sensores LEGACY aparecen con badge `LEGACY` y opacidad reducida.

### Restaurar un sensor LEGACY incorrectamente marcado

Editar `pielh_qa_master.json` y en el sensor correspondiente (buscar por `thing_id`):
```json
{
  "inventory_status": null,
  "legacy_reason": null,
  "legacy_marked_at": null,
  "legacy_source": null,
  "include": true
}
```

### Auditoría post-limpieza

```bash
python scripts/audit_post_cleanup.py
```

Genera `reports/post_cleanup_audit.{md,json}`.

---

## Confirmación: integridad del master

El master fue modificado solo para añadir campos LEGACY. Verificar integridad:

```bash
# SHA256 actual (PowerShell)
(Get-FileHash "pielh_qa_master.json" -Algorithm SHA256).Hash
# Resultado esperado: 7A5F173E8D305DE2088A77841CB8BE183A37D0293A234DE92FC5D614289E6BC2

# SHA256 pre-limpieza (backup)
(Get-FileHash "data/backups/pielh_qa_master_before_high_confidence_legacy_20260621_220222.json" -Algorithm SHA256).Hash
# Resultado esperado: 9E4BD2EA87F76541C45F42C71C3D69DBB10747544B871C49A527339AC0E031E6
```
