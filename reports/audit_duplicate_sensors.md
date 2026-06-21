# Auditoria de Sensores Duplicados y Sustituciones

- Generado: 2026-06-21T21:47:53.887711
- Master: `pielh_qa_master.json`  |  master_modified: **false**

## Resumen ejecutivo

| Concepto | Valor |
|---|---|
| Total sensores analizados | 1564 |
| Total incidencias detectadas | 415 |
| Sensores implicados en alguna incidencia | 693 |
| CRITICAL | 238 |
| HIGH | 75 |
| MEDIUM | 17 |
| LOW | 85 |

## Tabla de incidencias por categoria

| Clasificacion | Descripcion | Total |
|---|---|---|
| SYNC_CONFLICT | Mismo ID de texto, things distintos | 231 |
| DUPLICATE_ACTIVE | 2+ activos en mismo HOS+sistema | 7 |
| REPLACE_CANDIDATE | Activo + inactivo, things distintos (sustitucion) | 75 |
| LIKELY_REPLACED | Activo + inactivo, mismo thing (datos duplicados) | 0 |
| DUPLICATE_INACTIVE | Todos inactivos, HOS+sistema compartido | 102 |

## Deteccion por metodo

| Metodo | Grupos | Descripcion |
|---|---|---|
| same_id | 231 | Mismo texto de sensor ID |
| same_thing_id | 0 | Mismo thing_id de TheThings |
| same_token | 0 | Mismo thing_token de TheThings |
| same_hos_system_id | 324 | Mismo edificio HOS y sistema |

## Top 50 incidencias criticas / de mayor riesgo

| # | Riesgo | Clasificacion | Grupo | Sensores | Activos | Geo (m) | Sim nombre |
|---|---|---|---|---|---|---|---|
| 1 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS125` | 7 | 4 | — | 1.00 |
| 2 | 🔴 CRITICAL | SYNC_CONFLICT | `Esc. Patufet Sant Jordi-HOS056` | 7 | 0 | 0.0 | 1.00 |
| 3 | 🔴 CRITICAL | SYNC_CONFLICT | `I17BE085778O` | 6 | 0 | — | 1.00 |
| 4 | 🔴 CRITICAL | SYNC_CONFLICT | `H23VA083135U` | 5 | 0 | — | 1.00 |
| 5 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS041` | 5 | 2 | — | 1.00 |
| 6 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS041|S21` | 5 | 2 | — | 1.00 |
| 7 | 🔴 CRITICAL | SYNC_CONFLICT | `I18BD012202M` | 4 | 0 | — | 1.00 |
| 8 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS033|S04` | 4 | 2 | 0.0 | 0.92 |
| 9 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS099|S21` | 4 | 2 | — | 1.00 |
| 10 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS005|S21` | 4 | 2 | — | 1.00 |
| 11 | 🔴 CRITICAL | SYNC_CONFLICT | `I22BC092123D` | 3 | 0 | — | 1.00 |
| 12 | 🔴 CRITICAL | SYNC_CONFLICT | `I22BC056178O` | 3 | 0 | — | 1.00 |
| 13 | 🔴 CRITICAL | SYNC_CONFLICT | `I22BC022199O` | 3 | 0 | — | 1.00 |
| 14 | 🔴 CRITICAL | SYNC_CONFLICT | `Esc. Joaquim Ruyra - HOS046` | 3 | 1 | 0.0 | 1.00 |
| 15 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS099` | 3 | 2 | — | 1.00 |
| 16 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS005` | 3 | 2 | — | 1.00 |
| 17 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS034|S04` | 3 | 2 | — | 1.00 |
| 18 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS037|S21` | 3 | 2 | — | 1.00 |
| 19 | 🔴 CRITICAL | DUPLICATE_ACTIVE | `HOS125|S21` | 3 | 2 | — | 1.00 |
| 20 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS044-S01-01` | 2 | 1 | 0.0 | 1.00 |
| 21 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS508-S02-01 BET00230064` | 2 | 1 | 0.0 | 1.00 |
| 22 | 🔴 CRITICAL | SYNC_CONFLICT | `Deixalleria Municipal - HOS132-S02-01 BET00230060` | 2 | 1 | 0.0 | 1.00 |
| 23 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS024-S02-01-BET00230039` | 2 | 1 | 0.0 | 1.00 |
| 24 | 🔴 CRITICAL | SYNC_CONFLICT | `BET00230154` | 2 | 1 | — | 1.00 |
| 25 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS128-S02-01 BET00230038` | 2 | 1 | 0.0 | 1.00 |
| 26 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS520-S02-01 BET00230151` | 2 | 1 | 0.0 | 1.00 |
| 27 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS521-S02-01 BET00230152` | 2 | 1 | 0.0 | 1.00 |
| 28 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS105-S02-01 BET00230045` | 2 | 1 | 0.0 | 1.00 |
| 29 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS157-S02-01 BET00230040` | 2 | 1 | 0.0 | 1.00 |
| 30 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS504-S02-01 BET00230059` | 2 | 1 | — | 1.00 |
| 31 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS522-S02-01 BET00230153` | 2 | 1 | 0.0 | 1.00 |
| 32 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS103-S02-01 BET00230036` | 2 | 1 | 0.0 | 1.00 |
| 33 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS514-S02-01 BET00230145` | 2 | 1 | 0.0 | 1.00 |
| 34 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS503-S02-01 BET00230058` | 2 | 1 | 0.0 | 1.00 |
| 35 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS507-S02-01 BET00230063` | 2 | 1 | 0.0 | 1.00 |
| 36 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS517-S02-01 BET00230148` | 2 | 1 | 0.0 | 1.00 |
| 37 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS137-S02-01 BET00230037` | 2 | 1 | 0.0 | 1.00 |
| 38 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS502-S02-01 BET00230027` | 2 | 1 | 0.0 | 1.00 |
| 39 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS134-S02-01 BET00230041` | 2 | 1 | 0.0 | 1.00 |
| 40 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS510-S02-01 BET00230066` | 2 | 1 | 0.0 | 1.00 |
| 41 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS518-S02-01 BET00230149` | 2 | 1 | 0.0 | 1.00 |
| 42 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS509-S02-01 BET00230065` | 2 | 1 | 0.0 | 1.00 |
| 43 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS102-S02-01 BET00230042` | 2 | 1 | 0.0 | 1.00 |
| 44 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS515-S02-01 BET00230146` | 2 | 1 | 0.0 | 1.00 |
| 45 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS519-S02-01 BET00230150` | 2 | 1 | 0.0 | 1.00 |
| 46 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS511-S02-01 BET00230067` | 2 | 1 | 0.0 | 1.00 |
| 47 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS104-S02-01 BET00230044` | 2 | 1 | 0.0 | 1.00 |
| 48 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS513-S02-01 BET00230144` | 2 | 1 | 0.0 | 1.00 |
| 49 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS505-S02-01 BET00230061` | 2 | 1 | 0.0 | 1.00 |
| 50 | 🔴 CRITICAL | SYNC_CONFLICT | `HOS512-S02-01 BET00230068` | 2 | 1 | 0.0 | 1.00 |

## Detalle ejemplos CRITICAL / HIGH (max 20)

### [CRITICAL] `HOS125` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 7 | Activos: 4 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS125 | HxqFoabN_Off1zb_jHZmSSZEy_waWo | SI | 2026-06-14T08:45:19 | 7 |
| HOS125 | GkNv-eqtzBCeoUUVIGUEhjmDFOZkAA | SI | 2026-06-14T08:48:59 | 7 |
| HOS125 | 8UrJXULhdS1lEJBVWiygwML09DlkN0 | NO | — | ? |
| HOS125 | FUc4wPJ1LGvMtHEurQAwmy34KU3fGJ | NO | — | ? |
| HOS125 | _hFS8aJzm2H4HMBxTDO6ZGUMvrcxRl | NO | — | ? |
| HOS125 | rYmgj3Mo4yrZKr5rjB1Mv7UOgdj0Cl | SI | 2026-06-10T12:14:07 | 11 |
| HOS125 | 8CteMRvWB6hEMJwCc6vJqrxHyarTuF | SI | 2026-06-13T12:14:06 | 8 |

### [CRITICAL] `Esc. Patufet Sant Jordi-HOS056` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 7 | Activos: 0 | Inactivos: 7
- Distancia minima: 0.0 m
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| Esc. Patufet Sant Jordi-HOS056 | gU6QtsH-W3RIwAWn-5xfKhGBfkwA9J | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | uUkVyKf__21jKoPlkvfN9rIm8SbPMH | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | RymKKw5lFTB21OZ69rA5gVJgEsEb-U | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | iThkjcej5ejN-mlaT1Lz71L0tLXvkz | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | J2myS3z26Rrk1ubm439sAH8HtlVF6f | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | f7xWoXcDYvJXcOjNvic5IZFkdMoDN6 | NO | — | ? |
| Esc. Patufet Sant Jordi-HOS056 | vpSOVLMYSkfmQx7Iu0sY01rPq01_AS | NO | — | ? |

### [CRITICAL] `I17BE085778O` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 6 | Activos: 0 | Inactivos: 6
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| I17BE085778O | bvDyRLP6B4Ena6VIHWZx6DLinEAJ4B | NO | — | ? |
| I17BE085778O | 7TnMajRCyaJhcGkzO9DWsi7zp004Z7 | NO | — | ? |
| I17BE085778O | y3SUvmcY87NtRsooY_rXxoXvd3_vfL | NO | — | ? |
| I17BE085778O | YlItyWsROEa_UW-xU4lmeRf3n2OqSh | NO | — | ? |
| I17BE085778O | 5yoe5uUPfAeQP6RGoOzErp7U8eUgUY | NO | — | ? |
| I17BE085778O | OSBz9gHsfpCZFsNN-nOtWp77KdnIUb | NO | — | ? |

### [CRITICAL] `H23VA083135U` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 5 | Activos: 0 | Inactivos: 5
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| H23VA083135U | c6cRV_3BOt29TcJplk7B0yUWZ3mPna | NO | — | ? |
| H23VA083135U | Uo7BXvGh-uS0_toA8JkS8RjMPFUVhO | NO | — | ? |
| H23VA083135U | i1DiJjhlw8xBUUdeDKr_QDKwqf9abm | NO | — | ? |
| H23VA083135U | lyEkpPhU7grfnxCVNVTIA0LFb2h6gH | NO | — | ? |
| H23VA083135U | _1AKrmXDbKj2-d4d-77mC-tB93x969 | NO | — | ? |

### [CRITICAL] `HOS041` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 5 | Activos: 2 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS041 | TlRJtyhgPzypbmzl9JjCqRBxIiIGIa | NO | — | ? |
| HOS041 | OAEm-hYWRV1MhIpV5mFYMb1O-22RIu | SI | 2026-06-20T07:30:36 | 1 |
| HOS041 | cCrXmxE29M0zkTKmTKgx6bfmxseK9E | SI | 2026-06-11T07:30:45 | 10 |
| HOS041 | Lv5on0rGTo6xAcBoarsFxi2BH1_bfo | NO | — | ? |
| HOS041 | _dH2w7KP5ovEx5y9z9r28835iqaysV | NO | — | ? |

### [CRITICAL] `HOS041|S21` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 5 | Activos: 2 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS041 | OAEm-hYWRV1MhIpV5mFYMb1O-22RIu | SI | 2026-06-20T07:30:36 | 1 |
| HOS041 | cCrXmxE29M0zkTKmTKgx6bfmxseK9E | SI | 2026-06-11T07:30:45 | 10 |
| HOS041 | Lv5on0rGTo6xAcBoarsFxi2BH1_bfo | NO | — | ? |
| HOS041 | _dH2w7KP5ovEx5y9z9r28835iqaysV | NO | — | ? |
| HOS041-S21-01 | kZHrR6nJix6V4aDj096D9HcuG4YWJd | NO | — | ? |

### [CRITICAL] `I18BD012202M` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 4 | Activos: 0 | Inactivos: 4
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| I18BD012202M | JFA4pbO-LVPuQ-GjAfGirqnX7RCM8F | NO | — | ? |
| I18BD012202M | Blq7xEEmop51cHn_hZD6_7snMmJOPM | NO | — | ? |
| I18BD012202M | s7HX76CPNimXDeExfhesgMap55IqIK | NO | — | ? |
| I18BD012202M | zu1e7LuxR6pCllwJQdCEqmqbIt9HNy | NO | — | ? |

### [CRITICAL] `HOS033|S04` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 4 | Activos: 2 | Inactivos: 2
- Distancia minima: 0.0 m
- Similitud nombre: 0.92

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| S4E-HOS033-1 | Cf-b6ps2YNjPvXGK9XW6YrKIZkATy3 | SI | 2026-06-20T22:38:42 | 0 |
| S4E-HOS033 | MH5SO0NuQaHC5s-m1QgG09t3ZUt-BE | SI | 2026-06-20T22:38:42 | 0 |
| HOS033-S04-02 | 49ZBJTtH3ae4cYsJDTRgZJDPel-nOw | NO | — | ? |
| HOS033-S04-01 | WSugBd3UdvMi376ZOb9dqEbYyh2KBP | NO | — | ? |

### [CRITICAL] `HOS099|S21` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 4 | Activos: 2 | Inactivos: 2
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS099 | JY_AV0vvQGdprWUakd7ZbqFQXoAssE | SI | 2026-06-20T12:09:17 | 1 |
| HOS099 | jrxI1ckQNg4vpY5z3BOr-5TFEnWsce | SI | 2026-06-10T12:09:26 | 11 |
| HOS099 | 81oWGqUDRKW-KrWCRlAPZfiAiZdBJK | NO | — | ? |
| HOS099-S21-01 | 0puxxgrwGHbHExKVUeHXVSY1rPmO1f | NO | — | ? |

### [CRITICAL] `HOS005|S21` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 4 | Activos: 2 | Inactivos: 2
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS005 | PUUgtwBtrgURPILjWNqi7NVauPzMa9 | SI | 2026-06-20T09:07:06 | 1 |
| HOS005 | Nm-I6lRYsH0XWcYcYl-C2ILfDmuL_Y | SI | 2026-06-11T09:07:24 | 10 |
| HOS005 | 25fyMYitYqfEItY5xOJTyY6vq9B7lL | NO | — | ? |
| HOS005-S21-01 | FFbQxmKdbPT1LiJdW2hnR3wdq_cJT6 | NO | — | ? |

### [CRITICAL] `I22BC092123D` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 0 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| I22BC092123D | kqS0ZopvD9SVwPOyYhKqFGF100pnBU | NO | — | ? |
| I22BC092123D | IL7NXBSvpddGpqyKq1eX41ezmzWMyr | NO | — | ? |
| I22BC092123D | wKYgEL79xi9cyLpmcit9FEkW1D_B36 | NO | — | ? |

### [CRITICAL] `I22BC056178O` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 0 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| I22BC056178O | ChkWbVIZ1VivtdjBeSi50NCQ95M_TP | NO | — | ? |
| I22BC056178O | Lya7cUqq9pylVSXwCD5pyYcCet5OtK | NO | — | ? |
| I22BC056178O | h4a_hExT5sahbPAvoXCiknzWVJKv1I | NO | — | ? |

### [CRITICAL] `I22BC022199O` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 0 | Inactivos: 3
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| I22BC022199O | GaXU5xo9CEobrWJKKqRn-n526bslA0 | NO | — | ? |
| I22BC022199O | 363WV9xYkL88DI9XaYY4bZtcL-J8ww | NO | — | ? |
| I22BC022199O | 1GjOoR4KLympzI9aHUit9kNO_gI2rE | NO | — | ? |

### [CRITICAL] `Esc. Joaquim Ruyra - HOS046` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 1 | Inactivos: 2
- Distancia minima: 0.0 m
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| Esc. Joaquim Ruyra - HOS046 | j3jiSpRPggHMLz7j8YtkIipatMVGHh | SI | 2026-06-20T08:50:32 | 1 |
| Esc. Joaquim Ruyra - HOS046 | FtZk8-T-9e3bwYjF8useUBLqv2tTwD | NO | — | ? |
| Esc. Joaquim Ruyra - HOS046 | COINlvOVgEJSvetVBSBFVNuWxCR2oY | NO | — | ? |

### [CRITICAL] `HOS099` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 2 | Inactivos: 1
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS099 | JY_AV0vvQGdprWUakd7ZbqFQXoAssE | SI | 2026-06-20T12:09:17 | 1 |
| HOS099 | jrxI1ckQNg4vpY5z3BOr-5TFEnWsce | SI | 2026-06-10T12:09:26 | 11 |
| HOS099 | 81oWGqUDRKW-KrWCRlAPZfiAiZdBJK | NO | — | ? |

### [CRITICAL] `HOS005` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 3 | Activos: 2 | Inactivos: 1
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS005 | PUUgtwBtrgURPILjWNqi7NVauPzMa9 | SI | 2026-06-20T09:07:06 | 1 |
| HOS005 | Nm-I6lRYsH0XWcYcYl-C2ILfDmuL_Y | SI | 2026-06-11T09:07:24 | 10 |
| HOS005 | 25fyMYitYqfEItY5xOJTyY6vq9B7lL | NO | — | ? |

### [CRITICAL] `HOS034|S04` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 3 | Activos: 2 | Inactivos: 1
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| S4E-HOS034 | yJLYrIKoPdIeCSTXSlzRde0pJHZx9n | SI | 2026-06-20T05:55:42 | 1 |
| S4E-HOS034 | OGW8gpuDCp21SzNSrACArtRblkejEj | SI | 2026-06-10T11:03:42 | 11 |
| HOS034-S04-01 | 1Nv34WONkSAjWMl9yyXE2-8TGPuSix | NO | — | ? |

### [CRITICAL] `HOS037|S21` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 3 | Activos: 2 | Inactivos: 1
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS037 | FiCd7-BzVYpdRl8ZgH0jIQcpDriz3G | SI | 2026-06-20T09:10:24 | 1 |
| HOS037 | _ae2PDx-p9CkKyeJNr88aOSVwsSv_j | SI | 2026-06-11T09:10:35 | 10 |
| HOS037-S21-01 | -pcVBoEjXxaiy8IEsoLvYsk9VurIWH | NO | — | ? |

### [CRITICAL] `HOS125|S21` — DUPLICATE_ACTIVE
- Deteccion: `same_hos_system_id` | Sensores: 3 | Activos: 2 | Inactivos: 1
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS125 | rYmgj3Mo4yrZKr5rjB1Mv7UOgdj0Cl | SI | 2026-06-10T12:14:07 | 11 |
| HOS125 | 8CteMRvWB6hEMJwCc6vJqrxHyarTuF | SI | 2026-06-13T12:14:06 | 8 |
| HOS125-S21-01 | akoDVfszm-IpXbMswnFTNw18seQSiy | NO | — | ? |

### [CRITICAL] `HOS044-S01-01` — SYNC_CONFLICT
- Deteccion: `same_id` | Sensores: 2 | Activos: 1 | Inactivos: 1
- Distancia minima: 0.0 m
- Similitud nombre: 1.00

| sensor id | thing_id | activo | last_seen | dias |
|---|---|---|---|---|
| HOS044-S01-01 | SnHdcxnnzpD1Z79Dvxs_8O-CkgSE79 | SI | 2026-06-20T22:39:16 | 0 |
| HOS044-S01-01 | suj9PiI4JbekaYqNnsbjaQY2kR1TrC | NO | — | ? |

## Recomendacion de limpieza

**PRECAUCION**: 238 incidencias CRITICAL detectadas.

- `SYNC_CONFLICT`: Mismo ID de texto asignado a things distintos. Puede causar errores 404 en sincronizacion con TheThings. Revisar manualmente y renombrar el registro incorrecto.

- `DUPLICATE_ACTIVE`: Dos sensores activos para el mismo HOS+sistema. Determinar cual es el dispositivo real y marcar el otro como OLD.

**AVISO**: 75 incidencias HIGH (`REPLACE_CANDIDATE`).
Probable sustitucion de dispositivo. El sensor inactivo puede marcarse como OLD usando `scripts/mark_old_duplicate_sensors.py` tras verificacion manual.

---
CSV compatibilidad: `reports/duplicate_sensors_audit.csv`
JSON completo     : `reports/audit_duplicate_sensors.json`