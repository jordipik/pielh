"""
PIELH - Export Legacy 02
Copia pielh_qa_master.json a data/legacy/ sin modificar el original.
Solo lectura. No modifica pielh_qa_master.json.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent.parent
    cfg_path = base_dir / "config.json"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    json_file = cfg.get("json_file", "pielh_qa_master.json")
    src = base_dir / json_file

    if not src.exists():
        print(f"[ERROR] No encontrado: {src}")
        return 1

    legacy_dir = base_dir / "data" / "legacy"
    legacy_dir.mkdir(parents=True, exist_ok=True)

    dst_fixed = legacy_dir / "pielh_qa_master_legacy_02.json"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst_ts = legacy_dir / f"pielh_qa_master_legacy_02_{ts}.json"

    shutil.copy2(src, dst_fixed)
    shutil.copy2(src, dst_ts)

    size = src.stat().st_size
    print(f"[OK] Legacy guardado:")
    print(f"     {dst_fixed}")
    print(f"     {dst_ts}")
    print(f"     Tamaño: {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
