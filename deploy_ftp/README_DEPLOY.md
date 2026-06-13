# PIELH QA — Deploy en servidor Linux

## Qué subir por FileZilla

Subir el contenido completo de `deploy_ftp/` al servidor.

Estructura resultante en el servidor:

```
/var/www/pielh/
├── index.html
├── app.js
├── styles.css
├── server.py
├── config.json
├── pielh_qa_master.json
├── data/
│   ├── geojson/
│   │   ├── hospitalet_barris.geojson
│   │   └── hospitalet_districtes.geojson
│   └── backups/
├── logs/
└── start_pielh.sh
```

## Dónde subir

Ruta recomendada: `/var/www/pielh/`

Ajustar `config.json` si se cambia la ruta.

## Arrancar el servidor

```bash
cd /var/www/pielh
python3 server.py
```

O usando el script de arranque:

```bash
chmod +x start_pielh.sh
./start_pielh.sh
```

El servidor escucha en el puerto definido en `config.json` (por defecto: 8080).

## Comprobar que funciona

```
http://IP:8080/api/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "json_file": "ok",
  "backup_dir": "ok",
  "log_file": "ok"
}
```

## Ver logs en tiempo real

```bash
tail -f logs/pielh.log
```

Formato de cada línea:

```
2026-06-12 18:34:10 | sensor | S04-001 | neighborhood_key | CENTRE -> COLLBLANC
```

## Revisar backups

```bash
ls -lah data/backups/
```

Se generan automáticamente con cada guardado. Máximo 20 (configurable en `config.json`).

## config.json

```json
{
  "json_file": "pielh_qa_master.json",
  "backup_dir": "data/backups",
  "log_file": "logs/pielh.log",
  "max_backups": 20,
  "host": "127.0.0.1",
  "port": 8080
}
```

Cambiar `host` a `0.0.0.0` solo si el servidor no está detrás de un proxy.

---

## Configuración Nginx (reverse proxy)

Si el servidor está detrás de Nginx, crear `/etc/nginx/sites-available/pielh`:

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

Activar y recargar:

```bash
ln -s /etc/nginx/sites-available/pielh /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

Con esta configuración, dejar `host` en `127.0.0.1` en `config.json`.
