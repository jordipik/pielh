# Plan de Limpieza de Sensores Duplicados (Dry-Run)

- Generado: 2026-06-21T21:55:58.339719
- Auditoria base: `audit_duplicate_sensors.json`
- **master_modified: false** — solo lectura, ningun dato modificado

## Resumen ejecutivo

| Concepto | Valor |
|---|---|
| Grupos analizados | 415 |
| Sensores propuestos KEEP | 235 |
| Sensores propuestos MARK_LEGACY | 287 |
| Sensores enviados a MANUAL_REVIEW | 469 |
| Decisiones HIGH confidence | 235 |
| Decisiones MEDIUM confidence | 0 |
| Decisiones LOW confidence | 180 |

## Conteos por clasificacion

| Clasificacion | Grupos | Sensores KEEP | MARK_LEGACY | MANUAL_REVIEW |
|---|---|---|---|---|
| DUPLICATE_ACTIVE | 7 | 0 | 0 | 26 |
| DUPLICATE_INACTIVE | 102 | 0 | 0 | 286 |
| REPLACE_CANDIDATE | 75 | 75 | 114 | 0 |
| SYNC_CONFLICT | 231 | 160 | 173 | 157 |

## Casos HIGH confidence con decision automatica (max 20)

| Grupo | Clase | HOS | Sistema | Decision |
|---|---|---|---|---|
| `I17BE085778O` | SYNC_CONFLICT |  | S06 | KEEP I17BE085778O (unico con datos) |
| `H23VA083135U` | SYNC_CONFLICT |  | S06 | KEEP H23VA083135U (unico con datos) |
| `I18BD012202M` | SYNC_CONFLICT |  | S06 | KEEP I18BD012202M (unico con datos) |
| `I22BC092123D` | SYNC_CONFLICT |  | S06 | KEEP I22BC092123D (unico con datos) |
| `I22BC056178O` | SYNC_CONFLICT |  | S06 | KEEP I22BC056178O (unico con datos) |
| `I22BC022199O` | SYNC_CONFLICT |  | S06 | KEEP I22BC022199O (unico con datos) |
| `Esc. Joaquim Ruyra - HOS046` | SYNC_CONFLICT | HOS046 | S07 | KEEP Esc. Joaquim Ruyra - HOS046 (unico con datos) |
| `HOS044-S01-01` | SYNC_CONFLICT | HOS044 | S01 | KEEP HOS044-S01-01 (unico con datos) |
| `HOS508-S02-01 BET00230064` | SYNC_CONFLICT | HOS508 | S02 | KEEP HOS508-S02-01 BET00230064 (unico con datos) |
| `Deixalleria Municipal - HOS132-S02-01 BET00230060` | SYNC_CONFLICT | HOS132 | S02 | KEEP Deixalleria Municipal - HOS132 (unico con datos) |
| `HOS024-S02-01-BET00230039` | SYNC_CONFLICT | HOS024 | S02 | KEEP HOS024-S02-01-BET00230039 (unico con datos) |
| `BET00230154` | SYNC_CONFLICT |  | S02 | KEEP BET00230154 (unico con datos) |
| `HOS128-S02-01 BET00230038` | SYNC_CONFLICT | HOS128 | S02 | KEEP HOS128-S02-01 BET00230038 (unico con datos) |
| `HOS520-S02-01 BET00230151` | SYNC_CONFLICT | HOS520 | S02 | KEEP HOS520-S02-01 BET00230151 (unico con datos) |
| `HOS521-S02-01 BET00230152` | SYNC_CONFLICT | HOS521 | S02 | KEEP HOS521-S02-01 BET00230152 (unico con datos) |
| `HOS105-S02-01 BET00230045` | SYNC_CONFLICT | HOS105 | S02 | KEEP HOS105-S02-01 BET00230045 (unico con datos) |
| `HOS157-S02-01 BET00230040` | SYNC_CONFLICT | HOS157 | S02 | KEEP HOS157-S02-01 BET00230040 (unico con datos) |
| `HOS504-S02-01 BET00230059` | SYNC_CONFLICT | HOS504 | S02 | KEEP HOS504-S02-01 BET00230059 (unico con datos) |
| `HOS522-S02-01 BET00230153` | SYNC_CONFLICT | HOS522 | S02 | KEEP HOS522-S02-01 BET00230153 (unico con datos) |
| `HOS103-S02-01 BET00230036` | SYNC_CONFLICT | HOS103 | S02 | KEEP HOS103-S02-01 BET00230036 (unico con datos) |

### Detalle ejemplos HIGH confidence (5 primeros)

**`I17BE085778O`** — SYNC_CONFLICT — HIGH
_KEEP I17BE085778O (unico con datos)_

| id | thing_id | has_data | last_seen | decision | razon |
|---|---|---|---|---|---|
| I17BE085778O | bvDyRLP6B4Ena6VIHWZx6DLinEAJ | SI | 2026-06-19 | **KEEP** | unico sensor con datos reales |
| I17BE085778O | 7TnMajRCyaJhcGkzO9DWsi7zp004 | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I17BE085778O | y3SUvmcY87NtRsooY_rXxoXvd3_v | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I17BE085778O | YlItyWsROEa_UW-xU4lmeRf3n2Oq | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I17BE085778O | 5yoe5uUPfAeQP6RGoOzErp7U8eUg | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I17BE085778O | OSBz9gHsfpCZFsNN-nOtWp77KdnI | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |

**`H23VA083135U`** — SYNC_CONFLICT — HIGH
_KEEP H23VA083135U (unico con datos)_

| id | thing_id | has_data | last_seen | decision | razon |
|---|---|---|---|---|---|
| H23VA083135U | c6cRV_3BOt29TcJplk7B0yUWZ3mP | SI | 2026-06-20 | **KEEP** | unico sensor con datos reales |
| H23VA083135U | Uo7BXvGh-uS0_toA8JkS8RjMPFUV | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| H23VA083135U | i1DiJjhlw8xBUUdeDKr_QDKwqf9a | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| H23VA083135U | lyEkpPhU7grfnxCVNVTIA0LFb2h6 | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| H23VA083135U | _1AKrmXDbKj2-d4d-77mC-tB93x9 | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |

**`I18BD012202M`** — SYNC_CONFLICT — HIGH
_KEEP I18BD012202M (unico con datos)_

| id | thing_id | has_data | last_seen | decision | razon |
|---|---|---|---|---|---|
| I18BD012202M | JFA4pbO-LVPuQ-GjAfGirqnX7RCM | SI | 2026-06-17 | **KEEP** | unico sensor con datos reales |
| I18BD012202M | Blq7xEEmop51cHn_hZD6_7snMmJO | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I18BD012202M | s7HX76CPNimXDeExfhesgMap55Iq | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I18BD012202M | zu1e7LuxR6pCllwJQdCEqmqbIt9H | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |

**`I22BC092123D`** — SYNC_CONFLICT — HIGH
_KEEP I22BC092123D (unico con datos)_

| id | thing_id | has_data | last_seen | decision | razon |
|---|---|---|---|---|---|
| I22BC092123D | kqS0ZopvD9SVwPOyYhKqFGF100pn | SI | 2026-06-07 | **KEEP** | unico sensor con datos reales |
| I22BC092123D | IL7NXBSvpddGpqyKq1eX41ezmzWM | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I22BC092123D | wKYgEL79xi9cyLpmcit9FEkW1D_B | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |

**`I22BC056178O`** — SYNC_CONFLICT — HIGH
_KEEP I22BC056178O (unico con datos)_

| id | thing_id | has_data | last_seen | decision | razon |
|---|---|---|---|---|---|
| I22BC056178O | ChkWbVIZ1VivtdjBeSi50NCQ95M_ | SI | 2026-06-07 | **KEEP** | unico sensor con datos reales |
| I22BC056178O | Lya7cUqq9pylVSXwCD5pyYcCet5O | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |
| I22BC056178O | h4a_hExT5sahbPAvoXCiknzWVJKv | NO | — | **MARK_LEGACY** | sin datos reales, sustituido |

## Casos MANUAL_REVIEW (max 10 ejemplos)

| Grupo | Clase | HOS | Sistema | Sensores | Razon |
|---|---|---|---|---|---|
| `HOS125` | SYNC_CONFLICT | HOS125 | S04 | 7 | varios activos con datos recientes (diff 5d si disponible) |
| `Esc. Patufet Sant Jordi-HOS056` | SYNC_CONFLICT | HOS056 | S05 | 7 | ninguno tiene datos y puntuacion identica |
| `HOS041` | SYNC_CONFLICT | HOS041 | S08 | 5 | varios activos con datos recientes (diff 12d si disponible) |
| `HOS041|S21` | DUPLICATE_ACTIVE | HOS041 | S21 | 5 | mas de un sensor activo en mismo HOS+sistema |
| `HOS033|S04` | DUPLICATE_ACTIVE | HOS033 | S04 | 4 | mas de un sensor activo en mismo HOS+sistema |
| `HOS099|S21` | DUPLICATE_ACTIVE | HOS099 | S21 | 4 | mas de un sensor activo en mismo HOS+sistema |
| `HOS005|S21` | DUPLICATE_ACTIVE | HOS005 | S21 | 4 | mas de un sensor activo en mismo HOS+sistema |
| `HOS099` | SYNC_CONFLICT | HOS099 | S21 | 3 | varios activos con datos recientes (diff 10d si disponible) |
| `HOS005` | SYNC_CONFLICT | HOS005 | S21 | 3 | varios activos con datos recientes (diff 10d si disponible) |
| `HOS034|S04` | DUPLICATE_ACTIVE | HOS034 | S04 | 3 | mas de un sensor activo en mismo HOS+sistema |

## Advertencias

- 231 grupos SYNC_CONFLICT: mismo ID visible asignado a things distintos. Riesgo de escritura contra thing incorrecto en sync.
- 7 grupos DUPLICATE_ACTIVE: dos o mas sensores activos para mismo HOS+sistema. Revisar manualmente cual es el dispositivo real.
- Los sensores MARK_LEGACY propuestos NO han sido modificados. Este es un plan dry-run.

## Siguiente paso recomendado

1. Revisar los `MANUAL_REVIEW` manualmente usando el CSV generado.
2. Para los HIGH confidence, ejecutar `scripts/mark_old_duplicate_sensors.py`    tras verificacion visual de una muestra.
3. Para DUPLICATE_ACTIVE, identificar el thing_id correcto en TheThings antes de actuar.

---
JSON: `reports/duplicate_sensor_cleanup_plan.json`
CSV:  `reports/duplicate_sensor_cleanup_plan.csv`