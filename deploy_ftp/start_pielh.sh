#!/bin/bash
# Arrancar servidor PIELH QA en Linux

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PORT=$(python3 -c "import json; c=json.load(open('config.json')); print(c.get('port',8080))" 2>/dev/null || echo 8080)

echo "Iniciando PIELH QA en puerto $PORT..."
python3 server.py
