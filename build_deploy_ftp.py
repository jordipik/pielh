#!/usr/bin/env python3
"""Genera carpeta deploy_ftp lista para subir por FileZilla."""

import os
import shutil
import stat
from pathlib import Path


def _rmtree_onerror(func, path, exc_info):
    """Maneja errores de permisos en Windows al borrar."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

ROOT   = Path(__file__).parent
DEST   = ROOT / 'deploy_ftp'

FILES = [
    'index.html',
    'app.js',
    'styles.css',
    'server.py',
    'config.json',
    'pielh_qa_master.json',
    'start_pielh.sh',
    'README_DEPLOY.md',
]

DIRS_TO_CREATE = [
    'data/backups',
    'logs',
]

DATA_DIRS = [
    ('data/geojson', 'data/geojson'),
]


def build():
    # Limpiar destino previo
    if DEST.exists():
        shutil.rmtree(DEST, onerror=_rmtree_onerror)
    DEST.mkdir()

    copied   = []
    skipped  = []
    errors   = []

    # Copiar archivos raíz
    for fname in FILES:
        src = ROOT / fname
        if src.exists():
            shutil.copy2(src, DEST / fname)
            copied.append(fname)
        else:
            skipped.append(f'{fname} (no encontrado)')

    # Copiar directorios de datos
    for src_rel, dst_rel in DATA_DIRS:
        src_dir = ROOT / src_rel
        dst_dir = DEST / dst_rel
        if src_dir.exists():
            shutil.copytree(src_dir, dst_dir)
            for f in src_dir.iterdir():
                copied.append(f'{dst_rel}/{f.name}')
        else:
            skipped.append(f'{src_rel}/ (no encontrado)')

    # Crear carpetas vacías necesarias
    for d in DIRS_TO_CREATE:
        (DEST / d).mkdir(parents=True, exist_ok=True)
        # Añadir .gitkeep para que no quede vacía en algunos sistemas
        keep = DEST / d / '.gitkeep'
        keep.touch()

    # Calcular tamaño total
    total_bytes = sum(f.stat().st_size for f in DEST.rglob('*') if f.is_file())
    total_kb = total_bytes / 1024

    # Resumen
    print('\n=== build_deploy_ftp ===\n')
    print(f'Destino: {DEST}')
    print(f'\nArchivos copiados ({len(copied)}):')
    for f in copied:
        print(f'  + {f}')
    if skipped:
        print(f'\nOmitidos ({len(skipped)}):')
        for f in skipped:
            print(f'  - {f}')
    if errors:
        print(f'\nErrores ({len(errors)}):')
        for e in errors:
            print(f'  ! {e}')
    print(f'\nTamaño total: {total_kb:.1f} KB')
    print(f'\nEstado: {"OK" if not errors else "ERRORES"}')
    print()


if __name__ == '__main__':
    build()
