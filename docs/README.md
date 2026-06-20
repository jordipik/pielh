# PIELH QA — Documentació Tècnica

Documentació generada el 2026-06-18 a partir de la lectura directa del codi font.

## Índex

| Document | Contingut |
|---|---|
| [PIELH_PROJECT_INVENTORY.md](PIELH_PROJECT_INVENTORY.md) | Inventari complet de fitxers, dependències i APIs externes |
| [PIELH_ARCHITECTURE.md](PIELH_ARCHITECTURE.md) | Arquitectura global: Frontend / Backend / Persistència |
| [PIELH_DATA_MODEL.md](PIELH_DATA_MODEL.md) | Model de dades de `pielh_qa_master.json` |
| [PIELH_GIS.md](PIELH_GIS.md) | Mapa Leaflet: capes, marcadors, interacció |
| [PIELH_UI.md](PIELH_UI.md) | Interfície d'usuari: pestanyes, taules, filtres, panells |
| [PIELH_FUNCTIONALITY.md](PIELH_FUNCTIONALITY.md) | Funcionalitats detallades amb fluxos i fitxers afectats |
| [PIELH_API.md](PIELH_API.md) | Endpoints de `server.py` |
| [PIELH_SAVE_PROCESS.md](PIELH_SAVE_PROCESS.md) | Flux complet de guardada de dades |
| [PIELH_DEPLOYMENT.md](PIELH_DEPLOYMENT.md) | Desplegament des de zero (local i producció) |
| [PIELH_STATUS.md](PIELH_STATUS.md) | Estat de cada funcionalitat: FUNCIONAL / PARCIAL / NO IMPLEMENTAT |

## Diagrames Mermaid

| Diagrama | Contingut |
|---|---|
| [diagrams/architecture.mmd](diagrams/architecture.mmd) | Arquitectura global |
| [diagrams/data_model.mmd](diagrams/data_model.mmd) | Model ER de les dades |
| [diagrams/save_flow.mmd](diagrams/save_flow.mmd) | Flux de guardada (seqüència) |
| [diagrams/map_flow.mmd](diagrams/map_flow.mmd) | Flux de renderitzat del mapa |
| [diagrams/ui_flow.mmd](diagrams/ui_flow.mmd) | Transicions d'estat de la UI |

## Visió general ràpida

**Projecte:** PIELH QA Dashboard — L'Hospitalet de Llobregat  
**Tipus:** Eina de gestió i QA d'actius IoT (edificis + sensors)  
**Stack:** HTML + CSS + JavaScript vanilla (Leaflet) / Python stdlib (servidor HTTP)  
**Dades:** `pielh_qa_master.json` (font de veritat única, JSON)  
**API externa:** `api.smartpielh.l-h.cat` (thethings IoT platform)
