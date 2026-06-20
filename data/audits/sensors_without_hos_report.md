# PIELH — Auditoría Sensores sin HOS

_Generado: 2026-06-20T15:55:41.561936+00:00_

> **Solo lectura.** No se ha modificado ningún dato.

---
## Resumen

| Métrica | Valor |
|---|---|
| Total sensores | 1564 |
| Total edificios | 192 |
| **Sensores sin HOS** | **301** |
| HOS roto (no existe en buildings) | 2 |

---
## Clasificación

| Categoría | Sensores | Descripción |
|---|---|---|
| BUILDING_MATCH_BY_ID | 0 | `id` contiene `HOSxxx` que existe en buildings — asignable automáticamente |
| DUPLICATE_OR_SIBLING | 0 | Hermano de un sensor con HOS ya asignado — asignable automáticamente |
| STREET_SENSOR | 288 | ID de hardware (EUI/serial) sin referencia a edificio — sensor urbano independiente |
| UNKNOWN | 13 | No se puede determinar automáticamente — revisión manual |
| **Total asignables automáticamente** | **0** | BUILDING_MATCH_BY_ID + DUPLICATE_OR_SIBLING con HOS resuelto |

---
## Por sistema

| Sistema | Total sin HOS | MATCH_BY_ID | SIBLING | STREET | UNKNOWN |
|---|---|---|---|---|---|
| S06 | 140 | 0 | 0 | 138 | 2 |
| SIP | 64 | 0 | 0 | 63 | 1 |
| S21 | 62 | 0 | 0 | 62 | 0 |
| S07 | 12 | 0 | 0 | 11 | 1 |
| S05 | 8 | 0 | 0 | 7 | 1 |
| S08 | 7 | 0 | 0 | 7 | 0 |
| S02 | 2 | 0 | 0 | 0 | 2 |
| S04 | 2 | 0 | 0 | 0 | 2 |
| S14A | 2 | 0 | 0 | 0 | 2 |
| S22 | 2 | 0 | 0 | 0 | 2 |

---
## HOS rotos (apuntan a edificio inexistente)

| Sensor ID | HOS (roto) | Sistema |
|---|---|---|
| Hospital General de L'Hospitalet-HOS032 | HOSPITAL | S22 |
| Hospital de Bellvitge (L1)-HOS084 | HOSPITAL | S22 |

---
## Detalle sensores sin HOS

| Sensor ID | Sistema | Categoría | Candidato HOS | Confianza | Motivo |
|---|---|---|---|---|---|
| BET00230154 | S02 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| BET00230154 | S02 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| S4E-143 | S04 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| SISTEMA_4 | S04 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| 22323387990187 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22324388010270 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22324388010270 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22323387990069 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22324388010283 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22324388010284 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 22323387990187 | S05 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| SISTEMA_5 | S05 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BD014384G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA083135U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D16TD053003Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BC041526Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BD096770I | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE063112M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| S06-01 I17BC095962D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D17BA245795C | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D16FE086647C | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA864747G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D15TC125050O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I16BD105801Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BC062758S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BC030788S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD012202M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BE082533S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD033258Q | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BB015889I | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BC012582E | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BD042447D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD033597G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD020143F | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD039671X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD036673D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BD053196L | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BD089718C | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BE056200A | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22LA020277R | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD078435T | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BD089717B | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20LA078279G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BD015287S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC092123D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BB036576Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BD022197K | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BC007276L | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BB051758B | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC056178O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC022199O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I26BB006351N | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P25AD361634T | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I25BD102387U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P24UG742875Q | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P24UF737486P | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P24AB721542X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P23UH800297G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P23FA018698V | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P22UF521430S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P22UE716341M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P22UE716336P | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P20VA163658V | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P19UF026339P | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P19UE040018G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P19UE039966U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P18UG043847A | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P18UE276483R | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P18UE276339K | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P18AD500332D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I25BD024186Z | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I24LA138052L | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I24BD057468Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I24BC057126Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BE066999T | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BE024445O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BD017868H | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BD011418N | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BD005562F | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BC010176D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BB001380X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22LA020277R | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BD089718C | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
|  | S06 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| I22BD089717B | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BD053196L | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC092123D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC092123D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC056178O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC056178O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC022199O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC022199O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D8683450377492801I21BE056200A | S06 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| I21BD017030D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BD015287S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BC007276L | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I21BB036576Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20LA078279G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD078435T | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD036673D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BD020143F | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BD042447D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BB015889I | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BE082533S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD033597G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD033258Q | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BC012582E | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE063112M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BD096770I | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BD014384G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA083135U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA083135U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA083135U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA083135U | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D17BA245795C | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D16TD053003Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| D15TC125050O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P21UE000954H | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P16VA111023D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BB012089G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BB012089G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BB051758B | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I19BC062758S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD012202M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD012202M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD012202M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BE085778O | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BC041526Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I16BD105801Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| H23VA864747G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20LA223736D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| J25FA091773F | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P23AD727226R | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| P19UE039975V | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I23BD021926H | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BC001723Y | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I22BB010257N | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20LA228706R | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I20BB038156H | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BD039671X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I18BC030788S | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| I17BF045531G | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| S06-01 I17BC095962D | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| S06-01 H23VA120599M | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ZZ-DUPLICADO D18BA010631X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| S06-01 D17BA087741E | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| S06-01 D16BA113364X | S06 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b24000019623 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b24000019407 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b2400001962e | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b24000019612 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b24000019632 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b240000198aa | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b240000198a3 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b2400001962d | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b2400001989a | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b2400001961a | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b240000193f3 | S07 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 0018b24000019858 - Edificio 1 | S07 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| 1112 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1113 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1092 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1117 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1122 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1119 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 1121 | S08 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| test | S14A | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| 215285 | S14A | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| 70B3D5CEC0000380 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000376 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000351 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003CE | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000040B | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000396 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000007E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000394 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000040 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000039A | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003DC | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003FD | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000037C | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000034C | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003A5 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000040F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003C4 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000402 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000389 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000373 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003AD | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000393 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000399 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000037F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003F4 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000039F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000040E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000034F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000386 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000371 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003B6 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003A5 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000007E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000394 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000040 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000039A | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000037C | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003DC | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000396 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003CE | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000351 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000380 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000386 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000371 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003B6 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003F4 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000037F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000399 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000393 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003AD | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000034F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000040E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000373 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000389 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000402 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003C4 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000040F | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000034C | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC00003FD | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC0000376 | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000038E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| 70B3D5CEC000038E | S21 | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| LH_MAIN | S22 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| DIPRO-MTI | S22 | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| ID0200J23007500262 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500273 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500358 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500231 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500255 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500236 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500245 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500261 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500313 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500199 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500254 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500344 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500247 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500282 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500274 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500340 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500317 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500258 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500322 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500281 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500271 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500260 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500283 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500338 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500319 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500334 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500257 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500383 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500259 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500264 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500268 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500140 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500388 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500336 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500325 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500373 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500263 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500331 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500312 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500238 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500315 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500275 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500252 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500278 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500362 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500345 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500253 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500341 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500337 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500191 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500331 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500383 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500191 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| IPEX1 | SIP | UNKNOWN | - | LOW | no coincide con ningun patron conocido |
| ID0200J23007500196 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500343 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500409 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500415 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500415 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500342 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500398 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500399 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500316 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |
| ID0200J23007500141 | SIP | STREET_SENSOR | - | MEDIUM | id con formato EUI/serial/numerico de hardware sin referencia a edificio |

---
_PIELH Smart City — Auditoría FASE 0 — Solo lectura._