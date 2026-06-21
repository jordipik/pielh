# PIELH — Informe de Salud del Inventario IoT

_Generado: 2026-06-20T22:55:25.568993+00:00_

_Fuente: `thethings_activity_20260620_223934.csv`_

---
## 1. Resumen ejecutivo

| Métrica | Valor |
|---|---|
| Total sensores | 1564 |
| Things válidos | 1564 |
| Things inválidos (token/thing roto) | 0 |
| Sensores activos (24h + 7d) | 238 |
| Sensores con datos | 286 |
| Sensores sin datos | 1277 |
| TOKEN_OR_THING_INVALID | 0 |
| Errores API | 0 |

---
## 2. Sistemas con sensores válidos y datos

| Sistema | Nombre | Total | Válidos | Inválidos | Activos | Con datos | Clase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SIP | IPS | 139 | 139 | 0 | 49 | 50 | **A** |
| S22 | TRANSPORTE PUBLICO | 325 | 325 | 0 | 48 | 48 | **A** |
| S21 | DETECCION HUMOS | 158 | 158 | 0 | 36 | 70 | **A** |
| S02 | CONTAMINACIÓN EXTERIOR | 69 | 69 | 0 | 33 | 33 | **A** |
| S05 | ELECTRICIDAD | 102 | 102 | 0 | 32 | 32 | **A** |
| S04 | AMBIENTE INTERIOR | 112 | 112 | 0 | 27 | 40 | **A** |
| S14A | METEO | 19 | 19 | 0 | 6 | 7 | **A** |
| S07 | GAS | 25 | 25 | 0 | 5 | 5 | **A** |
| S01 | RUIDO | 3 | 3 | 0 | 1 | 1 | **A** |
| S24 | TRAFICO | 6 | 6 | 0 | 1 | 1 | **A** |
| S06 | AGUA | 257 | 257 | 0 | 0 | 0 | **B** |
| S08 | CALDERAS | 107 | 107 | 0 | 0 | 0 | **B** |
| S19 | GAS | 65 | 65 | 0 | 0 | 0 | **B** |
| S20 | INUNDACION | 61 | 61 | 0 | 0 | 0 | **B** |
| S09 | CLIMATIZACIÓN | 53 | 53 | 0 | 0 | 0 | **B** |
| S15 | PRESENCIA | 31 | 31 | 0 | 0 | 0 | **B** |
| S13A | SOSTENIBILIDAD EDIFICIOS | 14 | 14 | 0 | 0 | 0 | **B** |
| S14B | METEO SENSOR | 11 | 11 | 0 | 0 | 0 | **B** |
| S17 | AFORO | 4 | 4 | 0 | 0 | 0 | **B** |
| S23 | PARKING | 2 | 2 | 0 | 0 | 0 | **B** |
| S03 | GAS RADON | 1 | 1 | 0 | 0 | 0 | **B** |

---
## 3. Sistemas con tokens rotos (>50% inválidos)

_Ningún sistema supera el 50% de tokens inválidos._

---
## 4. Sistemas recomendados para demo

_Criterio: ACTIVE\_24H + ACTIVE\_7D > 0, ordenados por sensores activos._

| Sistema | Nombre | Activos | ACTIVE\_24H | ACTIVE\_7D | Con datos | Total |
|---|---|---|---|---|---|---|
| SIP | IPS | 49 | 45 | 4 | 50 | 139 |
| S22 | TRANSPORTE PUBLICO | 48 | 48 | 0 | 48 | 325 |
| S21 | DETECCION HUMOS | 36 | 33 | 3 | 70 | 158 |
| S02 | CONTAMINACIÓN EXTERIOR | 33 | 33 | 0 | 33 | 69 |
| S05 | ELECTRICIDAD | 32 | 29 | 3 | 32 | 102 |
| S04 | AMBIENTE INTERIOR | 27 | 20 | 7 | 40 | 112 |
| S14A | METEO | 6 | 6 | 0 | 7 | 19 |
| S07 | GAS | 5 | 4 | 1 | 5 | 25 |
| S01 | RUIDO | 1 | 1 | 0 | 1 | 3 |
| S24 | TRAFICO | 1 | 1 | 0 | 1 | 6 |

---
## 5. KPIs demo

| KPI | Valor |
|---|---|
| demo\_ready\_sensors | 238 |
| demo\_ready\_systems | 10 |
| demo\_ready\_percent | 15.2% |

---
## 6. Clasificación completa A / B / C

| Clase | Criterio |
|---|---|
| **A** — Operativo | ACTIVE\_24H + ACTIVE\_7D > 0 |
| **B** — Recuperable | Things válidos existentes, datos o tokens a renovar |
| **C** — Roto | >80% inválidos, 0 activos, 0 datos |

| Sistema | Nombre | Clase | Total | Válidos | Inválidos | Activos | Con datos |
|---|---|---|---|---|---|---|---|
| S01 | RUIDO | **A** | 3 | 3 | 0 | 1 | 1 |
| S02 | CONTAMINACIÓN EXTERIOR | **A** | 69 | 69 | 0 | 33 | 33 |
| S03 | GAS RADON | B | 1 | 1 | 0 | 0 | 0 |
| S04 | AMBIENTE INTERIOR | **A** | 112 | 112 | 0 | 27 | 40 |
| S05 | ELECTRICIDAD | **A** | 102 | 102 | 0 | 32 | 32 |
| S06 | AGUA | B | 257 | 257 | 0 | 0 | 0 |
| S07 | GAS | **A** | 25 | 25 | 0 | 5 | 5 |
| S08 | CALDERAS | B | 107 | 107 | 0 | 0 | 0 |
| S09 | CLIMATIZACIÓN | B | 53 | 53 | 0 | 0 | 0 |
| S13A | SOSTENIBILIDAD EDIFICIOS | B | 14 | 14 | 0 | 0 | 0 |
| S14A | METEO | **A** | 19 | 19 | 0 | 6 | 7 |
| S14B | METEO SENSOR | B | 11 | 11 | 0 | 0 | 0 |
| S15 | PRESENCIA | B | 31 | 31 | 0 | 0 | 0 |
| S17 | AFORO | B | 4 | 4 | 0 | 0 | 0 |
| S19 | GAS | B | 65 | 65 | 0 | 0 | 0 |
| S20 | INUNDACION | B | 61 | 61 | 0 | 0 | 0 |
| S21 | DETECCION HUMOS | **A** | 158 | 158 | 0 | 36 | 70 |
| S22 | TRANSPORTE PUBLICO | **A** | 325 | 325 | 0 | 48 | 48 |
| S23 | PARKING | B | 2 | 2 | 0 | 0 | 0 |
| S24 | TRAFICO | **A** | 6 | 6 | 0 | 1 | 1 |
| SIP | IPS | **A** | 139 | 139 | 0 | 49 | 50 |

---
_PIELH Smart City — Auditoría FASE 0 — Solo lectura._