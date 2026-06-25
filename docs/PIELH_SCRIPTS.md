# PIELH QA — Inventari Complet de Scripts

Data de creació: 2026-06-22

Document canònic sobre tots els scripts del projecte: funció, mode lectura/escriptura, entrades, sortides i estat.

**Convencions:**
- **ACTIU** — En ús regular al flux de manteniment.
- **UTILITAT** — Eina puntual, no part del flux regular.
- **LEGACY** — Obsolet o substituït per una versió millor.
- **PELIGRÓS** — Modifica dades sense dry-run clar o afecta sistemes externs.
- **READ-ONLY** — No modifica mai `pielh_qa_master.json`.
- **MODIFICA MASTER** — Pot modificar `pielh_qa_master.json`. Genera backup previ.

---

## 1. Scripts de servidor i desplegament

| Script | Funció | Mode | Backup | API TheThings | config.json | Estat |
|---|---|---|---|---|---|---|
| `build_deploy_ftp.py` | Genera `deploy_ftp/` amb còpia dels fitxers per pujar per FTP | Escriu a `deploy_ftp/` | No | No | No | ACTIU |
| `deploy_ftp/server.py` | Còpia del servidor per al desplegament FTP | READ-ONLY (còpia) | No | No | Sí | ACTIU |

**Comanda habitual:**
```
python build_deploy_ftp.py
```

---

## 2. Scripts GIS

| Script | Funció | Mode | Sortida | Estat |
|---|---|---|---|---|
| `scripts/download_hospitalet_geojson.py` | Descarrega GeoJSON districtes i barris des d'OpenStreetMap (Overpass) | Escriu a `data/geojson/` | `hospitalet_districtes.geojson`, `hospitalet_barris.geojson` | UTILITAT |
| `scripts/build_hospitalet_boundary.py` | Genera límit municipal unint polígons de districtes | Escriu a `data/geojson/` | `hospitalet_boundary.geojson` | UTILITAT |
| `descarga_mapas_hospitalet_barrios/.../download_hospitalet_geojson.py` | Versió antiga de descàrrega GeoJSON | Escriu a directori propi | — | LEGACY (usar scripts/ en el seu lloc) |
| `descarga_mapas_hospitalet_barrios/.../download_hospitalet_streets.py` | Descarrega GeoJSON de carrers | Escriu a directori propi | — | UTILITAT |

**Comanda habitual:**
```
python scripts/download_hospitalet_geojson.py
python scripts/build_hospitalet_boundary.py
```

---

## 3. Scripts TheThings — Snapshot i Auditoría

### 3.1 Descàrrega de dades TheThings

| Script | Funció | Mode | Usa API | Sortida | Estat |
|---|---|---|---|---|---|
| `scripts/fetch_thethings_structure.py` | **Fase 1** — Descarrega estructura buildings/sensors des de l'API TheThings | READ-ONLY del master | Sí | `data/thethings_snapshots/latest/thethings_structure_only.json` | ACTIU |
| `scripts/fetch_thethings_tags.py` | **Fase 2** — Extreu tags des dels raw descarregats (sense noves crides API) | READ-ONLY del master | No | `data/thethings_snapshots/latest/thethings_tags_only.json` | ACTIU |
| `scripts/discover_thethings_resources.py` | **Fase 3** — Descubriment de recursos IoT (cridat a `GET /resources/{resource}`) | READ-ONLY del master | Sí | `data/thethings_snapshots/latest/thethings_resources_probe.json` | ACTIU |

**Comanda habitual (en ordre):**
```
python scripts/fetch_thethings_structure.py --no-ssl-verify
python scripts/fetch_thethings_tags.py
python scripts/discover_thethings_resources.py --no-ssl-verify
```

### 3.2 Auditoría sobre snapshot

| Script | Funció | Mode | Entrada | Sortida | Estat |
|---|---|---|---|---|---|
| `scripts/audit_thethings_structure.py` | Compara master vs snapshot TheThings (estructura) | READ-ONLY | `thethings_structure_only.json` | Informe Markdown | ACTIU |
| `scripts/audit_thethings_tags.py` | Compara tags del master vs snapshot TheThings | READ-ONLY | `thethings_tags_only.json` | Informe Markdown | ACTIU |
| `scripts/audit_thethings_data_health.py` | Audita salut de dades IoT (freqüència, gaps, recursos) | READ-ONLY | `thethings_resources_probe.json` | Informe CSV/JSON | ACTIU |
| `scripts/audit_thethings_activity.py` | Audita activitat IoT vs master (sensors actius, iot_health) | READ-ONLY | Snapshot + crides API TheThings | CSV + JSON a `data/audits/` | ACTIU |

---

## 4. Scripts Inventari IoT i Health

| Script | Funció | Mode | Entrada | Sortida | Backup | Estat |
|---|---|---|---|---|---|---|
| `scripts/build_inventory_health_report.py` | Genera informe de salut IoT en JSON + Markdown | READ-ONLY | Summary JSON de `audit_thethings_activity` | `data/audits/inventory_health_report.md` + `.json` | No | ACTIU |
| `scripts/apply_inventory_health_to_master.py` | Enriqueix el master amb `iot_health` per sensor | **MODIFICA MASTER** | Master + CSV auditoría + `inventory_health_report.json` | `pielh_qa_master.json` actualitzat | Sí | ACTIU |

**Comanda habitual:**
```
python scripts/build_inventory_health_report.py
python scripts/apply_inventory_health_to_master.py   # fa backup automàtic
```

---

## 5. Scripts Herència Sensor-Edifici i Resolució HOS

> **Aquests scripts gestionen la relació `sensor.hos → building.id` i la propagació de camps.**
> Vegeu la secció "Fluix HOS" al final d'aquest document per l'ordre correcte d'execució.

| Script | Funció | Mode | Dry-run | Entrada | Sortida/Efecte | Backup | Estat |
|---|---|---|---|---|---|---|---|
| `scripts/audit_sensors_without_hos.py` | **Audita** sensors sense HOS. Classifica BUILDING_MATCH, DUPLICATE_OR_SIBLING, STREET_SENSOR, UNKNOWN. Proposa candidats HIGH per a `apply_hos_assignments.py` | READ-ONLY | N/A | `pielh_qa_master.json` | `data/audits/sensors_without_hos_audit.json` + `.md` | No | ACTIU |
| `scripts/apply_hos_assignments.py` | **Aplica** HOS als sensors candidats HIGH. Propaga `district_code`, `district_name`, `neighborhood_key`, `neighborhood`, `type`, `zone`, `street_etra` | **MODIFICA MASTER** | `--dry-run` | `data/audits/sensors_without_hos_audit.json` + master | `pielh_qa_master.json` + informe aplicació | Sí | ACTIU |
| `scripts/audit_sensor_building_inheritance.py` | **Audita** que els sensors hereten correctament camps administratius i coordenades del seu edifici pare | READ-ONLY | N/A | `pielh_qa_master.json` | `reports/sensor_building_inheritance_report.json` + `.md` | No | ACTIU |
| `scripts/apply_sensor_building_inheritance.py` | **Propaga** camps admin+geo (`district_code`, `district_name`, `neighborhood_key`, `neighborhood`, `type`, `zone`, `street_etra`, `street_mti`, `lat`, `lon`) de l'edifici als seus sensors | **MODIFICA MASTER** | `--dry-run` (per defecte) | `pielh_qa_master.json` | `pielh_qa_master.json` actualitzat + informe | Sí | ACTIU |
| `scripts/sync_thethings_tags.py` | **Sincronitza** tags HOS amb TheThings (pull: TheThings→master; push: master→TheThings) | **MODIFICA MASTER** (--pull) / **MODIFICA TheThings** (--push) | `--dry-run` | Master + API TheThings | Master + crides API | Sí (--pull) | ACTIU / **PELIGRÓS amb --push** |

**Scripts canònics per al fluix HOS (veure apartat 8):**
1. `audit_sensors_without_hos.py` → detecta sensors sense HOS i classifica candidats
2. `apply_hos_assignments.py --dry-run` → verifica; `--apply` → aplica
3. `audit_sensor_building_inheritance.py` → verifica herència
4. `apply_sensor_building_inheritance.py --dry-run` → verifica; `--apply` → propaga

---

## 6. Scripts Duplicats i Marques LEGACY

| Script | Funció | Mode | Dry-run | Entrada | Sortida/Efecte | Backup | Estat |
|---|---|---|---|---|---|---|---|
| `scripts/audit_duplicate_sensors.py` | Detecta sensors duplicats per id, thing_id, thing_token, HOS+system_id, geo, similitud de nom. Classifica risc: CRITICAL/HIGH/MEDIUM/LOW | READ-ONLY | N/A | `pielh_qa_master.json` | `reports/audit_duplicate_sensors.json` + CSV | No | ACTIU |
| `scripts/plan_duplicate_sensor_cleanup.py` | Genera pla dry-run de neteja de duplicats (decisions MARK_LEGACY, KEEP, REVIEW) | READ-ONLY | N/A | `reports/audit_duplicate_sensors.json` + `thethings_resources_probe.json` | `reports/duplicate_sensor_cleanup_plan.json` + CSV | No | ACTIU |
| `scripts/apply_high_confidence_legacy_marks.py` | Aplica marques LEGACY als sensors amb `decision=MARK_LEGACY` + `confidence=HIGH` del pla | **MODIFICA MASTER** | `--dry-run` | `reports/duplicate_sensor_cleanup_plan.json` + master | Master actualitzat + informe | Sí | ACTIU |
| `scripts/mark_old_duplicate_sensors.py` | Marca com a OLD sensors inactius CRITICAL detectats a l'auditoría de duplicats | **MODIFICA MASTER** | No té dry-run explícit | `reports/duplicate_sensors_audit.csv` + master | Master actualitzat + informe | Sí | ACTIU |
| `scripts/dedupe_sensor_siblings.py` | Completa camps buits entre sensors que comparteixen el mateix `id` (germanos), usant la mateixa lògica de `server.py` | **MODIFICA MASTER** | No (crea backup primer) | Master via `server.py` | Master actualitzat | Sí (via server.py) | UTILITAT |

---

## 7. Scripts d'Informes i Exportació

| Script | Funció | Mode | Entrada | Sortida | Estat |
|---|---|---|---|---|---|
| `scripts/report_sensors_data_cleanup.py` | Informe de depuració de sensors: creua master + probe IoT | READ-ONLY | Master + `thethings_resources_probe.json` | Markdown/CSV informe | ACTIU |
| `scripts/audit_post_cleanup.py` | Mètriques pre/post neteja LEGACY (comparativa) | READ-ONLY | Master + probe + pla de neteja | Informe a `reports/` | ACTIU |
| `scripts/export_legacy_02.py` | Copia el master a `data/legacy/` sense modificar-lo | READ-ONLY del master | Master + `config.json` | `data/legacy/pielh_qa_master_YYYYMMDD.json` | UTILITAT |

---

## 8. Scripts de Normalització (ús crític)

| Script | Funció | Mode | Dry-run | Entrada | Sortida/Efecte | Backup | Estat |
|---|---|---|---|---|---|---|---|
| `scripts/normalize_sensor_ids.py` | Normalitza IDs de sensors al format `HOSXXX-SXX-NN`. Guarda l'ID original a `id_old`. Marca inactius duplicats com `Old-` | **MODIFICA MASTER** | **No té dry-run clar** | `pielh_qa_master.json` | Master actualitzat | Sí | **PELIGRÓS** — Revisar informe i fer backup manual abans d'executar |

---

## 9. Fluix HOS complet — ordre canònic d'execució

El fluix per resoldre i propagar la relació `sensor.hos → building.id` és:

```
FASE 1 — Detecció
python scripts/audit_sensors_without_hos.py
→ Genera: data/audits/sensors_without_hos_audit.json

FASE 2 — Revisió del pla (dry-run obligatori)
python scripts/apply_hos_assignments.py --dry-run
→ Revisa informe. Si tot OK:

FASE 3 — Aplicació HOS
python scripts/apply_hos_assignments.py --apply
→ Modifica master. Genera backup + informe a data/audits/

FASE 4 — Auditar herència
python scripts/audit_sensor_building_inheritance.py
→ Genera: reports/sensor_building_inheritance_report.json

FASE 5 — Propagació de camps (dry-run obligatori)
python scripts/apply_sensor_building_inheritance.py --dry-run
→ Revisa informe. Si tot OK:

FASE 6 — Aplicació herència
python scripts/apply_sensor_building_inheritance.py --apply
→ Modifica master. Genera backup + informe a data/audits/
```

**Camps propagats per `apply_hos_assignments.py`** (BUILDING_TO_SENSOR_FIELDS):
`district_code`, `district_name`, `neighborhood_key`, `neighborhood`, `type`, `zone`, `street_etra`

**Camps propagats per `apply_sensor_building_inheritance.py`** (ADMIN_FIELDS, superset):
`district_code`, `district_name`, `neighborhood_key`, `neighborhood`, `type`, `zone`, `street_etra`, `street_mti`, `lat`, `lon`

**Camps PROTEGITS** (mai es toquen):
`thing_id`, `thing_token`, `id`, `system_id`, `system_name`, `iot_health`, `raw`, `tags`, `has_data`, `status`, `sensor_order`, `cu_old`, `ref_etra`

---

## 10. Resum: scripts que modifiquen `pielh_qa_master.json`

| Script | Condició | Backup automàtic |
|---|---|---|
| `apply_hos_assignments.py` | Sempre (sense opció read-only) | Sí |
| `apply_sensor_building_inheritance.py` | Només amb `--apply` | Sí |
| `apply_inventory_health_to_master.py` | Sempre | Sí |
| `apply_high_confidence_legacy_marks.py` | Només amb `--apply` | Sí |
| `mark_old_duplicate_sensors.py` | Sempre | Sí |
| `dedupe_sensor_siblings.py` | Sempre (usa backup via server.py) | Sí |
| `normalize_sensor_ids.py` | Sempre — **sense dry-run clar** | Sí |
| `sync_thethings_tags.py` (--pull) | Amb `--pull` (sense `--dry-run`) | Sí |

> **Regla:** Qualsevol script que modifiqui el master **ha de fer backup previ**.
> Tots els scripts anteriors compleixen aquesta regla excepte `normalize_sensor_ids.py` que ha de ser revisat abans d'executar.

---

## 11. Scripts que criden l'API TheThings

| Script | Tipus de crida | Risc |
|---|---|---|
| `fetch_thethings_structure.py` | GET (lectura) | Baix |
| `discover_thethings_resources.py` | GET (lectura) | Baix |
| `audit_thethings_activity.py` | GET (lectura) | Baix |
| `sync_thethings_tags.py --pull` | GET (lectura) | Baix |
| `sync_thethings_tags.py --push` | PUT/POST (escriptura) | **ALT — modifica dades a TheThings** |

---

## 12. Informes generats (outputs a `reports/` i `data/audits/`)

| Fitxer | Generat per | Contingut |
|---|---|---|
| `reports/audit_duplicate_sensors.json` | `audit_duplicate_sensors.py` | Grups de sensors duplicats amb risc |
| `reports/duplicate_sensor_cleanup_plan.json` | `plan_duplicate_sensor_cleanup.py` | Pla de neteja (MARK_LEGACY/KEEP/REVIEW) |
| `reports/post_cleanup_audit.json` | `audit_post_cleanup.py` | Mètriques pre/post neteja |
| `reports/sensor_building_inheritance_report.json` | `audit_sensor_building_inheritance.py` | Herència edifici→sensor |
| `data/audits/sensors_without_hos_report.md` | `audit_sensors_without_hos.py` | Sensors sense HOS classificats |
| `data/audits/hos_assignments_applied.md` | `apply_hos_assignments.py` | Informe d'aplicació HOS |
| `data/audits/sensor_building_inheritance_report.md` | `audit_sensor_building_inheritance.py` | Herència (versió Markdown) |
| `data/audits/sensor_building_inheritance_applied.md` | `apply_sensor_building_inheritance.py` | Informe d'aplicació herència |
| `data/audits/inventory_health_report.md` | `build_inventory_health_report.py` | Salut inventari IoT |
