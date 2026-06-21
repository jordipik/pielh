# Informe de depuracion de sensores IoT

- Generado: 2026-06-21T21:36:53.717011
- Probe base: `2026-06-21T21:18:35.548930`
- Sensores procesados: 1564

## Resumen

| Concepto | Valor |
|---|---|
| Total sensores | 1564 |
| Con datos reales | 400 (25.6%) |
| Sin datos | 1164 (74.4%) |
| Recurso existe pero sin muestras | 47 |

## Resumen por sistema

| Sistema | Nombre | Total | Con datos | Sin datos | % util |
|---|---|---|---|---|---|
| S01 | RUIDO | 3 | 1 | 2 | 33.3% |
| S02 | CONTAMINACIÓN EXTERIOR | 69 | 33 | 36 | 47.8% |
| S03 | GAS RADON | 1 | 0 | 1 | 0.0% |
| S04 | AMBIENTE INTERIOR | 112 | 40 | 72 | 35.7% |
| S05 | ELECTRICIDAD | 102 | 32 | 70 | 31.4% |
| S06 | AGUA | 257 | 78 | 179 | 30.4% |
| S07 | GAS | 25 | 5 | 20 | 20.0% |
| S08 | CALDERAS | 107 | 35 | 72 | 32.7% |
| S09 | CLIMATIZACIÓN | 53 | 0 | 53 | 0.0% |
| S13A | SOSTENIBILIDAD EDIFICIOS | 14 | 0 | 14 | 0.0% |
| S14A | METEO | 19 | 7 | 12 | 36.8% |
| S14B | METEO SENSOR | 11 | 0 | 11 | 0.0% |
| S15 | PRESENCIA | 31 | 0 | 31 | 0.0% |
| S17 | AFORO | 4 | 0 | 4 | 0.0% |
| S19 | GAS | 65 | 0 | 65 | 0.0% |
| S20 | INUNDACION | 61 | 0 | 61 | 0.0% |
| S21 | DETECCION HUMOS | 158 | 70 | 88 | 44.3% |
| S22 | TRANSPORTE PUBLICO | 325 | 48 | 277 | 14.8% |
| S23 | PARKING | 2 | 0 | 2 | 0.0% |
| S24 | TRAFICO | 6 | 1 | 5 | 16.7% |
| SIP | IPS | 139 | 50 | 89 | 36.0% |

## Resumen por edificio (HOS con al menos 1 sensor)

| HOS | Nombre edificio | Total | Con datos | Sin datos |
|---|---|---|---|---|
| HOS001 | HOS001 Aj L'H-Casa Consistorial | 28 | 5 | 23 |
| HOS002 | HOS002 Aj L'H-Ed. Migdia | 6 | 2 | 4 |
| HOS003 | HOS003 Aj L'H-Ed. Girona | 14 | 4 | 10 |
| HOS004 | HOS004 CEMFO | 19 | 4 | 15 |
| HOS005 | HOS005 Edificio Cobalt | 14 | 4 | 10 |
| HOS006 | HOS006 Cal Gotlla | 9 | 1 | 8 |
| HOS007 | HOS007 Biblioteca Can Sumarro | 6 | 2 | 4 |
| HOS008 | HOS008 Bibl. i C. C. la Bòbila | 6 | 0 | 6 |
| HOS009 | HOS009 Biblioteca la Florida | 3 | 1 | 2 |
| HOS010 | HOS010 Bibl. i esc. pl. Europa | 9 | 4 | 5 |
| HOS011 | Bombers de L'Hospitalet-HOS011 | 2 | 0 | 2 |
| HOS012 | HOS012 Cement. Mun. L'Hospitalet | 12 | 4 | 8 |
| HOS013 | HOS013 CGG Sanfeliu | 4 | 1 | 3 |
| HOS014 | HOS014 CGG de la Torrassa | 2 | 0 | 2 |
| HOS015 | HOS015 CGG Santa Eulalia | 3 | 0 | 3 |
| HOS016 | Centre d'Atenció Primària Collblanc (dte. II)-HOS0 | 1 | 0 | 1 |
| HOS017 | Centre d'Atenció Primària Gornal (dte. VI)-HOS017 | 2 | 0 | 2 |
| HOS018 | Centre d'Atenció Primària Just Oliveras (dte. I)-H | 2 | 1 | 1 |
| HOS019 | Centre d'Atenció Primària Florida (dte. IV)-HOS019 | 2 | 0 | 2 |
| HOS020 | Centre d'Atenció Primària Ronda de la Torrassa (dt | 1 | 0 | 1 |
| HOS021 | HOS021 C. C. Santa Eulàlia | 6 | 0 | 6 |
| HOS022 | HOS022 C. C.  Tecla Sala | 11 | 3 | 8 |
| HOS023 | HOS023 C. M. Ana Díaz Rico | 13 | 3 | 10 |
| HOS024 | HOS024 Torre Barrina | 13 | 1 | 12 |
| HOS025 | HOS025 CGG Pubilla Casas | 11 | 3 | 8 |
| HOS026 | HOS026 A. B. S. S. - Dte. IV/V | 15 | 3 | 12 |
| HOS027 | HOS027 A. B. B. S. - Dte. VI | 12 | 2 | 10 |
| HOS028 | HOS028 Area de Benestar social | 9 | 2 | 7 |
| HOS029 | HOS029 Casa dels Cargols | 13 | 2 | 11 |
| HOS030 | HOS030 Can Colom | 15 | 3 | 12 |
| HOS031 | Hospital Duran i Reynals - Institut Catala Oncolog | 2 | 0 | 2 |
| HOS032 | Hospital General de L'Hospitalet-HOS032 | 1 | 0 | 1 |
| HOS033 | HOS033 Regidoria Districte I | 19 | 4 | 15 |
| HOS034 | HOS034 Regidoria Districte II | 16 | 4 | 12 |
| HOS035 | HOS035 Regidoria Districte III | 13 | 0 | 13 |
| HOS036 | HOS036 Dipòsit Santa Eulàlia | 9 | 1 | 8 |
| HOS037 | HOS037 Dipòsit Parc de la serp | 13 | 5 | 8 |
| HOS038 | HOS038 Esc. Busquets i Punset | 12 | 1 | 11 |
| HOS039 | HOS039 Esc. Ausias March | 15 | 2 | 13 |
| HOS040 | HOS040 Esc. Bernat Metge | 14 | 5 | 9 |
| HOS041 | HOS041 Esc. Charlie Rivel | 23 | 8 | 15 |
| HOS042 | HOS042 Esc. J. M. Folch i Torres | 11 | 0 | 11 |
| HOS043 | HOS043 Esc. Frederic Mistral | 12 | 3 | 9 |
| HOS044 | HOS044 Esc. Gornal | 12 | 1 | 11 |
| HOS045 | HOS045 Esc. Joan Maragall | 18 | 5 | 13 |
| HOS046 | HOS046 Esc. Joaquim Ruyra | 16 | 4 | 12 |
| HOS047 | HOS047 Esc. Josep Janes | 16 | 2 | 14 |
| HOS048 | HOS048 Esc. La Carpa | 14 | 3 | 11 |
| HOS049 | HOS049 Esc. La Marina | 15 | 1 | 14 |
| HOS050 | HOS050 Esc. Lola Anglada | 21 | 6 | 15 |
| HOS051 | HOS051 Esc. M. d'E. de Bellvitge | 14 | 2 | 12 |
| HOS052 | HOS052 Esc. Màrius Torres | 12 | 0 | 12 |
| HOS053 | HOS053 Esc. Menéndez Pidal | 13 | 1 | 12 |
| HOS054 | HOS054 Esc. Milagros Consarnau | 20 | 6 | 14 |
| HOS055 | HOS055 Esc. Pablo Neruda | 14 | 1 | 13 |
| HOS056 | HOS056 Esc. Patufet Sant Jordi | 19 | 2 | 17 |
| HOS057 | HOS057 Esc. Pau Casals | 14 | 1 | 13 |
| HOS058 | HOS058 Esc. Pau Sans | 15 | 2 | 13 |
| HOS059 | HOS059 Esc. Pau Vila | 13 | 0 | 13 |
| HOS060 | HOS060 Esc. Pep Ventura | 11 | 2 | 9 |
| HOS061 | HOS061 Esc. Pere Lliscart | 16 | 4 | 12 |
| HOS062 | HOS062 Esc. Pompeu Fabra | 11 | 1 | 10 |
| HOS063 | HOS063 Esc. Prat de la Manta | 14 | 0 | 14 |
| HOS064 | HOS064 Esc. Puig i Gairalt | 19 | 3 | 16 |
| HOS065 | HOS065 Esc. S. Ramón y Cajal | 17 | 4 | 13 |
| HOS066 | HOS066 Esc. Ramon Muntaner | 12 | 2 | 10 |
| HOS067 | HOS067 Esc. Sant Josep - El Pi | 11 | 1 | 10 |
| HOS068 | HOS068 Palauet Can Buxeres | 4 | 1 | 3 |
| HOS069 | HOS069 Ca n'Olivé | 16 | 4 | 12 |
| HOS070 | HOS070 Ca n'Arús | 6 | 2 | 4 |
| HOS071 | Escola de Música - Centre de les Arts-HOS071 | 3 | 0 | 3 |
| HOS072 | L'Hospitalet de Llogregat-HOS072 | 2 | 1 | 1 |
| HOS073 | Bellvitge-HOS073 | 2 | 1 | 1 |
| HOS074 | Fira (L9)-HOS074 | 2 | 0 | 2 |
| HOS075 | Collblanc (L5)-HOS075 | 2 | 0 | 2 |
| HOS076 | Torrassa (L1)-HOS076 | 2 | 0 | 2 |
| HOS077 | Florida (L1)-HOS077 | 2 | 0 | 2 |
| HOS078 | Santa Eulàlia (L1)-HOS078 | 1 | 0 | 1 |
| HOS079 | Can Serra (L1)-HOS079 | 2 | 0 | 2 |
| HOS080 | Can Vidalet (L5)-HOS080 | 2 | 0 | 2 |
| HOS081 | Can Boixeres (L5)-HOS081 | 2 | 0 | 2 |
| HOS082 | Avinguda Carrilet (L1)-HOS082 | 2 | 1 | 1 |
| HOS083 | Bellvitge (L1)-HOS083 | 2 | 1 | 1 |
| HOS084 | Hospital de Bellvitge (L1)-HOS084 | 1 | 0 | 1 |
| HOS085 | Pubilla Cases (L5)-HOS085 | 2 | 0 | 2 |
| HOS086 | Rambla Just Oliveras (L1)-HOS086 | 2 | 1 | 1 |
| HOS087 | Can Tries Gornal (L9)-HOS087 | 2 | 0 | 2 |
| HOS088 | HOS088 Radio-TV de L'Hospitalet | 6 | 0 | 6 |
| HOS089 | Sant Josep-HOS089 | 2 | 1 | 1 |
| HOS090 | Ildefons Cerdà-HOS090 | 1 | 0 | 1 |
| HOS091 | Europa Fira-HOS091 | 2 | 0 | 2 |
| HOS092 | Gornal-HOS092 | 2 | 0 | 2 |
| HOS093 | Centre comercial Gran Via 2-HOS093 | 2 | 0 | 2 |
| HOS094 | Provençana (L10)-HOS094 | 2 | 0 | 2 |
| HOS095 | Ikea-HOS095 | 2 | 0 | 2 |
| HOS096 | HOS096 Esc. Br. Nova Fortuny | 10 | 0 | 10 |
| HOS097 | HOS097 Esc. Br. Garabatos | 4 | 1 | 3 |
| HOS098 | HOS098 Esc. Br. La Casa del Molí | 10 | 1 | 9 |
| HOS099 | HOS099 Esc. Br. Patufet | 17 | 5 | 12 |
| HOS100 | Centre d'Atenció Primària Pura Fernández-HOS100 | 2 | 1 | 1 |
| HOS101 | Centre d'Atenció Primària Alhambra-HOS101 | 1 | 0 | 1 |
| HOS102 | HOS102 Hotel Hesperia Tower | 3 | 1 | 2 |
| HOS103 | HOS103 CLD | 3 | 1 | 2 |
| HOS104 | HOS104 Ara Vinc | 3 | 1 | 2 |
| HOS105 | HOS105 Calzedonia | 5 | 1 | 4 |
| HOS106 | HOS106 Pavelló M. d'Esports | 3 | 1 | 2 |
| HOS107 | HOS107 Piscines M. L'Hospitalet | 2 | 0 | 2 |
| HOS108 | HOS108 E. M. Futbol L'Hospitalet | 3 | 0 | 3 |
| HOS109 | HOS109 C.E.M. L'Hospitalet Nord | 6 | 0 | 6 |
| HOS110 | HOS110 P. M. Fum d'Estampa | 5 | 0 | 5 |
| HOS111 | HOS111 P. M. Les Planes | 3 | 0 | 3 |
| HOS112 | HOS112 P. M. Santa Eulàlia | 3 | 0 | 3 |
| HOS113 | HOS113 P. M. Sergio Manzano | 3 | 0 | 3 |
| HOS114 | HOS114 P. M. Sanfeliu | 3 | 0 | 3 |
| HOS115 | HOS115 P. M. Centre | 5 | 1 | 4 |
| HOS116 | Ciudad de la Justicia (Juzgado 1ª Instancia Nº 2)- | 1 | 0 | 1 |
| HOS117 | HOS117 Mercat Merca-2 Bellvitge | 6 | 0 | 6 |
| HOS118 | HOS118 CGG la Ermita | 5 | 2 | 3 |
| HOS119 | Mercat Merca-2 Can Serra-HOS119 | 2 | 0 | 2 |
| HOS120 | HOS120 CGG del polígon Gornal | 3 | 1 | 2 |
| HOS121 | HOS121 CGG de Ca n'arús | 3 | 0 | 3 |
| HOS122 | HOS122 CGG de Can Serra | 2 | 0 | 2 |
| HOS123 | HOS123 CGG Provençana | 2 | 1 | 1 |
| HOS124 | HOS124 Mercat del Torrent Gornal | 3 | 0 | 3 |
| HOS125 | HOS125 Museu Casa Espanya | 22 | 6 | 16 |
| HOS126 | HOS126 Museu L'Harmonia | 13 | 1 | 12 |
| HOS127 | HOS127 Museu Can Riera | 10 | 4 | 6 |
| HOS128 | HOS128 Edificio PUIG | 4 | 1 | 3 |
| HOS129 | HOS129 C. A. Prytanis pl Europa | 2 | 0 | 2 |
| HOS130 | HOS130 P. M. Gornal | 11 | 1 | 10 |
| HOS131 | Fira Barcelona Gran Via-HOS131 | 1 | 0 | 1 |
| HOS132 | HOS132 Deixalleria Municipal | 12 | 2 | 10 |
| HOS133 | HOS133 Ermita de Santa Eulàlia | 3 | 1 | 2 |
| HOS134 | HOS134 Iglesia de la Florida | 3 | 1 | 2 |
| HOS135 | Mezquita de Santa Eulàlia-HOS135 | 1 | 0 | 1 |
| HOS136 | HOS136 Residencia Els Alps | 14 | 2 | 12 |
| HOS137 | HOS137 C. A.Prytanis Hospitalet | 3 | 1 | 2 |
| HOS138 | Residència Collblanc Companys Socials-HOS138 | 2 | 0 | 2 |
| HOS139 | HOS139 Esc. Rest. El Repartidor | 5 | 1 | 4 |
| HOS140 | IFP (Innovación en Formación Profesional)-HOS140 | 2 | 1 | 1 |
| HOS141 | HOS141 Institut Eugeni d'Ors | 7 | 3 | 4 |
| HOS142 | HOS142 Institut Apel·les Mestres | 4 | 0 | 4 |
| HOS143 | HOS143 Institut Bellvitge | 7 | 2 | 5 |
| HOS144 | HOS144 Institut Bisbe Berenguer | 3 | 1 | 2 |
| HOS145 | HOS145 Institut Eduard Fontserè | 2 | 0 | 2 |
| HOS146 | HOS146 Institut Europa | 8 | 4 | 4 |
| HOS147 | HOS147 Institut Mercè Rodoreda | 8 | 1 | 7 |
| HOS148 | HOS148 Institut Margarida Xirgu | 4 | 1 | 3 |
| HOS149 | HOS149 Institut Pedraforca | 5 | 0 | 5 |
| HOS150 | HOS150 Institut Rubio i Ors | 7 | 3 | 4 |
| HOS151 | HOS151 Institut Santa Eulàlia | 3 | 0 | 3 |
| HOS152 | HOS152 Institut Torras i Bages | 9 | 4 | 5 |
| HOS153 | HOS153 Institut Can Vilumara | 5 | 2 | 3 |
| HOS154 | HOS154 Institut Jaume Botey | 9 | 3 | 6 |
| HOS155 | HOS155 Institut Llobregat | 3 | 0 | 3 |
| HOS156 | HOS156 Institut Provençana | 4 | 0 | 4 |
| HOS157 | HOS157 Tanat. L'Hospitalet Ronda | 3 | 1 | 2 |
| HOS158 | Tanatori - Crematori L'Hospitalet Gran Via-HOS158 | 1 | 0 | 1 |
| HOS159 | HOS159 Teatre Joventut | 3 | 0 | 3 |
| HOS160 | Hospital Universitari Bellvitge-HOS160 | 1 | 0 | 1 |
| HOS161 | Universitat de Barcelona-HOS161 | 1 | 0 | 1 |
| HOS162 | Edificio de viviendas C. Prat-HOS162 | 4 | 1 | 3 |
| HOS163 | Unifamiliar C. Ebre-HOS163 | 2 | 1 | 1 |
| HOS164 | Edificio de viviendas Plaza Guernica-HOS164 | 2 | 0 | 2 |
| HOS165 | Centre Telecom. i Tecnologies de la Informació (CT | 2 | 0 | 2 |
| HOS166 | ETRA BONAL - Cornellà-HOS166 | 1 | 0 | 1 |
| HOS501 | HOS501 | 2 | 1 | 1 |
| HOS502 | HOS502 | 2 | 1 | 1 |
| HOS503 | HOS503 | 2 | 1 | 1 |
| HOS504 | HOS504 | 2 | 1 | 1 |
| HOS505 | HOS505 | 2 | 1 | 1 |
| HOS506 | HOS506 | 2 | 1 | 1 |
| HOS507 | HOS507 | 2 | 1 | 1 |
| HOS508 | HOS508 | 2 | 1 | 1 |
| HOS509 | HOS509 | 2 | 1 | 1 |
| HOS510 | HOS510 | 2 | 1 | 1 |
| HOS511 | HOS511 | 2 | 1 | 1 |
| HOS512 | HOS512 | 2 | 1 | 1 |
| HOS513 | HOS513 | 2 | 1 | 1 |
| HOS514 | HOS514 | 2 | 1 | 1 |
| HOS515 | HOS515 | 2 | 1 | 1 |
| HOS516 | HOS516 | 2 | 1 | 1 |
| HOS517 | HOS517 | 2 | 1 | 1 |
| HOS518 | HOS518 | 2 | 1 | 1 |
| HOS519 | HOS519 | 2 | 1 | 1 |
| HOS520 | HOS520 | 2 | 1 | 1 |
| HOS521 | HOS521 | 2 | 1 | 1 |
| HOS522 | HOS522 | 2 | 1 | 1 |
| HOS523 | HOS523 | 1 | 0 | 1 |
| HOSPITAL | Hospital de Bellvitge (L1)-HOS084 | 2 | 0 | 2 |
| SIN_HOS |  | 322 | 156 | 166 |

## Sensores con datos reales (400)

| id | HOS | Edificio | Sistema | Ultimo dato | Recurso |
|---|---|---|---|---|---|
| HOS044-S01-01 | HOS044 | HOS044 Esc. Gornal | S01 | 2026-06-21T18:51:17.806Z | noise |
| BET00230154 | — |  | S02 | 2026-06-21T18:50:45.244Z | temperature |
| HOS024-S02-01-BET00230039 | HOS024 | HOS024 Torre Barrina | S02 | 2026-06-21T18:50:46.590Z | temperature |
| HOS102-S02-01 BET00230042 | HOS102 | HOS102 Hotel Hesperia Tower | S02 | 2026-06-21T18:50:47.024Z | temperature |
| HOS103-S02-01 BET00230036 | HOS103 | HOS103 CLD | S02 | 2026-06-21T18:50:46.782Z | temperature |
| HOS104-S02-01 BET00230044 | HOS104 | HOS104 Ara Vinc | S02 | 2026-06-21T18:50:44.674Z | temperature |
| HOS105-S02-01 BET00230045 | HOS105 | HOS105 Calzedonia | S02 | 2026-06-21T18:50:46.387Z | temperature |
| HOS128-S02-01 BET00230038 | HOS128 | HOS128 Edificio PUIG | S02 | 2026-06-21T18:50:46.618Z | temperature |
| Deixalleria Municipal - HOS132-S02-01 BET00230060 | HOS132 | HOS132 Deixalleria Municipal | S02 | 2026-06-21T18:50:46.832Z | temperature |
| HOS134-S02-01 BET00230041 | HOS134 | HOS134 Iglesia de la Florida | S02 | 2026-06-21T18:52:46.900Z | temperature |
| HOS137-S02-01 BET00230037 | HOS137 | HOS137 C. A.Prytanis Hospitalet | S02 | 2026-06-21T18:50:47.063Z | temperature |
| HOS157-S02-01 BET00230040 | HOS157 | HOS157 Tanat. L'Hospitalet Ronda | S02 | 2026-06-21T18:50:45.024Z | temperature |
| HOS501-S02-01 BET00230026 - AJUNTAMENT | HOS501 | HOS501 | S02 | 2026-06-21T18:50:44.521Z | temperature |
| HOS502-S02-01 BET00230027 | HOS502 | HOS502 | S02 | 2026-06-21T18:50:44.520Z | temperature |
| HOS503-S02-01 BET00230058 | HOS503 | HOS503 | S02 | 2026-06-21T18:50:45.214Z | temperature |
| HOS504-S02-01 BET00230059 | HOS504 | HOS504 | S02 | 2026-06-21T18:50:47.024Z | temperature |
| HOS505-S02-01 BET00230061 | HOS505 | HOS505 | S02 | 2026-06-21T18:52:46.821Z | temperature |
| HOS506-S02-01 BET00230062 | HOS506 | HOS506 | S02 | 2026-06-21T18:50:44.295Z | temperature |
| HOS507-S02-01 BET00230063 | HOS507 | HOS507 | S02 | 2026-06-21T18:52:44.878Z | temperature |
| HOS508-S02-01 BET00230064 | HOS508 | HOS508 | S02 | 2026-06-21T18:50:45.210Z | temperature |
| HOS509-S02-01 BET00230065 | HOS509 | HOS509 | S02 | 2026-06-21T18:50:45.243Z | temperature |
| HOS510-S02-01 BET00230066 | HOS510 | HOS510 | S02 | 2026-06-21T18:50:44.788Z | temperature |
| HOS511-S02-01 BET00230067 | HOS511 | HOS511 | S02 | 2026-06-21T18:50:44.911Z | temperature |
| HOS512-S02-01 BET00230068 | HOS512 | HOS512 | S02 | 2026-06-21T18:52:44.869Z | temperature |
| HOS513-S02-01 BET00230144 | HOS513 | HOS513 | S02 | 2026-06-21T18:52:47.042Z | temperature |
| HOS514-S02-01 BET00230145 | HOS514 | HOS514 | S02 | 2026-06-21T18:52:44.156Z | temperature |
| HOS515-S02-01 BET00230146 | HOS515 | HOS515 | S02 | 2026-06-21T18:50:46.777Z | temperature |
| HOS516-S02-01 BET00230147 | HOS516 | HOS516 | S02 | 2026-06-21T18:50:46.726Z | temperature |
| HOS517-S02-01 BET00230148 | HOS517 | HOS517 | S02 | 2026-06-21T18:50:47.020Z | temperature |
| HOS518-S02-01 BET00230149 | HOS518 | HOS518 | S02 | 2026-06-21T18:50:47.024Z | temperature |
| HOS519-S02-01 BET00230150 | HOS519 | HOS519 | S02 | 2026-06-21T18:50:46.857Z | temperature |
| HOS520-S02-01 BET00230151 | HOS520 | HOS520 | S02 | 2026-06-21T18:52:44.869Z | temperature |
| HOS521-S02-01 BET00230152 | HOS521 | HOS521 | S02 | 2026-06-21T18:50:45.216Z | temperature |
| HOS522-S02-01 BET00230153 | HOS522 | HOS522 | S02 | 2026-06-21T18:50:44.474Z | temperature |
| S4E-143 | — |  | S04 | 2026-06-13T17:43:45.000Z | temperature |
| SISTEMA_4 | — |  | S04 | 2026-06-13T16:32:44.000Z | temperature |
| HOS001 | HOS001 | HOS001 Aj L'H-Casa Consistorial | S04 | 2026-06-21T18:53:55.000Z | temperature |
| S4E-HOS003 | HOS003 | HOS003 Aj L'H-Ed. Girona | S04 | 2026-06-13T16:32:44.000Z | temperature |
| S4E-HOS004 | HOS004 | HOS004 CEMFO | S04 | 2026-06-13T18:44:50.000Z | temperature |
| S4E-HOS010 | HOS010 | HOS010 Bibl. i esc. pl. Europa | S04 | 2026-06-21T18:53:29.000Z | temperature |
| S4E-HOS022 | HOS022 | HOS022 C. C.  Tecla Sala | S04 | 2026-06-19T23:30:32.000Z | temperature |
| S4E-HOS023 | HOS023 | HOS023 C. M. Ana Díaz Rico | S04 | 2026-06-13T16:32:43.000Z | temperature |
| S4E-HOS025 | HOS025 | HOS025 CGG Pubilla Casas | S04 | 2026-06-13T17:43:51.000Z | temperature |
| S4E-HOS026 | HOS026 | HOS026 A. B. S. S. - Dte. IV/V | S04 | 2026-06-10T20:32:26.000Z | temperature |
| S4E-HOS027 | HOS027 | HOS027 A. B. B. S. - Dte. VI | S04 | 2026-06-21T18:53:07.000Z | temperature |
| S4E-HOS030 | HOS030 | HOS030 Can Colom | S04 | 2026-06-21T18:53:06.000Z | temperature |
| S4E-HOS033 | HOS033 | HOS033 Regidoria Districte I | S04 | 2026-06-21T18:52:42.000Z | temperature |
| S4E-HOS033-1 | HOS033 | HOS033 Regidoria Districte I | S04 | 2026-06-21T18:52:42.000Z | temperature |
| S4E-HOS034 | HOS034 | HOS034 Regidoria Districte II | S04 | 2026-06-20T05:55:42.000Z | temperature |
| S4E-HOS034 | HOS034 | HOS034 Regidoria Districte II | S04 | 2026-06-10T11:03:42.000Z | temperature |
| S4E-HOS040 | HOS040 | HOS040 Esc. Bernat Metge | S04 | 2026-06-21T18:53:46.000Z | temperature |
| S4E-HOS041 | HOS041 | HOS041 Esc. Charlie Rivel | S04 | 2026-06-19T22:15:35.000Z | temperature |
| S4E-HOS043 | HOS043 | HOS043 Esc. Frederic Mistral | S04 | 2026-06-17T01:45:12.000Z | temperature |
| S4E-HOS045 | HOS045 | HOS045 Esc. Joan Maragall | S04 | 2026-06-21T12:46:57.000Z | temperature |
| S4E-HOS046 | HOS046 | HOS046 Esc. Joaquim Ruyra | S04 | 2026-06-21T12:46:52.000Z | temperature |
| S4E-HOS048 | HOS048 | HOS048 Esc. La Carpa | S04 | 2026-06-14T13:09:01.000Z | temperature |
| S4E-HOS054 | HOS054 | HOS054 Esc. Milagros Consarnau | S04 | 2026-06-21T18:53:07.000Z | temperature |
| S4E-HOS060 | HOS060 | HOS060 Esc. Pep Ventura | S04 | 2026-06-21T18:53:43.000Z | temperature |
| S4E-HOS061 | HOS061 | HOS061 Esc. Pere Lliscart | S04 | 2026-06-13T17:43:51.000Z | temperature |
| S4E-HOS064 | HOS064 | HOS064 Esc. Puig i Gairalt | S04 | 2026-06-21T18:53:12.000Z | temperature |
| S4E-HOS065 | HOS065 | HOS065 Esc. S. Ramón y Cajal | S04 | 2026-06-13T17:43:56.000Z | temperature |
| S4E-HOS066 | HOS066 | HOS066 Esc. Ramon Muntaner | S04 | 2026-06-17T00:43:01.000Z | temperature |
| S4E-HOS069 | HOS069 | HOS069 Ca n'Olivé | S04 | 2026-06-13T17:43:50.000Z | temperature |
| S4E-HOS099 | HOS099 | HOS099 Esc. Br. Patufet | S04 | 2026-06-21T18:53:55.000Z | temperature |
| HOS125 | HOS125 | HOS125 Museu Casa Espanya | S04 | 2026-06-14T08:45:19.000Z | temperature |
| HOS127 | HOS127 | HOS127 Museu Can Riera | S04 | 2026-06-21T18:52:40.000Z | temperature |
| S4E-HOS141 | HOS141 | HOS141 Institut Eugeni d'Ors | S04 | 2026-06-21T18:53:13.000Z | temperature |
| S4E-HOS144 | HOS144 | HOS144 Institut Bisbe Berenguer | S04 | 2026-06-18T08:22:09.000Z | temperature |
| S4E-HOS146 | HOS146 | HOS146 Institut Europa | S04 | 2026-06-10T20:32:27.000Z | temperature |
| S4E-HOS148 | HOS148 | HOS148 Institut Margarida Xirgu | S04 | 2026-06-20T10:46:17.000Z | temperature |
| S4E-HOS150 | HOS150 | HOS150 Institut Rubio i Ors | S04 | 2026-06-21T18:53:51.000Z | temperature |
| S4E-HOS152 | HOS152 | HOS152 Institut Torras i Bages | S04 | 2026-06-10T20:32:27.000Z | temperature |
| S4E-HOS153 | HOS153 | HOS153 Institut Can Vilumara | S04 | 2026-06-21T18:54:14.000Z | temperature |
| S4E-HOS154 | HOS154 | HOS154 Institut Jaume Botey | S04 | 2026-06-14T13:09:00.000Z | temperature |
| 22323387990187 | — |  | S05 | 2026-06-21T18:52:01.319Z | energy |
| 22324388010270 | — |  | S05 | 2026-06-14T22:14:51.438Z | energy |
| HOS003-S05-01 | HOS003 | HOS003 Aj L'H-Ed. Girona | S05 | 2026-06-21T18:51:20.932Z | energy |
| HOS004-S05-01 | HOS004 | HOS004 CEMFO | S05 | 2026-06-21T18:51:41.035Z | energy |
| HOS005-S05-01 | HOS005 | HOS005 Edificio Cobalt | S05 | 2026-06-21T18:53:21.030Z | energy |
| HOS012-S05-01 | HOS012 | HOS012 Cement. Mun. L'Hospitalet | S05 | 2026-06-21T18:55:11.052Z | energy |
| HOS022-S05-01 | HOS022 | HOS022 C. C.  Tecla Sala | S05 | 2026-06-21T18:55:31.075Z | energy |
| HOS023-S05-01 | HOS023 | HOS023 C. M. Ana Díaz Rico | S05 | 2026-06-21T18:51:10.945Z | energy |
| HOS025-S05-01 | HOS025 | HOS025 CGG Pubilla Casas | S05 | 2026-06-21T18:54:31.025Z | energy |
| HOS026-S05-01 | HOS026 | HOS026 A. B. S. S. - Dte. IV/V | S05 | 2026-06-21T18:55:21.124Z | energy |
| HOS027-S05-01 | HOS027 | HOS027 A. B. B. S. - Dte. VI | S05 | 2026-06-21T18:52:50.987Z | energy |
| HOS029 | HOS029 | HOS029 Casa dels Cargols | S05 | 2026-06-21T18:53:31.070Z | energy |
| HOS030-S05-01 | HOS030 | HOS030 Can Colom | S05 | 2026-06-21T18:52:41.007Z | energy |
| HOS033-S05-01 | HOS033 | HOS033 Regidoria Districte I | S05 | 2026-06-21T18:51:01.017Z | energy |
| HOS034-S05-01 | HOS034 | HOS034 Regidoria Districte II | S05 | 2026-06-21T18:53:53.729Z | energy |
| HOS036-S05-01 | HOS036 | HOS036 Dipòsit Santa Eulàlia | S05 | 2026-06-15T03:08:16.729Z | energy |
| HOS037-S05-01 | HOS037 | HOS037 Dipòsit Parc de la serp | S05 | 2026-06-21T18:54:51.119Z | energy |
| HOS040-S05-01 | HOS040 | HOS040 Esc. Bernat Metge | S05 | 2026-06-21T18:54:11.022Z | energy |
| HOS041-S05-01 | HOS041 | HOS041 Esc. Charlie Rivel | S05 | 2026-06-21T18:53:41.010Z | energy |
| HOS043-S05-01 | HOS043 | HOS043 Esc. Frederic Mistral | S05 | 2026-06-21T18:53:11.005Z | energy |
| HOS045-S05-01 | HOS045 | HOS045 Esc. Joan Maragall | S05 | 2026-06-21T18:52:10.992Z | energy |
| HOS046-S05-01 | HOS046 | HOS046 Esc. Joaquim Ruyra | S05 | 2026-06-21T18:51:54.180Z | energy |
| HOS048-S05-01 | HOS048 | HOS048 Esc. La Carpa | S05 | 2026-06-21T18:52:21.003Z | energy |
| HOS050-S05-01 | HOS050 | HOS050 Esc. Lola Anglada | S05 | 2026-06-21T18:51:31.008Z | energy |
| HOS060 | HOS060 | HOS060 Esc. Pep Ventura | S05 | 2026-06-21T18:54:01.067Z | energy |
| HOS064-S05-01 | HOS064 | HOS064 Esc. Puig i Gairalt | S05 | 2026-06-21T18:53:01.085Z | energy |
| HOS065-S05-01 | HOS065 | HOS065 Esc. S. Ramón y Cajal | S05 | 2026-06-21T18:55:01.075Z | energy |
| HOS066-S05-01 | HOS066 | HOS066 Esc. Ramon Muntaner | S05 | 2026-06-21T18:52:31.019Z | energy |
| HOS069-S05-01 | HOS069 | HOS069 Ca n'Olivé | S05 | 2026-06-21T18:54:21.029Z | energy |
| HOS099-S05-01 | HOS099 | HOS099 Esc. Br. Patufet | S05 | 2026-06-21T18:54:41.208Z | energy |
| HOS125 | HOS125 | HOS125 Museu Casa Espanya | S05 | 2026-06-14T08:48:59.151Z | energy |
| HOS127-S05-01 | HOS127 | HOS127 Museu Can Riera | S05 | 2026-06-21T18:55:41.128Z | energy |
| D15TC125050O | — |  | S06 | 2026-06-20T15:05:02.000Z | m3 |
| D16FE086647C | — |  | S06 | 2026-06-20T18:18:37.000Z | m3 |
| D16TD053003Y | — |  | S06 | 2026-06-20T17:35:48.000Z | m3 |
| D17BA245795C | — |  | S06 | 2026-06-20T16:39:06.000Z | m3 |
| H23VA083135U | — |  | S06 | 2026-06-20T15:58:55.000Z | m3 |
| H23VA864747G | — |  | S06 | 2026-06-20T17:02:35.000Z | m3 |
| I16BD105801Y | — |  | S06 | 2026-06-20T17:48:39.000Z | m3 |
| I17BC041526Y | — |  | S06 | 2026-06-19T17:43:44.000Z | m3 |
| I17BD014384G | — |  | S06 | 2026-06-19T16:02:19.000Z | m3 |
| I17BD096770I | — |  | S06 | 2026-06-19T16:23:49.000Z | m3 |
| I17BE063112M | — |  | S06 | 2026-06-19T16:00:27.000Z | m3 |
| I17BE085778O | — |  | S06 | 2026-06-19T06:16:02.000Z | m3 |
| I18BC012582E | — |  | S06 | 2026-06-17T15:38:56.000Z | m3 |
| I18BC030788S | — |  | S06 | 2026-06-17T19:01:12.000Z | m3 |
| I18BD012202M | — |  | S06 | 2026-06-17T18:37:38.000Z | m3 |
| I18BD033258Q | — |  | S06 | 2026-06-17T17:42:56.000Z | m3 |
| I18BD033597G | — |  | S06 | 2026-06-17T16:00:35.000Z | m3 |
| I18BD039671X | — |  | S06 | 2026-06-17T18:15:43.000Z | m3 |
| I18BE082533S | — |  | S06 | 2026-06-17T17:58:57.000Z | m3 |
| I19BB015889I | — |  | S06 | 2026-06-17T16:56:14.000Z | m3 |
| I19BC062758S | — |  | S06 | 2026-06-17T15:53:40.000Z | m3 |
| I19BD042447D | — |  | S06 | 2026-06-17T06:56:18.000Z | m3 |
| I20BD020143F | — |  | S06 | 2026-06-17T11:58:58.000Z | m3 |
| I20BD036673D | — |  | S06 | 2026-06-17T13:59:14.000Z | m3 |
| I20BD078435T | — |  | S06 | 2026-06-07T14:57:19.000Z | m3 |
| I20LA078279G | — |  | S06 | 2026-06-07T16:00:56.000Z | m3 |
| I21BB036576Y | — |  | S06 | 2026-06-07T18:21:11.000Z | m3 |
| I21BC007276L | — |  | S06 | 2026-06-07T16:00:49.000Z | m3 |
| I21BD015287S | — |  | S06 | 2026-06-07T15:55:33.000Z | m3 |
| I21BD022197K | — |  | S06 | 2026-06-07T17:53:52.000Z | m3 |
| I21BE056200A | — |  | S06 | 2026-06-07T17:57:27.000Z | m3 |
| I22BB051758B | — |  | S06 | 2026-06-07T15:57:23.000Z | m3 |
| I22BC022199O | — |  | S06 | 2026-06-07T11:57:13.000Z | m3 |
| I22BC056178O | — |  | S06 | 2026-06-07T12:01:05.000Z | m3 |
| I22BC092123D | — |  | S06 | 2026-06-07T17:00:50.000Z | m3 |
| I22BD053196L | — |  | S06 | 2026-06-07T17:57:24.000Z | m3 |
| I22BD089717B | — |  | S06 | 2026-06-07T14:58:59.000Z | m3 |
| I22BD089718C | — |  | S06 | 2026-06-07T10:59:40.000Z | m3 |
| S06-01 I17BC095962D | — |  | S06 | 2026-06-19T16:03:10.000Z | m3 |
| HOS001-S06-01 I19BD035462J | HOS001 | HOS001 Aj L'H-Casa Consistorial | S06 | 2026-06-17T15:58:35.000Z | m3 |
| Aj L'H-Ed. Migdia - HOS002-S06-01 D16UH084259X | HOS002 | HOS002 Aj L'H-Ed. Migdia | S06 | 2026-06-20T18:48:34.000Z | m3 |
| Aj L'H-Ed. Girona - HOS003-S06-01 I22BB010103W | HOS003 | HOS003 Aj L'H-Ed. Girona | S06 | 2026-06-07T16:59:28.000Z | m3 |
| CEMFO - HOS004-S06-01 I17BE046798C | HOS004 | HOS004 CEMFO | S06 | 2026-06-19T15:26:26.000Z | m3 |
| Cal Gotlla - HOS006-S06-01 D18BA388376I | HOS006 | HOS006 Cal Gotlla | S06 | 2026-06-20T15:19:02.000Z | m3 |
| Biblioteca Can Sumarro - HOS007-S06-01 I17BD504878W | HOS007 | HOS007 Biblioteca Can Sumarro | S06 | 2026-06-19T17:36:51.000Z | m3 |
| Biblioteca la Florida - HOS009-S06-01 D17BA214472T | HOS009 | HOS009 Biblioteca la Florida | S06 | 2026-06-20T18:39:20.000Z | m3 |
| Bibl. i esc. pl. Europa - HOS010-S06-01 I22BD035149C | HOS010 | HOS010 Bibl. i esc. pl. Europa | S06 | 2026-06-07T15:58:03.000Z | m3 |
| C. C.  Tecla Sala - HOS022-S06-01 I17BD504011F | HOS022 | HOS022 C. C.  Tecla Sala | S06 | 2026-06-19T17:39:49.000Z | m3 |
| CGG Provençana - HOS023-S06-01 I17BC013010U | HOS023 | HOS023 C. M. Ana Díaz Rico | S06 | 2026-06-19T16:53:44.000Z | m3 |
| CGG Pubilla Casas - HOS025-S06-01 H23VA084841R | HOS025 | HOS025 CGG Pubilla Casas | S06 | 2026-06-20T15:59:21.000Z | m3 |
| A. B. S. S. - Dte. IV/V - HOS026-S06-01 D16BA108177L | HOS026 | HOS026 A. B. S. S. - Dte. IV/V | S06 | 2026-06-20T17:22:57.000Z | m3 |
| Area de Benestar social - HOS028-S06-01 H23VA120131G | HOS028 | HOS028 Area de Benestar social | S06 | 2026-06-20T15:49:22.000Z | m3 |
| Casa dels Cargols - HOS029-S06-01 H22VA827558M | HOS029 | HOS029 Casa dels Cargols | S06 | 2026-06-20T15:01:19.000Z | m3 |
| Can Colom - HOS030-S06-02 I22BB051956F | HOS030 | HOS030 Can Colom | S06 | 2026-06-07T17:59:50.000Z | m3 |
| Regidoria Districte II - HOS034-S06-01 C15FA260208R | HOS034 | HOS034 Regidoria Districte II | S06 | 2026-06-10T21:23:56.000Z | m3 |
| Dipòsit Parc de la serp - HOS037-S06-01 H24VA628016X | HOS037 | HOS037 Dipòsit Parc de la serp | S06 | 2026-06-20T13:01:23.000Z | m3 |
| Esc. Ausias March - HOS039-S06-01 I20BD036700P | HOS039 | HOS039 Esc. Ausias March | S06 | 2026-06-17T18:02:25.000Z | m3 |
| Esc. Charlie Rivel - HOS041-S06-01 I22BB010137G | HOS041 | HOS041 Esc. Charlie Rivel | S06 | 2026-06-07T13:57:25.000Z | m3 |
| Esc. Josep Janes - HOS047-S06-01 I17BE094519Y | HOS047 | HOS047 Esc. Josep Janes | S06 | 2026-06-17T17:59:28.000Z | m3 |
| R6Wzy1sTy4MvM-lnIXD92Q2x1tN-7Tfo9ZSAvIXO6YA | HOS051 | HOS051 Esc. M. d'E. de Bellvitge | S06 | 2026-06-07T16:57:39.000Z | m3 |
| Esc. Menéndez Pidal - HOS053-S06-01 I18BD030305U | HOS053 | HOS053 Esc. Menéndez Pidal | S06 | 2026-06-17T17:58:46.000Z | m3 |
| Esc. Milagros Consarnau - HOS054-S06-S1 I18BD030306V | HOS054 | HOS054 Esc. Milagros Consarnau | S06 | 2026-06-17T18:05:41.000Z | m3 |
| Esc. Patufet Sant Jordi - HOS056-S06-01 D15FE071450J | HOS056 | HOS056 Esc. Patufet Sant Jordi | S06 | 2026-06-20T17:39:08.000Z | m3 |
| Esc. Pau Casals - HOS057-S06-01 I18BD030309Y | HOS057 | HOS057 Esc. Pau Casals | S06 | 2026-06-17T18:47:58.000Z | m3 |
| Esc. Pau Sans - HOS058-S06-01 I22BD021841U | HOS058 | HOS058 Esc. Pau Sans | S06 | 2026-06-07T14:00:02.000Z | m3 |
| Esc. Pere Lliscart - HOS061-S06-01 I18BD030283F | HOS061 | HOS061 Esc. Pere Lliscart | S06 | 2026-06-17T18:26:19.000Z | m3 |
| Esc. Pompeu Fabra - HOS062-S06-01 I18BD030308X | HOS062 | HOS062 Esc. Pompeu Fabra | S06 | 2026-06-17T15:01:15.000Z | m3 |
| Esc. Puig i Gairalt - HOS064-S06-1 I18BD030289L | HOS064 | HOS064 Esc. Puig i Gairalt | S06 | 2026-06-17T18:24:12.000Z | m3 |
| Esc. S. Ramón y Cajal - HOS065-S06-01 I22BD089711V | HOS065 | HOS065 Esc. S. Ramón y Cajal | S06 | 2026-06-07T17:57:07.000Z | m3 |
| Ca n'Olivé - HOS069-S06-01 H23VA095642V | HOS069 | HOS069 Ca n'Olivé | S06 | 2026-06-20T17:03:16.000Z | m3 |
| Ca n'Arús - HOS070-S06-01 I20BD020169P | HOS070 | HOS070 Ca n'Arús | S06 | 2026-06-17T05:59:33.000Z | m3 |
| Esc. Br. La Casa del Molí - HOS098-S06-01 I22BB009987T | HOS098 | HOS098 Esc. Br. La Casa del Molí | S06 | 2026-06-07T16:58:27.000Z | m3 |
| Pavelló M. d'Esports - HOS106-S06-01 I18BD030318Z | HOS106 | HOS106 Pavelló M. d'Esports | S06 | 2026-06-17T17:55:12.000Z | m3 |
| CGG la Ermita - HOS118-S06-01 I19BD042435Z | HOS118 | HOS118 CGG la Ermita | S06 | 2026-06-17T15:51:37.000Z | m3 |
| CGG del polígon Gornal - HOS120-S06-01 H23VA120591E | HOS120 | HOS120 CGG del polígon Gornal | S06 | 2026-06-20T16:03:26.000Z | m3 |
| Museu Can Riera - HOS127-S06-01 H23VA095644X | HOS127 | HOS127 Museu Can Riera | S06 | 2026-06-20T18:58:03.000Z | m3 |
| Deixalleria Municipal - HOS132-S06-01 I17BD045696M | HOS132 | HOS132 Deixalleria Municipal | S06 | 2026-06-19T17:01:12.000Z | m3 |
| Residencia Els Alps - HOS136-S06-01 I17BD083286K | HOS136 | HOS136 Residencia Els Alps | S06 | 2026-06-19T17:46:01.000Z | m3 |
| 0018b24000019623 | — |  | S07 | 2026-06-19T11:45:32.491Z | gas |
| Esc. Bernat Metge - 0018b2400001960b - HOS040 | HOS040 | HOS040 Esc. Bernat Metge | S07 | 2026-06-21T18:59:00.811Z | gas |
| Esc. Joaquim Ruyra - HOS046 | HOS046 | HOS046 Esc. Joaquim Ruyra | S07 | 2026-06-21T08:50:42.940Z | gas |
| Esc. Pablo Neruda - 0018b240000198cb-HOS055 | HOS055 | HOS055 Esc. Pablo Neruda | S07 | 2026-06-21T18:59:24.205Z | gas |
| P. M. Gornal - 0018b2400001947d - HOS130 | HOS130 | HOS130 P. M. Gornal | S07 | 2026-06-21T18:56:33.405Z | gas |
| HOS001-1 | HOS001 | HOS001 Aj L'H-Casa Consistorial | S08 | 2026-06-08T13:00:26.323Z | description |
| HOS001-2 | HOS001 | HOS001 Aj L'H-Casa Consistorial | S08 | 2026-06-08T12:32:27.345Z | description |
| HOS010-1 | HOS010 | HOS010 Bibl. i esc. pl. Europa | S08 | 2026-06-08T12:31:26.165Z | description |
| HOS010-2 | HOS010 | HOS010 Bibl. i esc. pl. Europa | S08 | 2026-06-08T12:31:26.273Z | description |
| HOS012-1 | HOS012 | HOS012 Cement. Mun. L'Hospitalet | S08 | 2026-06-08T12:31:57.464Z | description |
| HOS012-2 | HOS012 | HOS012 Cement. Mun. L'Hospitalet | S08 | 2026-06-08T12:33:55.391Z | description |
| HOS040 | HOS040 | HOS040 Esc. Bernat Metge | S08 | 2026-06-08T12:31:43.227Z | description |
| HOS041 | HOS041 | HOS041 Esc. Charlie Rivel | S08 | 2026-06-08T12:31:32.321Z | description |
| HOS041-2 | HOS041 | HOS041 Esc. Charlie Rivel | S08 | 2026-06-08T12:31:32.333Z | description |
| HOS043 | HOS043 | HOS043 Esc. Frederic Mistral | S08 | 2026-06-08T12:31:09.259Z | description |
| HOS045-1 | HOS045 | HOS045 Esc. Joan Maragall | S08 | 2026-06-08T12:32:54.255Z | description |
| HOS045-2 | HOS045 | HOS045 Esc. Joan Maragall | S08 | 2026-06-08T12:32:54.325Z | description |
| HOS046 | HOS046 | HOS046 Esc. Joaquim Ruyra | S08 | 2026-06-08T12:32:49.501Z | description |
| HOS048 | HOS048 | HOS048 Esc. La Carpa | S08 | 2026-06-08T12:32:49.501Z | description |
| HOS050-1 | HOS050 | HOS050 Esc. Lola Anglada | S08 | 2026-06-08T12:32:41.621Z | description |
| HOS050-2 | HOS050 | HOS050 Esc. Lola Anglada | S08 | 2026-06-08T12:32:41.665Z | description |
| HOS050-3 | HOS050 | HOS050 Esc. Lola Anglada | S08 | 2026-06-08T12:32:41.724Z | description |
| HOS054-1 | HOS054 | HOS054 Esc. Milagros Consarnau | S08 | 2026-06-08T12:33:06.232Z | description |
| HOS054-2 | HOS054 | HOS054 Esc. Milagros Consarnau | S08 | 2026-06-08T12:33:06.461Z | description |
| HOS054-3 | HOS054 | HOS054 Esc. Milagros Consarnau | S08 | 2026-06-08T12:33:06.564Z | description |
| HOS061 | HOS061 | HOS061 Esc. Pere Lliscart | S08 | 2026-06-08T12:31:50.317Z | description |
| HOS065 | HOS065 | HOS065 Esc. S. Ramón y Cajal | S08 | 2026-06-08T12:31:53.327Z | description |
| HOS125 | HOS125 | HOS125 Museu Casa Espanya | S08 | 2026-06-08T12:32:41.041Z | description |
| HOS141-1 | HOS141 | HOS141 Institut Eugeni d'Ors | S08 | 2026-06-08T12:31:12.255Z | description |
| HOS141-2 | HOS141 | HOS141 Institut Eugeni d'Ors | S08 | 2026-06-08T12:31:12.332Z | description |
| HOS143-1 | HOS143 | HOS143 Institut Bellvitge | S08 | 2026-06-08T12:31:44.263Z | description |
| HOS143-2 | HOS143 | HOS143 Institut Bellvitge | S08 | 2026-06-08T12:31:44.435Z | description |
| HOS146-1 | HOS146 | HOS146 Institut Europa | S08 | 2026-06-08T12:34:26.226Z | description |
| HOS146-2 | HOS146 | HOS146 Institut Europa | S08 | 2026-06-08T12:32:26.572Z | description |
| HOS150-1 | HOS150 | HOS150 Institut Rubio i Ors | S08 | 2026-06-08T12:31:51.321Z | description |
| HOS150-2 | HOS150 | HOS150 Institut Rubio i Ors | S08 | 2026-06-08T12:31:51.393Z | description |
| HOS152-1 | HOS152 | HOS152 Institut Torras i Bages | S08 | 2026-06-08T12:32:26.461Z | description |
| HOS152-2 | HOS152 | HOS152 Institut Torras i Bages | S08 | 2026-06-08T12:34:26.279Z | description |
| HOS154-1 | HOS154 | HOS154 Institut Jaume Botey | S08 | 2026-06-08T12:32:59.056Z | description |
| HOS154-2 | HOS154 | HOS154 Institut Jaume Botey | S08 | 2026-06-08T12:32:59.273Z | description |
| test | — |  | S14A | 2026-06-08T12:23:58.439Z | temperature_ext |
| HOS041-S14-Meteo (214189) | HOS041 | HOS041 Esc. Charlie Rivel | S14A | 2026-06-21T19:05:31.479Z | temperature_ext |
| HOS045-S14-Meteo (216699) | HOS045 | HOS045 Esc. Joan Maragall | S14A | 2026-06-21T19:05:33.936Z | temperature_ext |
| HOS047-S14-Meteo (215360) | HOS047 | HOS047 Esc. Josep Janes | S14A | 2026-06-21T19:05:32.162Z | temperature_ext |
| HOS050-S14-Meteo (215733) | HOS050 | HOS050 Esc. Lola Anglada | S14A | 2026-06-21T19:05:32.373Z | temperature_ext |
| HOS054-S14-Meteo (215946) | HOS054 | HOS054 Esc. Milagros Consarnau | S14A | 2026-06-21T19:05:33.340Z | temperature_ext |
| HOS061-S14-Meteo(215864) | HOS061 | HOS061 Esc. Pere Lliscart | S14A | 2026-06-21T19:05:33.152Z | temperature_ext |
| 70B3D5CEC0000040 | — |  | S21 | 2026-06-21T11:40:02.889Z | alert_fire |
| 70B3D5CEC0000040 | — |  | S21 | 2026-06-10T11:40:17.976Z | alert_fire |
| 70B3D5CEC000007E | — |  | S21 | 2026-06-21T11:58:41.575Z | alert_fire |
| 70B3D5CEC000007E | — |  | S21 | 2026-06-10T11:59:03.162Z | alert_fire |
| 70B3D5CEC000034C | — |  | S21 | 2026-06-21T10:22:25.354Z | alert_fire |
| 70B3D5CEC000034C | — |  | S21 | 2026-06-11T10:22:41.949Z | alert_fire |
| 70B3D5CEC000034F | — |  | S21 | 2026-06-21T09:36:04.117Z | alert_fire |
| 70B3D5CEC000034F | — |  | S21 | 2026-06-11T09:36:18.317Z | alert_fire |
| 70B3D5CEC0000351 | — |  | S21 | 2026-06-21T13:09:40.066Z | alert_fire |
| 70B3D5CEC0000351 | — |  | S21 | 2026-06-10T13:10:04.630Z | alert_fire |
| 70B3D5CEC0000371 | — |  | S21 | 2026-06-21T15:23:45.777Z | alert_fire |
| 70B3D5CEC0000371 | — |  | S21 | 2026-06-10T15:24:11.613Z | alert_fire |
| 70B3D5CEC0000373 | — |  | S21 | 2026-06-21T09:23:11.035Z | alert_fire |
| 70B3D5CEC0000373 | — |  | S21 | 2026-06-11T09:23:16.328Z | alert_fire |
| 70B3D5CEC0000376 | — |  | S21 | 2026-06-21T13:01:27.071Z | alert_fire |
| 70B3D5CEC0000376 | — |  | S21 | 2026-06-11T13:01:41.129Z | alert_fire |
| 70B3D5CEC000037C | — |  | S21 | 2026-06-21T10:17:50.976Z | alert_fire |
| 70B3D5CEC000037C | — |  | S21 | 2026-06-10T11:36:42.845Z | keepalive |
| 70B3D5CEC000037F | — |  | S21 | 2026-06-21T08:02:50.973Z | alert_fire |
| 70B3D5CEC000037F | — |  | S21 | 2026-06-11T08:03:19.470Z | alert_fire |
| 70B3D5CEC0000380 | — |  | S21 | 2026-06-21T14:03:37.616Z | alert_fire |
| 70B3D5CEC0000380 | — |  | S21 | 2026-06-10T14:04:07.441Z | alert_fire |
| 70B3D5CEC0000386 | — |  | S21 | 2026-06-21T15:29:25.773Z | alert_fire |
| 70B3D5CEC0000386 | — |  | S21 | 2026-06-10T15:28:35.225Z | alert_fire |
| 70B3D5CEC0000389 | — |  | S21 | 2026-06-21T09:13:15.291Z | alert_fire |
| 70B3D5CEC0000389 | — |  | S21 | 2026-06-11T09:13:43.919Z | alert_fire |
| 70B3D5CEC0000393 | — |  | S21 | 2026-06-20T09:49:37.655Z | alert_fire |
| 70B3D5CEC0000393 | — |  | S21 | 2026-06-11T09:50:06.638Z | alert_fire |
| 70B3D5CEC0000394 | — |  | S21 | 2026-06-21T11:56:38.086Z | alert_fire |
| 70B3D5CEC0000394 | — |  | S21 | 2026-06-10T11:56:44.439Z | alert_fire |
| 70B3D5CEC0000396 | — |  | S21 | 2026-06-21T12:58:57.531Z | alert_fire |
| 70B3D5CEC0000396 | — |  | S21 | 2026-06-10T12:59:11.126Z | alert_fire |
| 70B3D5CEC0000399 | — |  | S21 | 2026-06-21T09:56:33.944Z | alert_fire |
| 70B3D5CEC0000399 | — |  | S21 | 2026-06-11T09:56:32.210Z | alert_fire |
| 70B3D5CEC000039A | — |  | S21 | 2026-06-21T11:36:45.525Z | alert_fire |
| 70B3D5CEC000039A | — |  | S21 | 2026-06-10T11:36:58.624Z | alert_fire |
| 70B3D5CEC000039F | — |  | S21 | 2026-06-21T07:06:40.574Z | alert_fire |
| 70B3D5CEC00003A5 | — |  | S21 | 2026-06-21T10:29:27.085Z | alert_fire |
| 70B3D5CEC00003A5 | — |  | S21 | 2026-06-15T06:36:17.532Z | alert_fire |
| 70B3D5CEC00003AD | — |  | S21 | 2026-06-21T09:40:32.991Z | alert_fire |
| 70B3D5CEC00003AD | — |  | S21 | 2026-06-11T09:40:51.467Z | alert_fire |
| 70B3D5CEC00003B6 | — |  | S21 | 2026-06-21T18:31:24.722Z | alert_fire |
| 70B3D5CEC00003B6 | — |  | S21 | 2026-06-10T18:31:35.685Z | alert_fire |
| 70B3D5CEC00003C4 | — |  | S21 | 2026-06-21T10:47:47.310Z | alert_fire |
| 70B3D5CEC00003C4 | — |  | S21 | 2026-06-11T10:48:21.525Z | alert_fire |
| 70B3D5CEC00003CE | — |  | S21 | 2026-06-21T13:38:16.628Z | alert_fire |
| 70B3D5CEC00003CE | — |  | S21 | 2026-06-10T13:38:53.165Z | alert_fire |
| 70B3D5CEC00003DC | — |  | S21 | 2026-06-21T11:10:20.998Z | alert_fire |
| 70B3D5CEC00003DC | — |  | S21 | 2026-06-10T11:10:30.768Z | alert_fire |
| 70B3D5CEC00003F4 | — |  | S21 | 2026-06-21T08:50:45.305Z | alert_fire |
| 70B3D5CEC00003F4 | — |  | S21 | 2026-06-11T08:50:55.699Z | alert_fire |
| 70B3D5CEC00003FD | — |  | S21 | 2026-06-20T10:01:04.414Z | alert_fire |
| 70B3D5CEC00003FD | — |  | S21 | 2026-06-11T10:01:06.192Z | alert_fire |
| 70B3D5CEC0000402 | — |  | S21 | 2026-06-21T09:12:35.177Z | alert_fire |
| 70B3D5CEC0000402 | — |  | S21 | 2026-06-11T09:12:57.418Z | alert_fire |
| 70B3D5CEC000040B | — |  | S21 | 2026-06-21T12:40:30.484Z | alert_fire |
| 70B3D5CEC000040E | — |  | S21 | 2026-06-18T12:16:07.950Z | alert_fire |
| 70B3D5CEC000040E | — |  | S21 | 2026-06-11T09:34:29.532Z | alert_fire |
| 70B3D5CEC000040F | — |  | S21 | 2026-06-21T10:33:24.748Z | alert_fire |
| 70B3D5CEC000040F | — |  | S21 | 2026-06-11T10:33:29.814Z | alert_fire |
| HOS005 | HOS005 | HOS005 Edificio Cobalt | S21 | 2026-06-21T09:13:09.431Z | alert_fire |
| HOS005 | HOS005 | HOS005 Edificio Cobalt | S21 | 2026-06-11T09:07:24.690Z | alert_fire |
| HOS037 | HOS037 | HOS037 Dipòsit Parc de la serp | S21 | 2026-06-21T09:10:20.741Z | alert_fire |
| HOS037 | HOS037 | HOS037 Dipòsit Parc de la serp | S21 | 2026-06-11T09:10:35.785Z | alert_fire |
| HOS041 | HOS041 | HOS041 Esc. Charlie Rivel | S21 | 2026-06-21T07:30:34.434Z | alert_fire |
| HOS041 | HOS041 | HOS041 Esc. Charlie Rivel | S21 | 2026-06-11T07:30:45.307Z | alert_fire |
| HOS099 | HOS099 | HOS099 Esc. Br. Patufet | S21 | 2026-06-21T12:09:15.973Z | alert_fire |
| HOS099 | HOS099 | HOS099 Esc. Br. Patufet | S21 | 2026-06-10T12:09:26.827Z | alert_fire |
| HOS125 | HOS125 | HOS125 Museu Casa Espanya | S21 | 2026-06-10T12:14:07.992Z | alert_fire |
| HOS125 | HOS125 | HOS125 Museu Casa Espanya | S21 | 2026-06-13T12:14:06.042Z | alert_fire |
| HOS001 Aj L'H-Casa Consistorial | HOS001 | HOS001 Aj L'H-Casa Consistorial | S22 | 2026-06-21T19:06:02.492Z | next_time_ferrocarril |
| HOS002 Aj L'H-Ed. Migdia | HOS002 | HOS002 Aj L'H-Ed. Migdia | S22 | 2026-06-21T19:06:02.221Z | next_time_ferrocarril |
| HOS003 Aj L'H-Ed. Girona | HOS003 | HOS003 Aj L'H-Ed. Girona | S22 | 2026-06-21T19:06:02.173Z | next_time_ferrocarril |
| HOS004 CEMFO | HOS004 | HOS004 CEMFO | S22 | 2026-06-21T19:06:01.444Z | next_time_ferrocarril |
| HOS005 Edificio Cobalt | HOS005 | HOS005 Edificio Cobalt | S22 | 2026-06-21T19:06:19.181Z | next_time_ferrocarril |
| HOS007 Biblioteca Can Sumarro | HOS007 | HOS007 Biblioteca Can Sumarro | S22 | 2026-06-21T19:06:17.461Z | next_time_ferrocarril |
| HOS012 Cement. Mun. L'Hospitalet | HOS012 | HOS012 Cement. Mun. L'Hospitalet | S22 | 2026-06-21T19:06:06.340Z | next_time_ferrocarril |
| HOS013 CGG Sanfeliu | HOS013 | HOS013 CGG Sanfeliu | S22 | 2026-06-21T19:06:13.143Z | next_time_ferrocarril |
| Centre d'Atenció Primària Just Oliveras (dte. I)-HOS018 | HOS018 | Centre d'Atenció Primària Just Oliveras  | S22 | 2026-06-21T19:06:06.899Z | next_time_ferrocarril |
| HOS028 Area de Benestar social | HOS028 | HOS028 Area de Benestar social | S22 | 2026-06-21T19:06:13.071Z | next_time_ferrocarril |
| HOS033 Regidoria Districte I | HOS033 | HOS033 Regidoria Districte I | S22 | 2026-06-21T19:06:21.422Z | next_time_ferrocarril |
| HOS037 Dipòsit Parc de la serp | HOS037 | HOS037 Dipòsit Parc de la serp | S22 | 2026-06-21T19:06:19.179Z | next_time_ferrocarril |
| HOS038 Esc. Busquets i Punset | HOS038 | HOS038 Esc. Busquets i Punset | S22 | 2026-06-21T19:06:10.789Z | next_time_ferrocarril |
| HOS039 Esc. Ausias March | HOS039 | HOS039 Esc. Ausias March | S22 | 2026-06-21T19:06:10.500Z | next_time_ferrocarril |
| HOS040 Esc. Bernat Metge | HOS040 | HOS040 Esc. Bernat Metge | S22 | 2026-06-21T19:06:13.693Z | next_time_ferrocarril |
| HOS049 Esc. La Marina | HOS049 | HOS049 Esc. La Marina | S22 | 2026-06-21T19:06:05.867Z | next_time_ferrocarril |
| HOS051 Esc. M. d'E. de Bellvitge | HOS051 | HOS051 Esc. M. d'E. de Bellvitge | S22 | 2026-06-21T19:06:09.728Z | next_time_ferrocarril |
| HOS056 Esc. Patufet Sant Jordi | HOS056 | HOS056 Esc. Patufet Sant Jordi | S22 | 2026-06-21T19:06:19.448Z | next_time_ferrocarril |
| HOS058 Esc. Pau Sans | HOS058 | HOS058 Esc. Pau Sans | S22 | 2026-06-21T19:06:02.222Z | next_time_ferrocarril |
| HOS067 Esc. Sant Josep - El Pi | HOS067 | HOS067 Esc. Sant Josep - El Pi | S22 | 2026-06-21T19:06:04.742Z | next_time_ferrocarril |
| HOS068 Palauet Can Buxeres | HOS068 | HOS068 Palauet Can Buxeres | S22 | 2026-06-21T19:06:01.863Z | next_time_ferrocarril |
| HOS069 Ca n'Olivé | HOS069 | HOS069 Ca n'Olivé | S22 | 2026-06-21T19:06:09.726Z | next_time_ferrocarril |
| HOS070 Ca n'Arús | HOS070 | HOS070 Ca n'Arús | S22 | 2026-06-21T19:06:21.413Z | next_time_ferrocarril |
| L'Hospitalet de Llogregat-HOS072 | HOS072 | L'Hospitalet de Llogregat-HOS072 | S22 | 2026-06-21T19:06:06.320Z | next_time_ferrocarril |
| Bellvitge-HOS073 | HOS073 | Bellvitge-HOS073 | S22 | 2026-06-21T19:06:11.309Z | next_time_ferrocarril |
| Avinguda Carrilet (L1)-HOS082 | HOS082 | Avinguda Carrilet (L1)-HOS082 | S22 | 2026-06-21T19:06:11.310Z | next_time_ferrocarril |
| Bellvitge (L1)-HOS083 | HOS083 | Bellvitge (L1)-HOS083 | S22 | 2026-06-21T19:06:14.833Z | next_time_ferrocarril |
| Rambla Just Oliveras (L1)-HOS086 | HOS086 | Rambla Just Oliveras (L1)-HOS086 | S22 | 2026-06-21T19:06:21.444Z | next_time_ferrocarril |
| Sant Josep-HOS089 | HOS089 | Sant Josep-HOS089 | S22 | 2026-06-21T19:06:04.555Z | next_time_ferrocarril |
| HOS097 Esc. Br. Garabatos | HOS097 | HOS097 Esc. Br. Garabatos | S22 | 2026-06-21T19:06:21.446Z | next_time_ferrocarril |
| HOS099 Esc. Br. Patufet | HOS099 | HOS099 Esc. Br. Patufet | S22 | 2026-06-21T19:06:10.513Z | next_time_ferrocarril |
| Centre d'Atenció Primària Pura Fernández-HOS100 | HOS100 | Centre d'Atenció Primària Pura Fernández | S22 | 2026-06-21T19:06:04.766Z | next_time_ferrocarril |
| HOS115 P. M. Centre | HOS115 | HOS115 P. M. Centre | S22 | 2026-06-21T19:06:10.788Z | next_time_ferrocarril |
| HOS118 CGG la Ermita | HOS118 | HOS118 CGG la Ermita | S22 | 2026-06-21T19:06:01.507Z | next_time_ferrocarril |
| HOS123 CGG Provençana | HOS123 | HOS123 CGG Provençana | S22 | 2026-06-21T19:06:08.971Z | next_time_ferrocarril |
| HOS125 Museu Casa Espanya | HOS125 | HOS125 Museu Casa Espanya | S22 | 2026-06-21T19:06:01.850Z | next_time_ferrocarril |
| HOS126 Museu L'Harmonia | HOS126 | HOS126 Museu L'Harmonia | S22 | 2026-06-21T19:06:13.135Z | next_time_ferrocarril |
| HOS127 Museu Can Riera | HOS127 | HOS127 Museu Can Riera | S22 | 2026-06-21T19:06:16.690Z | next_time_ferrocarril |
| HOS133 Ermita de Santa Eulàlia | HOS133 | HOS133 Ermita de Santa Eulàlia | S22 | 2026-06-21T19:06:06.366Z | next_time_ferrocarril |
| HOS136 Residencia Els Alps | HOS136 | HOS136 Residencia Els Alps | S22 | 2026-06-21T19:06:13.073Z | next_time_ferrocarril |
| HOS139 Esc. Rest. El Repartidor | HOS139 | HOS139 Esc. Rest. El Repartidor | S22 | 2026-06-21T19:06:18.753Z | next_time_ferrocarril |
| IFP (Innovación en Formación Profesional)-HOS140 | HOS140 | IFP (Innovación en Formación Profesional | S22 | 2026-06-21T19:06:19.449Z | next_time_ferrocarril |
| HOS146 Institut Europa | HOS146 | HOS146 Institut Europa | S22 | 2026-06-21T19:06:13.123Z | next_time_ferrocarril |
| HOS147 Institut Mercè Rodoreda | HOS147 | HOS147 Institut Mercè Rodoreda | S22 | 2026-06-21T19:06:06.332Z | next_time_ferrocarril |
| HOS152 Institut Torras i Bages | HOS152 | HOS152 Institut Torras i Bages | S22 | 2026-06-21T19:06:06.889Z | next_time_ferrocarril |
| HOS153 Institut Can Vilumara | HOS153 | HOS153 Institut Can Vilumara | S22 | 2026-06-21T19:06:10.449Z | next_time_ferrocarril |
| Edificio de viviendas C. Prat-HOS162 | HOS162 | Edificio de viviendas C. Prat-HOS162 | S22 | 2026-06-21T19:06:17.145Z | next_time_ferrocarril |
| Unifamiliar C. Ebre-HOS163 | HOS163 | Unifamiliar C. Ebre-HOS163 | S22 | 2026-06-21T19:06:19.128Z | next_time_ferrocarril |
| HOS050-1 | HOS050 | HOS050 Esc. Lola Anglada | S24 | 2026-06-21T19:17:13.614Z | all |
| ID0200J23007500140 | — |  | SIP | 2026-06-21T19:16:14.987Z | connected |
| ID0200J23007500191 | — |  | SIP | 2026-06-14T08:45:55.706Z | connected |
| ID0200J23007500199 | — |  | SIP | 2026-06-21T19:17:15.937Z | connected |
| ID0200J23007500231 | — |  | SIP | 2026-06-21T19:17:32.584Z | connected |
| ID0200J23007500236 | — |  | SIP | 2026-06-21T19:17:34.131Z | connected |
| ID0200J23007500238 | — |  | SIP | 2026-06-21T19:07:37.371Z | connected |
| ID0200J23007500245 | — |  | SIP | 2026-06-21T19:17:41.066Z | connected |
| ID0200J23007500247 | — |  | SIP | 2026-06-21T19:17:46.231Z | connected |
| ID0200J23007500252 | — |  | SIP | 2026-06-21T19:15:59.069Z | connected |
| ID0200J23007500253 | — |  | SIP | 2026-06-19T17:58:54.342Z | connected |
| ID0200J23007500254 | — |  | SIP | 2026-06-21T19:17:33.090Z | connected |
| ID0200J23007500255 | — |  | SIP | 2026-06-21T19:17:36.253Z | connected |
| ID0200J23007500257 | — |  | SIP | 2026-06-21T19:16:10.951Z | connected |
| ID0200J23007500258 | — |  | SIP | 2026-06-21T19:16:08.195Z | connected |
| ID0200J23007500259 | — |  | SIP | 2026-06-21T19:15:59.043Z | connected |
| ID0200J23007500260 | — |  | SIP | 2026-06-21T19:15:55.163Z | connected |
| ID0200J23007500261 | — |  | SIP | 2026-06-21T19:17:41.494Z | connected |
| ID0200J23007500262 | — |  | SIP | 2026-06-21T19:17:34.492Z | connected |
| ID0200J23007500263 | — |  | SIP | 2026-06-21T19:16:18.919Z | connected |
| ID0200J23007500264 | — |  | SIP | 2026-06-21T19:16:00.519Z | connected |
| ID0200J23007500268 | — |  | SIP | 2026-06-21T19:15:57.986Z | connected |
| ID0200J23007500271 | — |  | SIP | 2026-06-21T19:16:03.749Z | connected |
| ID0200J23007500273 | — |  | SIP | 2026-06-21T19:17:39.224Z | connected |
| ID0200J23007500274 | — |  | SIP | 2026-06-21T19:16:18.919Z | connected |
| ID0200J23007500275 | — |  | SIP | 2026-06-21T19:17:47.717Z | connected |
| ID0200J23007500278 | — |  | SIP | 2026-06-21T18:45:26.251Z | connected |
| ID0200J23007500281 | — |  | SIP | 2026-06-21T19:16:06.933Z | connected |
| ID0200J23007500282 | — |  | SIP | 2026-06-21T19:16:53.172Z | connected |
| ID0200J23007500283 | — |  | SIP | 2026-06-21T19:16:14.987Z | connected |
| ID0200J23007500312 | — |  | SIP | 2026-06-21T19:15:54.486Z | connected |
| ID0200J23007500313 | — |  | SIP | 2026-06-21T19:17:10.009Z | connected |
| ID0200J23007500315 | — |  | SIP | 2026-06-21T19:17:47.197Z | connected |
| ID0200J23007500317 | — |  | SIP | 2026-06-21T19:16:08.906Z | connected |
| ID0200J23007500319 | — |  | SIP | 2026-06-21T19:16:00.516Z | connected |
| ID0200J23007500322 | — |  | SIP | 2026-06-21T19:16:18.919Z | connected |
| ID0200J23007500325 | — |  | SIP | 2026-06-21T19:16:18.227Z | connected |
| ID0200J23007500331 | — |  | SIP | 2026-06-21T19:16:21.350Z | connected |
| ID0200J23007500331 | — |  | SIP | 2026-06-08T12:32:01.993Z | connected |
| ID0200J23007500334 | — |  | SIP | 2026-06-21T19:15:59.796Z | connected |
| ID0200J23007500336 | — |  | SIP | 2026-06-21T19:17:47.902Z | connected |
| ID0200J23007500337 | — |  | SIP | 2026-06-14T08:46:07.397Z | connected |
| ID0200J23007500338 | — |  | SIP | 2026-06-21T19:16:10.523Z | connected |
| ID0200J23007500340 | — |  | SIP | 2026-06-21T19:16:13.749Z | connected |
| ID0200J23007500341 | — |  | SIP | 2026-06-19T09:01:34.749Z | connected |
| ID0200J23007500344 | — |  | SIP | 2026-06-21T19:17:40.019Z | connected |
| ID0200J23007500345 | — |  | SIP | 2026-06-20T10:16:53.941Z | connected |
| ID0200J23007500358 | — |  | SIP | 2026-06-21T19:17:34.327Z | connected |
| ID0200J23007500362 | — |  | SIP | 2026-06-21T19:17:05.073Z | connected |
| ID0200J23007500373 | — |  | SIP | 2026-06-21T19:16:20.626Z | connected |
| ID0200J23007500388 | — |  | SIP | 2026-06-21T19:16:07.747Z | connected |

## Sensores sin datos (1164)

| id | HOS | Sistema | Motivo |
|---|---|---|---|
| I22LA020277R | — | S06 | NO_DATA |
| Can Boixeres (L5)-HOS081 | HOS081 | S22 | NO_DATA |
| Can Serra (L1)-HOS079 | HOS079 | S22 | NO_DATA |
| Can Tries Gornal (L9)-HOS087 | HOS087 | S22 | NO_DATA |
| Can Vidalet (L5)-HOS080 | HOS080 | S22 | NO_DATA |
| Centre Telecom. i Tecnologies de la Informació (CTTI)-HOS165 | HOS165 | S22 | NO_DATA |
| Centre comercial Gran Via 2-HOS093 | HOS093 | S22 | NO_DATA |
| Centre d'Atenció Primària Florida (dte. IV)-HOS019 | HOS019 | S22 | NO_DATA |
| Centre d'Atenció Primària Gornal (dte. VI)-HOS017 | HOS017 | S22 | NO_DATA |
| Collblanc (L5)-HOS075 | HOS075 | S22 | NO_DATA |
| Escola de Música - Centre de les Arts-HOS071 | HOS071 | S22 | NO_DATA |
| Europa Fira-HOS091 | HOS091 | S22 | NO_DATA |
| Fira (L9)-HOS074 | HOS074 | S22 | NO_DATA |
| Florida (L1)-HOS077 | HOS077 | S22 | NO_DATA |
| Gornal-HOS092 | HOS092 | S22 | NO_DATA |
| HOS006 Cal Gotlla | HOS006 | S22 | NO_DATA |
| HOS010 Bibl. i esc. pl. Europa | HOS010 | S22 | NO_DATA |
| HOS014 CGG de la Torrassa | HOS014 | S22 | NO_DATA |
| HOS015 CGG Santa Eulalia | HOS015 | S22 | NO_DATA |
| HOS023 C. M. Ana Díaz Rico | HOS023 | S22 | NO_DATA |
| HOS024 Torre Barrina | HOS024 | S22 | NO_DATA |
| HOS027 A. B. B. S. - Dte. VI | HOS027 | S22 | NO_DATA |
| HOS044 Esc. Gornal | HOS044 | S22 | NO_DATA |
| HOS046 Esc. Joaquim Ruyra | HOS046 | S22 | NO_DATA |
| HOS047 Esc. Josep Janes | HOS047 | S22 | NO_DATA |
| HOS052 Esc. Màrius Torres | HOS052 | S22 | NO_DATA |
| HOS059 Esc. Pau Vila | HOS059 | S22 | NO_DATA |
| HOS063 Esc. Prat de la Manta | HOS063 | S22 | NO_DATA |
| HOS064 Esc. Puig i Gairalt | HOS064 | S22 | NO_DATA |
| HOS066 Esc. Ramon Muntaner | HOS066 | S22 | NO_DATA |
| HOS096 Esc. Br. Nova Fortuny | HOS096 | S22 | NO_DATA |
| HOS105 Calzedonia | HOS105 | S22 | NO_DATA |
| HOS110 P. M. Fum d'Estampa | HOS110 | S22 | NO_DATA |
| HOS117 Mercat Merca-2 Bellvitge | HOS117 | S22 | NO_DATA |
| HOS128 Edificio PUIG | HOS128 | S22 | NO_DATA |
| HOS130 P. M. Gornal | HOS130 | S22 | NO_DATA |
| HOS143 Institut Bellvitge | HOS143 | S22 | NO_DATA |
| HOS154 Institut Jaume Botey | HOS154 | S22 | NO_DATA |
| Hospital Duran i Reynals - Institut Catala Oncologia-HOS031 | HOS031 | S22 | NO_DATA |
| Hospital General de L'Hospitalet-HOS032 | HOSPITAL | S22 | NO_DATA |
| Hospital de Bellvitge (L1)-HOS084 | HOSPITAL | S22 | NO_DATA |
| Ikea-HOS095 | HOS095 | S22 | NO_DATA |
| Provençana (L10)-HOS094 | HOS094 | S22 | NO_DATA |
| Pubilla Cases (L5)-HOS085 | HOS085 | S22 | NO_DATA |
| Residència Collblanc Companys Socials-HOS138 | HOS138 | S22 | NO_DATA |
| Torrassa (L1)-HOS076 | HOS076 | S22 | NO_DATA |
| ID0200J23007500383 | — | SIP | NO_DATA |
| HOS044-S01-01 | HOS044 | S01 | NO_RESOURCE |
| HOS136-S01-01 (T257517) | HOS136 | S01 | NO_RESOURCE |
| BET00230154 | — | S02 | NO_RESOURCE |
| Deixalleria Municipal - HOS132-S02-01 BET00230060 | HOS132 | S02 | NO_RESOURCE |
| HOS011-S02-01 BET00210039 | HOS011 | S02 | NO_RESOURCE |
| HOS015-S02-01 | HOS015 | S02 | NO_RESOURCE |
| HOS024-S02-01-BET00230039 | HOS024 | S02 | NO_RESOURCE |
| HOS102-S02-01 BET00230042 | HOS102 | S02 | NO_RESOURCE |
| HOS103-S02-01 BET00230036 | HOS103 | S02 | NO_RESOURCE |
| HOS104-S02-01 BET00230044 | HOS104 | S02 | NO_RESOURCE |
| HOS105-S02-01 BET00230045 | HOS105 | S02 | NO_RESOURCE |
| HOS128-S02-01 BET00230038 | HOS128 | S02 | NO_RESOURCE |
| HOS134-S02-01 BET00230041 | HOS134 | S02 | NO_RESOURCE |
| HOS137-S02-01 BET00230037 | HOS137 | S02 | NO_RESOURCE |
| HOS157-S02-01 BET00230040 | HOS157 | S02 | NO_RESOURCE |
| HOS501-S02-01 BET00230026 - AJUNTAMENT | HOS501 | S02 | NO_RESOURCE |
| HOS502-S02-01 BET00230027 | HOS502 | S02 | NO_RESOURCE |
| HOS503-S02-01 BET00230058 | HOS503 | S02 | NO_RESOURCE |
| HOS504-S02-01 BET00230059 | HOS504 | S02 | NO_RESOURCE |
| HOS505-S02-01 BET00230061 | HOS505 | S02 | NO_RESOURCE |
| HOS506-S02-01 BET00230062 | HOS506 | S02 | NO_RESOURCE |
| HOS507-S02-01 BET00230063 | HOS507 | S02 | NO_RESOURCE |
| HOS508-S02-01 BET00230064 | HOS508 | S02 | NO_RESOURCE |
| HOS509-S02-01 BET00230065 | HOS509 | S02 | NO_RESOURCE |
| HOS510-S02-01 BET00230066 | HOS510 | S02 | NO_RESOURCE |
| HOS511-S02-01 BET00230067 | HOS511 | S02 | NO_RESOURCE |
| HOS512-S02-01 BET00230068 | HOS512 | S02 | NO_RESOURCE |
| HOS513-S02-01 BET00230144 | HOS513 | S02 | NO_RESOURCE |
| HOS514-S02-01 BET00230145 | HOS514 | S02 | NO_RESOURCE |
| HOS515-S02-01 BET00230146 | HOS515 | S02 | NO_RESOURCE |
| HOS516-S02-01 BET00230147 | HOS516 | S02 | NO_RESOURCE |
| HOS517-S02-01 BET00230148 | HOS517 | S02 | NO_RESOURCE |
| HOS518-S02-01 BET00230149 | HOS518 | S02 | NO_RESOURCE |
| HOS519-S02-01 BET00230150 | HOS519 | S02 | NO_RESOURCE |
| HOS520-S02-01 BET00230151 | HOS520 | S02 | NO_RESOURCE |
| HOS521-S02-01 BET00230152 | HOS521 | S02 | NO_RESOURCE |
| HOS522-S02-01 BET00230153 | HOS522 | S02 | NO_RESOURCE |
| HOS523-S02-01 BET00240027 | HOS523 | S02 | NO_RESOURCE |
| HOS001-S03-01 | HOS001 | S03 | NO_RESOURCE |
| Aj L'H-Casa Consistorial-HOS001 | — | S04 | NO_RESOURCE |
| HOS001-S04-01 | HOS001 | S04 | NO_RESOURCE |
| HOS003-S04-01 | HOS003 | S04 | NO_RESOURCE |
| HOS004-S04-01 | HOS004 | S04 | NO_RESOURCE |
| HOS008-S04-01 | HOS008 | S04 | NO_RESOURCE |
| HOS010-S04-01 | HOS010 | S04 | NO_RESOURCE |
| HOS021-S04-01 | HOS021 | S04 | NO_RESOURCE |
| HOS022-S04-01 | HOS022 | S04 | NO_RESOURCE |
| HOS023-S04-01 | HOS023 | S04 | NO_RESOURCE |
| HOS024-S04-01 | HOS024 | S04 | NO_RESOURCE |
| HOS025-S04-01 | HOS025 | S04 | NO_RESOURCE |
| HOS026-S04-01 | HOS026 | S04 | NO_RESOURCE |
| HOS027-S04-01 | HOS027 | S04 | NO_RESOURCE |
| HOS030-S04-01 | HOS030 | S04 | NO_RESOURCE |
| HOS033-S04-01 | HOS033 | S04 | NO_RESOURCE |
| HOS033-S04-02 | HOS033 | S04 | NO_RESOURCE |
| HOS034-S04-01 | HOS034 | S04 | NO_RESOURCE |
| HOS035-S04-01 | HOS035 | S04 | NO_RESOURCE |
| HOS038-S04-01 | HOS038 | S04 | NO_RESOURCE |
| HOS039-S04-01 | HOS039 | S04 | NO_RESOURCE |
| HOS040-S04-01 | HOS040 | S04 | NO_RESOURCE |
| HOS041-S04-01 | HOS041 | S04 | NO_RESOURCE |
| HOS042-S04-01 | HOS042 | S04 | NO_RESOURCE |
| HOS043-S04-01 | HOS043 | S04 | NO_RESOURCE |
| HOS044-S04-01 | HOS044 | S04 | NO_RESOURCE |
| HOS045-S04-01 | HOS045 | S04 | NO_RESOURCE |
| HOS046-S04-01 | HOS046 | S04 | NO_RESOURCE |
| HOS047-S04-01 | HOS047 | S04 | NO_RESOURCE |
| HOS048-S04-01 | HOS048 | S04 | NO_RESOURCE |
| HOS049-S04-01 | HOS049 | S04 | NO_RESOURCE |
| HOS050-S04-01 | HOS050 | S04 | NO_RESOURCE |
| HOS051-S04-01 | HOS051 | S04 | NO_RESOURCE |
| HOS052-S04-01 | HOS052 | S04 | NO_RESOURCE |
| HOS053-S04-01 | HOS053 | S04 | NO_RESOURCE |
| HOS054-S04-01 | HOS054 | S04 | NO_RESOURCE |
| HOS055-S04-01 | HOS055 | S04 | NO_RESOURCE |
| HOS056-S04-01 | HOS056 | S04 | NO_RESOURCE |
| HOS057-S04-01 | HOS057 | S04 | NO_RESOURCE |
| HOS058-S04-01 | HOS058 | S04 | NO_RESOURCE |
| HOS059-S04-01 | HOS059 | S04 | NO_RESOURCE |
| HOS060-S04-01 | HOS060 | S04 | NO_RESOURCE |
| HOS061-S04-01 | HOS061 | S04 | NO_RESOURCE |
| HOS062-S04-01 | HOS062 | S04 | NO_RESOURCE |
| HOS063-S04-01 | HOS063 | S04 | NO_RESOURCE |
| HOS064-S04-01 | HOS064 | S04 | NO_RESOURCE |
| HOS065-S04-01 | HOS065 | S04 | NO_RESOURCE |
| HOS066-S04-01 | HOS066 | S04 | NO_RESOURCE |
| HOS067-S04-01 | HOS067 | S04 | NO_RESOURCE |
| HOS069-S04-01 | HOS069 | S04 | NO_RESOURCE |
| HOS096-S04-01 | HOS096 | S04 | NO_RESOURCE |
| HOS098-S04-01 | HOS098 | S04 | NO_RESOURCE |
| HOS099-S04-01 | HOS099 | S04 | NO_RESOURCE |
| HOS117-S04-01 | HOS117 | S04 | NO_RESOURCE |
| HOS121-S04-01 | HOS121 | S04 | NO_RESOURCE |
| HOS125-S04-01 | HOS125 | S04 | NO_RESOURCE |
| HOS126-S04-01 | HOS126 | S04 | NO_RESOURCE |
| HOS127-S04-01 | HOS127 | S04 | NO_RESOURCE |
| HOS136-S04-01 | HOS136 | S04 | NO_RESOURCE |
| HOS141-S04-01 | HOS141 | S04 | NO_RESOURCE |
| HOS143-S04-01 | HOS143 | S04 | NO_RESOURCE |
| HOS144-S04-01 | HOS144 | S04 | NO_RESOURCE |
| HOS146-S04-01 | HOS146 | S04 | NO_RESOURCE |
| HOS147-S04-01 | HOS147 | S04 | NO_RESOURCE |
| HOS148-S04-01 | HOS148 | S04 | NO_RESOURCE |
| HOS149-S04-01 | HOS149 | S04 | NO_RESOURCE |
| HOS150-S04-01 | HOS150 | S04 | NO_RESOURCE |
| HOS151-S04-01 | HOS151 | S04 | NO_RESOURCE |
| HOS152-S04-01 | HOS152 | S04 | NO_RESOURCE |
| HOS153-S04-01 | HOS153 | S04 | NO_RESOURCE |
| HOS154-S04-01 | HOS154 | S04 | NO_RESOURCE |
| HOS155-S04-01 | HOS155 | S04 | NO_RESOURCE |
| HOS156-S04-01 | HOS156 | S04 | NO_RESOURCE |
| 22323387990069 | — | S05 | NO_RESOURCE |
| 22323387990187 | — | S05 | NO_RESOURCE |
| 22324388010270 | — | S05 | NO_RESOURCE |
| 22324388010283 | — | S05 | NO_RESOURCE |
| 22324388010284 | — | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| Esc. Patufet Sant Jordi-HOS056 | HOS056 | S05 | NO_RESOURCE |
| HOS003-S05-01 | HOS003 | S05 | NO_RESOURCE |
| HOS004-S05-01 | HOS004 | S05 | NO_RESOURCE |
| HOS005-S05-01 | HOS005 | S05 | NO_RESOURCE |
| HOS006-S05-01 | HOS006 | S05 | NO_RESOURCE |
| HOS012-S05-01 | HOS012 | S05 | NO_RESOURCE |
| HOS022-S05-01 | HOS022 | S05 | NO_RESOURCE |
| HOS023-S05-01 | HOS023 | S05 | NO_RESOURCE |
| HOS024-S05-01 | HOS024 | S05 | NO_RESOURCE |
| HOS025-S05-01 | HOS025 | S05 | NO_RESOURCE |
| HOS026-S05-01 | HOS026 | S05 | NO_RESOURCE |
| HOS027-S05-01 | HOS027 | S05 | NO_RESOURCE |
| HOS029 | HOS029 | S05 | NO_RESOURCE |
| HOS030-S05-01 | HOS030 | S05 | NO_RESOURCE |
| HOS033-S05-01 | HOS033 | S05 | NO_RESOURCE |
| HOS034-S05-01 | HOS034 | S05 | NO_RESOURCE |
| HOS035-S05-01 | HOS035 | S05 | NO_RESOURCE |
| HOS036-S05-01 | HOS036 | S05 | NO_RESOURCE |
| HOS037-S05-01 | HOS037 | S05 | NO_RESOURCE |
| HOS038-S05-01 | HOS038 | S05 | NO_RESOURCE |
| HOS039-S05-01 | HOS039 | S05 | NO_RESOURCE |
| HOS040-S05-01 | HOS040 | S05 | NO_RESOURCE |
| HOS041-S05-01 | HOS041 | S05 | NO_RESOURCE |
| HOS042-S05-01 | HOS042 | S05 | NO_RESOURCE |
| HOS043-S05-01 | HOS043 | S05 | NO_RESOURCE |
| HOS044-S05-01 | HOS044 | S05 | NO_RESOURCE |
| HOS045-S05-01 | HOS045 | S05 | NO_RESOURCE |
| HOS046-S05-01 | HOS046 | S05 | NO_RESOURCE |
| HOS047-S05-01 | HOS047 | S05 | NO_RESOURCE |
| HOS048-S05-01 | HOS048 | S05 | NO_RESOURCE |
| HOS049-S05-01 | HOS049 | S05 | NO_RESOURCE |
| HOS050-S05-01 | HOS050 | S05 | NO_RESOURCE |
| HOS051-S05-01 | HOS051 | S05 | NO_RESOURCE |
| HOS052-S05-01 | HOS052 | S05 | NO_RESOURCE |
| HOS054-S05-01 | HOS054 | S05 | NO_RESOURCE |
| HOS055-S05-01 | HOS055 | S05 | NO_RESOURCE |
| HOS057-S05-01 | HOS057 | S05 | NO_RESOURCE |
| HOS058-S05-01 | HOS058 | S05 | NO_RESOURCE |
| HOS059-S05-01 | HOS059 | S05 | NO_RESOURCE |
| HOS060-S05-01 | HOS060 | S05 | NO_RESOURCE |
| HOS061-S05-01 | HOS061 | S05 | NO_RESOURCE |
| HOS062-S05-01 | HOS062 | S05 | NO_RESOURCE |
| HOS063-S05-01 | HOS063 | S05 | NO_RESOURCE |
| HOS064-S05-01 | HOS064 | S05 | NO_RESOURCE |
| HOS065-S05-01 | HOS065 | S05 | NO_RESOURCE |
| HOS066-S05-01 | HOS066 | S05 | NO_RESOURCE |
| HOS067-S05-01 | HOS067 | S05 | NO_RESOURCE |
| HOS069-S05-01 | HOS069 | S05 | NO_RESOURCE |
| HOS088-S05-01 | HOS088 | S05 | NO_RESOURCE |
| HOS096-S05-01 | HOS096 | S05 | NO_RESOURCE |
| HOS098-S05-01 | HOS098 | S05 | NO_RESOURCE |
| HOS099-S05-01 | HOS099 | S05 | NO_RESOURCE |
| HOS125-S05-01 | HOS125 | S05 | NO_RESOURCE |
| HOS126-S05-01 | HOS126 | S05 | NO_RESOURCE |
| HOS127-S05-01 | HOS127 | S05 | NO_RESOURCE |
| HOS132-S05-01 | HOS132 | S05 | NO_RESOURCE |
| HOS136-S05-01 | HOS136 | S05 | NO_RESOURCE |
| P. M. Centre-HOS115 | HOS115 | S05 | NO_RESOURCE |
| SISTEMA_5 | — | S05 | NO_RESOURCE |
|  | — | S06 | NO_RESOURCE |
| A. B. B. S. - Dte. VI - HOS027-S06-01 I23BD005559K | HOS027 | S06 | NO_RESOURCE |
| A. B. S. S. - Dte. IV/V - HOS026-S06-01 D16BA108177L | HOS026 | S06 | NO_RESOURCE |
| Aj L'H-Ed. Girona - HOS003-S06-01 I22BB010103W | HOS003 | S06 | NO_RESOURCE |
| Aj L'H-Ed. Migdia - HOS002-S06-01 D16UH084259X | HOS002 | S06 | NO_RESOURCE |
| Area de Benestar social - HOS028-S06-01 H23VA120131G | HOS028 | S06 | NO_RESOURCE |
| Bibl. i C. C. la Bòbila - HOS008-S06-01 P18UF031335N | HOS008 | S06 | NO_RESOURCE |
| Bibl. i esc. pl. Europa - HOS010-S06-01 I22BD035149C | — | S06 | NO_RESOURCE |
| Biblioteca Can Sumarro - HOS007-S06-01 I17BD504878W | HOS007 | S06 | NO_RESOURCE |
| Biblioteca la Florida - HOS009-S06-01 D17BA214472T | HOS009 | S06 | NO_RESOURCE |
| C. C.  Tecla Sala - HOS022-S06-01 I17BD504011F | HOS022 | S06 | NO_RESOURCE |
| C. C. Santa Eulàlia - HOS021-S06-01 P20VA148641W | HOS021 | S06 | NO_RESOURCE |
| C.E.M. L'Hospitalet Nord - HOS109-S06-01 P22UH724572R | HOS109 | S06 | NO_RESOURCE |
| CEMFO - HOS004-S06-01 I17BE046798C | HOS004 | S06 | NO_RESOURCE |
| CGG Provençana - HOS023-S06-01 I17BC013010U | HOS023 | S06 | NO_RESOURCE |
| CGG Pubilla Casas - HOS025-S06-01 H23VA084841R | HOS025 | S06 | NO_RESOURCE |
| CGG de Can Serra - HOS122-S06-01 P21VA198542C | HOS122 | S06 | NO_RESOURCE |
| CGG del polígon Gornal - HOS120-S06-01 H23VA120591E | HOS120 | S06 | NO_RESOURCE |
| CGG la Ermita - HOS118-S06-01 I19BD042435Z | HOS118 | S06 | NO_RESOURCE |
| Ca n'Arús - HOS070-S06-01 I20BD020169P | HOS070 | S06 | NO_RESOURCE |
| Ca n'Olivé - HOS069-S06-01 H23VA095642V | HOS069 | S06 | NO_RESOURCE |
| Cal Gotlla - HOS006-S06-01 D18BA388376I | HOS006 | S06 | NO_RESOURCE |
| Can Colom - HOS030-S06-02 I22BB051956F | HOS030 | S06 | NO_RESOURCE |
| Casa dels Cargols - HOS029-S06-01 H22VA827558M | HOS029 | S06 | NO_RESOURCE |
| D15TC125050O | — | S06 | NO_RESOURCE |
| D16TD053003Y | — | S06 | NO_RESOURCE |
| D17BA245795C | — | S06 | NO_RESOURCE |
| D8683450377492801I21BE056200A | — | S06 | NO_RESOURCE |
| Deixalleria Municipal - HOS132-S06-01 I17BD045696M | HOS132 | S06 | NO_RESOURCE |
| Dipòsit Parc de la serp - HOS037-S06-01 H24VA628016X | HOS037 | S06 | NO_RESOURCE |
| Dipòsit Santa Eulàlia - HOS036-S06-01 I20LA195865W | HOS036 | S06 | NO_RESOURCE |
| E. M. Futbol L'Hospitalet - HOS108-S06-01 P22UI000467I | HOS108 | S06 | NO_RESOURCE |
| Edificio Cobalt - HOS005-S06-01 P24VA123225Q | HOS005 | S06 | NO_RESOURCE |
| Esc. Ausias March - HOS039-S06-01 I20BD036700P | HOS039 | S06 | NO_RESOURCE |
| Esc. Br. Garabatos - HOS097-S06-01 P22FA007729T | — | S06 | NO_RESOURCE |
| Esc. Br. La Casa del Molí - HOS098-S06-01 I22BB009987T | HOS098 | S06 | NO_RESOURCE |
| Esc. Br. Nova Fortuny - HOS096-S06-01 P23AD727227S | HOS096 | S06 | NO_RESOURCE |
| Esc. Br. Patufet - HOS099-S06-01 I24LA262898U | HOS099 | S06 | NO_RESOURCE |
| Esc. Busquets i Punset - HOS038-S06-01 P20AD552738S | HOS038 | S06 | NO_RESOURCE |
| Esc. Charlie Rivel - HOS041-S06-01 I22BB010137G | HOS041 | S06 | NO_RESOURCE |
| Esc. J. M. Folch i Torres - HOS042-S06-01 P18AD500362J | HOS042 | S06 | NO_RESOURCE |
| Esc. Joaquim Ruyra - HOS046-S06-01 I25BD024043L | HOS046 | S06 | NO_RESOURCE |
| Esc. Josep Janes - HOS047-S06-01 I17BE094519Y | HOS047 | S06 | NO_RESOURCE |
| Esc. La Carpa - HOS048-S06-01 P18UE276480O | HOS048 | S06 | NO_RESOURCE |
| Esc. Lola Anglada - HOS050-S06-01 P18AD500319G | HOS050 | S06 | NO_RESOURCE |
| Esc. M. d'E. de Bellvitge - HOS051-S06-01 I21BC007255G | HOS051 | S06 | NO_RESOURCE |
| Esc. Menéndez Pidal - HOS053-S06-01 I18BD030305U | HOS053 | S06 | NO_RESOURCE |
| Esc. Milagros Consarnau - HOS054-S06-S1 I18BD030306V | HOS054 | S06 | NO_RESOURCE |
| Esc. Pablo Neruda - HOS055-S06-01 I24BC057137B | HOS055 | S06 | NO_RESOURCE |
| Esc. Patufet Sant Jordi - HOS056-S06-01 D15FE071450J | HOS056 | S06 | NO_RESOURCE |
| Esc. Pau Casals - HOS057-S06-01 I18BD030309Y | HOS057 | S06 | NO_RESOURCE |
| Esc. Pau Sans - HOS058-S06-01 I22BD021841U | HOS058 | S06 | NO_RESOURCE |
| Esc. Pau Vila - HOS059-S06-01 P22FA001797H | HOS059 | S06 | NO_RESOURCE |
| Esc. Pep Ventura - HOS060-S06-01 ESCOLA PEP VENTURA | HOS060 | S06 | NO_RESOURCE |
| Esc. Pere Lliscart - HOS061-S06-01 I18BD030283F | HOS061 | S06 | NO_RESOURCE |
| Esc. Pompeu Fabra - HOS062-S06-01 I18BD030308X | HOS062 | S06 | NO_RESOURCE |
| Esc. Prat de la Manta - HOS063-S06-01 P18UE276499Z | HOS063 | S06 | NO_RESOURCE |
| Esc. Puig i Gairalt - HOS064-S06-1 I18BD030289L | HOS064 | S06 | NO_RESOURCE |
| Esc. Rest. El Repartidor - HOS139-S06-01 C15FA550083J | HOS139 | S06 | NO_RESOURCE |
| Esc. S. Ramón y Cajal - HOS065-S06-01 I22BD089711V | HOS065 | S06 | NO_RESOURCE |
| H23VA083135U | — | S06 | NO_RESOURCE |
| H23VA083135U | — | S06 | NO_RESOURCE |
| H23VA083135U | — | S06 | NO_RESOURCE |
| H23VA083135U | — | S06 | NO_RESOURCE |
| H23VA864747G | — | S06 | NO_RESOURCE |
| HOS001-S06-01 I19BD035462J | HOS001 | S06 | NO_RESOURCE |
| HOS119-S06-01 P21UF000569J | HOS119 | S06 | NO_RESOURCE |
| HOS162-S06-01 D17BA088747O | HOS162 | S06 | NO_RESOURCE |
| HOS164-S06-01 D18BA010631X | HOS164 | S06 | NO_RESOURCE |
| I16BD105801Y | — | S06 | NO_RESOURCE |
| I17BC041526Y | — | S06 | NO_RESOURCE |
| I17BD014384G | — | S06 | NO_RESOURCE |
| I17BD096770I | — | S06 | NO_RESOURCE |
| I17BE063112M | — | S06 | NO_RESOURCE |
| I17BE085778O | — | S06 | NO_RESOURCE |
| I17BE085778O | — | S06 | NO_RESOURCE |
| I17BE085778O | — | S06 | NO_RESOURCE |
| I17BE085778O | — | S06 | NO_RESOURCE |
| I17BE085778O | — | S06 | NO_RESOURCE |
| I17BF045531G | — | S06 | NO_RESOURCE |
| I18BC012582E | — | S06 | NO_RESOURCE |
| I18BC030788S | — | S06 | NO_RESOURCE |
| I18BD012202M | — | S06 | NO_RESOURCE |
| I18BD012202M | — | S06 | NO_RESOURCE |
| I18BD012202M | — | S06 | NO_RESOURCE |
| I18BD033258Q | — | S06 | NO_RESOURCE |
| I18BD033597G | — | S06 | NO_RESOURCE |
| I18BD039671X | — | S06 | NO_RESOURCE |
| I18BE082533S | — | S06 | NO_RESOURCE |
| I19BB015889I | — | S06 | NO_RESOURCE |
| I19BC062758S | — | S06 | NO_RESOURCE |
| I19BD042447D | — | S06 | NO_RESOURCE |
| I20BB038156H | — | S06 | NO_RESOURCE |
| I20BD020143F | — | S06 | NO_RESOURCE |
| I20BD036673D | — | S06 | NO_RESOURCE |
| I20BD078435T | — | S06 | NO_RESOURCE |
| I20LA078279G | — | S06 | NO_RESOURCE |
| I20LA223736D | — | S06 | NO_RESOURCE |
| I20LA228706R | — | S06 | NO_RESOURCE |
| I21BB036576Y | — | S06 | NO_RESOURCE |
| I21BC007276L | — | S06 | NO_RESOURCE |
| I21BD015287S | — | S06 | NO_RESOURCE |
| I21BD017030D | — | S06 | NO_RESOURCE |
| I22BB010257N | — | S06 | NO_RESOURCE |
| I22BB051758B | — | S06 | NO_RESOURCE |
| I22BC001723Y | — | S06 | NO_RESOURCE |
| I22BC022199O | — | S06 | NO_RESOURCE |
| I22BC022199O | — | S06 | NO_RESOURCE |
| I22BC056178O | — | S06 | NO_RESOURCE |
| I22BC056178O | — | S06 | NO_RESOURCE |
| I22BC092123D | — | S06 | NO_RESOURCE |
| I22BC092123D | — | S06 | NO_RESOURCE |
| I22BD053196L | — | S06 | NO_RESOURCE |
| I22BD089717B | — | S06 | NO_RESOURCE |
| I22BD089718C | — | S06 | NO_RESOURCE |
| I22LA020277R | — | S06 | NO_RESOURCE |
| I23BB001380X | — | S06 | NO_RESOURCE |
| I23BB012089G | — | S06 | NO_RESOURCE |
| I23BB012089G | — | S06 | NO_RESOURCE |
| I23BC010176D | — | S06 | NO_RESOURCE |
| I23BD005562F | — | S06 | NO_RESOURCE |
| I23BD011418N | — | S06 | NO_RESOURCE |
| I23BD017868H | — | S06 | NO_RESOURCE |
| I23BD021926H | — | S06 | NO_RESOURCE |
| I23BE024445O | — | S06 | NO_RESOURCE |
| I23BE066999T | — | S06 | NO_RESOURCE |
| I24BC057126Y | — | S06 | NO_RESOURCE |
| I24BD057468Y | — | S06 | NO_RESOURCE |
| I24LA138052L | — | S06 | NO_RESOURCE |
| I25BD024186Z | — | S06 | NO_RESOURCE |
| I25BD102387U | — | S06 | NO_RESOURCE |
| I26BB006351N | — | S06 | NO_RESOURCE |
| J25FA091773F | — | S06 | NO_RESOURCE |
| Mercat Merca-2 Bellvitge - HOS117-S06-01 P24UG742861K | HOS117 | S06 | NO_RESOURCE |
| Mercat del Torrent Gornal - HOS124-S06-01 P23VA148607V | HOS124 | S06 | NO_RESOURCE |
| Museu Can Riera - HOS127-S06-01 H23VA095644X | HOS127 | S06 | NO_RESOURCE |
| Museu Casa Espanya - HOS125-S06-01 P23FA027637J | HOS125 | S06 | NO_RESOURCE |
| Museu L'Harmonia - HOS126-S06-01 P23FA005374N | HOS126 | S06 | NO_RESOURCE |
| P. M. Centre - HOS115-S06-01 P14BH094224F | HOS115 | S06 | NO_RESOURCE |
| P. M. Fum d'Estampa - HOS110-S06-01 P23UF789879A | HOS110 | S06 | NO_RESOURCE |
| P. M. Gornal - HOS130-S06-01 P24UG743696T | HOS130 | S06 | NO_RESOURCE |
| P. M. Les Planes - HOS111-S06-01 P21UG990150O | HOS111 | S06 | NO_RESOURCE |
| P. M. Sanfeliu - HOS114-S06-01 POLIESPORTIU SANFELIU | HOS114 | S06 | NO_RESOURCE |
| P. M. Santa Eulàlia - HOS112-S06-01 P16BH813211W | HOS112 | S06 | NO_RESOURCE |
| P. M. Sergio Manzano - HOS113-S06-01 P18UG031358B | HOS113 | S06 | NO_RESOURCE |
| P16VA111023D | — | S06 | NO_RESOURCE |
| P18AD500332D | — | S06 | NO_RESOURCE |
| P18UE276339K | — | S06 | NO_RESOURCE |
| P18UE276483R | — | S06 | NO_RESOURCE |
| P18UG043847A | — | S06 | NO_RESOURCE |
| P19UE039966U | — | S06 | NO_RESOURCE |
| P19UE039975V | — | S06 | NO_RESOURCE |
| P19UE040018G | — | S06 | NO_RESOURCE |
| P19UF026339P | — | S06 | NO_RESOURCE |
| P20VA163658V | — | S06 | NO_RESOURCE |
| P21UE000954H | — | S06 | NO_RESOURCE |
| P22UE716336P | — | S06 | NO_RESOURCE |
| P22UE716341M | — | S06 | NO_RESOURCE |
| P22UF521430S | — | S06 | NO_RESOURCE |
| P23AD727226R | — | S06 | NO_RESOURCE |
| P23FA018698V | — | S06 | NO_RESOURCE |
| P23UH800297G | — | S06 | NO_RESOURCE |
| P24AB721542X | — | S06 | NO_RESOURCE |
| P24UF737486P | — | S06 | NO_RESOURCE |
| P24UG742875Q | — | S06 | NO_RESOURCE |
| P25AD361634T | — | S06 | NO_RESOURCE |
| Pavelló M. d'Esports - HOS106-S06-01 I18BD030318Z | HOS106 | S06 | NO_RESOURCE |
| Piscines M. L'Hospitalet - HOS107-S06-01 P19UF003436T | HOS107 | S06 | NO_RESOURCE |
| Radio-TV de L'Hospitalet - HOS088-S06-01 I24LA138394E | — | S06 | NO_RESOURCE |
| Regidoria Districte I - HOS033-S06-01 P23FA015384U | HOS033 | S06 | NO_RESOURCE |
| Regidoria Districte II - HOS034-S06-01 C15FA260208R | HOS034 | S06 | NO_RESOURCE |
| Residencia Els Alps - HOS136-S06-01 I17BD083286K | HOS136 | S06 | NO_RESOURCE |
| S06-01 D16BA113364X | — | S06 | NO_RESOURCE |
| S06-01 D17BA087741E | — | S06 | NO_RESOURCE |
| S06-01 H23VA120599M | — | S06 | NO_RESOURCE |
| S06-01 I17BC095962D | — | S06 | NO_RESOURCE |
| Teatre Joventut - HOS159-S06-01 P20UH000838Q | HOS159 | S06 | NO_RESOURCE |
| ZZ-DUPLICADO D18BA010631X | — | S06 | NO_RESOURCE |
| 0018b240000193f3 | — | S07 | NO_RESOURCE |
| 0018b24000019407 | — | S07 | NO_RESOURCE |
| 0018b24000019612 | — | S07 | NO_RESOURCE |
| 0018b2400001961a | — | S07 | NO_RESOURCE |
| 0018b2400001961f-HOS045 | — | S07 | NO_RESOURCE |
| 0018b2400001962d | — | S07 | NO_RESOURCE |
| 0018b2400001962e | — | S07 | NO_RESOURCE |
| 0018b24000019632 | — | S07 | NO_RESOURCE |
| 0018b24000019858 - Edificio 1 | — | S07 | NO_RESOURCE |
| 0018b2400001989a | — | S07 | NO_RESOURCE |
| 0018b240000198a3 | — | S07 | NO_RESOURCE |
| 0018b240000198aa | — | S07 | NO_RESOURCE |
| CEMFO - 0018b24000019306 - HOS004 | HOS004 | S07 | NO_RESOURCE |
| Dipòsit Santa Eulàlia - 0018b24000019430 - HOS036 | HOS036 | S07 | NO_RESOURCE |
| Esc. Bernat Metge - 0018b2400001960b - HOS040 | HOS040 | S07 | NO_RESOURCE |
| Esc. Joaquim Ruyra - HOS046 | HOS046 | S07 | NO_RESOURCE |
| Esc. La Carpa - HOS048 | HOS048 | S07 | NO_RESOURCE |
| Esc. Pablo Neruda - 0018b240000198cb-HOS055 | HOS055 | S07 | NO_RESOURCE |
| P. M. Gornal - 0018b2400001947d - HOS130 | HOS130 | S07 | NO_RESOURCE |
| Residencia Els Alps - HOS136 | HOS136 | S07 | NO_RESOURCE |
| 1092 | — | S08 | NO_RESOURCE |
| 1112 | — | S08 | NO_RESOURCE |
| 1113 | — | S08 | NO_RESOURCE |
| 1117 | — | S08 | NO_RESOURCE |
| 1119 | — | S08 | NO_RESOURCE |
| 1121 | — | S08 | NO_RESOURCE |
| 1122 | — | S08 | NO_RESOURCE |
| Esc. Pau Sans-HOS058-1 | HOS058 | S08 | NO_RESOURCE |
| Esc. Puig i Gairalt-HOS064-1 | HOS064 | S08 | NO_RESOURCE |
| Esc. Sant Josep - El Pi-HOS067 | HOS067 | S08 | NO_RESOURCE |
| Esc. Sant Josep - El Pi-HOS067-1131 | HOS067 | S08 | NO_RESOURCE |
| HOS001-S08-01 | HOS001 | S08 | NO_RESOURCE |
| HOS001-S08-02 | HOS001 | S08 | NO_RESOURCE |
| HOS012-S08-01 | HOS012 | S08 | NO_RESOURCE |
| HOS012-S08-02 | HOS012 | S08 | NO_RESOURCE |
| HOS039-S08-01 | HOS039 | S08 | NO_RESOURCE |
| HOS039-S08-02 | HOS039 | S08 | NO_RESOURCE |
| HOS040-S08-01 | HOS040 | S08 | NO_RESOURCE |
| HOS041-S08-01 | HOS041 | S08 | NO_RESOURCE |
| HOS041-S08-02 | HOS041 | S08 | NO_RESOURCE |
| HOS042-S08-01 | HOS042 | S08 | NO_RESOURCE |
| HOS043-S08-01 | HOS043 | S08 | NO_RESOURCE |
| HOS044-S08-01 | HOS044 | S08 | NO_RESOURCE |
| HOS044-S08-02 | HOS044 | S08 | NO_RESOURCE |
| HOS045-S08-01 | HOS045 | S08 | NO_RESOURCE |
| HOS045-S08-02 | HOS045 | S08 | NO_RESOURCE |
| HOS046-S08-01 | HOS046 | S08 | NO_RESOURCE |
| HOS047-S08-01 | HOS047 | S08 | NO_RESOURCE |
| HOS048-S08-01 | HOS048 | S08 | NO_RESOURCE |
| HOS049-S08-01 | HOS049 | S08 | NO_RESOURCE |
| HOS049-S08-02 | HOS049 | S08 | NO_RESOURCE |
| HOS049-S08-03 | HOS049 | S08 | NO_RESOURCE |
| HOS050-S08-01 | HOS050 | S08 | NO_RESOURCE |
| HOS050-S08-02 | HOS050 | S08 | NO_RESOURCE |
| HOS050-S08-03 | HOS050 | S08 | NO_RESOURCE |
| HOS051-S08-01 | HOS051 | S08 | NO_RESOURCE |
| HOS052-S08-01 | HOS052 | S08 | NO_RESOURCE |
| HOS053-S08-01 | HOS053 | S08 | NO_RESOURCE |
| HOS054-S08-01 | HOS054 | S08 | NO_RESOURCE |
| HOS054-S08-02 | HOS054 | S08 | NO_RESOURCE |
| HOS054-S08-03 | HOS054 | S08 | NO_RESOURCE |
| HOS055-S08-01 | HOS055 | S08 | NO_RESOURCE |
| HOS057-S08-01 | HOS057 | S08 | NO_RESOURCE |
| HOS057-S08-02 | HOS057 | S08 | NO_RESOURCE |
| HOS061-S08-01 | HOS061 | S08 | NO_RESOURCE |
| HOS065-S08-01 | HOS065 | S08 | NO_RESOURCE |
| HOS096-S08-01 | HOS096 | S08 | NO_RESOURCE |
| HOS125-S08-01 | HOS125 | S08 | NO_RESOURCE |
| HOS136-S08-01 | HOS136 | S08 | NO_RESOURCE |
| HOS141-S08-01 | HOS141 | S08 | NO_RESOURCE |
| HOS141-S08-02 | HOS141 | S08 | NO_RESOURCE |
| HOS142-S08-01 | HOS142 | S08 | NO_RESOURCE |
| HOS142-S08-02 | HOS142 | S08 | NO_RESOURCE |
| HOS143-S08-01 | HOS143 | S08 | NO_RESOURCE |
| HOS143-S08-02 | HOS143 | S08 | NO_RESOURCE |
| HOS145-S08-02 | HOS145 | S08 | NO_RESOURCE |
| HOS146-S08-01 | HOS146 | S08 | NO_RESOURCE |
| HOS146-S08-02 | HOS146 | S08 | NO_RESOURCE |
| HOS147-S08-01 | HOS147 | S08 | NO_RESOURCE |
| HOS147-S08-02 | HOS147 | S08 | NO_RESOURCE |
| HOS150-S08-01 | HOS150 | S08 | NO_RESOURCE |
| HOS150-S08-02 | HOS150 | S08 | NO_RESOURCE |
| HOS151-S08-01 | HOS151 | S08 | NO_RESOURCE |
| HOS152-S08-01 | HOS152 | S08 | NO_RESOURCE |
| HOS152-S08-02 | HOS152 | S08 | NO_RESOURCE |
| HOS154-S08-01 | HOS154 | S08 | NO_RESOURCE |
| HOS154-S08-02 | HOS154 | S08 | NO_RESOURCE |
| HOS156-S08-01 | HOS156 | S08 | NO_RESOURCE |
| HOS156-S08-02 | HOS156 | S08 | NO_RESOURCE |
| Institut Llobregat-HOS155-2 | HOS155 | S08 | NO_RESOURCE |
| Institut Margarida Xirgu-HOS148-2 | HOS148 | S08 | NO_RESOURCE |
| Institut Pedraforca-HOS149-2 | HOS149 | S08 | NO_RESOURCE |
| HOS001-S09-01 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-02 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-03 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-04 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-05 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-06 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-07 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-08 | HOS001 | S09 | NO_RESOURCE |
| HOS001-S09-09 | HOS001 | S09 | NO_RESOURCE |
| HOS003-S09-01 | HOS003 | S09 | NO_RESOURCE |
| HOS004-S09-01 | HOS004 | S09 | NO_RESOURCE |
| HOS005-S09-01 | HOS005 | S09 | NO_RESOURCE |
| HOS006-S09-01 | HOS006 | S09 | NO_RESOURCE |
| HOS008-S09-01 | HOS008 | S09 | NO_RESOURCE |
| HOS010-S09-01 | HOS010 | S09 | NO_RESOURCE |
| HOS012-S09-01 | HOS012 | S09 | NO_RESOURCE |
| HOS021-S09-01 | HOS021 | S09 | NO_RESOURCE |
| HOS022-S09-01 | HOS022 | S09 | NO_RESOURCE |
| HOS023-S09-01 | HOS023 | S09 | NO_RESOURCE |
| HOS024-S09-01 | HOS024 | S09 | NO_RESOURCE |
| HOS025-S09-01 | HOS025 | S09 | NO_RESOURCE |
| HOS026-S09-01 | HOS026 | S09 | NO_RESOURCE |
| HOS027-S09-01 | HOS027 | S09 | NO_RESOURCE |
| HOS028-S09-01 | HOS028 | S09 | NO_RESOURCE |
| HOS029-S09-01 | HOS029 | S09 | NO_RESOURCE |
| HOS030-S09-01 | HOS030 | S09 | NO_RESOURCE |
| HOS033-S09-01 | HOS033 | S09 | NO_RESOURCE |
| HOS034-S09-01 | HOS034 | S09 | NO_RESOURCE |
| HOS035-S09-01 | HOS035 | S09 | NO_RESOURCE |
| HOS036-S09-01 | HOS036 | S09 | NO_RESOURCE |
| HOS037-S09-01 | HOS037 | S09 | NO_RESOURCE |
| HOS042-S09-01 | HOS042 | S09 | NO_RESOURCE |
| HOS043-S09-01 | HOS043 | S09 | NO_RESOURCE |
| HOS045-S09-01 | HOS045 | S09 | NO_RESOURCE |
| HOS048-S09-01 | HOS048 | S09 | NO_RESOURCE |
| HOS049-S09-01 | HOS049 | S09 | NO_RESOURCE |
| HOS052-S09-01 | HOS052 | S09 | NO_RESOURCE |
| HOS053-S09-01 | HOS053 | S09 | NO_RESOURCE |
| HOS056-S09-01 | HOS056 | S09 | NO_RESOURCE |
| HOS060-S09-01 | HOS060 | S09 | NO_RESOURCE |
| HOS061-S09-01 | HOS061 | S09 | NO_RESOURCE |
| HOS062-S09-01 | HOS062 | S09 | NO_RESOURCE |
| HOS064-S09-01 | HOS064 | S09 | NO_RESOURCE |
| HOS065-S09-01 | HOS065 | S09 | NO_RESOURCE |
| HOS069-S09-01 | HOS069 | S09 | NO_RESOURCE |
| HOS088-S09-01 | HOS088 | S09 | NO_RESOURCE |
| HOS096-S09-01 | HOS096 | S09 | NO_RESOURCE |
| HOS098-S09-01 | HOS098 | S09 | NO_RESOURCE |
| HOS099-S09-01 | HOS099 | S09 | NO_RESOURCE |
| HOS125-S09-01 | HOS125 | S09 | NO_RESOURCE |
| HOS126-S09-01 | HOS126 | S09 | NO_RESOURCE |
| HOS132-S09-01 | HOS132 | S09 | NO_RESOURCE |
| HOS136-S09-01 | HOS136 | S09 | NO_RESOURCE |
| HOS024-S13-01 | HOS024 | S13A | NO_RESOURCE |
| HOS033-S13-01 | HOS033 | S13A | NO_RESOURCE |
| HOS049-S13-01 | HOS049 | S13A | NO_RESOURCE |
| HOS050-S13-01 | HOS050 | S13A | NO_RESOURCE |
| HOS052-S13-01 | HOS052 | S13A | NO_RESOURCE |
| HOS055-S13-01 | HOS055 | S13A | NO_RESOURCE |
| HOS056-S13-01 | HOS056 | S13A | NO_RESOURCE |
| HOS057-S13-01 | HOS057 | S13A | NO_RESOURCE |
| HOS059-S13-01 | HOS059 | S13A | NO_RESOURCE |
| HOS063-S13-01 | HOS063 | S13A | NO_RESOURCE |
| HOS099 - Esc. Br. Patufet | HOS099 | S13A | NO_RESOURCE |
| HOS125-S13-01 | HOS125 | S13A | NO_RESOURCE |
| HOS126-S13-01 | HOS126 | S13A | NO_RESOURCE |
| HOS129-S13-01 | HOS129 | S13A | NO_RESOURCE |
| 215285 | — | S14A | NO_RESOURCE |
| HOS039-S14-Meteo (216694) | HOS039 | S14A | NO_RESOURCE |
| HOS041-S14-Meteo (214189) | HOS041 | S14A | NO_RESOURCE |
| HOS045-S14-Meteo (216699) | HOS045 | S14A | NO_RESOURCE |
| HOS047-S14-Meteo (215360) | HOS047 | S14A | NO_RESOURCE |
| HOS050-S14-Meteo (215733) | HOS050 | S14A | NO_RESOURCE |
| HOS053-S14-Meteo (215854) | HOS053 | S14A | NO_RESOURCE |
| HOS054-S14-Meteo (215946) | HOS054 | S14A | NO_RESOURCE |
| HOS058-S14-Meteo (215289) | HOS058 | S14A | NO_RESOURCE |
| HOS061-S14-Meteo(215864) | HOS061 | S14A | NO_RESOURCE |
| HOS125-S14-Meteo (???) | HOS125 | S14A | NO_RESOURCE |
| HOS126-S14-Meteo (221405 ) | HOS126 | S14A | NO_RESOURCE |
| HOS039-S14-Pira | HOS039 | S14B | NO_RESOURCE |
| HOS041-S14-Pira | HOS041 | S14B | NO_RESOURCE |
| HOS045-S14-Pira | HOS045 | S14B | NO_RESOURCE |
| HOS047-S14-Pira | HOS047 | S14B | NO_RESOURCE |
| HOS050-S14-Pira | HOS050 | S14B | NO_RESOURCE |
| HOS053-S14-Pira | HOS053 | S14B | NO_RESOURCE |
| HOS054-S14-Pira | HOS054 | S14B | NO_RESOURCE |
| HOS058-S14-Pira | HOS058 | S14B | NO_RESOURCE |
| HOS061-S14-Pira | HOS061 | S14B | NO_RESOURCE |
| HOS125-S14-Pira | HOS125 | S14B | NO_RESOURCE |
| HOS126-S14-Pira | HOS126 | S14B | NO_RESOURCE |
| HOS001-S15-01 | HOS001 | S15 | NO_RESOURCE |
| HOS003-S15-01 | HOS003 | S15 | NO_RESOURCE |
| HOS004-S15-01 | HOS004 | S15 | NO_RESOURCE |
| HOS004-S15-02 | HOS004 | S15 | NO_RESOURCE |
| HOS004-S15-03 | HOS004 | S15 | NO_RESOURCE |
| HOS026-S15-01 | HOS026 | S15 | NO_RESOURCE |
| HOS026-S15-02 | HOS026 | S15 | NO_RESOURCE |
| HOS026-S15-03 | HOS026 | S15 | NO_RESOURCE |
| HOS027-S15-01 | HOS027 | S15 | NO_RESOURCE |
| HOS029-S1-01 | HOS029 | S15 | NO_RESOURCE |
| HOS029-S1-02 | HOS029 | S15 | NO_RESOURCE |
| HOS029-S1-03 | HOS029 | S15 | NO_RESOURCE |
| HOS030-S15-01 | HOS030 | S15 | NO_RESOURCE |
| HOS030-S15-02 | HOS030 | S15 | NO_RESOURCE |
| HOS030-S15-03 | HOS030 | S15 | NO_RESOURCE |
| HOS033-S15-01 | HOS033 | S15 | NO_RESOURCE |
| HOS033-S15-02 | HOS033 | S15 | NO_RESOURCE |
| HOS033-S15-03 | HOS033 | S15 | NO_RESOURCE |
| HOS034-S15-01 | HOS034 | S15 | NO_RESOURCE |
| HOS034-S15-02 | HOS034 | S15 | NO_RESOURCE |
| HOS034-S15-03 | HOS034 | S15 | NO_RESOURCE |
| HOS035-S15-01 | HOS035 | S15 | NO_RESOURCE |
| HOS035-S15-02 | HOS035 | S15 | NO_RESOURCE |
| HOS035-S15-03 | HOS035 | S15 | NO_RESOURCE |
| HOS035-S15-04 | HOS035 | S15 | NO_RESOURCE |
| HOS035-S15-05 | HOS035 | S15 | NO_RESOURCE |
| HOS069-S15-01 | HOS069 | S15 | NO_RESOURCE |
| HOS069-S15-02 | HOS069 | S15 | NO_RESOURCE |
| HOS132-S15-01 | HOS132 | S15 | NO_RESOURCE |
| HOS132-S15-02 | HOS132 | S15 | NO_RESOURCE |
| HOS132-S15-03 | HOS132 | S15 | NO_RESOURCE |
| HOS109-S17-01 | HOS109 | S17 | NO_RESOURCE |
| HOS121-S17-01 | HOS121 | S17 | NO_RESOURCE |
| HOS130-S17-01 (051001812) | HOS130 | S17 | NO_RESOURCE |
| HOS130-S17-02 (051001716) | HOS130 | S17 | NO_RESOURCE |
| HOS004-S19-01 | HOS004 | S19 | NO_RESOURCE |
| HOS005-S19-01 | HOS005 | S19 | NO_RESOURCE |
| HOS038-S19-01 | HOS038 | S19 | NO_RESOURCE |
| HOS038-S19-02 | HOS038 | S19 | NO_RESOURCE |
| HOS039-S19-01 | HOS039 | S19 | NO_RESOURCE |
| HOS040-S19-01 | HOS040 | S19 | NO_RESOURCE |
| HOS041-S19-01 | HOS041 | S19 | NO_RESOURCE |
| HOS041-S19-02 | HOS041 | S19 | NO_RESOURCE |
| HOS042-S19-01 | HOS042 | S19 | NO_RESOURCE |
| HOS042-S19-02 | HOS042 | S19 | NO_RESOURCE |
| HOS043-S19-01 | HOS043 | S19 | NO_RESOURCE |
| HOS044-S19-01 | HOS044 | S19 | NO_RESOURCE |
| HOS045-S19-01 | HOS045 | S19 | NO_RESOURCE |
| HOS045-S19-02 | HOS045 | S19 | NO_RESOURCE |
| HOS046-S19-01 | HOS046 | S19 | NO_RESOURCE |
| HOS047-S19-01 | HOS047 | S19 | NO_RESOURCE |
| HOS047-S19-02 | HOS047 | S19 | NO_RESOURCE |
| HOS047-S19-03 | HOS047 | S19 | NO_RESOURCE |
| HOS048-S19-01 | HOS048 | S19 | NO_RESOURCE |
| HOS049-S19-01 | HOS049 | S19 | NO_RESOURCE |
| HOS049-S19-02 | HOS049 | S19 | NO_RESOURCE |
| HOS050-S19-01 | HOS050 | S19 | NO_RESOURCE |
| HOS051-S19-01 | HOS051 | S19 | NO_RESOURCE |
| HOS051-S19-02 | HOS051 | S19 | NO_RESOURCE |
| HOS051-S19-03 | HOS051 | S19 | NO_RESOURCE |
| HOS052-S19-01 | HOS052 | S19 | NO_RESOURCE |
| HOS053-S19-01 | HOS053 | S19 | NO_RESOURCE |
| HOS053-S19-02 | HOS053 | S19 | NO_RESOURCE |
| HOS054-S19-01 | HOS054 | S19 | NO_RESOURCE |
| HOS054-S19-02 | HOS054 | S19 | NO_RESOURCE |
| HOS055-S19-01 | HOS055 | S19 | NO_RESOURCE |
| HOS055-S19-02 | HOS055 | S19 | NO_RESOURCE |
| HOS055-S19-03 | HOS055 | S19 | NO_RESOURCE |
| HOS056-S19-01 | HOS056 | S19 | NO_RESOURCE |
| HOS057-S19-01 | HOS057 | S19 | NO_RESOURCE |
| HOS057-S19-02 | HOS057 | S19 | NO_RESOURCE |
| HOS058-S19-01 | HOS058 | S19 | NO_RESOURCE |
| HOS058-S19-02 | HOS058 | S19 | NO_RESOURCE |
| HOS059-S19-01 | HOS059 | S19 | NO_RESOURCE |
| HOS059-S19-02 | HOS059 | S19 | NO_RESOURCE |
| HOS059-S19-03 | HOS059 | S19 | NO_RESOURCE |
| HOS060-S19-01 | HOS060 | S19 | NO_RESOURCE |
| HOS061-S19-01 | HOS061 | S19 | NO_RESOURCE |
| HOS062-S19-01 | HOS062 | S19 | NO_RESOURCE |
| HOS062-S19-02 | HOS062 | S19 | NO_RESOURCE |
| HOS063-S19-01 | HOS063 | S19 | NO_RESOURCE |
| HOS063-S19-02 | HOS063 | S19 | NO_RESOURCE |
| HOS063-S19-03 | HOS063 | S19 | NO_RESOURCE |
| HOS064-S19-01 | HOS064 | S19 | NO_RESOURCE |
| HOS064-S19-02 | HOS064 | S19 | NO_RESOURCE |
| HOS064-S19-03 | HOS064 | S19 | NO_RESOURCE |
| HOS064-S19-04 | HOS064 | S19 | NO_RESOURCE |
| HOS065-S19-01 | HOS065 | S19 | NO_RESOURCE |
| HOS065-S19-02 | HOS065 | S19 | NO_RESOURCE |
| HOS065-S19-03 | HOS065 | S19 | NO_RESOURCE |
| HOS066-S19-01 | HOS066 | S19 | NO_RESOURCE |
| HOS066-S19-02 | HOS066 | S19 | NO_RESOURCE |
| HOS066-S19-03 | HOS066 | S19 | NO_RESOURCE |
| HOS067-S19-01 | HOS067 | S19 | NO_RESOURCE |
| HOS098-S19-01 | HOS098 | S19 | NO_RESOURCE |
| HOS099-S19-01 | HOS099 | S19 | NO_RESOURCE |
| HOS125 | HOS125 | S19 | NO_RESOURCE |
| HOS125-S19-01 | HOS125 | S19 | NO_RESOURCE |
| HOS136-S19-01 | HOS136 | S19 | NO_RESOURCE |
| Torre Barrina - HOS024 | HOS024 | S19 | NO_RESOURCE |
| HOS001-S20-01 | HOS001 | S20 | NO_RESOURCE |
| HOS003-S20-01 | HOS003 | S20 | NO_RESOURCE |
| HOS004-S20-01 | HOS004 | S20 | NO_RESOURCE |
| HOS005-S20-01 | HOS005 | S20 | NO_RESOURCE |
| HOS006-S20-01 | HOS006 | S20 | NO_RESOURCE |
| HOS012-S20-01 | HOS012 | S20 | NO_RESOURCE |
| HOS021-S20-01 | HOS021 | S20 | NO_RESOURCE |
| HOS022-S20-01 | HOS022 | S20 | NO_RESOURCE |
| HOS023-S20-01 | HOS023 | S20 | NO_RESOURCE |
| HOS024-S20-01 | HOS024 | S20 | NO_RESOURCE |
| HOS025-S20-01 | HOS025 | S20 | NO_RESOURCE |
| HOS026-S20-01 | HOS026 | S20 | NO_RESOURCE |
| HOS027-S20-01 | HOS027 | S20 | NO_RESOURCE |
| HOS029-S20-01 | HOS029 | S20 | NO_RESOURCE |
| HOS030-S20-01 | HOS030 | S20 | NO_RESOURCE |
| HOS033-S20-01 | HOS033 | S20 | NO_RESOURCE |
| HOS034-S20-01 | HOS034 | S20 | NO_RESOURCE |
| HOS035-S20-01 | HOS035 | S20 | NO_RESOURCE |
| HOS036-S20-01 | HOS036 | S20 | NO_RESOURCE |
| HOS037-S20-01 | HOS037 | S20 | NO_RESOURCE |
| HOS038-S20-01 | HOS038 | S20 | NO_RESOURCE |
| HOS039-S20-01 | HOS039 | S20 | NO_RESOURCE |
| HOS040-S20-01 | HOS040 | S20 | NO_RESOURCE |
| HOS041-S20-01 | HOS041 | S20 | NO_RESOURCE |
| HOS042-S20-01 | HOS042 | S20 | NO_RESOURCE |
| HOS043-S20-01 | HOS043 | S20 | NO_RESOURCE |
| HOS044-S20-01 | HOS044 | S20 | NO_RESOURCE |
| HOS045-S20-01 | HOS045 | S20 | NO_RESOURCE |
| HOS046-S20-01 | HOS046 | S20 | NO_RESOURCE |
| HOS047-S20-01 | HOS047 | S20 | NO_RESOURCE |
| HOS048-S20-01 | HOS048 | S20 | NO_RESOURCE |
| HOS049-S20-01 | HOS049 | S20 | NO_RESOURCE |
| HOS050-S20-01 | HOS050 | S20 | NO_RESOURCE |
| HOS051-S20-01 | HOS051 | S20 | NO_RESOURCE |
| HOS052-S20-01 | HOS052 | S20 | NO_RESOURCE |
| HOS053-S20-01 | HOS053 | S20 | NO_RESOURCE |
| HOS054-S20-01 | HOS054 | S20 | NO_RESOURCE |
| HOS055-S20-01 | HOS055 | S20 | NO_RESOURCE |
| HOS056-S20-01 | HOS056 | S20 | NO_RESOURCE |
| HOS057-S20-01 | HOS057 | S20 | NO_RESOURCE |
| HOS058-S20-01 | HOS058 | S20 | NO_RESOURCE |
| HOS059-S20-01 | HOS059 | S20 | NO_RESOURCE |
| HOS060-S20-01 | HOS060 | S20 | NO_RESOURCE |
| HOS061-S20-01 | HOS061 | S20 | NO_RESOURCE |
| HOS062-S20-01 | HOS062 | S20 | NO_RESOURCE |
| HOS063-S20-01 | HOS063 | S20 | NO_RESOURCE |
| HOS064-S20-01 | HOS064 | S20 | NO_RESOURCE |
| HOS065-S20-01 | HOS065 | S20 | NO_RESOURCE |
| HOS066-S20-01 | HOS066 | S20 | NO_RESOURCE |
| HOS067-S20-01 | HOS067 | S20 | NO_RESOURCE |
| HOS069-S20-01 | HOS069 | S20 | NO_RESOURCE |
| HOS088-S20-01 | HOS088 | S20 | NO_RESOURCE |
| HOS096-S20-01 | HOS096 | S20 | NO_RESOURCE |
| HOS098-S20-01 | HOS098 | S20 | NO_RESOURCE |
| HOS099-S20-01 | HOS099 | S20 | NO_RESOURCE |
| HOS109-S20-01 | HOS109 | S20 | NO_RESOURCE |
| HOS125 | HOS125 | S20 | NO_RESOURCE |
| HOS125-S20-01 | HOS125 | S20 | NO_RESOURCE |
| HOS126-S20-01 | HOS126 | S20 | NO_RESOURCE |
| HOS132-S20-01 | HOS132 | S20 | NO_RESOURCE |
| HOS136-S20-01 | HOS136 | S20 | NO_RESOURCE |
| 70B3D5CEC000038E | — | S21 | NO_RESOURCE |
| 70B3D5CEC000038E | — | S21 | NO_RESOURCE |
| HOS001-S21-01 | HOS001 | S21 | NO_RESOURCE |
| HOS002-S21-01 | HOS002 | S21 | NO_RESOURCE |
| HOS003-S21-01 | HOS003 | S21 | NO_RESOURCE |
| HOS004-S21-01 | HOS004 | S21 | NO_RESOURCE |
| HOS005 | HOS005 | S21 | NO_RESOURCE |
| HOS005-S21-01 | HOS005 | S21 | NO_RESOURCE |
| HOS006-S21-01 | HOS006 | S21 | NO_RESOURCE |
| HOS007-S21-01 | HOS007 | S21 | NO_RESOURCE |
| HOS008-S21-01 | HOS008 | S21 | NO_RESOURCE |
| HOS012-S21-01 | HOS012 | S21 | NO_RESOURCE |
| HOS021-S21-01 | HOS021 | S21 | NO_RESOURCE |
| HOS022-S21-01 | HOS022 | S21 | NO_RESOURCE |
| HOS023-S21-01 | HOS023 | S21 | NO_RESOURCE |
| HOS024-S21-01 | HOS024 | S21 | NO_RESOURCE |
| HOS025-S21-01 | HOS025 | S21 | NO_RESOURCE |
| HOS026-S21-01 | HOS026 | S21 | NO_RESOURCE |
| HOS027-S21-01 | HOS027 | S21 | NO_RESOURCE |
| HOS028-S21-01 | HOS028 | S21 | NO_RESOURCE |
| HOS029-S21-01 | HOS029 | S21 | NO_RESOURCE |
| HOS030-S21-01 | HOS030 | S21 | NO_RESOURCE |
| HOS033-S21-01 | HOS033 | S21 | NO_RESOURCE |
| HOS034-S21-01 | HOS034 | S21 | NO_RESOURCE |
| HOS035-S21-01 | HOS035 | S21 | NO_RESOURCE |
| HOS036-S21-01 | HOS036 | S21 | NO_RESOURCE |
| HOS037-S21-01 | HOS037 | S21 | NO_RESOURCE |
| HOS038-S21-01 | HOS038 | S21 | NO_RESOURCE |
| HOS038-S21-02 | HOS038 | S21 | NO_RESOURCE |
| HOS039-S21-01 | HOS039 | S21 | NO_RESOURCE |
| HOS040-S21-01 | HOS040 | S21 | NO_RESOURCE |
| HOS041 | HOS041 | S21 | NO_RESOURCE |
| HOS041 | HOS041 | S21 | NO_RESOURCE |
| HOS041-S21-01 | HOS041 | S21 | NO_RESOURCE |
| HOS042-S21-01 | HOS042 | S21 | NO_RESOURCE |
| HOS043-S21-01 | HOS043 | S21 | NO_RESOURCE |
| HOS044-S21-01 | HOS044 | S21 | NO_RESOURCE |
| HOS045-S21-01 | HOS045 | S21 | NO_RESOURCE |
| HOS046-S21-01 | HOS046 | S21 | NO_RESOURCE |
| HOS047-S21-01 | HOS047 | S21 | NO_RESOURCE |
| HOS048-S21-01 | HOS048 | S21 | NO_RESOURCE |
| HOS049-S21-01 | HOS049 | S21 | NO_RESOURCE |
| HOS050-S21-01 | HOS050 | S21 | NO_RESOURCE |
| HOS051-S21-01 | HOS051 | S21 | NO_RESOURCE |
| HOS052-S21-01 | HOS052 | S21 | NO_RESOURCE |
| HOS053-S21-01 | HOS053 | S21 | NO_RESOURCE |
| HOS054-S21-01 | HOS054 | S21 | NO_RESOURCE |
| HOS055-S21-01 | HOS055 | S21 | NO_RESOURCE |
| HOS056-S21-01 | HOS056 | S21 | NO_RESOURCE |
| HOS057-S21-01 | HOS057 | S21 | NO_RESOURCE |
| HOS058-S21-01 | HOS058 | S21 | NO_RESOURCE |
| HOS059-S21-01 | HOS059 | S21 | NO_RESOURCE |
| HOS060-S1-01 | HOS060 | S21 | NO_RESOURCE |
| HOS061-S21-01 | HOS061 | S21 | NO_RESOURCE |
| HOS062-S21-01 | HOS062 | S21 | NO_RESOURCE |
| HOS063-S21-01 | HOS063 | S21 | NO_RESOURCE |
| HOS064-S21-01 | HOS064 | S21 | NO_RESOURCE |
| HOS065-S21-01 | HOS065 | S21 | NO_RESOURCE |
| HOS066-S21-01 | HOS066 | S21 | NO_RESOURCE |
| HOS067-S21-01 | HOS067 | S21 | NO_RESOURCE |
| HOS068-S21-01 | HOS068 | S21 | NO_RESOURCE |
| HOS069-S21-01 | HOS069 | S21 | NO_RESOURCE |
| HOS070-S21-01 | HOS070 | S21 | NO_RESOURCE |
| HOS071-S21-01 | HOS071 | S21 | NO_RESOURCE |
| HOS088-S21-01 | HOS088 | S21 | NO_RESOURCE |
| HOS096-S21-01 | HOS096 | S21 | NO_RESOURCE |
| HOS097-S21-01 | HOS097 | S21 | NO_RESOURCE |
| HOS098-S21-01 | HOS098 | S21 | NO_RESOURCE |
| HOS099 | HOS099 | S21 | NO_RESOURCE |
| HOS099-S21-01 | HOS099 | S21 | NO_RESOURCE |
| HOS108-S21-01 | HOS108 | S21 | NO_RESOURCE |
| HOS109-S21-01 | HOS109 | S21 | NO_RESOURCE |
| HOS110-S21-01 | HOS110 | S21 | NO_RESOURCE |
| HOS111-S21-01 | HOS111 | S21 | NO_RESOURCE |
| HOS112-S21-01 | HOS112 | S21 | NO_RESOURCE |
| HOS113-S21-01 | HOS113 | S21 | NO_RESOURCE |
| HOS114-S21-01 | HOS114 | S21 | NO_RESOURCE |
| HOS117-S21-01 | HOS117 | S21 | NO_RESOURCE |
| HOS124-S21-01 | HOS124 | S21 | NO_RESOURCE |
| HOS125-S21-01 | HOS125 | S21 | NO_RESOURCE |
| HOS126-S21-01 | HOS126 | S21 | NO_RESOURCE |
| HOS127-S21-01 | HOS127 | S21 | NO_RESOURCE |
| HOS130-S21-01 | HOS130 | S21 | NO_RESOURCE |
| HOS132-S21-01 | HOS132 | S21 | NO_RESOURCE |
| HOS136-S21-01 | HOS136 | S21 | NO_RESOURCE |
| HOS139-S21-01 | HOS139 | S21 | NO_RESOURCE |
| HOS159-S21-01 | HOS159 | S21 | NO_RESOURCE |
| HOS162-S21-01 | HOS162 | S21 | NO_RESOURCE |
| A. B. B. S. - Dte. VI - HOS027 | — | S22 | NO_RESOURCE |
| Aj L'H-Casa Consistorial - HOS001 | HOS001 | S22 | NO_RESOURCE |
| Aj L'H-Ed. Girona - HOS003 | HOS003 | S22 | NO_RESOURCE |
| Aj L'H-Ed. Migdia - HOS002 | HOS002 | S22 | NO_RESOURCE |
| Ajuntament de L'Hospitalet - Casa Consistorial-HOS001 | HOS001 | S22 | NO_RESOURCE |
| Ajuntament de L'Hospitalet - Ed. Girona-HOS003 | HOS003 | S22 | NO_RESOURCE |
| Ajuntament de L'Hospitalet - Ed. Migdia-HOS002 | HOS002 | S22 | NO_RESOURCE |
| Ara Vinc-HOS104 | HOS104 | S22 | NO_RESOURCE |
| Area Basica Serveis Socials - Dte. IV/V - Benestar Social-HOS026 | HOS026 | S22 | NO_RESOURCE |
| Area Basica de Serveis Socials - Districte VI-HOS027 | HOS027 | S22 | NO_RESOURCE |
| Area de Benestar social-HOS028 | HOS028 | S22 | NO_RESOURCE |
| Area de Benestar social-HOS028 | HOS028 | S22 | NO_RESOURCE |
| Avinguda Carrilet (L1)-HOS082 | HOS082 | S22 | NO_RESOURCE |
| Bellvitge (L1)-HOS083 | HOS083 | S22 | NO_RESOURCE |
| Bellvitge-HOS073 | HOS073 | S22 | NO_RESOURCE |
| Bibl. i esc. pl. Europa-HOS010 | — | S22 | NO_RESOURCE |
| Biblioteca Can Sumarro - HOS007 | HOS007 | S22 | NO_RESOURCE |
| Biblioteca Can Sumarro-HOS007 | HOS007 | S22 | NO_RESOURCE |
| Biblioteca i Centre Cultural la Bòbila-HOS008 | HOS008 | S22 | NO_RESOURCE |
| Biblioteca i escola bressol plaça Europa-HOS010 | HOS010 | S22 | NO_RESOURCE |
| Biblioteca la Florida-HOS009 | HOS009 | S22 | NO_RESOURCE |
| Bombers de L'Hospitalet-HOS011 | HOS011 | S22 | NO_RESOURCE |
| C. M. Ana Díaz Rico - HOS023 | HOS023 | S22 | NO_RESOURCE |
| CEMFO - HOS004 | HOS004 | S22 | NO_RESOURCE |
| CEMFO-HOS004 | HOS004 | S22 | NO_RESOURCE |
| CGG Provençana - HOS123 | — | S22 | NO_RESOURCE |
| CGG Sanfeliu-HOS013 | HOS013 | S22 | NO_RESOURCE |
| CGG Santa Eulalia - HOS015 | — | S22 | NO_RESOURCE |
| CGG de la Torrassa - HOS014 | — | S22 | NO_RESOURCE |
| CGG la Ermita - HOS118 | HOS118 | S22 | NO_RESOURCE |
| CLD-HOS103 | HOS103 | S22 | NO_RESOURCE |
| Ca n'Arús - HOS070 | HOS070 | S22 | NO_RESOURCE |
| Ca n'Arús-HOS070 | HOS070 | S22 | NO_RESOURCE |
| Ca n'Olivé - HOS069 | HOS069 | S22 | NO_RESOURCE |
| Ca n'Olivé-HOS069 | HOS069 | S22 | NO_RESOURCE |
| Cal Gotlla - HOS006 | — | S22 | NO_RESOURCE |
| Cal Gotlla-HOS006 | HOS006 | S22 | NO_RESOURCE |
| Calzedonia - HOS105 | HOS105 | S22 | NO_RESOURCE |
| Calzedonia-HOS105 | HOS105 | S22 | NO_RESOURCE |
| Can Boixeres (L5)-HOS081 | HOS081 | S22 | NO_RESOURCE |
| Can Colom (Centre Atenció a la Infància i la Dòna)-HOS030 | HOS030 | S22 | NO_RESOURCE |
| Can Serra (L1)-HOS079 | HOS079 | S22 | NO_RESOURCE |
| Can Tries Gornal (L9)-HOS087 | HOS087 | S22 | NO_RESOURCE |
| Can Vidalet (L5)-HOS080 | HOS080 | S22 | NO_RESOURCE |
| Casa dels Cargols-HOS029 | HOS029 | S22 | NO_RESOURCE |
| Casal gent gran Pubilla Casas-HOS025 | HOS025 | S22 | NO_RESOURCE |
| Cement. Mun. L'Hospitalet - HOS012 | HOS012 | S22 | NO_RESOURCE |
| Cementerio Municipal L'Hospitalet-HOS012 | HOS012 | S22 | NO_RESOURCE |
| Centre Cultural Metropolità Tecla Sala-HOS022 | HOS022 | S22 | NO_RESOURCE |
| Centre Cultural Santa Eulàlia-HOS021 | HOS021 | S22 | NO_RESOURCE |
| Centre Municipal la Florida - Ana Díaz Rico-HOS023 | HOS023 | S22 | NO_RESOURCE |
| Centre Telecom. i Tecnologies de la Informació (CTTI)-HOS165 | HOS165 | S22 | NO_RESOURCE |
| Centre assistencial Prytanis Hospitalet-HOS137 | HOS137 | S22 | NO_RESOURCE |
| Centre assistencial Prytanis Plaça Europa-HOS129 | HOS129 | S22 | NO_RESOURCE |
| Centre comercial Gran Via 2-HOS093 | HOS093 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Alhambra-HOS101 | HOS101 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Amadeu Torner (dte. III)-HOS014 | HOS014 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Bellvitge (dte. VI)-HOS015 | HOS015 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Collblanc (dte. II)-HOS016 | HOS016 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Florida (dte. IV)-HOS019 | HOS019 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Gornal (dte. VI)-HOS017 | HOS017 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Just Oliveras (dte. I)-HOS018 | HOS018 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Pura Fernández-HOS100 | HOS100 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Rb.Marina (dte. VI)-HOS013 | HOS013 | S22 | NO_RESOURCE |
| Centre d'Atenció Primària Ronda de la Torrassa (dte. II)-HOS020 | HOS020 | S22 | NO_RESOURCE |
| Centre de Rehabilitació Rambla Marina i Servei de Proves - Institut Català de la Salut (dte. VI)-HOS013 | — | S22 | NO_RESOURCE |
| Ciudad de la Justicia (Juzgado 1ª Instancia Nº 2)-HOS116 | HOS116 | S22 | NO_RESOURCE |
| Collblanc (L5)-HOS075 | HOS075 | S22 | NO_RESOURCE |
| Complex Esportiu Municipal L'Hospitalet Nord-HOS109 | HOS109 | S22 | NO_RESOURCE |
| DIPRO-MTI | — | S22 | NO_RESOURCE |
| Deixalleria Municipal-HOS132 | HOS132 | S22 | NO_RESOURCE |
| Dipòsit Parc de la serp - HOS037 | HOS037 | S22 | NO_RESOURCE |
| Dipòsit de vehicles (parc de la serp)-HOS037 | HOS037 | S22 | NO_RESOURCE |
| Dipòsit de vehicles (santa eulàlia)-HOS036 | HOS036 | S22 | NO_RESOURCE |
| ETRA BONAL - Cornellà-HOS166 | HOS166 | S22 | NO_RESOURCE |
| Edificio Cobalt (archivo municipal)-HOS005 | HOS005 | S22 | NO_RESOURCE |
| Edificio Cobalt-HOS005 | HOS005 | S22 | NO_RESOURCE |
| Edificio PUIG - HOS128 | — | S22 | NO_RESOURCE |
| Edificio PUIG-HOS128 | HOS128 | S22 | NO_RESOURCE |
| Edificio de viviendas C. Prat-HOS162 | HOS162 | S22 | NO_RESOURCE |
| Edificio de viviendas Plaza Guernica-HOS164 | HOS164 | S22 | NO_RESOURCE |
| Ermita de Santa Eulàlia - HOS133 | HOS133 | S22 | NO_RESOURCE |
| Ermita de Santa Eulàlia-HOS133 | HOS133 | S22 | NO_RESOURCE |
| Esc. Ausias March - HOS039 | HOS039 | S22 | NO_RESOURCE |
| Esc. Bernat Metge - HOS040 | — | S22 | NO_RESOURCE |
| Esc. Br. Garabatos-HOS097 | HOS097 | S22 | NO_RESOURCE |
| Esc. Br. Nova Fortuny - HOS096 | — | S22 | NO_RESOURCE |
| Esc. Br. Patufet - HOS099 | HOS099 | S22 | NO_RESOURCE |
| Esc. Busquets i Punset - HOS038 | HOS038 | S22 | NO_RESOURCE |
| Esc. Gornal - HOS044 | — | S22 | NO_RESOURCE |
| Esc. Joaquim Ruyra - HOS046 | HOS046 | S22 | NO_RESOURCE |
| Esc. Josep Janes - HOS047 | — | S22 | NO_RESOURCE |
| Esc. La Marina - HOS049 | HOS049 | S22 | NO_RESOURCE |
| Esc. M. d'E. de Bellvitge - HOS051 | HOS051 | S22 | NO_RESOURCE |
| Esc. Màrius Torres - HOS052 | HOS052 | S22 | NO_RESOURCE |
| Esc. Patufet Sant Jordi - HOS056 | HOS056 | S22 | NO_RESOURCE |
| Esc. Pau Sans - HOS058 | HOS058 | S22 | NO_RESOURCE |
| Esc. Pau Vila - HOS059 | HOS059 | S22 | NO_RESOURCE |
| Esc. Prat de la Manta - HOS063 | HOS063 | S22 | NO_RESOURCE |
| Esc. Puig i Gairalt - HOS064 | HOS064 | S22 | NO_RESOURCE |
| Esc. Ramon Muntaner - HOS066 | — | S22 | NO_RESOURCE |
| Esc. Rest. El Repartidor - HOS139 | HOS139 | S22 | NO_RESOURCE |
| Esc. Sant Josep - El Pi - HOS067 | HOS067 | S22 | NO_RESOURCE |
| Escola Ausias March-HOS039 | HOS039 | S22 | NO_RESOURCE |
| Escola Bernat Metge-HOS040 | HOS040 | S22 | NO_RESOURCE |
| Escola Bressol Garabatos-HOS097 | HOS097 | S22 | NO_RESOURCE |
| Escola Bressol Municipal La Casa del Molí-HOS098 | HOS098 | S22 | NO_RESOURCE |
| Escola Bressol Nova Fortuny-HOS096 | HOS096 | S22 | NO_RESOURCE |
| Escola Bressol Patufet-HOS099 | HOS099 | S22 | NO_RESOURCE |
| Escola Busquets i Punset-HOS038 | HOS038 | S22 | NO_RESOURCE |
| Escola Charlie Rivel-HOS041 | HOS041 | S22 | NO_RESOURCE |
| Escola Frederic Mistral-HOS043 | HOS043 | S22 | NO_RESOURCE |
| Escola Gornal-HOS044 | HOS044 | S22 | NO_RESOURCE |
| Escola Joan Maragall-HOS045 | HOS045 | S22 | NO_RESOURCE |
| Escola Joaquim Ruyra-HOS046 | HOS046 | S22 | NO_RESOURCE |
| Escola Josep Janes-HOS047 | HOS047 | S22 | NO_RESOURCE |
| Escola Josep Maria Folch i Torres-HOS042 | HOS042 | S22 | NO_RESOURCE |
| Escola La Carpa-HOS048 | HOS048 | S22 | NO_RESOURCE |
| Escola La Marina-HOS049 | HOS049 | S22 | NO_RESOURCE |
| Escola Lola Anglada-HOS050 | HOS050 | S22 | NO_RESOURCE |
| Escola Mare de Déu de Bellvitge-HOS051 | HOS051 | S22 | NO_RESOURCE |
| Escola Menéndez Pidal-HOS053 | HOS053 | S22 | NO_RESOURCE |
| Escola Milagros Consarnau-HOS054 | HOS054 | S22 | NO_RESOURCE |
| Escola Màrius Torres-HOS052 | HOS052 | S22 | NO_RESOURCE |
| Escola Pablo Neruda-HOS055 | HOS055 | S22 | NO_RESOURCE |
| Escola Patufet Sant Jordi-HOS056 | HOS056 | S22 | NO_RESOURCE |
| Escola Pau Casals-HOS057 | HOS057 | S22 | NO_RESOURCE |
| Escola Pau Sans-HOS058 | HOS058 | S22 | NO_RESOURCE |
| Escola Pau Vila-HOS059 | HOS059 | S22 | NO_RESOURCE |
| Escola Pep Ventura-HOS060 | HOS060 | S22 | NO_RESOURCE |
| Escola Pere Lliscart-HOS061 | HOS061 | S22 | NO_RESOURCE |
| Escola Pompeu Fabra-HOS062 | HOS062 | S22 | NO_RESOURCE |
| Escola Prat de la Manta-HOS063 | HOS063 | S22 | NO_RESOURCE |
| Escola Prat de la Manta-HOS063 | HOS063 | S22 | NO_RESOURCE |
| Escola Puig i Gairalt-HOS064 | HOS064 | S22 | NO_RESOURCE |
| Escola Ramon Muntaner-HOS066 | HOS066 | S22 | NO_RESOURCE |
| Escola Sant Josep - El Pi-HOS067 | HOS067 | S22 | NO_RESOURCE |
| Escola Santiago Ramón y Cajal-HOS065 | HOS065 | S22 | NO_RESOURCE |
| Escola de Música - Centre de les Arts-HOS071 | HOS071 | S22 | NO_RESOURCE |
| Escola restaurant El Repartidor / Tragaluz - El Llindar-HOS139 | HOS139 | S22 | NO_RESOURCE |
| Estadi Municipal Futbol L'Hospitalet-HOS108 | HOS108 | S22 | NO_RESOURCE |
| Europa Fira-HOS091 | HOS091 | S22 | NO_RESOURCE |
| Fira (L9)-HOS074 | HOS074 | S22 | NO_RESOURCE |
| Fira Barcelona Gran Via-HOS131 | HOS131 | S22 | NO_RESOURCE |
| Florida (L1)-HOS077 | HOS077 | S22 | NO_RESOURCE |
| Gornal-HOS092 | HOS092 | S22 | NO_RESOURCE |
| Hospital Duran i Reynals - Institut Catala Oncologia-HOS031 | HOS031 | S22 | NO_RESOURCE |
| Hospital General de L'Hospitalet-HOS032 | HOS032 | S22 | NO_RESOURCE |
| Hospital Universitari Bellvitge-HOS160 | HOS160 | S22 | NO_RESOURCE |
| Hospital de Bellvitge (L1)-HOS084 | HOS084 | S22 | NO_RESOURCE |
| Hotel Hesperia Tower-HOS102 | HOS102 | S22 | NO_RESOURCE |
| IFP (Innovación en Formación Profesional)-HOS140 | HOS140 | S22 | NO_RESOURCE |
| Iglesia de la Florida-HOS134 | HOS134 | S22 | NO_RESOURCE |
| Ikea-HOS095 | HOS095 | S22 | NO_RESOURCE |
| Ildefons Cerdà-HOS090 | HOS090 | S22 | NO_RESOURCE |
| Institut Apel·les Mestres-HOS142 | HOS142 | S22 | NO_RESOURCE |
| Institut Bellvitge-HOS143 | — | S22 | NO_RESOURCE |
| Institut Bellvitge-HOS143 | HOS143 | S22 | NO_RESOURCE |
| Institut Bisbe Berenguer-HOS144 | HOS144 | S22 | NO_RESOURCE |
| Institut Can Vilumara-HOS153 | HOS153 | S22 | NO_RESOURCE |
| Institut Can Vilumara-HOS153 | HOS153 | S22 | NO_RESOURCE |
| Institut Eduard Fontserè-HOS145 | HOS145 | S22 | NO_RESOURCE |
| Institut Eugeni d'Ors-HOS141 | HOS141 | S22 | NO_RESOURCE |
| Institut Europa - HOS146 | — | S22 | NO_RESOURCE |
| Institut Europa-HOS146 | HOS146 | S22 | NO_RESOURCE |
| Institut Jaume Botey - HOS154 | — | S22 | NO_RESOURCE |
| Institut Llobregat (2)-HOS154 | HOS154 | S22 | NO_RESOURCE |
| Institut Llobregat-HOS155 | HOS155 | S22 | NO_RESOURCE |
| Institut Margarida Xirgu-HOS148 | HOS148 | S22 | NO_RESOURCE |
| Institut Mercè Rodoreda - HOS147 | HOS147 | S22 | NO_RESOURCE |
| Institut Mercè Rodoreda-HOS147 | HOS147 | S22 | NO_RESOURCE |
| Institut Pedraforca-HOS149 | HOS149 | S22 | NO_RESOURCE |
| Institut Provençana-HOS156 | HOS156 | S22 | NO_RESOURCE |
| Institut Rubio i Ors-HOS150 | HOS150 | S22 | NO_RESOURCE |
| Institut Santa Eulàlia-HOS151 | HOS151 | S22 | NO_RESOURCE |
| Institut Torras i Bages - HOS152 | HOS152 | S22 | NO_RESOURCE |
| Institut Torras i Bages-HOS152 | HOS152 | S22 | NO_RESOURCE |
| Jaueme Botey-HOS154 | HOS154 | S22 | NO_RESOURCE |
| L'Hospitalet de Llogregat-HOS072 | HOS072 | S22 | NO_RESOURCE |
| LH_MAIN | — | S22 | NO_RESOURCE |
| Mercat Bellvitge-HOS118 | HOS118 | S22 | NO_RESOURCE |
| Mercat Merca-2 Bellvitge - HOS117 | HOS117 | S22 | NO_RESOURCE |
| Mercat Merca-2 Bellvitge-HOS117 | HOS117 | S22 | NO_RESOURCE |
| Mercat Merca-2 Can Serra-HOS119 | HOS119 | S22 | NO_RESOURCE |
| Mercat de Collblanc-HOS120 | HOS120 | S22 | NO_RESOURCE |
| Mercat de La Florida-HOS121 | HOS121 | S22 | NO_RESOURCE |
| Mercat de Santa Eulàlia-HOS122 | HOS122 | S22 | NO_RESOURCE |
| Mercat del Centre-HOS123 | HOS123 | S22 | NO_RESOURCE |
| Mercat del Torrent Gornal-HOS124 | HOS124 | S22 | NO_RESOURCE |
| Mezquita de Santa Eulàlia-HOS135 | HOS135 | S22 | NO_RESOURCE |
| Museu Can Riera - HOS127 | HOS127 | S22 | NO_RESOURCE |
| Museu Casa Espanya - HOS125 | HOS125 | S22 | NO_RESOURCE |
| Museu L'Harmonia - HOS126 | HOS126 | S22 | NO_RESOURCE |
| Museu de L'Hospitalet - Can Riera-HOS127 | HOS127 | S22 | NO_RESOURCE |
| Museu de L'Hospitalet - Casa Espanya-HOS125 | HOS125 | S22 | NO_RESOURCE |
| Museu de L'Hospitalet - L'Harmonia-HOS126 | HOS126 | S22 | NO_RESOURCE |
| P. M. Centre - HOS115 | HOS115 | S22 | NO_RESOURCE |
| P. M. Fum d'Estampa - HOS110 | HOS110 | S22 | NO_RESOURCE |
| P. M. Gornal - HOS130 | HOS130 | S22 | NO_RESOURCE |
| Palauet Can Buxeres - HOS068 | HOS068 | S22 | NO_RESOURCE |
| Palauet Can Buxeres-HOS068 | HOS068 | S22 | NO_RESOURCE |
| Pavelló Municipal d'Esports-HOS106 | HOS106 | S22 | NO_RESOURCE |
| Piscines Municipals L'Hospitalet-HOS107 | HOS107 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Bellvitge Sergio Manzano-HOS113 | HOS113 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Centre-HOS115 | HOS115 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Fum d'Estampa-HOS110 | HOS110 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Gornal-HOS130 | HOS130 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Les Planes-HOS111 | HOS111 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Sanfeliu-HOS114 | HOS114 | S22 | NO_RESOURCE |
| Poliesportiu Municipal Santa Eulàlia-HOS112 | HOS112 | S22 | NO_RESOURCE |
| Provençana (L10)-HOS094 | HOS094 | S22 | NO_RESOURCE |
| Pubilla Cases (L5)-HOS085 | HOS085 | S22 | NO_RESOURCE |
| Radio-TV de L'Hospitalet-HOS088 | HOS088 | S22 | NO_RESOURCE |
| Rambla Just Oliveras (L1)-HOS086 | HOS086 | S22 | NO_RESOURCE |
| Regidoria Districte I - HOS033 | HOS033 | S22 | NO_RESOURCE |
| Regidoria Districte I-HOS033 | HOS033 | S22 | NO_RESOURCE |
| Regidoria Districte II-HOS034 | HOS034 | S22 | NO_RESOURCE |
| Regidoria Districte III-HOS035 | HOS035 | S22 | NO_RESOURCE |
| Residencia Els Alps - HOS136 | HOS136 | S22 | NO_RESOURCE |
| Residencia Els Alps-HOS136 | HOS136 | S22 | NO_RESOURCE |
| Residència Collblanc Companys Socials-HOS138 | HOS138 | S22 | NO_RESOURCE |
| S4E-HOS142 | HOS142 | S22 | NO_RESOURCE |
| Sant Josep-HOS089 | HOS089 | S22 | NO_RESOURCE |
| Santa Eulàlia (L1)-HOS078 | HOS078 | S22 | NO_RESOURCE |
| Tanatori - Crematori L'Hospitalet Gran Via-HOS158 | HOS158 | S22 | NO_RESOURCE |
| Tanatori L'Hospitalet Ronda-HOS157 | HOS157 | S22 | NO_RESOURCE |
| Teatre Joventut-HOS159 | HOS159 | S22 | NO_RESOURCE |
| Torrassa (L1)-HOS076 | HOS076 | S22 | NO_RESOURCE |
| Torre Barrina - HOS024 | HOS024 | S22 | NO_RESOURCE |
| Torre Barrina-HOS024 | HOS024 | S22 | NO_RESOURCE |
| Unifamiliar C. Ebre-HOS163 | HOS163 | S22 | NO_RESOURCE |
| Universitat de Barcelona-HOS161 | HOS161 | S22 | NO_RESOURCE |
| P. M. Gornal - Plaza 1 - HOS130 | HOS130 | S23 | NO_RESOURCE |
| P. M. Gornal - Plaza 2 - HOS130 | HOS130 | S23 | NO_RESOURCE |
| HOS050-S24-01 | HOS050 | S24 | NO_RESOURCE |
| HOS147-S24-01 | HOS147 | S24 | NO_RESOURCE |
| HOS147-S24-02 | HOS147 | S24 | NO_RESOURCE |
| HOS149-S24-01 | HOS149 | S24 | NO_RESOURCE |
| HOS149-S24-02 | HOS149 | S24 | NO_RESOURCE |
| HOS001-IPEX04-ID0200J23007500258 | HOS001 | SIP | NO_RESOURCE |
| HOS001-IPEX04-ID0200J23007500260 | HOS001 | SIP | NO_RESOURCE |
| HOS001-IPEX04-ID0200J23007500322 | HOS001 | SIP | NO_RESOURCE |
| HOS001-IPEX04-ID0200J23007500325 | HOS001 | SIP | NO_RESOURCE |
| HOS003-IPEX04-ID0200J23007500140 | HOS003 | SIP | NO_RESOURCE |
| HOS004-IPEX04-ID0200J23007500315 | HOS004 | SIP | NO_RESOURCE |
| HOS004-IPEX04-ID0200J23007500319 | HOS004 | SIP | NO_RESOURCE |
| HOS005-IPEX04-ID0200J23007500373 | HOS005 | SIP | NO_RESOURCE |
| HOS006-IPEX04-ID0200J23007500330 | HOS006 | SIP | NO_RESOURCE |
| HOS008-IPEX04-ID0200J23007500310 | HOS008 | SIP | NO_RESOURCE |
| HOS010-IPEX04-ID0200J23007500334 | HOS010 | SIP | NO_RESOURCE |
| HOS013-IPEX04-ID0200J23007500335 | HOS013 | SIP | NO_RESOURCE |
| HOS022-IPEX04-ID0200J23007500252 | HOS022 | SIP | NO_RESOURCE |
| HOS023-IPEX04-ID0200J23007500333 | HOS023 | SIP | NO_RESOURCE |
| HOS024-IPEX04-ID0200J23007500348 | HOS024 | SIP | NO_RESOURCE |
| HOS025-IPEX-04-ID0200J23007500264 | HOS025 | SIP | NO_RESOURCE |
| HOS026-IPEX04-ID0200J23007500253 | HOS026 | SIP | NO_RESOURCE |
| HOS026-IPEX04-ID0200J23007500254 | HOS026 | SIP | NO_RESOURCE |
| HOS027-IPEX04-ID0200J23007500313 | HOS027 | SIP | NO_RESOURCE |
| HOS028-IPEX04-ID0200J23007500266 | HOS028 | SIP | NO_RESOURCE |
| HOS028-IPEX04-ID0200J23007500269 | HOS028 | SIP | NO_RESOURCE |
| HOS029-IPEX04-ID0200J23007500259 | HOS029 | SIP | NO_RESOURCE |
| HOS029-IPEX04-ID0200J23007500265 | HOS029 | SIP | NO_RESOURCE |
| HOS030-IPEX04-ID0200J23007500255 | HOS030 | SIP | NO_RESOURCE |
| HOS030-IPEX04-ID0200J23007500262 | HOS030 | SIP | NO_RESOURCE |
| HOS033-IPEX04-01-ID0200J23007500345 | HOS033 | SIP | NO_RESOURCE |
| HOS033-IPEX04-02-ID0200J23007500344 | HOS033 | SIP | NO_RESOURCE |
| HOS034-IPEX04-ID0200J23007500312 | HOS034 | SIP | NO_RESOURCE |
| HOS034-IPEX04-ID0200J23007500336 | HOS034 | SIP | NO_RESOURCE |
| HOS035-IPEX04-ID0200J23007500314 | HOS035 | SIP | NO_RESOURCE |
| HOS035-IPEX04-ID0200J23007500328 | HOS035 | SIP | NO_RESOURCE |
| HOS036-IPEX04-ID0200J23007500268 | HOS036 | SIP | NO_RESOURCE |
| HOS037-IPEX-04-ID0200J23007500271 | HOS037 | SIP | NO_RESOURCE |
| HOS038-IPEX04-ID0200J23007500408 | HOS038 | SIP | NO_RESOURCE |
| HOS039-IPEX04-ID0200J23007500321 | HOS039 | SIP | NO_RESOURCE |
| HOS040-IPEX04-ID0200J23007500341 | HOS040 | SIP | NO_RESOURCE |
| HOS041-IPEX04-ID0200J23007500283 | HOS041 | SIP | NO_RESOURCE |
| HOS042-IPEX04-ID0200J23007500231 | HOS042 | SIP | NO_RESOURCE |
| HOS043-IPEX04-ID0200J23007500261 | HOS043 | SIP | NO_RESOURCE |
| HOS044-PEX04-ID0200J23007500340 | HOS044 | SIP | NO_RESOURCE |
| HOS045-IPEX04-ID0200J23007500238 | HOS045 | SIP | NO_RESOURCE |
| HOS046-IPEX04-ID0200J23007500278 | HOS046 | SIP | NO_RESOURCE |
| HOS047-IPEX04-ID0200J23007500362 | HOS047 | SIP | NO_RESOURCE |
| HOS048-IPEX04-ID0200J23007500273 | HOS048 | SIP | NO_RESOURCE |
| HOS049-IPEX04-ID0200J23007500339 | HOS049 | SIP | NO_RESOURCE |
| HOS050-IPEX04-ID0200J23007500274 | HOS050 | SIP | NO_RESOURCE |
| HOS051-IPEX04-ID0200J23007500376 | HOS051 | SIP | NO_RESOURCE |
| HOS052-IPEX04-ID0200J23007500272 | HOS052 | SIP | NO_RESOURCE |
| HOS053-IPEX04-ID0200J23007500364 | HOS053 | SIP | NO_RESOURCE |
| HOS054-IPEX04-ID0200J23007500282 | HOS054 | SIP | NO_RESOURCE |
| HOS055-IPEX04-ID0200J23007500338 | HOS055 | SIP | NO_RESOURCE |
| HOS056-IPEX04-ID0200J23007500243 | HOS056 | SIP | NO_RESOURCE |
| HOS057-IPEX04-ID0200J23007500332 | HOS057 | SIP | NO_RESOURCE |
| HOS057-IPEX04-ID0200J23007500393 | HOS057 | SIP | NO_RESOURCE |
| HOS058-IPEX04-ID0200J23007500249 | HOS058 | SIP | NO_RESOURCE |
| HOS059-IPEX04-ID0200J23007500279 | HOS059 | SIP | NO_RESOURCE |
| HOS060-IPEX04-ID0200J23007500275 | HOS060 | SIP | NO_RESOURCE |
| HOS061-IPEX04-ID0200J23007500281 | HOS061 | SIP | NO_RESOURCE |
| HOS062-IPEX04-ID0200J23007500233 | HOS062 | SIP | NO_RESOURCE |
| HOS063-IPEX04-ID0200J23007500350 | HOS063 | SIP | NO_RESOURCE |
| HOS064-IPEX04-ID0200J23007500236 | HOS064 | SIP | NO_RESOURCE |
| HOS064-IPEX04-ID0200J23007500247 | HOS064 | SIP | NO_RESOURCE |
| HOS065-IPEX04-ID0200J23007500245 | HOS065 | SIP | NO_RESOURCE |
| HOS065-IPEX04-ID0200J23007500358 | HOS065 | SIP | NO_RESOURCE |
| HOS066-IPEX04-ID0200J23007500199 | HOS066 | SIP | NO_RESOURCE |
| HOS067-IPEX04-ID0200J23007500280 | HOS067 | SIP | NO_RESOURCE |
| HOS069-IPEX04-ID0200J23007500257 | HOS069 | SIP | NO_RESOURCE |
| HOS069-IPEX04-ID0200J23007500263 | HOS069 | SIP | NO_RESOURCE |
| HOS096-IPEX04-ID0200J23007500284 | HOS096 | SIP | NO_RESOURCE |
| HOS098-IPEX04-ID0200J23007500421 | HOS098 | SIP | NO_RESOURCE |
| HOS099-IPEX04-ID0200J23007500388 | HOS099 | SIP | NO_RESOURCE |
| HOS109-IPEX04-ID0200J23007500317 | HOS109 | SIP | NO_RESOURCE |
| HOS125-IPEX04-ID0200J23007500337 | HOS125 | SIP | NO_RESOURCE |
| HOS126-IPEX04-ID0200J23007500277 | HOS126 | SIP | NO_RESOURCE |
| HOS88-IPEX04-ID0200J23007500270 | HOS088 | SIP | NO_RESOURCE |
| ID0200J23007500141 | — | SIP | NO_RESOURCE |
| ID0200J23007500191 | — | SIP | NO_RESOURCE |
| ID0200J23007500196 | — | SIP | NO_RESOURCE |
| ID0200J23007500316 | — | SIP | NO_RESOURCE |
| ID0200J23007500342 | — | SIP | NO_RESOURCE |
| ID0200J23007500343 | — | SIP | NO_RESOURCE |
| ID0200J23007500383 | — | SIP | NO_RESOURCE |
| ID0200J23007500398 | — | SIP | NO_RESOURCE |
| ID0200J23007500399 | — | SIP | NO_RESOURCE |
| ID0200J23007500409 | — | SIP | NO_RESOURCE |
| ID0200J23007500415 | — | SIP | NO_RESOURCE |
| ID0200J23007500415 | — | SIP | NO_RESOURCE |
| IPEX1 | — | SIP | NO_RESOURCE |

## Recurso existe pero sin muestras (47)

| id | HOS | Sistema | Recursos existentes |
|---|---|---|---|
| I22LA020277R | — | S06 | flow, volume, liters, m3, water |
| Can Boixeres (L5)-HOS081 | HOS081 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Can Serra (L1)-HOS079 | HOS079 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Can Tries Gornal (L9)-HOS087 | HOS087 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Can Vidalet (L5)-HOS080 | HOS080 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Centre Telecom. i Tecnologies de la Informació (CTTI)-HOS165 | HOS165 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Centre comercial Gran Via 2-HOS093 | HOS093 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Centre d'Atenció Primària Florida (dte. IV)-HOS019 | HOS019 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Centre d'Atenció Primària Gornal (dte. VI)-HOS017 | HOS017 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Collblanc (L5)-HOS075 | HOS075 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Escola de Música - Centre de les Arts-HOS071 | HOS071 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Europa Fira-HOS091 | HOS091 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Fira (L9)-HOS074 | HOS074 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Florida (L1)-HOS077 | HOS077 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Gornal-HOS092 | HOS092 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS006 Cal Gotlla | HOS006 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS010 Bibl. i esc. pl. Europa | HOS010 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS014 CGG de la Torrassa | HOS014 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS015 CGG Santa Eulalia | HOS015 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS023 C. M. Ana Díaz Rico | HOS023 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS024 Torre Barrina | HOS024 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS027 A. B. B. S. - Dte. VI | HOS027 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS044 Esc. Gornal | HOS044 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS046 Esc. Joaquim Ruyra | HOS046 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS047 Esc. Josep Janes | HOS047 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS052 Esc. Màrius Torres | HOS052 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS059 Esc. Pau Vila | HOS059 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS063 Esc. Prat de la Manta | HOS063 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS064 Esc. Puig i Gairalt | HOS064 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS066 Esc. Ramon Muntaner | HOS066 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS096 Esc. Br. Nova Fortuny | HOS096 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS105 Calzedonia | HOS105 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS110 P. M. Fum d'Estampa | HOS110 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS117 Mercat Merca-2 Bellvitge | HOS117 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS128 Edificio PUIG | HOS128 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS130 P. M. Gornal | HOS130 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS143 Institut Bellvitge | HOS143 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| HOS154 Institut Jaume Botey | HOS154 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Hospital Duran i Reynals - Institut Catala Oncologia-HOS031 | HOS031 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Hospital General de L'Hospitalet-HOS032 | HOSPITAL | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Hospital de Bellvitge (L1)-HOS084 | HOSPITAL | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Ikea-HOS095 | HOS095 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Provençana (L10)-HOS094 | HOS094 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Pubilla Cases (L5)-HOS085 | HOS085 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Residència Collblanc Companys Socials-HOS138 | HOS138 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| Torrassa (L1)-HOS076 | HOS076 | S22 | next_time_ferrocarril, destination_ferrocarril, code_line_ferrocarril, name_ferrocarril |
| ID0200J23007500383 | — | SIP | connected, keepalive |