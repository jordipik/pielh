"""
PIELH — Rellena short_name de sensores con el patrón HOSAAA-SBB-CC.
Si el id no contiene ese patrón, short_name queda vacío.
Sobreescribe todos los sensores (normaliza valores previos incorrectos).
"""

import json
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def _backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime('%Y%m%d_%H%M%S')
    dst = backup_dir / f'pielh_qa_master_before_fill_sensor_short_name_{ts}.json'
    shutil.copy2(master_path, dst)
    backups = sorted(backup_dir.glob('pielh_qa_master_before_fill_sensor_short_name_*.json'))
    for old in backups[:-20]:
        old.unlink(missing_ok=True)
    return dst


def fill_short_names(master: dict, dry_run: bool = True) -> dict:
    sensors   = master.get('sensors', [])
    counters  = {}   # (hos, system_id) -> next order number
    set_ok    = 0
    set_blank = 0
    examples_ok    = []
    examples_blank = []

    for s in sensors:
        hos    = s.get('hos', '') or ''
        sys_id = s.get('system_id', '') or ''
        if not hos or not sys_id:
            new_name = ''
        else:
            key = (hos, sys_id)
            n   = counters.get(key, 0) + 1
            counters[key] = n
            new_name = f'{hos}-{sys_id}-{n:02d}'

        if not dry_run:
            s['short_name'] = new_name

        if new_name:
            set_ok += 1
            if len(examples_ok) < 5:
                examples_ok.append(f'{s.get("id")!r} -> {new_name!r}')
        else:
            set_blank += 1
            if len(examples_blank) < 10:
                examples_blank.append(repr(s.get('id')))

    return {
        'total':          len(sensors),
        'set_ok':         set_ok,
        'set_blank':      set_blank,
        'examples_ok':    examples_ok,
        'examples_blank': examples_blank,
    }


def main():
    parser = argparse.ArgumentParser(description='PIELH — fill sensor short_name')
    parser.add_argument('--master',  default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--apply',   action='store_true')
    args = parser.parse_args()

    dry_run = not args.apply

    base_dir    = Path(__file__).resolve().parent.parent
    master_path = Path(args.master) if args.master else base_dir / 'pielh_qa_master.json'
    backup_dir  = base_dir / 'data' / 'backups'

    print(f'[PIELH] Master: {master_path.name}')
    print(f'[PIELH] Modo: {"DRY-RUN" if dry_run else "APPLY"}')

    with open(master_path, encoding='utf-8') as f:
        master = json.load(f)

    backup_path = _backup(master_path, backup_dir)
    print(f'[PIELH] Backup: {backup_path.name}')

    result = fill_short_names(master, dry_run=dry_run)

    if not dry_run:
        with open(master_path, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        print('[PIELH] Master guardado.')

    print(f'\n  Total sensores:    {result["total"]}')
    print(f'  Con short_name:    {result["set_ok"]}')
    print(f'  Sin patrón (vacío):{result["set_blank"]}')
    if result['examples_ok']:
        print('  Muestra OK:')
        for ex in result['examples_ok']:
            print(f'    {ex}')
    if result['examples_blank']:
        print('  Sin patrón:')
        for ex in result['examples_blank']:
            print(f'    {ex}')


if __name__ == '__main__':
    main()
