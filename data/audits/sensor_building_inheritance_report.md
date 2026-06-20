# PIELH — Auditoría Herencia Edificio → Sensor

_Generado: 2026-06-20T16:13:19.209222+00:00_

> **Solo lectura.** No se ha modificado ningún dato.

---
## Resumen general

| Métrica | Valor |
|---|---|
| Total sensores | 1564 |
| Sensores con HOS | 1263 |
| Sensores sin HOS (excluidos) | 301 |

---
## Clasificación

| Categoría | Sensores | Descripción |
|---|---|---|
| OK | 1171 | Todos los campos heredados correctamente |
| MISSING_FIELDS | 0 | Campos vacíos en sensor que el edificio sí tiene |
| COORDINATE_MISMATCH | 90 | Coordenadas distintas al edificio |
| MISMATCH_FIELDS | 0 | Campos administrativos en conflicto |
| MISSING_BUILDING | 2 | HOS apunta a edificio inexistente |
| **Auto-corregibles** | **58** | Se pueden rellenar/corregir automáticamente |
| **Revisión manual** | **34** | Requieren decisión humana |

---
## Coordenadas

| Situación | Sensores |
|---|---|
| Sensor sin lat/lon (edificio sí tiene) | 0 |
| Edificio sin lat/lon (sensor sí tiene) | 41 |
| Ambos tienen coords pero difieren | 90 |
| &nbsp;&nbsp;→ Diferencia >100m (revisar antes de sobrescribir) | 32 |
| &nbsp;&nbsp;→ Diferencia <100m (auto-corregible, ruido de redondeo) | 58 |

---
## Top edificios con más sensores afectados

| HOS | Sensores con diferencias |
|---|---|
| HOS047 | 8 |
| HOS003 | 8 |
| HOS069 | 7 |
| HOS154 | 5 |
| HOS130 | 5 |
| HOS141 | 4 |
| HOS132 | 3 |
| HOS151 | 3 |
| HOS142 | 3 |
| HOS059 | 3 |
| HOS054 | 2 |
| HOS050 | 2 |
| HOS049 | 2 |
| HOS004 | 2 |
| HOS026 | 2 |
| HOS029 | 2 |
| HOS033 | 2 |
| HOS035 | 2 |
| HOS034 | 2 |
| HOS030 | 2 |

---
## Por sistema

| Sistema | OK | MISSING_FIELDS | COORD_MISMATCH | MISMATCH | MISSING_BLDG |
|---|---|---|---|---|---|
| S22 | 306 | 0 | 15 | 0 | 2 |
| S06 | 115 | 0 | 2 | 0 | 0 |
| S04 | 104 | 0 | 6 | 0 | 0 |
| S08 | 73 | 0 | 27 | 0 | 0 |
| S21 | 90 | 0 | 6 | 0 | 0 |
| S05 | 91 | 0 | 3 | 0 | 0 |
| SIP | 75 | 0 | 0 | 0 | 0 |
| S02 | 65 | 0 | 2 | 0 | 0 |
| S19 | 65 | 0 | 0 | 0 | 0 |
| S20 | 57 | 0 | 4 | 0 | 0 |
| S09 | 51 | 0 | 2 | 0 | 0 |
| S15 | 14 | 0 | 17 | 0 | 0 |
| S14A | 14 | 0 | 3 | 0 | 0 |
| S13A | 14 | 0 | 0 | 0 | 0 |
| S07 | 13 | 0 | 0 | 0 | 0 |
| S14B | 11 | 0 | 0 | 0 | 0 |
| S24 | 6 | 0 | 0 | 0 | 0 |
| S17 | 3 | 0 | 1 | 0 | 0 |
| S01 | 3 | 0 | 0 | 0 | 0 |
| S23 | 0 | 0 | 2 | 0 | 0 |
| S03 | 1 | 0 | 0 | 0 | 0 |

---
## Muestra: MISSING_BUILDING

- **Hospital General de L'Hospitalet-HOS032** (HOS `HOSPITAL`, sys `S22`)
  - Acción: _revision_manual — HOS invalido_
  - error: HOS 'HOSPITAL' no existe en buildings
- **Hospital de Bellvitge (L1)-HOS084** (HOS `HOSPITAL`, sys `S22`)
  - Acción: _revision_manual — HOS invalido_
  - error: HOS 'HOSPITAL' no existe en buildings

---
## Muestra: COORDINATE_MISMATCH

- **Deixalleria Municipal - HOS132-S02-01 BET00230060** (HOS `HOS132`, sys `S02`)
  - Acción: _revision_manual — sensor a >100m del edificio (posicion fisica propia?)_
  - coords: {'status': 'mismatch', 'dlat': 0.0246413, 'dlon': 0.0119217, 'max_diff': 0.0246413, 'needs_review': True, 'building_lat': 41.349618730784414, 'building_lon': 2.0957683290275684, 'sensor_lat': 41.37426, 'sensor_lon': 2.10769}
- **Deixalleria Municipal - HOS132-S02-01 BET00230060** (HOS `HOS132`, sys `S02`)
  - Acción: _revision_manual — sensor a >100m del edificio (posicion fisica propia?)_
  - coords: {'status': 'mismatch', 'dlat': 0.0246413, 'dlon': 0.0119217, 'max_diff': 0.0246413, 'needs_review': True, 'building_lat': 41.349618730784414, 'building_lon': 2.0957683290275684, 'sensor_lat': 41.37426, 'sensor_lon': 2.10769}
- **HOS047-S04-01** (HOS `HOS047`, sys `S04`)
  - Acción: _revision_manual — sensor a >100m del edificio (posicion fisica propia?)_
  - coords: {'status': 'mismatch', 'dlat': 0.0140793, 'dlon': 0.0036746, 'max_diff': 0.0140793, 'needs_review': True, 'building_lat': 41.351301390285286, 'building_lon': 2.114261566414811, 'sensor_lat': 41.36538072196777, 'sensor_lon': 2.110586996877262}

---
_PIELH Smart City — Auditoría FASE 0 — Solo lectura._