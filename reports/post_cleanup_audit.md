# Auditoría Post-Limpieza de Duplicados

- Generado: 2026-06-21T22:11:54.627793
- Master: `pielh_qa_master.json` (solo lectura)
- Probe disponible: SI

## Comparación antes / después

| Concepto | Antes | Después | Diferencia |
|---|---|---|---|
| Total sensores en JSON | 1564 | 1564 | 0 (ninguno borrado) |
| Sensores visibles | 1564 | 1278 | -286 (18.3%) |
| Sensores LEGACY (ocultos) | 0 | 286 | +286 |
| Sensores con datos reales | 400 | 400 | +0 |
| Sensores sin datos | 1164 | 878 | -286 |

> Los sensores LEGACY siguen existiendo en `pielh_qa_master.json`.
> Solo tienen `include=false` e `inventory_status="LEGACY"`.
> No se ha borrado ningún sensor ni modificado IDs o tokens.

## Plan de limpieza aplicado

| Concepto | Valor |
|---|---|
| Grupos analizados | 415 |
| KEEP propuestos | 235 |
| MARK_LEGACY aplicados | 287 |
| MANUAL_REVIEW pendientes | 469 |

## Por sistema

| Sistema | Nombre | Total orig. | Visibles | LEGACY | Con datos | Sin datos | % LEGACY |
|---|---|---|---|---|---|---|---|
| S01 | RUIDO | 3 | 2 | 1 | 1 | 1 | 33.3% |
| S02 | CONTAMINACIÓN EXTERIOR | 69 | 36 | 33 | 33 | 3 | 47.8% |
| S03 | GAS RADON | 1 | 1 | 0 | 0 | 1 | 0.0% |
| S04 | AMBIENTE INTERIOR | 112 | 77 | 35 | 40 | 37 | 31.2% |
| S05 | ELECTRICIDAD | 102 | 70 | 32 | 32 | 38 | 31.4% |
| S06 | AGUA | 257 | 171 | 86 | 78 | 93 | 33.5% |
| S07 | GAS | 25 | 21 | 4 | 5 | 16 | 16.0% |
| S08 | CALDERAS | 107 | 107 | 0 | 35 | 72 | 0.0% |
| S09 | CLIMATIZACIÓN | 53 | 53 | 0 | 0 | 53 | 0.0% |
| S13A | SOSTENIBILIDAD EDIFICIOS | 14 | 14 | 0 | 0 | 14 | 0.0% |
| S14A | METEO | 19 | 13 | 6 | 7 | 6 | 31.6% |
| S14B | METEO SENSOR | 11 | 11 | 0 | 0 | 11 | 0.0% |
| S15 | PRESENCIA | 31 | 31 | 0 | 0 | 31 | 0.0% |
| S17 | AFORO | 4 | 4 | 0 | 0 | 4 | 0.0% |
| S19 | GAS | 65 | 65 | 0 | 0 | 65 | 0.0% |
| S20 | INUNDACION | 61 | 61 | 0 | 0 | 61 | 0.0% |
| S21 | DETECCION HUMOS | 158 | 158 | 0 | 70 | 88 | 0.0% |
| S22 | TRANSPORTE PUBLICO | 325 | 238 | 87 | 48 | 190 | 26.8% |
| S23 | PARKING | 2 | 2 | 0 | 0 | 2 | 0.0% |
| S24 | TRAFICO | 6 | 5 | 1 | 1 | 4 | 16.7% |
| SIP | IPS | 139 | 138 | 1 | 50 | 88 | 0.7% |

## Edificios afectados por limpieza (120 edificios con ≥1 sensor LEGACY)

| HOS | Nombre | Total | Visibles | LEGACY |
|---|---|---|---|---|
| SIN_HOS |  | 301 | 249 | 52 |
| HOS001 | HOS001 Aj L'H-Casa Consistorial | 29 | 24 | 5 |
| HOS127 | HOS127 Museu Can Riera | 10 | 5 | 5 |
| HOS040 | HOS040 Esc. Bernat Metge | 15 | 10 | 5 |
| HOS004 | HOS004 CEMFO | 19 | 14 | 5 |
| HOS069 | HOS069 Ca n'Olivé | 16 | 11 | 5 |
| HOS003 | HOS003 Aj L'H-Ed. Girona | 14 | 9 | 5 |
| HOS046 | HOS046 Esc. Joaquim Ruyra | 16 | 12 | 4 |
| HOS099 | HOS099 Esc. Br. Patufet | 17 | 13 | 4 |
| HOS041 | HOS041 Esc. Charlie Rivel | 23 | 19 | 4 |
| HOS125 | HOS125 Museu Casa Espanya | 22 | 18 | 4 |
| HOS037 | HOS037 Dipòsit Parc de la serp | 13 | 9 | 4 |
| HOS136 | HOS136 Residencia Els Alps | 14 | 11 | 3 |
| HOS064 | HOS064 Esc. Puig i Gairalt | 19 | 16 | 3 |
| HOS054 | HOS054 Esc. Milagros Consarnau | 20 | 17 | 3 |
| HOS030 | HOS030 Can Colom | 15 | 12 | 3 |
| HOS045 | HOS045 Esc. Joan Maragall | 19 | 16 | 3 |
| HOS033 | HOS033 Regidoria Districte I | 19 | 16 | 3 |
| HOS153 | HOS153 Institut Can Vilumara | 5 | 2 | 3 |
| HOS022 | HOS022 C. C.  Tecla Sala | 11 | 8 | 3 |
| HOS146 | HOS146 Institut Europa | 9 | 6 | 3 |
| HOS026 | HOS026 A. B. S. S. - Dte. IV/V | 15 | 12 | 3 |
| HOS152 | HOS152 Institut Torras i Bages | 9 | 6 | 3 |
| HOS061 | HOS061 Esc. Pere Lliscart | 16 | 13 | 3 |
| HOS025 | HOS025 CGG Pubilla Casas | 11 | 8 | 3 |
| HOS065 | HOS065 Esc. S. Ramón y Cajal | 17 | 14 | 3 |
| HOS023 | HOS023 C. M. Ana Díaz Rico | 13 | 10 | 3 |
| HOS050 | HOS050 Esc. Lola Anglada | 21 | 18 | 3 |
| HOS058 | HOS058 Esc. Pau Sans | 15 | 12 | 3 |
| HOS056 | HOS056 Esc. Patufet Sant Jordi | 19 | 16 | 3 |
| HOS039 | HOS039 Esc. Ausias March | 15 | 12 | 3 |
| HOS005 | HOS005 Edificio Cobalt | 14 | 11 | 3 |
| HOS012 | HOS012 Cement. Mun. L'Hospitalet | 12 | 9 | 3 |
| HOS028 | HOS028 Area de Benestar social | 9 | 6 | 3 |
| HOS007 | HOS007 Biblioteca Can Sumarro | 6 | 3 | 3 |
| HOS002 | HOS002 Aj L'H-Ed. Migdia | 6 | 3 | 3 |
| HOS118 | HOS118 CGG la Ermita | 5 | 2 | 3 |
| HOS070 | HOS070 Ca n'Arús | 6 | 3 | 3 |
| HOS013 | HOS013 CGG Sanfeliu | 5 | 2 | 3 |
| HOS132 | HOS132 Deixalleria Municipal | 12 | 10 | 2 |
| HOS027 | HOS027 A. B. B. S. - Dte. VI | 13 | 11 | 2 |
| HOS060 | HOS060 Esc. Pep Ventura | 11 | 9 | 2 |
| HOS010 | HOS010 Bibl. i esc. pl. Europa | 11 | 9 | 2 |
| HOS034 | HOS034 Regidoria Districte II | 16 | 14 | 2 |
| HOS066 | HOS066 Esc. Ramon Muntaner | 13 | 11 | 2 |
| HOS043 | HOS043 Esc. Frederic Mistral | 12 | 10 | 2 |
| HOS048 | HOS048 Esc. La Carpa | 14 | 12 | 2 |
| HOS126 | HOS126 Museu L'Harmonia | 13 | 11 | 2 |
| HOS047 | HOS047 Esc. Josep Janes | 17 | 15 | 2 |
| HOS067 | HOS067 Esc. Sant Josep - El Pi | 11 | 9 | 2 |
| HOS049 | HOS049 Esc. La Marina | 15 | 13 | 2 |
| HOS051 | HOS051 Esc. M. d'E. de Bellvitge | 14 | 12 | 2 |
| HOS038 | HOS038 Esc. Busquets i Punset | 12 | 10 | 2 |
| HOS147 | HOS147 Institut Mercè Rodoreda | 8 | 6 | 2 |
| HOS029 | HOS029 Casa dels Cargols | 13 | 11 | 2 |
| HOS115 | HOS115 P. M. Centre | 5 | 3 | 2 |
| HOS097 | HOS097 Esc. Br. Garabatos | 5 | 3 | 2 |
| HOS139 | HOS139 Esc. Rest. El Repartidor | 5 | 3 | 2 |
| HOS068 | HOS068 Palauet Can Buxeres | 4 | 2 | 2 |
| HOS123 | HOS123 CGG Provençana | 3 | 1 | 2 |
| HOS133 | HOS133 Ermita de Santa Eulàlia | 3 | 1 | 2 |
| HOS044 | HOS044 Esc. Gornal | 13 | 12 | 1 |
| HOS508 | HOS508 | 2 | 1 | 1 |
| HOS024 | HOS024 Torre Barrina | 13 | 12 | 1 |
| HOS128 | HOS128 Edificio PUIG | 5 | 4 | 1 |
| HOS520 | HOS520 | 2 | 1 | 1 |
| HOS521 | HOS521 | 2 | 1 | 1 |
| HOS105 | HOS105 Calzedonia | 5 | 4 | 1 |
| HOS157 | HOS157 Tanat. L'Hospitalet Ronda | 3 | 2 | 1 |
| HOS504 | HOS504 | 2 | 1 | 1 |
| HOS522 | HOS522 | 2 | 1 | 1 |
| HOS103 | HOS103 CLD | 3 | 2 | 1 |
| HOS514 | HOS514 | 2 | 1 | 1 |
| HOS503 | HOS503 | 2 | 1 | 1 |
| HOS507 | HOS507 | 2 | 1 | 1 |
| HOS517 | HOS517 | 2 | 1 | 1 |
| HOS137 | HOS137 C. A.Prytanis Hospitalet | 3 | 2 | 1 |
| HOS502 | HOS502 | 2 | 1 | 1 |
| HOS134 | HOS134 Iglesia de la Florida | 3 | 2 | 1 |
| HOS510 | HOS510 | 2 | 1 | 1 |
| HOS518 | HOS518 | 2 | 1 | 1 |
| HOS509 | HOS509 | 2 | 1 | 1 |
| HOS102 | HOS102 Hotel Hesperia Tower | 3 | 2 | 1 |
| HOS515 | HOS515 | 2 | 1 | 1 |
| HOS519 | HOS519 | 2 | 1 | 1 |
| HOS511 | HOS511 | 2 | 1 | 1 |
| HOS104 | HOS104 Ara Vinc | 3 | 2 | 1 |
| HOS513 | HOS513 | 2 | 1 | 1 |
| HOS505 | HOS505 | 2 | 1 | 1 |
| HOS512 | HOS512 | 2 | 1 | 1 |
| HOS501 | HOS501 | 2 | 1 | 1 |
| HOS506 | HOS506 | 2 | 1 | 1 |
| HOS516 | HOS516 | 2 | 1 | 1 |
| HOS141 | HOS141 Institut Eugeni d'Ors | 7 | 6 | 1 |
| HOS150 | HOS150 Institut Rubio i Ors | 7 | 6 | 1 |
| HOS148 | HOS148 Institut Margarida Xirgu | 4 | 3 | 1 |
| HOS144 | HOS144 Institut Bisbe Berenguer | 3 | 2 | 1 |
| HOS154 | HOS154 Institut Jaume Botey | 10 | 9 | 1 |
| HOS098 | HOS098 Esc. Br. La Casa del Molí | 10 | 9 | 1 |
| HOS055 | HOS055 Esc. Pablo Neruda | 14 | 13 | 1 |
| HOS053 | HOS053 Esc. Menéndez Pidal | 13 | 12 | 1 |
| HOS062 | HOS062 Esc. Pompeu Fabra | 11 | 10 | 1 |
| HOS057 | HOS057 Esc. Pau Casals | 14 | 13 | 1 |
| HOS036 | HOS036 Dipòsit Santa Eulàlia | 9 | 8 | 1 |
| HOS006 | HOS006 Cal Gotlla | 10 | 9 | 1 |
| HOS120 | HOS120 CGG del polígon Gornal | 3 | 2 | 1 |
| HOS009 | HOS009 Biblioteca la Florida | 3 | 2 | 1 |
| HOS106 | HOS106 Pavelló M. d'Esports | 3 | 2 | 1 |
| HOS130 | HOS130 P. M. Gornal | 11 | 10 | 1 |
| HOS162 | Edificio de viviendas C. Prat-HOS162 | 4 | 3 | 1 |
| HOS073 | Bellvitge-HOS073 | 2 | 1 | 1 |
| HOS140 | IFP (Innovación en Formación Profesional)-HOS | 2 | 1 | 1 |
| HOS100 | Centre d'Atenció Primària Pura Fernández-HOS1 | 2 | 1 | 1 |
| HOS018 | Centre d'Atenció Primària Just Oliveras (dte. | 2 | 1 | 1 |
| HOS072 | L'Hospitalet de Llogregat-HOS072 | 2 | 1 | 1 |
| HOS083 | Bellvitge (L1)-HOS083 | 2 | 1 | 1 |
| HOS163 | Unifamiliar C. Ebre-HOS163 | 2 | 1 | 1 |
| HOS086 | Rambla Just Oliveras (L1)-HOS086 | 2 | 1 | 1 |
| HOS089 | Sant Josep-HOS089 | 2 | 1 | 1 |
| HOS082 | Avinguda Carrilet (L1)-HOS082 | 2 | 1 | 1 |

## Acciones recomendadas

1. Revisar MANUAL_REVIEW en `reports/duplicate_sensor_cleanup_plan.csv` — 469 sensores pendientes de decisión manual.
2. Para DUPLICATE_ACTIVE (varios activos mismo HOS+sistema): verificar en TheThings cuál es el dispositivo real.
3. Para DUPLICATE_INACTIVE: confirmar si son inventario histórico o errores de registro.

## Restaurar un sensor LEGACY

Si un sensor fue marcado LEGACY incorrectamente, editar `pielh_qa_master.json`:

```json
{
  "inventory_status": null,
  "legacy_reason": null,
  "legacy_marked_at": null,
  "legacy_source": null,
  "include": true
}
```

## Verificación de integridad

- Sensores en JSON: **1564** (ninguno borrado)
- Sensores visibles: **1278**
- Sensores LEGACY: **286**
- Backup disponible en: `data/backups/pielh_qa_master_before_high_confidence_legacy_*.json`