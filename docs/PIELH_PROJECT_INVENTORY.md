# PIELH QA — Inventari de Fitxers

## Fitxers principals (producció)

| Fitxer | Funció | En ús | Dependències |
|---|---|---|---|
| `index.html` | Interfície principal del dashboard QA | SI | `app.js`, `styles.css`, Leaflet CDN |
| `app.js` | Lògica principal de la UI: mapa, taules, filtres, editor, API calls | SI | `pielh_qa_master.json`, `server.py` (API) |
| `server.py` | Servidor HTTP Python: fitxers estàtics + API REST | SI | `config.json`, `pielh_qa_master.json` |
| `styles.css` | Estils CSS del dashboard principal | SI | — |
| `config.json` | Configuració del servidor (ports, paths, tokens) | SI | — |
| `pielh_qa_master.json` | Font de veritat única: edificis, sensors, catàlegs, QA | SI | — |

## Fitxers de l'explorador QA (eina secundària)

| Fitxer | Funció | En ús | Dependències |
|---|---|---|---|
| `qa_explorer.html` | Explorador alternatiu (Tabulator + mapa) | SI (eina separada) | `modules/*.js`, Leaflet CDN, Tabulator CDN |
| `qa_explorer_app.js` | Inicialització i cableig de mòduls de l'explorador | SI | `modules/*.js` |
| `qa_explorer_styles.css` | Estils CSS de l'explorador QA | SI | — |

## Mòduls JS (usats només per qa_explorer)

| Fitxer | Funció | En ús | Dependències |
|---|---|---|---|
| `modules/data.js` | Càrrega i indexació de `pielh_qa_master.json` | SI (qa_explorer) | — |
| `modules/filters.js` | Estat i lògica de filtrat | SI (qa_explorer) | — |
| `modules/map.js` | Capa Leaflet de l'explorador | SI (qa_explorer) | `data.js`, Leaflet |
| `modules/table.js` | Instància Tabulator | SI (qa_explorer) | Tabulator, `data.js` |
| `modules/details.js` | Panell de fitxa inferior | SI (qa_explorer) | `data.js` |

**Nota:** Els fitxers de `modules/` NO els utilitza `index.html`/`app.js`. El dashboard principal té tota la lògica inlinada a `app.js`.

## Fitxers legacy

| Fitxer | Funció | En ús |
|---|---|---|
| `pielh_qa_master_legacy.json` | Còpia antiga de les dades | NO — arxiu históric |

## Fitxers temporals / auxiliars

| Fitxer | Funció | En ús |
|---|---|---|
| `data/backups/pielh_qa_master_YYYYMMDD_HHMMSS.json` | Còpies de seguretat automàtiques (màx. 20) | Generats per `server.py` |
| `logs/pielh.log` | Registre de canvis de camps | Generat per `server.py` |
| `deploy_ftp/` | Còpia de desplegament (generada per `build_deploy_ftp.py`) | Temporal |

## Scripts de suport

> **Inventari complet de scripts:** Vegeu [PIELH_SCRIPTS.md](PIELH_SCRIPTS.md) per a la llista detallada de tots els scripts (25+), amb mode lectura/escriptura, entrades, sortides, backup i estat.

| Fitxer | Funció | En ús |
|---|---|---|
| `build_deploy_ftp.py` | Genera la carpeta `deploy_ftp/` llesta per pujar per FTP | Manual |
| `start_pielh.sh` | Script bash per arrencar el servidor en Linux | Producció |
| `Ejecutar_PIELH_Localhost.bat` | Script Windows per arrencar en local | Local |
| `scripts/build_hospitalet_boundary.py` | Genera GeoJSON del contorn de la ciutat | Manual / utilitat |
| `scripts/dedupe_sensor_siblings.py` | Utilitat per deduplicar sensors amb el mateix ID | Manual |
| `scripts/download_hospitalet_geojson.py` | Descarrega les dades GeoJSON d'OpenStreetMap | Manual |
| `scripts/audit_sensors_without_hos.py` | Audita sensors sense HOS assignat (READ-ONLY) | Manual |
| `scripts/apply_hos_assignments.py` | Aplica assignacions HOS als sensors (MODIFICA MASTER) | Manual |
| `scripts/audit_sensor_building_inheritance.py` | Audita herència edifici→sensor (READ-ONLY) | Manual |
| `scripts/apply_sensor_building_inheritance.py` | Propaga camps edifici→sensor (MODIFICA MASTER amb --apply) | Manual |
| `scripts/audit_duplicate_sensors.py` | Detecta sensors duplicats (READ-ONLY) | Manual |
| `scripts/plan_duplicate_sensor_cleanup.py` | Genera pla de neteja de duplicats (READ-ONLY) | Manual |
| `scripts/apply_high_confidence_legacy_marks.py` | Aplica marques LEGACY HIGH (MODIFICA MASTER amb --apply) | Manual |
| `scripts/fetch_thethings_structure.py` | Descarrega estructura TheThings a snapshot | Manual |
| `scripts/fetch_thethings_tags.py` | Extreu tags del snapshot TheThings | Manual |
| `scripts/audit_thethings_activity.py` | Audita activitat IoT des de TheThings | Manual |
| `scripts/apply_inventory_health_to_master.py` | Enriqueix master amb iot_health (MODIFICA MASTER) | Manual |

## Fitxers de dades GeoJSON

| Fitxer | Contingut | Obligatori |
|---|---|---|
| `data/geojson/hospitalet_barris.geojson` | Polígons dels barris | Recomanat (fallback a punts) |
| `data/geojson/hospitalet_boundary.geojson` | Contorn de la ciutat | Opcional |
| `data/geojson/hospitalet_districtes.geojson` | Polígons dels districtes | Recomanat (fallback a punts) |
| `data/geojson/hospitalet_streets.geojson` | Carrers (no carregat al dashboard) | Referència |

## Documentació inclosa al projecte

| Fitxer | Contingut |
|---|---|
| `README_DEPLOY.md` | Instruccions de desplegament en servidor Linux + Nginx |
| `documentation/thethingsAPI_example_mail.txt` | Exemple d'ús de l'API thethings |
| `documentation/thethingsDocumentation.txt` | Documentació de la plataforma IoT |

## Dependències externes

### CDN (Frontend)
| Biblioteca | Versió | URL | Ús |
|---|---|---|---|
| Leaflet | 1.9.4 | `unpkg.com/leaflet@1.9.4` | Mapa interactiu (ambdós apps) |
| Tabulator | 6.2.1 | `unpkg.com/tabulator-tables@6.2.1` | Taula avançada (qa_explorer únicament) |

### Python stdlib (Backend)
`http.server`, `json`, `shutil`, `logging`, `ssl`, `threading`, `time`, `urllib`, `webbrowser`, `datetime`, `pathlib`, `copy`, `re`

Cap dependència externa de Python (sense pip install).

## APIs externes

| API | URL | Autenticació | Ús |
|---|---|---|---|
| thethings IoT platform | `https://api.smartpielh.l-h.cat` | Bearer token (`thethings_token` a `config.json`) | Importació de buildings i sensors des de la plataforma |

### Models API thethings usats
21 models registrats a `server.py` (`MODELS`):
- Model 34738: ASSETS (buildings)
- Models 33814–36331: Sistemes S01 a SIP (sensors)
