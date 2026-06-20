#!/usr/bin/env python3
"""Limpieza única: completa campos vacíos entre sensores que comparten el
mismo `id` (hermanos), usando la misma lógica que server.py aplica ahora en
cada guardado. Nunca sobreescribe valores existentes; crea backup antes de
escribir."""

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import server as srv  # noqa: E402

handler = srv.Handler


def main():
    master = handler._load(None)

    groups = defaultdict(list)
    for s in master.get('sensors', []):
        groups[s.get('id')].append(s)

    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}
    print(f'Grupos con id repetido: {len(dup_groups)}')

    handler._backup(None)

    total_changes = 0
    for rid, siblings in dup_groups.items():
        before = [dict(r) for r in siblings]
        handler._complete_empty_fields(None, siblings)
        for old, new in zip(before, siblings):
            for field, new_val in new.items():
                if field == 'raw':
                    continue
                if old.get(field) != new_val:
                    srv._log_change('sensor', new.get('id'), field, old.get(field), new_val)
                    total_changes += 1

    handler._save(None, master)
    print(f'Campos completados: {total_changes}')


if __name__ == '__main__':
    main()
