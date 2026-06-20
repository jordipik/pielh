# PIELH QA — Desplegament

## Requisits

| Requisit | Notes |
|---|---|
| Python 3.8+ | Sense dependències pip; stdlib only |
| Navegador modern | Chrome / Firefox / Edge |
| Accés a internet (opcional) | Per a Leaflet, Tabulator (CDN), i API thethings |

---

## Execució en local (Windows)

### Via script BAT

```bat
Ejecutar_PIELH_Localhost.bat
```

### Via línia de comandes

```bash
cd C:\Users\jordi\source\repos\pielh\pielh_v02
python server.py
```

El servidor obre automàticament el navegador a `http://localhost:8080` (delay de 1.5s).

---

## Execució en local (Linux/macOS)

```bash
cd /path/to/pielh_v02
python3 server.py
```

O usant l'script:
```bash
chmod +x start_pielh.sh
./start_pielh.sh
```

---

## Fitxers necessaris per funcionar

**Obligatoris:**
- `index.html`
- `app.js`
- `styles.css`
- `server.py`
- `config.json`
- `pielh_qa_master.json` (ha d'existir, pot ser `{}` per a una instal·lació nova)

**Opcionals (millorar l'experiència GIS):**
- `data/geojson/hospitalet_barris.geojson`
- `data/geojson/hospitalet_districtes.geojson`
- `data/geojson/hospitalet_boundary.geojson`
- Si no existeixen: cau en fallback de marcadors punt, sense error

**Creats automàticament:**
- `data/backups/` — en el primer guardado
- `logs/pielh.log` — en arrencar el servidor

---

## Desplegament en producció (servidor Linux)

### Pas 1: Generar la carpeta de desplegament

```bash
python build_deploy_ftp.py
```

Genera `deploy_ftp/` amb:
- `index.html`, `app.js`, `styles.css`, `server.py`, `config.json`
- `pielh_qa_master.json`
- `start_pielh.sh`
- `data/geojson/` (còpia)
- `data/backups/` (buit)
- `logs/` (buit)

### Pas 2: Pujar per FTP

Pujar el contingut de `deploy_ftp/` a `/var/www/pielh/` (o el path configurat).

Via FileZilla: pujar tot el directori al servidor remot.

### Pas 3: Configurar `config.json` al servidor

```json
{
  "json_file": "pielh_qa_master.json",
  "backup_dir": "data/backups",
  "log_file": "logs/pielh.log",
  "max_backups": 20,
  "host": "127.0.0.1",
  "port": 8080,
  "thethings_api": "https://api.smartpielh.l-h.cat",
  "thethings_token": "TOKEN_AQUI"
}
```

- `host`: `127.0.0.1` si hi ha Nginx davant (recomanat)
- `host`: `0.0.0.0` si s'exposa directament (no recomanat)

### Pas 4: Arrencar el servidor

```bash
cd /var/www/pielh
python3 server.py
```

Per a producció, arrencar com a procés persistent (systemd o screen/tmux):

```bash
# Amb screen:
screen -S pielh
python3 /var/www/pielh/server.py
# Ctrl+A, D per desconnectar

# Amb systemd (crear /etc/systemd/system/pielh.service):
[Unit]
Description=PIELH QA Server
After=network.target

[Service]
WorkingDirectory=/var/www/pielh
ExecStart=/usr/bin/python3 server.py
Restart=on-failure
User=www-data

[Install]
WantedBy=multi-user.target
```

### Pas 5: Nginx (reverse proxy — recomanat)

```nginx
server {
    server_name pielh.dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/pielh /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## Verificació post-desplegament

```bash
curl http://localhost:8080/api/health
```

Resposta esperada:
```json
{"status": "ok", "json_file": "ok", "backup_dir": "ok", "log_file": "ok"}
```

---

## Gestió de backups

**Verificació:**
```bash
ls -lah /var/www/pielh/data/backups/
```

**Restauració manual:**
```bash
cp data/backups/pielh_qa_master_20260618_103045.json pielh_qa_master.json
```

El servidor ha d'estar aturat o no ha d'haver guardades simultànies.

**Rotació:** Automàtica — el servidor manté els últims `max_backups` (defecte 20). Es pot canviar a `config.json`.

---

## Monitoratge de logs

```bash
tail -f /var/www/pielh/logs/pielh.log
```

Format de línia:
```
2026-06-12 10:20:59 | building | HOS001 | neighborhood_key | CENTRE -> COLLBLANC
```

---

## Importació inicial de dades

Si `pielh_qa_master.json` és buit o inexistent:

1. Crear un JSON mínim:
```json
{
  "buildings": [],
  "sensors": [],
  "other_objects": [],
  "catalogs": {
    "systems": [],
    "neighborhoods": [],
    "districts": []
  },
  "qa": {"findings": []}
}
```

2. Arrencar el servidor
3. Obrir l'app → clicar "⟳ Sincronizar" per importar des de thethings
4. Clicar "⚙ Resolver Tags" per omplir camps de catàleg

---

## Sense accés a internet (mode offline)

Si no hi ha accés a la CDN de Leaflet/Tabulator:
- Descarregar localment `leaflet.css`, `leaflet.js`, `tabulator.css`, `tabulator.js`
- Modificar les URLs als fitxers HTML de CDN a rutes locals

L'API thethings no serà accessible, però les dades locals (`pielh_qa_master.json`) es podran consultar i editar.

---

## `build_deploy_ftp.py` — detalls

**Fitxers copiats:**
```
index.html, app.js, styles.css, server.py, config.json,
pielh_qa_master.json, start_pielh.sh, README_DEPLOY.md
```

**Directoris creats buits:**
```
data/backups/, logs/
```

**Directoris copiats:**
```
data/geojson/ → data/geojson/
```

**Nota:** `qa_explorer.html`, `qa_explorer_app.js`, `modules/`, `qa_explorer_styles.css` **NO s'inclouen** en el deploy FTP actual (tal com es defineix a `build_deploy_ftp.py`).
