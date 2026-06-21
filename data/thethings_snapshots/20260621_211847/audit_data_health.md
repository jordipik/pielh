# Auditoría Salud de Datos IoT — Fase 3

- Fecha: 2026-06-21T21:18:47.368565
- Snapshot probe: `2026-06-21T21:18:35.548930`

## Resumen general

| Concepto | Valor |
|---|---|
| Sensores procesados | 1564 |
| Con al menos 1 recurso válido | 447 (28.6%) |
| Con datos reales | 400 (25.6%) |
| Sin datos | 1164 |
| Con error API | 0 |
| Recursos únicos encontrados | 53 |
| Última lectura global | 2026-06-21T19:17:47.902Z |
| Activos últimas 24h | 261 |
| Activos últimos 7 días | 334 |
| Activos últimos 30 días | 447 |
| Inactivos >30 días | 0 |
| Sin ningún timestamp | 1117 |

## Recursos únicos detectados

Bicycle, Bus, Car, Truck, alarm, alert_fire, all, amps, battery, ch_a, ch_b, co, co2, code_line_ferrocarril, connected, description, destination_ferrocarril, energy, flow, gas, humidity, humidity_ext, keepalive, liters, m3, m3_a, m3_b, name_ferrocarril, next_time_ferrocarril, no2, noise, noise_avg_d, noise_avg_h, noise_avg_w, o3, pf, plate, pm1, pm10, pm25, pressure, rainfall, solar_rad, status, temperature, temperature_ext, uv_index, var, volts, volume, water, watts, wind_speed

## Resumen por sistema

| Sistema | Nombre | Procesados | Con datos | % | 24h | 7d | 30d | Recursos | Último dato |
|---|---|---|---|---|---|---|---|---|---|
| S01 | RUIDO | 3 | 1 | 33.3% | 1 | 1 | 1 | noise, noise_avg_d, noise_avg_h, noise_avg_w | 2026-06-21T18:51:17.806Z |
| S02 | CONTAMINACIÓN EXTERIOR | 69 | 33 | 47.8% | 33 | 33 | 33 | co, co2, no2, o3 (+5) | 2026-06-21T18:52:47.042Z |
| S03 | GAS RADON | 1 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S04 | AMBIENTE INTERIOR | 112 | 40 | 35.7% | 17 | 24 | 40 | co2, humidity, temperature | 2026-06-21T18:54:14.000Z |
| S05 | ELECTRICIDAD | 102 | 32 | 31.4% | 29 | 31 | 32 | amps, energy, pf, var (+2) | 2026-06-21T18:55:41.128Z |
| S06 | AGUA | 257 | 78 | 30.4% | 0 | 56 | 79 | flow, liters, m3, volume (+1) | 2026-06-20T18:58:03.000Z |
| S07 | GAS | 25 | 5 | 20.0% | 4 | 5 | 5 | ch_a, ch_b, gas, m3_a (+1) | 2026-06-21T18:59:24.205Z |
| S08 | CALDERAS | 107 | 35 | 32.7% | 0 | 0 | 35 | alarm, description, pressure, status (+1) | 2026-06-08T13:00:26.323Z |
| S09 | CLIMATIZACIÓN | 53 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S13A | SOSTENIBILIDAD EDIFICIOS | 14 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S14A | METEO | 19 | 7 | 36.8% | 6 | 6 | 7 | humidity_ext, pressure, rainfall, solar_rad (+3) | 2026-06-21T19:05:33.936Z |
| S14B | METEO SENSOR | 11 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S15 | PRESENCIA | 31 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S17 | AFORO | 4 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S19 | GAS | 65 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S20 | INUNDACION | 61 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S21 | DETECCION HUMOS | 158 | 70 | 44.3% | 32 | 36 | 70 | alert_fire, battery, keepalive, temperature | 2026-06-21T18:31:24.722Z |
| S22 | TRANSPORTE PUBLICO | 325 | 48 | 14.8% | 93 | 93 | 93 | code_line_ferrocarril, destination_ferrocarril, name_ferrocarril, next_time_ferrocarril | 2026-06-21T19:06:21.446Z |
| S23 | PARKING | 2 | 0 | 0.0% | 0 | 0 | 0 | — | — |
| S24 | TRAFICO | 6 | 1 | 16.7% | 1 | 1 | 1 | Bicycle, Bus, Car, Truck (+2) | 2026-06-21T19:17:13.614Z |
| SIP | IPS | 139 | 50 | 36.0% | 45 | 48 | 51 | connected, keepalive | 2026-06-21T19:17:47.902Z |

## Top sensores activos recientes (máx. 20)

| Sensor | Sistema | Última lectura |
|---|---|---|
| ID0200J23007500336 | SIP | 2026-06-21T19:17:47.902Z |
| ID0200J23007500275 | SIP | 2026-06-21T19:17:47.717Z |
| ID0200J23007500315 | SIP | 2026-06-21T19:17:47.197Z |
| ID0200J23007500247 | SIP | 2026-06-21T19:17:46.231Z |
| ID0200J23007500261 | SIP | 2026-06-21T19:17:41.494Z |
| ID0200J23007500245 | SIP | 2026-06-21T19:17:41.066Z |
| ID0200J23007500344 | SIP | 2026-06-21T19:17:40.019Z |
| ID0200J23007500273 | SIP | 2026-06-21T19:17:39.224Z |
| ID0200J23007500255 | SIP | 2026-06-21T19:17:36.253Z |
| ID0200J23007500262 | SIP | 2026-06-21T19:17:34.492Z |
| ID0200J23007500358 | SIP | 2026-06-21T19:17:34.327Z |
| ID0200J23007500236 | SIP | 2026-06-21T19:17:34.131Z |
| ID0200J23007500254 | SIP | 2026-06-21T19:17:33.090Z |
| ID0200J23007500231 | SIP | 2026-06-21T19:17:32.584Z |
| ID0200J23007500199 | SIP | 2026-06-21T19:17:15.937Z |
| HOS050-1 | S24 | 2026-06-21T19:17:13.614Z |
| ID0200J23007500313 | SIP | 2026-06-21T19:17:10.009Z |
| ID0200J23007500362 | SIP | 2026-06-21T19:17:05.073Z |
| ID0200J23007500282 | SIP | 2026-06-21T19:16:53.172Z |
| ID0200J23007500331 | SIP | 2026-06-21T19:16:21.350Z |

## Sensores sin datos por sistema

**S01** (2 sensores):
- HOS044-S01-01
- HOS136-S01-01 (T257517)
**S02** (36 sensores):
- BET00230154
- HOS128-S02-01 BET00230038
- HOS105-S02-01 BET00230045
- HOS103-S02-01 BET00230036
- HOS102-S02-01 BET00230042
- HOS157-S02-01 BET00230040
- HOS134-S02-01 BET00230041
- HOS104-S02-01 BET00230044
- HOS137-S02-01 BET00230037
- HOS523-S02-01 BET00240027
  _(y 26 más — ver audit_data_health.json)_
**S03** (1 sensores):
- HOS001-S03-01
**S04** (72 sensores):
- HOS001-S04-01
- Aj L'H-Casa Consistorial-HOS001
- HOS125-S04-01
- HOS098-S04-01
- HOS121-S04-01
- HOS117-S04-01
- HOS126-S04-01
- HOS127-S04-01
- HOS034-S04-01
- HOS022-S04-01
  _(y 62 más — ver audit_data_health.json)_
**S05** (70 sensores):
- 22324388010270
- HOS029
- HOS088-S05-01
- HOS037-S05-01
- HOS099-S05-01
- HOS036-S05-01
- HOS125-S05-01
- HOS126-S05-01
- HOS098-S05-01
- HOS127-S05-01
  _(y 60 más — ver audit_data_health.json)_
**S06** (179 sensores):
- I22LA020277R
- I26BB006351N
- P25AD361634T
- I25BD102387U
- P24UG742875Q
- P24UF737486P
- P24AB721542X
- P23UH800297G
- P23FA018698V
- P22UF521430S
  _(y 169 más — ver audit_data_health.json)_
**S07** (20 sensores):
- 0018b24000019407
- Esc. Pablo Neruda - 0018b240000198cb-HOS055
- 0018b2400001962e
- 0018b2400001961f-HOS045
- 0018b24000019612
- 0018b24000019632
- 0018b240000198aa
- Esc. Bernat Metge - 0018b2400001960b - HOS040
- 0018b240000198a3
- Esc. Joaquim Ruyra - HOS046
  _(y 10 más — ver audit_data_health.json)_
**S08** (72 sensores):
- HOS041-S08-01
- HOS001-S08-02
- HOS001-S08-01
- HOS125-S08-01
- HOS054-S08-03
- HOS054-S08-02
- HOS054-S08-01
- HOS055-S08-01
- HOS061-S08-01
- 1112
  _(y 62 más — ver audit_data_health.json)_
**S09** (53 sensores):
- HOS010-S09-01
- HOS001-S09-09
- HOS001-S09-05
- HOS001-S09-08
- HOS001-S09-07
- HOS001-S09-02
- HOS001-S09-06
- HOS001-S09-04
- HOS001-S09-03
- HOS001-S09-01
  _(y 43 más — ver audit_data_health.json)_
**S13A** (14 sensores):
- HOS125-S13-01
- HOS126-S13-01
- HOS055-S13-01
- HOS050-S13-01
- HOS129-S13-01
- HOS063-S13-01
- HOS033-S13-01
- HOS049-S13-01
- HOS059-S13-01
- HOS052-S13-01
  _(y 4 más — ver audit_data_health.json)_
**S14A** (12 sensores):
- HOS126-S14-Meteo (221405 )
- HOS045-S14-Meteo (216699)
- HOS039-S14-Meteo (216694)
- HOS054-S14-Meteo (215946)
- HOS061-S14-Meteo(215864)
- HOS053-S14-Meteo (215854)
- HOS050-S14-Meteo (215733)
- HOS047-S14-Meteo (215360)
- HOS058-S14-Meteo (215289)
- 215285
  _(y 2 más — ver audit_data_health.json)_
**S14B** (11 sensores):
- HOS041-S14-Pira
- HOS125-S14-Pira
- HOS126-S14-Pira
- HOS047-S14-Pira
- HOS054-S14-Pira
- HOS061-S14-Pira
- HOS053-S14-Pira
- HOS050-S14-Pira
- HOS045-S14-Pira
- HOS058-S14-Pira
  _(y 1 más — ver audit_data_health.json)_
**S15** (31 sensores):
- HOS001-S15-01
- HOS132-S15-02
- HOS132-S15-03
- HOS132-S15-01
- HOS069-S15-02
- HOS069-S15-01
- HOS027-S15-01
- HOS035-S15-04
- HOS035-S15-05
- HOS004-S15-02
  _(y 21 más — ver audit_data_health.json)_
**S17** (4 sensores):
- HOS109-S17-01
- HOS121-S17-01
- HOS130-S17-01 (051001812)
- HOS130-S17-02 (051001716)
**S19** (65 sensores):
- HOS125
- HOS125-S19-01
- HOS099-S19-01
- HOS098-S19-01
- HOS005-S19-01
- HOS049-S19-02
- HOS049-S19-01
- HOS061-S19-01
- HOS050-S19-01
- HOS054-S19-02
  _(y 55 más — ver audit_data_health.json)_
**S20** (61 sensores):
- HOS125
- HOS125-S20-01
- HOS109-S20-01
- HOS001-S20-01
- HOS036-S20-01
- HOS088-S20-01
- HOS099-S20-01
- HOS037-S20-01
- HOS098-S20-01
- HOS126-S20-01
  _(y 51 más — ver audit_data_health.json)_
**S21** (88 sensores):
- HOS041
- HOS041
- HOS099
- 70B3D5CEC000038E
- 70B3D5CEC000038E
- HOS005
- HOS041-S21-01
- HOS088-S21-01
- HOS125-S21-01
- HOS037-S21-01
  _(y 78 más — ver audit_data_health.json)_
**S22** (277 sensores):
- HOS052 Esc. Màrius Torres
- HOS023 C. M. Ana Díaz Rico
- HOS130 P. M. Gornal
- Hospital Duran i Reynals - Institut Catala Oncologia-HOS031
- HOS059 Esc. Pau Vila
- Provençana (L10)-HOS094
- Can Vidalet (L5)-HOS080
- HOS047 Esc. Josep Janes
- Escola de Música - Centre de les Arts-HOS071
- Centre Telecom. i Tecnologies de la Informació (CTTI)-HOS165
  _(y 267 más — ver audit_data_health.json)_
**S23** (2 sensores):
- P. M. Gornal - Plaza 1 - HOS130
- P. M. Gornal - Plaza 2 - HOS130
**S24** (5 sensores):
- HOS050-S24-01
- HOS147-S24-01
- HOS149-S24-01
- HOS149-S24-02
- HOS147-S24-02
**SIP** (89 sensores):
- ID0200J23007500383
- ID0200J23007500383
- ID0200J23007500191
- HOS109-IPEX04-ID0200J23007500317
- HOS001-IPEX04-ID0200J23007500325
- HOS001-IPEX04-ID0200J23007500322
- HOS88-IPEX04-ID0200J23007500270
- HOS001-IPEX04-ID0200J23007500260
- HOS001-IPEX04-ID0200J23007500258
- HOS125-IPEX04-ID0200J23007500337
  _(y 79 más — ver audit_data_health.json)_