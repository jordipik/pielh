# PIELH FASE 0 — Auditoría IoT TheThings

## Objetivo

Script de solo lectura que cruza `pielh_qa_master.json` con la API real de TheThings para detectar qué sensores transmiten datos y con qué antigüedad.

No modifica ningún archivo de datos.

---

## Cómo ejecutarlo

```bash
# Auditar todos los sensores (puede tardar varios minutos)
python scripts/audit_thethings_activity.py --no-ssl-verify

# Solo los 20 primeros
python scripts/audit_thethings_activity.py --limit 20 --no-ssl-verify

# Solo sensores de ruido (S01)
python scripts/audit_thethings_activity.py --system S01 --no-ssl-verify

# Solo sensores de un edificio
python scripts/audit_thethings_activity.py --hos HOS001 --no-ssl-verify

# Pausa más lenta entre peticiones (por defecto 0.2s)
python scripts/audit_thethings_activity.py --sleep 0.5 --no-ssl-verify
```

---

## Salidas generadas

Todas en `data/audits/` con timestamp `YYYYMMDD_HHMMSS`:

| Archivo | Contenido |
|---|---|
| `thethings_activity_TIMESTAMP.json` | Resultado completo por sensor (incluye `raw_sample`) |
| `thethings_activity_TIMESTAMP.csv` | Tabla plana, abrir en Excel |
| `thethings_activity_summary_TIMESTAMP.json` | Contadores globales + desglose por sistema, distrito y barrio |

`raw_sample` solo aparece en el JSON, no en el CSV.

---

## Interpretación de `active_status`

| Estado | Significado |
|---|---|
| `ACTIVE_24H` | Último dato hace menos de 24 horas — sensor activo |
| `ACTIVE_7D` | Último dato hace 1–7 días — activo pero algo lento |
| `STALE_30D` | Último dato hace 7–30 días — posiblemente problema |
| `STALE_90D` | Último dato hace 30–90 días — sensor degradado |
| `INACTIVE_90D` | Sin datos desde hace más de 90 días — inactivo |
| `DATA_NO_TIMESTAMP` | La API devuelve un valor válido pero sin fecha/hora — el sensor transmite pero no se puede calcular antigüedad |
| `NO_DATA` | La API no devuelve ningún valor legible, o el sensor no tiene `thing_token` |

### Diferencia entre `NO_DATA` y `DATA_NO_TIMESTAMP`

- `NO_DATA`: no se encontró ningún valor en la respuesta de TheThings (o no se llamó a la API por falta de token).
- `DATA_NO_TIMESTAMP`: se encontró un valor numérico (`has_real_value=true`) pero la respuesta no incluye ningún campo de fecha reconocible. El sensor está transmitiendo, pero no se puede calcular cuándo fue el último dato.

---

## Columnas de calidad de dato

### `has_real_value`

| Valor | Significado |
|---|---|
| `true` | La API devolvió un valor numérico para este sensor |
| `false` | No se encontró ningún valor útil |

### `timestamp_status`

| Valor | Significado |
|---|---|
| `OK` | Timestamp encontrado y parseado correctamente |
| `MISSING` | Valor encontrado pero sin campo de fecha en la respuesta |
| `INVALID` | Campo de fecha presente pero con formato no reconocido |
| `NOT_APPLICABLE` | No hay valor — no aplica evaluar el timestamp |

---

## Problemas detectados (`issues`)

| Código | Causa |
|---|---|
| `MISSING_THING_TOKEN` | El sensor no tiene `thing_token` — no se llama a la API |
| `MISSING_THING_ID` | El sensor no tiene `thing_id` |
| `MISSING_HOS` | El sensor no tiene código de edificio |
| `BUILDING_NOT_FOUND` | El HOS del sensor no existe en `buildings[]` |
| `MISSING_COORDS` | Sin latitud/longitud |
| `MISSING_DISTRICT` | Sin nombre de distrito |
| `MISSING_NEIGHBORHOOD` | Sin nombre de barrio |
| `API_ERROR` | Error de red o HTTP al llamar a TheThings |
| `NO_DATA` | La API respondió pero sin valores legibles |

---

## Notas

- El script usa solo librerías estándar de Python (no requiere `pip install`).
- Lee `config.json` de la raíz del proyecto para obtener `thethings_api` y `thethings_token`.
- `--no-ssl-verify` es necesario en entornos locales (igual que en `server.py`).
- Para evitar saturar la API, usa `--sleep 0.2` por defecto entre peticiones.
- El script busca timestamps en múltiples claves: `timestamp`, `ts`, `at`, `datetime`, `date`, `created_at`, `created`, `time`, `recv`, `recvTime`.
